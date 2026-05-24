#!/usr/bin/env python3
"""
修复hreflang x-default指向英文版本的问题
"""

import os
import glob

def fix_hreflang_xdefault(content):
    """修复hreflang x-default指向英文版本"""
    # 查找x-default标签，应该指向英文版本(不带语言代码)
    content = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="https://picete\.com/ja/([^"]*)" />',
        r'<link rel="alternate" hreflang="x-default" href="https://picete.com/\1" />',
        content
    )

    # 处理根路径情况
    content = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="https://picete\.com/ja/" />',
        r'<link rel="alternate" hreflang="x-default" href="https://picete.com/" />',
        content
    )

    return content

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 修复x-default
    content = fix_hreflang_xdefault(content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 修复完成: {os.path.basename(os.path.dirname(filepath))}")
        return True
    else:
        return False

def main():
    """主函数"""
    base_path = '/home/wu/picete-site/ja'

    # 获取所有需要处理的index.html文件
    html_files = glob.glob(os.path.join(base_path, '*/index.html'))
    html_files.extend(glob.glob(os.path.join(base_path, '*/*/index.html')))

    print(f"找到 {len(html_files)} 个需要处理的文件")

    fixed_count = 0
    # 处理每个文件
    for filepath in sorted(html_files):
        try:
            if fix_file(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"✗ 错误处理 {filepath}: {e}")

    print(f"\n完成! 共修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    import re
    main()