#!/usr/bin/env python3
"""
修复image-splitter页面的剩余英文内容
"""

import os

def fix_image_splitter():
    """修复image-splitter页面"""
    filepath = '/home/wu/picete-site/ja/image-splitter/index.html'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换剩余的英文内容
    replacements = {
        'Free online image grid splitter. Slice any photo into a grid for Instagram, carousel, or puzzle layouts. Custom rows, columns, and formats. 100% free, no registration, local processing.':
        '無料オンライン画像グリッド分割ツール。Instagram、カルーセル、パズルレイアウト用に任意の写真をグリッドにスライス。カスタム行、列、フォーマット。100%無料、登録不要、ローカル処理。',

        'image grid splitter, photo slicer, instagram grid maker, split image into grid, photo grid maker, online image splitter':
        '画像グリッド分割, 写真スライサー, Instagramグリッドメーカー, 画像をグリッドに分割, 写真グリッドメーカー, オンライン画像分割',

        'Free online image grid splitter. Slice any photo into a grid. Custom rows, columns, formats. No upload, runs in your browser.':
        '無料オンライン画像グリッド分割ツール。任意の写真をグリッドにスライス。カスタム行、列、フォーマット。アップロードなし、ブラウザで実行。',

        'Free online image grid splitter for Instagram and social media':
        'Instagramやソーシャルメディア用の無料オンライン画像グリッド分割ツール'
    }

    modified = False
    for en_text, ja_text in replacements.items():
        if en_text in content:
            content = content.replace(en_text, ja_text)
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ 修复完成: image-splitter")
    else:
        print("- 无需修复: image-splitter")

if __name__ == '__main__':
    fix_image_splitter()