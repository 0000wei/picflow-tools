import os

file_path = "d:/knowledge-base/06项目/哥飞建站/picete/ko/png-to-jpg/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    '<title>PNG to JPG - Free Online PNG to JPG Converter | PicEte</title>': '<title>PNG를 JPG로 변환 - 무료 온라인 PNG to JPG 변환기 | PicEte</title>',
    '<meta content="Free online PNG to JPG converter. Quickly convert PNG images to JPG format. Supports batch conversion, high-quality output, no registration required, local processing for privacy." name="description"/>': '<meta content="무료 온라인 PNG to JPG 변환기. PNG 이미지를 JPG 형식으로 빠르게 변환하세요. 일괄 변환, 고품질 출력 지원, 가입 불필요, 개인 정보 보호를 위한 로컬 처리를 제공합니다." name="description"/>',
    '<meta content="PNG to JPG, PNG to JPEG, online converter, batch conversion, free tool" name="keywords"/>': '<meta content="PNG를 JPG로, PNG JPEG 변환, 온라인 변환기, 일괄 변환, 무료 도구" name="keywords"/>',
    '<meta content="PNG to JPG - Free Online PNG to JPG Converter" property="og:title"/>': '<meta content="PNG를 JPG로 변환 - 무료 온라인 PNG to JPG 변환기" property="og:title"/>',
    '<meta content="Free online PNG to JPG converter, quickly convert PNG images to JPG format." property="og:description"/>': '<meta content="무료 온라인 PNG to JPG 변환기. PNG 이미지를 JPG 형식으로 빠르게 변환하세요." property="og:description"/>',
    '"name": "PNG to JPG Converter"': '"name": "PNG to JPG 변환기"',
    '"description": "Free online PNG to JPG conversion tool"': '"description": "무료 온라인 PNG to JPG 변환 도구"',
    '<p class="tagline">PNG to JPG Converter</p>': '<p class="tagline">PNG to JPG 변환기</p>',
    '"name": "Home"': '"name": "홈"',
    '"name": "PNG to JPG"': '"name": "PNG를 JPG로"',
    '<a class="nav-link" href="../">Home</a>': '<a class="nav-link" href="../">홈</a>',
    '<a class="nav-link" href="../#tools">More Tools</a>': '<a class="nav-link" href="../#tools">더 많은 도구</a>',
    '<div class="breadcrumb"><a href="https://picete.com/">Home</a><span class="separator">›</span><span class="current">PNG to JPG</span></div>': '<div class="breadcrumb"><a href="https://picete.com/">홈</a><span class="separator">›</span><span class="current">PNG to JPG</span></div>',
    '<h2 class="hero-title">PNG to JPG Online Converter</h2>': '<h2 class="hero-title">PNG to JPG 온라인 변환기</h2>',
    '<p class="hero-subtitle">Quickly convert PNG images to JPG format. Supports batch conversion with high-quality output.</p>': '<p class="hero-subtitle">PNG 이미지를 JPG 형식으로 빠르게 변환하세요. 고품질 출력과 일괄 변환을 지원합니다.</p>',
    '<p class="upload-text">Drop PNG images here</p>': '<p class="upload-text">여기에 PNG 이미지를 드롭하세요</p>',
    '<p class="upload-subtext">or click to select files, supports multiple selection</p>': '<p class="upload-subtext">또는 클릭하여 파일을 선택하세요 (다중 선택 지원)</p>',
    '<button class="btn-primary" id="selectBtn">Select PNG Images</button>': '<button class="btn-primary" id="selectBtn">PNG 이미지 선택</button>',
    '<h3>Selected PNG Images</h3>': '<h3>선택된 PNG 이미지</h3>',
    '<h4>Conversion Options</h4>': '<h4>변환 옵션</h4>',
    '<label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">JPG Quality</label>': '<label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">JPG 품질</label>',
    '<span>Smaller file</span>': '<span>파일 크기 작음</span>',
    '<span>Higher quality</span>': '<span>고품질</span>',
    '<button class="btn-primary" id="convertBtn">Convert to JPG</button>': '<button class="btn-primary" id="convertBtn">JPG로 변환</button>',
    '<button class="btn-secondary" id="resetBtn">Choose Again</button>': '<button class="btn-secondary" id="resetBtn">다시 선택</button>',
    '<h3>Conversion Complete!</h3>': '<h3>변환 완료!</h3>',
    '<button class="btn-primary" id="downloadAllBtn">Download All JPG</button>': '<button class="btn-primary" id="downloadAllBtn">모든 JPG 다운로드</button>',
    '<button class="btn-link" id="startOverBtn">Convert More Images</button>': '<button class="btn-link" id="startOverBtn">더 많은 이미지 변환</button>',
    '← Back to PicEte Home': '← PicEte 홈으로 돌아가기',
    '<h2 class="section-title">Why Use Our PNG to JPG Converter</h2>': '<h2 class="section-title">당사의 PNG to JPG 변환기를 사용해야 하는 이유</h2>',
    '<h3>Fast Conversion</h3>': '<h3>빠른 변환</h3>',
    '<p>Leveraging browser Canvas technology for millisecond-fast conversion without waiting for server processing.</p>': '<p>서버 처리를 기다릴 필요 없이 브라우저의 Canvas 기술을 활용하여 밀리초 단위의 빠른 변환을 제공합니다.</p>',
    '<h3>High Quality Output</h3>': '<h3>고품질 출력</h3>',
    '<p>Adjustable JPG quality parameters to find the perfect balance between file size and image quality.</p>': '<p>조절 가능한 JPG 품질 매개변수로 파일 크기와 이미지 품질 간의 완벽한 균형을 맞출 수 있습니다.</p>',
    '<h3>Batch Processing</h3>': '<h3>일괄 처리</h3>',
    '<p>Select multiple PNG images at once for batch conversion, dramatically improving your workflow.</p>': '<p>한 번에 여러 PNG 이미지를 선택하여 일괄 변환함으로써 작업 흐름을 획기적으로 향상시킬 수 있습니다.</p>',
    '<h3>Privacy Protection</h3>': '<h3>개인정보 보호</h3>',
    '<p>All conversion is done locally in your browser. Images are never uploaded to any server.</p>': '<p>모든 변환은 브라우저에서 로컬로 진행됩니다. 이미지는 어떤 서버에도 업로드되지 않습니다.</p>',
    '<h2 class="section-title">How to Convert PNG to JPG Online Free</h2>': '<h2 class="section-title">온라인에서 무료로 PNG를 JPG로 변환하는 방법</h2>',
    'Drop Your PNG Files': 'PNG 파일 드롭',
    'Click the upload area or drag PNG images into the browser. This PNG to JPG converter handles multiple files at once — batch convert an entire folder in one go. All PNG variants work, including transparent ones (they get flattened to white during conversion). Processing stays in your browser, so your files never leave your device.': '업로드 영역을 클릭하거나 PNG 이미지를 브라우저로 드래그하세요. 이 PNG to JPG 변환기는 한 번에 여러 파일을 처리합니다 — 한 폴더 전체를 일괄 변환할 수 있습니다. 투명한 이미지를 포함하여 모든 PNG 종류가 작동합니다 (변환 중에 투명한 부분은 흰색으로 병합됩니다). 처리는 브라우저에서 이루어지므로 파일이 기기 외부로 전송되지 않습니다.',
    'Pick Your Quality Level': '품질 수준 선택',
    'The quality slider controls JPG compression. For prints and professional portfolios, set it to 90-95% — most visual detail stays while file size drops compared to the original PNG. For web and social media, 80-85% looks great with significantly smaller files. For thumbnails where every byte counts, 70-75% works. The slider updates in real time, so you can dial in exactly what you need.': '품질 슬라이더로 JPG 압축률을 조정합니다. 인쇄물이나 전문 포트폴리오의 경우 90-95%로 설정하세요 — 원본 PNG와 비교하여 파일 크기는 줄어들면서 시각적 디테일의 대부분이 유지됩니다. 웹과 소셜 미디어의 경우 80-85%를 설정하면 파일 크기가 훨씬 줄어들고 멋진 화질을 유지할 수 있습니다. 용량을 최대한 줄여야 하는 썸네일에는 70-75%가 적합합니다. 슬라이더가 실시간으로 업데이트되므로 원하는 값을 정확하게 맞출 수 있습니다.',
    'Download Your JPGs': 'JPG 파일 다운로드',
    'Each converted JPG shows a preview with the new file size next to the original PNG size. Download individually or hit the batch button to grab everything at once. The JPGs are ready for website uploads, email attachments, or social media. The whole process takes seconds, even with multiple high-res images.': '변환된 각 JPG는 원본 PNG 크기 옆에 새로운 파일 크기와 함께 미리보기를 표시합니다. 개별적으로 다운로드하거나 일괄 처리 버튼을 눌러 한 번에 모두 받을 수 있습니다. JPG는 웹사이트 업로드, 이메일 첨부 또는 소셜 미디어에서 즉시 사용할 수 있습니다. 여러 개의 고해상도 이미지라도 전체 과정은 몇 초밖에 걸리지 않습니다.',
    '<h2 class="section-title">PNG to JPG Tips</h2>': '<h2 class="section-title">PNG to JPG 팁</h2>',
    'Why Size Matters: PNG vs JPG': '크기가 중요한 이유: PNG 대 JPG',
    'The main reason to switch from PNG to JPG is file size. PNG\'s lossless compression keeps every pixel, but that makes files 5 to 10 times larger than JPG equivalents. For websites, oversized PNGs directly hurt load speed and bandwidth costs. Converting to JPG can cut file sizes by 80% or more while looking the same for photos and complex images. Faster pages, lower hosting costs, better user experience — especially on mobile where data is precious.': 'PNG에서 JPG로 변경하는 주된 이유는 파일 크기입니다. PNG의 무손실 압축은 모든 픽셀을 보존하지만, 파일이 동일한 JPG보다 5배에서 10배 더 큽니다. 웹사이트의 경우 과도하게 큰 PNG는 로드 속도와 대역폭 비용에 직접적인 악영향을 미칩니다. JPG로 변환하면 사진이나 복잡한 이미지에서 겉보기에 차이가 없으면서 파일 크기를 80% 이상 줄일 수 있습니다. 더 빠른 페이지 로딩, 호스팅 비용 절감, 더 나은 사용자 경험을 제공하며 특히 데이터가 제한된 모바일 환경에서 유용합니다.',
    'Nailing the Quality Setting': '적절한 품질 설정 찾기',
    'The right JPG quality setting makes or breaks the result. For photos and gradient-rich images, 85-90% is often indistinguishable from the original PNG while being much smaller. For screenshots and text-heavy images, bump it to 92-95% to keep crisp edges and avoid artifacts around letters. Always preview at 100% zoom. And remember: JPG does not support transparency — any transparent areas get filled with white, so plan ahead.': '올바른 JPG 품질 설정은 결과물의 성패를 좌우합니다. 사진이나 그라디언트가 풍부한 이미지의 경우, 85-90%로 설정하면 원본 PNG와 시각적 차이가 없으면서도 파일 크기는 훨씬 작아집니다. 스크린샷이나 텍스트가 많은 이미지의 경우, 92-95%로 높여 윤곽선을 선명하게 유지하고 글자 주변의 아티팩트를 방지하세요. 항상 100% 확대율로 미리보기를 확인하세요. 기억해야 할 점: JPG는 투명도를 지원하지 않습니다. 투명한 부분은 흰색으로 채워지므로 미리 고려하세요.',
    'When to Convert PNG to JPG': 'PNG를 JPG로 변환해야 할 때',
    'Go JPG when file size matters and you do not need transparency. Common cases: uploading photos to a website where speed counts, sending images in email with attachment limits, creating social media posts, or storing large photo libraries. Platforms that recompress images anyway will do less damage starting from a smaller JPG. But keep originals as PNG for logos, text-heavy graphics, screenshots, and anything you might edit later — JPG\'s lossy compression gets worse with every re-save.': '파일 크기가 중요하고 투명도가 필요하지 않을 때 JPG를 사용하세요. 일반적인 사례: 로딩 속도가 중요한 웹사이트에 사진 업로드, 첨부 용량 제한이 있는 이메일 전송, 소셜 미디어 게시물 작성, 대용량 사진 라이브러리 저장 등. 이미지를 재압축하는 플랫폼의 경우에도 더 작은 용량의 JPG에서 시작하면 화질 손실이 적습니다. 단, 로고, 텍스트 위주 그래픽, 스크린샷 및 나중에 다시 편집할 이미지는 원본을 PNG로 보관하세요 — JPG의 손실 압축은 다시 저장할 때마다 화질이 저하됩니다.',
    '<h2 class="section-title">Frequently Asked Questions</h2>': '<h2 class="section-title">자주 묻는 질문</h2>',
    '"name": "Does PNG to JPG conversion affect image quality?"': '"name": "PNG를 JPG로 변환하면 화질에 영향을 주나요?"',
    '"text": "Yes, JPG uses lossy compression, so there is some quality loss. Our tool lets you adjust the quality from 10% to 100%. For most web uses, 80-90% quality produces visually identical results to the original PNG while cutting file size by 80% or more. Set it higher for prints and archival where every pixel matters."': '"text": "네, JPG는 손실 압축을 사용하므로 화질 저하가 발생합니다. 저희 도구는 품질을 10%에서 100%까지 조정할 수 있습니다. 대부분의 웹 용도의 경우 80-90% 품질 설정 시 원본 PNG와 시각적으로 동일한 결과를 얻으면서 파일 크기를 80% 이상 줄일 수 있습니다. 모든 픽셀이 중요한 인쇄 및 보관용으로는 품질을 더 높게 설정하세요."',
    '"name": "Will I lose transparency converting PNG to JPG?"': '"name": "PNG를 JPG로 변환하면 투명도가 사라지나요?"',
    '"text": "Yes. JPG does not support transparency. Any transparent areas in your PNG will be filled with white. If you need to preserve transparency, consider keeping the original PNG or using a format like WebP that supports both transparency and good compression."': '"text": "네. JPG는 투명도를 지원하지 않습니다. PNG의 모든 투명한 부분은 흰색으로 채워집니다. 투명도를 유지해야 하는 경우, 원본 PNG를 보관하거나 투명도와 우수한 압축을 모두 지원하는 WebP 같은 형식을 사용하는 것을 고려해 보세요."',
    '"name": "How fast is the PNG to JPG conversion?"': '"name": "PNG에서 JPG로의 변환은 얼마나 빠른가요?"',
    '"text": "The conversion is instant and happens entirely in your browser using Canvas technology. Even large files or batch conversions complete in milliseconds. The speed depends on your device\'s processing power, but there is no server upload or waiting."': '"text": "변환은 Canvas 기술을 사용하여 완전히 브라우저 내에서 즉각적으로 이루어집니다. 큰 파일이나 일괄 변환도 밀리초 안에 완료됩니다. 속도는 기기의 처리 성능에 따라 다르지만 서버 업로드나 대기 시간이 없습니다."',
    '"name": "How many PNG files can I convert at once?"': '"name": "한 번에 몇 개의 PNG 파일을 변환할 수 있나요?"',
    '"text": "There is no limit on the number of files. Select a whole folder of PNGs and convert them all at once. Each image is processed independently, and you can download them individually or click \'Download All\' to get everything in one go."': '"text": "파일 개수에 제한이 없습니다. PNG 폴더 전체를 선택하고 한 번에 모두 변환할 수 있습니다. 각 이미지는 독립적으로 처리되며 개별적으로 다운로드하거나 \'모두 다운로드\'를 클릭하여 한꺼번에 받을 수 있습니다."',
    '<summary class="faq-question">Does PNG to JPG conversion affect image quality?</summary>': '<summary class="faq-question">PNG를 JPG로 변환하면 화질에 영향을 주나요?</summary>',
    '<p class="faq-answer">Yes, JPG uses lossy compression, so there is some quality loss. Our tool lets you adjust the quality from 10% to 100%. For most web uses, 80-90% quality produces visually identical results to the original PNG while cutting file size by 80% or more. Set it higher for prints and archival where every pixel matters.</p>': '<p class="faq-answer">네, JPG는 손실 압축을 사용하므로 화질 저하가 발생합니다. 저희 도구는 품질을 10%에서 100%까지 조정할 수 있습니다. 대부분의 웹 용도의 경우 80-90% 품질 설정 시 원본 PNG와 시각적으로 동일한 결과를 얻으면서 파일 크기를 80% 이상 줄일 수 있습니다. 모든 픽셀이 중요한 인쇄 및 보관용으로는 품질을 더 높게 설정하세요.</p>',
    '<summary class="faq-question">Will I lose transparency converting PNG to JPG?</summary>': '<summary class="faq-question">PNG를 JPG로 변환하면 투명도가 사라지나요?</summary>',
    '<p class="faq-answer">Yes. JPG does not support transparency. Any transparent areas in your PNG will be filled with white. If you need to preserve transparency, consider keeping the original PNG or using a format like WebP that supports both transparency and good compression.</p>': '<p class="faq-answer">네. JPG는 투명도를 지원하지 않습니다. PNG의 모든 투명한 부분은 흰색으로 채워집니다. 투명도를 유지해야 하는 경우, 원본 PNG를 보관하거나 투명도와 우수한 압축을 모두 지원하는 WebP 같은 형식을 사용하는 것을 고려해 보세요.</p>',
    '<summary class="faq-question">How fast is the PNG to JPG conversion?</summary>': '<summary class="faq-question">PNG에서 JPG로의 변환은 얼마나 빠른가요?</summary>',
    '<p class="faq-answer">The conversion is instant and happens entirely in your browser using Canvas technology. Even large files or batch conversions complete in milliseconds. The speed depends on your device\'s processing power, but there is no server upload or waiting.</p>': '<p class="faq-answer">변환은 Canvas 기술을 사용하여 완전히 브라우저 내에서 즉각적으로 이루어집니다. 큰 파일이나 일괄 변환도 밀리초 안에 완료됩니다. 속도는 기기의 처리 성능에 따라 다르지만 서버 업로드나 대기 시간이 없습니다.</p>',
    '<summary class="faq-question">How many PNG files can I convert at once?</summary>': '<summary class="faq-question">한 번에 몇 개의 PNG 파일을 변환할 수 있나요?</summary>',
    '<p class="faq-answer">There is no limit on the number of files. Select a whole folder of PNGs and convert them all at once. Each image is processed independently, and you can download them individually or click \'Download All\' to get everything in one go.</p>': '<p class="faq-answer">파일 개수에 제한이 없습니다. PNG 폴더 전체를 선택하고 한 번에 모두 변환할 수 있습니다. 각 이미지는 독립적으로 처리되며 개별적으로 다운로드하거나 \'모두 다운로드\'를 클릭하여 한꺼번에 받을 수 있습니다.</p>',
    "alert('Please select PNG images')": "alert('PNG 이미지를 선택해주세요')",
    "alert('Failed to load images')": "alert('이미지 로드에 실패했습니다')",
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
print("Done png-to-jpg")
