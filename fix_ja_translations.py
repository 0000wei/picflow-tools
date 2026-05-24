#!/usr/bin/env python3
"""
批量修复日语页面翻译问题的脚本
修复以下问题：
1. meta description 和 keywords 翻译为日语
2. hreflang 标签指向正确的语言版本
3. schema.org 中的 name 和 description 翻译为日语
4. Open Graph 标签翻译为日语
"""

import re
import os
from pathlib import Path

# 日语翻译映射字典
TRANSLATIONS = {
    # 通用翻译
    "Free online image compressor tool. Smartly compress images to reduce file size. Maintain high quality, supports batch compression, no registration required, local processing for privacy.":
        "無料オンライン画像圧縮ツール。画像を賢く圧縮してファイルサイズを削減。高品質を維持、バッチ圧縮に対応、登録不要、プライバシーを保護するローカル処理。",
    "Free online image resizer tool. Quickly resize images to your desired dimensions. Supports width/height scaling, aspect ratio preservation, batch processing, no registration required, local processing for privacy.":
        "無料オンライン画像リサイズツール。画像を希望の寸法に素早くリサイズ。幅/高さのスケーリング、アスペクト比維持、バッチ処理、登録不要、プライバシーを保護するローカル処理。",
    "Free online color palette extractor. Upload any image and extract its dominant colors. Get HEX, RGB, HSL values with visual swatches and percentages. No upload, private.":
        "無料オンラインカラーパレット抽出ツール。任意の画像をアップロードして支配的な色を抽出。HEX、RGB、HSL値を視覚的なスウォッチと割合で取得。アップロードなし、プライベート。",
    "Free online image splitter tool. Split images into grid for Instagram. Custom rows and columns, supports preview, download individual slices, no registration required, local processing.":
        "無料オンライン画像分割ツール。Instagram用グリッドに画像を分割。カスタム行と列、プレビュー、個別スライスのダウンロード、登録不要、ローカル処理.",
    "Free online image to Base64 converter. Convert images to Base64 strings instantly. Supports multiple formats, batch conversion, no registration required, runs in your browser.":
        "無料オンライン画像からBase64変換ツール。画像を即座にBase64文字列に変換。複数フォーマット、バッチ変換、登録不要、ブラウザで実行.",

    # Keywords
    "image compressor, image compression, online compressor, batch compression, reduce file size, free tool":
        "画像圧縮, 画像圧縮ツール, オンライン圧縮, バッチ圧縮, ファイルサイズ削減, 無料ツール",
    "image resizer, resize image, image dimension changer, online image editor, batch resize, free tool":
        "画像リサイズ, 画像サイズ変更, 画像寸法変更, オンライン画像編集, バッチリサイズ, 無料ツール",
    "color palette extractor, extract colors from image, image color palette generator, color picker from image, dominant color extractor":
        "カラーパレット抽出, 画像から色抽出, 画像カラーパレット生成, 画像からカラーピッカー, 支配的な色抽出",
    "image splitter, split image for instagram, image grid splitter, photo slicer, divide image, free tool":
        "画像分割, Instagram用画像分割, 画像グリッド分割, 写真スライサー, 画像分割, 無料ツール",
    "image to base64, base64 converter, encode image to base64, base64 encoder, image to string, free tool":
        "画像からBase64, Base64変換, 画像をBase64にエンコード, Base64エンコーダ, 画像から文字列, 無料ツール",

    # Open Graph descriptions
    "Free online image compressor tool. Smartly compress images to reduce file size.":
        "無料オンライン画像圧縮ツール。画像を賢く圧縮してファイルサイズを削減。",
    "Free online image resizer tool. Quickly resize images to your desired dimensions.":
        "無料オンライン画像リサイズツール。画像を希望の寸法に素早くリサイズ。",
    "Upload any image and extract its dominant colors. Get HEX, RGB, HSL values with visual swatches. No upload, runs in your browser.":
        "任意の画像をアップロードして支配的な色を抽出。HEX、RGB、HSL値を視覚的なスウォッチで取得。アップロードなし、ブラウザで実行。",
    "Split images into grid for Instagram. Custom rows/columns, preview, download slices.":
        "Instagram用グリッドに画像を分割。カスタム行/列、プレビュー、スライスをダウンロード.",
    "Convert images to Base64 strings instantly. Multiple formats, batch conversion.":
        "画像を即座にBase64文字列に変換。複数フォーマット、バッチ変換.",

    # Schema.org names and descriptions
    "Image Compressor Tool": "画像圧縮ツール",
    "Free online image compressor tool": "無料オンライン画像圧縮ツール",
    "Image Resizer Tool": "画像リサイズツール",
    "Free online image resizer tool": "無料オンライン画像リサイズツール",
    "Color Palette Extractor": "カラーパレット抽出ツール",
    "Free online color palette extractor from images": "画像からカラーパレットを抽出する無料オンラインツール",
    "Image Splitter": "画像分割ツール",
    "Free online image splitter tool": "無料オンライン画像分割ツール",
    "Image to Base64 Converter": "画像からBase64変換ツール",
    "Free online image to Base64 converter": "無料オンライン画像からBase64変換ツール",

    # Breadcrumb names
    "Home": "ホーム",
    "Image Compressor": "画像圧縮",
    "Image Resizer": "画像リサイズ",
    "Color Palette Extractor": "カラーパレット抽出",
    "Image Splitter": "画像分割",
    "Image to Base64": "画像からBase64",
}

