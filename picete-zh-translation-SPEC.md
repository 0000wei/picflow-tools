# PicEte Longtail Pages — Chinese Translation (zh/)

## Background

PicEte already has a Chinese version at `/home/wu/picete-site/zh/`. The existing Chinese pages follow an exact translation pattern of the English pages.

The 15 new longtail pages need Chinese translations created at `/home/wu/picete-site/zh/{page-name}/index.html`.

## Translation Rules

1. **File structure:** Each page goes in `/home/wu/picete-site/zh/{page-name}/index.html`
2. **DOC TYPE:** `<!DOCTYPE html>` with `<html lang="zh">`
3. **URL references** use `../../` to go up two levels (zh/ → picete-site root)
   - CSS: `../../css/style.css`
   - Favicon: `../../favicon.svg`
   - Logo: `../../images/picete-logo.svg`
   - Core tool links: `../../resize-image/` or `../../compress-image/` or `../../png-to-jpg/` etc.
   - Footer links to other tools: `../../compress-image/` etc.
   - Footer Home: `../../`
   - Footer privacy: `../../privacy-policy.html`
   - Partner sites use full URLs (same as English)
4. **Canonical** points to English URL (same as existing zh pages do: `https://picete.com/{page-name}/`)
5. **No hreflang tags** in zh version (existing zh pages don't include them - only canonical)
6. **OG url** points to `https://picete.com/zh/{page-name}/`
7. **Title** format: `{Chinese Translation} | PicEte`
8. **Language selector** defaults to zh (selected)
9. **Breadcrumb:** `首页 › 图片缩放 › {具体尺寸}` for resize, `首页 › 图片压缩 › {具体}` for compress, `首页 › 图片转换 › {具体}` for convert
10. **CTA button text:** `免费使用 PicEte 图片缩放工具 →` or `免费使用 PicEte 图片压缩工具 →` or `免费使用 PicEte 图片转换工具 →`

## Template Reference

Use `/home/wu/picete-site/zh/compress-image-to-100kb/index.html` as the exact template for file structure.

Use the corresponding English page at `/home/wu/picete-site/{page-name}/index.html` for the content to translate.

## Pages to Create (15 pages)

### Resize Pages (8) — CTA links to ../../resize-image/
Breadcrumb: `首页 › 图片缩放 › {具体尺寸}`

1. `zh/resize-image-to-512x512/index.html`
2. `zh/resize-image-to-300x250/index.html`
3. `zh/resize-image-to-600x600/index.html`
4. `zh/resize-image-to-1500x500/index.html`
5. `zh/resize-image-to-200x200/index.html`
6. `zh/resize-image-to-250x250/index.html`
7. `zh/resize-image-to-728x90/index.html`
8. `zh/resize-image-for-facebook-cover/index.html`

### Compress Pages (6) — CTA links to ../../compress-image/
Breadcrumb: `首页 › 图片压缩 › {具体}`

9. `zh/compress-image-to-200kb/index.html`
10. `zh/compress-image-to-500kb/index.html`
11. `zh/compress-jpg-to-100kb/index.html`
12. `zh/compress-image-for-wordpress/index.html`
13. `zh/compress-image-for-website/index.html`
14. `zh/compress-image-for-email/index.html`

### Convert Pages (2) — CTA links:
- jpg-to-png-for-instagram: `../../jpg-to-png/`
- batch-convert-png-to-jpg: `../../png-to-jpg/`
Breadcrumb: `首页 › 图片转换 › {具体}`

15. `zh/jpg-to-png-for-instagram/index.html`
16. `zh/batch-convert-png-to-jpg/index.html`

## Translation Guidelines

- Translate ALL visible text: title, description, H1, H2, headings, paragraphs, bullet lists, FAQ questions/answers, button text, breadcrumb, tagline
- DO NOT translate: schema ld+json name/description fields (keep English as-is, matching existing zh pages)
- DO NOT translate: URLs, file paths, file names
- Keep HTML structure EXACTLY the same as the English original
- Keep CSS and JavaScript exactly the same
- CTA button text examples:
  - Resize: `免费使用 PicEte 图片缩放工具 →`
  - Compress: `免费使用 PicEte 图片压缩工具 →`
  - Convert (jpg-to-png): `免费使用 PicEte JPG 转 PNG 工具 →`
  - Convert (batch png to jpg): `免费使用 PicEte PNG 转 JPG 工具 →`
- For tagline in the header logo area:
  - Resize pages: `图片缩放`
  - Compress pages: `图片压缩`
  - Convert pages: `图片转换`
- Footer "More Tools" heading: `更多工具`
- Footer "About" heading: `关于`
- Footer "Partner Sites" heading: `合作伙伴`
- Footer Back to Home: `返回首页`
- Footer privacy: `隐私政策`
- Footer copyright: keep as `© 2024 PicEte. All rights reserved.` (brand, not translated)
- "Related" section heading: `相关尺寸` or `相关选项`
- FAQ section heading: `常见问题`
- CTA sub-text: `免费 · 无需注册 · 浏览器本地处理`
