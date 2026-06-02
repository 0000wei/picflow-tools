#!/usr/bin/env python3
"""
F5: Inject hreflang tags into ar/ and zh/ pages that are missing them.

Logic:
- Scans ar/, zh/ tool pages and ar/index.html
- If hreflang count == 0 → inject full 9 tags (en, zh, ja, de, fr, es, pt, ar, x-default)
- If hreflang count == 9 → skip (already complete)
- Injection point: after <link rel="canonical" .../> line, before <!-- Open Graph -->

Usage: python3 scripts/fix/f5_hreflang.py
"""

import os
import re
import sys

PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LANGUAGES = ["en", "zh", "ja", "de", "fr", "es", "pt", "ar"]

def hreflang_block(tool_path):
    """
    Generate the 9 hreflang <link> tags for a given tool path.
    tool_path examples:
      - "" (empty for homepage)
      - "compress-image" (for a tool page)
    
    Root (English): https://picete.com/{tool_path}/
    Other langs:    https://picete.com/{lang}/{tool_path}/
    """
    # Normalize: strip leading/trailing slashes
    tool_path = tool_path.strip("/")
    
    lines = []
    lines.append("    <!-- hreflang 标签 -->")
    
    for lang in LANGUAGES:
        if lang == "en":
            href = f"https://picete.com/{tool_path}/" if tool_path else "https://picete.com/"
        else:
            href = f"https://picete.com/{lang}/{tool_path}/" if tool_path else f"https://picete.com/{lang}/"
        lines.append(f'    <link rel="alternate" hreflang="{lang}" href="{href}" />')
    
    # x-default → same as English
    xdefault_href = f"https://picete.com/{tool_path}/" if tool_path else "https://picete.com/"
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="{xdefault_href}" />')
    
    return "\n".join(lines)


def get_tool_path(filepath):
    """
    Extract the tool path from a file path.
    Examples:
      ar/index.html → ""
      ar/compress-image/index.html → "compress-image"
      zh/batch-convert-png-to-jpg/index.html → "batch-convert-png-to-jpg"
    """
    rel = os.path.relpath(filepath, PROJECT)
    parts = rel.split(os.sep)
    if len(parts) == 2 and parts[1] == "index.html":
        # Language homepage: ar/index.html → tool_path=""
        return ""
    elif len(parts) == 3 and parts[2] == "index.html":
        # Tool page: ar/compress-image/index.html → tool_path="compress-image"
        return parts[1]
    return None


def count_hreflang(content):
    """Count hreflang attributes in the file content."""
    return len(re.findall(r'hreflang="[^"]*"', content))


def inject_hreflang(content, tool_path):
    """Inject hreflang block after the canonical link tag."""
    block = hreflang_block(tool_path)
    
    # Find the canonical link tag and insert after it
    # Pattern: <link ... rel="canonical" ... />
    # The canonical link is followed by <!-- Open Graph --> in most files
    canonical_pattern = re.compile(
        r'(<link[^>]*rel="canonical"[^>]*/>)',
        re.IGNORECASE
    )
    
    match = canonical_pattern.search(content)
    if match:
        canonical_tag = match.group(1)
        # Insert hreflang block after the canonical tag (before newline)
        replacement = canonical_tag + "\n" + block
        new_content = content.replace(canonical_tag, replacement, 1)
        return new_content
    
    # Fallback: insert after <title> tag
    title_pattern = re.compile(r'(</title>)', re.IGNORECASE)
    match = title_pattern.search(content)
    if match:
        replacement = match.group(1) + "\n" + block
        new_content = content.replace(match.group(1), replacement, 1)
        return new_content
    
    return None


def main():
    print("=" * 60)
    print("F5: 补全 hreflang 标签")
    print("=" * 60)
    
    modified = []
    skipped_complete = []
    errors = []
    
    # Collect all HTML files to check
    files_to_check = []
    
    # ar/index.html
    ar_index = os.path.join(PROJECT, "ar", "index.html")
    if os.path.exists(ar_index):
        files_to_check.append(ar_index)
    
    # ar/ tool pages
    for entry in sorted(os.listdir(os.path.join(PROJECT, "ar"))):
        tool_dir = os.path.join(PROJECT, "ar", entry)
        tool_index = os.path.join(tool_dir, "index.html")
        if os.path.isdir(tool_dir) and os.path.exists(tool_index):
            files_to_check.append(tool_index)
    
    # zh/ tool pages (not zh/index.html — that's homepage, already has hreflang)
    for entry in sorted(os.listdir(os.path.join(PROJECT, "zh"))):
        tool_dir = os.path.join(PROJECT, "zh", entry)
        tool_index = os.path.join(tool_dir, "index.html")
        if os.path.isdir(tool_dir) and os.path.exists(tool_index):
            files_to_check.append(tool_index)
    
    for filepath in files_to_check:
        relpath = os.path.relpath(filepath, PROJECT)
        tool_path = get_tool_path(filepath)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            errors.append(f"  ❌ {relpath}: read error: {e}")
            continue
        
        count = count_hreflang(content)
        
        if count == 9:
            skipped_complete.append(relpath)
            continue
        
        if count > 0 and count != 9:
            errors.append(f"  ⚠️  {relpath}: unexpected hreflang count={count}, skipping")
            continue
        
        # count == 0: inject hreflang
        new_content = inject_hreflang(content, tool_path)
        if new_content is None or new_content == content:
            errors.append(f"  ❌ {relpath}: failed to inject hreflang (no insertion point)")
            continue
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            modified.append(relpath)
        except Exception as e:
            errors.append(f"  ❌ {relpath}: write error: {e}")
    
    # Report
    print(f"\n✅ 已修复 ({len(modified)} 页):")
    for p in sorted(modified):
        print(f"   + {p}")
    
    print(f"\n⏭️  已跳过 — 完整 9 条 ({len(skipped_complete)} 页):")
    for p in sorted(skipped_complete):
        print(f"   = {p}")
    
    print(f"\n❌ 错误 ({len(errors)}):")
    for e in errors:
        print(f"   {e}")
    
    print(f"\n📊 总计: {len(modified)} 修改 | {len(skipped_complete)} 已完整 | {len(errors)} 错误")
    
    return 0 if len(errors) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
