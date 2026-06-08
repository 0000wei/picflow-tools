import os

file_path = "d:/knowledge-base/06项目/哥飞建站/picete/ko/png-to-webp-for-wordpress/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    '<title>Convert PNG to WebP for WordPress - Free Performance Optimizer | PicEte</title>': '<title>WordPress용 PNG를 WebP로 변환 - 무료 성능 최적화기 | PicEte</title>',
    '<meta content="Convert PNG to WebP for WordPress. Free online tool to optimize images for WordPress sites. Reduce file size by 80% while maintaining quality." name="description"/>': '<meta content="WordPress용 PNG를 WebP로 변환하세요. WordPress 사이트의 이미지를 최적화하는 무료 온라인 도구입니다. 품질을 유지하면서 파일 크기를 80%까지 줄입니다." name="description"/>',
    '<meta content="PNG to WebP for WordPress, convert PNG to WebP, WordPress image optimization, WebP converter" name="keywords"/>': '<meta content="WordPress용 PNG를 WebP로, PNG WebP 변환, WordPress 이미지 최적화, WebP 변환기" name="keywords"/>',
    '<meta content="Convert PNG to WebP for WordPress - Performance Optimizer" property="og:title"/>': '<meta content="WordPress용 PNG를 WebP로 변환 - 성능 최적화기" property="og:title"/>',
    '<meta content="Free online tool to convert PNG to WebP for faster WordPress sites." property="og:description"/>': '<meta content="더 빠른 WordPress 사이트를 위해 PNG를 WebP로 변환하는 무료 온라인 도구입니다." property="og:description"/>',
    '"name": "PNG to WebP for WordPress"': '"name": "WordPress용 PNG to WebP"',
    '"description": "Free online tool to convert PNG images to WebP format for WordPress optimization"': '"description": "WordPress 최적화를 위해 PNG 이미지를 WebP 형식으로 변환하는 무료 온라인 도구"',
    '"name": "Does WordPress support WebP natively?"': '"name": "WordPress는 기본적으로 WebP를 지원하나요?"',
    '"text": "Yes, WordPress has supported WebP since version 5.8. You can upload WebP images directly in the Media Library. Some hosting providers may need a minor server config update, but most modern WordPress hosts handle WebP without any extra setup."': '"text": "네, WordPress는 버전 5.8부터 WebP를 지원해 왔습니다. 미디어 라이브러리에서 WebP 이미지를 직접 업로드할 수 있습니다. 일부 호스팅 제공업체는 약간의 서버 구성 업데이트가 필요할 수 있지만, 대부분의 최신 WordPress 호스트는 추가 설정 없이 WebP를 처리합니다."',
    '"name": "How much will converting PNG to WebP speed up my WordPress site?"': '"name": "PNG를 WebP로 변환하면 WordPress 사이트 속도가 얼마나 향상되나요?"',
    '"text": "WebP images are typically 25-35% smaller than PNGs. For a WordPress site with 50+ images per page (common in galleries and portfolios), this means 30-50% faster load times. Core Web Vitals scores improve significantly \\u2014 especially LCP (Largest Contentful Paint)."': '"text": "WebP 이미지는 일반적으로 PNG보다 25-35% 더 작습니다. 페이지당 50개 이상의 이미지가 있는 WordPress 사이트(갤러리 및 포트폴리오에서 흔함)의 경우 로드 시간이 30-50% 더 빨라집니다. 코어 웹 바이탈 점수, 특히 LCP(최대 콘텐츠 풀 페인트)가 크게 향상됩니다."',
    '"name": "Do I need a plugin to serve WebP on WordPress?"': '"name": "WordPress에서 WebP를 제공하려면 플러그인이 필요한가요?"',
    '"text": "No. WordPress 5.8+ accepts WebP uploads natively. Just upload your converted WebP files directly. For automatic conversion at upload time or serving WebP only to compatible browsers, plugins like WebP Express or EWWW Image Optimizer are helpful but not required."': '"text": "아니요. WordPress 5.8 이상은 WebP 업로드를 기본적으로 허용합니다. 변환된 WebP 파일을 직접 업로드하기만 하면 됩니다. 업로드 시 자동 변환하거나 호환되는 브라우저에만 WebP를 제공하려면 WebP Express 또는 EWWW Image Optimizer와 같은 플러그인이 유용하지만 필수는 아닙니다."',
    '"name": "Will conversion affect image transparency for WordPress?"': '"name": "변환이 WordPress의 이미지 투명도에 영향을 미치나요?"',
    '"text": "WebP fully supports alpha transparency, so your transparent PNG logos and graphics will work perfectly as WebP on WordPress. The transparency is preserved during conversion, and WordPress displays it correctly in both the admin panel and on the frontend."': '"text": "WebP는 알파 투명도를 완벽하게 지원하므로 투명한 PNG 로고 및 그래픽이 WordPress에서 WebP로 완벽하게 작동합니다. 변환 중 투명도가 유지되며 WordPress는 관리자 패널과 프런트엔드 모두에서 투명도를 올바르게 표시합니다."',
    '<p class="tagline">Format Converter</p>': '<p class="tagline">형식 변환기</p>',
    '<a class="nav-link" href="../">Home</a>': '<a class="nav-link" href="../">홈</a>',
    '<a class="nav-link" href="../#tools">More Tools</a>': '<a class="nav-link" href="../#tools">더 많은 도구</a>',
    '<div class="breadcrumb"><a href="https://picete.com/">Home</a><span class="separator">›</span><a href="../png-to-webp/">PNG to WebP</a><span class="separator">›</span><span class="current">For WordPress</span></div>': '<div class="breadcrumb"><a href="https://picete.com/">홈</a><span class="separator">›</span><a href="../png-to-webp/">PNG to WebP</a><span class="separator">›</span><span class="current">WordPress용</span></div>',
    '<h1 class="hero-title">Convert PNG to WebP for WordPress</h1>': '<h1 class="hero-title">WordPress용 PNG를 WebP로 변환</h1>',
    '<h2 class="hero-subtitle">Speed Up Your WordPress Site</h2>': '<h2 class="hero-subtitle">WordPress 사이트 속도 향상</h2>',
    'Large PNG images slow down WordPress sites. Converting to WebP can reduce file sizes by 70-90% while maintaining the same visual quality. Faster pages mean better Google rankings, improved user experience, and lower hosting costs. PicEte converts PNG to WebP instantly — just upload, convert, and use in WordPress with any WebP plugin or native support.': '큰 PNG 이미지는 WordPress 사이트의 속도를 늦춥니다. WebP로 변환하면 동일한 시각적 품질을 유지하면서 파일 크기를 70-90% 줄일 수 있습니다. 페이지가 빨라지면 Google 순위가 높아지고 사용자 경험이 향상되며 호스팅 비용이 절감됩니다. PicEte는 PNG를 WebP로 즉시 변환합니다 — 업로드하고 변환한 다음 WebP 플러그인이나 기본 지원을 통해 WordPress에서 사용하세요.',
    '<h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: var(--text-color);">Why Use WebP for WordPress?</h3>': '<h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: var(--text-color);">WordPress에서 WebP를 사용해야 하는 이유</h3>',
    "WordPress natively supports WebP since version 5.8, making it the default recommended format for new uploads. Modern plugins like ShortPixel, Smush, and EWWW automatically convert images to WebP for better performance. Google's Core Web Vitals ranking factors directly reward faster pages — large image files are the most common cause of slow LCP (Largest Contentful Paint) scores. Converting PNG screenshots, graphics, and photos to WebP is the single most effective image optimization for most WordPress sites.": "WordPress는 버전 5.8부터 WebP를 기본적으로 지원하므로 새 업로드의 권장 기본 형식입니다. ShortPixel, Smush, EWWW와 같은 최신 플러그인은 더 나은 성능을 위해 이미지를 자동으로 WebP로 변환합니다. Google의 코어 웹 바이탈 순위 요소는 더 빠른 페이지에 직접적인 보상을 제공합니다 — 큰 이미지 파일은 느린 LCP(최대 콘텐츠 풀 페인트) 점수의 가장 일반적인 원인입니다. PNG 스크린샷, 그래픽 및 사진을 WebP로 변환하는 것은 대부분의 WordPress 사이트에서 가장 효과적인 단일 이미지 최적화 방법입니다.",
    '<h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: var(--text-color);">WebP Support in WordPress</h3>': '<h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: var(--text-color);">WordPress의 WebP 지원</h3>',
    "WordPress 5.8+ generates WebP versions automatically when you upload images. Browsers that support WebP receive the smaller file; older browsers get PNG/JPG fallbacks. This seamless compatibility means no users see broken images. For themes and page builders that don't automatically handle WebP, plugins like LiteSpeed Cache or WP Rocket add support. PicEte's conversion preserves transparency in PNG files, converting it to WebP's alpha channel so your graphics display correctly with transparent backgrounds.": "WordPress 5.8 이상에서는 이미지를 업로드할 때 WebP 버전을 자동으로 생성합니다. WebP를 지원하는 브라우저는 더 작은 파일을 받고, 구형 브라우저는 PNG/JPG 대체 이미지를 받습니다. 이러한 원활한 호환성 덕분에 사용자는 깨진 이미지를 볼 수 없습니다. WebP를 자동으로 처리하지 않는 테마 및 페이지 빌더의 경우 LiteSpeed Cache 또는 WP Rocket과 같은 플러그인이 지원을 추가합니다. PicEte의 변환은 PNG 파일의 투명도를 보존하고 이를 WebP의 알파 채널로 변환하므로 투명한 배경에서도 그래픽이 올바르게 표시됩니다.",
    '<h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: var(--text-color);">WordPress Performance Benefits</h3>': '<h3 style="font-size: 1.25rem; margin-bottom: 1rem; color: var(--text-color);">WordPress 성능 향상 이점</h3>',
    '<li>70-90% smaller file sizes reduce bandwidth usage and hosting costs</li>': '<li>70-90% 더 작은 파일 크기로 대역폭 사용량 및 호스팅 비용 절감</li>',
    '<li>Faster page loads improve Google search rankings</li>': '<li>더 빠른 페이지 로딩으로 Google 검색 순위 향상</li>',
    '<li>Better mobile experience leads to higher engagement and conversions</li>': '<li>더 나은 모바일 경험으로 참여도 및 전환율 증가</li>',
    '<li>CDN storage goes further, allowing more images for same budget</li>': '<li>CDN 스토리지를 효율적으로 사용하여 동일한 예산으로 더 많은 이미지 허용</li>',
    '<li>Core Web Vitals scores improve, directly impacting SEO performance</li>': '<li>코어 웹 바이탈 점수 향상으로 SEO 성능에 직접적인 영향</li>',
    'Use PicEte PNG to WebP Converter Free →': 'PicEte PNG to WebP 변환기 무료로 사용하기 →',
    'Free • No signup • WordPress-ready output': '무료 • 가입 불필요 • WordPress용으로 즉시 사용 가능',
    '<h3 style="font-size: 1.125rem; margin-bottom: 1rem; color: var(--text-color);">Related WordPress Tools</h3>': '<h3 style="font-size: 1.125rem; margin-bottom: 1rem; color: var(--text-color);">관련 WordPress 도구</h3>',
    '<h4>Image Optimization</h4>': '<h4>이미지 최적화</h4>',
    '<li><a href="../compress-image/">Image Compressor</a> — Further size reduction</li>': '<li><a href="../compress-image/">이미지 압축기</a> — 추가 크기 축소</li>',
    '<li><a href="../resize-image-to-1200x630/">Resize to 1200x630</a> — Social sharing</li>': '<li><a href="../resize-image-to-1200x630/">1200x630으로 크기 조정</a> — 소셜 공유</li>',
    '<li><a href="../png-to-jpg/">PNG to JPG</a> — Alternative format</li>': '<li><a href="../png-to-jpg/">PNG to JPG</a> — 대체 형식</li>',
    '<h2 class="section-title">Frequently Asked Questions</h2>': '<h2 class="section-title">자주 묻는 질문</h2>',
    '<summary class="faq-question">Does WordPress support WebP natively?</summary>': '<summary class="faq-question">WordPress는 기본적으로 WebP를 지원하나요?</summary>',
    '<p class="faq-answer">Yes, WordPress has supported WebP since version 5.8. You can upload WebP images directly in the Media Library. Some hosting providers may need a minor server config update, but most modern WordPress hosts handle WebP without any extra setup.</p>': '<p class="faq-answer">네, WordPress는 버전 5.8부터 WebP를 지원해 왔습니다. 미디어 라이브러리에서 WebP 이미지를 직접 업로드할 수 있습니다. 일부 호스팅 제공업체는 약간의 서버 구성 업데이트가 필요할 수 있지만, 대부분의 최신 WordPress 호스트는 추가 설정 없이 WebP를 처리합니다.</p>',
    '<summary class="faq-question">How much will converting PNG to WebP speed up my WordPress site?</summary>': '<summary class="faq-question">PNG를 WebP로 변환하면 WordPress 사이트 속도가 얼마나 향상되나요?</summary>',
    '<p class="faq-answer">WebP images are typically 25-35% smaller than PNGs. For a WordPress site with 50+ images per page (common in galleries and portfolios), this means 30-50% faster load times. Core Web Vitals scores improve significantly — especially LCP (Largest Contentful Paint).</p>': '<p class="faq-answer">WebP 이미지는 일반적으로 PNG보다 25-35% 더 작습니다. 페이지당 50개 이상의 이미지가 있는 WordPress 사이트(갤러리 및 포트폴리오에서 흔함)의 경우 로드 시간이 30-50% 더 빨라집니다. 코어 웹 바이탈 점수, 특히 LCP(최대 콘텐츠 풀 페인트)가 크게 향상됩니다.</p>',
    '<summary class="faq-question">Do I need a plugin to serve WebP on WordPress?</summary>': '<summary class="faq-question">WordPress에서 WebP를 제공하려면 플러그인이 필요한가요?</summary>',
    '<p class="faq-answer">No. WordPress 5.8+ accepts WebP uploads natively. Just upload your converted WebP files directly. For automatic conversion at upload time or serving WebP only to compatible browsers, plugins like WebP Express or EWWW Image Optimizer are helpful but not required.</p>': '<p class="faq-answer">아니요. WordPress 5.8 이상은 WebP 업로드를 기본적으로 허용합니다. 변환된 WebP 파일을 직접 업로드하기만 하면 됩니다. 업로드 시 자동 변환하거나 호환되는 브라우저에만 WebP를 제공하려면 WebP Express 또는 EWWW Image Optimizer와 같은 플러그인이 유용하지만 필수는 아닙니다.</p>',
    '<summary class="faq-question">Will conversion affect image transparency for WordPress?</summary>': '<summary class="faq-question">변환이 WordPress의 이미지 투명도에 영향을 미치나요?</summary>',
    '<p class="faq-answer">WebP fully supports alpha transparency, so your transparent PNG logos and graphics will work perfectly as WebP on WordPress. The transparency is preserved during conversion, and WordPress displays it correctly in both the admin panel and on the frontend.</p>': '<p class="faq-answer">WebP는 알파 투명도를 완벽하게 지원하므로 투명한 PNG 로고 및 그래픽이 WordPress에서 WebP로 완벽하게 작동합니다. 변환 중 투명도가 유지되며 WordPress는 관리자 패널과 프런트엔드 모두에서 투명도를 올바르게 표시합니다.</p>',
    '<h4>More Tools</h4>': '<h4>더 많은 도구</h4>',
    '<li><a href="../compress-image/">Image Compressor</a></li>': '<li><a href="../compress-image/">이미지 압축기</a></li>',
    '<li><a href="../resize-image/">Image Resizer</a></li>': '<li><a href="../resize-image/">이미지 크기 조정</a></li>',
    '<h4>About</h4>': '<h4>소개</h4>',
    '<li><a href="../">Back to Home</a></li>': '<li><a href="../">홈으로 돌아가기</a></li>',
    '<li><a href="/privacy-policy.html">Privacy Policy</a></li>': '<li><a href="/privacy-policy.html">개인정보 처리방침</a></li>',
    '<h4>Partner Sites</h4>': '<h4>파트너 사이트</h4>',
    '<li><a href="https://mockupshot.online/">MockupShot - Screenshot Mockup</a></li>': '<li><a href="https://mockupshot.online/">MockupShot - 스크린샷 목업</a></li>',
    '<li><a href="https://ilovepalette.com/">ILovePalette - Color Tools</a></li>': '<li><a href="https://ilovepalette.com/">ILovePalette - 색상 도구</a></li>'
}

for k, v in replacements.items():
    content = content.replace(k, v)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done wp")
