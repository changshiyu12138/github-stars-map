# -*- coding: utf-8 -*-
"""用 GitHub Models（免费额度）给新 Star 项目自动分类并写中文说明。

为什么需要它：
  规则引擎（classifier.py）精确率 100%，但覆盖率约 81%——剩下 19%
  是它"判定不了"的边界项目，以前只能丢进待归类等人工。
  LLM 可以读懂描述语义，处理这些边界情况，并且写出比
  「概念重组」自然得多的中文说明。

关键设计（都是踩过的坑换来的）：
  1. **零配置**：Actions 里用内置 GITHUB_TOKEN + `models: read` 权限，
     不需要任何外部 API key，不花钱。
  2. **输出必须受约束**：只允许模型从 15 个固定分类里选，
     并要求 JSON 输出。分类错了比不分类更糟，所以要校验。
  3. **必须缓存**：结果写进 map_auto.py，同一项目永不重复调用。
     这解决了 LLM 非确定性导致的 git diff 抖动，也省额度。
  4. **必须优雅降级**：限流/网络故障/输出不合法时，自动退回规则引擎，
     再不行才进待归类。任何情况下都不让流水线断掉。

用法（在 Actions 里）：
    python llm_classify.py
环境变量：
    GITHUB_TOKEN   Actions 内置令牌（需 models: read 权限）
    GITHUB_MODELS_MODEL  可选，指定模型，默认 openai/gpt-4o-mini
"""

import json, os, re, sys, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import map as M
import classifier as C

PENDING = os.path.join(BASE, 'stars_pending.json')
AUTO_OUT = os.path.join(BASE, 'map_auto.py')

ENDPOINT = 'https://models.github.ai/inference/chat/completions'
MODEL = os.environ.get('GITHUB_MODELS_MODEL', 'openai/gpt-4o-mini')
# 备用模型：主模型不可用时依次尝试
FALLBACK_MODELS = ['openai/gpt-4o-mini', 'microsoft/Phi-4-mini-instruct',
                   'meta/Llama-3.3-70B-Instruct']

CATEGORY_HINTS = {
    'ai-agent': 'AI 智能体、Agent 工作流、Skills、MCP、编码助手',
    'ai-infra': '大模型训练/推理/部署、模型 API 网关、图像语音生成',
    'finance': '股票、量化投资、加密货币交易、金融数据分析',
    'reading': '电子书阅读器、书库管理、漫画小说、有声书',
    'rss-news': 'RSS 订阅、新闻聚合、热点与舆情监控',
    'crawl-browser': '网页爬虫、浏览器自动化、数据抓取',
    'tools': '实用小工具、效率软件、桌面应用、下载器、格式转换',
    'mobile': 'Android/iOS/Flutter 移动端开发与 App',
    'media': '影音媒体：Jellyfin 家庭媒体、字幕、播放器、电视直播',
    'system': '硬件、嵌入式、固件、操作系统、IoT 设备',
    'frontend': '网页前端：CSS、框架、静态站点',
    'learning': '学习资料：教程、书籍、面试指南、Awesome 清单',
    'games': '游戏开发、游戏引擎、模拟器、游戏素材',
    'security': '安全隐私：加密、代理、渗透、逆向、反检测浏览器',
    'life': '生活：健康健身、菜谱、副业、个人成长指南',
}

SYSTEM_PROMPT = """你是一个 GitHub 项目分类助手。用户会给你一个仓库的信息，
你需要从给定的固定分类列表中选出**唯一一个**最合适的分类，并写一句中文说明。

分类列表（category 字段只能填这些值之一）：
{categories}

要求：
1. category 必须是上面列表中的一个英文 key，不确定时选最接近的，不要编造新分类。
2. summary 用中文写一句话，不超过 30 个字，说明这个项目**是干什么的**。
   要具体，不要套话，例如"把网页转成 Markdown 的命令行工具"而不是"一个工具"。
3. confidence 取 high / medium / low：
   - high：分类非常明确
   - medium：大致对，但存在其他合理解释
   - low：真的看不出来

只输出 JSON，不要任何解释文字。格式：
{{"category": "<key>", "summary": "<中文说明>", "confidence": "high|medium|low"}}"""


def build_user_prompt(repo):
    topics = ', '.join(repo.get('topics') or []) or '(无)'
    desc = repo.get('desc') or '(官方无简介)'
    name = repo.get('full') or ''
    return f"仓库：{name}\n官方简介：{desc}\nTopics：{topics}"


def call_model(repo, token, model):
    """调用一次 GitHub Models，返回解析后的 dict，失败抛异常。"""
    cats = '\n'.join(f'  - {k}: {v}' for k, v in CATEGORY_HINTS.items())
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT.format(categories=cats)},
            {'role': 'user', 'content': build_user_prompt(repo)},
        ],
        'temperature': 0,
        'max_tokens': 300,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = json.loads(resp.read().decode('utf-8'))
    content = body['choices'][0]['message']['content']
    return parse_json(content)


