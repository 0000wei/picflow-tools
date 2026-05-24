#!/usr/bin/env python3
"""
第二轮修复：解决脚本生成的问题
1. 修复多余的 > 符号
2. 修复重复的 /ja/ 路径
3. 修复Breadcrumb中的 "Home" 为 "ホーム"
"""

import re
import os

def fix_og_tags(content):
    """修复Open Graph标签中的多余 > 符号"""
    # 查找并修复多余的 > 符号
    content = re.sub(r'>\s*>', '>', content)
    content = re.sub(r'">\s*>', '">', content)
    return content

def fix_duplicate_ja_path(content):
    """修复重复的 /ja/ 路径"""
    # 修复 https://picete.com/ja/ja/ 为 https://picete.com/ja/
    content = re.sub(r'https://picete\.com/ja/ja/', 'https://picete.com/ja/', content)
    return content

def fix_breadcrumb_home(content):
    """修复Breadcrumb中的Home为ホーム"""
    # 只修复BreadcrumbList中的Home
    content = re.sub(
        r'"type":\s*"BreadcrumbList".*?"position":\s*1,\s*"name":\s*"Home"',
        '"type": "BreadcrumbList", "position": 1, "name": "ホーム"',
        content,
        flags=re.DOTALL
    )
    return content

def fix_file(filepath):
    """修复单个文件"""
    print(f"处理文件: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 进行各种修复
    content = fix_og_tags(content)
    content = fix_duplicate_ja_path(content)
    content = fix_breadcrumb_home(content)

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