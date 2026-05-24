#!/usr/bin/env python3
"""
简单直接修复Breadcrumb中的Home为ホーム
"""

import os
import glob

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 简单直接的替换
    modified = False

    # 替换BreadcrumbList中的Home为ホーム
    # 寻找 "position": 1, 后面的 "name": "Home"
    if '"position": 1' in content and '"name": "Home"' in content:
        # 使用更简单的方法：直接替换
        content = content.replace('"position": 1,\n            "name": "Home"', '"position": 1,\n            "name": "ホーム"')
        content = content.replace('"position": 1, \n            "name": "Home"', '"position": 1, \n            "name": "ホーム"')
        content = content.replace('"position":1,\n            "name": "Home"', '"position": 1,\n            "name": "ホーム"')
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 修复完成: {os.path.basename(os.path.dirname(filepath))}")
        return True
    else:
        print(f"- 无需修复: {os.path.basename(os.path.dirname(filepath))}")
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
    main()