"""Fix untranslated FAQ content across all language directories.
Replaces English FAQ entries in both HTML and JSON-LD sections."""
import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))

# Translation database: maps English Q -> {lang: (translated_q, translated_a)}
TRANSLATIONS = {
    # ============================================================
    # compress-image (DE, ES, PT)
    # ============================================================
    "How much can I compress an image without visible quality loss?": {
        "de": ("Wie stark kann ich ein Bild komprimieren, ohne sichtbare Qualitätsverluste zu sehen?", "Die meisten Bilder können um 50-80 % komprimiert werden, bevor Qualitätsverluste sichtbar werden. Fotos mit sanften Farbverläufen komprimieren sich bei 60-70 % Qualität gut. Textreiche Screenshots benötigen höhere Qualität (85-90 %), um die Kanten scharf zu halten. Unser Schieberegler hilft Ihnen, den optimalen Punkt für jedes Bild zu finden."),
        "es": ("¿Cuánto puedo comprimir una imagen sin pérdida de calidad visible?", "La mayoría de las imágenes se pueden comprimir entre un 50-80% antes de que la pérdida de calidad sea notable. Las fotos con gradientes suaves se comprimen bien al 60-70% de calidad. Las capturas de pantalla con mucho texto necesitan mayor calidad (85-90%) para mantener los bordes nítidos. Nuestro control deslizante le permite encontrar el punto óptimo para cada imagen."),
        "pt": ("Quanto posso comprimir uma imagem sem perda visível de qualidade?", "A maioria das imagens pode ser comprimida em 50-80% antes que a perda de qualidade se torne visível. Fotos com gradientes suaves comprimem bem a 60-70% de qualidade. Capturas de tela com muito texto precisam de qualidade mais alta (85-90%) para manter as bordas nítidas. Nosso controle deslizante permite encontrar o ponto ideal para cada imagem."),
    },
    "Is the compression lossy or lossless?": {
        "de": ("Ist die Komprimierung verlustbehaftet oder verlustfrei?", "Unser Tool verwendet standardmäßig verlustbehaftete Komprimierung (JPEG/WebP-Neucodierung), die deutlich kleinere Dateigrößen erzielt als verlustfreie Methoden. Der Qualitätsregler steuert den Kompromiss. Bei PNG-Bildern empfehlen wir die gleichzeitige Konvertierung in JPEG oder WebP für eine maximale Dateigrößenreduzierung."),
        "es": ("¿La compresión es con pérdida o sin pérdida?", "Nuestra herramienta utiliza compresión con pérdida (recodificación JPEG/WebP) de forma predeterminada, lo que logra archivos mucho más pequeños que los métodos sin pérdida. El control de calidad ajusta el equilibrio. Para imágenes PNG, recomendamos convertir a JPEG o WebP durante la compresión para obtener la máxima reducción de tamaño."),
        "pt": ("A compressão é com perdas ou sem perdas?", "Nossa ferramenta usa compressão com perdas (recodificação JPEG/WebP) por padrão, alcançando tamanhos de arquivo muito menores que métodos sem perdas. O controle de qualidade ajusta o equilíbrio. Para imagens PNG, recomendamos converter para JPEG ou WebP durante a compressão para máxima redução de tamanho."),
    },
    "Are my images uploaded to any server during compression?": {
        "de": ("Werden meine Bilder während der Komprimierung auf einen Server hochgeladen?", "Nein. Die gesamte Komprimierung erfolgt lokal in Ihrem Browser über die Canvas-API. Ihre Bilder verlassen niemals Ihr Gerät. Dies garantiert Ihre Privatsphäre und macht unseren Kompressor sicher für vertrauliche Inhalte."),
        "es": ("¿Se suben mis imágenes a algún servidor durante la compresión?", "No. Toda la compresión se realiza localmente en su navegador mediante la API Canvas. Sus imágenes nunca salen de su dispositivo. Esto garantiza su privacidad y hace que nuestro compresor sea seguro para contenido confidencial."),
        "pt": ("Minhas imagens são enviadas para algum servidor durante a compressão?", "Não. Toda a compressão acontece localmente no seu navegador usando a API Canvas. Suas imagens nunca saem do seu dispositivo. Isso garante sua privacidade e torna nosso compressor seguro para conteúdo confidencial."),
    },
    "What file types can I compress?": {
        "de": ("Welche Dateitypen kann ich komprimieren?", "Unser Kompressor unterstützt JPG, JPEG, PNG, WebP, GIF und BMP. Die Komprimierung funktioniert am besten bei JPG- und WebP-Formaten. Bei PNG-Bildern empfiehlt sich die Kombination aus Komprimierung und Formatkonvertierung in JPG oder WebP für eine maximale Reduzierung — oft 80-90 % kleiner bei minimalem Qualitätsverlust."),
        "es": ("¿Qué tipos de archivos puedo comprimir?", "Nuestro compresor admite JPG, JPEG, PNG, WebP, GIF y BMP. La compresión funciona mejor con formatos JPG y WebP. Para imágenes PNG, combine la compresión con la conversión a JPG o WebP para obtener la máxima reducción de tamaño, a menudo un 80-90% más pequeño con un impacto mínimo en la calidad."),
        "pt": ("Quais tipos de arquivo posso comprimir?", "Nosso compressor suporta JPG, JPEG, PNG, WebP, GIF e BMP. A compressão funciona melhor nos formatos JPG e WebP. Para imagens PNG, combine compressão com conversão para JPG ou WebP para máxima redução de tamanho — geralmente 80-90% menor com impacto mínimo na qualidade."),
    },
    # ============================================================
    # extract-colors (DE, ES, JA, PT)
    # ============================================================
    "How many colors can the extractor detect?": {
        "de": ("Wie viele Farben kann der Extraktor erkennen?", "Unser Tool kann 5, 10, 15 oder 20 dominante Farben aus jedem Bild extrahieren. Es verwendet einen Median-Schnitt-Algorithmus, um die repräsentativsten Farben zu identifizieren. Mehr Farben liefern feinere Details, während weniger eine vereinfachte Palette ergeben, perfekt für Branding und Design."),
        "es": ("¿Cuántos colores puede detectar el extractor?", "Nuestra herramienta puede extraer 5, 10, 15 o 20 colores dominantes de cualquier imagen. Utiliza un algoritmo de cuantización de corte mediano para identificar los colores más representativos. Más colores dan mayor detalle, mientras que menos ofrecen una paleta simplificada perfecta para branding y diseño."),
        "ja": ("カラーチャートは何色まで検出できますか？", "このツールでは、5色、10色、15色、または20色の主要なカラーを抽出できます。中央値カット量子化アルゴリズムを使用して、最も代表的な色を特定します。色数を多くすると細かいディテールが得られ、少なくするとブランディングやデザインに最適なシンプルなパレットになります。"),
        "pt": ("Quantas cores o extrator pode detectar?", "Nossa ferramenta pode extrair 5, 10, 15 ou 20 cores dominantes de qualquer imagem. Usa um algoritmo de quantização de corte mediano para identificar as cores mais representativas. Mais cores dão detalhes mais finos, enquanto menos cores oferecem uma paleta simplificada perfeita para branding e design."),
    },
    "Can I copy the hex codes from the extracted palette?": {
        "de": ("Kann ich die Hex-Codes aus der extrahierten Palette kopieren?", "Ja. Jede extrahierte Farbe wird mit ihrem Hex-Code angezeigt. Klicken Sie auf den Code, um ihn sofort in die Zwischenablage zu kopieren. Sie können auch die gesamte Palette als kommagetrennte Liste von Hex-Codes für Design-Tools wie Figma, Adobe oder Tailwind-CSS-Projekte kopieren."),
        "es": ("¿Puedo copiar los códigos hexadecimales de la paleta extraída?", "Sí. Cada color extraído muestra su código hexadecimal. Haga clic en el código para copiarlo al portapapeles al instante. También puede copiar la paleta completa como una lista separada por comas para importar a herramientas como Figma, Adobe o proyectos Tailwind CSS."),
        "ja": ("抽出されたパレットのHEXカラーコードをコピーできますか？", "はい。抽出された各カラーにはHEXコードが表示されます。コードをクリックするだけで即座にクリップボードにコピーできます。Figma、Adobe、Tailwind CSSなどのデザインツール用に、カンマ区切りのHEXコードリストとしてパレット全体をコピーすることも可能です。"),
        "pt": ("Posso copiar os códigos hexadecimais da paleta extraída?", "Sim. Cada cor extraída é exibida com seu código hexadecimal. Clique no código para copiá-lo instantaneamente para a área de transferência. Você também pode copiar a paleta completa como uma lista separada por vírgulas para importar em ferramentas como Figma, Adobe ou projetos Tailwind CSS."),
    },
    "What image formats work with the color extractor?": {
        "de": ("Welche Bildformate sind mit dem Farbextraktor kompatibel?", "Alle gängigen Bildformate werden unterstützt: JPG, JPEG, PNG, WebP, GIF und BMP. Der Extraktionsalgorithmus arbeitet mit den Pixeldaten nach dem Laden im Browser. Bilder mit höherer Auflösung liefern genauere Ergebnisse — laden Sie die bestmögliche Version hoch."),
        "es": ("¿Qué formatos de imagen son compatibles con el extractor de colores?", "Todos los formatos principales son compatibles: JPG, JPEG, PNG, WebP, GIF y BMP. El algoritmo funciona con los datos de píxeles después de cargar la imagen en el navegador. Las imágenes de mayor resolución producen resultados más precisos, así que suba la versión de mayor calidad disponible."),
        "ja": ("カラーチャートはどの画像フォーマットに対応していますか？", "JPG、JPEG、PNG、WebP、GIF、BMPなど、すべての主要な画像フォーマットに対応しています。抽出アルゴリズムは、ブラウザに画像が読み込まれた後のピクセルデータに基づいて動作します。高解像度の画像ほど正確な結果が得られるため、最高品質のバージョンをアップロードしてください。"),
        "pt": ("Quais formatos de imagem funcionam com o extrator de cores?", "Todos os principais formatos são suportados: JPG, JPEG, PNG, WebP, GIF e BMP. O algoritmo de extração funciona com os dados de pixels após a imagem carregar no navegador. Imagens de maior resolução produzem resultados mais precisos, então envie a versão de melhor qualidade disponível."),
    },
    "How accurate is the color extraction?": {
        "de": ("Wie genau ist die Farbgewinnung?", "Der Median-Schnitt-Algorithmus ist sehr zuverlässig bei der Identifizierung dominanter Farben. Er analysiert jeden Pixel, um die häufigsten Farbcluster zu finden. Bei Bildern mit tausenden subtiler Farbschattierungen kann die Palette jedoch vereinfacht ausfallen, da das Tool das Bild auf eine begrenzte Anzahl von Farbgruppen reduziert."),
        "es": ("¿Qué tan precisa es la extracción de colores?", "El algoritmo de corte mediano es muy confiable para identificar colores dominantes. Analiza cada píxel para encontrar los grupos de colores más frecuentes. Sin embargo, las imágenes con miles de tonos sutiles pueden producir una paleta simplificada porque la herramienta reduce la imagen a un número limitado de grupos de colores."),
        "ja": ("カラー抽出の精度はどの程度ですか？", "中央値カットアルゴリズムは主要なカラーの特定において非常に信頼性が高いです。すべてのピクセルを分析して最も頻度の高いカラークラスターを見つけます。ただし、何千もの微妙な色合いを含む画像では、限られた数のカラーグループに減らすため、パレットが簡略化される場合があります。"),
        "pt": ("Quão precisa é a extração de cores?", "O algoritmo de corte mediano é muito confiável para identificar cores dominantes. Ele analisa cada pixel para encontrar os agrupamentos de cores mais frequentes. No entanto, imagens com milhares de tons sutis podem produzir uma paleta simplificada porque a ferramenta reduz a imagem a um número limitado de grupos de cores."),
    },
    # ============================================================
    # jpg-to-png (DE, ES, PT)
    # ============================================================
    "Does converting JPG to PNG lose quality?": {
        "de": ("Geht bei der Konvertierung von JPG zu PNG Qualität verloren?", "Nein. Die Konvertierung von JPG zu PNG ist verlustfrei — PNG bewahrt jedes Detail des ursprünglichen JPG. Die Konvertierung eines komprimierten JPG stellt jedoch keine verlorenen Details wieder her. Die Dateigröße wird zudem deutlich zunehmen, da PNG volle Pixeldaten speichert."),
        "es": ("¿La conversión de JPG a PNG pierde calidad?", "No. La conversión de JPG a PNG es sin pérdida — PNG conserva cada detalle del JPG original. Sin embargo, convertir un JPG comprimido a PNG no restaurará los detalles perdidos durante la compresión original. El tamaño del archivo también aumentará significativamente."),
        "pt": ("A conversão de JPG para PNG perde qualidade?", "Não. A conversão de JPG para PNG é sem perdas — PNG preserva cada detalhe do JPG original. No entanto, converter um JPG já comprimido para PNG não restaurará detalhes perdidos durante a compressão original. O tamanho do arquivo também aumentará significativamente."),
    },
    "Why would I convert JPG to PNG?": {
        "de": ("Warum sollte ich JPG zu PNG konvertieren?", "Konvertieren Sie JPG zu PNG, wenn Sie verlustfreie Qualität für die Bearbeitung benötigen, Ihr Design-Workflow das PNG-Format erfordert oder die Ausgabe mehrmals bearbeitet wird. PNG unterstützt auch Transparenz. Ideal für Screenshots, Grafiken und Inhalte mit scharfen Kanten."),
        "es": ("¿Por qué convertiría JPG a PNG?", "Convierta JPG a PNG cuando necesite calidad sin pérdida para edición, cuando su flujo de diseño requiera formato PNG, o cuando la salida se editará múltiples veces. PNG también admite transparencia. Es ideal para capturas de pantalla, gráficos y contenido que requiere bordes nítidos."),
        "pt": ("Por que converteria JPG para PNG?", "Converta JPG para PNG quando precisar de qualidade sem perdas para edição, quando seu fluxo de design exigir formato PNG, ou quando a saída será editada várias vezes. PNG também suporta transparência. É ideal para capturas de tela, gráficos e conteúdo que exija bordas nítidas."),
    },
    "Will the file size be larger after conversion?": {
        "de": ("Wird die Dateigröße nach der Konvertierung größer?", "Ja, PNG-Dateien sind 5-10x größer als die ursprünglichen JPG-Dateien. Die verlustfreie Komprimierung bewahrt jeden Pixel, erfordert jedoch mehr Speicherplatz. Für Fotos auf Websites ist JPG oft praktischer. Verwenden Sie PNG, wenn Qualitätserhaltung wichtiger ist als die Dateigröße."),
        "es": ("¿El tamaño del archivo será mayor después de la conversión?", "Sí, espere que los archivos PNG sean 5-10 veces más grandes que los JPG originales. La compresión sin pérdida conserva cada píxel pero requiere más almacenamiento. Para fotos en sitios web, JPG suele ser más práctico. Use PNG cuando la calidad sea más importante que el tamaño."),
        "pt": ("O tamanho do arquivo será maior após a conversão?", "Sim, espere que arquivos PNG sejam 5-10 vezes maiores que os JPG originais. A compressão sem perdas preserva cada pixel mas exige mais armazenamento. Para fotos em sites, JPG geralmente é mais prático. Use PNG quando a qualidade for mais importante que o tamanho."),
    },
    "Can I convert multiple JPG images at once?": {
        "de": ("Kann ich mehrere JPG-Bilder gleichzeitig konvertieren?", "Absolut. Wählen Sie mehrere JPG-Dateien aus und unser Tool konvertiert sie alle gleichzeitig. Jedes Bild erhält eine eigene Vorschau mit der neuen Dateigröße. Laden Sie PNGs einzeln herunter oder klicken Sie auf 'Alle herunterladen' für den Massendownload."),
        "es": ("¿Puedo convertir múltiples imágenes JPG a la vez?", "Por supuesto. Seleccione múltiples archivos JPG y nuestra herramienta los convierte todos simultáneamente. Cada imagen obtiene su propia vista previa. Descargue los PNG uno por uno o use 'Descargar todo' para descarga masiva."),
        "pt": ("Posso converter várias imagens JPG de uma vez?", "Com certeza. Selecione vários arquivos JPG e nossa ferramenta converte todos simultaneamente. Cada imagem recebe sua própria prévia. Baixe os PNGs individualmente ou clique em 'Baixar tudo' para download em lote."),
    },
    # ============================================================
    # jpg-to-webp (DE, ES, JA, PT)
    # ============================================================
    "How much can JPG to WebP reduce file size?": {
        "de": ("Wie stark kann die Konvertierung von JPG zu WebP die Dateigröße reduzieren?", "WebP reduziert die Dateigröße typischerweise um 25-35 % im Vergleich zu JPG bei gleicher Qualität. Bei Bildern mit großen gleichmäßigen Flächen können die Einsparungen 50 % oder mehr erreichen. Niedrigere Qualitätseinstellungen in WebP erzeugen deutlich bessere Ergebnisse als vergleichbare JPG-Komprimierung."),
        "es": ("¿Cuánto puede reducir JPG a WebP el tamaño del archivo?", "WebP normalmente reduce el tamaño entre un 25-35% comparado con JPG al mismo nivel de calidad. Para imágenes con grandes áreas suaves como cielos, el ahorro puede llegar al 50% o más. Configuraciones más bajas en WebP producen mejores resultados que la compresión JPG equivalente."),
        "ja": ("JPGからWebPへの変換でファイルサイズはどれくらい小さくなりますか？", "WebPは同じ品質レベルのJPGと比較して、通常25〜35%ファイルサイズを削減できます。空やグラデーションのような滑らかな領域が多い画像では50%以上の削減が可能です。WebPの低品質設定でも同等のJPG圧縮より良好な結果が得られます。"),
        "pt": ("Quanto a conversão de JPG para WebP pode reduzir o tamanho do arquivo?", "WebP normalmente reduz o tamanho em 25-35% comparado ao JPG no mesmo nível de qualidade. Para imagens com grandes áreas uniformes como céus, a economia pode chegar a 50% ou mais. Configurações mais baixas no WebP produzem resultados melhores que a compressão JPG equivalente."),
    },
    "Is WebP quality better than JPG at the same file size?": {
        "de": ("Ist die WebP-Qualität bei gleicher Dateigröße besser als JPG?", "Ja. WebP verwendet fortschrittlichere Komprimierungsalgorithmen, die weniger Artefakte erzeugen als JPG bei äquivalenten Bitraten. Sie können die Qualität in WebP niedriger einstellen und erhalten dennoch ein besseres Bild als bei JPG."),
        "es": ("¿Es la calidad de WebP mejor que JPG con el mismo tamaño?", "Sí. WebP utiliza algoritmos más avanzados que producen menos artefactos que JPG a tasas equivalentes. Puede configurar calidad más baja en WebP y aún obtener una imagen mejor que JPG."),
        "ja": ("同じファイルサイズの場合、WebPの品質はJPGより優れていますか？", "はい。WebPはより高度な圧縮アルゴリズムを使用し、同等のビットレートでJPGより少ないアーティファクトを生成します。WebPで品質を低く設定してもJPGより見た目の良い画像が得られます。"),
        "pt": ("A qualidade do WebP é melhor que JPG no mesmo tamanho?", "Sim. WebP usa algoritmos mais avançados que produzem menos artefatos que JPG em taxas equivalentes. Você pode definir qualidade mais baixa no WebP e ainda assim obter uma imagem melhor que JPG."),
    },
    "Does WebP support metadata from the original JPG?": {
        "de": ("Unterstützt WebP die Metadaten des ursprünglichen JPG?", "WebP unterstützt EXIF- und XMP-Metadaten. Unser Tool bewahrt grundlegende Bilddaten. Bei kritischen Metadaten wie GPS-Koordinaten überprüfen Sie die Ausgabe. Die meisten modernen Bildverwaltungstools verarbeiten WebP-Metadaten korrekt."),
        "es": ("¿WebP admite los metadatos del JPG original?", "WebP admite metadatos EXIF y XMP. Nuestra herramienta preserva los datos básicos. Para metadatos críticos como coordenadas GPS, verifique la salida. La mayoría de las herramientas modernas manejan metadatos WebP correctamente."),
        "ja": ("WebPは元のJPGのメタデータをサポートしていますか？", "WebPフォーマットはEXIFおよびXMPメタデータをサポートしています。このツールは基本的な画像データを保持します。GPS座標などの重要なメタデータについては、出力を確認してください。"),
        "pt": ("O WebP suporta os metadados do JPG original?", "WebP suporta metadados EXIF e XMP. Nossa ferramenta preserva dados básicos. Para metadados críticos como coordenadas GPS, verifique a saída. A maioria das ferramentas modernas lida com metadados WebP corretamente."),
    },
    "Can I batch convert JPG to WebP?": {
        "de": ("Kann ich JPG im Batch zu WebP konvertieren?", "Ja, wählen Sie beliebig viele JPG-Dateien und konvertieren Sie alle in einem Vorgang. Das Tool verarbeitet sie gleichzeitig und zeigt Vorschauen mit Dateigrößenvergleichen. Laden Sie Dateien einzeln oder im Batch herunter."),
        "es": ("¿Puedo convertir JPG a WebP por lotes?", "Sí, seleccione tantos archivos JPG como necesite y conviértalos en una sola operación. La herramienta los procesa simultáneamente. Descargue archivos individualmente o use la descarga por lotes."),
        "ja": ("JPGを一括でWebPに変換できますか？", "はい、必要な数のJPGファイルを選択して一度の操作で全て変換できます。ツールが同時に処理し、ファイルサイズの比較プレビューを表示します。"),
        "pt": ("Posso converter JPG para WebP em lote?", "Sim, selecione quantos arquivos JPG precisar e converta todos em uma única operação. A ferramenta os processa simultaneamente. Baixe arquivos individuais ou use o download em lote."),
    },
    # ============================================================
    # png-to-webp (DE, ES, JA, PT)
    # ============================================================
    "How much smaller is WebP compared to PNG?": {
        "de": ("Wie viel kleiner ist WebP im Vergleich zu PNG?", "WebP reduziert die Dateigröße typischerweise um 25-35 % bei gleicher Qualität. Bei verlustbehafteter Komprimierung erreichen die Einsparungen 80-90 %. Bei verlustfreiem WebP erhalten Sie immer noch etwa 30 % kleinere Dateien."),
        "es": ("¿Cuánto más pequeño es WebP comparado con PNG?", "WebP normalmente reduce el tamaño entre un 25-35% manteniendo la misma calidad visual. Con compresión con pérdida, el ahorro llega al 80-90%. Para WebP sin pérdida, aún obtiene archivos aproximadamente un 30% más pequeños."),
        "ja": ("WebPはPNGと比べてどれくらい小さくなりますか？", "WebPは同じ視覚品質を維持したまま、PNGと比較して通常25〜35%ファイルサイズを削減します。ロッシー圧縮では80〜90%の削減が可能です。ロスレスWebPでも約30%小さいファイルが得られます。"),
        "pt": ("Quanto menor é WebP comparado ao PNG?", "WebP normalmente reduz o tamanho em 25-35% mantendo a mesma qualidade visual. Com compressão com perdas, a economia chega a 80-90%. Para WebP sem perdas, você ainda obtém arquivos cerca de 30% menores."),
    },
    "Does WebP support transparency like PNG?": {
        "de": ("Unterstützt WebP Transparenz wie PNG?", "Ja, WebP unterstützt vollständig Alpha-Transparenzkanäle. Transparente PNGs werden perfekt zu WebP konvertiert. Das macht WebP zum idealen Ersatz für PNG im Web — gleiche Qualität mit Transparenz, aber deutlich kleinere Dateien."),
        "es": ("¿WebP admite transparencia como PNG?", "Sí, WebP admite completamente canales de transparencia alfa. Puede convertir PNGs transparentes a WebP perfectamente. Esto convierte a WebP en un reemplazo ideal para PNG en la web."),
        "ja": ("WebPはPNGのように透過をサポートしていますか？", "はい、WebPはアルファ透過チャンネルを完全にサポートしています。透過付きのPNGを完璧にWebPに変換できます。WebPはWebにおけるPNGの理想的な代替です。"),
        "pt": ("O WebP suporta transparência como o PNG?", "Sim, o WebP suporta totalmente canais de transparência alfa. Você pode converter PNGs transparentes para WebP perfeitamente. Isso torna o WebP um substituto ideal para PNG na web."),
    },
    "Is WebP supported in all browsers?": {
        "de": ("Wird WebP von allen Browsern unterstützt?", "WebP wird von allen modernen Browsern unterstützt: Chrome (seit 2010), Firefox (seit 2018), Safari (seit 2020) und Edge (seit 2018). Über 97 % der Web-Nutzer können WebP-Bilder anzeigen."),
        "es": ("¿WebP es compatible con todos los navegadores?", "WebP es compatible con todos los navegadores modernos: Chrome (desde 2010), Firefox (desde 2018), Safari (desde 2020) y Edge (desde 2018). Más del 97% de los usuarios web pueden ver imágenes WebP."),
        "ja": ("WebPはすべてのブラウザでサポートされていますか？", "Chrome（2010年以降）、Firefox（2018年以降）、Safari（2020年以降）、Edge（2018年以降）など、すべての主要ブラウザでサポートされています。Webユーザーの97%以上がWebP画像を表示できます。"),
        "pt": ("O WebP é suportado em todos os navegadores?", "WebP é suportado por todos os navegadores modernos: Chrome (desde 2010), Firefox (desde 2018), Safari (desde 2020) e Edge (desde 2018). Mais de 97% dos usuários web podem visualizar imagens WebP."),
    },
    "Should I convert all my PNGs to WebP?": {
        "de": ("Sollte ich alle meine PNGs zu WebP konvertieren?", "Für die Web-Nutzung: Ja — der Ersatz von PNG durch WebP verbessert die Ladezeit ohne Qualitätsverlust. Für Bilder zum Bearbeiten oder Teilen außerhalb des Webs behalten Sie das Original-PNG."),
        "es": ("¿Debería convertir todos mis PNG a WebP?", "Para uso web, sí: reemplazar PNG con WebP mejora la velocidad de carga sin pérdida de calidad. Para imágenes que necesite editar fuera de la web, conserve el PNG original."),
        "ja": ("すべてのPNGをWebPに変換すべきですか？", "Webでの使用においてはイエスです。PNGをWebPに置き換えることで品質を損なうことなく読み込み速度が向上します。Web以外で編集が必要な画像は元のPNGを保管してください。"),
        "pt": ("Devo converter todos os meus PNGs para WebP?", "Para uso na web, sim — substituir PNG por WebP melhora a velocidade de carregamento sem perda de qualidade. Para imagens que você precisa editar fora da web, mantenha o PNG original."),
    },
    # ============================================================
    # resize-image (DE, ES, JA, PT)
    # ============================================================
    "Does resizing an image affect its quality?": {
        "de": ("Beeinträchtigt die Größenänderung eines Bildes dessen Qualität?", "Das Verkleinern erhält die wahrgenommene Qualität gut, da überschüssige Pixel zusammengeführt werden. Das Vergrößern führt zu Qualitätsverlust, da Pixel erzeugt werden müssen. Verwenden Sie immer das größtmögliche Quellbild zum Vergrößern."),
        "es": ("¿Cambiar el tamaño de una imagen afecta su calidad?", "Reducir el tamaño conserva bien la calidad porque los píxeles excesivos se combinan. Aumentar el tamaño causa pérdida de calidad porque el software tiene que inventar píxeles. Siempre comience con la imagen más grande disponible para ampliar."),
        "ja": ("画像のリサイズは品質に影響しますか？", "縮小は余分なピクセルが統合されるため、品質がよく保たれます。拡大はピクセルを生成する必要があるため、品質の低下を招きます。拡大する場合は、常に最大のソース画像を使用してください。"),
        "pt": ("Redimensionar uma imagem afeta sua qualidade?", "Reduzir preserva bem a qualidade porque pixels excessivos são mesclados. Ampliar causa perda de qualidade porque o software precisa inventar pixels. Sempre comece com a maior imagem disponível para ampliar."),
    },
    "What dimensions can I resize my image to?": {
        "de": ("Auf welche Abmessungen kann ich mein Bild skalieren?", "Sie können beliebige Breiten und Höhen in Pixeln eingeben. Das Tool behält standardmäßig das Seitenverhältnis bei. Gängige Voreinstellungen: 1080×1080 (Instagram), 1920×1080 (HD), 800×800 (Produktfotos), 1200×630 (Social Media)."),
        "es": ("¿A qué dimensiones puedo cambiar el tamaño de mi imagen?", "Puede ingresar cualquier ancho y alto en píxeles. La herramienta mantiene la relación de aspecto por defecto. Preajustes comunes: 1080×1080 (Instagram), 1920×1080 (HD), 800×800 (productos), 1200×630 (redes sociales)."),
        "ja": ("画像をどのサイズにリサイズできますか？", "幅と高さをピクセル単位で自由に入力できます。デフォルトでアスペクト比を維持します。一般的なプリセット：1080×1080（Instagram）、1920×1080（HD）、800×800（商品写真）、1200×630（SNS）。"),
        "pt": ("Para quais dimensões posso redimensionar minha imagem?", "Você pode inserir qualquer largura e altura em pixels. A ferramenta mantém a proporção por padrão. Predefinições comuns: 1080×1080 (Instagram), 1920×1080 (HD), 800×800 (produtos), 1200×630 (redes sociais)."),
    },
    "Will metadata be preserved after resizing?": {
        "de": ("Werden Metadaten nach der Größenänderung beibehalten?", "Grundlegende Metadaten können entfernt werden, da das Tool das Bild neu generiert. Für die meisten Web-Anwendungen ist dies unproblematisch. Bei Bedarf an EXIF-Daten speichern Sie vorab eine Kopie des Originals."),
        "es": ("¿Se conservarán los metadatos después de cambiar el tamaño?", "Los metadatos básicos pueden eliminarse ya que la herramienta regenera la imagen. Para la mayoría de usos web no es un problema. Si necesita datos EXIF, guarde una copia del original antes."),
        "ja": ("リサイズ後もメタデータは保持されますか？", "ツールが画像を再生成するため、基本的なメタデータは削除される場合があります。ほとんどのWeb用途では問題ありません。EXIFデータが必要な場合は、事前に元の画像のコピーを保存してください。"),
        "pt": ("Os metadados serão preservados após o redimensionamento?", "Metadados básicos podem ser removidos pois a ferramenta regenera a imagem. Para a maioria dos usos web não é problema. Se precisar de dados EXIF, salve uma cópia do original antes."),
    },
    "How many images can I resize at once?": {
        "de": ("Wie viele Bilder kann ich gleichzeitig skalieren?", "Es gibt keine Begrenzung. Laden Sie mehrere Bilder hoch und skalieren Sie alle auf dieselben Abmessungen in einem Batch-Vorgang. Jedes Bild wird unabhängig verarbeitet."),
        "es": ("¿Cuántas imágenes puedo redimensionar a la vez?", "No hay límite. Suba múltiples imágenes y redimensiónelas todas a las mismas dimensiones en una sola operación. Cada imagen se procesa independientemente."),
        "ja": ("一度に何枚の画像をリサイズできますか？", "制限はありません。複数の画像をアップロードし、一度のバッチ処理ですべて同じサイズにリサイズできます。各画像は個別に処理されます。"),
        "pt": ("Quantas imagens posso redimensionar de uma vez?", "Não há limite. Carregue várias imagens e redimensione todas para as mesmas dimensões em uma única operação. Cada imagem é processada independentemente."),
    },
    # ============================================================
    # webp-to-png (DE, ES, PT)
    # ============================================================
    "Is WebP to PNG conversion lossless?": {
        "de": ("Ist die Konvertierung von WebP zu PNG verlustfrei?", "Ja, unser Tool bewahrt die ursprüngliche Qualität. PNG ist ein verlustfreies Format, sodass alle Pixeldaten erhalten bleiben. Das Ausgabe-PNG ist größer als das WebP, aber voll kompatibel mit allen Plattformen."),
        "es": ("¿La conversión de WebP a PNG es sin pérdida?", "Sí, nuestra herramienta preserva la calidad original. PNG es un formato sin pérdida, por lo que todos los datos se conservan. El PNG resultante será más grande pero totalmente compatible."),
        "pt": ("A conversão de WebP para PNG é sem perdas?", "Sim, nossa ferramenta preserva a qualidade original. PNG é um formato sem perdas, então todos os dados de pixels são mantidos. O PNG resultante será maior mas totalmente compatível."),
    },
    "Why would I convert WebP to PNG?": {
        "de": ("Warum sollte ich WebP zu PNG konvertieren?", "WebP ist hervorragend für die Web-Performance, aber nicht alle Software unterstützt es. Konvertieren Sie zu PNG für ältere Bildeditoren, Plattformen ohne WebP-Unterstützung oder zum Teilen mit Personen ohne moderne Browser. PNG funktioniert überall."),
        "es": ("¿Por qué convertiría WebP a PNG?", "WebP es excelente para la web, pero no todo el software lo admite. Convierta a PNG para editores antiguos, plataformas sin soporte WebP, o compartir con personas sin navegadores modernos. PNG funciona en todas partes."),
        "pt": ("Por que converteria WebP para PNG?", "WebP é ótimo para a web, mas nem todo software suporta. Converta para PNG para editores legados, plataformas sem suporte WebP, ou compartilhar com pessoas sem navegadores modernos. PNG funciona em qualquer lugar."),
    },
    "Does WebP transparency transfer to PNG?": {
        "de": ("Wird die WebP-Transparenz auf PNG übertragen?", "Ja. Beide Formate unterstützen Alpha-Transparenz. Bei der Konvertierung werden alle Transparenzinformationen perfekt erhalten — sicher für Grafiken, Logos und Symbole mit transparenten Hintergründen."),
        "es": ("¿La transparencia de WebP se transfiere a PNG?", "Sí. Ambos formatos admiten canales de transparencia alfa. Toda la información de transparencia se conserva perfectamente durante la conversión."),
        "pt": ("A transparência do WebP é transferida para PNG?", "Sim. Ambos formatos suportam canais de transparência alfa. Todas as informações de transparência são preservadas perfeitamente durante a conversão."),
    },
    "How do I convert WebP to PNG in bulk?": {
        "de": ("Wie konvertiere ich WebP im Batch zu PNG?", "Ziehen Sie mehrere WebP-Dateien per Drag & Drop in den Upload-Bereich oder wählen Sie alle gleichzeitig aus. Das Tool verarbeitet jede Datei parallel und zeigt Vorschauen an."),
        "es": ("¿Cómo convierto WebP a PNG en lote?", "Arrastre y suelte múltiples archivos WebP en el área de carga o selecciónelos todos a la vez. La herramienta procesa cada archivo en paralelo y muestra vistas previas."),
        "pt": ("Como converto WebP para PNG em lote?", "Arraste e solte vários arquivos WebP na área de upload ou selecione todos de uma vez. A ferramenta processa cada arquivo em paralelo e exibe prévias."),
    },
    # ============================================================
    # Shared single-FAQ entries (png-to-jpg-for-email, png-to-webp-for-wordpress, webp-to-png-for-website)
    # ============================================================
    "Can I batch convert multiple PNGs for email?": {
        "de": ("Kann ich mehrere PNGs gleichzeitig für E-Mail konvertieren?", "Absolut. Wählen Sie alle gewünschten Screenshots oder Bilder und konvertieren Sie sie in einem Batch. Das Tool verarbeitet alles gleichzeitig, und Sie können jedes JPG einzeln oder alle auf einmal herunterladen."),
        "es": ("¿Puedo convertir múltiples PNG por lotes para correo electrónico?", "Por supuesto. Seleccione todas las capturas o imágenes que desee enviar por correo y conviértalas en un lote. La herramienta procesa todo simultáneamente y puede descargar cada JPG individualmente o todos a la vez."),
        "pt": ("Posso converter vários PNGs em lote para e-mail?", "Com certeza. Selecione todas as capturas de tela ou imagens que deseja enviar por e-mail e converta-as em lote. A ferramenta processa tudo simultaneamente e você pode baixar cada JPG individualmente ou todos de uma vez."),
    },
    "Will conversion affect image transparency for WordPress?": {
        "de": ("Beeinträchtigt die Konvertierung die Bildtransparenz für WordPress?", "WebP unterstützt vollständig Alpha-Transparenz, sodass Ihre transparenten PNG-Logos und -Grafiken als WebP in WordPress einwandfrei funktionieren. Die Transparenz wird bei der Konvertierung erhalten und in WordPress korrekt angezeigt."),
        "es": ("¿La conversión afectará la transparencia de la imagen en WordPress?", "WebP admite completamente la transparencia alfa, por lo que sus logos y gráficos PNG transparentes funcionarán perfectamente como WebP en WordPress. La transparencia se conserva durante la conversión."),
        "pt": ("A conversão afetará a transparência da imagem no WordPress?", "WebP suporta totalmente transparência alfa, então seus logotipos e gráficos PNG transparentes funcionarão perfeitamente como WebP no WordPress. A transparência é preservada durante a conversão."),
    },
    "Can I batch convert multiple WebP images for my website?": {
        "de": ("Kann ich mehrere WebP-Bilder gleichzeitig für meine Website konvertieren?", "Ja, laden Sie alle WebP-Dateien auf einmal hoch. Das Tool verarbeitet sie im Batch und behält die Dateinamen mit der Endung .png bei — einfach herunterladen und ins CMS hochladen."),
        "es": ("¿Puedo convertir múltiples imágenes WebP por lotes para mi sitio web?", "Sí, suba todos sus archivos WebP a la vez. La herramienta los procesa por lotes conservando los nombres con extensión .png para una fácil integración en su sitio web."),
        "pt": ("Posso converter várias imagens WebP em lote para meu site?", "Sim, envie todos os seus arquivos WebP de uma vez. A ferramenta os processa em lote preservando os nomes com extensão .png para fácil integração no seu site."),
    },
    # ============================================================
    # AR-only: compress-image-for-email, compress-image-for-website, compress-image-for-wordpress, compress-image-to-200kb, compress-image-to-500kb, compress-jpg-to-100kb, jpg-to-png-for-instagram
    # ============================================================
    "What are email attachment size limits?": {
        "ar": ("ما هي حدود حجم مرفقات البريد الإلكتروني؟", "يسمح Gmail بمرفقات تصل إلى 25 ميجابايت لكل بريد. Outlook لديه حد 20 ميجابايت لمعظم الحسابات. العديد من أنظمة البريد المؤسسية تفرض حدود 10 ميجابايت. عند إرسال صور متعددة، فإن إبقاء كل صورة تحت 500 كيلوبايت يضمن إرفاق 40-50 صورة في Gmail دون تجاوز الحد."),
    },
    "Can I send unlimited photos by compressing them?": {
        "ar": ("هل يمكنني إرسال عدد غير محدود من الصور عن طريق ضغطها؟", "ليس غير محدود، لكن الضغط يزيد السعة بشكل كبير. صور iPhone غير المضغوطة حجمها 3-5 ميجابايت لكل منها — يمكنك إرفاق 5-8 فقط في بريد 25 ميجابايت. عند الضغط إلى 300 كيلوبايت، يمكنك إرسال أكثر من 80 صورة. للمجموعات الكبيرة جداً، استخدم روابط التخزين السحابي."),
    },
    "Should I resize or compress for email attachments?": {
        "ar": ("هل يجب تغيير الحجم أم الضغط لمرفقات البريد الإلكتروني؟", "كلاهما. غيّر الحجم أولاً إلى أبعاد مناسبة (1200-1600 بكسل عرض كافٍ)، ثم اضغط لتقليل حجم الملف. يستقبل معظم المستلمين البريد على الهواتف حيث لا حاجة لدقة 4K. تغيير الحجم من 4000 إلى 1200 بكسل يمكن أن يقلل الحجم بنسبة 60% قبل بدء الضغط."),
    },
    "Which format is best for web images?": {
        "ar": ("ما هو أفضل تنسيق لصور الويب؟", "JPG الأفضل للصور المعقدة. PNG مثالي للرسومات التي تحتوي على نص أو شعارات أو شفافية. WebP يوفر ضغطاً أفضل بنسبة 25-35% من JPG ومدعوم من 95% من المتصفحات. للتوافق الأقصى، استخدم JPG كبديل."),
    },
    "How much does image compression affect page speed?": {
        "ar": ("كم يؤثر ضغط الصور على سرعة الصفحة؟", "ضغط الصور هو أكثر طريقة فعالة لتحسين سرعة الصفحة. الصور غير المحسنة (2-5 ميجابايت لكل منها) قد تستغرق 10+ ثوانٍ للتحميل على الهاتف. الضغط إلى أقل من 500 كيلوبايت يقلل وقت التحميل إلى 1-2 ثانية. إصلاح تحسين الصور يمكن أن يحسن تقييمك بنسبة 20-30 نقطة."),
    },
    "Does WordPress automatically compress images?": {
        "ar": ("هل يقوم ووردبريس بضغط الصور تلقائياً؟", "نعم، يقوم ووردبريس بضغط صور JPG عند الرفع بجودة 82% افتراضياً، لكن هذا ليس كافياً لاحتياجات أداء الويب الحديثة. الضغط المسبق مع PicEte قبل الرفع يمنحك تحكماً أفضل وأحجام ملفات أصغر."),
    },
    "Should I use WebP for WordPress?": {
        "ar": ("هل يجب استخدام WebP لووردبريس؟", "نعم، WebP ممتاز لووردبريس. أصغر بنسبة 25-35% من JPG المكافئ بجودة مماثلة. العديد من القوالب الحديثة تدعم WebP أصلاً. للقوالب القديمة، استخدم إضافات تقدم WebP للمتصفحات الداعمة مع الرجوع إلى JPG."),
    },
    "How do I speed up WordPress with image optimization?": {
        "ar": ("كيف أسرّع ووردبريس بتحسين الصور؟", "اضغط جميع الصور قبل الرفع باستخدام PicEte. استخدم أبعاداً مناسبة — لا ترفع صوراً بعرض 4000 بكسل لمنطقة محتوى 800 بكسل. فعّل التحميل الكسول في ووردبريس. فكر في إضافة تخزين مؤقت وشبكة CDN. الصور المحسنة جيداً يمكن أن تقطع أوقات التحميل بنسبة 50% أو أكثر."),
    },
    "How do I compress an image to under 200KB?": {
        "ar": ("كيف أضغط صورة إلى أقل من 200 كيلوبايت؟", "ارفع صورتك إلى PicEte واستخدم شريط تمرير الجودة لإيجاد التوازن الصحيح. لصورة 1920×1080، جودة 50-70% عادة تصل إلى أقل من 200 كيلوبايت. الصور الأصغر مثل 800×600 يمكنها استخدام جودة 70-85%. الأداة تعرض حجم ملف الإخراج في الوقت الفعلي."),
    },
    "Why do I need to compress images to 200KB?": {
        "ar": ("لماذا أحتاج لضغط الصور إلى 200 كيلوبايت؟", "200 كيلوبايت هو حد حجم ملف شائق لتحميل المستندات وتطبيقات المنحstudette وبوابات التوظيف وبعض أنظمة إدارة المحتوى. العديد من النماذج عبر الإنترنت ترفض الصور الأكبر من 200 كيلوبايت لتقليل حمل الخادم."),
    },
    "Will compressing to 200KB lose image quality?": {
        "ar": ("هل سيؤدي الضغط إلى 200 كيلوبايت إلى فقدان جودة الصورة؟", "بعض فقدان الجودة أمر لا مفر منه عند الضغط إلى 200 كيلوبايت، لكن PicEte يستخدم ضغط JPEG ذكي يقلل التشوهات المرئية. عند 200 كيلوبايت، معظم الصور تبدو ممتازة على الشاشات وتطبع جيداً حتى 5×7 بوصة."),
    },
    "Can I batch compress images to 200KB?": {
        "ar": ("هل يمكنني ضغط صور متعددة إلى 200 كيلوبايت؟", "نعم. ارفع صوراً متعددة والأداة تعالجها جميعاً في وقت واحد. بما أن كل صورة تحتاج مستويات ضغط مختلفة للوصول إلى 200 كيلوبايت، قد تحتاج لضبط شريط الجودة لكل واحدة."),
    },
    "How do I compress images to under 500KB?": {
        "ar": ("كيف أضغط صوراً إلى أقل من 500 كيلوبايت؟", "ارفع صورتك إلى PicEte واضبط شريط تمرير الجودة. لصورة 1920×1080، جودة 60-80% عادة تعطي ملفات 300-500 كيلوبايت. لصور أصغر مثل 1200×800، جودة 70-85% تعمل جيداً. الأداة تعرض حجم الإخراج في الوقت الفعلي."),
    },
    "Will 500KB compression affect print quality?": {
        "ar": ("هل سيؤثر ضغط 500 كيلوبايت على جودة الطباعة؟", "ملفات 500 كيلوبايت عادة تطبع جيداً حتى 8×10 بوصة بدقة 150 DPI. لطباعة الصور القياسية (4×6 أو 5×7)، تبدو الصور المضغوطة 500 كيلوبايت ممتازة. معظم المستخدمين لا يمكنهم التمييز بين الصورة المضغوطة والأصلية عند المشاهدة العادية."),
    },
    "Can I batch compress to 500KB?": {
        "ar": ("هل يمكنني الضغط الدفعي إلى 500 كيلوبايت؟", "بالتأكيد. ارفع جميع صورك دفعة واحدة وPicEte يعالجها في وقت واحد. اضبط شريط الجودة مرة واحدة، وسيتم ضغط جميع الصور تقريباً لنفس المستوى. تحقق من أحجام الملفات الفردية قبل التحميل."),
    },
    "How do I compress a JPG to exactly 100KB?": {
        "ar": ("كيف أضغط JPG إلى 100 كيلوبايت بالضبط؟", "ارفع JPG إلى PicEte واستخدم شريط تمرير الجودة. لصورة 1920×1080، جودة 30-50% عادة تحقق 100 كيلوبايت. الصور الأصغر مثل 1200×800 قد تحتاج جودة 40-60%. الأداة تعرض حجم الإخراج في الوقت الفعلي."),
    },
    "Why compress JPG specifically instead of PNG?": {
        "ar": ("لماذا ضغط JPG تحديداً بدلاً من PNG؟", "JPG مضغوط أصلاً، مما يجعله مثالياً لتحقيق أحجام ملفات صغيرة مثل 100 كيلوبايت. ملفات PNG بدون فقدان ولا تضغط بكفاءة. إذا كان لديك PNG يحتاج أن يكون 100 كيلوبايت، حوّله إلى JPG أولاً. PicEte يتعامل مع كلا التنسيقين."),
    },
    "Will JPG compression at 100KB look acceptable?": {
        "ar": ("هل سيبدو ضغط JPG عند 100 كيلوبايت مقبولاً؟", "عند 100 كيلوبايت، ضغط JPG ملحوظ لكنه مقبول للعديد من الأغراض. الصور تبدو جيدة على الشاشات وعلى الويب. للتطبيقات الحرجة مثل الطباعة الاحترافية، 100 كيلوبايت قد يكون صغيراً جداً. لصور المستندات وصور الهوية ورفع الويب، 100 كيلوبايت عادة كافٍ تماماً."),
    },
    "Can I batch compress multiple JPGs to 100KB?": {
        "ar": ("هل يمكنني ضغط عدة ملفات JPG دفعة واحدة إلى 100 كيلوبايت؟", "نعم. ارفع جميع ملفات JPG دفعة واحدة وPicEte يعالجها في وقت واحد. بما أن كل صورة لها خصائص ضغط مختلفة، قد تحتاج لضبط شريط الجودة لكل صورة. اطلع على النتائج قبل التحميل."),
    },
    "Why convert JPG to PNG for Instagram?": {
        "ar": ("لماذا تحويل JPG إلى PNG لإنستغرام؟", "PNG تنسيق بدون فقدان يحافظ على أقصى جودة للصورة، مما يجعله مثالياً لإنستغرام حيث الضغط أثناء الرفع قد يتلف JPG أكثر. PNG يدعم أيضاً الشفافية. بينما ملفات PNG أكبر، إنستغرام يقبلها حتى 30 ميجابايت."),
    },
    "Does Instagram accept PNG files?": {
        "ar": ("هل يقبل إنستغرام ملفات PNG؟", "نعم، إنستغرام يدعم رفع PNG بالكامل للمنشورات والقصص والريلز. يمكنك رفع ملفات PNG حتى 30 ميجابايت تماماً مثل JPG. إنستغرام يحول الصور أثناء الرفع بغض النظر عن التنسيق، لكن البدء بـ PNG عالي الجودة يمنحك أفضل فرصة للحفاظ على الوضوح."),
    },
    "Is PNG better quality than JPG for Instagram?": {
        "ar": ("هل PNG بجودة أفضل من JPG لإنستغرام؟", "PNG بدون فقدان تقنياً ويحافظ على جودة مثالية، لكن الفرق ضئيل بعد ضغط إنستغرام. لمعظم الصور، JPG بجودة 85-95% يبدو مطابقاً لـ PNG ويرفع أسرع. استخدم PNG للرسومات ذات الخطوط الحادة أو النصوص أو الشعارات."),
    },
    "Can I batch convert JPG to PNG for Instagram?": {
        "ar": ("هل يمكنني تحويل JPG متعددة إلى PNG لإنستغرام؟", "بالتأكيد. ارفع جميع ملفات JPG دفعة واحدة وPicEte يحولها جميعاً إلى PNG في وقت واحد. كل صورة تُعالج في ثوانٍ. هذا مثالي لإعداد سلسلة صور لشبكة إنستغرام. كل المعالجة تتم محلياً في متصفحك."),
    },
    # ============================================================
    # JA-only: image-splitter, image-to-base64, compress-image (partial), resize-image (partial)
    # ============================================================
    "What grid layouts are supported?": {
        "ja": ("どのようなグリッドレイアウトに対応していますか？", "カスタムの行と列に対応しています。最も一般的なレイアウトは3×3（Instagram 9グリッド）、2×2（4分割モザイク）、および水平/垂直ストリップです。3×1の三連画、4×1のストーリーストリップ、2×3の6分割グリッドなど、あらゆるグリッドサイズで画像を分割できます。"),
    },
    "Will splitting an image reduce its quality?": {
        "ja": ("画像を分割すると品質が低下しますか？", "いいえ。各分割ピースは元の画像の品質をそのまま保持します。各タイルは元のキャンバスの一部をカバーするため、個々のピースの寸法は小さくなりますが、ピクセル密度と品質は同一のままです。"),
    },
    "What is splitting an image used for?": {
        "ja": ("画像分割は何に使われますか？", "Instagramグリッド投稿（パノラマを9タイルに分割）、ビフォーアフター比較の作成、画像パズルの作成、大きなインフォグラフィックを分割、プロフィールグリッドでシームレスに見えるマルチパートソーシャルメディアコンテンツのデザインに人気があります。"),
    },
    "How do I download all the split pieces?": {
        "ja": ("分割されたすべてのピースをダウンロードするには？", "分割後、各タイルにプレビューとファイルサイズが表示されます。各ピースを個別にダウンロードするか、「すべてダウンロード」をクリックしてすべてのタイルを一度に保存できます。ファイルは順番に番号が付けられます（例：image_1x1.jpg、image_1x2.jpg）。"),
    },
    "What is Base64 encoding used for?": {
        "ja": ("Base64エンコーディングは何に使われますか？", "Base64エンコーディングはバイナリ画像データをテキスト形式に変換し、HTML、CSS、JavaScriptに直接埋め込めるようにします。小さなアイコンをCSSに埋め込む、単一ファイルHTMLページのデータURIを作成する、データベースにテキストとして保存する、Base64入力を受け付けるAPIとの連携などに使用されます。"),
    },
    "How much larger is the Base64 output compared to the original?": {
        "ja": ("Base64出力は元のファイルよりどれくらい大きくなりますか？", "Base64エンコーディングは元のバイナリファイルより約33%ファイルサイズが増加します。小さな画像（10KB未満）では、このオーバーヘッドは埋め込みの利便性に対して許容範囲です。大きな画像ではBase64は非効率です。20KBを超えるファイルはURL経由の読み込みが適しています。"),
    },
    "Can I convert multiple images to Base64 at once?": {
        "ja": ("複数の画像を一度にBase64に変換できますか？", "はい、複数の画像をアップロードすると、それぞれが独立してBase64に変換されます。すべての結果にコピーボタンが表示されます。単一プロジェクトの複数のアイコンやアセットにBase64文字列が必要な場合に特に便利です。"),
    },
    "What format is the Base64 output?": {
        "ja": ("Base64出力のフォーマットは？", "出力にはデータURIプレフィックス（例：'data:image/png;base64,...'）が含まれているため、文字列はHTML src属性、CSS background-imageプロパティ、JavaScript Imageオブジェクトで即座に使用できます。そのまま貼り付けるだけでフォーマット不要です。"),
    },
    # ============================================================
    # ES-only longtail resize tools
    # ============================================================
    "What is the ideal Twitter header image size?": {
        "es": ("¿Cuál es el tamaño ideal para la imagen de encabezado de Twitter?", "Twitter recomienda 1500x500 píxeles para banners de perfil. Esta relación 3:1 se muestra correctamente en escritorio y móvil. Tenga en cuenta que Twitter recorta la parte superior e inferior en móvil, así que evite colocar texto crítico cerca de los bordes."),
    },
    "Why is my Twitter header cut off on mobile?": {
        "es": ("¿Por qué mi encabezado de Twitter se corta en el móvil?", "Twitter muestra solo la parte central del encabezado en dispositivos móviles. El banner completo de 1500x500 es visible en escritorio, pero el móvil muestra un recorte de aproximadamente 600x200 del centro. Mantenga los elementos importantes en el tercio medio de la imagen."),
    },
    "Can I use any image format for my Twitter header?": {
        "es": ("¿Puedo usar cualquier formato de imagen para mi encabezado de Twitter?", "Twitter acepta JPG y PNG. JPG es recomendado para fotos por su tamaño menor, mientras PNG es mejor para gráficos con texto o logotipos. El tamaño máximo es 5MB. PicEte puede convertir sus imágenes al formato óptimo mientras redimensiona a 1500x500."),
    },
    "How often should I update my Twitter header?": {
        "es": ("¿Con qué frecuencia debo actualizar mi encabezado de Twitter?", "Actualice su encabezado cuando cambie su marca, tenga nuevas promociones, o quiera renovar su perfil. Muchas empresas actualizan estacionalmente. PicEte hace rápido redimensionar nuevas imágenes a 1500x500 para mantener su perfil fresco."),
    },
    "Why use 200x200 for thumbnails?": {
        "es": ("¿Por qué usar 200x200 para miniaturas?", "200x200 píxeles es ideal para miniaturas pequeñas porque es suficientemente grande para ser reconocible pero pequeño para cargar rápido. Muchos sitios web usan 200x200 para avatares, fotos de perfil en foros y vistas previas de productos. Las imágenes se mantienen claras incluso en pantallas de alta densidad."),
    },
    "Will my images be clear at 200x200?": {
        "es": ("¿Mis imágenes se verán claras a 200x200?", "Sí. 200x200 es suficiente para que las miniaturas sean claramente visibles. PicEte aplica anti-aliasing durante la reducción. Las fotos mantienen rostros reconocibles. Para logotipos e iconos, el texto permanece legible. Si necesita más detalle, considere 400x400 o 512x512."),
    },
    "Can I batch create thumbnails at 200x200?": {
        "es": ("¿Puedo crear miniaturas por lotes a 200x200?", "Por supuesto. Suba todas sus imágenes a la vez y PicEte las redimensionará todas a 200x200 simultáneamente. Cada imagen se procesa en milisegundos, por lo que puede generar cientos de miniaturas rápidamente."),
    },
    "What's the difference between 200x200 and 250x250?": {
        "es": ("¿Cuál es la diferencia entre 200x200 y 250x250?", "200x200 es 56% más pequeño en tamaño de archivo y resolución que 250x250. Use 200x200 cuando necesite tamaños mínimos y carga rápida. Use 250x250 cuando necesite un poco más de detalle. Ambos tamaños sirven propósitos similares — la elección depende de su caso específico."),
    },
    "Why is 250x250 the standard avatar size?": {
        "es": ("¿Por qué 250x250 es el tamaño estándar de avatar?", "250x250 se ha convertido en el estándar para avatares de foros, fotos de perfil comunitario e iconos de usuario. Es suficientemente grande para mostrar detalles faciales y suficientemente pequeño para cargas rápidas. La mayoría del software de foros muestra avatares a 250x250 o menos."),
    },
    "Will 250x250 look good on modern screens?": {
        "es": ("¿Se verá bien 250x250 en pantallas modernas?", "Sí. 250x250 se ve nítido en pantallas estándar y permanece claro en pantallas de alta densidad/Retina. Este tamaño proporciona suficientes píxeles para que los rostros sean reconocibles. Para necesidades profesionales, considere 512x512."),
    },
    "Can I batch resize avatar images to 250x250?": {
        "es": ("¿Puedo redimensionar avatares por lotes a 250x250?", "Por supuesto. Suba todas sus imágenes de avatar a la vez y PicEte las redimensionará todas a 250x250 simultáneamente. Cada imagen se procesa en milisegundos, ideal para crear conjuntos uniformes de avatares."),
    },
    "Should I use 250x250 or 512x512 for avatars?": {
        "es": ("¿Debo usar 250x250 o 512x512 para avatares?", "Use 250x250 para foros y comunidades donde la velocidad importa. Use 512x512 para redes profesionales como LinkedIn o cuando necesite máximo detalle. Los archivos 250x250 son 75% más pequeños que 512x512, mejores para sitios con muchos avatares por página."),
    },
    "Why is 300x250 the most popular display ad size?": {
        "es": ("¿Por qué 300x250 es el tamaño de anuncio más popular?", "300x250 (Rectángulo Mediano) es el formato de anuncio display más usado porque cabe bien en casi cualquier diseño de página. Es pequeño para no ser intrusivo pero grande para ser efectivo visualmente. Funciona en escritorio y móvil, siendo la opción predeterminada para AdSense."),
    },
    "Where are 300x250 ads commonly displayed?": {
        "es": ("¿Dónde se muestran comúnmente los anuncios 300x250?", "Los anuncios 300x250 aparecen en barras laterales, dentro de áreas de contenido y al final de artículos. Son flexibles para ajustarse a diseños de escritorio y móvil. Este formato es estándar para Google AdSense y plataformas publicitarias programáticas."),
    },
    "Will my images look good at 300x250?": {
        "es": ("¿Mis imágenes se verán bien a 300x250?", "Sí. PicEte usa reducción inteligente que preserva la claridad. Al redimensionar a 300x250, la herramienta mantiene la relación de aspecto y aplica anti-aliasing. Para mejores resultados, comience con imágenes de alta resolución de al menos 600x500."),
    },
    "Can I create multiple 300x250 ads at once?": {
        "es": ("¿Puedo crear múltiples anuncios 300x250 a la vez?", "Por supuesto. Suba todas sus imágenes de banner a la vez y PicEte las redimensionará a 300x250 simultáneamente. Cada imagen se procesa en milisegundos, ideal para crear un conjunto completo de anuncios para pruebas A/B."),
    },
    "Why is 600x600 the standard for e-commerce product photos?": {
        "es": ("¿Por qué 600x600 es el estándar para fotos de productos de comercio electrónico?", "600x600 es el requisito mínimo para imágenes de Amazon y el tamaño recomendado para eBay, Shopify y la mayoría de plataformas. Este formato cuadrado proporciona suficiente detalle para que los clientes vean los productos claramente mientras carga rápido."),
    },
    "Will 600x600 images look professional on my online store?": {
        "es": ("¿Las imágenes 600x600 se verán profesionales en mi tienda online?", "Absolutamente. 600x600 da a los clientes suficiente resolución para ampliar detalles del producto. La reducción de PicEte preserva nitidez y claridad. Resoluciones más altas como 800x800 también son compatibles si necesita más detalle."),
    },
    "Can I batch resize multiple product photos to 600x600?": {
        "es": ("¿Puedo redimensionar múltiples fotos de productos por lotes a 600x600?", "Sí. Suba todas sus fotos de productos a la vez y PicEte las redimensionará a 600x600 simultáneamente. Cada imagen se procesa en milisegundos. Perfecto para vendedores con grandes inventarios."),
    },
    "Do all e-commerce platforms accept 600x600 images?": {
        "es": ("¿Todas las plataformas de comercio electrónico aceptan imágenes 600x600?", "Prácticamente todas las plataformas principales aceptan 600x600. Amazon requiere al menos 500x500 (600x600 recomendado), eBay permite 600x600, Shopify lo soporta, y funciona en Etsy, WooCommerce y la mayoría de sistemas. Siempre verifique los requisitos específicos de su plataforma."),
    },
    # ============================================================
    # PT-only: jpg-to-png (2 EN), png-to-jpg (2 EN)
    # ============================================================
    "Beeinträchtigt die Konvertierung von PNG zu JPG die Bildqualität?": {
        # This is a DE question that appeared as EN in the scan - skip
    },
}


