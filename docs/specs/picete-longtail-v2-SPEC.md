# PicEte Longtail Pages v2 — SPEC

## Background

PicEte (picete.com) is a free online image tool site. Currently has 24 pages in sitemap. Goal: add 15 more longtail SEO pages to cover more specific search keywords.

Each page follows the exact same template as `resize-image-to-512x512/index.html` (already created in the project). 

## Template Reference

Use `/home/wu/picete-site/resize-image-to-512x512/index.html` as the exact template. Every page must:
- Be a complete, valid HTML file (NOT just a fragment)
- Have the full header with hreflang for all 8 languages (en/zh/ja/de/fr/es/pt/ar + x-default)
- Have the full language switcher + theme toggle JS
- Have the full footer with "More Tools", "About", "Partner Sites" sections
- Have breadcrumb: Home › [Tool Category] › [Specific Use]
- Have FAQ section with 4 questions unique to that page's topic
- Have schema ld+json (WebApplication + FAQPage)
- Have 3 content sections inside the hero area (background div) + a use cases section
- Link to the core tool: `../resize-image/` or `../compress-image/` or `../png-to-jpg/` etc.
- Call-to-action button: "Use PicEte [Tool Name] Free →" linking to the core tool

## Pages to Create

### Group A: Resize Scene Pages (7 pages)

All follow template of `resize-image-to-512x512/index.html`. CTA links to `../resize-image/`.

1. `resize-image-to-300x250/index.html`
   - Title: "Resize Image to 300x250 - Free Display Ad Banner Size Converter | PicEte"
   - Description: "Resize images to 300x250 pixels for display ads and banner placements. Free online tool to convert any image to 300x250 medium rectangle format."
   - Breadcrumb: Home › Image Resizer › 300x250
   - H1: "Resize Image to 300x250"
   - H2: "Standard Medium Rectangle Ad Size"
   - Keyword angle: 300x250 is the most common display ad format
   - Related links: resize-image-to-728x90, resize-image-512x512, resize-image-1080x1080

2. `resize-image-to-600x600/index.html`
   - Title: "Resize Image to 600x600 - Free E-Commerce Product Photo Resizer | PicEte"
   - Description: "Resize images to 600x600 pixels for e-commerce product photos. Free online tool to convert any image to perfect square product format."
   - Breadcrumb: Home › Image Resizer › 600x600
   - H1: "Resize Image to 600x600"
   - H2: "Perfect E-Commerce Product Photo Size"
   - Keyword angle: eBay, Amazon, Shopify product photo standard
   - Related links: resize-image-to-800x800, resize-image-to-512x512, resize-image-to-1080x1080

3. `resize-image-to-1500x500/index.html`
   - Title: "Resize Image to 1500x500 - Free Twitter Header Banner Resizer | PicEte"
   - Description: "Resize images to 1500x500 pixels for Twitter/X profile banners. Free online tool to create the perfect Twitter header size."
   - Breadcrumb: Home › Image Resizer › 1500x500
   - H1: "Resize Image to 1500x500"
   - H2: "Twitter/X Profile Banner Size"
   - Keyword angle: Twitter header banner dimensions
   - Related links: resize-image-to-1200x630, resize-image-to-1920x1080, resize-image-1080x1080

4. `resize-image-to-200x200/index.html`
   - Title: "Resize Image to 200x200 - Free Small Thumbnail Resizer | PicEte"
   - Description: "Resize images to 200x200 pixels for thumbnails and small avatars. Free online tool to create tiny square images."
   - Breadcrumb: Home › Image Resizer › 200x200
   - H1: "Resize Image to 200x200"
   - H2: "Small Thumbnail & Avatar Size"
   - Keyword angle: small thumbnails, comment avatars, forum profile pics
   - Related links: resize-image-to-250x250, resize-image-to-512x512, resize-image-to-800x800

5. `resize-image-to-250x250/index.html`
   - Title: "Resize Image to 250x250 - Free Profile Avatar Resizer | PicEte"
   - Description: "Resize images to 250x250 pixels for avatars and profile pictures. Free online tool for perfect square avatar sizing."
   - Breadcrumb: Home › Image Resizer › 250x250
   - H1: "Resize Image to 250x250"
   - H2: "Standard Avatar & Profile Picture Size"
   - Keyword angle: avatars, profile pictures, forum icons
   - Related links: resize-image-to-200x200, resize-image-to-512x512, resize-image-to-300x250

6. `resize-image-to-728x90/index.html`
   - Title: "Resize Image to 728x90 - Free Leaderboard Ad Banner Resizer | PicEte"
   - Description: "Resize images to 728x90 pixels for leaderboard banner ads. Free online tool to create standard ad banner sizes."
   - Breadcrumb: Home › Image Resizer › 728x90
   - H1: "Resize Image to 728x90"
   - H2: "Standard Leaderboard Ad Size"
   - Keyword angle: IAB standard leaderboard ad format, AdSense banner
   - Related links: resize-image-to-300x250, resize-image-to-1500x500, resize-image-1920x1080

