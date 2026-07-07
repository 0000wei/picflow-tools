import os
import json
import re
from bs4 import BeautifulSoup

# List of folders to exclude from tool search
EXCLUDE_DIRS = {
    '.git', '.git-crypt', '.codegraph', '__pycache__', 'node_modules',
    'config', 'scripts', 'docs', 'seo', 'css', 'js', 'images', 'assets',
    'templates', 'rawtest'
}

# Supported locales
LOCALES = ['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko']

# Standard localized features for SoftwareApplication
LOCALIZED_FEATURES = {
    'en': '100% Client-side image processing, Privacy secured, Batch converting',
    'zh': '100% 浏览器本地处理，保障隐私安全，支持批量转换',
    'ja': '100% ブラウザ内ローカル処理、プライバシー保護、一括変換対応',
    'de': '100% Lokale Verarbeitung im Browser, Datenschutz garantiert, Stapelverarbeitung',
    'fr': 'Traitement 100% local dans le navigateur, Confidentialité garantie, Conversion par lot',
    'es': 'Procesamiento 100% local en el navegador, Privacidad garantizada, Conversión por lotes',
    'pt': 'Processamento 100% local no navegador, Privacidade garantida, Conversão em lote',
    'ar': 'معالجة محلية 100% في المتصفح، أمان الخصوصية، تحويل دفعات',
    'ko': '100% 브라우저 로컬 처리, 개인정보 보장, 일괄 변환 지원'
}

# Standard localized home names
LOCALIZED_HOME = {
    'en': 'Home',
    'zh': '首页',
    'ja': 'ホーム',
    'de': 'Startseite',
    'fr': 'Accueil',
    'es': 'Inicio',
    'pt': 'Início',
    'ar': 'الرئيسية',
    'ko': '홈'
}

# Tools eligible for the Before/After comparison slider
# Excludes text-only redirects: webp-to-png-for-website, png-to-webp-for-wordpress, png-to-jpg-for-email, jpg-to-png-for-instagram
SLIDER_ELIGIBLE_TOOLS = {
    # Compress tools
    'compress-image',
    # Convert tools
    'png-to-jpg', 'jpg-to-png', 'webp-to-png', 'png-to-webp', 'jpg-to-webp',
    'avif-to-png', 'png-to-avif', 'jpg-to-avif', 'webp-to-avif',
    'raw-to-jpg', 'raw-to-png', 'raw-to-webp', 'raw-to-avif'
}

def get_tool_directories(root_dir):
    """Scan root_dir for directories that contain index.html and are not excluded."""
    tools = []
    for entry in os.scandir(root_dir):
        if entry.is_dir() and entry.name not in EXCLUDE_DIRS and entry.name not in LOCALES:
            if os.path.exists(os.path.join(entry.path, 'index.html')):
                tools.append(entry.name)
    return sorted(tools)

def extract_faqs_from_html(soup):
    """Scrape details/summary elements to construct FAQ list."""
    faqs = []
    for details in soup.find_all('details', class_='faq-item'):
        summary = details.find('summary', class_='faq-question')
        answer = details.find(class_='faq-answer') or details.find('p')
        if summary and answer:
            faqs.append({
                "question": summary.get_text().strip(),
                "answer": answer.get_text().strip()
            })
    return faqs

def generate_hreflang_tags(tool_name):
    """Generate the standard 10-line hreflang alternate tags."""
    lines = [
        f'<link rel="alternate" hreflang="en" href="https://picete.com/{tool_name}/" />'
    ]
    for lang in LOCALES:
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="https://picete.com/{lang}/{tool_name}/" />')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="https://picete.com/{tool_name}/" />')
    return '\n'.join(lines)

