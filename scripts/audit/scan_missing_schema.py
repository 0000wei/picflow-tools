#!/usr/bin/env python3
"""Scan multi-language tool pages for missing JSON-LD structured data."""

import os, re, json, sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(root)

skip_dirs = {'zh','ja','de','fr','es','pt','ar','css','js','images','config','docs','scripts','seo','.git','__pycache__','.well-known'}

en_tools = sorted(d for d in os.listdir('.') 
    if os.path.isdir(d) and os.path.isfile(os.path.join(d, 'index.html'))
    and d not in skip_dirs)

results = {}
for lang in ['zh','ja','de','fr','es','pt','ar']:
    lang_missing = {}
    for tool in en_tools:
        idx = os.path.join(lang, tool, 'index.html')
        if not os.path.isfile(idx):
            continue
        with open(idx) as f:
            c = f.read()
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
        types = []
        for b in blocks:
            try:
                data = json.loads(b)
                types.append(data.get('@type','?'))
            except:
                types.append('INVALID')
        if len(types) < 2:
            lang_missing[tool] = ('ZERO' if len(types)==0 else f'PARTIAL({len(types)})', types)
    if lang_missing:
        results[lang] = lang_missing

# FAQPage coverage
faq_missing = []
for tool in en_tools:
    with open(f'{tool}/index.html') as f:
        c = f.read()
    if 'FAQPage' not in c:
        faq_missing.append(tool)

# hreflang
hreflang_status = {}
for lang in ['zh','ja','de','fr','es','pt','ar']:
    for tool in en_tools:
        idx = os.path.join(lang, tool, 'index.html')
        if os.path.isfile(idx):
            with open(idx) as f:
                c = f.read()
            h = c.count('hreflang')
            if h == 0:
                hreflang_status.setdefault(lang, []).append(tool)

# Output
print("=" * 78)
print("  多语言工具页 JSON-LD 缺失扫瞄报告")
print("=" * 78)

if not results:
    print("\n  ✅ 所有语言工具页 JSON-LD >= 2 块，无需修复")
else:
    for lang in sorted(results.keys()):
        missing = results[lang]
        zero = {k:v for k,v in missing.items() if v[0] == 'ZERO'}
        partial = {k:v for k,v in missing.items() if v[0].startswith('PARTIAL')}
        print(f"\n  【{lang}】—— {len(missing)} 个工具需修复")
        if zero:
            print(f"    ZERO JSON-LD ({len(zero)}):")
            for t in sorted(zero.keys()):
                print(f"      ✗ {t}")
        if partial:
            print(f"    PARTIAL ({len(partial)}):")
            for t, (s, types) in sorted(partial.items()):
                print(f"      ⚠ {t} (has: {types})")

print(f"\n\n---")
print(f"  英文工具缺 FAQPage: {len(faq_missing)} 个")
for t in faq_missing:
    print(f"    - {t}")

print(f"\n---")
print(f"  多语言工具页缺 hreflang: {sum(len(v) for v in hreflang_status.values())} 个")
for lang in sorted(hreflang_status.keys()):
    print(f"    {lang}: {len(hreflang_status[lang])} pages")
    for t in sorted(hreflang_status[lang])[:5]:
        print(f"      - {t}")
    if len(hreflang_status[lang]) > 5:
        print(f"      ... and {len(hreflang_status[lang])-5} more")

print(f"\n---")
sys.exit(0 if not results else 1)
