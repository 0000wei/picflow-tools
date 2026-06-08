import os

file_path = "d:/knowledge-base/06项目/哥飞建站/picete/ko/mcp-guide/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    '<title>PicEte MCP Integration Guide — Use from Claude, Cursor & Any AI Agent</title>': '<title>PicEte MCP 연동 가이드 — Claude, Cursor 및 모든 AI 에이전트에서 사용하기</title>',
    '<meta name="description" content="Learn how to integrate PicEte\'s image processing tools into your AI workflow via MCP. Works with Claude Code, Cursor, Claude Desktop, and any MCP-compatible client.">': '<meta name="description" content="MCP를 통해 PicEte의 이미지 처리 도구를 AI 워크플로에 연동하는 방법을 알아보세요. Claude Code, Cursor, Claude Desktop 및 모든 MCP 호환 클라이언트에서 작동합니다.">',
    '"name": "PicEte MCP Integration Guide"': '"name": "PicEte MCP 연동 가이드"',
    '"headline": "Use PicEte from Claude, Cursor & Any AI Agent"': '"headline": "Claude, Cursor 및 모든 AI 에이전트에서 PicEte 사용하기"',
    '"description": "Step-by-step guide to integrate PicEte MCP Server for local image processing in AI workflows."': '"description": "AI 워크플로에서 로컬 이미지 처리를 위한 PicEte MCP 서버 연동 단계별 가이드."',
    '<h1>PicEte MCP Integration Guide</h1>': '<h1>PicEte MCP 연동 가이드</h1>',
    '<p class="subtitle">Use PicEte\'s image processing tools from Claude Code, Cursor, Claude Desktop, or any MCP-compatible AI client.</p>': '<p class="subtitle">Claude Code, Cursor, Claude Desktop 또는 기타 MCP 호환 AI 클라이언트에서 PicEte의 이미지 처리 도구를 사용하세요.</p>',
    '<h2>What is MCP?</h2>': '<h2>MCP란 무엇인가요?</h2>',
    '<p><strong>Model Context Protocol (MCP)</strong> is an open standard that lets AI agents (like Claude Code, Cursor) call external tools directly. With <code>picete-mcp</code>, your AI can process images — compress, convert, resize, extract colors — <strong>without leaving your terminal and without uploading to any server</strong>.</p>': '<p><strong>모델 컨텍스트 프로토콜(MCP)</strong>은 AI 에이전트(예: Claude Code, Cursor)가 외부 도구를 직접 호출할 수 있게 해주는 오픈 표준입니다. <code>picete-mcp</code>를 사용하면 AI가 터미널을 벗어나거나 <strong>서버에 업로드하지 않고도</strong> 이미지를 처리(압축, 변환, 크기 조정, 색상 추출)할 수 있습니다.</p>',
    '<p>All processing runs locally via <strong>Sharp</strong>. Zero data leaves your machine. Same privacy guarantee as <a href="https://picete.com">PicEte</a>.</p>': '<p>모든 처리는 <strong>Sharp</strong>를 통해 로컬에서 실행됩니다. 어떤 데이터도 기기 외부로 전송되지 않습니다. <a href="https://picete.com">PicEte</a>와 동일한 개인정보 보호를 보장합니다.</p>',
    '<h2>Quick Start</h2>': '<h2>빠른 시작</h2>',
    '<p>Install and run with a single command (no signup, no config needed for testing):</p>': '<p>단일 명령어로 설치 및 실행하세요 (테스트를 위한 가입이나 설정이 필요하지 않습니다):</p>',
    '<p><span class="npm-badge">npm</span> Package: <a href="https://www.npmjs.com/package/picete-mcp">picete-mcp@1.0.0</a></p>': '<p><span class="npm-badge">npm</span> 패키지: <a href="https://www.npmjs.com/package/picete-mcp">picete-mcp@1.0.0</a></p>',
    '<h2>Platform Configuration</h2>': '<h2>플랫폼 설정</h2>',
    '<p>Add the following to your AI client\'s MCP configuration:</p>': '<p>AI 클라이언트의 MCP 설정에 다음을 추가하세요:</p>',
    '<h3>Claude Desktop</h3>': '<h3>Claude Desktop</h3>',
    '<p>Edit <code>claude_desktop_config.json</code>:</p>': '<p><code>claude_desktop_config.json</code> 수정:</p>',
    '<h3>Cursor</h3>': '<h3>Cursor</h3>',
    '<p>Edit <code>.cursor/mcp.json</code> in your project root:</p>': '<p>프로젝트 루트의 <code>.cursor/mcp.json</code> 수정:</p>',
    '<h3>Claude Code</h3>': '<h3>Claude Code</h3>',
    '<p>Edit <code>~/.claude/settings.json</code>:</p>': '<p><code>~/.claude/settings.json</code> 수정:</p>',
    '<h2>Available Tools</h2>': '<h2>사용 가능한 도구</h2>',
    '<p>picete-mcp provides <strong>13 tools</strong> across two categories:</p>': '<p>picete-mcp는 두 가지 카테고리에 걸쳐 <strong>13개의 도구</strong>를 제공합니다:</p>',
    '<h3>Atomic Tools</h3>': '<h3>원자 단위 도구(Atomic Tools)</h3>',
    '<tr><th>Tool</th><th>Function</th><th>Key Parameters</th></tr>': '<tr><th>도구</th><th>기능</th><th>주요 매개변수</th></tr>',
    '<tr><td><code>convert</code></td><td>Format conversion</td><td>source, format (jpeg/png/webp/gif), quality</td></tr>': '<tr><td><code>convert</code></td><td>형식 변환</td><td>source, format (jpeg/png/webp/gif), quality</td></tr>',
    '<tr><td><code>resize</code></td><td>Resize image</td><td>source, width, height, fit, keep_aspect_ratio</td></tr>': '<tr><td><code>resize</code></td><td>이미지 크기 조정</td><td>source, width, height, fit, keep_aspect_ratio</td></tr>',
    '<tr><td><code>compress</code></td><td>Compress file size</td><td>source, quality, target_format, max_size_bytes</td></tr>': '<tr><td><code>compress</code></td><td>파일 크기 압축</td><td>source, quality, target_format, max_size_bytes</td></tr>',
    '<tr><td><code>extract-colors</code></td><td>Extract dominant colors</td><td>source, color_count (default 5)</td></tr>': '<tr><td><code>extract-colors</code></td><td>주요 색상 추출</td><td>source, color_count (기본 5)</td></tr>',
    '<tr><td><code>image-to-base64</code></td><td>Convert to base64/data URL</td><td>source, format, data_url</td></tr>': '<tr><td><code>image-to-base64</code></td><td>base64/data URL로 변환</td><td>source, format, data_url</td></tr>',
    '<tr><td><code>split-image</code></td><td>Split into grid tiles</td><td>source, rows, cols, overlap_px</td></tr>': '<tr><td><code>split-image</code></td><td>그리드 타일로 분할</td><td>source, rows, cols, overlap_px</td></tr>',
    '<tr><td><code>metadata</code></td><td>Get image metadata</td><td>source</td></tr>': '<tr><td><code>metadata</code></td><td>이미지 메타데이터 가져오기</td><td>source</td></tr>',
    '<tr><td><code>batch</code></td><td>Chain multiple operations</td><td>sources[], operations[]</td></tr>': '<tr><td><code>batch</code></td><td>여러 작업 체이닝(일괄 처리)</td><td>sources[], operations[]</td></tr>',
    '<h3>Smart Tools</h3>': '<h3>스마트 도구(Smart Tools)</h3>',
    '<tr><td><code>optimize-for-web</code></td><td>One-click web optimization</td><td>source, max_width, quality, output_format</td></tr>': '<tr><td><code>optimize-for-web</code></td><td>원클릭 웹 최적화</td><td>source, max_width, quality, output_format</td></tr>',
    '<tr><td><code>prepare-for-vision-api</code></td><td>AI Vision preprocessing + token estimation</td><td>source, max_longest_side, quality</td></tr>': '<tr><td><code>prepare-for-vision-api</code></td><td>AI 비전 전처리 + 토큰 예측</td><td>source, max_longest_side, quality</td></tr>',
    '<tr><td><code>favicon</code></td><td>Generate favicon suite (ico + png)</td><td>source, output_dir</td></tr>': '<tr><td><code>favicon</code></td><td>파비콘 세트(ico + png) 생성</td><td>source, output_dir</td></tr>',
    '<tr><td><code>compare-images</code></td><td>Compare two images (MSE/SSIM/diff)</td><td>source1, source2, metric</td></tr>': '<tr><td><code>compare-images</code></td><td>두 이미지 비교(MSE/SSIM/diff)</td><td>source1, source2, metric</td></tr>',
    '<tr><td><code>collage</code></td><td>Stitch images together</td><td>sources[], direction, gap</td></tr>': '<tr><td><code>collage</code></td><td>이미지 이어 붙이기</td><td>sources[], direction, gap</td></tr>',
    '<h2>Usage Examples</h2>': '<h2>사용 예시</h2>',
    '<p>Ask your AI in natural language — it will call the right tool automatically:</p>': '<p>자연어로 AI에게 요청하세요 — 자동으로 올바른 도구를 호출합니다:</p>',
    '<tr><th>You Say</th><th>Tool Called</th></tr>': '<tr><th>요청 예시</th><th>호출되는 도구</th></tr>',
    '<tr><td>"Compress this image to under 200KB"</td><td>compress</td></tr>': '<tr><td>"이 이미지를 200KB 이하로 압축해 줘"</td><td>compress</td></tr>',
    '<tr><td>"Convert this PNG to WebP"</td><td>convert</td></tr>': '<tr><td>"이 PNG를 WebP로 변환해 줘"</td><td>convert</td></tr>',
    '<tr><td>"Resize this photo to 1200px wide"</td><td>resize</td></tr>': '<tr><td>"이 사진을 가로 1200px로 크기 조정해 줘"</td><td>resize</td></tr>',
    '<tr><td>"Generate all favicon sizes from this logo"</td><td>favicon</td></tr>': '<tr><td>"이 로고로 모든 크기의 파비콘을 생성해 줘"</td><td>favicon</td></tr>',
    '<tr><td>"What colors are in this image?"</td><td>extract-colors</td></tr>': '<tr><td>"이 이미지에 어떤 색상이 있니?"</td><td>extract-colors</td></tr>',
    '<tr><td>"Optimize this for my website"</td><td>optimize-for-web</td></tr>': '<tr><td>"내 웹사이트에 맞게 최적화해 줘"</td><td>optimize-for-web</td></tr>',
    '<tr><td>"Prepare this image for GPT-4 Vision"</td><td>prepare-for-vision-api</td></tr>': '<tr><td>"GPT-4 Vision용으로 이 이미지를 준비해 줘"</td><td>prepare-for-vision-api</td></tr>',
    '<tr><td>"Split this image into a 3x3 grid"</td><td>split-image</td></tr>': '<tr><td>"이 이미지를 3x3 그리드로 분할해 줘"</td><td>split-image</td></tr>',
    '<tr><td>"Compare these two screenshots"</td><td>compare-images</td></tr>': '<tr><td>"이 두 스크린샷을 비교해 줘"</td><td>compare-images</td></tr>',
    '<tr><td>"Get the metadata of this image"</td><td>metadata</td></tr>': '<tr><td>"이 이미지의 메타데이터를 가져와 줘"</td><td>metadata</td></tr>',
    '<tr><td>"Stitch these images horizontally"</td><td>collage</td></tr>': '<tr><td>"이 이미지들을 가로로 이어 붙여 줘"</td><td>collage</td></tr>',
    '<tr><td>"Convert this to base64"</td><td>image-to-base64</td></tr>': '<tr><td>"이것을 base64로 변환해 줘"</td><td>image-to-base64</td></tr>',
    '<tr><td>"Batch resize and compress these 10 images"</td><td>batch</td></tr>': '<tr><td>"이 10개 이미지를 일괄 크기 조정하고 압축해 줘"</td><td>batch</td></tr>',
    '<h2>Development</h2>': '<h2>개발</h2>',
    '# Clone and build': '# 클론 및 빌드',
    '# Start the MCP server': '# MCP 서버 시작',
    '<a href="https://picete.com/" class="back-link">← Back to PicEte</a>': '<a href="https://picete.com/" class="back-link">← PicEte 홈으로 돌아가기</a>',
    '<p style="margin-top: 2rem; font-size: 0.85rem; color: #9ca3af;">Powered by <a href="https://picete.com">PicEte</a> — Free Online Image Tools</p>': '<p style="margin-top: 2rem; font-size: 0.85rem; color: #9ca3af;">Powered by <a href="https://picete.com">PicEte</a> — 무료 온라인 이미지 도구</p>'
}

for k, v in replacements.items():
    content = content.replace(k, v)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done mcp")
