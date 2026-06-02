"""Fix remaining untranslated FAQ content - supplementary pass for edge cases."""
import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))

# Map: filepath -> list of (old_answer, new_question, new_answer) for HTML fix
# For files where questions are already translated but answers are in English
FILE_FIXES = {
    # DE png-to-jpg: German Q, English A
    "de/png-to-jpg/index.html": {
        "Yes, JPG uses lossy compression, so there is some quality loss.": "Ja, JPG verwendet verlustbehaftete Komprimierung, sodass es zu einem gewissen Qualitätsverlust kommt. Unser Tool lässt Sie die Qualität von 10% bis 100% einstellen. Für die meisten Web-Anwendungen erzeugt 80-90% Qualität visuell identische Ergebnisse zum Original-PNG bei einer Dateigrößenreduzierung von 80% oder mehr.",
        "Yes. JPG does not support transparency.": "Ja. JPG unterstützt keine Transparenz. Alle transparenten Bereiche Ihres PNG werden mit Weiß gefüllt. Wenn Sie Transparenz erhalten müssen, behalten Sie das Original-PNG oder verwenden Sie ein Format wie WebP, das sowohl Transparenz als auch gute Komprimierung unterstützt.",
        "The conversion is instant and happens entirely in your browser using Canvas technology.": "Die Konvertierung erfolgt sofort und passiert vollständig in Ihrem Browser mittels Canvas-Technologie. Auch große Dateien oder Batch-Konvertierungen werden in Millisekunden abgeschlossen. Die Geschwindigkeit hängt von der Leistungsfähigkeit Ihres Geräts ab.",
        "There is no limit on the number of files. Select a whole folder of PNGs": "Es gibt keine Begrenzung der Dateianzahl. Wählen Sie einen ganzen Ordner mit PNGs und konvertieren Sie alle auf einmal. Jedes Bild wird unabhängig verarbeitet und Sie können sie einzeln herunterladen oder auf 'Alle herunterladen' klicken.",
    },
    # DE jpg-to-webp: mixed EN/DE questions
    "de/jpg-to-webp/index.html": {
        "How much can JPG zu WebP reduce file size?": ("Wie stark kann die Konvertierung von JPG zu WebP die Dateigröße reduzieren?", "WebP reduziert die Dateigröße typischerweise um 25-35 % im Vergleich zu JPG bei gleicher Qualität. Bei Bildern mit großen gleichmäßigen Flächen können die Einsparungen 50 % oder mehr erreichen."),
        "Can I batch convert JPG zu WebP?": ("Kann ich JPG im Batch zu WebP konvertieren?", "Ja, wählen Sie beliebig viele JPG-Dateien und konvertieren Sie alle in einem Vorgang. Das Tool verarbeitet sie gleichzeitig und zeigt Vorschauen mit Dateigrößenvergleichen an."),
    },
    # DE webp-to-png: mixed EN/DE questions
    "de/webp-to-png/index.html": {
        "Is WebP zu PNG conversion lossless?": ("Ist die Konvertierung von WebP zu PNG verlustfrei?", "Ja, unser Tool bewahrt die ursprüngliche Qualität. PNG ist ein verlustfreies Format, sodass alle Pixeldaten erhalten bleiben. Das Ausgabe-PNG ist größer, aber voll kompatibel."),
        "Why would I convert WebP zu PNG?": ("Warum sollte ich WebP zu PNG konvertieren?", "WebP ist hervorragend für die Web-Performance, aber nicht alle Software unterstützt es. Konvertieren Sie zu PNG für ältere Bildeditoren, Plattformen ohne WebP-Unterstützung oder zum Teilen. PNG funktioniert überall."),
        "How do I convert WebP zu PNG in bulk?": ("Wie konvertiere ich WebP im Batch zu PNG?", "Ziehen Sie mehrere WebP-Dateien per Drag & Drop in den Upload-Bereich oder wählen Sie alle gleichzeitig aus. Das Tool verarbeitet jede Datei parallel."),
    },
    # ES jpg-to-webp: mixed EN/ES questions
    "es/jpg-to-webp/index.html": {
        "How much can JPG a WebP reduce file size?": ("¿Cuánto puede reducir JPG a WebP el tamaño del archivo?", "WebP normalmente reduce el tamaño entre un 25-35% comparado con JPG al mismo nivel de calidad. Para imágenes con grandes áreas suaves, el ahorro puede llegar al 50% o más."),
        "Can I batch convert JPG a WebP?": ("¿Puedo convertir JPG a WebP por lotes?", "Sí, seleccione tantos archivos JPG como necesite y conviértalos en una sola operación. La herramienta los procesa simultáneamente."),
    },
    # ES png-to-jpg: Spanish Q, English A
    "es/png-to-jpg/index.html": {
        "The conversion is instant and happens entirely in your browser using Canvas technology.": "La conversión es instantánea y ocurre completamente en su navegador usando tecnología Canvas. Incluso archivos grandes o conversiones por lotes se completan en milisegundos.",
        "There is no limit on the number of files. Select a whole folder of PNGs": "No hay límite en la cantidad de archivos. Seleccione una carpeta completa de PNGs y conviértalos todos a la vez. Cada imagen se procesa independientemente.",
    },
    # ES webp-to-png: mixed EN/ES questions
    "es/webp-to-png/index.html": {
        "Is WebP a PNG conversion lossless?": ("¿La conversión de WebP a PNG es sin pérdida?", "Sí, nuestra herramienta preserva la calidad original. PNG es un formato sin pérdida, por lo que todos los datos se conservan. El PNG resultante será más grande pero totalmente compatible."),
        "Why would I convert WebP a PNG?": ("¿Por qué convertiría WebP a PNG?", "WebP es excelente para la web, pero no todo el software lo admite. Convierta a PNG para editores antiguos, plataformas sin soporte WebP, o compartir con personas sin navegadores modernos."),
        "How do I convert WebP a PNG in bulk?": ("¿Cómo convierto WebP a PNG en lote?", "Arrastre y suelte múltiples archivos WebP en el área de carga o selecciónelos todos a la vez. La herramienta procesa cada archivo en paralelo."),
    },
    # AR remaining single FAQs
    "ar/png-to-jpg-for-email/index.html": {
        "Absolutely. Select all the screenshots or images you want to email": "بالتأكيد. حدد جميع لقطات الشاشة أو الصور التي تريد إرسالها بالبريد الإلكتروني وقم بتحويلها دفعة واحدة. الأداة تعالج كل شيء في وقت واحد، ويمكنك تحميل كل JPG على حدة أو جميعها مرة واحدة.",
    },
    "ar/png-to-webp-for-wordpress/index.html": {
        "WebP fully supports alpha transparency": "WebP يدعم بالكامل شفافية ألفا، لذا شعاراتك ورسوماتك PNG الشفافة ستعمل بشكل مثالي كـ WebP على ووردبريس. يتم الحفاظ على الشفافية أثناء التحويل ويعرضها ووردبريس بشكل صحيح.",
    },
    "ar/webp-to-png-for-website/index.html": {
        "Yes, upload all your WebP assets at once.": "نعم، ارفع جميع ملفات WebP دفعة واحدة. الأداة تعالجها دفعياً وتحافظ على أسماء الملفات بامتداد .png لسهولة التكامل مع موقعك.",
    },
    # JA compress-image remaining 2 FAQs
    "ja/compress-image/index.html": {
        "No. All compression happens locally in your browser using the Canvas API.": "いいえ。すべての圧縮はブラウザ内のCanvas APIを使用してローカルで行われます。画像がデバイスの外に出ることはありません。プライバシーが保証され、機密コンテンツにも安全にご利用いただけます。",
        "Our compressor supports JPG, JPEG, PNG, WebP, GIF, and BMP.": "当社の圧縮ツールはJPG、JPEG、PNG、WebP、GIF、BMPに対応しています。圧縮はJPGとWebPフォーマットで最も効果的です。PNG画像の場合は、JPGまたはWebPへのフォーマット変換と組み合わせることで、品質への影響を最小限に抑えつつ80〜90%のサイズ削減が可能です。",
    },
    # PT image-to-base64: all 4 FAQs
    "pt/image-to-base64/index.html": {
        "What is Base64 encoding used for?": ("Para que serve a codificação Base64?", "A codificação Base64 converte dados binários de imagem em formato de texto que pode ser incorporado diretamente em HTML, CSS ou JavaScript. Usos comuns incluem: incorporar ícones pequenos em CSS sem requisições HTTP, criar URIs de dados para páginas HTML de arquivo único, armazenar imagens em bancos de dados como texto."),
        "How much larger is the Base64 output compared to the original?": ("Quanto maior é a saída Base64 comparada ao original?", "A codificação Base64 aumenta o tamanho do arquivo em aproximadamente 33% comparado ao arquivo binário original. Para imagens pequenas (menos de 10KB), esta sobrecarga é aceitável pela conveniência de incorporação. Para imagens maiores, Base64 é ineficiente."),
        "Can I convert multiple images to Base64 at once?": ("Posso converter várias imagens para Base64 de uma vez?", "Sim, carregue várias imagens e cada uma é convertida para Base64 independentemente. Todos os resultados são exibidos com botões de cópia para fácil recuperação."),
        "What format is the Base64 output?": ("Qual é o formato da saída Base64?", "A saída inclui o prefixo data URI (ex: 'data:image/png;base64,...') para que a string funcione imediatamente em atributos HTML src, propriedades CSS background-image ou objetos JavaScript Image."),
    },
    # PT png-to-jpg: mixed PT/EN
    "pt/png-to-jpg/index.html": {
        "The conversion is instant and happens entirely in your browser using Canvas technology.": "A conversão é instantânea e acontece inteiramente no seu navegador usando tecnologia Canvas. Mesmo arquivos grandes ou conversões em lote são concluídos em milissegundos.",
        "There is no limit on the number of files. Select a whole folder of PNGs": "Não há limite no número de arquivos. Selecione uma pasta inteira de PNGs e converta todos de uma vez. Cada imagem é processada independentemente.",
    },
}