7. `resize-image-for-facebook-cover/index.html`
   - Title: "Resize Image for Facebook Cover - Free Facebook Banner Size Tool | PicEte"
   - Description: "Resize images to Facebook cover photo size. Free online tool to create the perfect Facebook profile banner dimensions."
   - Breadcrumb: Home › Image Resizer › Facebook Cover
   - H1: "Resize Image for Facebook Cover"
   - H2: "Perfect Facebook Profile Banner Size"
   - Keyword angle: Facebook cover photo dimensions (851x315 recommended), Facebook banner
   - Related links: resize-image-to-1500x500, resize-image-to-1200x630, resize-image-1080x1080
   - FAQ topics: Facebook cover dimensions, mobile vs desktop display

### Group B: Compress Scene Pages (6 pages)

All follow template of `compress-image-to-100kb/index.html`. CTA links to `../compress-image/`.
Breadcrumb: Home › Image Compressor › [Specific]

8. `compress-image-to-200kb/index.html`
   - Breadcrumb: Home › Image Compressor › 200KB
   - Title: "Compress Image to 200KB - Free Online File Size Reducer | PicEte"
   - Description: "Compress images to under 200KB. Free online tool to reduce image file size to 200KB while maintaining good quality."
   - FAQ topics: 200KB limit, document upload requirements, quality vs size tradeoff

9. `compress-image-to-500kb/index.html`
   - Breadcrumb: Home › Image Compressor › 500KB
   - Title: "Compress Image to 500KB - Free Online Image Size Optimizer | PicEte"
   - Description: "Compress images to under 500KB. Free online tool to reduce file size to 500KB for email and web uploads."
   - FAQ topics: email attachment limits, web upload requirements, image quality

10. `compress-jpg-to-100kb/index.html`
    - Breadcrumb: Home › Image Compressor › JPG 100KB
    - Title: "Compress JPG to 100KB - Free Online JPEG Size Reducer | PicEte"
    - Description: "Compress JPG images to exactly 100KB. Free online tool to reduce JPEG file size to 100KB for applications."
    - FAQ topics: JPG-specific compression, photo quality, batch JPG compression

11. `compress-image-for-wordpress/index.html`
    - Breadcrumb: Home › Image Compressor › WordPress
    - Title: "Compress Image for WordPress - Free Website Image Optimizer | PicEte"
    - Description: "Compress images optimized for WordPress websites. Free online tool to reduce image sizes for faster WordPress loading."
    - FAQ topics: WordPress image optimization, page speed, recommended sizes, WebP support

12. `compress-image-for-website/index.html`
    - Breadcrumb: Home › Image Compressor › Website
    - Title: "Compress Image for Website - Free Web Image Optimizer | PicEte"
    - Description: "Compress images for websites. Free online tool to optimize images for web use - smaller files, faster loading."
    - FAQ topics: web optimization, page speed, image formats for web, responsive images

13. `compress-image-for-email/index.html`
    - Breadcrumb: Home › Image Compressor › Email
    - Title: "Compress Image for Email - Free Email Attachment Size Reducer | PicEte"
    - Description: "Compress images for email attachments. Free online tool to reduce image sizes so they fit within email size limits."
    - FAQ topics: email attachment limits (Gmail 25MB, Outlook 20MB), batch email compression

### Group C: Convert Scene Pages (2 pages)

All follow template of `png-to-jpg-for-email/index.html`. 

14. `jpg-to-png-for-instagram/index.html`
    - Breadcrumb: Home › Image Converter › JPG to PNG for Instagram
    - Title: "Convert JPG to PNG for Instagram - Free Transparent PNG Creator | PicEte"
    - Description: "Convert JPG images to PNG for Instagram. Free online tool to get high-quality PNG files with transparency support."
    - CTA links to `../jpg-to-png/`
    - Keyword angle: Instagram PNG uploads, lossless quality for social media
    - FAQ topics: JPG vs PNG for Instagram, transparency, image quality

15. `batch-convert-png-to-jpg/index.html`
    - Breadcrumb: Home › Image Converter › Batch PNG to JPG
    - Title: "Batch Convert PNG to JPG - Free Bulk Image Format Converter | PicEte"
    - Description: "Batch convert multiple PNG files to JPG format at once. Free online bulk PNG to JPG converter."
    - CTA links to `../png-to-jpg/`
    - Keyword angle: batch processing, bulk conversion, multiple files
    - FAQ topics: batch limits, processing speed, downloading individual vs all

## Execution

Create ALL 14 pages (index.html in each subdirectory). Each must be a complete, valid HTML document matching the template structure exactly. Use the directory: ~/picete-site/
