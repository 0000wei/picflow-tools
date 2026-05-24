#!/usr/bin/env python3
"""
Add FAQPage schema + visible FAQ section to all PicEte sub-pages.
Targets: all 10 main tool pages + 12 long-tail pages.
"""

import re
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── FAQ content per page ──────────────────────────────────────────────

FAQ_DATA = {
    # ── Conversion tools ──
    "png-to-jpg": {
        "tool": "PNG to JPG Converter",
        "faqs": [
            ("Does PNG to JPG conversion affect image quality?",
             "Yes, JPG uses lossy compression, so there is some quality loss. Our tool lets you adjust the quality from 10% to 100%. For most web uses, 80-90% quality produces visually identical results to the original PNG while cutting file size by 80% or more. Set it higher for prints and archival where every pixel matters."),
            ("Will I lose transparency converting PNG to JPG?",
             "Yes. JPG does not support transparency. Any transparent areas in your PNG will be filled with white. If you need to preserve transparency, consider keeping the original PNG or using a format like WebP that supports both transparency and good compression."),
            ("How fast is the PNG to JPG conversion?",
             "The conversion is instant and happens entirely in your browser using Canvas technology. Even large files or batch conversions complete in milliseconds. The speed depends on your device's processing power, but there is no server upload or waiting."),
            ("How many PNG files can I convert at once?",
             "There is no limit on the number of files. Select a whole folder of PNGs and convert them all at once. Each image is processed independently, and you can download them individually or click 'Download All' to get everything in one go."),
        ]
    },
    "jpg-to-png": {
        "tool": "JPG to PNG Converter",
        "faqs": [
            ("Does converting JPG to PNG lose quality?",
             "No. JPG to PNG conversion is lossless — PNG is a lossless format, so the output preserves every detail of the original JPG. However, converting a compressed JPG to PNG will not restore detail lost during the original JPG compression. The file size will also increase significantly because PNG retains full pixel data."),
            ("Why would I convert JPG to PNG?",
             "Convert JPG to PNG when you need lossless quality for editing, when your design workflow requires PNG format, or when the output will be edited and re-saved multiple times. PNG also supports transparency, allowing you to remove backgrounds later. It's ideal for screenshots, graphics, and any content requiring crisp edges."),
            ("Will the file size be larger after conversion?",
             "Yes, expect PNG files to be 5-10x larger than the original JPG files. PNG's lossless compression preserves every pixel without quality loss, so it demands more storage. For photos on websites, JPG is often more practical. Use PNG when quality preservation matters more than file size."),
            ("Can I convert multiple JPG images at once?",
             "Absolutely. Select multiple JPG files and our tool batch converts them all simultaneously. Each image gets its own preview showing the new file size. Download converted PNGs one by one or click 'Download All' for bulk download — no waiting between conversions."),
        ]
    },
    "webp-to-png": {
        "tool": "WebP to PNG Converter",
        "faqs": [
            ("Is WebP to PNG conversion lossless?",
             "Yes, converting WebP to PNG with our tool preserves the original quality. PNG is a lossless format, so all pixel data from the WebP source is retained. The output PNG will be larger in file size than the original WebP, but you get full compatibility with all platforms and editing software."),
            ("Why would I convert WebP to PNG?",
             "WebP is great for web performance, but not all software supports it. Convert to PNG when you need to open WebP files in legacy image editors, upload to platforms that don't support WebP, or share files with people who may not have modern browsers. PNG works everywhere."),
            ("Does WebP transparency transfer to PNG?",
             "Yes. Both WebP and PNG support alpha transparency channels. When you convert a transparent WebP to PNG, all transparency information is preserved perfectly. This makes it safe to convert WebP graphics, logos, and icons with transparent backgrounds to PNG."),
            ("How do I convert WebP to PNG in bulk?",
             "Simply drag and drop multiple WebP files onto the upload area or select them all at once. The tool processes each file in parallel and displays previews with file size comparisons. Download individual PNGs or use 'Download All' for the complete batch."),
        ]
    },
    "png-to-webp": {
        "tool": "PNG to WebP Converter",
        "faqs": [
            ("How much smaller is WebP compared to PNG?",
             "WebP typically reduces file size by 25-35% compared to PNG while maintaining the same visual quality. For photos with lossy WebP compression, savings reach 80-90%. For lossless WebP (preserving transparency), you still get roughly 30% smaller files. WebP is designed specifically for web performance."),
            ("Does WebP support transparency like PNG?",
             "Yes, WebP fully supports alpha transparency channels. You can convert transparent PNGs to WebP and the transparency is preserved perfectly. This makes WebP an ideal replacement for PNG on the web — same visual quality with transparency, but significantly smaller file sizes."),
            ("Is WebP supported in all browsers?",
             "WebP is supported by all modern browsers including Chrome (since 2010), Firefox (since 2018), Safari (since 2020), and Edge (since 2018). Over 97% of web users can view WebP images. For edge cases, you can use a fallback strategy with the <picture> element."),
            ("Should I convert all my PNGs to WebP?",
             "For web use, yes — replacing PNG with WebP improves page load speed without quality loss, especially beneficial for mobile users on slow connections. For images you need to edit or share outside the web, keep the original PNG. WebP is still not universally supported in offline tools like Photoshop without plugins."),
        ]
    },
    "jpg-to-webp": {
        "tool": "JPG to WebP Converter",
        "faqs": [
            ("How much can JPG to WebP reduce file size?",
             "WebP typically reduces file size by 25-35% compared to JPG at the same quality level. For images with large smooth areas like skies or gradients, the savings can reach 50% or more. Lower quality settings in WebP also produce noticeably better-looking results than equivalent JPG compression."),
            ("Is WebP quality better than JPG at the same file size?",
             "Yes. WebP uses more advanced compression algorithms that produce fewer artifacts than JPG at equivalent bitrates. This means you can set the quality lower in WebP and still get a better-looking image than JPG, making WebP the clear winner for web performance."),
            ("Does WebP support metadata from the original JPG?",
             "WebP format supports EXIF and XMP metadata. Our tool preserves basic image data during conversion. For critical metadata like GPS coordinates or camera settings, verify the output retains what you need. Most modern image management tools handle WebP metadata correctly."),
            ("Can I batch convert JPG to WebP?",
             "Yes, select as many JPG files as you need and convert them all in one operation. The tool processes them simultaneously and shows previews with file size comparisons. Download converted WebP files individually or use the batch download to get everything at once."),
        ]
    },

    # ── Image processing tools ──
    "resize-image": {
        "tool": "Image Resizer",
        "faqs": [
            ("Does resizing an image affect its quality?",
             "Downscaling (making the image smaller) typically preserves perceived quality well because excess pixels are merged. Upscaling (making it larger) causes quality loss because the software has to invent pixels. For best results, always start with the largest source image available when you need to upscale."),
            ("What dimensions can I resize my image to?",
             "You can enter any width and height in pixels. The tool supports custom dimensions and maintains aspect ratio by default. Common presets include 1080×1080 (Instagram square), 1920×1080 (HD wallpaper), 800×800 (product photos), and 1200×630 (social share images)."),
            ("Will metadata be preserved after resizing?",
             "Basic image metadata may be stripped during resizing as the tool regenerates the image. For most web and social media use, this is fine. If you need to preserve EXIF data like camera settings or GPS coordinates, save a copy of the original before resizing."),
            ("How many images can I resize at once?",
             "There is no limit. Upload multiple images and resize them all to the same dimensions in one batch operation. Each image is processed independently, and you can download them individually or use the 'Download All' button for efficient bulk processing."),
        ]
    },
    "compress-image": {
        "tool": "Image Compressor",
        "faqs": [
            ("How much can I compress an image without visible quality loss?",
             "Most images can be compressed 50-80% before quality loss becomes noticeable. Photos with smooth gradients compress well at 60-70% quality. Text-heavy screenshots need higher quality (85-90%) to keep edges crisp. Our slider lets you find the sweet spot for each image."),
            ("Is the compression lossy or lossless?",
             "Our tool uses lossy compression (JPEG/WebP re-encoding) by default, which achieves much smaller file sizes than lossless methods. The quality slider controls the trade-off. For PNG images, we recommend converting to JPEG or WebP during compression for maximum file size reduction."),
            ("Are my images uploaded to any server during compression?",
             "No. All compression happens locally in your browser using the Canvas API. Your images never leave your device. This guarantees your privacy and makes our compressor safe for sensitive or confidential content."),
            ("What file types can I compress?",
             "Our compressor supports JPG, JPEG, PNG, WebP, GIF, and BMP. The compression works best on JPG and WebP formats. For PNG images, pair compression with format conversion to JPG or WebP for maximum file size reduction — often 80-90% smaller with minimal quality impact."),
        ]
    },
    "image-splitter": {
        "tool": "Image Grid Splitter",
        "faqs": [
            ("What grid layouts are supported?",
             "Our splitter supports custom rows and columns. The most common layouts are 3×3 (Instagram 9-grid), 2×2 (4 parts for mosaic), and horizontal/vertical strips. You can split any image into virtually any grid size — try 3×1 for a triptych, 4×1 for a story strip, or 2×3 for a 6-part grid."),
            ("Will splitting an image reduce its quality?",
             "No. Each split piece retains the full quality of the original image at its native resolution. Since each tile covers a portion of the original canvas, the individual piece dimensions are smaller, but the pixel density and quality remain identical."),
            ("What is splitting an image used for?",
             "Image splitting is popular for: Instagram grid posts (split a panorama into 9 tiles), creating before/after comparisons, making image puzzles, dividing large infographics into digestible parts, and designing multi-part social media content that looks seamless when viewed on a profile grid."),
            ("How do I download all the split pieces?",
             "After splitting, every tile displays with a preview and file size. You can download each piece individually or click 'Download All' to save every tile at once. Files are numbered sequentially (e.g., image_1x1.jpg, image_1x2.jpg) to help reassemble them later."),
        ]
    },
    "extract-colors": {
        "tool": "Color Palette Extractor",
        "faqs": [
            ("How many colors can the extractor detect?",
             "Our tool can extract 5, 10, 15, or 20 dominant colors from any image. It uses a median cut quantization algorithm to identify the most representative colors. More colors give finer detail, while fewer gives a simplified palette perfect for branding and design work."),
            ("Can I copy the hex codes from the extracted palette?",
             "Yes. Each extracted color displays with its hex code. Click the code to copy it to your clipboard instantly. You can also copy the complete palette as a comma-separated list of hex codes for importing into design tools like Figma, Adobe, or Tailwind CSS projects."),
            ("What image formats work with the color extractor?",
             "All major image formats are supported: JPG, JPEG, PNG, WebP, GIF, and BMP. The extraction algorithm works on the pixel data after the image loads in the browser. Higher resolution images produce more accurate results, so upload the highest quality version available."),
            ("How accurate is the color extraction?",
             "The median cut algorithm is very reliable for identifying dominant colors. It analyzes every pixel to find the most frequent color clusters. However, images with thousands of subtle shades (like sunsets) may produce a simplified palette because the tool reduces the image to a limited number of color groups."),
        ]
    },
    "image-to-base64": {
        "tool": "Image to Base64 Converter",
        "faqs": [
            ("What is Base64 encoding used for?",
             "Base64 encoding converts binary image data into text format that can be embedded directly in HTML, CSS, or JavaScript. Common uses include: embedding small icons in CSS without HTTP requests, creating data URIs for single-file HTML pages, storing images in databases as text, and working with APIs that accept Base64 input."),
            ("How much larger is the Base64 output compared to the original?",
             "Base64 encoding increases file size by approximately 33% compared to the original binary file. For small images (under 10KB), this overhead is acceptable for the convenience of embedding. For larger images, Base64 is inefficient — loading via URL is better for file sizes over 20KB."),
            ("Can I convert multiple images to Base64 at once?",
             "Yes, upload multiple images and each one gets converted to Base64 independently. All results are displayed with copy buttons for easy retrieval. This is particularly useful when you need multiple Base64 strings for different icons or assets in a single project."),
            ("What format is the Base64 output?",
             "The output includes the data URI prefix (e.g., 'data:image/png;base64,...') so the string works immediately in HTML src attributes, CSS background-image properties, or JavaScript Image objects. Just paste the complete string — no formatting needed."),
        ]
    },

    # ── Long-tail resize pages ──
    "resize-image-to-1080x1080": {
        "tool": "Image Resizer to 1080x1080",
        "faqs": [
            ("Why is 1080×1080 a common image size?",
             "1080×1080 pixels is the ideal square format for Instagram posts, profile pictures, and social media grid layouts. Most platforms optimize display at this resolution — sharp on Retina displays without being unnecessarily large. It also works well as a standard product photo square."),
            ("Will my image be cropped or stretched to fit 1080×1080?",
             "The tool resizes while maintaining aspect ratio. If your original image isn't a perfect square, it will fit within 1080×1080 boundaries with its original proportions preserved. Non-square images get letterboxed (blank space on the sides or top/bottom). For a true square crop, crop your image to square first."),
            ("How fast is batch resizing to 1080×1080?",
             "Extremely fast. Canvas-based processing means each image resizes in milliseconds. Upload multiple images at once and the tool processes them all in parallel. You can resize an entire folder of images to 1080×1080 in seconds."),
            ("Is this resize tool free?",
             "Yes, completely free with no usage limits, registration, or watermarks. All processing runs locally in your browser — nothing is uploaded to any server."),
        ]
    },
    "resize-image-to-1920x1080": {
        "tool": "Image Resizer to 1920x1080",
        "faqs": [
            ("What is 1920×1080 used for?",
             "1920×1080 (Full HD / 1080p) is the standard desktop wallpaper resolution, YouTube thumbnail size, presentation slide dimensions, and widescreen display format. It's also commonly used for hero images on websites, blog featured images, and video cover art."),
            ("Will resizing to 1920×1080 maintain the original aspect ratio?",
             "Yes, the tool preserves aspect ratio automatically. Images that aren't 16:9 will fit within the 1920×1080 box with their original proportions. For a perfect 16:9 crop, manually crop the image before resizing, or use a dedicated cropping tool."),
            ("How much will the file size change?",
             "Resizing significantly reduces file size if your original is larger than 1920×1080 — most photos from modern cameras and smartphones exceed this resolution. The exact change depends on the original dimensions and compression settings."),
        ]
    },
    "resize-image-to-800x800": {
        "tool": "Image Resizer to 800x800",
        "faqs": [
            ("When would I need 800×800 images?",
             "800×800 is the standard for e-commerce product photos (Amazon, Shopify, eBay), avatar/profile images, square product thumbnails, listing images on marketplace platforms, and mobile app icons. It's large enough to show detail but small enough to load quickly."),
            ("Can I batch resize product photos to 800×800?",
             "Yes, upload all your product images at once and resize them all to 800×800 in a single batch operation. Each image maintains its aspect ratio. Ideal for e-commerce sellers who need consistent image dimensions across their entire catalog."),
            ("Will 800×800 be sharp on Retina displays?",
             "800×800 appears as 400×400 on 2x Retina screens (like iPhones with Retina displays). For true Retina sharpness at a 400×400 display size, 800×800 is perfect — double the pixel density for crisp rendering."),
        ]
    },
    "resize-image-to-1200x630": {
        "tool": "Image Resizer to 1200x630",
        "faqs": [
            ("Why is 1200×630 the recommended social share size?",
             "1200×630 pixels is the Open Graph (OG) image standard recommended by Facebook, LinkedIn, and most social platforms. It's a 1.91:1 aspect ratio that displays well both in feeds and when shared as a link preview. Twitter also displays this ratio for its summary card with large image."),
            ("Will my image be cropped on different social platforms?",
             "Each platform handles OG images slightly differently. 1200×630 is the safest standard — it centers the image and most platforms show the full width. Keep critical content (text, logos) within the center-safe zone (roughly 600×630) to avoid clipping on any platform."),
            ("What happens if my image isn't 1.91:1 ratio?",
             "The tool preserves aspect ratio. Non-1.91:1 images will fit within 1200×630 with letterboxing. For the best social sharing experience, crop your image to approximately 1.91:1 before resizing so the preview fills the entire card without black bars."),
        ]
    },

    # ── Long-tail compress pages ──
    "compress-image-to-100kb": {
        "tool": "Image Compressor to 100KB",
        "faqs": [
            ("How do I get an image under 100KB?",
             "Start with a reasonable resolution (under 2000px wide). Use the quality slider between 50-70% for most images. Photos with lots of detail may need lower quality settings, while simple graphics with solid colors can stay crisp even at higher compression."),
            ("What's the best quality setting to stay under 100KB?",
             "For a 1920×1080 photo, 40-60% quality usually lands under 100KB. For smaller images like 800×800, 60-80% works. The tool shows the output file size in real time, so experiment with the slider to find the best quality that keeps you under the limit."),
            ("Why does my image need to be under 100KB?",
             "100KB is a common limit for email attachments, forum uploads, job application portals, and some CMS platforms. Smaller images also improve page load speed — every 100KB saved makes your page load noticeably faster, especially on mobile networks."),
            ("Can I batch compress images to under 100KB?",
             "Yes, upload multiple images and the tool processes them all simultaneously. Since each image needs different compression levels to hit 100KB, adjust the quality slider for your batch and preview the results before downloading."),
        ]
    },
    "compress-image-to-50kb": {
        "tool": "Image Compressor to 50KB",
        "faqs": [
            ("Can I keep good quality at 50KB?",
             "For thumbnails and preview images, 50KB produces acceptable quality. Small images (under 800px) can look excellent at 50KB with 70-80% quality. Large photos will show visible compression artifacts — keep them small in dimensions (under 1200px) for best results."),
            ("What image dimensions work best for 50KB target?",
             "Aim for 600-800px on the longest side. Combining moderate resolution with 50-70% JPEG quality reliably produces images under 50KB. Higher resolution images will need much more aggressive compression to fit under 50KB, resulting in poor visual quality."),
            ("Is 50KB too small for web images?",
             "Not at all. 50KB is ideal for blog thumbnails, comment avatars, small product grid images, and inline content previews. On slow mobile connections, 50KB images load almost instantly. Use larger sizes only for hero images and full-width content where detail matters."),
        ]
    },
    "compress-jpg-to-200kb": {
        "tool": "JPG Compressor to 200KB",
        "faqs": [
            ("What quality does a 200KB JPG give me?",
             "For a 1920×1080 image, 200KB typically corresponds to 70-85% JPEG quality — a good balance: visually near-lossless but with significant compression. For smaller images, you can use even higher quality and still stay under 200KB."),
            ("Is 200KB good for website images?",
             "200KB per image is a reasonable target for blog posts, portfolio items, and product pages. A page with 5-10 images at 200KB each loads smoothly on most connections. For hero images and banners, aim lower (100-150KB) since they're often full-width and critical to first impressions."),
            ("How do I batch compress JPGs to 200KB?",
             "Simply upload all your JPG files and adjust the quality slider until the previews show file sizes near 200KB. Since compression depends on image content, start with 75% quality and adjust up or down. Download individual images or use batch download for all at once."),
        ]
    },

    # ── Long-tail specialized conversion pages ──
    "png-to-jpg-for-email": {
        "tool": "PNG to JPG for Email",
        "faqs": [
            ("Why convert PNG to JPG for email?",
             "Email services often have attachment size limits (10-25MB total). PNGs from phone screenshots can be 3-5MB each. Converting to JPG typically reduces file sizes by 80-90%, making it easy to attach multiple images without hitting limits. Recipients also download email faster."),
            ("How small should images be for email attachments?",
             "Aim for under 500KB per image. Set JPG quality to 70-85% — this keeps the image looking good on screens while keeping attachments manageable. For very large original PNGs (over 5MB), also consider resizing to 1920px on the longest side before converting."),
            ("Will image quality be acceptable for email recipients?",
             "Yes. Most email clients display images at screen resolution (72-96 DPI), so JPG compression at 80% quality looks excellent. Recipients viewing on phones won't notice any difference from the original PNG, and they get the benefit of faster download and smaller attachment size."),
            ("Can I batch convert multiple PNGs for email?",
             "Absolutely. Select all the screenshots or images you want to email and convert them in one batch. The tool processes everything simultaneously, and you can download each converted JPG individually or grab them all at once for easy drag-and-drop into your email."),
        ]
    },
    "webp-to-png-for-website": {
        "tool": "WebP to PNG for Website",
        "faqs": [
            ("Why would a website need WebP converted to PNG?",
             "Not all platforms and CMS systems support WebP uploads. Convert WebP to PNG when: your website's media library rejects WebP, you're uploading to an older CMS, your CDN doesn't serve WebP correctly, or your contributors use browsers that don't handle WebP uploads reliably."),
            ("Does converting WebP to PNG preserve image quality for web use?",
             "Yes, PNG is lossless so the conversion preserves every pixel. The trade-off is file size — PNG will be 3-5x larger than the original WebP. For web use, consider re-compressing with a tool like TinyPNG after conversion, or keep WebP format where your CMS supports it."),
            ("Does the conversion retain transparency for web graphics?",
             "Yes, both WebP and PNG support alpha transparency. Logos, icons, and graphics with transparent backgrounds convert perfectly. The PNG output is ready for immediate use in your website's design assets and image directories."),
            ("Can I batch convert multiple WebP images for my website?",
             "Yes, upload all your WebP assets at once. The tool batch processes them and preserves filenames with the .png extension for easy website integration — just download and upload to your CMS or copy to your assets folder."),
        ]
    },
    "png-to-webp-for-wordpress": {
        "tool": "PNG to WebP for WordPress",
        "faqs": [
            ("Does WordPress support WebP natively?",
             "Yes, WordPress has supported WebP since version 5.8. You can upload WebP images directly in the Media Library. Some hosting providers may need a minor server config update, but most modern WordPress hosts handle WebP without any extra setup."),
            ("How much will converting PNG to WebP speed up my WordPress site?",
             "WebP images are typically 25-35% smaller than PNGs. For a WordPress site with 50+ images per page (common in galleries and portfolios), this means 30-50% faster load times. Core Web Vitals scores improve significantly — especially LCP (Largest Contentful Paint)."),
            ("Do I need a plugin to serve WebP on WordPress?",
             "No. WordPress 5.8+ accepts WebP uploads natively. Just upload your converted WebP files directly. For automatic conversion at upload time or serving WebP only to compatible browsers, plugins like WebP Express or EWWW Image Optimizer are helpful but not required."),
            ("Will conversion affect image transparency for WordPress?",
             "WebP fully supports alpha transparency, so your transparent PNG logos and graphics will work perfectly as WebP on WordPress. The transparency is preserved during conversion, and WordPress displays it correctly in both the admin panel and on the frontend."),
        ]
    },

    # ── Long-tail image split pages ──
    "split-image-into-3x3": {
        "tool": "Image Splitter 3x3 Grid",
        "faqs": [
            ("What is a 3×3 grid split used for?",
             "A 3×3 grid creates 9 equal tiles from one image — the classic Instagram carousel grid. When posted across 9 consecutive Instagram posts, the tiles reassemble into a single seamless image on your profile grid. It's popular for announcements, reveal campaigns, and artistic photo displays."),
            ("Will the 3×3 grid crop my image?",
             "If your original image is square, all 9 tiles will be perfect squares. If your image is rectangular (e.g., 3:2 or 16:9), the tool fits it within the 3×3 boundaries and each tile maintains the overall proportions. For a true Instagram 3×3 grid, start with a square image."),
            ("How do I post the 3×3 grid on Instagram?",
             "After splitting, you get 9 separate image files numbered 1-9 (top-left to bottom-right). Post them in order to your Instagram feed — tile 1 in position 1, tile 2 in position 2, etc. On your profile grid, they automatically align to form one cohesive image. Use a scheduling tool to arrange the order."),
            ("Can I split any image into a 3×3 grid?",
             "Yes, any image format supported by our tool (JPG, PNG, WebP, GIF, BMP) can be split into a 3×3 grid. The tool handles the math automatically — just upload your image and select the 3×3 option. Each tile is saved at the same quality and resolution as the original."),
        ]
    },
    "split-image-into-4-parts": {
        "tool": "Image Splitter 4 Parts",
        "faqs": [
            ("What is splitting an image into 4 parts used for?",
             "A 2×2 split creates 4 equal tiles — great for before/after showcases, product feature displays, puzzle-style reveals, large infographics divided into readable chunks, and mosaic wall art previews. It's simpler than a 9-grid but still creates an engaging multi-post layout."),
            ("Does a 4-part split mean 2×2 grid?",
             "Yes, the 4-part split is a 2×2 grid: 2 columns × 2 rows. Each tile is a quarter of the original image. The tiles are numbered sequentially left-to-right, top-to-bottom for easy reassembly. You can also choose different grid configurations in our full splitter tool."),
            ("Can I use 4-part split for print projects?",
             "Absolutely. Splitting a large image into 4 printable sections is useful for posters, banners, and large-format prints that need to be printed on standard-sized paper. Each tile retains full quality from the original, so the assembled print looks seamless."),
        ]
    },
}


