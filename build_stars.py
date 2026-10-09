# -*- coding: utf-8 -*-
"""把 stars_raw.json 解析成结构化的 stars.json，并报告分类映射缺口。

用法：
    python build_stars.py
前置：
    gh api -H "Accept: application/vnd.github.star+json" --paginate \
       "user/starred?per_page=100" > stars_raw.json

设计要点（配合每6 小时的自动监控）：
  - 新出现的 Star 不会导致脚本崩溃。未在 map.py 中登记的项目会被归入
    PENDING_CAT 占位分类，并在 stars_pending.json 中单独列出，
    等人工补写中文说明后再归位。
  - 退出码：0 = 映射完整；2 = 存在待补充项目（供 CI 判断是否需要通知）。
"""
import json, os, sys, collections

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import map as M

RAW = os.path.join(BASE, 'stars_raw.json')
OUT = os.path.join(BASE, 'stars.json')
PENDING = os.path.join(BASE, 'stars_pending.json')

# 未登记项目的占位分类
PENDING_CAT = 'pending'

raw = json.load(open(RAW, encoding='utf-8'))

rows = []
for item in raw:
    r = item['repo']
    rows.append({
        'full': r['full_name'],
        'url': r['html_url'],
        'desc': (r.get('description') or '').strip(),
        'lang': r.get('language') or '未标注',
        'stars': r.get('stargazers_count', 0),
        'topics': r.get('topics', []),
        'at': item['starred_at'][:10],
        'fork': r.get('fork', False),
        'archived': r.get('archived', False),
    })
rows.sort(key=lambda x: x['at'])

# ---- 与旧数据对比，找出新增 Star ----
old_full = set()
if os.path.exists(OUT):
    try:
        old_full = {r['full'] for r in json.load(open(OUT, encoding='utf-8'))}
    except Exception:
        pass
newly_starred = [r['full'] for r in rows if r['full'] not in old_full]

real = {r['full'] for r in rows}
missing = sorted(real - set(M.NOTES))       # 新 Star 但没写说明
extra = sorted(set(M.NOTES) - real)          # 取消 Star 或改名了

# 待补充清单：保留足够信息，便于人工补写说明
pending = []
for full in missing:
    r = next(x for x in rows if x['full'] == full)
    pending.append({
        'full': r['full'], 'url': r['url'], 'lang': r['lang'],
        'stars': r['stars'], 'topics': r['topics'], 'at': r['at'],
        'desc': r['desc'],
    })
json.dump(pending, open(PENDING, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 把待补充项目也写入 stars.json，标注为待归类，保证 README 不会漏掉它们
for r in rows:
    r['pending'] = r['full'] in missing

json.dump(rows, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print(f'stars.json 已生成：{len(rows)} 个项目')
if newly_starred:
    print(f'\n🆕 本次新增 {len(newly_starred)} 个 Star：')
    for f in newly_starred:
        print(f'   + {f}')
else:
    print('\n本次无新增 Star')

if missing:
    print(f'\n⚠️  map.py 缺少 {len(missing)} 个项目的分类与说明（已记入 stars_pending.json）：')
    for p in pending:
        print(f'  - {p["full"]}  [{p["lang"]}]  {p["desc"][:50]}')
else:
    print('\n✅ 分类映射完整，覆盖 100%')

if extra:
    print(f'\nℹ️  map.py 中有 {len(extra)} 个键不在 Star 列表里（可能已改名或取消 Star）：')
    for k in extra:
        print(f'  - {k}')

no_desc = [r['full'] for r in rows if not r['desc']]
print(f'\n官方无简介：{len(no_desc)} 个')

c = collections.Counter(v[0] for v in M.NOTES.values() if v[0] in real)
print('\n分类分布：')
for k, (name, emo) in M.CATS.items():
    if c[k]:
        print(f'  {c[k]:3d}  {emo} {name}')

sys.exit(2 if missing else 0)