# 页面特定的翻译映射
PAGE_SPECIFIC = {
    "compress-image": {
        "title": "画像圧縮 - 無料オンライン画像圧縮ツール | PicEte",
        "name": "画像圧縮ツール",
        "breadcrumb": "画像圧縮"
    },
    "resize-image": {
        "title": "画像リサイズ - 無料オンライン画像リサイズツール | PicEte",
        "name": "画像リサイズツール",
        "breadcrumb": "画像リサイズ"
    },
    "extract-colors": {
        "title": "カラーパレット抽出 - 画像から色を抽出する無料オンラインツール | PicEte",
        "name": "カラーパレット抽出ツール",
        "breadcrumb": "カラーパレット抽出"
    },
    "image-splitter": {
        "title": "画像分割 - Instagram用グリッドに画像を分割する無料オンラインツール | PicEte",
        "name": "画像分割ツール",
        "breadcrumb": "画像分割"
    },
    "image-to-base64": {
        "title": "画像からBase64 - 無料オンライン画像Base64変換ツール | PicEte",
        "name": "画像からBase64変換ツール",
        "breadcrumb": "画像からBase64"
    }
}

def get_page_key(filepath):
    """从文件路径获取页面key"""
    path_parts = filepath.split('/')
    if 'index.html' in path_parts:
        dir_name = path_parts[-2]
        return dir_name
    return None

def fix_hreflang(content, page_path):
    """修复hreflang标签"""
    # 提取页面相对路径
    if '/ja/index.html' in page_path:
        page_rel_path = ''
    else:
        page_rel_path = page_path.split('/ja/')[1].replace('index.html', '')

    # 构建正确的hreflang标签
    hreflang_block = f'''    <!-- hreflang 标签 -->
    <link rel="alternate" hreflang="en" href="https://picete.com/{page_rel_path}" />
    <link rel="alternate" hreflang="zh" href="https://picete.com/zh/{page_rel_path}" />
    <link rel="alternate" hreflang="ja" href="https://picete.com/ja/{page_rel_path}" />
    <link rel="alternate" hreflang="de" href="https://picete.com/de/{page_rel_path}" />
    <link rel="alternate" hreflang="fr" href="https://picete.com/fr/{page_rel_path}" />
    <link rel="alternate" hreflang="es" href="https://picete.com/es/{page_rel_path}" />
    <link rel="alternate" hreflang="pt" href="https://picete.com/pt/{page_rel_path}" />
    <link rel="alternate" hreflang="ar" href="https://picete.com/ar/{page_rel_path}" />
    <link rel="alternate" hreflang="x-default" href="https://picete.com/{page_rel_path}" />'''

    # 使用正则表达式替换hreflang块
    pattern = r'    <!-- hreflang 标签 -->.*?(?=\n\n    <!--|$)'
    content = re.sub(pattern, hreflang_block, content, flags=re.DOTALL)

    return content

