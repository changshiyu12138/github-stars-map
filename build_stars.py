# -*- coding: utf-8 -*-
"""把 stars_raw.json 解析成结构化的 stars.json，并报告分类映射缺口。

用法：
    python build_stars.py
前置：
    gh api -H "Accept: application/vnd.github.star+json" --paginate \
       "user/starred?per_page=100" > stars_raw.json

设计要点（配合每6 小时的自动监控）：
  - 新出现的 Star 不会导致脚本崩溃。未在 map.py 中登记的项目会被标记
    pending=True，并在 stars_pending.json 中单独列出，等人工补写中文说明后再归位。
  - 活跃度：使用 API 自带的 pushed_at（最后一次代码推送）判断项目死活，
    无需额外请求。分档为 active / recent / stale / dormant / archived。
  - 退出码：0 = 映射完整；2 = 存在待补充项目（供 CI 判断是否需要通知）。
"""
import json, os, sys, collections, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import map as M

RAW = os.path.join(BASE, 'stars_raw.json')
OUT = os.path.join(BASE, 'stars.json')
PENDING = os.path.join(BASE, 'stars_pending.json')
AUTO_OUT = os.path.join(BASE, 'map_auto.py')

TODAY = datetime.date.today()


def activity_level(pushed_at, archived):
    """按最后推送时间判断项目活跃度。归档项目仍返回距今天数，便于展示。"""
    days = None
    if pushed_at:
        days = (TODAY - datetime.date.fromisoformat(pushed_at[:10])).days
    if archived:
        return 'archived', days
    if days is None:
        return 'unknown', None
    if days <= 90:
        return 'active', days
    if days <= 365:
        return 'recent', days
    if days <= 730:
        return 'stale', days
    return 'dormant', days


LEVEL_CN = {
    'active':   '活跃',
    'recent':   '近期',
    'stale':    '半休眠',
    'dormant':  '长期停更',
    'archived': '已归档',
    'unknown':  '未知',
}

raw = json.load(open(RAW, encoding='utf-8'))

rows = []
for item in raw:
    r = item['repo']
    archived = bool(r.get('archived'))
    pushed = r.get('pushed_at')
    level, days = activity_level(pushed, archived)
    rows.append({
        'full': r['full_name'],
        'url': r['html_url'],
        'desc': (r.get('description') or '').strip(),
        'lang': r.get('language') or '未标注',
        'stars': r.get('stargazers_count', 0),
        'topics': r.get('topics', []),
        'at': item['starred_at'][:10],
        'created': (r.get('created_at') or '')[:10],
        'pushed': (pushed or '')[:10],
        'idle_days': days,
        'level': level,
        'archived': archived,
        'fork': r.get('fork', False),
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

# ---- 本步骤只负责「找出还没归类的项目」 ----
# 具体分类交给后续的 llm_classify.py（LLM 优先，规则引擎兜底），
# 分类结果缓存在 map_auto.py，避免重复调用 LLM。
pending = []
for full in missing:
    r = next(x for x in rows if x['full'] == full)
    pending.append({
        'full': r['full'], 'url': r['url'], 'lang': r['lang'],
        'stars': r['stars'], 'topics': r['topics'], 'at': r['at'],
        'desc': r['desc'],
    })
json.dump(pending, open(PENDING, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 标记状态：auto / pending 由 map_auto.py 与 stars_pending.json 决定
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location('map_auto_cache', AUTO_OUT)
    if os.path.exists(AUTO_OUT):
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        auto_set = set(getattr(mod, 'AUTO_NOTES', {}))
    else:
        auto_set = set()
except Exception:
    auto_set = set()
pend_set = {p['full'] for p in pending}
for r in rows:
    r['auto'] = r['full'] in auto_set
    r['pending'] = r['full'] in pend_set and r['full'] not in auto_set

json.dump(rows, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print(f'stars.json 已生成：{len(rows)} 个项目')
if newly_starred:
    print(f'\n🆕 本次新增 {len(newly_starred)} 个 Star：')
    for f in newly_starred:
        print(f'   + {f}')
else:
    print('\n本次无新增 Star')

print(f'\n待分类项目：{len(pending)} 个（交由 llm_classify.py 处理）')
for p in pending:
    print(f'  ? {p["full"]}  [{p["lang"]}]')

if extra:
    print(f'\nℹ️  map.py 中有 {len(extra)} 个键不在 Star 列表里（可能已改名或取消 Star）：')
    for k in extra:
        print(f'  - {k}')

no_desc = [r['full'] for r in rows if not r['desc']]
print(f'\n官方无简介：{len(no_desc)} 个')

print('\n活跃度分布（按最后一次代码推送）：')
lev = collections.Counter(r['level'] for r in rows)
for k in ['active', 'recent', 'stale', 'dormant', 'archived', 'unknown']:
    if lev[k]:
        print(f'  {lev[k]:3d}  {LEVEL_CN[k]}')

c = collections.Counter(v[0] for v in M.NOTES.values() if v[0] in real)
print('\n分类分布：')
for k, (name, emo) in M.CATS.items():
    if c[k]:
        print(f'  {c[k]:3d}  {emo} {name}')

sys.exit(2 if missing else 0)
