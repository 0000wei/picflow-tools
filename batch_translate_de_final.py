#!/usr/bin/env python3
"""
Final comprehensive batch translation script for PicEte German sub-pages
Provides complete German translations with proper handling of all content types
"""

import os
import re
import json
from pathlib import Path

# Base paths
BASE_DIR = Path("/home/wu/picete-site")
DE_DIR = BASE_DIR / "de"

# Complete translation mappings
TRANSLATIONS = {
    # Navigation
    "Home": "Startseite",
    "More Tools": "Weitere Tools",
    "Back to Home": "Zurück zur Startseite",
    "Back to PicEte Home": "← Zurück zu PicEte Startseite",
    "Privacy Policy": "Datenschutzerklärung",
    "About": "Über uns",
    "All rights reserved": "Alle Rechte vorbehalten",

    # Hero sections
    "PNG to JPG Online Converter": "PNG zu JPG Online Konverter",
    "JPG to PNG Online Converter": "JPG zu PNG Online Konverter",
    "WebP to PNG Online Converter": "WebP zu PNG Online Konverter",
    "PNG to WebP Online Converter": "PNG zu WebP Online Konverter",
    "JPG to WebP Online Converter": "JPG zu WebP Online Konverter",
    "Resize Image Online": "Bildgröße ändern Online",
    "Compress Image Online": "Bild komprimieren Online",
    "Split Image Online": "Bild aufteilen Online",
    "Extract Colors from Image": "Farben aus Bild extrahieren",
    "Convert Image to Base64": "Bild in Base64 konvertieren",

    # Descriptions
    "Quickly convert PNG images to JPG format. Supports batch conversion with high-quality output.": "Konvertieren Sie schnell PNG-Bilder in das JPG-Format. Unterstützt Batch-Konvertierung mit qualitativ hochwertiger Ausgabe.",
    "Quickly convert JPG images to PNG format. Supports transparency and batch conversion.": "Konvertieren Sie schnell JPG-Bilder in das PNG-Format. Unterstützt Transparenz und Batch-Konvertierung.",
    "Quickly convert WebP images to PNG format. Supports transparency and batch conversion.": "Konvertieren Sie schnell WebP-Bilder in das PNG-Format. Unterstützt Transparenz und Batch-Konvertierung.",
    "Quickly convert PNG images to WebP format. Supports transparency and batch conversion.": "Konvertieren Sie schnell PNG-Bilder in das WebP-Format. Unterstützt Transparenz und Batch-Konvertierung.",
    "Quickly convert JPG images to WebP format. Supports transparency and batch conversion.": "Konvertieren Sie schnell JPG-Bilder in das WebP-Format. Unterstützt Transparenz und Batch-Konvertierung.",
    "Resize images quickly and easily. Supports batch processing with custom dimensions.": "Ändern Sie die Größe von Bildern schnell und einfach. Unterstützt Batch-Verarbeitung mit benutzerdefinierten Abmessungen.",
    "Compress images quickly and easily. Supports batch processing with quality control.": "Komprimieren Sie Bilder schnell und einfach. Unterstützt Batch-Verarbeitung mit Qualitätssteuerung.",
    "Split images into multiple parts. Supports custom rows and columns for social media grids.": "Teilen Sie Bilder in mehrere Teile auf. Unterstützt benutzerdefinierte Zeilen und Spalten für Social-Media-Grids.",
    "Extract colors from images and get color palettes with HEX and RGB values.": "Extrahieren Sie Farben aus Bildern und erhalten Sie Farbpaletten mit HEX- und RGB-Werten.",
    "Convert images to Base64 strings for use in HTML and CSS.": "Konvertieren Sie Bilder in Base64-Strings für die Verwendung in HTML und CSS.",

    # Upload areas
    "Drop PNG images here": "PNG-Bilder hier ablegen",
    "Drop JPG images here": "JPG-Bilder hier ablegen",
    "Drop WebP images here": "WebP-Bilder hier ablegen",
    "Drop images here": "Bilder hier ablegen",
    "Drop image here": "Bild hier ablegen",
    "or click to select files, supports multiple selection": "oder klicken Sie zur Dateiauswahl, unterstützt Mehrfachauswahl",
    "or click to select files": "oder klicken Sie zur Dateiauswahl",

    # Buttons
    "Select PNG Images": "PNG-Bilder auswählen",
    "Select JPG Images": "JPG-Bilder auswählen",
    "Select WebP Images": "WebP-Bilder auswählen",
    "Select Images": "Bilder auswählen",
    "Select Image": "Bild auswählen",
    "Choose Again": "Neu auswählen",
    "Convert to JPG": "In JPG konvertieren",
    "Convert to PNG": "In PNG konvertieren",
    "Convert to WebP": "In WebP konvertieren",
    "Resize Images": "Bildgröße ändern",
    "Compress Images": "Bilder komprimieren",
    "Split Image": "Bild aufteilen",
    "Extract Colors": "Farben extrahieren",
    "Convert to Base64": "In Base64 konvertieren",
    "Download All JPG": "Alle JPGs herunterladen",
    "Download All PNG": "Alle PNGs herunterladen",
    "Download All WebP": "Alle WebPs herunterladen",
    "Download All": "Alle herunterladen",
    "Convert More Images": "Weitere Bilder konvertieren",
    "Start Over": "Neu starten",

    # Processing areas
    "Selected PNG Images": "Ausgewählte PNG-Bilder",
    "Selected JPG Images": "Ausgewählte JPG-Bilder",
    "Selected WebP Images": "Ausgewählte WebP-Bilder",
    "Selected Images": "Ausgewählte Bilder",
    "Selected Image": "Ausgewähltes Bild",
    "Conversion Options": "Konvertierungsoptionen",
    "Resize Options": "Größenänderungsoptionen",
    "Compression Options": "Komprimierungsoptionen",
    "Split Options": "Aufteilungsoptionen",
    "JPG Quality": "JPG-Qualität",
    "PNG Quality": "PNG-Qualität",
    "WebP Quality": "WebP-Qualität",
    "Quality": "Qualität",
    "Target Size": "Zielgröße",
    "Width": "Breite",
    "Height": "Höhe",
    "Rows": "Zeilen",
    "Columns": "Spalten",
    "Maintain Aspect Ratio": "Seitenverhältnis beibehalten",
    "Smaller file": "Kleinere Datei",
    "Higher quality": "Höhere Qualität",

    # Status messages
    "Conversion Complete!": "Konvertierung abgeschlossen!",
    "Resize Complete!": "Größenänderung abgeschlossen!",
    "Compression Complete!": "Komprimierung abgeschlossen!",
    "Split Complete!": "Aufteilung abgeschlossen!",
    "Processing...": "Verarbeitung...",
    "Complete!": "Abgeschlossen!",

    # Features
    "Fast Conversion": "Schnelle Konvertierung",
    "High Quality Output": "Qualitativ hochwertige Ausgabe",
    "Batch Processing": "Batch-Verarbeitung",
    "Privacy Protection": "Datenschutz",
    "Why Use Our": "Warum unseren",
    "Why Use Our PNG to JPG Converter": "Warum unseren PNG zu JPG Konverter",
    "Why Use Our JPG to PNG Converter": "Warum unseren JPG zu PNG Konverter",
    "Why Use Our Image Resizer": "Warum unsere Bildgrößenänderung",
    "Why Use Our Image Compressor": "Warum unseren Bildkompressor",
    "Why Use Our Image Splitter": "Warum unseren Bildteiler",
    "Why Use Our Color Extractor": "Warum unseren Farbextrahierer",
    "Why Use Our Base64 Converter": "Warum unseren Base64 Konverter",

    # How to sections
    "How to Convert PNG to JPG Online Free": "Wie man PNG kostenlos online in JPG konvertiert",
    "How to Convert JPG to PNG Online Free": "Wie man JPG kostenlos online in PNG konvertiert",
    "How to Resize Images Online Free": "Wie man Bilder kostenlos online in der Größe ändert",
    "How to Compress Images Online Free": "Wie man Bilder kostenlos online komprimiert",
    "How to Split Images Online Free": "Wie man Bilder kostenlos online aufteilt",
    "How to Extract Colors Online Free": "Wie man Farben kostenlos online extrahiert",
    "How to Convert to Base64 Online Free": "Wie man kostenlos online in Base64 konvertiert",

    # Tips sections
    "PNG to JPG Tips": "PNG zu JPG Tipps",
    "JPG to PNG Tips": "JPG zu PNG Tipps",
    "Image Resize Tips": "Bildgröße ändern Tipps",
    "Image Compression Tips": "Bildkomprimierung Tipps",
    "Image Splitter Tips": "Bildteiler Tipps",
    "Color Extraction Tips": "Farbextraktion Tipps",
    "Base64 Conversion Tips": "Base64 Konvertierung Tipps",

    # FAQ
    "Frequently Asked Questions": "Häufig gestellte Fragen",
    "Does PNG to JPG conversion affect image quality?": "Beeinträchtigt die Konvertierung von PNG zu JPG die Bildqualität?",
    "Will I lose transparency converting PNG to JPG?": "Verliere ich Transparenz bei der Konvertierung von PNG zu JPG?",
    "How fast is the PNG to JPG conversion?": "Wie schnell ist die PNG-zu-JPG-Konvertierung?",
    "How many PNG files can I convert at once?": "Wie viele PNG-Dateien kann ich gleichzeitig konvertieren?",

    # Footer
    "More Tools": "Weitere Tools",
    "Image Resizer": "Bildgrößenänderung",
    "Image Compressor": "Bildkomprimierung",
    "PNG to WebP": "PNG zu WebP",
    "WebP to PNG": "WebP zu PNG",
    "JPG to WebP": "JPG zu WebP",

    # Taglines
    "PNG to JPG Converter": "PNG zu JPG Konverter",
    "JPG to PNG Converter": "JPG zu PNG Konverter",
    "WebP to PNG Converter": "WebP zu PNG Konverter",
    "PNG to WebP Converter": "PNG zu WebP Konverter",
    "JPG to WebP Converter": "JPG zu WebP Konverter",
    "Image Resizer": "Bildgrößenänderung",
    "Image Compressor": "Bildkomprimierung",
    "Image Splitter": "Bildteiler",
    "Color Extractor": "Farbextrahierer",
    "Base64 Converter": "Base64 Konverter",

    # Common UI
    "Free online": "Kostenloses Online",
    "free online": "kostenloses Online",
    "online converter": "Online-Konverter",
    "batch conversion": "Batch-Konvertierung",
    "high-quality output": "qualitativ hochwertige Ausgabe",
    "no registration required": "keine Anmeldung erforderlich",
    "local processing for privacy": "lokale Verarbeitung für den Datenschutz",
    "Supports batch conversion": "Unterstützt Batch-Konvertierung",
    "supports multiple selection": "unterstützt Mehrfachauswahl",
    "supports batch conversion,": "unterstützt Batch-Konvertierung,",
}

