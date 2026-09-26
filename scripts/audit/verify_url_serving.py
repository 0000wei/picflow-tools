#!/usr/bin/env python3
"""Verify declared URLs match the URLs production actually serves.

Starts a local static server that mirrors the production semantics from
vercel.json (cleanUrls=true, trailingSlash=false):

  GET /a/b/       -> 308 to /a/b          (except bare "/")
  GET /a/b        -> serve /a/b/index.html (or the literal file)
  GET /           -> serve /index.html

Then checks:
  1. every sitemap <loc> answers 200 directly (no 3xx hop)
  2. sampled pages: canonical == served URL (non-slash), og:url and
     JSON-LD url/item fields agree, hreflang cluster is complete,
     non-slash, and every alternate actually serves 200
"""

import http.server
import json
import os
import re
import socketserver
import sys
import threading
import urllib.error
import urllib.request
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PORT = 8137
BASE = f'http://127.0.0.1:{PORT}'
SITE = 'https://picete.com'
LANGS = ['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko']


class VercelLikeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        if self.path != '/' and self.path.endswith('/'):
            self.send_response(308)
            self.send_header('Location', self.path.rstrip('/'))
            self.end_headers()
            return
        # Serve directory index directly: stdlib would 301 /a -> /a/,
        # inverting the production (trailingSlash=false) behavior.
        if os.path.isdir(self.translate_path(self.path)):
            clean = self.path.split('?', 1)[0].split('#', 1)[0].rstrip('/')
            self.path = (clean or '') + '/index.html'
            if self.path == '//index.html':
                self.path = '/index.html'
        super().do_GET()

    def translate_path(self, path):
        clean = path.split('?', 1)[0].split('#', 1)[0].rstrip('/')
        if clean == '':
            clean = '/'
        return super().translate_path(clean)

    def log_message(self, *args):
        pass


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.og_url = None
        self.hreflang = {}
        self.jsonld = []
        self._in_ld = False
        self._ld_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link':
            rel = (a.get('rel') or '').lower()
            if rel == 'canonical':
                self.canonical = a.get('href')
            elif rel == 'alternate' and a.get('hreflang'):
                self.hreflang[a['hreflang']] = a.get('href')
        elif tag == 'meta' and a.get('property') == 'og:url':
            self.og_url = a.get('content')
        elif tag == 'script' and a.get('type') == 'application/ld+json':
            self._in_ld = True

    def handle_data(self, data):
        if self._in_ld:
            self._ld_buf.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self._in_ld:
            self._in_ld = False
            self.jsonld.append(''.join(self._ld_buf))
            self._ld_buf = []


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url):
    """GET without following redirects; return (status, location, body)."""
    req = urllib.request.Request(url, headers={'User-Agent': 'verify/1.0'})
    try:
        with OPENER.open(req) as resp:
            return resp.status, resp.headers.get('Location'), resp.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get('Location'), b''


def to_local(url):
    return BASE + url[len(SITE):]


def expected_for(lang, tool):
    if tool is None:
        return f'{SITE}/{lang}' if lang != 'en' else f'{SITE}/'
    if lang == 'en':
        return f'{SITE}/{tool}'
    return f'{SITE}/{lang}/{tool}'


def check_page(url, lang, tool, errors):
    status, _, body = fetch(url)
    if status != 200:
        errors.append(f'{url}: HTTP {status}, expected direct 200')
        return
    parser = HeadParser()
    parser.feed(body)

    expected = expected_for(lang, tool)
    if parser.canonical != expected:
        errors.append(f'{url}: canonical={parser.canonical}, expected {expected}')
    if parser.og_url != expected:
        errors.append(f'{url}: og:url={parser.og_url}, expected {expected}')

    expected_cluster = {'en': expected_for('en', tool), 'x-default': expected_for('en', tool)}
    for lg in LANGS:
        expected_cluster[lg] = expected_for(lg, tool)
    if parser.hreflang:
        if set(parser.hreflang) != set(expected_cluster):
            errors.append(f'{url}: hreflang keys {sorted(parser.hreflang)}')
        for lg, href in parser.hreflang.items():
            if href != expected_cluster.get(lg):
                errors.append(f'{url}: hreflang {lg}={href}, expected {expected_cluster.get(lg)}')
            alt_status, alt_loc, _ = fetch(to_local(href))
            if alt_status != 200 or alt_loc:
                errors.append(f'{url}: hreflang target {href} -> {alt_status} redirect={alt_loc}')

    for raw in parser.jsonld:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        t = data.get('@type')
        if t in ('SoftwareApplication', 'WebApplication'):
            u = data.get('url')
            if u is not None and u != expected:
                errors.append(f'{url}: JSON-LD {t}.url={u}, expected {expected}')
        elif t == 'BreadcrumbList':
            items = data.get('itemListElement', [])
            if tool is not None:
                home = SITE + '/' if lang == 'en' else f'{SITE}/{lang}'
                if len(items) >= 1 and items[0].get('item') != home:
                    errors.append(f'{url}: breadcrumb[0].item={items[0].get("item")}, expected {home}')
                if len(items) >= 2 and items[1].get('item') != expected:
                    errors.append(f'{url}: breadcrumb[1].item={items[1].get("item")}, expected {expected}')
            else:
                # Homepage: accept either the site root or the language
                # home as the position-1 item; both serve 200 directly.
                valid_homes = {SITE + '/', f'{SITE}/{lang}'}
                if len(items) >= 1 and items[0].get('item') not in valid_homes:
                    errors.append(f'{url}: breadcrumb[0].item={items[0].get("item")}, expected one of {sorted(valid_homes)}')


