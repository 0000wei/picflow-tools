#!/usr/bin/env python3
"""
Add a language switcher dropdown to the navigation bar of all PicEte pages
(English + all 7 translated languages).

Also add automatic redirect on the English homepage based on browser language.

LANGUAGES: en, zh, ja, de, fr, es, pt, ar
"""

import os
import re
import json

BASE = "/home/wu/picete-site"

LANGUAGES = [
    ("en", "English", "https://picete.com/"),
    ("zh", "中文", "https://picete.com/zh/"),
    ("ja", "日本語", "https://picete.com/ja/"),
    ("de", "Deutsch", "https://picete.com/de/"),
    ("fr", "Français", "https://picete.com/fr/"),
    ("es", "Español", "https://picete.com/es/"),
    ("pt", "Português", "https://picete.com/pt/"),
    ("ar", "العربية", "https://picete.com/ar/"),
]

# Map browser language codes to our language codes
BROWSER_LANG_MAP = {
    "zh": "zh", "zh-CN": "zh", "zh-TW": "zh", "zh-HK": "zh",
    "ja": "ja", "ja-JP": "ja",
    "de": "de", "de-DE": "de", "de-AT": "de", "de-CH": "de",
    "fr": "fr", "fr-FR": "fr", "fr-CA": "fr", "fr-BE": "fr", "fr-CH": "fr",
    "es": "es", "es-ES": "es", "es-MX": "es", "es-AR": "es",
    "pt": "pt", "pt-PT": "pt", "pt-BR": "pt",
    "ar": "ar", "ar-SA": "ar", "ar-AE": "ar", "ar-EG": "ar",
}

LANG_NAMES = {code: name for code, name, _ in LANGUAGES}
LANG_HREFS = {code: href for code, _, href in LANGUAGES}


def make_lang_switcher_html(current_lang):
    """Generate language switcher HTML."""
    items = []
    for code, name, href in LANGUAGES:
        selected = ' selected' if code == current_lang else ''
        display = f"🌐 {name}" if code != current_lang else f"🌐 {name}"
        items.append(f'            <option value="{code}"{selected}>{name}</option>')
    
    options = '\n'.join(items)
    
    return f'''    <!-- Language Switcher -->
    <style>
        .lang-switcher {{
            position: relative;
            display: inline-block;
        }}
        .lang-switcher select {{
            appearance: none;
            -webkit-appearance: none;
            background: transparent;
            border: 1px solid var(--border-color, #e5e7eb);
            border-radius: 6px;
            padding: 0.375rem 2rem 0.375rem 0.75rem;
            font-size: 0.875rem;
            color: var(--text-color, #374151);
            cursor: pointer;
            outline: none;
            transition: border-color 0.2s;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.5rem center;
            background-size: 12px;
            min-width: 120px;
        }}
        .lang-switcher select:hover {{
            border-color: var(--primary-color, #2563eb);
        }}
        .lang-switcher select:focus-visible {{
            border-color: var(--primary-color, #2563eb);
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
        }}
        /* RTL support for Arabic */
        [dir="rtl"] .lang-switcher select {{
            background-position: left 0.5rem center;
            padding: 0.375rem 0.75rem 0.375rem 2rem;
        }}
    </style>
    <div class="lang-switcher">
        <select onchange="switchLanguage(this.value)" aria-label="Switch language">
{options}
        </select>
    </div>
    <script>
    function switchLanguage(code) {{
        var paths = {json.dumps(LANG_HREFS)};
        // Get current page path from URL
        var path = window.location.pathname;
        
        // Remove language prefix if present
        var cleanPath = path.replace(/^\\/(zh|ja|de|fr|es|pt|ar)\\//, '/');
        if (!cleanPath.startsWith('/')) cleanPath = '/' + cleanPath;
        
        // Build target URL
        var baseUrl = paths[code];
        var targetPath = cleanPath;
        
        // For homepage (index.html or trailing slash)
        if (targetPath === '/' || targetPath === '/index.html') {{
            window.location.href = baseUrl;
        }} else {{
            // Remove leading slash before appending to base URL
            window.location.href = baseUrl.replace(/\\/$/, '') + targetPath;
        }}
    }}
    </script>'''


