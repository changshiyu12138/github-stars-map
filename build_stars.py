# -*- coding: utf-8 -*-
"""把 stars_raw.json 解析成结构化的 stars.json，并校验分类映射完整性。

用法：
    python build_stars.py
前置：
    gh api -H "Accept: application/vnd.github.star+json" --paginate \
       "user/starred?per_page=100" > stars_raw.json
"""
import json, os, sys, collections

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import map as M

RAW = os.path.join(BASE, 'stars_raw.json')
OUT = os.path.join(BASE, 'stars.json')

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
json.dump(rows, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print(f'stars.json 已生成：{len(rows)} 个项目')

# ---- 校验分类映射 ----
real = {r['full'] for r in rows}
missing = sorted(real - set(M.NOTES))
extra = sorted(set(M.NOTES) - real)
if missing:
    print(f'\n⚠️  map.py 缺少 {len(missing)} 个项目的分类与说明：')
    for k in missing:
        print('  -', k)
if extra:
    print(f'\n⚠️  map.py 中有 {len(extra)} 个键不在 Star 列表里（可能已改名或取消 Star）：')
    for k in extra:
        print('  -', k)
if not missing and not extra:
    print('✅ 分类映射完整，覆盖 100%')

# ---- 统计 ----
no_desc = [r['full'] for r in rows if not r['desc']]
print(f'\n官方无简介：{len(no_desc)} 个 -> {"、".join(no_desc)}')
c = collections.Counter(v[0] for v in M.NOTES.values() if v[0] in real)
print('\n分类分布：')
for k, (name, emo) in M.CATS.items():
    if c[k]:
        print(f'  {c[k]:3d}  {emo} {name}')