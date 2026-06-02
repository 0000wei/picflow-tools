import os
import re
import json
from pathlib import Path

# English FAQ patterns to search for
faq_patterns = [
    "Is image processing secure",
    "What image formats",
    "Is there a file size limit",
    "Can I process multiple images",
    "How do I convert",
    "What is the difference between",
    "Does this tool",
    "Will my images be",
    "Can I use this",
    "Is it free",
    "How to",
    "What happens to",
    "Are my images",
    "Is there a limit"
]

# Common FAQ section headers
faq_headers = [
    "Frequently Asked Questions",
    "FAQ",
    "اسئلة",
    "preguntas",
    "questions",
    "fréquentes",
    "よくある質問",
    "perguntas frequentes",
    "常见问题"
]

def check_file_for_english(file_path):
    """Check a file for English FAQ patterns in HTML and JSON-LD"""
    results = {
        'file_path': str(file_path),
        'html_has_english': False,
        'jsonld_has_english': False,
        'sample_text': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for visible HTML FAQ section
        for header in faq_headers:
            # Look for FAQ section with header
            faq_pattern = re.compile(
                rf'<(?:section|div)[^>]*>.*?{re.escape(header)}.*?</(?:section|div)>',
                re.IGNORECASE | re.DOTALL
            )
            faq_match = faq_pattern.search(content)
            if faq_match:
                faq_content = faq_match.group(0)
                
                # Check for English text in this section
                for pattern in faq_patterns:
                    if pattern.lower() in faq_content.lower():
                        results['html_has_english'] = True
                        if pattern not in results['sample_text']:
                            results['sample_text'].append(pattern)
                        break
                break
                
        # Check for JSON-LD structured data
        jsonld_matches = re.findall(
            r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
            content,
            re.DOTALL
        )
        
        for jsonld_content in jsonld_matches:
            # Check if it's FAQPage type
            if '"FAQPage"' in jsonld_content or '"@type": "FAQPage"' in jsonld_content:
                for pattern in faq_patterns:
                    if pattern.lower() in jsonld_content.lower():
                        results['jsonld_has_english'] = True
                        if pattern not in results['sample_text']:
                            results['sample_text'].append(pattern)
                        break
                        
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return results

# Main scan
languages = ['ar', 'de', 'es', 'fr', 'ja', 'pt', 'zh']
all_results = []

print("=== COMPREHENSIVE UNTRANSLATED FAQ SCAN ===")
print()

for lang in languages:
    lang_dir = Path(f'./{lang}')
    if lang_dir.exists():
        print(f"\n--- Scanning {lang.upper()} directory ---")
        
        # Find all index.html files
        html_files = list(lang_dir.rglob('index.html'))
        print(f"Found {len(html_files)} index.html files")
        
        lang_results = []
        for file_path in html_files:
            result = check_file_for_english(file_path)
            if result['html_has_english'] or result['jsonld_has_english']:
                lang_results.append(result)
                all_results.append(result)
                
        print(f"Files with untranslated FAQs in {lang}: {len(lang_results)}")

# Print detailed results
print("\n" + "="*80)
print("DETAILED RESULTS:")
print("="*80)

for result in sorted(all_results, key=lambda x: x['file_path']):
    # Extract language from path
    path_parts = result['file_path'].split(os.sep)
    lang = path_parts[1] if len(path_parts) > 1 else 'unknown'
    rel_path = os.sep.join(path_parts[2:])
    
    print(f"\nLanguage: {lang.upper()}")
    print(f"File: {rel_path}")
    print(f"English in HTML: {'YES' if result['html_has_english'] else 'NO'}")
    print(f"English in JSON-LD: {'YES' if result['jsonld_has_english'] else 'NO'}")
    if result['sample_text']:
        print(f"Sample English text: {', '.join(result['sample_text'][:3])}")
    print("-" * 80)

print(f"\n\nSUMMARY:")
print(f"Total files with untranslated FAQs: {len(all_results)}")
print(f"Languages affected: {len(set(r['file_path'].split(os.sep)[1] for r in all_results))}")

# Group by language
lang_summary = {}
for result in all_results:
    path_parts = result['file_path'].split(os.sep)
    lang = path_parts[1] if len(path_parts) > 1 else 'unknown'
    if lang not in lang_summary:
        lang_summary[lang] = []
    lang_summary[lang].append(result)

print("\nBreakdown by language:")
for lang, files in sorted(lang_summary.items()):
    print(f"\n{lang.upper()}: {len(files)} files")
    
    # Show specific files for this language
    for file_result in files:
        path_parts = file_result['file_path'].split(os.sep)
        rel_path = os.sep.join(path_parts[2:])
        print(f"  - {rel_path}")
        if file_result['html_has_english'] and file_result['jsonld_has_english']:
            print("    (English in both HTML and JSON-LD)")
        elif file_result['html_has_english']:
            print("    (English in HTML only)")
        elif file_result['jsonld_has_english']:
            print("    (English in JSON-LD only)")
