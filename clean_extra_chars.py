#!/usr/bin/env python3
"""
清理多余的字符和格式问题
"""

import os
import re
import glob

def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    modified = False

    # 修复多余的 >> 符号
    content = content.replace('">>"', '">')
    content = content.replace('"> >', '">')
    content = content.replace('> >', '>')

    # 修复其他多余的 > 符号
    content = re.sub(r'">\s*>"', '">', content)
    content = re.sub(r'\s+>', '>', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 清理完成: {os.path.basename(os.path.dirname(filepath))}")
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

    print(f"\n完成! 共清理了 {fixed_count} 个文件")

if __name__ == '__main__':
    main()