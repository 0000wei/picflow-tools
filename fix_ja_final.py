#!/usr/bin/env python3
"""
最终修复：处理剩余的英文内容和Breadcrumb Home问题
"""

import re
import os

# 扩展的翻译映射
EXTRA_TRANSLATIONS = {
    # image-to-base64 特定翻译
    "Free online Image to Base64 converter. Upload an image or paste a URL to get instant Base64 encoding. Copy as Data URL, HTML, CSS, or Markdown. No upload, 100% private.":
        "無料オンライン画像からBase64変換ツール。画像をアップロードまたはURLを貼り付けて即座にBase64エンコーディングを取得。Data URL、HTML、CSS、またはMarkdownとしてコピー。アップロードなし、100%プライベート。",
    "image to base64, base64 encoder, image to base64 converter, data URL generator, encode image to base64":
        "画像からBase64, Base64エンコーダ, 画像からBase64変換, Data URL生成, 画像をBase64にエンコード",
    "Free online Image to Base64 converter with format options":
        "フォーマットオプション付き無料オンライン画像からBase64変換ツール",

    # image-splitter 特定翻译
    "Free online image splitter tool. Split any image into grid for Instagram, collage, or design. Custom rows and columns. Download individual slices. No upload, runs in your browser.":
        "無料オンライン画像分割ツール。任意の画像をInstagram、コラージュ、またはデザイン用グリッドに分割。カスタム行と列。個別スライスをダウンロード。アップロードなし、ブラウザで実行。",
    "image splitter, split image for instagram, image grid splitter, photo slicer, divide image, free tool":
        "画像分割, Instagram用画像分割, 画像グリッド分割, 写真スライサー, 画像分割, 無料ツール",
    "Free online image splitter tool":
        "無料オンライン画像分割ツール",
}

def fix_breadcrumb_home_final(content):
    """最终修复Breadcrumb中的Home为ホーム"""
    # 更精准的模式匹配，只替换BreadcrumbList中的第一个Home
    pattern = r'("type":\s*"BreadcrumbList".*?"position":\s*1,\s*"name":\s*)"Home"'
    content = re.sub(pattern, r'\1"ホーム"', content, flags=re.DOTALL)
    return content

def fix_remaining_english(content, filepath):
    """修复剩余的英文内容"""
    # 检查文件路径以确定页面类型
    if 'image-to-base64' in filepath:
        for en_text, ja_text in EXTRA_TRANSLATIONS.items():
            if en_text in content:
                content = content.replace(en_text, ja_text)
    elif 'image-splitter' in filepath:
        for en_text, ja_text in EXTRA_TRANSLATIONS.items():
            if en_text in content:
                content = content.replace(en_text, ja_text)

    return content

def fix_file(filepath):
    """修复单个文件"""
    print(f"处理文件: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 进行各种修复
    content = fix_breadcrumb_home_final(content)
    content = fix_remaining_english(content, filepath)

    # 只有当内容确实发生变化时才写回
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 完成修复: {filepath}")
        return True
    else:
        print(f"- 无需修复: {filepath}")
        return False

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

    fixed_count = 0
    # 处理每个文件
    for filepath in html_files:
        try:
            if fix_file(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"✗ 错误处理 {filepath}: {e}")

    print(f"\n完成! 共修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    main()