#!/usr/bin/env python3
"""Inject JSON-LD (WebApplication + BreadcrumbList) into ja stub HTML pages.
These pages are 19-line stubs (no </head>, no </body>, no JSON-LD).
Strategy: append to end of file: JSON-LD blocks + </head> + empty body + </body></html>"""

import os, re, json, sys

os.chdir('/home/wu/桌面/knowledge-base/06项目/哥飞建站/picete')

# Template pages for JSON-LD reference (en versions)
# Map ja stub page -> en reference page for JSON-LD content
pages = {
    'png-to-webp-for-wordpress': {'name': 'PNG to WebP for WordPress Converter', 'desc': 'Convert PNG to WebP optimized for WordPress'},
    'resize-image-to-1080x1080': {'name': 'Resize Image to 1080x1080', 'desc': 'Resize image to 1080x1080 pixels (Instagram square)'},
    'resize-image-to-1200x630': {'name': 'Resize Image to 1200x630', 'desc': 'Resize image to 1200x630 pixels (Facebook link share)'},
    'resize-image-to-1920x1080': {'name': 'Resize Image to 1920x1080', 'desc': 'Resize image to 1920x1080 pixels (HD wallpaper)'},
    'resize-image-to-800x800': {'name': 'Resize Image to 800x800', 'desc': 'Resize image to 800x800 pixels'},
    'split-image-into-3x3': {'name': 'Image Grid Splitter (3x3)', 'desc': 'Split an image into a 3x3 grid'},
    'split-image-into-4-parts': {'name': 'Image Splitter (4 Parts)', 'desc': 'Split an image into 4 equal parts'},
    'webp-to-png-for-website': {'name': 'WebP to PNG for Website', 'desc': 'Convert WebP to PNG for website compatibility'},
}

for tool, meta in pages.items():
    path = f'ja/{tool}/index.html'
    if not os.path.isfile(path):
        print(f'  SKIP: {path} not found')
        continue
    
    with open(path) as f:
        content = f.read()
    
    # Check if already has JSON-LD
    if 'ld+json' in content:
        print(f'  SKIP: {path} already has JSON-LD ({content.count("<script")} scripts)')
        continue
    
    # Build JSON-LD blocks
    webapp = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": meta['name'],
        "description": meta['desc'],
        "url": f"https://picete.com/ja/{tool}",
        "applicationCategory": "MultimediaApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://picete.com/"},
            {"@type": "ListItem", "position": 2, "name": meta['name'], "item": f"https://picete.com/ja/{tool}/"}
        ]
    }
    
    ld_json = f'\n<script type="application/ld+json">\n{json.dumps(webapp, indent=2, ensure_ascii=False)}\n</script>\n<script type="application/ld+json">\n{json.dumps(breadcrumb, indent=2, ensure_ascii=False)}\n</script>\n</head>\n<body>\n</body>\n</html>\n'
    
    # Strip trailing whitespace/newlines, append JSON-LD
    content = content.rstrip() + ld_json
    
    with open(path, 'w') as f:
        f.write(content)
    
    print(f'  ✅ {path}: injected 2 JSON-LD blocks (was {os.path.getsize(path)} bytes)')

# Verify
print('\n=== 验证 ===')
for tool in pages:
    path = f'ja/{tool}/index.html'
    with open(path) as f:
        c = f.read()
    n = len(re.findall(r'<script type="application/ld\+json">', c))
    has_head = '</head>' in c
    has_body = '</body>' in c
    print(f'  {tool}: JSON-LD={n}, </head>={has_head}, </body>={has_body}')

print('\n✅ 完成')
