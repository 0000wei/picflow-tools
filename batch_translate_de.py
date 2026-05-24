#!/usr/bin/env python3
"""
Sophisticated batch translation script for PicEte German sub-pages
Handles HTML structure, preserves technical terms, and translates content properly
"""

import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser
from html import unescape

# Base paths
BASE_DIR = Path("/home/wu/picete-site")
DE_DIR = BASE_DIR / "de"

# Page-specific translation mappings
PAGE_TRANSLATIONS = {
    "png-to-jpg": {
        "title": "PNG zu JPG - Kostenloser Online PNG zu JPG Konverter | PicEte",
        "description": "Kostenloser Online PNG zu JPG Konverter. Konvertieren Sie schnell PNG-Bilder in das JPG-Format. Unterstützt Batch-Konvertierung, qualitativ hochwertige Ausgabe, keine Anmeldung erforderlich, lokale Verarbeitung für den Datenschutz.",
        "hero_title": "PNG zu JPG Online Konverter",
        "hero_subtitle": "Konvertieren Sie schnell PNG-Bilder in das JPG-Format. Unterstützt Batch-Konvertierung mit qualitativ hochwertiger Ausgabe.",
        "upload_text": "PNG-Bilder hier ablegen",
        "upload_subtext": "oder klicken Sie zur Dateiauswahl, unterstützt Mehrfachauswahl",
        "select_btn": "PNG-Bilder auswählen",
        "selected_images": "Ausgewählte PNG-Bilder",
        "conversion_options": "Konvertierungsoptionen",
        "quality_label": "JPG-Qualität",
        "convert_btn": "In JPG konvertieren",
        "reset_btn": "Neu auswählen",
        "conversion_complete": "Konvertierung abgeschlossen!",
        "download_all": "Alle JPGs herunterladen",
        "convert_more": "Weitere Bilder konvertieren",
        "back_home": "← Zurück zu PicEte Startseite",
        "why_use": "Warum unseren PNG zu JPG Konverter verwenden",
        "how_to": "Wie man PNG kostenlos online in JPG konvertiert",
        "tips_title": "PNG zu JPG Tipps",
        "faq_title": "Häufig gestellte Fragen",
        "tagline": "PNG zu JPG Konverter",
    },

    "jpg-to-png": {
        "title": "JPG zu PNG - Kostenloser Online JPG zu PNG Konverter | PicEte",
        "description": "Kostenloser Online JPG zu PNG Konverter. Konvertieren Sie schnell JPG-Bilder in das PNG-Format. Unterstützt Batch-Konvertierung, Transparenz, keine Anmeldung erforderlich.",
        "hero_title": "JPG zu PNG Online Konverter",
        "hero_subtitle": "Konvertieren Sie schnell JPG-Bilder in das PNG-Format. Behalten Sie die Transparenz bei, unterstützen Batch-Konvertierung.",
        "upload_text": "JPG-Bilder hier ablegen",
        "upload_subtext": "oder klicken Sie zur Dateiauswahl, unterstützt Mehrfachauswahl",
        "select_btn": "JPG-Bilder auswählen",
        "selected_images": "Ausgewählte JPG-Bilder",
        "convert_btn": "In PNG konvertieren",
        "download_all": "Alle PNGs herunterladen",
        "tagline": "JPG zu PNG Konverter",
    },

    "resize-image": {
        "title": "Bildgröße ändern - Kostenloser Online Bildgrößenänderer | PicEte",
        "description": "Kostenloses Online-Tool zur Bildgrößenänderung. Ändern Sie die Größe von Bildern schnell und einfach. Unterstützt Batch-Verarbeitung, benutzerdefinierte Abmessungen, Seitenverhältnis beibehalten.",
        "hero_title": "Bildgröße ändern Online",
        "hero_subtitle": "Ändern Sie die Größe von Bildern schnell und einfach. Unterstützt Batch-Verarbeitung mit benutzerdefinierten Abmessungen.",
        "upload_text": "Bilder hier ablegen",
        "select_btn": "Bilder auswählen",
        "tagline": "Bildgrößenänderung",
    },

    "compress-image": {
        "title": "Bild komprimieren - Kostenloser Online Bildkompressor | PicEte",
        "description": "Kostenloser Online Bildkompressor. Komprimieren Sie Bilder schnell und einfach. Unterstützt Batch-Verarbeitung, Qualitätssteuerung, keine Anmeldung erforderlich.",
        "hero_title": "Bild komprimieren Online",
        "hero_subtitle": "Komprimieren Sie Bilder schnell und einfach. Unterstützt Batch-Verarbeitung mit Qualitätssteuerung.",
        "upload_text": "Bilder hier ablegen",
        "select_btn": "Bilder auswählen",
        "tagline": "Bildkomprimierung",
    },

    "image-splitter": {
        "title": "Bild aufteilen - Kostenloser Online Bildteiler | PicEte",
        "description": "Kostenloser Online Bildteiler. Teilen Sie Bilder in mehrere Teile auf. Unterstützt benutzerdefinierte Zeilen und Spalten, Batch-Verarbeitung, keine Anmeldung erforderlich.",
        "hero_title": "Bild aufteilen Online",
        "hero_subtitle": "Teilen Sie Bilder in mehrere Teile auf. Unterstützt benutzerdefinierte Zeilen und Spalten für Social-Media-Grids.",
        "upload_text": "Bild hier ablegen",
        "select_btn": "Bild auswählen",
        "tagline": "Bildteiler",
    },

    "extract-colors": {
        "title": "Farben extrahieren - Kostenloser Online Farbextrahierer | PicEte",
        "description": "Kostenloser Online Farbextrahierer. Extrahieren Sie Farben aus Bildern. Erhalten Sie Farbpaletten, HEX-Codes, RGB-Werte, keine Anmeldung erforderlich.",
        "hero_title": "Farben aus Bild extrahieren",
        "hero_subtitle": "Extrahieren Sie Farben aus Bildern und erhalten Sie Farbpaletten mit HEX- und RGB-Werten.",
        "upload_text": "Bild hier ablegen",
        "select_btn": "Bild auswählen",
        "tagline": "Farbextrahierer",
    },

    "image-to-base64": {
        "title": "Bild zu Base64 - Kostenloser Online Base64 Konverter | PicEte",
        "description": "Kostenloser Online Bild zu Base64 Konverter. Konvertieren Sie Bilder in Base64-Strings. Unterstützt alle Bildformate, keine Anmeldung erforderlich.",
        "hero_title": "Bild zu Base64 Konverter",
        "hero_subtitle": "Konvertieren Sie Bilder in Base64-Strings für die Verwendung in HTML und CSS.",
        "upload_text": "Bild hier ablegen",
        "select_btn": "Bild auswählen",
        "tagline": "Bild zu Base64",
    },
}

