# -*- coding: utf-8 -*-
"""生成 Star 地图 README.md"""
import json, collections, datetime, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import map as M

rows = json.load(open(os.path.join(BASE, 'stars.json'), encoding='utf-8'))
today = datetime.date.today().isoformat()

# 活跃度徽章：以「最后一次代码推送」为准
LEVEL = {
    'active':   ('🟢', '活跃',     '90 天内有提交'),
    'recent':   ('🔵', '近期',     '半年到一年内'),
    'stale':    ('🟡', '半休眠',   '1–2 年未更新'),
    'dormant':  ('🔴', '长期停更', '超过 2 年没动'),
    'archived': ('⚫', '已归档',   '作者已停止维护'),
    'unknown':  ('⚪', '未知',     '无推送记录'),
}
LEVEL_ORDER = ['active', 'recent', 'stale', 'dormant', 'archived', 'unknown']

def badge(r):
    return LEVEL.get(r.get('level', 'unknown'), LEVEL['unknown'])[0]

def last_push(r):
    """把最后推送日期渲染成紧凑形式。"""
    p = r.get('pushed')
    if not p:
        return '—'
    return p

# 分类顺序与元信息（可加副标题）
CAT_META = {
    "ai-agent":      "真正在做事的东西 —— 工作流、Agent 循环、Skills 生态",
    "ai-infra":      "模型本身的训练、推理与 API 接入层",
    "finance":       "A股、加密货币与量化投研的全部工具箱",
    "reading":       "电子书阅读器、书库管理与本地化",
    "rss-news":      "信息获取：订阅源、热点聚合与舆情监控",
    "crawl-browser": "给 Agent 喂数据的抓取与浏览器自动化",
    "tools":         "日常真正会打开的小工具",
    "mobile":        "安卓与移动端开发，含 Smartisan 情怀项目",
    "media":         "Jellyfin 家庭媒体、字幕与电视盒子",
    "system":        "硬件、系统与嵌入式，含大量 Smartisan OS 遗产",
    "frontend":      "网页与前端",
    "learning":      "教程、书籍与 Awesome Lists",
    "games":         "游戏与模拟器",
    "security":      "隐私、安全与逆向工程",
    "life":          "健身、做饭、副业与人生指南",
}

groups = collections.defaultdict(list)
pending = []
auto_count = 0

