# PicEte 全站系统测试方案

## 测试目标
对 PicEte 所有 9 个工具页面做全面功能测试 + 链接检查 + 错误检查。

## 页面列表
1. `/home/wu/picete-site/index.html` — 首页
2. `/home/wu/picete-site/png-to-jpg/index.html`
3. `/home/wu/picete-site/jpg-to-png/index.html`
4. `/home/wu/picete-site/webp-to-png/index.html`
5. `/home/wu/picete-site/png-to-webp/index.html`
6. `/home/wu/picete-site/jpg-to-webp/index.html`
7. `/home/wu/picete-site/resize-image/index.html`
8. `/home/wu/picete-site/compress-image/index.html`
9. `/home/wu/picete-site/image-splitter/index.html`
10. `/home/wu/picete-site/extract-colors/index.html`
11. `/home/wu/picete-site/image-to-base64/index.html`

## 测试类型

### 1. 基础结构测试（所有页面）
- HTML 是否有基本结构（DOCTYPE, html, head, body）
- SEO meta: title, description, canonical 是否正确配置
- 页面标题是否包含 "PicEte"
- OG tags 是否完整（og:title, og:description, og:url, og:image）
- Schema.org WebApplication 是否有
- Google Analytics (G-H72N80TEBW) 是否存在
- favicon 链接是否正确（favicon.svg + favicon.ico）
- llms.txt + mcp.json 链接是否存在
- msvalidate.01 是否存在
- CSS 链接是否正确 (../css/style.css)
- Header: logo, navigation, tagline
- Footer: 所有工具链接是否可访问（不返回 404）
- 面包屑导航是否有

### 2. 功能测试（Playwright 浏览器测试）
每个工具页面：
- 页面是否正常加载（无 JS 错误）
- Upload area 是否可见
- 是否能上传图片
- 处理/转换按钮是否可用
- 结果是否正确展示
- 下载按钮是否可用
- "Reset" / "Start Over" 是否正常工作

具体页面特殊测试：
- **首页**: tools grid 里列出了多少个工具，是否和实际 pages 数量一致
- **Index.html 首页**: 所有工具链接可点击跳转
- **image-splitter**: 上传后能设置网格参数，切图，展示结果
- **extract-colors**: 上传后滑块调色板数量，提取颜色，展示色块
- **image-to-base64**: Upload/URL 双标签切换，Base64 输出，复制按钮，格式切换

### 3. 链接完整性检查
- 首页 tools-grid 里的每个工具链接是否对应正确的页面
- Footer 里每个链接是否都能访问
- 返回首页的链接是否正常
- sitemap.xml 里的所有 URL 是否和实际页面匹配

### 4. HTML 验证
- 基本 HTML 语法（标签闭合）
- 必要的 meta tags

## 测试图片
使用 Playwright 生成一张测试图片（彩色渐变），避免依赖外部资源。

## 输出
最终输出一份 HTML 测试报告，包含：
- 每个页面的测试结果（通过/失败）
- 发现的 bug 和具体位置
- 截图（如果有异常）