# ── HTML generation helpers ───────────────────────────────────────────

def make_faq_schema(faqs, tool_name):
    """Generate FAQPage JSON-LD."""
    main_entity = []
    for q, a in faqs:
        main_entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }
    return json.dumps(schema, indent=4)


def make_faq_html(faqs):
    """Generate visible FAQ section HTML (insert before </main>)."""
    items = []
    for q, a in faqs:
        items.append(f'''                <details class="faq-item">
                    <summary class="faq-question">{q}</summary>
                    <p class="faq-answer">{a}</p>
                </details>''')
    return '\n'.join(items)


def process_page(dir_name, faq_data):
    """Add FAQPage schema + FAQ section to a sub-page."""
    faqs = faq_data["faqs"]
    tool = faq_data["tool"]
    filepath = os.path.join(BASE, dir_name, "index.html")

    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    changes = []

    # 1. Add FAQPage schema before the </head>
    schema_json = make_faq_schema(faqs, tool)
    faq_schema_tag = f'''    <!-- FAQ Structured Data -->
    <script type="application/ld+json">
{schema_json}
    </script>'''

    if "FAQ Structured Data" in html:
        print(f"  SKIP (already has FAQ schema): {dir_name}")
        return False

    html = html.replace('</head>', f'{faq_schema_tag}\n</head>')
    changes.append("FAQPage schema")

    # 2. Add visible FAQ section before </main>
    faq_section_html = f'''        <!-- FAQ Section -->
        <section class="features-section" style="background: var(--bg-secondary); padding-top: 3rem; padding-bottom: 3rem;">
            <div class="container" style="max-width: 800px;">
                <h2 class="section-title">Frequently Asked Questions</h2>
                <div class="faq-list">
{make_faq_html(faqs)}
                </div>
            </div>
        </section>'''

    html = html.replace('</main>', f'{faq_section_html}\n    </main>')
    changes.append("visible FAQ section")

    # 3. Add FAQ CSS (if not already present)
    faq_css = '''
        /* FAQ Section */
        .faq-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        .faq-item {
            background: var(--bg-primary, #fff);
            border: 1px solid var(--border-color, #e5e7eb);
            border-radius: 8px;
            overflow: hidden;
            transition: box-shadow 0.2s;
        }
        .faq-item:hover {
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        .faq-question {
            padding: 1rem 1.25rem;
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-color, #1f2937);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }
        .faq-question::after {
            content: '+';
            font-size: 1.25rem;
            color: var(--primary-color, #2563eb);
            transition: transform 0.2s;
        }
        details[open] .faq-question::after {
            content: '−';
        }
        .faq-answer {
            padding: 0 1.25rem 1rem 1.25rem;
            line-height: 1.7;
            color: var(--text-light, #6b7280);
        }'''

    if '/* FAQ Section */' not in html:
        html = html.replace('</head>', f'    <style>{faq_css}\n    </style>\n</head>')
        changes.append("FAQ CSS styles")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  OK ({', '.join(changes)}): {dir_name}")
    return True


# ── Main ──────────────────────────────────────────────────────────────

def main():
    all_dirs = list(FAQ_DATA.keys())
    print(f"Processing {len(all_dirs)} sub-pages...\n")

    success = 0
    skipped = 0
    failed = 0

    for dir_name in all_dirs:
        try:
            if process_page(dir_name, FAQ_DATA[dir_name]):
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {dir_name}: {e}")
            failed += 1

    print(f"\nDone: {success} updated, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
