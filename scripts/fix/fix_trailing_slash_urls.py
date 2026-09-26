#!/usr/bin/env python3
"""Rewrite declared picete.com URLs from trailing-slash to non-slash form.

Production serves non-slash URLs with 200 (vercel.json: cleanUrls=true,
trailingSlash=false) and 308-redirects slash URLs. Every declaration
(canonical, og:url, hreflang alternates, JSON-LD url/item fields, internal
links) must therefore use the non-slash form.

Scope: matrix HTML (root tool pages, language homepages, language tool
pages, root index/privacy-policy) plus llms.txt. The bare homepage
"https://picete.com/" and "/" are preserved as-is.
"""

import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

EXCLUDED_ROOT_DIRS = {
    'zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko',
    'css', 'js', 'images', 'config', 'docs', 'scripts', 'seo', 'assets',
    'picete-mcp-dev', 'rawtest', 'specs',
    '.git', '.codegraph', '.well-known', 'node_modules', '.claude',
}
LANGS = ['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko']

# https://picete.com/<path>/  ->  https://picete.com/<path>
# Requires at least one path char before the trailing slash, so the bare
# homepage URL never matches. Trailing slash must be followed by a
# delimiter (quote, fragment, query, whitespace, or tag open).
ABS_URL = re.compile(r'(https://picete\.com/[^\s"\'<>#?]+)/(?=["\'#?\s<])')

# "/<path>/"  ->  "/<path>"  (quote-delimited root-relative link)
REL_URL_QUOTED = re.compile(r'(["\'])/([^\s"\'#?<>]+)/(?=\1)')

# (/<path>/)  ->  (/<path>)  (markdown-style link or prose, e.g. llms.txt)
REL_URL_PAREN = re.compile(r'\((/[^\s()#?<>]+)/\)')
# bare relative path inside parens after ", " or "(", e.g. "(e.g., /x/)"
REL_URL_PAREN_AFTER_COMMA = re.compile(r'(,\s*)/([^\s()#?<>]+)/\)')
REL_URL_PAREN_BARE = re.compile(r'(\(\s*)/([^\s()#?<>]+)/(\))')

# Homepage JSON-LD "url" must equal the homepage canonical exactly:
# "url": "https://picete.com" -> "url": "https://picete.com/"
HOME_JSONLD_URL = re.compile(r'("url"\s*:\s*"https://picete\.com)(?=")')


def collect_files():
    files = []
    for name in ('index.html', 'privacy-policy.html'):
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            files.append(p)
    for entry in sorted(os.scandir(ROOT), key=lambda e: e.name):
        if entry.is_dir() and entry.name not in EXCLUDED_ROOT_DIRS:
            p = os.path.join(entry.path, 'index.html')
            if os.path.exists(p):
                files.append(p)
    for lang in LANGS:
        lang_dir = os.path.join(ROOT, lang)
        if not os.path.isdir(lang_dir):
            continue
        home = os.path.join(lang_dir, 'index.html')
        if os.path.exists(home):
            files.append(home)
        for entry in sorted(os.scandir(lang_dir), key=lambda e: e.name):
            if entry.is_dir():
                p = os.path.join(entry.path, 'index.html')
                if os.path.exists(p):
                    files.append(p)
    llms = os.path.join(ROOT, 'llms.txt')
    if os.path.exists(llms):
        files.append(llms)
    return files


def fix_content(content, is_txt):
    n = len(ABS_URL.findall(content))
    content = ABS_URL.sub(r'\1', content)
    for pattern, repl in (
        (REL_URL_QUOTED, r'\1/\2'),
        (REL_URL_PAREN, r'(\1)'),
    ):
        n += len(pattern.findall(content))
        content = pattern.sub(repl, content)
    if not is_txt:
        n += len(HOME_JSONLD_URL.findall(content))
        content = HOME_JSONLD_URL.sub(r'\1/', content)
    else:
        for pattern, repl in (
            (REL_URL_PAREN_AFTER_COMMA, r'\1/\2)'),
            (REL_URL_PAREN_BARE, r'\1/\2\3'),
        ):
            n += len(pattern.findall(content))
            content = pattern.sub(repl, content)
    return content, n


def main():
    total_files = 0
    total_repls = 0
    for path in collect_files():
        with open(path, 'r', encoding='utf-8', newline='') as f:
            original = f.read()
        fixed, n = fix_content(original, path.endswith('.txt'))
        if n:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(fixed)
            total_files += 1
            total_repls += n
            print(f'  {os.path.relpath(path, ROOT)}: {n} replacement(s)')
    print(f'Done. {total_repls} replacements across {total_files} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