# Common translations
COMMON_TRANSLATIONS = {
    "Home": "Startseite",
    "More Tools": "Weitere Tools",
    "More Tools.": "Weitere Tools",
    "Back to Home": "Zurück zur Startseite",
    "Back to PicEte Home": "← Zurück zu PicEte Startseite",
    "Privacy Policy": "Datenschutzerklärung",
    "All rights reserved": "Alle Rechte vorbehalten",
    "Fast Conversion": "Schnelle Konvertierung",
    "High Quality Output": "Qualitativ hochwertige Ausgabe",
    "Batch Processing": "Batch-Verarbeitung",
    "Privacy Protection": "Datenschutz",
    "Selected Images": "Ausgewählte Bilder",
    "Smaller file": "Kleinere Datei",
    "Higher quality": "Höhere Qualität",
    "Download": "Herunterladen",
    "Select": "Auswählen",
    "Convert": "Konvertieren",
    "Quality": "Qualität",
    "Processing": "Verarbeitung",
    "Complete!": "Abgeschlossen!",
    "Success": "Erfolg",
    "Error": "Fehler",
    "Why Use Our": "Warum unseren",
    "How to": "Wie man",
    "Online Free": "Online kostenlos",
    "Tips": "Tipps",
    "Frequently Asked Questions": "Häufig gestellte Fragen",
}