def apply_comprehensive_translations(content):
    """Apply all translations to content"""
    for en, de in sorted(TRANSLATIONS.items(), key=len, reverse=True):
        content = content.replace(en, de)
    return content

def translate_faq_schema(faq_content):
    """Translate FAQ schema content"""
    faq_translations = {
        "Does PNG to JPG conversion affect image quality?": "Beeinträchtigt die Konvertierung von PNG zu JPG die Bildqualität?",
        "Will I lose transparency converting PNG to JPG?": "Verliere ich Transparenz bei der Konvertierung von PNG zu JPG?",
        "How fast is the PNG to JPG conversion?": "Wie schnell ist die PNG-zu-JPG-Konvertierung?",
        "How many PNG files can I convert at once?": "Wie viele PNG-Dateien kann ich gleichzeitig konvertieren?",
        "Yes, JPG uses lossy compression, so there is some quality loss. Our tool lets you adjust the quality from 10% to 100%. For most web uses, 80-90% quality produces visually identical results to the original PNG while cutting file size by 80% or more. Set it higher for prints and archival where every pixel matters.": "Ja, JPG verwendet verlustbehaftete Komprimierung, sodass es zu einem gewissen Qualitätsverlust kommt. Mit unserem Tool können Sie die Qualität von 10% bis 100% einstellen. Für die meisten Webanwendungen liefert eine Qualität von 80-90% visuell identische Ergebnisse zum ursprünglichen PNG bei gleichzeitiger Reduzierung der Dateigröße um 80% oder mehr. Stellen Sie für Drucke und Archive, wo jeder Pixel zählt, einen höheren Wert ein.",
        "Yes. JPG does not support transparency. Any transparent areas in your PNG will be filled with white. If you need to preserve transparency, consider keeping the original PNG or using a format like WebP that supports both transparency and good compression.": "Ja. JPG unterstützt keine Transparenz. Alle transparenten Bereiche in Ihrem PNG werden mit weiß gefüllt. Wenn Sie die Transparenz beibehalten müssen, erwägen Sie, das ursprüngliche PNG zu behalten oder ein Format wie WebP zu verwenden, das sowohl Transparenz als auch gute Komprimierung unterstützt.",
        "The conversion is instant and happens entirely in your browser using Canvas technology. Even large files or batch conversions complete in milliseconds. The speed depends on your device's processing power, but there is no server upload or waiting.": "Die Konvertierung ist sofort und erfolgt vollständig in Ihrem Browser mit Canvas-Technologie. Selbst große Dateien oder Batch-Konvertierungen werden in Millisekunden abgeschlossen. Die Geschwindigkeit hängt von der Verarbeitungsleistung Ihres Geräts ab, aber es gibt kein Server-Upload oder Warten.",
        "There is no limit on the number of files. Select a whole folder of PNGs and convert them all at once. Each image is processed independently, and you can download them individually or click 'Download All' to get everything in one go.": "Es gibt keine Begrenzung für die Anzahl der Dateien. Wählen Sie einen gesamten Ordner mit PNGs aus und konvertieren Sie alle auf einmal. Jedes Bild wird unabhängig verarbeitet, und Sie können sie einzeln herunterladen oder auf 'Alle herunterladen' klicken, um alles auf einmal zu erhalten.",
    }

    for en, de in faq_translations.items():
        faq_content = faq_content.replace(en, de)

    return faq_content

