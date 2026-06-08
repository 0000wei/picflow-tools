import os

file_path = "d:/knowledge-base/06项目/哥飞建站/picete/ko/raw-to-jpg/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    '<title>RAW to JPG - Free Online RAW to JPG Converter | PicEte</title>': '<title>RAW를 JPG로 변환 - 무료 온라인 RAW to JPG 변환기 | PicEte</title>',
    '<meta content="Free online RAW to JPG converter. Convert camera RAW files (CR2, NEF, ARW, DNG) to high-quality JPG images in your browser. No upload, no signup, private and free." name="description"/>': '<meta content="무료 온라인 RAW to JPG 변환기. 브라우저에서 카메라 RAW 파일(CR2, NEF, ARW, DNG)을 고품질 JPG 이미지로 변환하세요. 업로드나 가입이 필요 없으며, 안전하고 무료입니다." name="description"/>',
    '<meta content="RAW to JPG, RAW to JPG converter, CR2 to JPG, NEF to JPG, ARW to JPG, DNG to JPG, RAW image converter, online RAW converter, camera RAW converter" name="keywords"/>': '<meta content="RAW를 JPG로, RAW JPG 변환기, CR2 JPG 변환, NEF JPG 변환, ARW JPG 변환, DNG JPG 변환, RAW 이미지 변환기, 온라인 RAW 변환, 카메라 RAW 변환기" name="keywords"/>',
    '<meta content="RAW to JPG - Free Online RAW to JPG Converter" property="og:title"/>': '<meta content="RAW를 JPG로 변환 - 무료 온라인 RAW to JPG 변환기" property="og:title"/>',
    '<meta content="Free online RAW to JPG converter, convert camera RAW files (CR2, NEF, ARW, DNG) to high-quality JPG images in your browser." property="og:description"/>': '<meta content="무료 온라인 RAW to JPG 변환기. 브라우저에서 카메라 RAW 파일(CR2, NEF, ARW, DNG)을 고품질 JPG 이미지로 변환하세요." property="og:description"/>',
    '"name": "RAW to JPG Converter"': '"name": "RAW to JPG 변환기"',
    '"description": "Free online RAW to JPG conversion tool"': '"description": "무료 온라인 RAW to JPG 변환 도구"',
    '<p class="tagline">RAW to JPG Converter</p>': '<p class="tagline">RAW to JPG 변환기</p>',
    '"name": "Home"': '"name": "홈"',
    '"name": "RAW to JPG"': '"name": "RAW를 JPG로"',
    '<a class="nav-link" href="../">Home</a>': '<a class="nav-link" href="../">홈</a>',
    '<a class="nav-link" href="../#tools">More Tools</a>': '<a class="nav-link" href="../#tools">더 많은 도구</a>',
    '<div class="breadcrumb"><a href="https://picete.com/">Home</a><span class="separator">›</span><span class="current">RAW to JPG</span></div>': '<div class="breadcrumb"><a href="https://picete.com/">홈</a><span class="separator">›</span><span class="current">RAW to JPG</span></div>',
    '<h2 class="hero-title">RAW to JPG Online Converter</h2>': '<h2 class="hero-title">RAW to JPG 온라인 변환기</h2>',
    '<p class="hero-subtitle">Convert camera RAW files (CR2, CR3, NEF, ARW, DNG) to high-quality JPG images. Uses wasm-vips for accurate RAW decoding, supports batch conversion, and everything stays local.</p>': '<p class="hero-subtitle">카메라 RAW 파일(CR2, CR3, NEF, ARW, DNG)을 고품질 JPG 이미지로 변환하세요. wasm-vips를 사용하여 정확하게 RAW를 디코딩하고 일괄 변환을 지원하며 모든 작업이 로컬에서 안전하게 처리됩니다.</p>',
    '<p class="upload-text">Drop RAW files here</p>': '<p class="upload-text">여기에 RAW 파일을 드롭하세요</p>',
    '<p class="upload-subtext">or click to select files, supports multiple selection</p>': '<p class="upload-subtext">또는 클릭하여 파일을 선택하세요 (다중 선택 지원)</p>',
    '<button class="btn-primary" id="selectBtn">Select RAW Files</button>': '<button class="btn-primary" id="selectBtn">RAW 파일 선택</button>',
    '<h3>Selected RAW Files</h3>': '<h3>선택된 RAW 파일</h3>',
    '<label for="qualitySlider" style="display: inline-block; margin-right: 1rem; font-weight: 500;">JPEG Quality: <span id="qualityValue">85</span></label>': '<label for="qualitySlider" style="display: inline-block; margin-right: 1rem; font-weight: 500;">JPEG 품질: <span id="qualityValue">85</span></label>',
    '<button class="btn-primary" id="convertBtn">Convert to JPG</button>': '<button class="btn-primary" id="convertBtn">JPG로 변환</button>',
    '<button class="btn-secondary" id="resetBtn">Choose Again</button>': '<button class="btn-secondary" id="resetBtn">다시 선택</button>',
    '<h3>Conversion Complete!</h3>': '<h3>변환 완료!</h3>',
    '<button class="btn-primary" id="downloadAllBtn">Download All JPG</button>': '<button class="btn-primary" id="downloadAllBtn">모든 JPG 다운로드</button>',
    '<button class="btn-link" id="startOverBtn">Convert More Files</button>': '<button class="btn-link" id="startOverBtn">더 많은 파일 변환</button>',
    '← Back to PicEte Home': '← PicEte 홈으로 돌아가기',
    '<h2 class="section-title">Why Use Our RAW to JPG Converter</h2>': '<h2 class="section-title">당사의 RAW to JPG 변환기를 사용해야 하는 이유</h2>',
    '<h3>WASM-Powered RAW Decoding</h3>': '<h3>WASM 기반 RAW 디코딩</h3>',
    '<p>Uses wasm-vips, a WebAssembly port of the Vips library with libraw, to decode RAW files accurately in your browser. Supports Canon CR2/CR3, Nikon NEF, Sony ARW, Adobe DNG, and more. No server uploads needed.</p>': '<p>libraw가 포함된 Vips 라이브러리의 WebAssembly 포트인 wasm-vips를 사용하여 브라우저에서 RAW 파일을 정확하게 디코딩합니다. Canon CR2/CR3, Nikon NEF, Sony ARW, Adobe DNG 등을 지원합니다. 서버 업로드가 필요하지 않습니다.</p>',
    '<h3>High-Quality JPEG Output</h3>': '<h3>고품질 JPEG 출력</h3>',
    '<p>Adjustable JPEG quality from 10 to 100. The default 85 offers excellent balance between file size and visual quality. Full resolution output with proper color space handling.</p>': '<p>10에서 100까지 조정 가능한 JPEG 품질을 제공합니다. 기본값인 85는 파일 크기와 시각적 품질 간에 뛰어난 균형을 제공합니다. 올바른 색상 공간 처리와 함께 전체 해상도 출력을 지원합니다.</p>',
    '<h3>Batch Processing</h3>': '<h3>일괄 처리</h3>',
    '<p>Select multiple RAW files at once for batch conversion. Each image is processed independently with consistent quality settings, and you can download them all at once with one click.</p>': '<p>일괄 변환을 위해 한 번에 여러 RAW 파일을 선택할 수 있습니다. 각 이미지는 일관된 품질 설정으로 독립적으로 처리되며, 클릭 한 번으로 모든 이미지를 동시에 다운로드할 수 있습니다.</p>',
    '<h3>Privacy &amp; Local Processing</h3>': '<h3>개인정보 보호 및 로컬 처리</h3>',
    '<p>All conversion happens locally in your browser using WebAssembly. RAW files are never uploaded to any server. Your photos remain on your device at all times.</p>': '<p>모든 변환은 WebAssembly를 사용하여 브라우저에서 로컬로 진행됩니다. RAW 파일은 어떠한 서버로도 업로드되지 않습니다. 사진은 항상 기기에 안전하게 보관됩니다.</p>',
    '<h2 class="section-title">How to Convert RAW to JPG Online Free</h2>': '<h2 class="section-title">온라인에서 무료로 RAW를 JPG로 변환하는 방법</h2>',
    'Upload Your RAW Files': 'RAW 파일 업로드',
    'Click the upload area or drag RAW files into the browser. The tool accepts .cr2, .cr3, .nef, .arw, .dng, and many other RAW formats. Select multiple files at once for batch conversion. When you drop your files, you will see thumbnails showing a preview of each RAW image with its file name and dimensions. All processing stays in your browser — your photos never leave your device.': '업로드 영역을 클릭하거나 RAW 파일을 브라우저로 드래그하세요. 이 도구는 .cr2, .cr3, .nef, .arw, .dng 및 다양한 RAW 형식을 지원합니다. 일괄 처리를 위해 한 번에 여러 파일을 선택할 수 있습니다. 파일을 드롭하면 각 RAW 이미지의 미리보기 썸네일과 파일명, 크기가 표시됩니다. 모든 처리는 브라우저 내에서 이루어지며 사진이 기기 외부로 유출되지 않습니다.',
    'Adjust Quality and Convert': '품질 조절 및 변환',
    'Use the quality slider to set JPEG compression (10-100, default 85). Higher values mean better quality but larger files. Click the "Convert to JPG" button to start. The tool loads the WebAssembly-based vips library with libraw support (usually takes a moment on first use) and decodes each RAW file into full-resolution pixel data, then encodes to JPEG. Progress indicators show when each file has finished converting.': '품질 슬라이더를 사용하여 JPEG 압축률을 설정하세요(10-100, 기본값 85). 값이 높을수록 품질은 좋아지지만 파일 크기는 커집니다. "JPG로 변환" 버튼을 클릭하여 시작하세요. 이 도구는 libraw를 지원하는 WebAssembly 기반 vips 라이브러리를 로드하고(첫 사용 시 약간의 시간 소요), 각 RAW 파일을 전체 해상도의 픽셀 데이터로 디코딩한 다음 JPEG로 인코딩합니다. 진행률 표시기를 통해 각 파일의 변환 완료 상태를 확인할 수 있습니다.',
    'Download Your JPGs': 'JPG 파일 다운로드',
    'Each converted JPG displays a preview with its file size. Download images individually with the per-file button, or click "Download All JPG" to trigger staggered downloads for every converted file — browsers handle them one by one automatically. If you want to convert more, click "Convert More Files" to start a new batch. The whole workflow is fast, local, and private.': '변환된 각 JPG는 파일 크기와 함께 미리보기를 표시합니다. 각 파일별 버튼을 눌러 개별적으로 다운로드하거나, "모든 JPG 다운로드"를 클릭하여 변환된 모든 파일을 순차적으로 다운로드할 수 있습니다(브라우저가 자동으로 하나씩 처리함). 더 많은 파일을 변환하려면 "더 많은 파일 변환"을 클릭하여 새로운 작업을 시작하세요. 이 모든 작업 과정은 빠르고, 로컬 환경에서 안전하게 처리됩니다.',
    '<h2 class="section-title">RAW to JPG Tips</h2>': '<h2 class="section-title">RAW to JPG 팁</h2>',
    'Why Convert RAW to JPG?': 'RAW를 JPG로 변환해야 하는 이유',
    'RAW files contain unprocessed sensor data with maximum editing flexibility, but they are large and not widely supported by web platforms or mobile devices. Converting to JPG creates universally compatible images that work everywhere — email attachments, social media uploads, web hosting, and document embedding. JPG is also much smaller than RAW, making it practical for sharing and storage.': 'RAW 파일은 가공되지 않은 센서 데이터를 포함하여 최대의 편집 유연성을 제공하지만, 용량이 크고 웹 플랫폼이나 모바일 기기에서 널리 지원되지 않습니다. JPG로 변환하면 이메일 첨부, 소셜 미디어 업로드, 웹 호스팅, 문서 삽입 등 어디서나 사용할 수 있는 보편적으로 호환되는 이미지가 생성됩니다. JPG는 RAW보다 훨씬 작기 때문에 공유 및 저장에도 실용적입니다.',
    'Supported RAW Formats': '지원되는 RAW 형식',
    'We officially support Canon CR2 and CR3, Nikon NEF, Sony ARW, and Adobe DNG. Many other camera RAW formats (Fujifilm RAF, Panasonic RW2, Olympus ORF, Pentax PEF, etc.) are supported experimentally through libraw but may not be fully tested. If your format isn\'t listed, try uploading — it may still work. For best results, use DNG if your camera supports it.': '당사는 Canon CR2 및 CR3, Nikon NEF, Sony ARW, Adobe DNG를 공식적으로 지원합니다. Fujifilm RAF, Panasonic RW2, Olympus ORF, Pentax PEF 등 다양한 기타 카메라 RAW 형식도 libraw를 통해 실험적으로 지원되지만 완벽하게 테스트되지 않았을 수 있습니다. 목록에 없는 형식이라도 업로드해 보세요 — 작동할 수 있습니다. 최상의 결과를 얻으려면 카메라가 지원하는 경우 DNG를 사용하세요.',
    'Quality Settings Explained': '품질 설정 설명',
    'The JPEG quality slider controls compression: 10 is smallest file size with visible artifacts, 100 is largest with minimal compression. 85 is the recommended default — excellent quality for most purposes. Use 90-100 for archival or print, 70-85 for web sharing, and lower values only when file size matters more than quality. Remember that RAW originals are always superior for editing — convert to JPG as the final step for distribution.': 'JPEG 품질 슬라이더는 압축을 제어합니다. 10은 눈에 띄는 아티팩트가 있는 가장 작은 파일 크기이고, 100은 최소한의 압축이 적용된 가장 큰 파일입니다. 85는 권장 기본값으로 대부분의 목적에 훌륭한 품질을 제공합니다. 보관 또는 인쇄용으로는 90-100을, 웹 공유용으로는 70-85를 사용하고, 품질보다 파일 크기가 중요한 경우에만 더 낮은 값을 사용하세요. 편집에는 항상 RAW 원본이 우수하다는 점을 기억하세요 — 배포를 위한 최종 단계로 JPG로 변환하십시오.',
    '<h2 class="section-title">Frequently Asked Questions</h2>': '<h2 class="section-title">자주 묻는 질문</h2>',
    '"name": "What RAW formats are supported?"': '"name": "어떤 RAW 형식이 지원되나요?"',
    '"text": "We support Canon CR2/CR3, Nikon NEF, Sony ARW, and Adobe DNG files. Many other RAW formats (RAF, RW2, ORF, PEF, etc.) are supported experimentally via libraw but not officially tested."': '"text": "당사는 Canon CR2/CR3, Nikon NEF, Sony ARW 및 Adobe DNG 파일을 지원합니다. 다른 많은 RAW 형식(RAF, RW2, ORF, PEF 등)은 libraw를 통해 실험적으로 지원되지만 공식적으로 테스트되지는 않았습니다."',
    '"name": "Is the conversion quality adjustable?"': '"name": "변환 품질을 조절할 수 있나요?"',
    '"text": "Yes. You can adjust the JPEG quality from 10 to 100 using the slider. The default is 85, which offers a good balance of file size and visual quality."': '"text": "네. 슬라이더를 사용하여 JPEG 품질을 10에서 100 사이로 조절할 수 있습니다. 기본값은 85이며 파일 크기와 시각적 품질 간에 좋은 균형을 제공합니다."',
    '<summary class="faq-question">What RAW formats are supported?</summary>': '<summary class="faq-question">어떤 RAW 형식이 지원되나요?</summary>',
    '<p class="faq-answer">We support Canon CR2/CR3, Nikon NEF, Sony ARW, and Adobe DNG files. Many other RAW formats (RAF, RW2, ORF, PEF, etc.) are supported experimentally via libraw but not officially tested.</p>': '<p class="faq-answer">당사는 Canon CR2/CR3, Nikon NEF, Sony ARW 및 Adobe DNG 파일을 지원합니다. 다른 많은 RAW 형식(RAF, RW2, ORF, PEF 등)은 libraw를 통해 실험적으로 지원되지만 공식적으로 테스트되지는 않았습니다.</p>',
    '<summary class="faq-question">Is the conversion quality adjustable?</summary>': '<summary class="faq-question">변환 품질을 조절할 수 있나요?</summary>',
    '<p class="faq-answer">Yes. You can adjust the JPEG quality from 10 to 100 using the slider. The default is 85, which offers a good balance of file size and visual quality.</p>': '<p class="faq-answer">네. 슬라이더를 사용하여 JPEG 품질을 10에서 100 사이로 조절할 수 있습니다. 기본값은 85이며 파일 크기와 시각적 품질 간에 좋은 균형을 제공합니다.</p>',
    "alert('Please select RAW files')": "alert('RAW 파일을 선택해주세요')",
    "alert('Failed to load files')": "alert('파일 로드에 실패했습니다')",
    "No preview available": "미리보기 없음",
    "(RAW format)": "(RAW 형식)",
    "Converting...": "변환 중...",
    "alert('Failed to convert: ' + state.uploadedFiles[i].name + '\\n' + err.message);": "alert('변환 실패: ' + state.uploadedFiles[i].name + '\\n' + err.message);",
    "convertBtn.textContent = 'Convert to JPG';": "convertBtn.textContent = 'JPG로 변환';",
    "Failed to load wasm-vips library. This may be due to COOP/COEP restrictions. Please try using a modern browser with SharedArrayBuffer support, or check your browser settings.": "wasm-vips 라이브러리를 로드하지 못했습니다. COOP/COEP 제한 때문일 수 있습니다. SharedArrayBuffer를 지원하는 최신 브라우저를 사용하거나 브라우저 설정을 확인하세요.",
    "Failed to decode RAW file. The format may not be supported.": "RAW 파일 디코딩에 실패했습니다. 지원되지 않는 형식일 수 있습니다.",
    '<button class="btn-primary" onclick="downloadOne(${i})">Download</button>': '<button class="btn-primary" onclick="downloadOne(${i})">다운로드</button>',
    '<li><a href="../resize-image/">Image Resizer</a></li>': '<li><a href="../resize-image/">이미지 크기 조정</a></li>',
    '<li><a href="../compress-image/">Image Compressor</a></li>': '<li><a href="../compress-image/">이미지 압축기</a></li>',
    '<li><a href="../">Back to Home</a></li>': '<li><a href="../">홈으로 돌아가기</a></li>',
    '<li><a href="/privacy-policy.html">Privacy Policy</a></li>': '<li><a href="/privacy-policy.html">개인정보 처리방침</a></li>',
    '<li><a href="https://mockupshot.online/">MockupShot - Screenshot Mockup</a></li>': '<li><a href="https://mockupshot.online/">MockupShot - 스크린샷 목업</a></li>',
    '<li><a href="https://ilovepalette.com/">ILovePalette - Color Tools</a></li>': '<li><a href="https://ilovepalette.com/">ILovePalette - 색상 도구</a></li>'
}

for k, v in replacements.items():
    content = content.replace(k, v)

content = content.replace('<h4>More Tools</h4>', '<h4>더 많은 도구</h4>', 1)
content = content.replace('<h4>More Tools</h4>', '<h4>파트너 사이트</h4>', 1)
content = content.replace('<h4>About</h4>', '<h4>소개</h4>', 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done raw-to-jpg")