def get_page_type_from_path(file_path):
    """Determine page type from file path"""
    path_str = str(file_path).lower()

    if "png-to-jpg" in path_str:
        return "png-to-jpg"
    elif "jpg-to-png" in path_str:
        return "jpg-to-png"
    elif "webp-to-png" in path_str:
        return "webp-to-png"
    elif "png-to-webp" in path_str:
        return "png-to-webp"
    elif "jpg-to-webp" in path_str:
        return "jpg-to-webp"
    elif "resize-image" in path_str:
        return "resize-image"
    elif "compress-image" in path_str:
        return "compress-image"
    elif "image-splitter" in path_str:
        return "image-splitter"
    elif "extract-colors" in path_str:
        return "extract-colors"
    elif "image-to-base64" in path_str:
        return "image-to-base64"
    else:
        return "generic"

def translate_faq_questions(faq_content):
    """Translate FAQ questions and answers"""
    translations = {
        "Does PNG to JPG conversion affect image quality?": "Beeinträchtigt die Konvertierung von PNG zu JPG die Bildqualität?",
        "Will I lose transparency converting PNG to JPG?": "Verliere ich Transparenz bei der Konvertierung von PNG zu JPG?",
        "How fast is the PNG to JPG conversion?": "Wie schnell ist die PNG-zu-JPG-Konvertierung?",
        "How many PNG files can I convert at once?": "Wie viele PNG-Dateien kann ich gleichzeitig konvertieren?",
        "Yes, JPG uses lossy compression, so there is some quality loss. Our tool lets you adjust the quality from 10% to 100%. For most web uses, 80-90% quality produces visually identical results to the original PNG while cutting file size by 80% or more. Set it higher for prints and archival where every pixel matters.": "Ja, JPG verwendet verlustbehaftete Komprimierung, sodass es zu einem gewissen Qualitätsverlust kommt. Mit unserem Tool können Sie die Qualität von 10% bis 100% einstellen. Für die meisten Webanwendungen liefert eine Qualität von 80-90% visuell identische Ergebnisse zum ursprünglichen PNG bei gleichzeitiger Reduzierung der Dateigröße um 80% oder mehr. Stellen Sie für Drucke und Archive, wo jeder Pixel zählt, einen höheren Wert ein.",
        "Yes. JPG does not support transparency. Any transparent areas in your PNG will be filled with white. If you need to preserve transparency, consider keeping the original PNG or using a format like WebP that supports both transparency and good compression.": "Ja. JPG unterstützt keine Transparenz. Alle transparenten Bereiche in Ihrem PNG werden mit weiß gefüllt. Wenn Sie die Transparenz beibehalten müssen, erwägen Sie, das ursprüngliche PNG zu behalten oder ein Format wie WebP zu verwenden, das sowohl Transparenz als auch gute Komprimierung unterstützt.",
        "The conversion is instant and happens entirely in your browser using Canvas technology. Even large files or batch conversions complete in milliseconds. The speed depends on your device's processing power, but there is no server upload or waiting.": "Die Konvertierung ist sofort und erfolgt vollständig in Ihrem Browser mit Canvas-Technologie. Selbst große Dateien oder Batch-Konvertierungen werden in Millisekunden abgeschlossen. Die Geschwindigkeit hängt von der Verarbeitungsleistung Ihres Geräts ab, aber es gibt kein Server-Upload oder Warten.",
        "There is no limit on the number of files. Select a whole folder of PNGs and convert them all at once. Each image is processed independently, and you can download them individually or click 'Download All' to get everything in one go.": "Es gibt keine Begrenzung für die Anzahl der Dateien. Wählen Sie einen gesamten Ordner mit PNGs aus und konvertieren Sie alle auf einmal. Jedes Bild wird unabhängig verarbeitet, und Sie können sie einzeln herunterladen oder auf 'Alle herunterladen' klicken, um alles auf einmal zu erhalten.",
    }

    for en, de in translations.items():
        faq_content = faq_content.replace(en, de)

    return faq_content

