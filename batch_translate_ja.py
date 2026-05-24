#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成PicEte日语SEO页面
"""
import os
import re

# 定义剩余需要处理的页面及其翻译映射
pages_data = [
    {
        "source": "/home/wu/picete-site/png-to-webp-for-wordpress/index.html",
        "target": "/home/wu/picete-site/ja/png-to-webp-for-wordpress/index.html",
        "translations": {
            "Convert PNG to WebP for WordPress": "WordPress用にPNGをWebPに変換",
            "Free Performance Optimizer": "無料パフォーマンス最適化ツール",
            "PNG to WebP for WordPress": "WordPress用にPNGをWebPに変換",
            "Speed Up Your WordPress Site": "WordPressサイトを高速化",
            "Large PNG images slow down WordPress sites": "大きなPNG画像はWordPressサイトを遅くします",
            "Converting to WebP can reduce file sizes by 70-90%": "WebPに変換すると、ファイルサイズを70-90%削減できます",
            "Why Use WebP for WordPress?": "WordPressでWebPを使用する理由",
            "Does WordPress support WebP natively?": "WordPressはWebPをネイティブにサポートしていますか？",
            "How much will converting PNG to WebP speed up my WordPress site?": "PNGをWebPに変換すると、WordPressサイトはどのくらい高速化されますか？",
            "Do I need a plugin to serve WebP on WordPress?": "WordPressでWebPを配信するにはプラグインが必要ですか？",
            "Will conversion affect image transparency for WordPress?": "変換はWordPressの画像透明度に影響しますか？",
            "Frequently Asked Questions": "よくある質問",
            "More Tools": "その他のツール",
            "About": "について",
            "Back to Home": "ホームに戻る",
            "Privacy Policy": "プライバシーポリシー",
            "Partner Sites": "パートナーサイト",
            "Screenshot Mockup": "スクリーンショットモックアップ",
            "Color Tools": "カラーツール",
            "Image Compressor": "画像圧縮",
            "Image Resizer": "画像サイズ変更",
            "PNG to JPG": "PNGからJPGへ",
            "WebP to PNG": "WebPからPNGへ",
            "PNG to WebP": "PNGからWebPへ",
            "Home": "ホーム",
            "More Tools": "その他のツール"
        }
    },
    {
        "source": "/home/wu/picete-site/resize-image-to-1080x1080/index.html",
        "target": "/home/wu/picete-site/ja/resize-image-to-1080x1080/index.html",
        "translations": {
            "Resize Image to 1080x1080": "画像を1080x1080にサイズ変更",
            "Free Instagram Post Size Converter": "無料Instagram投稿サイズコンバータ",
            "Resize Image to 1080x1080": "画像を1080x1080にサイズ変更",
            "Perfect Instagram Post Size": "完璧なInstagram投稿サイズ",
            "Need to resize an image to 1080x1080 pixels": "画像を1080x1080ピクセルにサイズ変更する必要がありますか？",
            "Instagram posts": "Instagram投稿",
            "Why 1080x1080 for Instagram?": "Instagramで1080x1080を使用する理由",
            "How PicEte Resizes to 1080x1080": "PicEteが1080x1080にサイズ変更する方法",
            "Use Cases for 1080x1080 Images": "1080x1080画像の使用例",
            "Frequently Asked Questions": "よくある質問",
            "Why is 1080×1080 a common image size?": "1080×1080は一般的な画像サイズなのはなぜですか？",
            "Will my image be cropped or stretched to fit 1080×1080?": "画像は1080×1080に合わせて切り取られたり引き伸ばされたりしますか？",
            "How fast is batch resizing to 1080×1080?": "1080×1080への一括サイズ変更はどのくらい速いですか？",
            "Is this resize tool free?": "このサイズ変更ツールは無料ですか？",
            "Related Image Sizes": "関連する画像サイズ",
            "More Resize Options": "その他のサイズ変更オプション",
            "Resize to 1920x1080": "1920x1080にサイズ変更",
            "YouTube thumbnails": "YouTubeサムネイル",
            "Resize to 800x800": "800x800にサイズ変更",
            "E-commerce product photos": "ECサイトの商品写真",
            "Resize to 1200x630": "1200x630にサイズ変更",
            "Social media cards": "ソーシャルメディアカード",
            "Free • No signup • Works in your browser": "無料 • 登録不要 • ブラウザで動作"
        }
    }
]

def translate_page(source_path, target_path, translations):
    """翻译单个HTML页面"""
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 设置语言为日语
    content = re.sub(r'<html lang="en">', '<html lang="ja">', content)

    # 更新canonical链接
    canonical_match = re.search(r'<link rel="canonical" href="https://picete\.com/([^"]+?)">', content)
    if canonical_match:
        original_path = canonical_match.group(1)
        new_canonical = f'<link rel="canonical" href="https://picete.com/ja/{original_path}">'
        content = re.sub(r'<link rel="canonical" href="https://picete\.com/([^"]+?)">', new_canonical, content)

    # 更新OG URL
    og_url_match = re.search(r'<meta property="og:url" content="https://picete\.com/([^"]+?)">', content)
    if og_url_match:
        original_path = og_url_match.group(1)
        new_og_url = f'<meta property="og:url" content="https://picete.com/ja/{original_path}">'
        content = re.sub(r'<meta property="og:url" content="https://picete\.com/([^"]+?)">', new_og_url, content)

    # 更新Schema URL
    schema_url_matches = re.findall(r'"url":\s*"https://picete\.com/([^"]+)"', content)
    for match in schema_url_matches:
        old_schema_url = f'"url": "https://picete.com/{match}"'
        new_schema_url = f'"url": "https://picete.com/ja/{match}"'
        content = content.replace(old_schema_url, new_schema_url)

    # 应用翻译
    for en_text, ja_text in translations.items():
        content = content.replace(en_text, ja_text)

    # 更新内部链接为日语版本
    content = re.sub(r'href="../([^"]+?)"', lambda m: f'href="/ja/{m.group(1)}/' if m.group(1).count('/') == 0 else f'href="../{m.group(1)}', content)
    content = re.sub(r'href="\.\./([^"]+)/"', r'href="/ja/\1/"', content)
    content = re.sub(r'href="\.\./"', 'href="../"', content)  # 主页链接保持不变

    # 确保目录存在
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    # 写入目标文件
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Created: {target_path}")

def main():
    """批量处理所有页面"""
    print("开始批量翻译日语页面...")

    for page_data in pages_data:
        source_path = page_data["source"]
        target_path = page_data["target"]
        translations = page_data["translations"]

        print(f"Processing: {source_path}")
        translate_page(source_path, target_path, translations)

    print("\n✅ 所有页面翻译完成！")

if __name__ == "__main__":
    main()