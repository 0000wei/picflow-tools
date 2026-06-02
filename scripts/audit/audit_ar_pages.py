"""Audit ar/ pages for English content in meta description, title, H1, and body text."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
AR_DIR = os.path.join(BASE, 'ar')

def has_long_english(text):
    """Check if text has long English phrases (5+ consecutive English words)."""
    en_words = re.findall(r'[a-zA-Z]+', text)
    consecutive = 0
    for w in en_words:
        if len(w) > 2:  # Skip short words like "to", "in"
            consecutive += 1
            if consecutive >= 5:
                return True
        else:
            consecutive = 0
    return False

issues = []
for tool_dir in sorted(os.listdir(AR_DIR)):
    tool_path = os.path.join(AR_DIR, tool_dir)
    if not os.path.isdir(tool_path):
        continue
    idx = os.path.join(tool_path, 'index.html')
    if not os.path.isfile(idx):
        continue

    with open(idx, 'r', encoding='utf-8') as f:
        content = f.read()

    page_issues = []

    # Check meta description
    desc_match = re.search(r'name="description"\s+content="([^"]*)"', content)
    if not desc_match:
        desc_match = re.search(r'content="([^"]*)"\s+name="description"', content)
    if desc_match:
        desc = desc_match.group(1)
        if has_long_english(desc):
            page_issues.append(f"EN description: {desc[:60]}")

    # Check title
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        title = title_match.group(1)
        if has_long_english(title):
            page_issues.append(f"EN title: {title[:60]}")

    # Check H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if h1_match:
        h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
        if has_long_english(h1):
            page_issues.append(f"EN h1: {h1[:60]}")

    # Check body text sections (paragraphs)
    en_paragraphs = 0
    for p_match in re.finditer(r'<p[^>]*>(.*?)</p>', content, re.DOTALL):
        p_text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
        if len(p_text) > 50 and has_long_english(p_text):
            en_paragraphs += 1

    if en_paragraphs > 0:
        page_issues.append(f"EN paragraphs: {en_paragraphs}")

    if page_issues:
        print(f"{tool_dir}:")
        for issue in page_issues:
            print(f"  {issue}".encode('ascii', 'replace').decode())
        issues.append(tool_dir)

print(f"\nTotal pages with English content: {len(issues)}")