def process_html_content(content, page_type):
    """Process and translate HTML content"""

    # Set lang attribute
    content = re.sub(r'<html lang="[^"]*">', '<html lang="de">', content)

    # Get page-specific translations
    page_trans = PAGE_TRANSLATIONS.get(page_type, {})

    # Translate title
    if page_trans.get("title"):
        content = re.sub(r'<title>.*?</title>', f'<title>{page_trans["title"]}</title>', content, flags=re.DOTALL)

    # Translate meta description
    if page_trans.get("description"):
        content = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{page_trans["description"]}"', content)

    # Update URLs for German version
    # Canonical link
    content = re.sub(r'<link rel="canonical" href="https://picete\.com/([^"]*)"', r'<link rel="canonical" href="https://picete.com/de/\1"', content)

    # OG URL
    content = re.sub(r'<meta property="og:url" content="https://picete\.com/([^"]*)"', r'<meta property="og:url" content="https://picete.com/de/\1"', content)

    # Update internal links
    content = re.sub(r'href="\.\./"', 'href="/de/"', content)
    content = re.sub(r'href="\.\./([^"]+)"', r'href="/de/\1"', content)

    # Update static resource paths (one level up for sub-directories)
    content = re.sub(r'href="\.\./css/', 'href="../../css/', content)
    content = re.sub(r'src="\.\./images/', 'src="../../images/', content)
    content = re.sub(r'href="\.\./favicon', 'href="../../favicon', content)
    content = re.sub(r'href="\.\./llms\.txt"', 'href="../../llms.txt"', content)
    content = re.sub(r'href="\.\./mcp\.json"', 'href="../../mcp.json"', content)

    # Translate schema.org content
    def translate_schema(match):
        schema_json = match.group(1)
        try:
            schema_data = json.loads(schema_json)

            # Translate name and description
            if "name" in schema_data:
                if schema_data["name"] == "PNG to JPG Converter":
                    schema_data["name"] = "PNG zu JPG Konverter"
                elif schema_data["name"] == "JPG to PNG Converter":
                    schema_data["name"] = "JPG zu PNG Konverter"
                elif schema_data["name"] == "Image Resizer":
                    schema_data["name"] = "Bildgrößenänderung"
                elif schema_data["name"] == "Image Compressor":
                    schema_data["name"] = "Bildkomprimierung"
                elif schema_data["name"] == "PicEte":
                    schema_data["name"] = "PicEte"  # Keep brand name

            if "description" in schema_data:
                desc = schema_data["description"]
                if "PNG to JPG" in desc:
                    schema_data["description"] = desc.replace("PNG to JPG", "PNG zu JPG").replace("conversion tool", "Konvertierungstool").replace("free online", "kostenloses Online")
                elif "JPG to PNG" in desc:
                    schema_data["description"] = desc.replace("JPG to PNG", "JPG zu PNG").replace("conversion tool", "Konvertierungstool")

            # Translate BreadcrumbList
            if schema_data.get("@type") == "BreadcrumbList":
                for item in schema_data.get("itemListElement", []):
                    if item.get("name") == "Home":
                        item["name"] = "Startseite"
                    if "item" in item and "/de/" not in item["item"]:
                        item["item"] = item["item"].replace("picete.com/", "picete.com/de/")

            return f'<script type="application/ld+json">\n{json.dumps(schema_data, indent=4, ensure_ascii=False)}\n    </script>'
        except:
            return match.group(0)

    content = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', translate_schema, content, flags=re.DOTALL)

    # Translate FAQ sections
    faq_matches = re.findall(r'<script type="application/ld\+json">\s*\{[^@]*"@type":\s*"FAQPage"[^}]*\}([^<]+)\}\s*</script>', content, flags=re.DOTALL)
    for faq_match in faq_matches:
        # This needs more sophisticated JSON parsing for FAQ
        pass

    # Translate visible text content
    # Page-specific translations
    for key, value in page_trans.items():
        if key not in ["title", "description"]:
            content = content.replace(key, value)

    # Common translations
    for en, de in COMMON_TRANSLATIONS.items():
        content = content.replace(en, de)

    # Translate FAQ content in HTML
    content = translate_faq_questions(content)

    # Translate breadcrumbs
    content = content.replace('<span class="current">PNG to JPG</span>', '<span class="current">PNG zu JPG</span>')
    content = content.replace('<span class="current">JPG to PNG</span>', '<span class="current">JPG zu PNG</span>')
    content = content.replace('<span class="current">Resize Image</span>', '<span class="current">Bildgröße ändern</span>')
    content = content.replace('<span class="current">Compress Image</span>', '<span class="current">Bild komprimieren</span>')

    return content