def update_html_seo(file_path, tool_name, lang):
    """Load, parse, update and save the HTML file with correct TDK, hreflang, schemas, and slider DOM."""
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # We use BeautifulSoup to modify the structures
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Update Canonical link
    canonical_tag = soup.find('link', rel='canonical')
    expected_canonical = f"https://picete.com/{tool_name}/" if lang == 'en' else f"https://picete.com/{lang}/{tool_name}/"
    if canonical_tag:
        canonical_tag['href'] = expected_canonical
    else:
        new_canonical = soup.new_tag('link', rel='canonical', href=expected_canonical)
        if soup.head:
            soup.head.append(new_canonical)

    # 2. Update Hreflang alternate tags
    # Remove existing ones
    for tag in soup.find_all('link', rel='alternate'):
        if tag.get('hreflang'):
            tag.decompose()
            
    # Inject new Hreflang block in the head
    hreflang_html = generate_hreflang_tags(tool_name)
    hreflang_soup = BeautifulSoup(hreflang_html, 'html.parser')
    if soup.head:
        # Find canonical or first link and insert before/after
        ref_tag = soup.find('link', rel='canonical') or soup.head.find('link') or soup.head.find('meta')
        if ref_tag:
            for tag in reversed(list(hreflang_soup.children)):
                if tag.name:
                    ref_tag.insert_after(tag)
        else:
            for tag in hreflang_soup.children:
                if tag.name:
                    soup.head.append(tag)

    # 3. Schema.org JSON-LD Updates
    # We parse existing JSON-LD scripts to extract names
    tool_localized_name = tool_name.replace('-', ' ').title()
    
    # Check existing WebApplication/SoftwareApplication
    existing_ld_scripts = soup.find_all('script', type='application/ld+json')
    
    for i, script in enumerate(existing_ld_scripts):
        try:
            # Try parsing to get localized name
            data = json.loads(script.string or '')
            if isinstance(data, dict) and data.get('@type') in ('WebApplication', 'SoftwareApplication') and data.get('name'):
                tool_localized_name = data.get('name')
        except Exception:
            # Fallback to simple regex search inside script content to extract name
            text = script.string or ''
            match = re.search(r'"name"\s*:\s*"([^"]+)"', text)
            if match:
                tool_localized_name = match.group(1)

    # Build SoftwareApplication Schema
    app_schema_data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": tool_localized_name,
        "operatingSystem": "WebBrowser",
        "applicationCategory": "MultimediaApplication",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "browserRequirements": "Requires HTML5 Canvas/WebAssembly support.",
        "features": LOCALIZED_FEATURES.get(lang, LOCALIZED_FEATURES['en'])
    }
    
    # Build Breadcrumb Schema
    home_url = "https://picete.com/" if lang == 'en' else f"https://picete.com/{lang}/"
    tool_url = f"https://picete.com/{tool_name}/" if lang == 'en' else f"https://picete.com/{lang}/{tool_name}/"
    breadcrumb_schema_data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": LOCALIZED_HOME.get(lang, LOCALIZED_HOME['en']),
                "item": home_url
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": tool_localized_name,
                "item": tool_url
            }
        ]
    }

    # Build FAQ Schema
    faqs = extract_faqs_from_html(soup)
    faq_schema_data = None
    if faqs:
        faq_schema_data = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": []
        }
        for item in faqs:
            faq_schema_data["mainEntity"].append({
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"]
                }
            })

    # Clean old JSON-LD scripts using string matching (robust to parsing failures on legacy errors)
    for script in list(existing_ld_scripts):
        text = script.string or ''
        if '"WebApplication"' in text or '"SoftwareApplication"' in text or '"BreadcrumbList"' in text or '"FAQPage"' in text:
            script.decompose()

    # Inject new JSON-LD scripts
    def inject_json_ld(schema_data):
        tag = soup.new_tag('script', type='application/ld+json')
        tag.string = json.dumps(schema_data, indent=4, ensure_ascii=False)
        if soup.head:
            soup.head.append(tag)

    inject_json_ld(app_schema_data)
    inject_json_ld(breadcrumb_schema_data)
    if faq_schema_data:
        inject_json_ld(faq_schema_data)

    # 4. Before/After Slider Injection (For eligible tools only)
    if tool_name in SLIDER_ELIGIBLE_TOOLS:
        # Check if the slider is already injected
        if not soup.find(id='comparisonSlider'):
            # Find the download-section to insert it inside
            download_section = soup.find(id='downloadSection')
            
            # Self-healing: if ID is missing but Class is present
            if not download_section:
                download_section = soup.find(class_='download-section')
                if download_section:
                    download_section['id'] = 'downloadSection'
                    
            if download_section:
                # Localized labels for size information
                lbl_orig = "Original" if lang == 'en' else "原图" if lang == 'zh' else "元画像" if lang == 'ja' else "Original"
                lbl_conv = "Converted" if lang == 'en' else "转换后" if lang == 'zh' else "変換後" if lang == 'ja' else "Konvertiert" if lang == 'de' else "Converti" if lang == 'fr' else "Convertido" if lang == 'es' or lang == 'pt' else "تحويل" if lang == 'ar' else "변환됨" if lang == 'ko' else "Converted"
                
                slider_html = f"""
                <div class="image-comparison-slider" id="comparisonSlider" style="display: none; margin: 1.5rem auto; max-width: 800px;">
                  <div class="slider-aspect-ratio-holder" style="aspect-ratio: 16 / 9; position: relative; overflow: hidden; width: 100%; border-radius: 8px; border: 1px solid var(--border-color, #e5e7eb);">
                    <div class="slider-skeleton" style="position: absolute; inset: 0; background: linear-gradient(90deg, var(--bg-secondary, #f3f4f6) 25%, var(--border-color, #e5e7eb) 50%, var(--bg-secondary, #f3f4f6) 75%); background-size: 200% 100%; animation: loading-shimmer 1.5s infinite;"></div>
                    <div class="slider-container" style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; transition: opacity 0.3s ease;">
                      <img class="img-original" src="" alt="{lbl_orig}" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain;">
                      <div class="img-compressed-wrapper" style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; width: 50%; overflow: hidden; pointer-events: none; border-left: 2px solid var(--primary-color, #2563eb);">
                        <img class="img-compressed" src="" alt="{lbl_conv}" style="position: absolute; top: 0; left: 0; height: 100%; object-fit: contain; pointer-events: none;">
                      </div>
                      <div class="slider-handle" style="position: absolute; top: 0; bottom: 0; left: 50%; width: 40px; margin-left: -20px; cursor: ew-resize; display: flex; align-items: center; justify-content: center; z-index: 10;">
                        <div class="slider-handle-button" style="width: 40px; height: 40px; border-radius: 50%; background: var(--primary-color, #2563eb); border: 4px solid #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 18px; font-weight: bold; user-select: none;">
                          ↔
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="slider-info" style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-light, #6b7280); text-align: center;">
                    {lbl_orig}: <span class="size-orig">0 KB</span> | {lbl_conv}: <span class="size-conv">0 KB</span> (<span class="size-diff">-0%</span>)
                  </div>
                </div>
                """
                # Insert slider right after <h3>Conversion Complete!</h3> or download-grid
                dl_grid = download_section.find(id='downloadGrid')
                if dl_grid:
                    slider_soup = BeautifulSoup(slider_html, 'html.parser')
                    dl_grid.insert_before(slider_soup)
                else:
                    h3 = download_section.find('h3')
                    slider_soup = BeautifulSoup(slider_html, 'html.parser')
                    if h3:
                        h3.insert_after(slider_soup)
                    else:
                        download_section.insert(0, slider_soup)

        # Append script reference to body if not already present
        if not soup.find('script', src='/js/image-comparison-slider.js'):
            new_script = soup.new_tag('script', src='/js/image-comparison-slider.js', defer=True)
            if soup.body:
                soup.body.append(new_script)

    # Format and save
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    print(f"Scanning project workspace at: {root_dir}")
    tools = get_tool_directories(root_dir)
    print(f"Found {len(tools)} tools: {tools}")
    
    # Process EN (root) versions first
    for tool in tools:
        en_path = os.path.join(root_dir, tool, 'index.html')
        if os.path.exists(en_path):
            print(f"Processing EN tool: {tool}")
            update_html_seo(en_path, tool, 'en')
            
        # Process other locales
        for lang in LOCALES:
            lang_path = os.path.join(root_dir, lang, tool, 'index.html')
            if os.path.exists(lang_path):
                print(f"Processing {lang} tool: {tool}")
                update_html_seo(lang_path, tool, lang)

    print("Programmatic SEO matrix generation completed successfully!")

if __name__ == "__main__":
    main()