def fix_remaining_file(filepath: str) -> int:
    """Fix remaining untranslated FAQs in a single file."""
    relpath = os.path.relpath(filepath, BASE).replace('\\', '/')
    if relpath not in FILE_FIXES:
        return 0

    fixes = FILE_FIXES[relpath]
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    total_fixes = 0

    for key, value in fixes.items():
        if isinstance(value, tuple):
            # (new_question, new_answer) - replace both Q and A
            new_q, new_a = value
            # Find the summary/answer pair containing this key
            pattern = rf'(<summary\s+class="faq-question"[^>]*>)(.*?)(</summary>\s*<p\s+class="faq-answer"[^>]*>)(.*?)(</p>)'
            for match in re.finditer(pattern, content, re.DOTALL):
                old_q = match.group(2).strip()
                old_a = match.group(4).strip()
                # Check if this FAQ's question or answer contains the key
                if key in old_q or key in old_a:
                    replacement = f'{match.group(1)}{new_q}{match.group(3)}{new_a}{match.group(5)}'
                    content = content.replace(match.group(0), replacement, 1)
                    total_fixes += 2  # Q + A
                    break
        else:
            # Just replace the answer text
            if key in content:
                # Find the faq-answer containing this key
                pattern = r'(<p\s+class="faq-answer"[^>]*>)(.*?)(</p>)'
                for match in re.finditer(pattern, content, re.DOTALL):
                    if key in match.group(2):
                        old_full = match.group(0)
                        new_full = f'{match.group(1)}{value}{match.group(3)}'
                        content = content.replace(old_full, new_full, 1)
                        total_fixes += 1
                        break

    # Also fix JSON-LD for these entries
    def fix_jsonld(json_str):
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            return json_str

        changed = False
        def process(entity):
            nonlocal changed
            if not isinstance(entity, dict):
                return
            if entity.get('@type') == 'FAQPage':
                for item in entity.get('mainEntity', []):
                    name = item.get('name', '')
                    text = item.get('acceptedAnswer', {}).get('text', '')
                    for key, value in fixes.items():
                        if key in name or key in text:
                            if isinstance(value, tuple):
                                item['name'] = value[0]
                                item['acceptedAnswer']['text'] = value[1]
                            else:
                                item['acceptedAnswer']['text'] = value
                            changed = True
            if '@graph' in entity:
                for g in entity['@graph']:
                    process(g)

        process(data)
        if changed:
            return json.dumps(data, ensure_ascii=False, indent=2)
        return json_str

    content = re.sub(
        r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>',
        lambda m: f'<script type="application/ld+json">{fix_jsonld(m.group(1))}</script>',
        content, flags=re.DOTALL
    )

    if total_fixes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return total_fixes


def main():
    total = 0
    for relpath in FILE_FIXES:
        fpath = os.path.join(BASE, relpath)
        if os.path.isfile(fpath):
            n = fix_remaining_file(fpath)
            if n > 0:
                print(f"  Fixed {n} entries in {relpath}")
                total += n
    print(f"\nTotal: {total} entries fixed")


if __name__ == '__main__':
    main()