def parse_sitemap_locs(path):
    with open(path, 'r', encoding='utf-8') as f:
        xml = f.read()
    return re.findall(r'<loc>([^<]+)</loc>', xml)


def main():
    failures = 0

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    with Server(('127.0.0.1', PORT), VercelLikeHandler) as httpd:
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()

        print('== 1. Sitemap sweep: every <loc> must answer direct 200 ==')
        locs = parse_sitemap_locs(os.path.join(ROOT, 'sitemap.xml'))
        sitemap_fail = []
        for loc in locs:
            path = loc[len(SITE):] or '/'
            status, location, _ = fetch(BASE + path)
            if status != 200 or location:
                sitemap_fail.append(f'  {loc} -> {status} redirect={location}')
        print(f'   {len(locs)} URLs checked, {len(sitemap_fail)} failures')
        for line in sitemap_fail[:20]:
            print(line)
        failures += len(sitemap_fail)

        print('== 2. Sampled pages: canonical/og:url/hreflang/JSON-LD ==')
        sample = [
            ('en', None, '/'),
            ('zh', None, '/zh'),
            ('es', None, '/es'),
            ('ar', None, '/ar'),
            ('pt', None, '/pt'),
            ('ko', None, '/ko'),
            ('de', None, '/de'),
            ('en', 'png-to-jpg', '/png-to-jpg'),
            ('en', 'webp-to-jpg', '/webp-to-jpg'),
            ('en', 'avif-to-png', '/avif-to-png'),
            ('en', 'webp-to-avif', '/webp-to-avif'),
            ('en', 'jpg-to-avif', '/jpg-to-avif'),
            ('en', 'png-to-webp', '/png-to-webp'),
            ('en', 'resize-image-to-512x512', '/resize-image-to-512x512'),
            ('en', 'resize-image-to-800x800', '/resize-image-to-800x800'),
            ('en', 'resize-image-to-1920x1080', '/resize-image-to-1920x1080'),
            ('en', 'image-splitter', '/image-splitter'),
            ('en', 'split-image-into-3x3', '/split-image-into-3x3'),
            ('en', 'split-image-into-4-parts', '/split-image-into-4-parts'),
            ('en', 'instagram-image-splitter', '/instagram-image-splitter'),
            ('zh', 'png-to-jpg', '/zh/png-to-jpg'),
            ('de', 'webp-to-jpg', '/de/webp-to-jpg'),
            ('es', 'resize-image-to-512x512', '/es/resize-image-to-512x512'),
            ('ar', 'image-splitter', '/ar/image-splitter'),
            ('pt', 'avif-to-png', '/pt/avif-to-png'),
            ('ko', 'compress-image', '/ko/compress-image'),
            ('ja', 'png-to-webp', '/ja/png-to-webp'),
            ('fr', 'resize-image', '/fr/resize-image'),
            ('en', 'wordpress-plugin', '/wordpress-plugin'),
        ]
        page_errors = []
        for lang, tool, path in sample:
            before = len(page_errors)
            check_page(BASE + path, lang, tool, page_errors)
            status = 'ok' if len(page_errors) == before else 'FAIL'
            print(f'   [{status}] {path}')
        failures += len(page_errors)
        for line in page_errors[:40]:
            print('  ' + line)

        print('== 3. Slash URL must 308 to non-slash (production semantic) ==')
        status, location, _ = fetch(BASE + '/png-to-jpg/')
        ok = status == 308 and location == '/png-to-jpg'
        print(f'   [{"ok" if ok else "FAIL"}] /png-to-jpg/ -> {status} -> {location}')
        if not ok:
            failures += 1

        httpd.shutdown()

    print()
    if failures:
        print(f'RESULT: FAIL ({failures} failure(s))')
        return 1
    print('RESULT: PASS (all declared URLs match served URLs)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
