import os
import re
import json
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the exact translations for the missing FAQs
FIXES = {
    "ar/compress-image-for-email/index.html": {
        "How small should images be for email?": "ما هو الحجم المناسب للصور المرسلة عبر البريد الإلكتروني؟",
        "Aim for under 500KB per image. For casual sharing, even 200-300KB works well. Use JPG format at 75-85% quality. If you're sending 10+ photos, compress each to under 300KB to stay well within email limits. Recipients will appreciate faster downloads, especially on mobile devices or slow connections.": "احرص على أن يكون حجم كل صورة أقل من 500 كيلوبايت. بالنسبة للمشاركة العادية، فإن حجم 200-300 كيلوبايت يعتبر ممتازاً أيضاً. استخدم تنسيق JPG بجودة تتراوح بين 75% و85%. إذا كنت ترسل أكثر من 10 صور، فقم بضغط كل منها إلى أقل من 300 كيلوبايت لتبقى ضمن حدود حجم المرفقات. سيقدر المستلمون سرعة التنزيل، خاصة على الأجهزة المحمولة أو الاتصالات البطيئة."
    },
    "ar/compress-image-for-website/index.html": {
        "What's the ideal image size for websites?": "ما هو الحجم المثالي للصور في مواقع الويب؟",
        "For modern websites, aim for images under 500KB each. Hero banners work well at 1920x1080 or 1200x630. Content images should be 800-1200px wide. Product photos for e-commerce should be 600-1000px on the longest side. Compressing to these sizes ensures fast page loads while maintaining quality. Always resize before compressing for best results.": "بالنسبة لمواقع الويب الحديثة، احرص على أن تكون الصور أقل من 500 كيلوبايت لكل منها. تعمل لافتات البطل (Hero banners) بشكل جيد بأبعاد 1920×1080 أو 1200×630. يجب أن يتراوح عرض صور المحتوى بين 800-1200 بكسل. وبالنسبة لصور المنتجات في التجارة الإلكترونية، يفضل أن يتراوح حجمها بين 600-1000 بكسل على الجانب الأطول. يضمن الضغط إلى هذه الأحجام سرعة تحميل الصفحة مع الحفاظ على الجودة. قم دائماً بتغيير الحجم قبل الضغط للحصول على أفضل النتائج.",
        "Should I use responsive images for my website?": "هل يجب أن أستخدم صوراً متجاوبة لموقعي الإلكتروني؟",
        "Yes. Responsive images serve different sizes based on device — small images for phones, larger for desktops. Use srcset attributes or picture elements. Create multiple compressed versions (e.g., 400w, 800w, 1200w) and let browsers choose appropriately. PicEte makes it easy to batch compress multiple sizes for responsive image sets.": "نعم. تخدم الصور المتجاوبة أحجاماً مختلفة بناءً على الجهاز - صور صغيرة للهواتف، وصور أكبر لأجهزة الكمبيوتر المكتبية. استخدم سمات srcset أو عناصر picture. قم بإنشاء إصدارات مضغوطة متعددة (على سبيل المثال، 400w، 800w، 1200w) ودع المتصفحات تختار الحجم المناسب. تسهل PicEte ضغط مجموعات متعددة من الصور المتجاوبة دفعة واحدة."
    },
    "ar/compress-image-for-wordpress/index.html": {
        "What's the recommended image size for WordPress?": "ما هو حجم الصور الموصى به لووردبريس؟",
        "WordPress recommends keeping uploaded images under 500KB for optimal performance. For featured images, 1200x630 pixels at 70-80% JPG quality works well. Blog post images should be 800-1200px wide. Compressing images before uploading to WordPress significantly improves page load speed and SEO rankings.": "يوصي ووردبريس بإبقاء الصور المرفوعة أقل من 500 كيلوبايت للحصول على الأداء الأمثل. بالنسبة للصور البارزة (Featured images)، فإن أبعاد 1200×630 بكسل بجودة JPG تتراوح بين 70-80% تعمل بشكل جيد. يجب أن يتراوح عرض صور مقالات المدونة بين 800-1200 بكسل. يؤدي ضغط الصور قبل رفعها إلى ووردبريس إلى تحسين سرعة تحميل الصفحة وتصنيفات محركات البحث (SEO) بشكل كبير."
    },
    "ar/compress-image-to-500kb/index.html": {
        "Why 500KB for email attachments?": "لماذا 500 كيلوبايت لمرفقات البريد الإلكتروني؟",
        "Email providers like Gmail and Outlook allow attachments up to 25MB total, but many corporate email systems limit messages to 10MB. When sending multiple photos, keeping each image under 500KB ensures you can attach 20+ photos without hitting limits. Recipients also appreciate faster downloads, especially on mobile connections.": "يسمح موفرو البريد الإلكتروني مثل Gmail وOutlook بمرفقات تصل إلى 25 ميجابايت إجمالاً، ولكن العديد من أنظمة البريد الإلكتروني للشركات تفرض حداً أقصى للمرفقات يبلغ 10 ميجابايت. عند إرسال صور متعددة، فإن إبقاء كل صورة تحت 500 كيلوبايت يضمن إمكانية إرفاق أكثر من 20 صورة دون تجاوز الحدود. كما يقدر المستلمون سرعة التنزيل، خاصة على اتصالات الهاتف المحمول."
    },
    "ar/png-to-jpg-for-email/index.html": {
        "Can I batch convert multiple PNGs for email?": "هل يمكنني تحويل صور PNG متعددة دفعة واحدة للبريد الإلكتروني؟"
    },
    "ar/png-to-webp-for-wordpress/index.html": {
        "Will conversion affect image transparency for WordPress?": "هل سيؤثر التحويل على شفافية الصورة في ووردبريس؟"
    },
    "ar/webp-to-png-for-website/index.html": {
        "Can I batch convert multiple WebP images for my website?": "هل يمكنني تحويل صور WebP متعددة دفعة واحدة لموقعي الإلكتروني؟"
    },
    "es/index.html": {
        "Is image processing secure?": "¿Es seguro el procesamiento de imágenes?",
        "Absolutely secure. All processing is done locally in your browser. Images are never uploaded to any server, ensuring your privacy and data security.": "Absolutamente seguro. Todo el procesamiento se realiza localmente en su navegador. Las imágenes nunca se suben a ningún servidor, garantizando su privacidad y la seguridad de sus datos.",
        "What image formats are supported?": "¿Qué formatos de imagen son compatibles?",
        "We support all major image formats: JPG, JPEG, PNG, WebP, GIF, BMP, SVG, covering most image processing needs.": "Soportamos todos los formatos de imagen principales: JPG, JPEG, PNG, WebP, GIF, BMP, SVG, cubriendo la mayoría de las necesidades de procesamiento de imágenes.",
        "Is there a file size limit?": "¿Existe un límite de tamaño de archivo?",
        "There is no hard limit, but very large images (over 100MB) may be affected by browser memory limitations. We recommend keeping individual images under 50MB for the best experience.": "No hay un límite estricto, pero las imágenes muy grandes (de más de 100 MB) pueden verse afectadas por las limitaciones de memoria del navegador. Recomendamos mantener las imágenes individuales por debajo de 50 MB para una mejor experiencia.",
        "Can I process multiple images at once?": "¿Puedo procesar varias imágenes a la vez?",
        "Yes! You can select multiple images at once for batch processing. Each image is processed independently, and you can download them individually or all at once.": "¡Sí! Puede seleccionar varias imágenes a la vez para el procesamiento por lotes. Cada imagen se procesa de forma independiente y puede descargarlas individualmente o todas a la vez."
    },
    "ja/compress-image/index.html": {
        "Are my images uploaded to any server during compression?": "圧縮中に画像がサーバーにアップロードされますか？",
        "What file types can I compress?": "どのファイル形式を圧縮できますか？"
    },
    "pt/png-to-jpg/index.html": {
        "How many PNG files can I convert at once?": "Quantos arquivos PNG posso converter de uma vez?"
    }
}