# 合并人工分类与自动分类
# 注意：自动分类结果在 llm_classify.py 里产生，晚于 build_stars.py，
# 所以这里直接读文件算归属，不依赖 stars.json 里的标记（那会过期）。
ALL_NOTES = dict(M.NOTES)
auto_set = set()
PENDING_PATH = os.path.join(BASE, 'stars_pending.json')
AUTO_PATH = os.path.join(BASE, 'map_auto.py')
try:
    import importlib.util
    if os.path.exists(AUTO_PATH):
        spec = importlib.util.spec_from_file_location('map_auto_read', AUTO_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ALL_NOTES.update(mod.AUTO_NOTES)
        auto_set = set(mod.AUTO_NOTES)
except Exception:
    pass

# 真正仍未归类的项目（llm_classify.py 处理后剩下的）
pending_full = set()
try:
    if os.path.exists(PENDING_PATH):
        pending_full = {p['full'] for p in json.load(open(PENDING_PATH, encoding='utf-8'))}
except Exception:
    pass

for r in rows:
    if r['full'] in pending_full:
        pending.append(r)
        continue
    if r['full'] not in ALL_NOTES:
        # 理论上不会发生（build 已保证），兜底放进 pending
        pending.append(r)
        continue
    cat, note = ALL_NOTES[r['full']]
    r['cat'], r['note'] = cat, note
    if r['full'] in auto_set:
        auto_count += 1
    groups[cat].append(r)

# 语言分布（排除未标注）
langs = collections.Counter(r['lang'] for r in rows if r['lang'] != '未标注')
# 年份分布
years = collections.Counter(r['at'][:4] for r in rows)
# 高星项目（>= 30k），排除待归类
hot = sorted((r for r in rows if r['stars'] >= 30000 and not r.get('pending')),
             key=lambda x: -x['stars'])
# 活跃度分布
levels = collections.Counter(r.get('level', 'unknown') for r in rows)
live = levels['active'] + levels['recent']
dead = levels['dormant'] + levels['archived']

out = []
w = out.append

w("# 🗂️ 我的 GitHub Star 地图")
w("")
w(f"> 收录 **{len(rows)}** 个 Star 过的项目，按主题分类并逐个补上中文说明。  ")
w(f"> 数据来源：GitHub API（`changshiyu12138` 的公开 Star 列表）· 最后更新 {today}  ")
w("> 🤖 由 GitHub Actions 每 6 小时自动刷新。新项目会自动归类；置信度不足的才出现在文末「🆕 待归类」。")
w("")
w("这个仓库的用途只有一个：**过三个月再想起来某个项目是干嘛的时候，这里能查到。**")
w("")

# ---- 概览 ----
w("## 概览")
w("")
w(f"- **总收藏**：{len(rows)} 个项目")
w(f"- **时间跨度**：{min(r['at'] for r in rows)} → {max(r['at'] for r in rows)}")
top_years = sorted(years.items(), key=lambda x: -x[1])[:2]
w(f"- **收藏高峰**：{ '、'.join(f'{y} 年 {c} 个' for y, c in top_years)}（占总量 {sum(c for _, c in top_years)*100//len(rows)}%）")
w(f"- **主力语言**：{ '、'.join(f'{k} {v}' for k, v in langs.most_common(5))}")
w(f"- **分类数量**：{len([c for c in M.CATS if groups[c]])} 个主题")
w(f"- **项目存活**：{live} 个半年内仍有提交（{live*100//len(rows)}%），{dead} 个已停更或归档")
if pending:
    w(f"- **🆕 待归类**：{len(pending)} 个新项目置信度不足，需人工确认（见文末）")
if auto_count:
    w(f"- **🤖 自动分类**：{auto_count} 个项目由规则引擎自动归类（说明前带 🤖 标记）")
w("")

# 年份柱状图
w("### 收藏节奏")
w("")
w("```")
maxy = max(years.values())
for y in sorted(years):
    n = years[y]
    bar = "█" * max(1, round(n / maxy * 40))
    w(f"{y}  {bar} {n}")
w("```")
w("")

# 活跃度总览
w("### 项目存活情况")
w("")
w("以仓库**最后一次代码推送**（`pushed_at`）为准，不是 Star 数——星多不代表还在维护。")
w("")
w("| | 状态 | 判定 | 数量 | 占比 |")
w("|---|---|---|---:|---:|")
for k in LEVEL_ORDER:
    if not levels[k]:
        continue
    emo, cn, desc = LEVEL[k]
    w(f"| {emo} | {cn} | {desc} | {levels[k]} | {levels[k]*100//len(rows)}% |")
w("")
bar_parts = []
for k in LEVEL_ORDER:
    if not levels[k]:
        continue
    bar_parts.append(f"{LEVEL[k][0]} {levels[k]}")
w("```")
w(" ".join(bar_parts))
w("```")
w("")

# 主题目录
w("### 主题目录")
w("")
w("| | 主题 | 数量 | 存活 | 一句话概括 |")
w("|---|---|---:|---:|---|")
for c in M.CATS:
    if not groups.get(c):
        continue
    name, emo = M.CATS[c]
    g = groups[c]
    alive = sum(1 for r in g if r.get('level') in ('active', 'recent'))
    w(f"| {emo} | [{name}](#cat-{c}) | {len(g)} | {alive}/{len(g)} | {CAT_META.get(c,'')} |")
w("")

# ---- 待归类区块 ----
if pending:
    w("---")
    w("")
    w(f"## 🆕 待归类 · {len(pending)}")
    w("")
    w("> 这些新项目**规则引擎判定不了**（信号不足或多个分类打平），所以没有硬猜。")
    w("> 补写方式：编辑 `map.py`，加一行 `\"owner/repo\": (\"分类\", \"中文说明\"),` 后重跑 `gen_readme.py`。")
    w("")
    w("| 项目 | 官方简介 | 状态 | 最后提交 | 语言 | ⭐ | 收藏于 |")
    w("|---|---|---|---|---|---:|---|")
    for r in sorted(pending, key=lambda x: x['at'], reverse=True):
        desc = (r['desc'] or '（官方无简介）').replace('|', '｜')
        w(f"| [`{r['full']}`]({r['url']}) | {desc} | {badge(r)} | {last_push(r)} | {r['lang']} | {r['stars']:,} | {r['at']} |")
    w("")

# ---- 各分类详情 ----
w("---")
w("")
w("## 📚 项目清单")
w("")
w("> 排序：各分类内按 Star 时间倒序，最新的在最前面。⭐ 为该项目当前的总 Star 数。")
w("> 说明前带 🤖 的是自动分类的（规则判定，非人工撰写），分类可信、措辞需自行核对。")
w("")

for c in M.CATS:
    if not groups.get(c):
        continue
    name, emo = M.CATS[c]
    items = sorted(groups[c], key=lambda x: (x['at'], x['stars']), reverse=True)
    w(f"<a id=\"cat-{c}\"></a>")
    w("")
    w(f"### {emo} {name} · {len(items)}")
    w("")
    w(f"> {CAT_META.get(c,'')}")
    w("")
    w("| 项目 | 说明 | 状态 | 最后提交 | 语言 | ⭐ | 收藏于 |")
    w("|---|---|---|---|---|---:|---|")
    for r in items:
        note = r['note'].replace('|', '｜')
        mark = '🤖 ' if r.get('auto') else ''
        w(f"| [`{r['full']}`]({r['url']}) | {mark}{note} | {badge(r)} | {last_push(r)} | {r['lang']} | {r['stars']:,} | {r['at']} |")
    w("")

# ---- 高星项目 ----
w("---")
w("")
w("## ⭐ 万星以上的项目")
w("")
w("这些是Star 列表里体量最大的 10 个，Star 数远高于其他项目。")
w("")
w("| 项目 | 说明 | 状态 | ⭐ |")
w("|---|---|---|---:|")
for r in hot[:10]:
    w(f"| [`{r['full']}`]({r['url']}) | {r['note']} | {badge(r)} | {r['stars']:,} |")
w("")

# ---- 停更项目提醒 ----
dying = sorted((r for r in rows if r.get('level') in ('dormant', 'archived')),
               key=lambda x: (x.get('pushed') or ''))
if dying:
    w("---")
    w("")
    w(f"## 🪦 停更与归档 · {len(dying)}")
    w("")
    w("这些项目超过两年没有提交，或已被作者正式归档。**方案类项目要留意**：")
    w("上游一旦停更，你迟早得自己接手修 bug。")
    w("")
    w("| 项目 | 说明 | 最后提交 | 距今 | 语言 | ⭐ |")
    w("|---|---|---|---|---|---:|")
    for r in dying:
        if r.get('level') == 'archived':
            gap = '⚫ 已归档'
        elif r.get('idle_days'):
            gap = f"{r['idle_days']//365} 年 {r['idle_days']%365} 天"
        else:
            gap = '—'
        w(f"| [`{r['full']}`]({r['url']}) | {r['note']} | {last_push(r)} | {gap} | {r['lang']} | {r['stars']:,} |")
    w("")

# ---- 标签索引 ----
w("---")
w("")
w("## 🏷️ 标签索引")
w("")
w("按 GitHub 官方 Topic 检索（点击即搜索）：")
w("")
topic_cnt = collections.Counter(t for r in rows for t in r['topics'])
seen, chips = set(), []
for t, n in topic_cnt.most_common(40):
    if t in seen:
        continue
    seen.add(t)
    chips.append(f"[`{t}`](https://github.com/topics/{t})")
w(" · ".join(chips))
w("")

# ---- 语言分布 ----
w("---")
w("")
w("## 📊 语言分布")
w("")
w("| 语言 | 数量 | 占比 |")
w("|---|---:|---:|")
for k, v in langs.most_common():
    w(f"| {k} | {v} | {v*100/len(rows):.0f}% |")
w("")

# ---- 说明 ----
w("---")
w("")
w("## 📌 关于这个仓库")
w("")
w("- 数据来自 GitHub 官方 REST API 的 `/users/changshiyu12138/starred`，`starred_at` 为真实收藏时间。")
w("- **状态判定**基于仓库的 `pushed_at`（最后一次代码推送），由 API 随 Star 列表一并返回，无额外请求。")
w("  注意 `updated_at` 含义不同——它包含改描述、改设置等任何改动，会让已停更项目看起来还活着。")
w("- 说明分两种：")
w("  - **人工撰写**（无标记）：最初 193 个项目由人工逐个判定并撰写。")
w("  - **🤖 自动生成**：新项目由 `classifier.py` 规则引擎自动归类并重组官方 topics 拼出中文说明。")
w("    分类可信（回测精确率 100%），但措辞是机器拼的，不如人工撰写自然。")
w("- 分类依据项目实际功能而非仓库作者，个别归类带主观判断。")
w("- **每 6 小时自动刷新**：GitHub Actions 定时拉取 Star 列表，重新生成 README 并提交。")
w("  新项目由规则引擎自动归类；只有置信度不足的才进「🆕 待归类」等人工确认。")
w("")
w("### 状态图例")
w("")
w("| | 状态 | 含义 |")
w("|---|---|---|")
for k in LEVEL_ORDER:
    emo, cn, desc = LEVEL[k]
    w(f"| {emo} | {cn} | 最后一次提交在{desc}内 |")
w("")
w("### 本地重新生成")
w("")
w("```bash")
w("# 1. 拉取全部 Star（需要 gh 已登录）")
w("gh api -H \"Accept: application/vnd.github.star+json\" --paginate \"user/starred?per_page=100\" > stars_raw.json")
w("")
w("# 2. 生成 stars.json（退出码 2 表示有新项目待归类）")
w("python build_stars.py")
w("")
w("# 3. 重新渲染 README（分类与说明维护在 map.py）")
w("python gen_readme.py")
w("```")
w("")

readme = "\n".join(out)
open(os.path.join(BASE, 'README.md'), 'w', encoding='utf-8').write(readme)
print(f"README.md 已生成：{len(readme)} 字符，{readme.count(chr(10))} 行")