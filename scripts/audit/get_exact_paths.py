import os
import re
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

def check_file_for_english(file_path):
    """Check a file for English FAQ patterns"""
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
        for header in ["Frequently Asked Questions", "FAQ", "اسئلة", "preguntas", "questions", "fréquentes", "よくある質問", "perguntas frequentes", "常见问题"]:
            faq_pattern = re.compile(
                rf'<(?:section|div)[^>]*>.*?{re.escape(header)}.*?</(?:section|div)>',
                re.IGNORECASE | re.DOTALL
            )
            faq_match = faq_pattern.search(content)
            if faq_match:
                faq_content = faq_match.group(0)
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
        
        lang_results = []
        for file_path in html_files:
            result = check_file_for_english(file_path)
            if result['html_has_english'] or result['jsonld_has_english']:
                lang_results.append(result)
                all_results.append(result)
                
        print(f"Files with untranslated FAQs in {lang}: {len(lang_results)}")

# Print detailed organized results
print("\n" + "="*100)
print("COMPLETE LIST OF FILES WITH UNTRANSLATED FAQs")
print("="*100)

for lang in languages:
    print(f"\n{lang.upper()} LANGUAGE:")
    print("-" * 50)
    
    lang_files = []
    for r in all_results:
        if r['file_path'].startswith('.\' + lang + '\'):
            lang_files.append(r)
    
    if lang_files:
        for result in sorted(lang_files, key=lambda x: x['file_path']):
            rel_path = result['file_path'].replace('.\' + lang + '\', '')
            print(f"\nFile: {rel_path}")
            print(f"English in HTML: {'YES' if result['html_has_english'] else 'NO'}")
            print(f"English in JSON-LD: {'YES' if result['jsonld_has_english'] else 'NO'}")
            if result['sample_text']:
                print(f"Sample English text: {', '.join(result['sample_text'][:3])}")
    else:
        print("No untranslated FAQs found")

print(f"\n\nSUMMARY:")
print(f"Total files with untranslated FAQs: {len(all_results)}")