def process_html_file(source_file, target_file):
    """Process and translate a single HTML file"""

    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Set lang attribute
    content = re.sub(r'<html lang="[^"]*">', '<html lang="de">', content)

    # Detect page type for specific translations
    page_type = "generic"
    if "png-to-jpg" in str(source_file):
        page_type = "png-to-jpg"
    elif "jpg-to-png" in str(source_file):
        page_type = "jpg-to-png"
    elif "webp-to-png" in str(source_file):
        page_type = "webp-to-png"
    elif "png-to-webp" in str(source_file):
        page_type = "png-to-webp"
    elif "jpg-to-webp" in str(source_file):
        page_type = "jpg-to-webp"
    elif "resize-image" in str(source_file):
        page_type = "resize-image"
    elif "compress-image" in str(source_file):
        page_type = "compress-image"
    elif "image-splitter" in str(source_file):
        page_type = "image-splitter"
    elif "extract-colors" in str(source_file):
        page_type = "extract-colors"
    elif "image-to-base64" in str(source_file):
        page_type = "image-to-base64"

    # Translate title based on page type
    if page_type == "png-to-jpg":
        content = re.sub(r'<title>.*?</title>', '<title>PNG zu JPG - Kostenloser Online PNG zu JPG Konverter | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online PNG zu JPG Konverter. Konvertieren Sie schnell PNG-Bilder in das JPG-Format. Unterstützt Batch-Konvertierung, qualitativ hochwertige Ausgabe, keine Anmeldung erforderlich, lokale Verarbeitung für den Datenschutz.">', content)
    elif page_type == "jpg-to-png":
        content = re.sub(r'<title>.*?</title>', '<title>JPG zu PNG - Kostenloser Online JPG zu PNG Konverter | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online JPG zu PNG Konverter. Konvertieren Sie schnell JPG-Bilder in das PNG-Format. Behalten Sie die Transparenz bei, unterstützen Batch-Konvertierung.">', content)
    elif page_type == "webp-to-png":
        content = re.sub(r'<title>.*?</title>', '<title>WebP zu PNG - Kostenloser Online WebP zu PNG Konverter | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online WebP zu PNG Konverter. Konvertieren Sie schnell WebP-Bilder in das PNG-Format. Behalten Sie die Transparenz bei, unterstützen Batch-Konvertierung.">', content)
    elif page_type == "png-to-webp":
        content = re.sub(r'<title>.*?</title>', '<title>PNG zu WebP - Kostenloser Online PNG zu WebP Konverter | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online PNG zu WebP Konverter. Konvertieren Sie schnell PNG-Bilder in das WebP-Format. Unterstützt Transparenz und Batch-Konvertierung.">', content)
    elif page_type == "jpg-to-webp":
        content = re.sub(r'<title>.*?</title>', '<title>JPG zu WebP - Kostenloser Online JPG zu WebP Konverter | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online JPG zu WebP Konverter. Konvertieren Sie schnell JPG-Bilder in das WebP-Format. Unterstützt Batch-Konvertierung mit qualitativ hochwertiger Ausgabe.">', content)
    elif page_type == "resize-image":
        content = re.sub(r'<title>.*?</title>', '<title>Bildgröße ändern - Kostenloser Online Bildgrößenänderer | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloses Online-Tool zur Bildgrößenänderung. Ändern Sie die Größe von Bildern schnell und einfach. Unterstützt Batch-Verarbeitung, benutzerdefinierte Abmessungen, Seitenverhältnis beibehalten.">', content)
    elif page_type == "compress-image":
        content = re.sub(r'<title>.*?</title>', '<title>Bild komprimieren - Kostenloser Online Bildkompressor | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online Bildkompressor. Komprimieren Sie Bilder schnell und einfach. Unterstützt Batch-Verarbeitung, Qualitätssteuerung, keine Anmeldung erforderlich.">', content)
    elif page_type == "image-splitter":
        content = re.sub(r'<title>.*?</title>', '<title>Bild aufteilen - Kostenloser Online Bildteiler | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online Bildteiler. Teilen Sie Bilder in mehrere Teile auf. Unterstützt benutzerdefinierte Zeilen und Spalten für Social-Media-Grids.">', content)
    elif page_type == "extract-colors":
        content = re.sub(r'<title>.*?</title>', '<title>Farben extrahieren - Kostenloser Online Farbextrahierer | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online Farbextrahierer. Extrahieren Sie Farben aus Bildern und erhalten Sie Farbpaletten mit HEX- und RGB-Werten.">', content)
    elif page_type == "image-to-base64":
        content = re.sub(r'<title>.*?</title>', '<title>Bild zu Base64 - Kostenloser Online Base64 Konverter | PicEte</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Kostenloser Online Bild zu Base64 Konverter. Konvertieren Sie Bilder in Base64-Strings für die Verwendung in HTML und CSS.">', content)

    # Update URLs
    content = re.sub(r'<link rel="canonical" href="https://picete\.com/([^"]*)"', r'<link rel="canonical" href="https://picete.com/de/\1"', content)
    content = re.sub(r'<meta property="og:url" content="https://picete\.com/([^"]*)"', r'<meta property="og:url" content="https://picete.com/de/\1"', content)

    # Update paths
    content = re.sub(r'href="\.\./css/style\.css"', 'href="../../css/style.css"', content)
    content = re.sub(r'src="\.\./images/', 'src="../../images/', content)
    content = re.sub(r'href="\.\./favicon\.', 'href="../../favicon.', content)
    content = re.sub(r'href="\.\./llms\.txt"', 'href="../../llms.txt"', content)
    content = re.sub(r'href="\.\./mcp\.json"', 'href="../../mcp.json"', content)
    content = re.sub(r'href="\.\./"', 'href="/de/"', content)
    content = re.sub(r'href="\.\./#tools"', 'href="/de/#tools"', content)

    # Update internal links
    def update_internal_link(match):
        path = match.group(1)
        if path.startswith("http") or "css/" in path or "images/" in path or "favicon" in path or "llms.txt" in path or "mcp.json" in path:
            return match.group(0)
        return f'href="/de/{path}"'

    content = re.sub(r'href="\.\./([^"]+)"', update_internal_link, content)

    # Apply comprehensive translations
    content = apply_comprehensive_translations(content)

    return content

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
    print("🚀 Starting final comprehensive German translation of 22 PicEte sub-pages...")
    print("=" * 70)

    success_count = 0
    fail_count = 0

    for source_file, target_file in PAGES:
        source_path = BASE_DIR / source_file
        target_path = DE_DIR / target_file

        try:
            if source_path.exists():
                print(f"📝 Processing: {source_file}")
                translated_content = process_html_file(source_path, target_path)

                target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(translated_content)

                print(f"✅ Success: {target_file}")
                success_count += 1
            else:
                print(f"❌ Source not found: {source_file}")
                fail_count += 1
        except Exception as e:
            print(f"❌ Error processing {source_file}: {e}")
            fail_count += 1

    print("=" * 70)
    print(f"📊 Translation complete: {success_count} ✅ succeeded, {fail_count} ❌ failed")

    if fail_count == 0:
        print("🎉 All pages translated successfully!")
    else:
        print("⚠️  Some pages had issues - please review the errors above")

if __name__ == "__main__":
    main()