import os
import json
import sys
from bs4 import BeautifulSoup

# List of folders to exclude from tool search
EXCLUDE_DIRS = {
    '.git', '.git-crypt', '.codegraph', '__pycache__', 'node_modules',
    'config', 'scripts', 'docs', 'seo', 'css', 'js', 'images', 'assets',
    'templates', 'rawtest'
}

# Supported locales
LOCALES = ['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko']

SLIDER_ELIGIBLE_TOOLS = {
    # Compress tools
    'compress-image',
    # Convert tools
    'png-to-jpg', 'jpg-to-png', 'webp-to-png', 'png-to-webp', 'jpg-to-webp',
    'avif-to-png', 'png-to-avif', 'jpg-to-avif', 'webp-to-avif',
    'raw-to-jpg', 'raw-to-png', 'raw-to-webp', 'raw-to-avif',
    'webp-to-jpg'
}

def get_tool_directories(root_dir):
    tools = []
    for entry in os.scandir(root_dir):
        if entry.is_dir() and entry.name not in EXCLUDE_DIRS and entry.name not in LOCALES:
            if os.path.exists(os.path.join(entry.path, 'index.html')):
                tools.append(entry.name)
    return sorted(tools)

def check_file(file_path, tool_name, lang):
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Canonical Link Check
    canonical = soup.find('link', rel='canonical')
    expected_canonical = f"https://picete.com/{tool_name}/" if lang == 'en' else f"https://picete.com/{lang}/{tool_name}/"
    if not canonical:
        errors.append("Missing canonical link tag.")
    elif canonical.get('href') != expected_canonical:
        errors.append(f"Canonical URL mismatch: expected '{expected_canonical}', got '{canonical.get('href')}'")

    # 2. Hreflang Tags Check
    hreflangs = soup.find_all('link', rel='alternate')
    lang_tags = [tag.get('hreflang') for tag in hreflangs if tag.get('hreflang')]
    
    # Check for flat URLs (no "/tools/")
    for tag in hreflangs:
        href = tag.get('href', '')
        if '/tools/' in href:
            errors.append(f"Violation: hreflang contains '/tools/' in href: {href}")

    if len(lang_tags) != 10:
        errors.append(f"Incorrect number of hreflang tags: expected 10, got {len(lang_tags)}. Found: {lang_tags}")
        
    expected_langs = {'en', 'zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko', 'x-default'}
    missing_langs = expected_langs - set(lang_tags)
    if missing_langs:
        errors.append(f"Missing hreflang for locales: {missing_langs}")

    # 3. Schema JSON-LD Verification
    ld_scripts = soup.find_all('script', type='application/ld+json')
    types_found = []
    
    has_software_app = False
    has_breadcrumb = False
    has_faq_page = False
    
    for script in ld_scripts:
        try:
            data = json.loads(script.string or '')
            if isinstance(data, dict):
                t = data.get('@type')
                types_found.append(t)
                if t == 'SoftwareApplication':
                    has_software_app = True
                    # Check offers
                    offers = data.get('offers')
                    if not offers or offers.get('price') != '0':
                        errors.append("SoftwareApplication schema offers price is not '0'.")
                elif t == 'BreadcrumbList':
                    has_breadcrumb = True
                    items = data.get('itemListElement', [])
                    if len(items) != 2:
                        errors.append(f"BreadcrumbList should have exactly 2 items, found {len(items)}")
                elif t == 'FAQPage':
                    has_faq_page = True
        except Exception as e:
            errors.append(f"Failed to parse JSON-LD script: {e}")

    if not has_software_app:
        errors.append(f"Missing SoftwareApplication schema. Found types: {types_found}")
    if not has_breadcrumb:
        errors.append(f"Missing BreadcrumbList schema. Found types: {types_found}")
        
    # Check if FAQ HTML exists, FAQ Page Schema must also exist
    has_faq_html = len(soup.find_all('details', class_='faq-item')) > 0
    if has_faq_html and not has_faq_page:
        errors.append("FAQ HTML is present, but FAQPage JSON-LD schema is missing.")

    # 4. Slider verification (For eligible tools only)
    if tool_name in SLIDER_ELIGIBLE_TOOLS:
        slider = soup.find(id='comparisonSlider')
        if not slider:
            errors.append(f"Eligible tool '{tool_name}' is missing comparison slider div (#comparisonSlider).")
        slider_script = soup.find('script', src='/js/image-comparison-slider.js')
        if not slider_script:
            errors.append("Missing image-comparison-slider.js script import.")

    return errors

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    tools = get_tool_directories(root_dir)
    
    total_errors = 0
    total_files_checked = 0
    
    print("Starting SEO & Organic Growth programmatic audit...")
    
    for tool in tools:
        en_path = os.path.join(root_dir, tool, 'index.html')
        if os.path.exists(en_path):
            total_files_checked += 1
            errors = check_file(en_path, tool, 'en')
            if errors:
                total_errors += len(errors)
                print(f"[FAIL] EN/{tool}:")
                for err in errors:
                    print(f"   - {err}")
                    
        for lang in LOCALES:
            lang_path = os.path.join(root_dir, lang, tool, 'index.html')
            if os.path.exists(lang_path):
                total_files_checked += 1
                errors = check_file(lang_path, tool, lang)
                if errors:
                    total_errors += len(errors)
                    print(f"[FAIL] {lang.upper()}/{tool}:")
                    for err in errors:
                        print(f"   - {err}")
                        
    print(f"\nAudit complete: Checked {total_files_checked} files.")
    if total_errors > 0:
        print(f"[ERROR] Found {total_errors} errors in total.")
        sys.exit(1)
    else:
        print("[OK] All checks passed successfully! Zero errors found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