def fix_file(rel_path, translation_map):
    filepath = BASE_DIR / rel_path
    if not filepath.exists():
        print(f"File not found: {rel_path}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_content = content
    fixes_count = 0
    
    # 1. Replace FAQ Questions and Answers in HTML
    # We do a direct string replace for maximum reliability, handling different quotation marks
    for eng, trans in translation_map.items():
        # First, try standard strings directly (for HTML body content)
        if eng in content:
            content = content.replace(eng, trans)
            fixes_count += 1
            
        # Try variation with different smart quotes or whitespace normalized
        # Also clean up HTML representation
        eng_norm = eng.replace("'", "&#39;").replace('"', "&quot;")
        if eng_norm in content:
            content = content.replace(eng_norm, trans)
            fixes_count += 1
            
    # 2. Specifically process JSON-LD block
    def fix_jsonld(json_str):
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return json_str
            
        changed = False
        def process_entity(entity):
            nonlocal changed
            if not isinstance(entity, dict):
                return entity
            if entity.get('@type') == 'FAQPage':
                for item in entity.get('mainEntity', []):
                    name = item.get('name', '')
                    text = item.get('acceptedAnswer', {}).get('text', '')
                    
                    # Check if question name is in the translation map
                    if name in translation_map:
                        item['name'] = translation_map[name]
                        changed = True
                    # Check if answer text is in the translation map
                    if text in translation_map:
                        item['acceptedAnswer']['text'] = translation_map[text]
                        changed = True
            if '@graph' in entity:
                for g in entity['@graph']:
                    process_entity(g)
            return entity
            
        process_entity(data)
        if changed:
            return json.dumps(data, ensure_ascii=False, indent=2)
        return json_str

    content = re.sub(
        r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>',
        lambda m: f'<script type="application/ld+json">{fix_jsonld(m.group(1))}</script>',
        content, flags=re.DOTALL
    )

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed translation gaps in {rel_path} ({fixes_count} HTML replacements)")
    else:
        print(f"No changes made to {rel_path}")

def run():
    print("Fixing untranslated FAQ content gaps...")
    for rel_path, translation_map in FIXES.items():
        fix_file(rel_path, translation_map)
    print("Done fixing gaps.")

if __name__ == '__main__':
    run()