def is_english_text(text: str) -> bool:
    """Check if text appears to be English (not translated)."""
    markers = [' the ', ' is ', ' are ', ' can ', ' will ', ' our ', ' your ',
               ' this ', ' that ', ' with ', ' from ', ' into ', ' about ',
               'All processing', 'All compression', 'Our tool', 'Our compressor',
               'Your images', 'never leave', 'guarantees', 'No. All',
               'Yes!', 'Yes,', 'Most images', 'absolutely']
    count = sum(1 for m in markers if m.lower() in text.lower())
    return count >= 2


def fix_file(filepath: str, lang: str) -> int:
    """Fix untranslated FAQ entries in a single file. Returns number of fixes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fixes = 0

    # Fix HTML FAQ entries
    def replace_faq_html(match):
        nonlocal fixes, lang
        q_html = match.group(1)
        a_html = match.group(2)
        q_text = re.sub(r'<[^>]+>', '', q_html).strip()
        a_text = re.sub(r'<[^>]+>', '', a_html).strip()

        if not is_english_text(q_text + ' ' + a_text):
            return match.group(0)

        # Try to find translation by exact question match
        if q_text in TRANSLATIONS and lang in TRANSLATIONS[q_text]:
            tr_q, tr_a = TRANSLATIONS[q_text][lang]
            fixes += 1
            return f'<summary class="faq-question">{tr_q}</summary>\n<p class="faq-answer">{tr_a}</p>'
        return match.group(0)

    content = re.sub(
        r'<summary\s+class="faq-question"[^>]*>(.*?)</summary>\s*<p\s+class="faq-answer"[^>]*>(.*?)</p>',
        replace_faq_html, content, flags=re.DOTALL
    )

    # Fix JSON-LD FAQ entries
    jsonld_fixes = [0]  # Use list for mutable closure

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
                    if is_english_text(name + ' ' + text) and name in TRANSLATIONS and lang in TRANSLATIONS.get(name, {}):
                        tr_q, tr_a = TRANSLATIONS[name][lang]
                        item['name'] = tr_q
                        item['acceptedAnswer']['text'] = tr_a
                        changed = True
                        jsonld_fixes[0] += 1
            if '@graph' in entity:
                for g in entity['@graph']:
                    process_entity(g)
            return entity

        process_entity(data)
        if changed:
            return json.dumps(data, ensure_ascii=False, indent=2)
        return json_str

    def replace_jsonld(match):
        return f'<script type="application/ld+json">{fix_jsonld(match.group(1))}</script>'

    content = re.sub(
        r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>',
        replace_jsonld, content, flags=re.DOTALL
    )

    if fixes > 0 or jsonld_fixes[0] > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return fixes + jsonld_fixes[0]


def main():
    with open(os.path.join(BASE, 'untranslated_faqs_report.json'), 'r', encoding='utf-8') as f:
        report = json.load(f)

    total_fixes = 0
    total_files = 0

    for lang, files in sorted(report['languages'].items()):
        lang_fixes = 0
        lang_files = 0
        for fi in files:
            fpath = os.path.join(BASE, fi['file'])
            if not os.path.isfile(fpath):
                continue
            n = fix_file(fpath, lang)
            if n > 0:
                lang_fixes += n
                lang_files += 1
                print(f"  Fixed {n} FAQs in {fi['file']}")
        total_fixes += lang_fixes
        total_files += lang_files
        print(f"  {lang.upper()}: {lang_files} files, {lang_fixes} FAQ entries fixed")

    print(f"\nTotal: {total_files} files, {total_fixes} FAQ entries fixed")


if __name__ == '__main__':
    main()
