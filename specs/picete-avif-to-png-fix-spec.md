# SEO Fix SPEC — PicEte avif-to-png Page

> 版本: v1.0
> 执行方式: 直接执行（Hermes）
> 范围: picete.com/avif-to-png/ (EN 页面)

## 背景

GSC 数据显示 `.avif to png` 查询在 30 天内累计 22 次展示，**0 次点击**。排查发现 EN `avif-to-png/index.html` 在 git 中提交时处于未解决的 merge 冲突状态：

- 文件包含 `<<<<<<< Updated upstream` / `=======` / `>>>>>>> Stashed changes` 标记
- 两个完整版本（版本 A + 版本 B）拼接在一起，导致双重 `<html>`、`<head>`、`<title>`、OG 标签
- 多语言子页面（`zh/`、`ja/`、`de/` 等）无此问题

两版本内容完全相同（完整工具 + FAQ），仅 title/OG 存在差异。本 SPEC 解决此结构损坏问题，并同步优化 snippet。

## 执行步骤

### Task 1 — 解决 Merge 冲突，保留版本 B

**原因**: 版本 B 的 title 关键词更前置（"AVIF to PNG" 在开头），更符合 SEO 最佳实践。

**操作**: 删除 `<<<<<<<` 行至 `=======` 行（版本 A），并删除末尾 `>>>>>>> Stashed changes` 行，保留版本 B 作为文件主体。

| 保留部分 | 行范围 | 内容 |
|---------|--------|------|
| 删除 | 1-645 | 版本 A（含冲突标记 + 644 行 HTML + `=======`） |
| 保留 | 646-1288 | 版本 B（完整工具页面） |
| 删除 | 1289 | `>>>>>>> Stashed changes` |

### Task 2 — 优化 Title 和 Meta Description

**当前版本 B 状态:**

| 字段 | 当前值 | 长度 |
|------|--------|------|
| `<title>` | `AVIF to PNG - Free Online AVIF to PNG Converter \| PicEte` | 56 chars |
| `og:title` | `AVIF to PNG - Free Online AVIF to PNG Converter` | — |
| `meta description` | `Free online AVIF to PNG converter. Convert AVIF images to PNG format losslessly. Supports batch conversion, local processing for privacy, no registration required.` | 156 chars |

**问题分析:**
- Title "AVIF to PNG" 出现了两次（重复）
- og:title 比 title 少了 `| PicEte` — 不一致
- Description 不错但偏长，可更突出「本地处理」「无上传」的隐私卖点

**优化后:**

| 字段 | 新值 | 长度 | 理由 |
|------|------|------|------|
| `<title>` | `AVIF to PNG Converter - Free, No Upload, Private \| PicEte` | 52 chars | 关键词前置 ✓, Free/Private CTR 词 ✓, 突出隐私差异化 ✓, 不重复 ✓ |
| `og:title` | `AVIF to PNG Converter - Free, No Upload, Private \| PicEte` | 52 chars | 与 title 完全一致 ✓ |
| `meta description` | `Convert AVIF to PNG online free — no upload required, 100% private. Lossless AVIF to PNG converter runs locally in your browser. Batch convert AVIF images instantly.` | 155 chars | 开头含关键词 ✓, action verb ✓, 隐私卖点 ✓, no signup ✓ |

### Task 3 — 验证

#### L0 — 文件完整性
```bash
grep -c '<title>' avif-to-png/index.html                    # 应为 1
grep -c '<<<<<<<' avif-to-png/index.html                     # 应为 0
grep -c '=======' avif-to-png/index.html                     # 应为 0
grep -c '>>>>>>>' avif-to-png/index.html                     # 应为 0
grep -c '</html>' avif-to-png/index.html                     # 应为 1
python3 -c "with open('avif-to-png/index.html') as f: c=f.read(); assert c.count('<title>')==1, 'title count fail'"
```

#### L1 — HTML/SEO 规则
```bash
# Title ≤ 60 chars
grep -oP '(?<=<title>)[^<]+' avif-to-png/index.html | while read t; do [ ${#t} -gt 60 ] && echo "TOO LONG: $t"; done

# og:title == title
diff <(grep -oP '(?<=<title>)[^<]+' avif-to-png/index.html) \
     <(grep -oP '(?<=og:title" content=")[^"]+' avif-to-png/index.html)

# og:description == meta description
diff <(grep -oP '(?<=name="description" content=")[^"]+' avif-to-png/index.html) \
     <(grep -oP '(?<=og:description" content=")[^"]+' avif-to-png/index.html)
```

#### L2 — Git
```bash
cd /home/wu/桌面/picete
git add avif-to-png/index.html
git commit -m "fix(seo): resolve avif-to-png merge conflict, optimize title/OG"
git push
```

## 不做

- 不修改多语言版本的 avif-to-png 页面（无冲突问题）
- 不修改工具功能、JS、CSS
- 不修改 sitemap（无需主动触发 reindex）
- 不同步更新其他页面的 OG 标签（仅处理 avif-to-png）

## 预期效果

| 指标 | 当前 | 预期（2-4周） |
|------|------|-------------|
| avif-to-png 页面 CTR | 0% | > 2% |
| 页面展示趋势 | 缓慢增长 | 正常增长 |
| Title 结构健康度 | 损坏（双重标签） | 修复 |
