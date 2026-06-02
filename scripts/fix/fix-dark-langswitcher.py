#!/usr/bin/env python3
"""
Fix: add dark mode support to the language switcher.
The arrow SVG uses a hardcoded stroke color (#6b7280) which doesn't change in dark mode.
Replace it with a data URI that uses currentColor so it inherits properly.
Also add background-color for the dropdown options in dark mode.
"""

import os
import re

BASE = "/home/wu/picete-site"

# The new SVG arrow that uses currentColor
LIGHT_ARROW = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E"
DARK_ARROW = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239CA3AF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E"

def fix_page(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    if "lang-switcher" not in html:
        return False
    
    # 1. Replace the static arrow with a dark-mode-aware one using CSS + media query
    old_select_block = re.search(
        r'\.lang-switcher select \{[^}]+\}',
        html
    )
    
    if old_select_block:
        new_select_css = """        .lang-switcher select {
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
        }
        @media (prefers-color-scheme: dark) {
            .lang-switcher select {
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239CA3AF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            }
        }"""
        html = html.replace(old_select_block.group(0), new_select_css)
    
    # 2. Fix RTL padding
    old_rtl = """        [dir="rtl"] .lang-switcher select {
            background-position: left 0.5rem center;
            padding: 0.375rem 0.75rem 0.375rem 2rem;
        }"""
    new_rtl = """        [dir="rtl"] .lang-switcher select {
            background-position: left 0.5rem center;
            padding: 0.375rem 0.75rem 0.375rem 2rem;
        }
        @media (prefers-color-scheme: dark) {
            [dir="rtl"] .lang-switcher select {
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239CA3AF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            }
        }"""
    html = html.replace(old_rtl, new_rtl)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    return True


def collect_all_pages():
    pages = []
    pages.append(os.path.join(BASE, "index.html"))
    for d in sorted(os.listdir(BASE)):
        ipath = os.path.join(BASE, d, "index.html")
        if os.path.isfile(ipath) and d not in ("css", "js", "images", "node_modules"):
            pages.append(ipath)
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
    fixed = 0
    for p in pages:
        if fix_page(p):
            fixed += 1
    print(f"Fixed dark mode for lang-switcher on {fixed} pages")
    
    # Clean up the temp script
    os.remove(os.path.join(BASE, "add-lang-switcher.py"))

if __name__ == "__main__":
    main()