def fix_opengraph_url(content, page_path):
    """修复Open Graph URL"""
    # 提取正确的ja页面路径
    if '/ja/index.html' in page_path:
        og_url = 'https://picete.com/ja/'
    else:
        page_rel_path = page_path.split('/ja/')[1].replace('index.html', '')
        og_url = f'https://picete.com/ja/{page_rel_path}'

    # 替换og:url
    content = re.sub(
        r'<meta property="og:url" content="[^"]*"',
        f'<meta property="og:url" content="{og_url}">',
        content
    )

    return content

def fix_schema_urls(content, page_path):
    """修复schema.org中的URL"""
    # 提取正确的ja页面路径
    if '/ja/index.html' in page_path:
        ja_url = 'https://picete.com/ja/'
        en_url = 'https://picete.com/'
    else:
        page_rel_path = page_path.split('/ja/')[1].replace('index.html', '')
        ja_url = f'https://picete.com/ja/{page_rel_path}'
        en_url = f'https://picete.com/{page_rel_path}'

    # 替换WebApplication URL
    content = re.sub(
        r'"url":\s*"https://picete\.com/[^"]*"',
        f'"url": "{ja_url}"',
        content
    )

    # 替换Breadcrumb中的URL
    content = re.sub(
        r'"item":\s*"https://picete\.com/"',
        '"item": "https://picete.com/ja/"',
        content
    )

    # 替换Breadcrumb中的第二个URL
    content = re.sub(
        r'"item":\s*"https://picete\.com/([^/"]*/)"',
        lambda m: f'"item": "https://picete.com/ja/{m.group(1)}"' if m.group(1) else '"item": "https://picete.com/ja/"',
        content
    )

    return content

def translate_text(text, page_key=None):
    """翻译文本"""
    # 首先尝试直接匹配
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]

    # 如果有页面特定翻译，尝试使用
    if page_key and page_key in PAGE_SPECIFIC:
        spec = PAGE_SPECIFIC[page_key]
        if text in spec.values():
            return text  # 已经是正确的翻译

    return text  # 没有找到翻译，返回原文

def fix_meta_tags(content, page_key=None):
    """修复meta标签"""
    # 修复description
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', content)
    if desc_match:
        desc_text = desc_match.group(1)
        # 检查是否是英文（简单检查：包含英文单词且不包含日文字符）
        if re.search(r'[a-zA-Z]{3,}', desc_text) and not re.search(r'[぀-ゟ゠-ヿ]', desc_text):
            translated = translate_text(desc_text, page_key)
            if translated != desc_text:
                content = content.replace(desc_text, translated)

    # 修复keywords
    keywords_match = re.search(r'<meta name="keywords" content="([^"]*)"', content)
    if keywords_match:
        keywords_text = keywords_match.group(1)
        if re.search(r'[a-zA-Z]{3,}', keywords_text) and not re.search(r'[぀-ゟ゠-ヿ]', keywords_text):
            translated = translate_text(keywords_text, page_key)
            if translated != keywords_text:
                content = content.replace(keywords_text, translated)

    return content

