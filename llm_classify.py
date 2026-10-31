# -*- coding: utf-8 -*-
"""用在线大模型给新 Star 项目自动分类并写中文说明。

背景：
  规则引擎（classifier.py）精确率 100%，但覆盖率约 81%——剩下 19%
  是它"判定不了"的边界项目，以前只能丢进待归类等人工。
  LLM 能读懂描述语义，处理这些边界情况，并写出比「概念重组」自然得多的中文说明。

架构：多provider 通用（都走 OpenAI 兼容协议）
  1. GitHub Models   —— 零配置，用 Actions 内置 GITHUB_TOKEN + models: read 权限，不花钱
  2. DeepSeek / Kimi / 智谱 / 通义 —— 需要自备 API key，但便宜甚至有免费额度
  按顺序尝试，第一个可用的就用；也可用 LLM_PROVIDER 环境变量指定。

关键设计（都是踩过的坑换来的）：
  1. **输出必须受约束**：只允许模型从 15 个固定分类里选，并要求 JSON 输出。
     分类错了比不分类更糟，所以要校验；校验不过直接丢弃。
  2. **必须缓存**：结果写进 map_auto.py，同一项目永不重复调用。
     这解决了 LLM 非确定性导致的 git diff 抖动，也省额度。
  3. **必须优雅降级**：限流/网络故障/输出不合法时，自动退回规则引擎，
     再不行才进待归类。任何情况下都不让流水线断掉。
  4. **不能信任端点**：曾遇到 models.github.ai 对任何请求都返回 text/plain 的 "OK"，
     所以必须校验响应确实是 JSON 且含 choices，否则视为该provider 不可用。

用法：
    python llm_classify.py
环境变量：
    LLM_PROVIDER        可选，强制指定 provider 名
    GITHUB_TOKEN        GitHub Models 用（Actions 内置令牌）
    DEEPSEEK_API_KEY / MOONSHOT_API_KEY / ZHIPU_API_KEY / DASHSCOPE_API_KEY
"""

import json, os, re, sys, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import map as M
import classifier as C

PENDING = os.path.join(BASE, 'stars_pending.json')
AUTO_OUT = os.path.join(BASE, 'map_auto.py')

# (名称, base_url, 模型, api_key 环境变量)
PROVIDERS = [
    ('github-models', 'https://models.github.ai/inference', 'openai/gpt-4o-mini', 'GITHUB_TOKEN'),
    ('deepseek',      'https://api.deepseek.com/v1',              'deepseek-chat',     'DEEPSEEK_API_KEY'),
    ('kimi',          'https://api.moonshot.cn/v1',                'moonshot-v1-8k',   'MOONSHOT_API_KEY'),
    ('zhipu',         'https://open.bigmodel.cn/api/paas/v4',      'glm-4-flash',      'ZHIPU_API_KEY'),
    ('qwen',          'https://dashscope.aliyuncs.com/compatible-mode/v1', 'qwen-plus', 'DASHSCOPE_API_KEY'),
]

# 备用模型：主模型不可用时依次尝试
FALLBACK_MODELS = {
    'github-models': ['openai/gpt-4o-mini', 'microsoft/Phi-4-mini-instruct',
                      'meta/Llama-3.3-70B-Instruct'],
    'deepseek':      ['deepseek-chat'],
    'kimi':          ['moonshot-v1-8k', 'moonshot-v1-32k'],
    'zhipu':         ['glm-4-flash', 'glm-4-plus'],
    'qwen':          ['qwen-plus', 'qwen-turbo'],
}

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


def call_model(repo, base_url, model, key):
    """调用一次 OpenAI 兼容接口，返回解析后的 dict。

    失败抛异常。注意：必须确认响应真的是 JSON 且含 choices——
    曾遇到端点对任何请求都返回 text/plain 的 "OK"，那种要当失败处理。
    """
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
        base_url.rstrip('/') + '/chat/completions',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        ctype = resp.headers.get('Content-Type', '')
        raw = resp.read().decode('utf-8', errors='replace')
    # 端点占位符检测：返回的不是 JSON JSON 会直接抛错
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f'响应不是 JSON（Content-Type={ctype}）：{raw[:80]}')
    if 'choices' not in body:
        raise ValueError(f'响应缺少 choices 字段：{str(body)[:120]}')
    return parse_json(body['choices'][0]['message']['content'])


def parse_json(text):
    """从模型输出里抠出 JSON。模型有时会包 markdown 代码块或加前后缀。"""
    text = text.strip()
    m = re.search(r'```(?:json)?\s*(.+?)\s*```', text, re.S)
    if m:
        text = m.group(1).strip()
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
    if conf == 'low':
        return None          # low 置信度不采用，交给规则引擎
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


