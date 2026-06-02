import os
import re
import json
import urllib.parse
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
LANGUAGES = ['ar', 'de', 'es', 'fr', 'ja', 'pt', 'zh']

# Helper to normalize strings for comparison
def normalize(text):
    if not text:
        return ""
    # Remove HTML tags, convert to lowercase, keep only alphanumeric characters/words
    text = re.sub(r'<[^>]+>', '', text)
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_faqs_html(content):
    """Extract (question, answer) pairs from HTML FAQ structure."""
    faqs = []
    # Find all details or divs with faq items
    # Typically <summary class="faq-question">Question</summary> <p class="faq-answer">Answer</p>
    questions = re.findall(r'class="faq-question"[^>]*>(.*?)</summary>', content, re.DOTALL)
    answers = re.findall(r'class="faq-answer"[^>]*>(.*?)</p>', content, re.DOTALL)
    
    for q, a in zip(questions, answers):
        faqs.append((q.strip(), a.strip()))
    return faqs

def extract_faqs_jsonld(content):
    """Extract FAQ Q&A from JSON-LD blocks."""
    faqs = []
    for match in re.finditer(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', content, re.DOTALL):
        try:
            data = json.loads(match.group(1))
            if isinstance(data, dict):
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
                    faqs.append((name.strip(), text.strip()))
        except Exception:
            pass
    return faqs

def check_html_attributes(content, lang_code):
    """Verify html tag attributes."""
    html_tag = re.search(r'<html([^>]*)>', content)
    if not html_tag:
        return ["Missing <html> tag"]
    
    attrs = html_tag.group(1)
    errors = []
    
    # Check lang
    lang_match = re.search(r'lang="([^"]*)"', attrs)
    if not lang_match:
        errors.append("Missing lang attribute on <html>")
    elif lang_match.group(1) != lang_code:
        errors.append(f"Incorrect lang attribute on <html>: expected '{lang_code}', got '{lang_match.group(1)}'")
        
    # Check dir for Arabic
    dir_match = re.search(r'dir="([^"]*)"', attrs)
    if lang_code == 'ar':
        if not dir_match:
            errors.append("Missing dir=\"rtl\" on <html> for Arabic page")
        elif dir_match.group(1) != 'rtl':
            errors.append(f"Incorrect dir attribute on <html> for Arabic page: expected 'rtl', got '{dir_match.group(1)}'")
    else:
        if dir_match and dir_match.group(1) == 'rtl':
            errors.append(f"Unexpected dir=\"rtl\" on <html> for non-Arabic page")
            
    return errors

def verify_site():
    print("==================================================")
    print("STARTING COMPREHENSIVE SITE VERIFICATION")
    print("==================================================")
    
    # First, find all index.html files
    all_html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Exclude directories
        if '.git' in root or 'node_modules' in root or '.github' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                all_html_files.append(Path(root) / f)
                
    print(f"Found {len(all_html_files)} HTML files to check.")
    
    # Map file paths to their parsed data so we can do cross-validation (e.g. translation diffs)
    pages_data = {}
    
    for fpath in all_html_files:
        rel_path = fpath.relative_to(BASE_DIR).as_posix()
        
        # Determine language and target English page
        parts = rel_path.split('/')
        if parts[0] in LANGUAGES:
            lang = parts[0]
            eng_rel_path = '/'.join(parts[1:])
        else:
            lang = 'en'
            eng_rel_path = rel_path
            
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        faqs_html = extract_faqs_html(content)
        faqs_jsonld = extract_faqs_jsonld(content)
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        
        # Extract canonical
        canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', content)
        if not canonical_match:
            canonical_match = re.search(r'href="([^"]*)"\s+rel="canonical"', content)
        canonical = canonical_match.group(1).strip() if canonical_match else ""
        
        # Extract og:url
        og_url_match = re.search(r'property="og:url"\s+content="([^"]*)"', content)
        if not og_url_match:
            og_url_match = re.search(r'content="([^"]*)"\s+property="og:url"', content)
        og_url = og_url_match.group(1).strip() if og_url_match else ""
        
        # Extract og:image
        og_image_match = re.search(r'property="og:image"\s+content="([^"]*)"', content)
        if not og_image_match:
            og_image_match = re.search(r'content="([^"]*)"\s+property="og:image"', content)
        og_image = og_image_match.group(1).strip() if og_image_match else ""
        
        # Extract meta description
        desc_match = re.search(r'name="description"\s+content="([^"]*)"', content)
        if not desc_match:
            desc_match = re.search(r'content="([^"]*)"\s+name="description"', content)
        desc = desc_match.group(1).strip() if desc_match else ""
        
        # Extract all local links to verify them
        # (href="..." or src="...")
        links = []
        for match in re.finditer(r'(?:href|src)="([^"]*)"', content):
            link = match.group(1).strip()
            # Skip external links, anchors, mailto, javascript
            if (link.startswith('http://') or 
                link.startswith('https://') or 
                link.startswith('//') or 
                link.startswith('#') or 
                link.startswith('mailto:') or 
                link.startswith('javascript:')):
                continue
            links.append(link)
            
        pages_data[rel_path] = {
            'abs_path': fpath,
            'lang': lang,
            'eng_rel_path': eng_rel_path,
            'title': title,
            'canonical': canonical,
            'og_url': og_url,
            'og_image': og_image,
            'description': desc,
            'faqs_html': faqs_html,
            'faqs_jsonld': faqs_jsonld,
            'links': links,
            'content': content,
            'html_attr_errors': check_html_attributes(content, lang)
        }

    # Now perform the validation checks
    translation_errors = []
    canonical_errors = []
    og_errors = []
    link_errors = []
    html_errors = []
    
    for rel_path, data in pages_data.items():
        lang = data['lang']
        eng_rel_path = data['eng_rel_path']
        
        # --- 1. HTML tag errors ---
        for err in data['html_attr_errors']:
            html_errors.append((rel_path, err))
            
        # --- 2. Canonical Link Validation ---
        # Expected canonical points to: https://picete.com/{eng_rel_path_without_index_html}
        # e.g. compress-image/index.html -> https://picete.com/compress-image/
        # index.html -> https://picete.com/
        clean_eng_path = eng_rel_path.replace('index.html', '')
        expected_canonical = f"https://picete.com/{clean_eng_path}"
        if data['canonical'] != expected_canonical:
            canonical_errors.append((rel_path, f"Expected canonical '{expected_canonical}', got '{data['canonical']}'"))
            
        # --- 3. OG URL Validation ---
        # Expected og:url points to actual URL: https://picete.com/{rel_path_without_index_html}
        clean_rel_path = rel_path.replace('index.html', '')
        expected_og_url = f"https://picete.com/{clean_rel_path}"
        if data['og_url'] != expected_og_url:
            og_errors.append((rel_path, f"Expected og:url '{expected_og_url}', got '{data['og_url']}'"))
            
        # --- 4. Link Integrity Checks ---
        # For each local link, resolve it relative to the file's directory and verify it exists
        file_dir = data['abs_path'].parent
        for link in data['links']:
            # Strip query parameters or hashes from link
            parsed_link = urllib.parse.urlparse(link).path
            if not parsed_link:
                continue
                
            resolved_path = (file_dir / parsed_link).resolve()
            
            # If it's a directory link, it should point to an index.html inside that directory
            if resolved_path.is_dir():
                resolved_path = resolved_path / 'index.html'
                
            if not resolved_path.exists():
                link_errors.append((rel_path, f"Dead link: '{link}' (resolved to '{resolved_path}')"))
                
        # --- 5. FAQ Translation Validation (Non-English pages only) ---
        if lang != 'en':
            # Check if corresponding English page data exists
            if eng_rel_path in pages_data:
                eng_data = pages_data[eng_rel_path]
                
                # Check HTML FAQs
                for i, (q, a) in enumerate(data['faqs_html']):
                    # Check if matching English FAQ is identical
                    for eng_q, eng_a in eng_data['faqs_html']:
                        if normalize(q) == normalize(eng_q) and len(normalize(q)) > 10:
                            translation_errors.append((rel_path, f"HTML FAQ Question {i+1} is untranslated (matches English: '{q}')"))
                        if normalize(a) == normalize(eng_a) and len(normalize(a)) > 10:
                            translation_errors.append((rel_path, f"HTML FAQ Answer {i+1} is untranslated (matches English: '{a[:60]}...')"))
                            
                # Check JSON-LD FAQs
                for i, (q, a) in enumerate(data['faqs_jsonld']):
                    for eng_q, eng_a in eng_data['faqs_jsonld']:
                        if normalize(q) == normalize(eng_q) and len(normalize(q)) > 10:
                            translation_errors.append((rel_path, f"JSON-LD FAQ Question {i+1} is untranslated (matches English: '{q}')"))
                        if normalize(a) == normalize(eng_a) and len(normalize(a)) > 10:
                            translation_errors.append((rel_path, f"JSON-LD FAQ Answer {i+1} is untranslated (matches English: '{a[:60]}...')"))
            else:
                translation_errors.append((rel_path, f"Could not find corresponding English page '{eng_rel_path}' to compare FAQs"))

            # Simple heuristic check for large chunks of English text in translations
            # e.g., if there's an English sentence like "Is image processing secure?" or "Yes, our tool is free" in FAQ text
            for i, (q, a) in enumerate(data['faqs_html']):
                # Heuristic: check if question or answer is actually in English
                # We check if it contains typical English phrases that should have been translated
                eng_phrases = ["is it secure", "file size limit", "process multiple", "convert image", "how to use", "free to use"]
                for phrase in eng_phrases:
                    if phrase in normalize(q):
                        translation_errors.append((rel_path, f"HTML FAQ Question {i+1} contains English phrase '{phrase}': '{q}'"))
                    if phrase in normalize(a):
                        translation_errors.append((rel_path, f"HTML FAQ Answer {i+1} contains English phrase '{phrase}': '{a[:60]}...'"))

    # Write report to file
    report_lines = []
    def rprint(text=""):
        report_lines.append(text)
        
    rprint("==================================================")
    rprint("COMPREHENSIVE SITE VERIFICATION REPORT")
    rprint("==================================================")
    
    rprint(f"\n1. HTML ATTRIBUTE ERRORS ({len(html_errors)}):")
    if html_errors:
        for file, err in html_errors:
            rprint(f"  [{file}]: {err}")
    else:
        rprint("  All page <html> tags have correct lang and dir attributes!")

    rprint(f"\n2. CANONICAL LINK ERRORS ({len(canonical_errors)}):")
    if canonical_errors:
        for file, err in canonical_errors:
            rprint(f"  [{file}]: {err}")
    else:
        rprint("  All pages have correct canonical links!")

    rprint(f"\n3. OG URL ERRORS ({len(og_errors)}):")
    if og_errors:
        for file, err in og_errors:
            rprint(f"  [{file}]: {err}")
    else:
        rprint("  All pages have correct og:url values!")

    rprint(f"\n4. DEAD LINK ERRORS ({len(link_errors)}):")
    if link_errors:
        by_file = {}
        for file, err in link_errors:
            by_file.setdefault(file, []).append(err)
        for file, errs in sorted(by_file.items()):
            rprint(f"  [{file}]:")
            for err in errs:
                rprint(f"    - {err}")
    else:
        rprint("  All page links (href/src) are valid (no dead links)!")

    rprint(f"\n5. FAQ TRANSLATION ERRORS ({len(translation_errors)}):")
    if translation_errors:
        unique_trans_errors = sorted(list(set(translation_errors)))
        by_file = {}
        for file, err in unique_trans_errors:
            by_file.setdefault(file, []).append(err)
        for file, errs in sorted(by_file.items()):
            rprint(f"  [{file}]:")
            for err in errs:
                rprint(f"    - {err}")
    else:
        rprint("  All translated pages have unique non-English FAQ content compared to English versions!")

    total_issues = len(html_errors) + len(canonical_errors) + len(og_errors) + len(link_errors) + len(translation_errors)
    rprint("\n" + "="*80)
    if total_issues == 0:
        rprint("ALL TESTS PASSED! The site is fully verified and clean.")
    else:
        rprint(f"FOUND {total_issues} TOTAL ISSUES. Please review and fix.")
    rprint("="*80)
    
    # Save report
    report_content = "\n".join(report_lines)
    with open('verification_report.txt', 'w', encoding='utf-8') as rf:
        rf.write(report_content)
        
    # Console print safe summary
    print("\n" + "="*80)
    print("VERIFICATION COMPLETED. Safe console summary:")
    print("="*80)
    print(f"HTML Attribute Errors: {len(html_errors)}")
    print(f"Canonical Link Errors: {len(canonical_errors)}")
    print(f"OG URL Errors:         {len(og_errors)}")
    print(f"Dead Link Errors:      {len(link_errors)}")
    print(f"FAQ Translation Errors:{len(translation_errors)}")
    print(f"Total Issues:          {total_issues}")
    print("="*80)
    print("Detailed report written to 'verification_report.txt'")
    print("="*80)

if __name__ == '__main__':
    verify_site()

