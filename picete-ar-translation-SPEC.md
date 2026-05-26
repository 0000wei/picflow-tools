# PicEte Arabic Translation (ar/) — 16 Pages

## Background
PicEte needs Arabic translations for 16 new longtail SEO pages. Arabic is RTL (right-to-left), so all pages must include `dir="rtl"` on the `<html>` tag.

## Translation Rules

### Per-language constants
| Element | Arabic |
|---------|--------|
| Lang | `ar` |
| Dir | `rtl` |
| Tagline (resize) | `تغيير حجم الصورة` |
| Tagline (compress) | `ضغط الصورة` |
| Tagline (convert) | `تحويل الصورة` |
| CTA (resize) | `استخدم PicEte لتغيير حجم الصورة مجانًا ←` |
| CTA (compress) | `استخدم PicEte لضغط الصورة مجانًا ←` |
| CTA (convert) | `استخدم PicEte لتحويل الصورة مجانًا ←` |
| Breadcrumb prefix | `الرئيسية` |
| Breadcrumb (resize) | `الرئيسية › تغيير حجم الصورة › {name}` |
| Breadcrumb (compress) | `الرئيسية › ضغط الصورة › {name}` |
| Breadcrumb (convert) | `الرئيسية › تحويل الصورة › {name}` |
| Footer More Tools | `أدوات إضافية` |
| Footer About | `حول` |
| Footer Partners | `مواقع شريكة` |
| Footer Home | `العودة إلى الرئيسية` |
| Footer Privacy | `سياسة الخصوصية` |
| FAQ heading | `الأسئلة الشائعة` |
| Related heading | `أحجام ذات صلة` / `خيارات ذات صلة` |
| CTA sub-text | `مجاني · بدون تسجيل · يعمل في المتصفح` |
| Lang selector | `<option value="ar" selected>العربية</option>` |

### HTML structure rules
- `<html lang="ar" dir="rtl">` (not just lang)
- canonical: `https://picete.com/{name}/` (English URL)
- OG url: `https://picete.com/ar/{name}/`
- All paths use `../../` (e.g. `../../css/style.css`)
- hreflang for all 8 languages (en/zh/ja/de/fr/es/pt/ar + x-default)
- Schema ld+json name/description keep English
- All CSS and JS identical to English version

## Pages to Create (16 total)

### Batch 1: Resize (8 pages)
1. `ar/resize-image-to-512x512/index.html` — tagline: تغيير حجم الصورة
2. `ar/resize-image-to-300x250/index.html`
3. `ar/resize-image-to-600x600/index.html`
4. `ar/resize-image-to-1500x500/index.html`
5. `ar/resize-image-to-200x200/index.html`
6. `ar/resize-image-to-250x250/index.html`
7. `ar/resize-image-to-728x90/index.html`
8. `ar/resize-image-for-facebook-cover/index.html`

### Batch 2: Compress (6 pages)
9. `ar/compress-image-to-200kb/index.html` — tagline: ضغط الصورة
10. `ar/compress-image-to-500kb/index.html`
11. `ar/compress-jpg-to-100kb/index.html`
12. `ar/compress-image-for-wordpress/index.html`
13. `ar/compress-image-for-website/index.html`
14. `ar/compress-image-for-email/index.html`

### Batch 3: Convert (2 pages)
15. `ar/jpg-to-png-for-instagram/index.html` — tagline: تحويل الصورة
16. `ar/batch-convert-png-to-jpg/index.html`

## Execution
For each page: read the EN original at `{name}/index.html`, translate all visible text to Arabic, apply the rules above, write to `ar/{name}/index.html`. Verify file exists after creation.