def pick_providers():
    """选出可用 provider：有 key 才算可用，按优先级排序。

    LLM_BASE_URL 指定时视为「自定义端点」，只用这一个，
    配合 LLM_API_KEY / LLM_MODEL 使用（测试或自建代理场景）。
    否则按内置优先级列表，取第一个有 key 的 provider。
    """
    base_override = os.environ.get('LLM_BASE_URL', '').strip()
    if base_override:
        key = os.environ.get('LLM_API_KEY', '').strip()
        if not key:
            return []
        model = os.environ.get('LLM_MODEL', 'gpt-4o-mini').strip()
        return [('custom', base_override, model, 'LLM_API_KEY', key)]

    forced = os.environ.get('LLM_PROVIDER')
    out = []
    for name, base, model, env in PROVIDERS:
        if forced and name != forced:
            continue
        key = os.environ.get(env, '').strip()
        if not key:
            continue
        out.append((name, base, os.environ.get('LLM_MODEL', '').strip() or model, env, key))
    return out


def prune_cache(cache, keep):
    """移除已不在 Star 列表里的缓存项。

    keep: 本次解决的项目名集合（即使不在 star 列表里也要保留）
    """
    try:
        stars = json.load(open(os.path.join(BASE, 'stars.json'), encoding='utf-8'))
        alive = {r['full'] for r in stars}
        return {k: v for k, v in cache.items() if k in alive or k in keep}
    except Exception:
        return cache


def main():
    if not os.path.exists(PENDING):
        print('没有待处理项目')
        return 0
    pending = json.load(open(PENDING, encoding='utf-8'))
    cache = load_cache()

    todo = [p for p in pending if p['full'] not in cache]
    hit = len(pending) - len(todo)
    if hit:
        print(f'命中缓存 {hit} 个，跳过调用')

    if not todo:
        # 即使没有新项目也要清理缓存：用户可能取消了 Star，
        # 不清理的话 map_auto.py 会残留已不在列表里的项目。
        cache = prune_cache(cache, set())
        write_cache(cache)
        json.dump([], open(PENDING, 'w', encoding='utf-8'), ensure_ascii=False)
        print('没有需要处理的新项目')
        return 0

    providers = pick_providers()
    if not providers:
        print('⚠️ 没有可用的 provider（缺 API key 或端点不可用），仅用规则引擎')
    else:
        print(f'🤖 可用 provider: {", ".join(p[0] for p in providers)}，待处理 {len(todo)} 个')

    llm_ok = llm_fail = 0
    used_provider = None
    dead_providers = set()
    fail_streak = {}      # provider -> 连续「传输故障」次数

    for p in todo:
        got = None
        for name, base, model, env, key in providers:
            if name in dead_providers:
                continue
            if used_provider and name != used_provider:
                break
            transport_err = False
            for mdl in FALLBACK_MODELS.get(name, [model]):
                try:
                    raw = call_model(p, base, mdl, key)
                except urllib.error.HTTPError as e:
                    if e.code == 429:
                        print('  ⚠️ 触发限流 (429)，停止调用，剩余转规则引擎')
                        dead_providers.add(name)
                        transport_err = True
                        break
                    llm_fail += 1
                    transport_err = True
                    continue
                except Exception as e:
                    llm_fail += 1
                    transport_err = True
                    if llm_fail <= 2:
                        print(f'  · {name}/{mdl} 调用失败: {type(e).__name__}: {str(e)[:90]}')
                    continue

                # 拿到响应后做校验——校验不通过说明「这个项目本身有歧义」，
                # 不是 provider 的问题，不该触发熔断
                v = validate(raw)
                if v:
                    got = v
                    used_provider = used_provider or name
                    llm_ok += 1
                    fail_streak[name] = 0
                    break
                llm_fail += 1

            if got:
                break
            # 只有连续传输故障才判定 provider 不可用（避免单次抖动误杀）
            if transport_err:
                fail_streak[name] = fail_streak.get(name, 0) + 1
                if fail_streak[name] >= 2:
                    dead_providers.add(name)

        if got:
            cache[p['full']] = got
            print(f'  ✓ {p["full"]}  → {got[0]}  | {got[1][:36]}')
        else:
            cat, score, second, s2 = C.classify(p, p['full'])
            if cat and score >= C.STRONG:
                desc = C.auto_description(p, cat)
                cache[p['full']] = (cat, desc)
                print(f'  ↩ {p["full"]}  → {cat} (规则兜底, score={score}) | {desc[:36]}')
            else:
                print(f'  ? {p["full"]}  仍需人工确认')

    # 清理缓存：移除已不在 Star 列表里的项目，但保留本次解决的
    resolved = set(cache) & {p['full'] for p in pending}
    cache = prune_cache(cache, resolved)

    write_cache(cache)

    still = [p for p in pending if p['full'] not in resolved]
    json.dump(still, open(PENDING, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print(f'\nLLM 成功 {llm_ok}，失败 {llm_fail}；剩余待人工 {len(still)} 个')
    return 0


if __name__ == '__main__':
    sys.exit(main())
