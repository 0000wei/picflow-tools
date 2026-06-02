"""Extract all unique FAQ Q&A pairs from English root pages, then check which
language pages need them translated."""
import os, re, json, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
LANGS = ['ar', 'de', 'es', 'fr', 'ja', 'pt', 'zh']

def extract_faqs(filepath):
    """Extract FAQ questions and answers from an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    html_faqs = []
    # Match <details><summary class="faq-question">Q</summary><p class="faq-answer">A</p></details>
    for m in re.finditer(
        r'<summary\s+class="faq-question"[^>]*>(.*?)</summary>\s*'
        r'<p\s+class="faq-answer"[^>]*>(.*?)</p>',
        content, re.DOTALL
    ):
        q = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        a = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        html_faqs.append({'q': q, 'a': a})

    jsonld_faqs = []
    for match in re.finditer(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', content, re.DOTALL):
        try:
            data = json.loads(match.group(1))
            items = []
            if isinstance(data, dict):
                if data.get('@type') == 'FAQPage':
                    items = data.get('mainEntity', [])
                elif '@graph' in data:
                    for g in data['@graph']:
                        if isinstance(g, dict) and g.get('@type') == 'FAQPage':
                            items = g.get('mainEntity', [])
            for item in items:
                jsonld_faqs.append({
                    'q': item.get('name', ''),
                    'a': item.get('acceptedAnswer', {}).get('text', '')
                })
        except json.JSONDecodeError:
            pass

    return html_faqs, jsonld_faqs

def is_truly_english(text):
    """More precise English detection - check for English-specific words."""
    en_markers = [
        ' the ', ' is ', ' are ', ' can ', ' will ', ' our ', ' your ',
        ' this ', ' that ', ' with ', ' from ', ' into ', ' about ',
        'All processing', 'All compression', 'Our tool', 'Our compressor',
        'Your images', 'never leave', 'guarantees', 'No. All',
        'Yes!', 'Yes,', 'Most images', 'absolutely',
    ]
    lower = text.lower()
    count = sum(1 for m in en_markers if m.lower() in lower)
    return count >= 2  # At least 2 English markers = truly English

# Step 1: Collect all unique FAQ pairs from English root pages
print("Step 1: Collecting unique English FAQ pairs from root pages...")
en_faqs_by_tool = {}
for root_dir in os.listdir(BASE):
    dirpath = os.path.join(BASE, root_dir)
    if not os.path.isdir(dirpath):
        continue
    idx = os.path.join(dirpath, 'index.html')
    if not os.path.isfile(idx):
        continue
    # Skip language dirs
    if root_dir in LANGS:
        continue
    html_faqs, _ = extract_faqs(idx)
    if html_faqs:
        en_faqs_by_tool[root_dir] = html_faqs

print(f"Found {len(en_faqs_by_tool)} English tool pages with FAQs")

# Step 2: Check each language page for untranslated FAQs
print("\nStep 2: Scanning language pages for untranslated FAQs...")
report = {}
for lang in LANGS:
    lang_dir = os.path.join(BASE, lang)
    if not os.path.isdir(lang_dir):
        continue
    lang_issues = []
    for tool_dir in os.listdir(lang_dir):
        tool_path = os.path.join(lang_dir, tool_dir)
        if not os.path.isdir(tool_path):
            continue
        idx = os.path.join(tool_path, 'index.html')
        if not os.path.isfile(idx):
            continue
        html_faqs, jsonld_faqs = extract_faqs(idx)
        if not html_faqs:
            continue

        # Check each FAQ
        en_html = [f for f in html_faqs if is_truly_english(f['q'] + ' ' + f['a'])]
        en_jsonld = [f for f in jsonld_faqs if is_truly_english(f['q'] + ' ' + f['a'])]

        if en_html or en_jsonld:
            relpath = os.path.relpath(idx, BASE).replace('\\', '/')
            lang_issues.append({
                'file': relpath,
                'en_html': len(en_html),
                'total_html': len(html_faqs),
                'en_jsonld': len(en_jsonld),
                'total_jsonld': len(jsonld_faqs),
                'questions': [{'q': f['q'][:60], 'a': f['a'][:60]} for f in en_html[:3]],
            })

    if lang_issues:
        report[lang] = lang_issues

# Step 3: Report
print("\n" + "=" * 80)
print("UNTRANSLATED FAQ REPORT (precise detection)")
print("=" * 80)

grand_total = 0
for lang, issues in sorted(report.items()):
    total_files = len(issues)
    grand_total += total_files
    print(f"\n## {lang.upper()} — {total_files} files")
    for i in issues:
        status = f"HTML:{i['en_html']}/{i['total_html']} JSON-LD:{i['en_jsonld']}/{i['total_jsonld']}"
        print(f"  {i['file']}  [{status}]")
        for q in i['questions'][:2]:
            print(f"    Q: {q['q'].encode('ascii','replace').decode()}")

print(f"\n{'=' * 80}")
print(f"TOTAL: {grand_total} files across {len(report)} languages")
print(f"Affected languages: {', '.join(sorted(report.keys())).upper()}")
ok_langs = set(LANGS) - set(report.keys())
if ok_langs:
    print(f"Clean languages: {', '.join(sorted(ok_langs)).upper()}")

# Step 4: Collect all unique English Q&A pairs that need translation
print(f"\n{'=' * 80}")
print("UNIQUE ENGLISH FAQ PAIRS REQUIRING TRANSLATION:")
print("=" * 80)
seen = set()
unique_pairs = []
for lang, issues in sorted(report.items()):
    for i in issues:
        fpath = os.path.join(BASE, i['file'])
        html_faqs, _ = extract_faqs(fpath)
        for faq in html_faqs:
            if is_truly_english(faq['q'] + ' ' + faq['a']):
                key = faq['q']
                if key not in seen:
                    seen.add(key)
                    unique_pairs.append(faq)

for idx, pair in enumerate(unique_pairs, 1):
    q = pair['q'].encode('ascii', 'replace').decode()
    a = pair['a'][:120].encode('ascii', 'replace').decode()
    print(f"\n{idx}. Q: {q}")
    print(f"   A: {a}...")

print(f"\nTotal unique FAQ pairs: {len(unique_pairs)}")

# Save as JSON for the translation script
out_path = os.path.join(BASE, 'untranslated_faqs_report.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({
        'total_files': grand_total,
        'languages': {lang: [{'file': i['file'], 'en_html': i['en_html'], 'total_html': i['total_html']} for i in issues] for lang, issues in report.items()},
        'unique_pairs': unique_pairs,
    }, f, ensure_ascii=False, indent=2)
print(f"\nFull report saved to: untranslated_faqs_report.json")