def parse_json(text):
    """从模型输出里抠出 JSON。模型有时会包 markdown 代码块或加前后缀。"""
    text = text.strip()
    # 去掉 ```json ... ``` 包裹
    m = re.search(r'```(?:json)?\s*(.+?)\s*```', text, re.S)
    if m:
        text = m.group(1).strip()
    # 直接找最外层 {...}
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1:
        raise ValueError(f'输出中没有 JSON: {text[:120]}')
    return json.loads(text[start:end + 1])


def validate(result):
    """校验模型输出。不合法返回 None。"""
    if not isinstance(result, dict):
        return None
    cat = (result.get('category') or '').strip()
    summary = (result.get('summary') or '').strip()
    conf = (result.get('confidence') or 'medium').strip().lower()
    if cat not in CATEGORY_HINTS:
        return None
    if not summary:
        return None
    if len(summary) > 60:
        summary = summary[:58] + '…'
    if conf not in ('high', 'medium', 'low'):
        conf = 'medium'
    # low 置信度不采用，交给规则引擎
    if conf == 'low':
        return None
    return cat, summary


def load_cache():
    """读取已有的 map_auto.py 缓存。"""
    if not os.path.exists(AUTO_OUT):
        return {}
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location('map_auto_cache', AUTO_OUT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return dict(getattr(mod, 'AUTO_NOTES', {}))
    except Exception:
        return {}


def write_cache(cache):
    with open(AUTO_OUT, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('# 由 llm_classify.py / classifier.py 自动生成，勿手工编辑。\n')
        f.write('# 人工补充请写在 map.py。\n')
        f.write('AUTO_NOTES = {\n')
        for full, (cat, desc) in sorted(cache.items()):
            esc = desc.replace('\\', '\\\\').replace('"', '\\"')
            f.write(f'    "{full}": ("{cat}", "{esc}"),\n')
        f.write('}\n')


def main():
    if not os.path.exists(PENDING):
        print('没有待处理项目')
        return 0
    pending = json.load(open(PENDING, encoding='utf-8'))
    if not pending:
        print('没有待处理项目')
        write_cache({})
        return 0

    token = os.environ.get('GITHUB_TOKEN', '')
    cache = load_cache()

    # 只处理还没缓存过的
    todo = [p for p in pending if p['full'] not in cache]
    cached_hit = len(pending) - len(todo)
    if cached_hit:
        print(f'命中缓存 {cached_hit} 个，跳过 LLM 调用')

    if not todo:
        write_cache(cache)
        return 0

    if not token:
        print('⚠️ 无 GITHUB_TOKEN，跳过 LLM，仅用规则引擎')
    else:
        print(f'🤖 调用 {MODEL} 处理 {len(todo)} 个项目...')

    llm_ok = 0
    llm_fail = 0
    used_model = None

    for p in todo:
        got = None
        if token:
            for model in ([MODEL] if used_model else FALLBACK_MODELS):
                try:
                    res = call_model(p, token, model)
                    v = validate(res)
                    if v:
                        got = v
                        used_model = used_model or model
                        llm_ok += 1
                        break
                    # 输出不合法：换下一个模型
                    llm_fail += 1
                except urllib.error.HTTPError as e:
                    if e.code == 429:
                        print(f'  ⚠️ 触发限流 (429)，停止 LLM 调用，剩余转规则引擎')
                        break
                    llm_fail += 1
                except Exception as e:
                    llm_fail += 1
                    last_err = e
            else:
                pass

        if got:
            cache[p['full']] = got
            print(f'  ✓ {p["full"]}  → {got[0]}  | {got[1][:36]}')
        else:
            # LLM 失败/限流 → 退回规则引擎
            cat, score, second, s2 = C.classify(p, p['full'])
            if cat and score >= C.STRONG:
                desc = C.auto_description(p, cat)
                cache[p['full']] = (cat, desc)
                print(f'  ↩ {p["full"]}  → {cat} (规则兜底, score={score}) | {desc[:36]}')
            else:
                print(f'  ? {p["full"]}  仍需人工确认')

    # 清理缓存：移除已不在 Star 列表里的项目（取消 Star 或改名）
    # 注意不要在这里动 pending 的判定依据——刚解决的项目要先记账
    resolved = set(cache) & {p['full'] for p in pending}
    try:
        stars = json.load(open(os.path.join(BASE, 'stars.json'), encoding='utf-8'))
        alive = {r['full'] for r in stars}
        cache = {k: v for k, v in cache.items() if k in alive or k in resolved}
    except Exception:
        pass

    write_cache(cache)

    # 重写 pending：只剩真正解决不了的
    still = [p for p in pending if p['full'] not in resolved]
    json.dump(still, open(PENDING, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print(f'\nLLM 成功 {llm_ok}，失败 {llm_fail}；剩余待人工 {len(still)} 个')
    return 0


if __name__ == '__main__':
    sys.exit(main())
