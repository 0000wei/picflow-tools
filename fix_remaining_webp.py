#!/usr/bin/env python3
"""
修复剩余的WebP相关页面翻译
"""

import re
import os

# WebP页面翻译
WEBP_TRANSLATIONS = {
    "jpg-to-webp": {
        "description": "無料オンラインJPGからWebP変換ツール。JPG画像を素早くWebPフォーマットに変換。品質を維持しながらファイルサイズを削減。登録不要、プライバシーを保護するローカル処理。",
        "keywords": "JPGからWebP, JPEGからWebP, オンライン変換, バッチ変換, 画像圧縮, 無料ツール",
        "og_title": "JPGからWebP - 無料オンラインJPGからWebP変換ツール",
        "og_description": "無料オンラインJPGからWebP変換ツール、品質を維持しながらファイルサイズを削減。",
        "schema_name": "JPGからWebP変換ツール",
        "schema_description": "無料オンラインJPGからWebP変換ツール",
        "breadcrumb_name": "JPGからWebP"
    },
    "png-to-webp": {
        "description": "無料オンラインPNGからWebP変換ツール。PNG画像を素早くWebPフォーマットに変換。品質を維持しながらファイルサイズを大幅に削減。登録不要、プライバシーを保護するローカル処理。",
        "keywords": "PNGからWebP, オンライン変換, バッチ変換, 画像圧縮, 無料ツール",
        "og_title": "PNGからWebP - 無料オンラインPNGからWebP変換ツール",
        "og_description": "無料オンラインPNGからWebP変換ツール、品質を維持しながらファイルサイズを大幅に削減。",
        "schema_name": "PNGからWebP変換ツール",
        "schema_description": "無料オンラインPNGからWebP変換ツール",
        "breadcrumb_name": "PNGからWebP"
    },
    "image-splitter": {
        "description": "無料オンライン画像グリッド分割ツール。Instagram、カルーセル、パズルレイアウト用に任意の写真をグリッドにスライス。カスタム行、列、フォーマット。100%無料、登録不要、ローカル処理。",
        "keywords": "画像グリッド分割, 写真スライサー, Instagramグリッドメーカー, 画像をグリッドに分割, 写真グリッドメーカー, オンライン画像分割",
        "og_description": "無料オンライン画像グリッド分割ツール。任意の写真をグリッドにスライス。カスタム行、列、フォーマット。アップロードなし、ブラウザで実行。",
        "schema_description": "Instagramやソーシャルメディア用の無料オンライン画像グリッド分割ツール"
    }
}

def fix_webp_page(filepath, page_key):
    """修复WebP页面"""
    if page_key not in WEBP_TRANSLATIONS:
        return False

    translations = WEBP_TRANSLATIONS[page_key]

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 替换description
    content = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{translations["description"]}">',
        content
    )

    # 替换keywords
    content = re.sub(
        r'<meta name="keywords" content="[^"]*"',
        f'<meta name="keywords" content="{translations["keywords"]}">',
        content
    )

    # 替换og:title
    content = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{translations["og_title"]}">',
        content
    )

    # 替换og:description
    content = re.sub(
        r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="{translations["og_description"]}">',
        content
    )

    # 替换schema中的name和description
    content = re.sub(
        r'"name":\s*"[^"]*",\s*"description":\s*"[^"]*",\s*"url"',
        f'"name": "{translations["schema_name"]}", "description": "{translations["schema_description"]}", "url"',
        content
    )

    # 替换breadcrumb中的name (只替换WebP相关的)
    if page_key in ["jpg-to-webp", "png-to-webp"]:
        content = re.sub(
            r'"position":\s*2,\s*"name":\s*"[^"]*WebP[^"]*"',
            f'"position": 2, "name": "{translations["breadcrumb_name"]}"',
            content
        )

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    base_path = '/home/wu/picete-site/ja'

    fixed_count = 0
    for page_key in WEBP_TRANSLATIONS.keys():
        filepath = os.path.join(base_path, page_key, 'index.html')
        if os.path.exists(filepath):
            try:
                if fix_webp_page(filepath, page_key):
                    print(f"✓ 修复完成: {page_key}")
                    fixed_count += 1
                else:
                    print(f"- 无需修复: {page_key}")
            except Exception as e:
                print(f"✗ 错误处理 {page_key}: {e}")

    print(f"\n完成! 共修复了 {fixed_count} 个WebP页面")

if __name__ == '__main__':
    main()