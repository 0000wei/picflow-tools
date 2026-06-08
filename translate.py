import os

file_path = "d:/knowledge-base/06项目/哥飞建站/picete/ko/png-to-webp/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    "<title>PNG to WebP - Free Online PNG to WebP Converter | PicEte</title>": "<title>PNG를 WebP로 변환 - 무료 온라인 PNG to WebP 변환기 | PicEte</title>",
    '<meta content="Free online PNG to WebP converter. Quickly convert PNG images to WebP format. Significantly reduce file size while maintaining quality. No registration required, local processing for privacy." name="description"/>': '<meta content="무료 온라인 PNG to WebP 변환기. PNG 이미지를 WebP 형식으로 빠르게 변환하세요. 품질은 유지하면서 파일 크기를 크게 줄입니다. 가입이 필요 없으며 개인정보 보호를 위해 로컬에서 처리됩니다." name="description"/>',
    '<meta content="PNG to WebP, online converter, batch conversion, image compression, free tool" name="keywords"/>': '<meta content="PNG를 WebP로, 온라인 변환기, 일괄 변환, 이미지 압축, 무료 도구" name="keywords"/>',
    '<meta content="PNG to WebP - Free Online PNG to WebP Converter" property="og:title"/>': '<meta content="PNG를 WebP로 변환 - 무료 온라인 PNG to WebP 변환기" property="og:title"/>',
    '<meta content="Free online PNG to WebP converter, significantly reduce file size while maintaining high quality." property="og:description"/>': '<meta content="무료 온라인 PNG to WebP 변환기. 고품질을 유지하면서 파일 크기를 크게 줄이세요." property="og:description"/>',
    '"name": "PNG to WebP Converter"': '"name": "PNG to WebP 변환기"',
    '"description": "Free online PNG to WebP conversion tool"': '"description": "무료 온라인 PNG to WebP 변환 도구"',
    '"name": "Home"': '"name": "홈"',
    '"name": "PNG to WebP"': '"name": "PNG를 WebP로"',
    '"name": "How much smaller is WebP compared to PNG?"': '"name": "WebP는 PNG와 비교하여 얼마나 더 작은가요?"',
    '"text": "WebP typically reduces file size by 25-35% compared to PNG while maintaining the same visual quality. For photos with lossy WebP compression, savings reach 80-90%. For lossless WebP (preserving transparency), you still get roughly 30% smaller files. WebP is designed specifically for web performance."': '"text": "WebP는 동일한 시각적 품질을 유지하면서 PNG에 비해 파일 크기를 일반적으로 25-35% 줄입니다. 손실 WebP 압축을 사용하는 사진의 경우 최대 80-90%까지 줄일 수 있습니다. 무손실 WebP(투명도 유지)의 경우에도 약 30% 더 작은 파일을 얻을 수 있습니다. WebP는 특히 웹 성능을 위해 설계되었습니다."',
    '"name": "Does WebP support transparency like PNG?"': '"name": "WebP도 PNG처럼 투명도를 지원하나요?"',
    '"text": "Yes, WebP fully supports alpha transparency channels. You can convert transparent PNGs to WebP and the transparency is preserved perfectly. This makes WebP an ideal replacement for PNG on the web \\u2014 same visual quality with transparency, but significantly smaller file sizes."': '"text": "네, WebP는 알파 투명도 채널을 완벽하게 지원합니다. 투명한 PNG를 WebP로 변환해도 투명도가 완벽하게 유지됩니다. 이로 인해 WebP는 웹에서 PNG의 이상적인 대체품이 됩니다. 투명도를 포함한 동일한 시각적 품질에 파일 크기는 훨씬 작습니다."',
    '"name": "Is WebP supported in all browsers?"': '"name": "WebP는 모든 브라우저에서 지원되나요?"',
    '"text": "WebP is supported by all modern browsers including Chrome (since 2010), Firefox (since 2018), Safari (since 2020), and Edge (since 2018). Over 97% of web users can view WebP images. For edge cases, you can use a fallback strategy with the <picture> element."': '"text": "WebP는 Chrome(2010년 이후), Firefox(2018년 이후), Safari(2020년 이후), Edge(2018년 이후)를 포함한 모든 최신 브라우저에서 지원됩니다. 97% 이상의 웹 사용자가 WebP 이미지를 볼 수 있습니다. 예외적인 경우에는 <picture> 요소를 사용한 대체 전략을 사용할 수 있습니다."',
    '"name": "Should I convert all my PNGs to WebP?"': '"name": "모든 PNG를 WebP로 변환해야 하나요?"',
    '"text": "For web use, yes \\u2014 replacing PNG with WebP improves page load speed without quality loss, especially beneficial for mobile users on slow connections. For images you need to edit or share outside the web, keep the original PNG. WebP is still not universally supported in offline tools like Photoshop without plugins."': '"text": "웹용이라면 네 그렇습니다. PNG를 WebP로 대체하면 품질 저하 없이 페이지 로딩 속도가 향상되며, 느린 연결을 사용하는 모바일 사용자에게 특히 유용합니다. 웹 외부에서 편집하거나 공유해야 하는 이미지의 경우 원본 PNG를 유지하세요. WebP는 아직 플러그인 없이 Photoshop과 같은 오프라인 도구에서 보편적으로 지원되지는 않습니다."',
    '<p class="tagline">PNG to WebP Converter</p>': '<p class="tagline">PNG to WebP 변환기</p>',
    '<a class="nav-link" href="../">Home</a>': '<a class="nav-link" href="../">홈</a>',
    '<a class="nav-link" href="../#tools">More Tools</a>': '<a class="nav-link" href="../#tools">더 많은 도구</a>',
    '<div class="breadcrumb"><a href="https://picete.com/">Home</a><span class="separator">›</span><span class="current">PNG to WebP</span></div>': '<div class="breadcrumb"><a href="https://picete.com/">홈</a><span class="separator">›</span><span class="current">PNG to WebP</span></div>',
    '<h2 class="hero-title">PNG to WebP Online Converter</h2>': '<h2 class="hero-title">PNG to WebP 온라인 변환기</h2>',
    '<p class="hero-subtitle">Convert PNG images to WebP format, reducing file size by an average of 30-50%.</p>': '<p class="hero-subtitle">PNG 이미지를 WebP 형식으로 변환하여 파일 크기를 평균 30-50% 줄이세요.</p>',
    '<p class="upload-text">Drop PNG images here</p>': '<p class="upload-text">여기에 PNG 이미지를 드롭하세요</p>',
    '<p class="upload-subtext">or click to select files, supports multiple selection</p>': '<p class="upload-subtext">또는 클릭하여 파일을 선택하세요 (다중 선택 지원)</p>',
    '<button class="btn-primary" id="selectBtn">Select PNG Images</button>': '<button class="btn-primary" id="selectBtn">PNG 이미지 선택</button>',
    '<h3>Selected PNG Images</h3>': '<h3>선택된 PNG 이미지</h3>',
    '<h4>Conversion Options</h4>': '<h4>변환 옵션</h4>',
    '<label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">WebP Quality</label>': '<label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">WebP 품질</label>',
    '<span>Smaller file</span>': '<span>더 작은 파일</span>',
    '<span>Higher quality</span>': '<span>더 높은 품질</span>',
    '<button class="btn-primary" id="convertBtn">Convert to WebP</button>': '<button class="btn-primary" id="convertBtn">WebP로 변환</button>',
    '<button class="btn-secondary" id="resetBtn">Choose Again</button>': '<button class="btn-secondary" id="resetBtn">다시 선택</button>',
    '<h3>Conversion Complete!</h3>': '<h3>변환 완료!</h3>',
    '<button class="btn-primary" id="downloadAllBtn">Download All WebP</button>': '<button class="btn-primary" id="downloadAllBtn">모든 WebP 다운로드</button>',
    '<button class="btn-link" id="startOverBtn">Convert More Images</button>': '<button class="btn-link" id="startOverBtn">더 많은 이미지 변환</button>',
    '← Back to PicEte Home': '← PicEte 홈으로 돌아가기',
    '<h2 class="section-title">Why Convert to WebP Format</h2>': '<h2 class="section-title">WebP 형식으로 변환해야 하는 이유</h2>',
    '<h3>Smaller Files</h3>': '<h3>더 작은 파일</h3>',
    '<p>WebP is 30-50% smaller than PNG, significantly saving storage space and bandwidth.</p>': '<p>WebP는 PNG보다 30-50% 작아 저장 공간과 대역폭을 크게 절약합니다.</p>',
    '<h3>Maintain Quality</h3>': '<h3>품질 유지</h3>',
    '<p>While reducing file size, WebP maintains visual quality comparable to PNG.</p>': '<p>파일 크기를 줄이면서도 PNG에 필적하는 시각적 품질을 유지합니다.</p>',
    '<h3>Modern Standard</h3>': '<h3>최신 표준</h3>',
    '<p>WebP is the standard format for modern browsers, supported by all major browsers.</p>': '<p>WebP는 모든 주요 브라우저에서 지원되는 최신 브라우저 표준 형식입니다.</p>',
    '<h3>Better Performance</h3>': '<h3>향상된 성능</h3>',
    '<p>Smaller files mean faster loading times and improved user experience.</p>': '<p>파일이 작아지면 로딩 시간이 빨라지고 사용자 경험이 향상됩니다.</p>',
    '<h2 class="section-title">How to Convert PNG to WebP Online Free</h2>': '<h2 class="section-title">온라인에서 무료로 PNG를 WebP로 변환하는 방법</h2>',
    'Drop Your PNGs In': 'PNG 파일 드롭',
    'Click the upload area or drag PNG images into the browser. This PNG to WebP converter handles batch uploads — product photos, website graphics, design assets, all at once. Standard PNGs work, and so do files with alpha transparency (WebP preserves it perfectly). Everything runs locally, so your images never leave your computer.': '업로드 영역을 클릭하거나 브라우저로 PNG 이미지를 드래그하세요. 이 PNG to WebP 변환기는 제품 사진, 웹사이트 그래픽, 디자인 에셋 등 일괄 업로드를 지원합니다. 표준 PNG뿐만 아니라 알파 투명도를 가진 파일도 지원합니다(WebP가 완벽하게 유지함). 모든 과정이 로컬에서 실행되므로 이미지가 컴퓨터 외부로 전송되지 않습니다.',
    'Choose Quality, Get WebP': '품질 선택 및 WebP 얻기',
    'Conversion starts automatically once files are loaded. The quality slider controls compression — 90-100% gives near-lossless results visually identical to the original PNG. Lower values (70-85%) maximize file size savings. WebP supports both lossy and lossless modes, and the converter picks the best approach based on your setting. Alpha transparency carries over untouched.': '파일이 로드되면 변환이 자동으로 시작됩니다. 품질 슬라이더로 압축률을 조절할 수 있습니다 — 90-100%는 원본 PNG와 시각적으로 동일한 거의 무손실 결과를 제공합니다. 낮은 값(70-85%)은 파일 크기 절약을 극대화합니다. WebP는 손실 및 무손실 모드를 모두 지원하며, 변환기가 설정에 따라 최상의 접근 방식을 선택합니다. 알파 투명도는 그대로 유지됩니다.',
    'Download the Savings': '저장된 파일 다운로드',
    'Each WebP file shows its new size with a savings percentage compared to the original PNG. Download one by one or batch-save everything at once. Expect files 30-50% smaller than the originals — ready to upload to your website, CMS, or CDN for immediate performance gains.': '각 WebP 파일은 원본 PNG와 비교하여 절약된 비율과 함께 새로운 크기를 표시합니다. 하나씩 다운로드하거나 한 번에 모두 일괄 저장하세요. 원본보다 30-50% 더 작은 파일을 기대하세요. 즉각적인 성능 향상을 위해 웹사이트, CMS 또는 CDN에 업로드할 준비가 완료되었습니다.',
    '<h2 class="section-title">PNG to WebP Tips</h2>': '<h2 class="section-title">PNG to WebP 팁</h2>',
    'Why WebP Crushes PNG for Web Use': 'WebP가 웹용으로 PNG를 압도하는 이유',
    'WebP is 30-50% smaller than PNG at the same visual quality, with full transparency support. That means faster pages, lower bandwidth, and better Core Web Vitals scores — things that directly affect user experience and search rankings. WebP also handles animation (replacing animated GIFs with much smaller files), though this converter focuses on static images. For any site using PNG assets, switching to WebP is one of the highest-impact optimizations available.': 'WebP는 동일한 시각적 품질에 완벽한 투명도 지원을 갖추고서도 PNG보다 30-50% 더 작습니다. 이는 더 빠른 페이지 속도, 더 적은 대역폭, 더 나은 코어 웹 바이탈 점수를 의미하며, 사용자 경험과 검색 순위에 직접적인 영향을 미칩니다. 이 변환기는 정적 이미지에 중점을 두지만, WebP는 애니메이션도 지원합니다(애니메이션 GIF를 훨씬 더 작은 파일로 대체). PNG 에셋을 사용하는 모든 사이트에서 WebP로 전환하는 것은 가장 효과적인 최적화 방법 중 하나입니다.',
    'Real Performance Gains from WebP': 'WebP를 통한 실제 성능 향상',
    'A typical e-commerce site with hundreds of product images can cut total image weight by 30-50% just by converting PNGs to WebP. That translates to 1-3 seconds faster page loads — studies show this can boost conversion rates by up to 7%. For mobile users on limited data plans, the savings hit even harder. Combined with lazy loading and responsive images, WebP compression is the foundation of modern image optimization.': '수백 개의 제품 이미지가 있는 일반적인 전자상거래 사이트는 PNG를 WebP로 변환하는 것만으로 전체 이미지 용량을 30-50% 줄일 수 있습니다. 이는 페이지 로딩을 1-3초 더 빠르게 만들어, 연구에 따르면 전환율을 최대 7%까지 높일 수 있습니다. 제한된 데이터 요금제를 사용하는 모바일 사용자에게는 이 절약 효과가 더욱 크게 다가옵니다. 지연 로딩(lazy loading) 및 반응형 이미지와 결합하면 WebP 압축은 최신 이미지 최적화의 기반이 됩니다.',
    'Browser Support Is a Non-Issue Now': '브라우저 지원은 더 이상 문제가 아닙니다',
    'All major browsers support WebP — Chrome, Firefox, Edge, Safari, Opera. Over 95% of web users globally can view WebP images as of 2024. For the tiny fraction on older browsers, use the HTML picture element with PNG fallback. Most CMS platforms like WordPress handle this automatically through plugins. Our converter makes it easy to generate both formats so everyone sees optimized images.': '모든 주요 브라우저가 WebP를 지원합니다 — Chrome, Firefox, Edge, Safari, Opera 등. 2024년 기준 전 세계 95% 이상의 웹 사용자가 WebP 이미지를 볼 수 있습니다. 구형 브라우저를 사용하는 소수의 사용자를 위해서는 HTML picture 요소와 PNG 대체 이미지를 사용하세요. WordPress와 같은 대부분의 CMS 플랫폼은 플러그인을 통해 이를 자동으로 처리합니다. 당사의 변환기를 사용하면 두 가지 형식을 모두 쉽게 생성할 수 있어 누구나 최적화된 이미지를 볼 수 있습니다.',
    '<h2 class="section-title">Frequently Asked Questions</h2>': '<h2 class="section-title">자주 묻는 질문</h2>',
    '<summary class="faq-question">How much smaller is WebP compared to PNG?</summary>': '<summary class="faq-question">WebP는 PNG와 비교하여 얼마나 더 작은가요?</summary>',
    '<p class="faq-answer">WebP typically reduces file size by 25-35% compared to PNG while maintaining the same visual quality. For photos with lossy WebP compression, savings reach 80-90%. For lossless WebP (preserving transparency), you still get roughly 30% smaller files. WebP is designed specifically for web performance.</p>': '<p class="faq-answer">WebP는 동일한 시각적 품질을 유지하면서 PNG에 비해 파일 크기를 일반적으로 25-35% 줄입니다. 손실 WebP 압축을 사용하는 사진의 경우 최대 80-90%까지 줄일 수 있습니다. 무손실 WebP(투명도 유지)의 경우에도 약 30% 더 작은 파일을 얻을 수 있습니다. WebP는 특히 웹 성능을 위해 설계되었습니다.</p>',
    '<summary class="faq-question">Does WebP support transparency like PNG?</summary>': '<summary class="faq-question">WebP도 PNG처럼 투명도를 지원하나요?</summary>',
    '<p class="faq-answer">Yes, WebP fully supports alpha transparency channels. You can convert transparent PNGs to WebP and the transparency is preserved perfectly. This makes WebP an ideal replacement for PNG on the web — same visual quality with transparency, but significantly smaller file sizes.</p>': '<p class="faq-answer">네, WebP는 알파 투명도 채널을 완벽하게 지원합니다. 투명한 PNG를 WebP로 변환해도 투명도가 완벽하게 유지됩니다. 이로 인해 WebP는 웹에서 PNG의 이상적인 대체품이 됩니다. 투명도를 포함한 동일한 시각적 품질에 파일 크기는 훨씬 작습니다.</p>',
    '<summary class="faq-question">Is WebP supported in all browsers?</summary>': '<summary class="faq-question">WebP는 모든 브라우저에서 지원되나요?</summary>',
    '<p class="faq-answer">WebP is supported by all modern browsers including Chrome (since 2010), Firefox (since 2018), Safari (since 2020), and Edge (since 2018). Over 97% of web users can view WebP images. For edge cases, you can use a fallback strategy with the <picture> element.</picture></p>': '<p class="faq-answer">WebP는 Chrome(2010년 이후), Firefox(2018년 이후), Safari(2020년 이후), Edge(2018년 이후)를 포함한 모든 최신 브라우저에서 지원됩니다. 97% 이상의 웹 사용자가 WebP 이미지를 볼 수 있습니다. 예외적인 경우에는 <picture> 요소를 사용한 대체 전략을 사용할 수 있습니다.</p>',
    '<summary class="faq-question">Should I convert all my PNGs to WebP?</summary>': '<summary class="faq-question">모든 PNG를 WebP로 변환해야 하나요?</summary>',
    '<p class="faq-answer">For web use, yes — replacing PNG with WebP improves page load speed without quality loss, especially beneficial for mobile users on slow connections. For images you need to edit or share outside the web, keep the original PNG. WebP is still not universally supported in offline tools like Photoshop without plugins.</p>': '<p class="faq-answer">웹용이라면 네 그렇습니다. PNG를 WebP로 대체하면 품질 저하 없이 페이지 로딩 속도가 향상되며, 느린 연결을 사용하는 모바일 사용자에게 특히 유용합니다. 웹 외부에서 편집하거나 공유해야 하는 이미지의 경우 원본 PNG를 유지하세요. WebP는 아직 플러그인 없이 Photoshop과 같은 오프라인 도구에서 보편적으로 지원되지는 않습니다.</p>',
    '<li><a href="../resize-image/">Image Resizer</a></li>': '<li><a href="../resize-image/">이미지 크기 조정</a></li>',
    '<li><a href="../">Back to Home</a></li>': '<li><a href="../">홈으로 돌아가기</a></li>',
    '<li><a href="/privacy-policy.html">Privacy Policy</a></li>': '<li><a href="/privacy-policy.html">개인정보 처리방침</a></li>',
    'MockupShot - Screenshot Mockup': 'MockupShot - 스크린샷 목업',
    'ILovePalette - Color Tools': 'ILovePalette - 색상 도구',
    "alert('Please select PNG images')": "alert('PNG 이미지를 선택해주세요')",
    "alert('Failed to load images')": "alert('이미지 로드에 실패했습니다')",
    '<button class="btn-primary" onclick="downloadOne(${i})">Download</button>': '<button class="btn-primary" onclick="downloadOne(${i})">다운로드</button>'
}

for k, v in replacements.items():
    content = content.replace(k, v)

content = content.replace('<h4>More Tools</h4>', '<h4>더 많은 도구</h4>', 1)
content = content.replace('<h4>More Tools</h4>', '<h4>파트너 사이트</h4>', 1)
content = content.replace('<h4>About</h4>', '<h4>소개</h4>', 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
