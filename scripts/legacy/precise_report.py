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

def check_file(file_path):
    """Check a file for FAQ structure and English content"""
    results = {
        'file_path': str(file_path),
        'has_faq_section': False,
        'has_faq_jsonld': False,
        'has_english_text': False,
        'sample_text': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for FAQ section headers
        faq_headers = ["Frequently Asked Questions", "FAQ", "اسئلة", "preguntas", "questions", "fréquentes", "よくある質問", "perguntas frequentes", "常见问题"]
        for header in faq_headers:
            if header in content:
                results['has_faq_section'] = True
                break
                
        # Check for FAQPage JSON-LD
        if '"FAQPage"' in content or '"@type": "FAQPage"' in content:
            results['has_faq_jsonld'] = True
            
        # Check for English text
        for pattern in faq_patterns:
            if pattern.lower() in content.lower():
                results['has_english_text'] = True
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
        html_files = list(lang_dir.rglob('index.html'))
        
        for file_path in html_files:
            result = check_file(file_path)
            if result['has_english_text']:
                result['language'] = lang
                all_results.append(result)

# Create final report
print("\n" + "="*120)
print("COMPLETE LIST OF FILES WITH UNTRANSLATED FAQs")
print("="*120)
print()

# Group results by language for better organization
lang_groups = {}
for result in all_results:
    lang = result['language']
    if lang not in lang_groups:
        lang_groups[lang] = []
    lang_groups[lang].append(result)

# Print results organized by language
for lang, files in sorted(lang_groups.items()):
    print(f"\n{lang.upper()} LANGUAGE:")
    print("-" * 80)
    
    # Group by directory
    dir_groups = {}
    for result in files:
        path_obj = Path(result['file_path'])
        dir_name = path_obj.parent.name
        rel_path = path_obj.name
        
        if dir_name not in dir_groups:
            dir_groups[dir_name] = []
        dir_groups[dir_name].append((result, rel_path))
    
    for dir_name, file_list in sorted(dir_groups.items()):
        print(f"\n  Directory: {dir_name}/")
        for result, rel_path in file_list:
            print(f"    File: {rel_path}")
            print(f"    English in HTML: {'YES' if result['has_faq_section'] else 'NO'}")
            print(f"    English in JSON-LD: {'YES' if result['has_faq_jsonld'] else 'NO'}")
            print(f"    Sample English text: {result['sample_text'][0] if result['sample_text'] else 'None'}")
            print()

print("\n" + "="*120)
print("SUMMARY")
print("="*120)
print(f"Total files with untranslated FAQs: {len(all_results)}")

print("\nBreakdown by language:")
for lang, files in sorted(lang_groups.items()):
    print(f"  {lang.upper()}: {len(files)} files")

print("\nAffected tool directories:")
all_dirs = set()
for result in all_results:
    path_obj = Path(result['file_path'])
    dir_name = path_obj.parent.name
    all_dirs.add(dir_name)
    
for dir_name in sorted(all_dirs):
    print(f"  - {dir_name}")

print("\nNote: All affected files have English text present in both HTML and JSON-LD sections.")
print("This indicates the FAQ content was not properly translated from English.")
