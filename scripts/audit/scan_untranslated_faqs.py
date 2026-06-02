"""Scan all language subdirectories for untranslated (English) FAQ content."""
import os
import re
import json

BASE = os.path.dirname(os.path.abspath(__file__))
LANGS = ['ar', 'de', 'es', 'fr', 'ja', 'pt', 'zh']

# English FAQ patterns - if a faq-question starts with these, it's untranslated
EN_PATTERNS = [
    r'^[A-Z][a-z]+\s',  # Starts with capitalized English word
    r'^How\s', r'^What\s', r'^Is\s', r'^Can\s', r'^Does\s',
    r'^Will\s', r'^Are\s', r'^Why\s', r'^Do\s', r'^Which\s',
]

def get_faq_questions(content):
    """Extract FAQ question texts from HTML."""
    return re.findall(r'class="faq-question"[^>]*>(.*?)</summary>', content, re.DOTALL)

def get_jsonld_faqs(content):
    """Extract FAQ Q&A from JSON-LD blocks."""
    faqs = []
    for match in re.finditer(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', content, re.DOTALL):
        try:
            data = json.loads(match.group(1))
            if isinstance(data, dict):
                # Could be FAQPage directly or have @graph
                items = []
                if data.get('@type') == 'FAQPage':
                    items = data.get('mainEntity', [])
                elif '@graph' in data:
                    for g in data['@graph']:
                        if isinstance(g, dict) and g.get('@type') == 'FAQPage':
                            items = g.get('mainEntity', [])
                for item in items:
                    name = item.get('name', '')
                    text = item.get('acceptedAnswer', {}).get('text', '')
                    faqs.append({'q': name, 'a': text})
        except json.JSONDecodeError:
            pass
    return faqs

def is_english(text):
    """Check if text appears to be English."""
    text = text.strip()
    if not text:
        return False
    for pat in EN_PATTERNS:
        if re.match(pat, text):
            return True
    return False

results = {}
for lang in LANGS:
    lang_dir = os.path.join(BASE, lang)
    if not os.path.isdir(lang_dir):
        continue
    lang_results = []
    for root, dirs, files in os.walk(lang_dir):
        for f in files:
            if f != 'index.html':
                continue
            fpath = os.path.join(root, f)
            relpath = os.path.relpath(fpath, BASE)
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()

            html_faqs = get_faq_questions(content)
            jsonld_faqs = get_jsonld_faqs(content)

            en_html = [q for q in html_faqs if is_english(q)]
            en_jsonld = [f for f in jsonld_faqs if is_english(f['q'])]

            if en_html or en_jsonld:
                lang_results.append({
                    'file': relpath.replace('\\', '/'),
                    'en_html_count': len(en_html),
                    'total_html': len(html_faqs),
                    'en_jsonld_count': len(en_jsonld),
                    'total_jsonld': len(jsonld_faqs),
                    'sample_en_html': en_html[:2],
                    'sample_en_jsonld': [f['q'] for f in en_jsonld[:2]],
                })

    if lang_results:
        results[lang] = lang_results

# Report
total = 0
print("=" * 80)
print("UNTRANSLATED FAQ SCAN REPORT")
print("=" * 80)

for lang, files in sorted(results.items()):
    print(f"\n## {lang.upper()} — {len(files)} files affected")
    for f in files:
        total += 1
        html_status = f"HTML: {f['en_html_count']}/{f['total_html']} EN"
        jsonld_status = f"JSON-LD: {f['en_jsonld_count']}/{f['total_jsonld']} EN"
        print(f"  {f['file']}")
        print(f"    {html_status} | {jsonld_status}")
        if f['sample_en_html']:
            print(f"    Sample HTML: {f['sample_en_html'][0][:80]}".encode('ascii', 'replace').decode())
        if f['sample_en_jsonld']:
            print(f"    Sample JSON-LD: {f['sample_en_jsonld'][0][:80]}".encode('ascii', 'replace').decode())

print(f"\n{'=' * 80}")
print(f"TOTAL: {total} files need FAQ translation")
print(f"Languages affected: {', '.join(sorted(results.keys())).upper()}")
print(f"Languages OK: {', '.join(sorted(set(LANGS) - set(results.keys()))).upper()}")
