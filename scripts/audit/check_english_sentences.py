import os
import re
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
LANGUAGES = ['ar', 'de', 'es', 'fr', 'ja', 'pt', 'zh']

def clean_html(html_content):
    # Remove script, style, head, and comments
    content = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', ' ', html_content, flags=re.IGNORECASE)
    content = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', ' ', content, flags=re.IGNORECASE)
    content = re.sub(r'<!--.*?-->', ' ', content, flags=re.DOTALL)
    # Remove JSON-LD script blocks specifically
    content = re.sub(r'<script\b[^>]*>.*?</script>', ' ', content, flags=re.DOTALL)
    # Remove all HTML tags
    content = re.sub(r'<[^>]+>', ' ', content)
    # Normalize whitespace
    content = re.sub(r'\s+', ' ', content).strip()
    return content

def find_english_phrases(text):
    # Find sequences of 5 or more English words (each >= 3 characters) separated by spaces
    # To avoid matching things like "PNG JPG WebP SVG GIF", we check if it looks like natural language
    # Natural language usually contains common English lowercase words like 'the', 'and', 'for', 'with', 'you', 'your', 'this', 'that', 'from'
    words = text.split(' ')
    english_sequences = []
    current_seq = []
    
    common_english_words = {'the', 'and', 'for', 'with', 'you', 'your', 'this', 'that', 'from', 'are', 'will', 'have', 'not', 'but', 'how', 'what', 'can', 'has', 'our'}
    
    for w in words:
        # Strip punctuation
        w_clean = re.sub(r'[^\w]', '', w)
        if re.match(r'^[a-zA-Z]{3,}$', w_clean):
            current_seq.append(w)
        else:
            if len(current_seq) >= 5:
                # Check if the sequence contains at least one common English word (to ensure it is English prose, not a list of technical acronyms)
                seq_text = " ".join(current_seq)
                if any(cw in seq_text.lower() for cw in common_english_words):
                    english_sequences.append(seq_text)
            current_seq = []
            
    if len(current_seq) >= 5:
        seq_text = " ".join(current_seq)
        if any(cw in seq_text.lower() for cw in common_english_words):
            english_sequences.append(seq_text)
            
    return english_sequences

def scan():
    print("Scanning translated pages for visible English paragraphs...")
    issues = {}
    for lang in LANGUAGES:
        lang_dir = BASE_DIR / lang
        if not lang_dir.exists():
            continue
            
        for root, dirs, files in os.walk(lang_dir):
            for f in files:
                if f.endswith('.html'):
                    fpath = Path(root) / f
                    rel_path = fpath.relative_to(BASE_DIR).as_posix()
                    
                    with open(fpath, 'r', encoding='utf-8') as fh:
                        html = fh.read()
                        
                    visible_text = clean_html(html)
                    phrases = find_english_phrases(visible_text)
                    
                    # Exclude known false positives in the FAQ section if they are about to be fixed
                    # But for now, let's list everything
                    if phrases:
                        issues[rel_path] = phrases
                        
    if issues:
        print(f"\nFound {len(issues)} files with potential English text:")
        for file, phrases in sorted(issues.items()):
            print(f"\n  [{file}]:")
            for p in phrases[:5]:
                print(f"    - \"{p[:100]}...\"")
            if len(phrases) > 5:
                print(f"    - ... and {len(phrases) - 5} more phrases.")
    else:
        print("✅ No untranslated English paragraphs found in body text!")

if __name__ == '__main__':
    scan()