def translate_page(source_file, target_file):
    """Translate a single HTML page"""

    page_type = get_page_type_from_path(source_file)

    # Read source file
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Process content
    translated_content = process_html_content(content, page_type)

    # Create target directory if needed
    target_file.parent.mkdir(parents=True, exist_ok=True)

    # Write translated file
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)

    return True

# Pages to translate
PAGES = [
    ("png-to-jpg/index.html", "png-to-jpg/index.html"),
    ("jpg-to-png/index.html", "jpg-to-png/index.html"),
    ("webp-to-png/index.html", "webp-to-png/index.html"),
    ("png-to-webp/index.html", "png-to-webp/index.html"),
    ("jpg-to-webp/index.html", "jpg-to-webp/index.html"),
    ("resize-image/index.html", "resize-image/index.html"),
    ("compress-image/index.html", "compress-image/index.html"),
    ("image-splitter/index.html", "image-splitter/index.html"),
    ("extract-colors/index.html", "extract-colors/index.html"),
    ("image-to-base64/index.html", "image-to-base64/index.html"),
    ("resize-image-to-1080x1080/index.html", "resize-image-to-1080x1080/index.html"),
    ("resize-image-to-1920x1080/index.html", "resize-image-to-1920x1080/index.html"),
    ("resize-image-to-800x800/index.html", "resize-image-to-800x800/index.html"),
    ("resize-image-to-1200x630/index.html", "resize-image-to-1200x630/index.html"),
    ("compress-image-to-100kb/index.html", "compress-image-to-100kb/index.html"),
    ("compress-image-to-50kb/index.html", "compress-image-to-50kb/index.html"),
    ("compress-jpg-to-200kb/index.html", "compress-jpg-to-200kb/index.html"),
    ("png-to-jpg-for-email/index.html", "png-to-jpg-for-email/index.html"),
    ("webp-to-png-for-website/index.html", "webp-to-png-for-website/index.html"),
    ("png-to-webp-for-wordpress/index.html", "png-to-webp-for-wordpress/index.html"),
    ("split-image-into-3x3/index.html", "split-image-into-3x3/index.html"),
    ("split-image-into-4-parts/index.html", "split-image-into-4-parts/index.html"),
]

def main():
    """Main translation function"""
    print("🚀 Starting German translation of 22 PicEte sub-pages...")
    print("=" * 70)

    success_count = 0
    fail_count = 0
    results = []

    for source_file, target_file in PAGES:
        source_path = BASE_DIR / source_file
        target_path = DE_DIR / target_file

        try:
            if source_path.exists():
                print(f"📝 Translating: {source_file}")
                translate_page(source_path, target_path)
                print(f"✅ Success: {target_file}")
                success_count += 1
                results.append((source_file, "success"))
            else:
                print(f"❌ Source not found: {source_file}")
                fail_count += 1
                results.append((source_file, "not_found"))
        except Exception as e:
            print(f"❌ Error processing {source_file}: {e}")
            fail_count += 1
            results.append((source_file, f"error: {e}"))

    print("=" * 70)
    print(f"📊 Translation complete: {success_count} ✅ succeeded, {fail_count} ❌ failed")

    if fail_count == 0:
        print("🎉 All pages translated successfully!")
    else:
        print("⚠️  Some pages had issues - please review the errors above")

    print("\n📋 Summary of translated pages:")
    for page, status in results:
        status_icon = "✅" if status == "success" else "❌"
        print(f"  {status_icon} {page}")

if __name__ == "__main__":
    main()