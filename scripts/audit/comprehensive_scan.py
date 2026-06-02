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
            result = check_file(file_path)
            
            # A file is problematic if:
            # 1. It has English text but no FAQ section (not translated)
            # 2. It has English text in both HTML and JSON-LD (partially translated)
            # 3. It has English text only in JSON-LD (partially translated)
            if result['has_english_text']:
                lang_results.append(result)
                all_results.append(result)
                
        print(f"Files with English FAQ text in {lang}: {len(lang_results)}")

# Print organized results
print("\n" + "="*120)
print("COMPLETE LIST OF FILES WITH UNTRANSLATED FAQs")
print("="*120)

# Results by language
for lang in languages:
    print(f"\n{lang.upper()} LANGUAGE:")
    print("-" * 60)
    
    lang_files = []
    for r in all_results:
        if Path(r['file_path']).is_relative_to(Path(f'./{lang}')):
            lang_files.append(r)
    
    if lang_files:
        # Group by directory
        dir_groups = {}
        for result in lang_files:
            path = Path(result['file_path'])
            dir_name = path.parent.name
            if dir_name not in dir_groups:
                dir_groups[dir_name] = []
            dir_groups[dir_name].append(result)
        
        for dir_name, files in sorted(dir_groups.items()):
            print(f"\n  Directory: {dir_name}/")
            for result in files:
                rel_path = Path(result['file_path']).name
                print(f"    - {rel_path}")
                print(f"      English in HTML: {'YES' if result['has_faq_section'] else 'NO'}")
                print(f"      English in JSON-LD: {'YES' if result['has_faq_jsonld'] else 'NO'}")
                if result['sample_text']:
                    print(f"      Sample: {result['sample_text'][0]}")
                print()
    else:
        print("No untranslated FAQs found")

print("\n" + "="*120)
print("SUMMARY")
print("="*120)
print(f"Total files with English FAQ text: {len(all_results)}")

# Count by language
lang_counts = {}
for r in all_results:
    path = Path(r['file_path'])
    lang = path.parts[1]
    lang_counts[lang] = lang_counts.get(lang, 0) + 1

print("\nFiles by language:")
for lang, count in sorted(lang_counts.items()):
    print(f"  {lang.upper()}: {count} files")

print("\nNote: Files with 'NO' for HTML FAQ section indicate missing translations.")
print("Files with 'YES' for both HTML and JSON-LD indicate partial translations.")