def fix_opengraph_tags(content, page_key=None):
    """修复Open Graph标签"""
    # 修复og:title
    og_title_match = re.search(r'<meta property="og:title" content="([^"]*)"', content)
    if og_title_match:
        title_text = og_title_match.group(1)
        if re.search(r'[A-Z][a-z]{3,}', title_text) and not re.search(r'[぀-ゟ゠-ヿ]', title_text):
            # 检查是否有页面特定的标题
            if page_key and page_key in PAGE_SPECIFIC:
                spec = PAGE_SPECIFIC[page_key]
                if 'title' in spec:
                    content = re.sub(
                        r'<meta property="og:title" content="[^"]*"',
                        f'<meta property="og:title" content="{spec["title"]}">',
                        content
                    )

    # 修复og:description
    og_desc_match = re.search(r'<meta property="og:description" content="([^"]*)"', content)
    if og_desc_match:
        desc_text = og_desc_match.group(1)
        if re.search(r'[A-Z][a-z]{3,}', desc_text) and not re.search(r'[぀-ゟ゠-ヿ]', desc_text):
            translated = translate_text(desc_text, page_key)
            if translated != desc_text:
                content = re.sub(
                    f'<meta property="og:description" content="{re.escape(desc_text)}"',
                    f'<meta property="og:description" content="{translated}"',
                    content
                )

    return content

def fix_schema_tags(content, page_key=None):
    """修复schema.org标签"""
    # 修复WebApplication name
    name_match = re.search(r'"name":\s*"([^"]*)"(?:\s*,\s*"description":\s*"([^"]*)")?', content)
    if name_match:
        name_text = name_match.group(1)
        if re.search(r'[A-Z][a-z]{3,}', name_text) and not re.search(r'[぀-ゟ゠-ヿ]', name_text):
            # 检查是否有页面特定的name
            if page_key and page_key in PAGE_SPECIFIC:
                spec = PAGE_SPECIFIC[page_key]
                if 'name' in spec:
                    content = re.sub(
                        f'"name":\s*"{re.escape(name_text)}"',
                        f'"name": "{spec["name"]}"',
                        content
                    )

    # 修复description
    desc_match = re.search(r'"description":\s*"([^"]*)"', content)
    if desc_match:
        desc_text = desc_match.group(1)
        if re.search(r'[A-Z][a-z]{3,}', desc_text) and not re.search(r'[぀-ゟ゠-ヿ]', desc_text):
            translated = translate_text(desc_text, page_key)
            if translated != desc_text:
                content = re.sub(
                    f'"description":\s*"{re.escape(desc_text)}"',
                    f'"description": "{translated}"',
                    content
                )

    # 修复Breadcrumb name
    breadcrumb_pattern = r'"position":\s*2,\s*"name":\s*"([^"]*)"'
    breadcrumb_match = re.search(breadcrumb_pattern, content)
    if breadcrumb_match:
        breadcrumb_text = breadcrumb_match.group(1)
        if re.search(r'[A-Z][a-z]{3,}', breadcrumb_text) and not re.search(r'[぀-ゟ゠-ヿ]', breadcrumb_text):
            # 检查是否有页面特定的breadcrumb
            if page_key and page_key in PAGE_SPECIFIC:
                spec = PAGE_SPECIFIC[page_key]
                if 'breadcrumb' in spec:
                    content = re.sub(
                        f'"position":\s*2,\s*"name":\s*"{re.escape(breadcrumb_text)}"',
                        f'"position": 2, "name": "{spec["breadcrumb"]}"',
                        content
                    )

    return content

def fix_file(filepath):
    """修复单个文件"""
    print(f"处理文件: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 获取页面key
    page_key = get_page_key(filepath)

    # 进行各种修复
    content = fix_meta_tags(content, page_key)
    content = fix_hreflang(content, filepath)
    content = fix_opengraph_url(content, filepath)
    content = fix_opengraph_tags(content, page_key)
    content = fix_schema_urls(content, filepath)
    content = fix_schema_tags(content, page_key)

    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ 完成修复: {filepath}")

def main():
    """主函数"""
    base_path = '/home/wu/picete-site/ja'

    # 获取所有需要处理的index.html文件
    html_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == 'index.html':
                html_files.append(os.path.join(root, file))

    print(f"找到 {len(html_files)} 个需要处理的文件")

    # 处理每个文件
    for filepath in html_files:
        try:
            fix_file(filepath)
        except Exception as e:
            print(f"✗ 错误处理 {filepath}: {e}")

    print("\n所有文件处理完成!")

if __name__ == '__main__':
    main()