def get_page_lang(filepath):
    """Detect language from file path."""
    rel = os.path.relpath(filepath, BASE)
    parts = rel.split(os.sep)
    if parts[0] in ("zh", "ja", "de", "fr", "es", "pt", "ar"):
        return parts[0]
    return "en"


def get_page_lang_prefix(filepath):
    """Get the language prefix for internal links."""
    lang = get_page_lang(filepath)
    if lang == "en":
        return ""
    return lang


def add_switcher_to_page(filepath):
    """Add language switcher to a page."""
    lang = get_page_lang(filepath)
    
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Skip if already has lang-switcher
    if 'lang-switcher' in html:
        return False
    
    switcher_html = make_lang_switcher_html(lang)
    
    # Find the nav element and insert the language switcher before its closing
    # Pattern: <nav ...> ... </nav>
    # Insert switcher before the last nav-link
    m = re.search(r'(<nav[^>]*>.*?)(</nav>)', html, re.DOTALL)
    if m:
        nav_content = m.group(1)
        nav_close = m.group(2)
        # Add switcher before </nav>
        new_nav = nav_content + '\n' + switcher_html + '\n            ' + nav_close
        html = html.replace(m.group(0), new_nav)
    else:
        # Fallback: insert before </header>
        html = html.replace('</header>', switcher_html + '\n</header>')
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    return True


def add_client_redirect(filepath):
    """Add client-side language detection redirect to the English homepage only."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    if 'langRedirect' in html:
        return False
    
    # Build redirect logic
    cases = []
    for browser_code, our_code in BROWSER_LANG_MAP.items():
        cases.append(f'            if (lang.startsWith("{browser_code}")) return "{our_code}";')
    
    redirect_script = f'''
    <script>
    // Auto-redirect based on browser language (only on first visit)
    (function() {{
        if (localStorage.getItem('picete_lang_choice')) return;
        
        var lang = (navigator.language || navigator.userLanguage || '').toLowerCase();
        var target = 'en';
        
{cases}
        
        if (target !== 'en') {{
            localStorage.setItem('picete_lang_choice', target);
            window.location.href = '/{{target}}/'.replace('{{target}}', target);
        }}
    }})();
    </script>'''
    
    html = html.replace('<script async src="https://www.googletagmanager.com/gtag/js?id=G-H72N80TEBW"></script>', 
                        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-H72N80TEBW"></script>' + redirect_script)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    return True


def collect_all_pages():
    """Collect all HTML pages across all languages."""
    pages = []
    
    # English
    pages.append(os.path.join(BASE, "index.html"))
    for d in sorted(os.listdir(BASE)):
        ipath = os.path.join(BASE, d, "index.html")
        if os.path.isfile(ipath) and d not in ("css", "js", "images", "node_modules", 
                                                "zh", "ja", "de", "fr", "es", "pt", "ar"):
            pages.append(ipath)
    
    # All languages
    for lang_code in ("zh", "ja", "de", "fr", "es", "pt", "ar"):
        lang_dir = os.path.join(BASE, lang_code)
        if not os.path.isdir(lang_dir):
            continue
        pages.append(os.path.join(lang_dir, "index.html"))
        for d in sorted(os.listdir(lang_dir)):
            ipath = os.path.join(lang_dir, d, "index.html")
            if os.path.isfile(ipath) and os.path.isdir(os.path.join(lang_dir, d)):
                pages.append(ipath)
    
    return sorted(set(pages))


def main():
    pages = collect_all_pages()
    print(f"Total pages: {len(pages)}")
    
    # Add language switcher to all pages
    switcher_count = 0
    for p in pages:
        if add_switcher_to_page(p):
            lang = get_page_lang(p)
            rel = os.path.relpath(p, BASE)
            print(f"  Switcher added: [{lang}] {rel}")
            switcher_count += 1
    
    print(f"\nLanguage switcher added to {switcher_count} pages")
    
    # Add auto-redirect only to English homepage
    en_home = os.path.join(BASE, "index.html")
    add_client_redirect(en_home)
    print(f"Auto-redirect added to English homepage")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
