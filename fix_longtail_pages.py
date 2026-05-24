#!/usr/bin/env python3
"""
修复长尾SEO页面的翻译问题
"""

import re
import os

# 长尾页面的翻译映射
LONGTAIL_TRANSLATIONS = {
    "split-image-into-4-parts": {
        "title": "画像を4分割 - 無料2x2グリッド作成ツール | PicEte",
        "description": "画像を4等分に分割。ソーシャルメディア、印刷、クリエイティブプロジェクト用の2x2グリッドに写真を分割する無料オンラインツール。",
        "keywords": "画像を4分割, 2x2グリッド, 写真分割, 画像分割, 4分割",
        "og_title": "画像を4分割 - 無料2x2グリッド作成ツール",
        "og_description": "画像を4等分に分割。ソーシャルメディア、印刷、クリエイティブプロジェクト用の2x2グリッドに写真を分割。",
        "schema_name": "画像4分割ツール",
        "schema_description": "画像を4等分に分割する無料オンラインツール",
        "breadcrumb_name": "画像を4分割"
    },
    "split-image-into-3x3": {
        "title": "画像を9分割 - 無料3x3グリッド作成ツール | PicEte",
        "description": "画像を9等分に分割。Instagram用3x3グリッドに写真を分割する無料オンラインツール。パズル効果、カルーセル投稿に最適。",
        "keywords": "画像を9分割, 3x3グリッド, Instagram分割, 写真スライサー, 画像分割",
        "og_title": "画像を9分割 - 無料3x3グリッド作成ツール",
        "og_description": "画像を9等分に分割。Instagram用3x3グリッドに写真を分割。パズル効果、カルーセル投稿に最適。",
        "schema_name": "画像9分割ツール",
        "schema_description": "画像を9等分に分割する無料オンラインツール",
        "breadcrumb_name": "画像を9分割"
    },
    "resize-image-to-800x800": {
        "title": "画像を800x800にリサイズ - 無料オンラインツール | PicEte",
        "description": "画像を800x800ピクセルにリサイズ。製品写真、ソーシャルメディア、Instagram用に最適化。高品質、アスペクト比維持、バッチ処理対応。",
        "keywords": "画像を800x800にリサイズ, 800x800リサイザ, 製品写真リサイズ, Instagram写真リサイズ",
        "og_title": "画像を800x800にリサイズ - 無料オンラインツール",
        "og_description": "画像を800x800ピクセルにリサイズ。製品写真、ソーシャルメディアに最適化。",
        "schema_name": "画像800x800リサイザ",
        "schema_description": "画像を800x800ピクセルにリサイズする無料オンラインツール",
        "breadcrumb_name": "画像800x800リサイズ"
    },
    "resize-image-to-1080x1080": {
        "title": "画像を1080x1080にリサイズ - Instagram正方形リサイザ | PicEte",
        "description": "画像を1080x1080ピクセルにリサイズ。Instagram投稿に最適な正方形サイズ。高品質、アスペクト比維持、バッチ処理対応。",
        "keywords": "画像を1080x1080にリサイズ, Instagram正方形リサイズ, 1080x1080リサイザ, IG投稿サイズ",
        "og_title": "画像を1080x1080にリサイズ - Instagram正方形リサイザ",
        "og_description": "画像を1080x1080ピクセルにリサイズ。Instagram投稿に最適な正方形サイズ。",
        "schema_name": "画像1080x1080リサイザ",
        "schema_description": "画像を1080x1080ピクセルにリサイズする無料オンラインツール",
        "breadcrumb_name": "画像1080x1080リサイズ"
    },
    "resize-image-to-1200x630": {
        "title": "画像を1200x630にリサイズ - ソーシャルシェア画像リサイザ | PicEte",
        "description": "画像を1200x630ピクセルにリサイズ。Facebook、Twitter、LinkedInのシェア画像に最適なOGPサイズ。高品質、バッチ処理対応。",
        "keywords": "画像を1200x630にリサイズ, ソーシャルシェア画像, OGPサイズ, Facebook画像サイズ",
        "og_title": "画像を1200x630にリサイズ - ソーシャルシェア画像リサイザ",
        "og_description": "画像を1200x630ピクセルにリサイズ。Facebook、Twitter、LinkedInのシェア画像に最適。",
        "schema_name": "画像1200x630リサイザ",
        "schema_description": "画像を1200x630ピクセルにリサイズする無料オンラインツール",
        "breadcrumb_name": "画像1200x630リサイズ"
    },
    "resize-image-to-1920x1080": {
        "title": "画像を1920x1080にリサイズ - HD壁紙リサイザ | PicEte",
        "description": "画像を1920x1080ピクセルにリサイズ。Full HD壁紙、YouTubeサムネイル、プレゼンテーションに最適。高品質、アスペクト比維持。",
        "keywords": "画像を1920x1080にリサイズ, HD壁紙リサイズ, 1920x1080リサイザ, FHDサイズ",
        "og_title": "画像を1920x1080にリサイズ - HD壁紙リサイザ",
        "og_description": "画像を1920x1080ピクセルにリサイズ。HD壁紙、YouTubeサムネイルに最適。",
        "schema_name": "画像1920x1080リサイザ",
        "schema_description": "画像を1920x1080ピクセルにリサイズする無料オンラインツール",
        "breadcrumb_name": "画像1920x1080リサイズ"
    },
    "compress-image-to-50kb": {
        "title": "画像を50KB以下に圧縮 - 無料オンライン圧縮ツール | PicEte",
        "description": "画像を50KB以下に圧縮。公式書類、メール添付、Webアップロード用のファイルサイズ制限対応。高品質維持、バッチ処理。",
        "keywords": "画像を50KBに圧縮, ファイルサイズ削減, 画像圧縮, 50KB以下",
        "og_title": "画像を50KB以下に圧縮 - 無料オンライン圧縮ツール",
        "og_description": "画像を50KB以下に圧縮。公式書類、メール添付、Webアップロード用のファイルサイズ制限対応。",
        "schema_name": "画像50KB圧縮ツール",
        "schema_description": "画像を50KB以下に圧縮する無料オンラインツール",
        "breadcrumb_name": "画像50KB圧縮"
    },
    "compress-image-to-100kb": {
        "title": "画像を100KB以下に圧縮 - 無料オンライン圧縮ツール | PicEte",
        "description": "画像を100KB以下に圧縮。Webアップロード、メール添付、フォーム提出用のファイルサイズ制限対応。高品質維持、バッチ処理。",
        "keywords": "画像を100KBに圧縮, ファイルサイズ削減, 画像圧縮, 100KB以下",
        "og_title": "画像を100KB以下に圧縮 - 無料オンライン圧縮ツール",
        "og_description": "画像を100KB以下に圧縮。Webアップロード、メール添付、フォーム提出用のファイルサイズ制限対応。",
        "schema_name": "画像100KB圧縮ツール",
        "schema_description": "画像を100KB以下に圧縮する無料オンラインツール",
        "breadcrumb_name": "画像100KB圧縮"
    },
    "compress-jpg-to-200kb": {
        "title": "JPGを200KB以下に圧縮 - 無料オンライン圧縮ツール | PicEte",
        "description": "JPG画像を200KB以下に圧縮。LinkedIn、求人サイト、公式書類用のファイルサイズ制限対応。高品質維持、バッチ処理。",
        "keywords": "JPGを200KBに圧縮, JPEG圧縮, ファイルサイズ削減, 200KB以下",
        "og_title": "JPGを200KB以下に圧縮 - 無料オンライン圧縮ツール",
        "og_description": "JPG画像を200KB以下に圧縮。LinkedIn、求人サイト、公式書類用のファイルサイズ制限対応。",
        "schema_name": "JPG 200KB圧縮ツール",
        "schema_description": "JPG画像を200KB以下に圧縮する無料オンラインツール",
        "breadcrumb_name": "JPG 200KB圧縮"
    },
    "png-to-jpg-for-email": {
        "title": "メール用PNGからJPG変換 - 無料オンラインツール | PicEte",
        "description": "メール添付用にPNGをJPGに変換。ファイルサイズを削減して送信制限対応。高品質、バッチ変換、プライベート処理。",
        "keywords": "メール用PNGからJPG, メール添付画像, PNGからJPG変換, ファイルサイズ削減",
        "og_title": "メール用PNGからJPG変換 - 無料オンラインツール",
        "og_description": "メール添付用にPNGをJPGに変換。ファイルサイズを削減して送信制限対応。",
        "schema_name": "メール用PNGからJPG変換ツール",
        "schema_description": "メール添付用にPNGをJPGに変換する無料オンラインツール",
        "breadcrumb_name": "メール用PNGからJPG"
    },
    "png-to-webp-for-wordpress": {
        "title": "WordPress用PNGからWebP変換 - 無料オンラインツール | PicEte",
        "description": "WordPressサイト用にPNGをWebPに変換。サイト速度向上、帯域幅節約、SEO改善。高品質、バッチ変換、最適化。",
        "keywords": "WordPress用PNGからWebP, WebP変換, サイト最適化, 画像圧縮",
        "og_title": "WordPress用PNGからWebP変換 - 無料オンラインツール",
        "og_description": "WordPressサイト用にPNGをWebPに変換。サイト速度向上、帯域幅節約、SEO改善。",
        "schema_name": "WordPress用PNGからWebP変換ツール",
        "schema_description": "WordPressサイト用にPNGをWebPに変換する無料オンラインツール",
        "breadcrumb_name": "WordPress用PNGからWebP"
    },
    "webp-to-png-for-website": {
        "title": "Webサイト用WebPからPNG変換 - 無料オンラインツール | PicEte",
        "description": "Webサイト用にWebPをPNGに変換。互換性向上、透明度保持、高品質。バッチ変換、プライベート処理。",
        "keywords": "Webサイト用WebPからPNG, WebPからPNG変換, 画像互換性, 透明度保持",
        "og_title": "Webサイト用WebPからPNG変換 - 無料オンラインツール",
        "og_description": "Webサイト用にWebPをPNGに変換。互換性向上、透明度保持、高品質。",
        "schema_name": "Webサイト用WebPからPNG変換ツール",
        "schema_description": "Webサイト用にWebPをPNGに変換する無料オンラインツール",
        "breadcrumb_name": "Webサイト用WebPからPNG"
    }
}

def fix_longtail_page(filepath, page_key):
    """修复长尾页面"""
    if page_key not in LONGTAIL_TRANSLATIONS:
        return False

    translations = LONGTAIL_TRANSLATIONS[page_key]

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    page_rel_path = page_key + '/'

    # 替换title
    content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{translations["title"]}</title>',
        content
    )

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
        r'"name":\s*"[^"]*",\s*"description":\s*"[^"]*"',  # WebApplication
        f'"name": "{translations["schema_name"]}", "description": "{translations["schema_description"]}"',
        content
    )

    # 替换breadcrumb中的name
    content = re.sub(
        r'"position":\s*2,\s*"name":\s*"[^"]*"',
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
    for page_key in LONGTAIL_TRANSLATIONS.keys():
        filepath = os.path.join(base_path, page_key, 'index.html')
        if os.path.exists(filepath):
            try:
                if fix_longtail_page(filepath, page_key):
                    print(f"✓ 修复完成: {page_key}")
                    fixed_count += 1
                else:
                    print(f"- 无需修复: {page_key}")
            except Exception as e:
                print(f"✗ 错误处理 {page_key}: {e}")

    print(f"\n完成! 共修复了 {fixed_count} 个长尾页面")

if __name__ == '__main__':
    main()