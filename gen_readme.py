# -*- coding: utf-8 -*-
"""生成 Star 地图 README.md"""
import json, collections, datetime, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import map as M

rows = json.load(open(os.path.join(BASE, 'stars.json'), encoding='utf-8'))
today = datetime.date.today().isoformat()

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
for r in rows:
    if r.get('pending'):
        # 新增但尚未在 map.py 登记的项目，单独收集，不丢数据
        pending.append(r)
        continue
    cat, note = M.NOTES[r['full']]
    r['cat'], r['note'] = cat, note
    groups[cat].append(r)

# 语言分布（排除未标注）
langs = collections.Counter(r['lang'] for r in rows if r['lang'] != '未标注')
# 年份分布
years = collections.Counter(r['at'][:4] for r in rows)
# 高星项目（>= 30k），排除待归类
hot = sorted((r for r in rows if r['stars'] >= 30000 and not r.get('pending')),
             key=lambda x: -x['stars'])

out = []
w = out.append

w("# 🗂️ 我的 GitHub Star 地图")
w("")
w(f"> 收录 **{len(rows)}** 个 Star 过的项目，按主题分类并逐个补上中文说明。  ")
w(f"> 数据来源：GitHub API（`changshiyu12138` 的公开 Star 列表）· 最后更新 {today}  ")
w("> 🤖 由 GitHub Actions 每 6 小时自动刷新，新项目会出现在文末「🆕 待归类」。")
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
if pending:
    w(f"- **🆕 待归类**：{len(pending)} 个新项目尚未补写说明（见文末）")
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

# 主题目录
w("### 主题目录")
w("")
w("| | 主题 | 数量 | 一句话概括 |")
w("|---|---|---:|---|")
for c in M.CATS:
    if not groups.get(c):
        continue
    name, emo = M.CATS[c]
    w(f"| {emo} | [{name}](#cat-{c}) | {len(groups[c])} | {CAT_META.get(c,'')} |")
w("")

# ---- 待归类区块 ----
if pending:
    w("---")
    w("")
    w(f"## 🆕 待归类 · {len(pending)}")
    w("")
    w("> 自动监控发现的新Star 项目，还缺人工撰写的中文说明与分类。")
    w("> 补写方式：编辑 `map.py`，加一行 `\"owner/repo\": (\"分类\", \"中文说明\"),` 后重跑 `gen_readme.py`。")
    w("")
    w("| 项目 | 官方简介 | 语言 | ⭐ | 收藏于 |")
    w("|---|---|---|---:|---|")
    for r in sorted(pending, key=lambda x: x['at'], reverse=True):
        desc = (r['desc'] or '（官方无简介）').replace('|', '｜')
        w(f"| [`{r['full']}`]({r['url']}) | {desc} | {r['lang']} | {r['stars']:,} | {r['at']} |")
    w("")

# ---- 各分类详情 ----
w("---")
w("")
w("## 📚 项目清单")
w("")
w("> 排序：各分类内按 Star 时间倒序，最新的在最前面。⭐ 为该项目当前的总 Star 数。")
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
    w("| 项目 | 说明 | 语言 | ⭐ | 收藏于 |")
    w("|---|---|---|---:|---|")
    for r in items:
        note = r['note'].replace('|', '｜')
        w(f"| [`{r['full']}`]({r['url']}) | {note} | {r['lang']} | {r['stars']:,} | {r['at']} |")
    w("")

# ---- 高星项目 ----
w("---")
w("")
w("## ⭐ 万星以上的项目")
w("")
w("这些是Star 列表里体量最大的 10 个，Star 数远高于其他项目。")
w("")
w("| 项目 | 说明 | ⭐ |")
w("|---|---|---:|")
for r in hot[:10]:
    w(f"| [`{r['full']}`]({r['url']}) | {r['note']} | {r['stars']:,} |")
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
w("- 数据来自 GitHub 官方 REST API 的 `/user/starred` 接口，`starred_at` 为真实收藏时间。")
w("- 所有中文说明为人工撰写，非机器翻译；少数仓库官方无简介，已按项目内容补写并标注。")
w("- 分类依据项目实际功能而非仓库作者，个别归类带主观判断。")
w("- **每 6 小时自动刷新**：GitHub Actions 定时拉取 Star 列表，重新生成 README 并提交。")
w("  新项目会先落进「🆕 待归类」，等补写中文说明后归入对应分类。")
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