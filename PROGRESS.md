# PicEte 项目进度

## 项目概述
PicEte 是一个在线图片处理工具站（picete.com），提供 48 个图片处理工具，支持 8 种语言（EN/ZH/JA/DE/FR/ES/PT/AR），部署在 Vercel 上。

---

## 已完成

### 流量增长与 SEO (2026-07-07)
- [x] **pSEO 矩阵页全面覆盖**：对全站 441 个页面更新 SoftwareApplication 和 Breadcrumbs JSON-LD 结构化数据，注入 Canonical 和 10 行 Hreflang 跨语言关联标签，打通全部多语言（9语言）关联。
- [x] **前后效果对比滑动条 (Slider)**：对 15 个 eligible 的图片转换/压缩工具页面注入 Comparison Slider，引入 skeleton loading 骨架屏消除页面 CLS，防抖监听 state 数据自动匹配原图与转换后图片。
- [x] **自愈与审计机制**：编写 `verify_seo_matrix.py` 自动化检测矩阵合规，在 `pSEO_matrix_generator.py` 增强 JSON-LD 子串清理、自愈补充缺失的 container ID 保证全站零报错通过。
- [x] **修复韩语页面损坏**：全面重构、修复受损的 `ko/jpg-to-png` 和 `ko/jpg-to-avif`，保证 HTML 结构合法并完成多语言翻译。

### 工具开发（37 个 EN 工具 + 8 语言翻译）
- [x] 核心工具集（12 个）：resize-image, compress-image, png-to-jpg, jpg-to-png, webp-to-png, png-to-webp, jpg-to-webp, image-splitter, extract-colors, image-to-base64, split-image-into-3x3, split-image-into-4-parts
- [x] 尺寸长尾页（12 个）：resize-image-to-1080x1080, 1920x1080, 800x800, 1200x630, 512x512, 300x250, 600x600, 1500x500, 200x200, 250x250, 728x90, resize-image-for-facebook-cover
- [x] 压缩长尾页（7 个）：compress-image-to-50kb/100kb/200kb/500kb, compress-jpg-to-100kb/200kb, compress-image-for-wordpress/website/email
- [x] 格式长尾页（6 个）：png-to-jpg-for-email, webp-to-png-for-website, png-to-webp-for-wordpress, jpg-to-png-for-instagram, batch-convert-png-to-jpg
- [x] 8 语言全部覆盖（2026-05-26）：zh/ja/de/fr/es/pt/ar 各 38 个页面（1 首页 + 37 工具页）= 266 个翻译页面 + 40 个 EN 页面 = 306 页面

### 架构与基础设施
- [x] **2026-06-02**: Harness Engineering 结构重构 — 分离 config/, docs/, scripts/, seo/ 目录
- [x] **2026-06-02**: 清理跨项目污染文件（删除 mockupshot/screenprintfilter 等无关文件）
- [x] **2026-06-02**: 新增 HARNESS-EXECUTE.md, HARNESS-REFACTOR-SPEC.md, STRUCTURE-RULES.md
- [x] **2026-06-02**: 新增脚本审计工具集（audit 和 fix 脚本在 scripts/ 下）
- [x] SEO: sitemap.xml（313 URLs，含所有 7 个语言首页）, robots.txt, llms.txt, favicon.ico
- [x] **2026-06-02**: sitemap.xml + robots.txt 部署到根目录（cp 保留 seo/ 备份）
- [x] **2026-06-02**: convert/ 目录已删除（113 个空子目录清理完毕）
- [x] **2026-06-02**: privacy-policy 多语言版已复制到 zh/ja/de/fr/es/pt/ar
- [x] **2026-06-02**: F3 — fr 语言 JSON-LD 注入完成（7页：6 ZERO + 1 PARTIAL）
- [x] **P5 工具测试闭环** — 26 EN 工具 + zh/ja 语言抽样，257 assertions 全部 PASS（2026-06-03）

### 设计与体验
- [x] 统一设计系统 + 响应式改进 + 跨工具一致性（2026-05-29）
- [x] 深色模式（深靛蓝黑色背景，暖色文本，logo 适配）
- [x] 语言选择器：用户选择而非自动重定向（SEO 友好）
- [x] P1 多语言 — 7 语言 mcp-guide 翻译完成并部署（2026-06-03）
- [x] P0 POC — wasm-vips 技术验证完成（2026-06-03）：AVIF ✅、RAW ❌(libraw-wasm)、单线程⚠️、COOP/COEP ✅（Vercel 验证通过）
- [x] AI Toolz Dir 外链（独立 footer 行）

---

## 待办

### 执行顺序（V2 优化计划，详见 docs/specs/PICETE-OPTIMIZATION-PLAN-V2.md）

|**P5 — 工具测试闭环（共 10 个 Task）**
|- [x] 5.1 安装 Playwright
|- [x] 5.2 生成 3 张测试图片
|- [x] 5.3 写 resize-image Playwright 测试（框架验证）
|- [x] 5.4 压缩类 7 工具扩展
|- [x] 5.5 格式转换类 6 工具扩展
|- [x] 5.6 缩放类 12 工具扩展
|- [x] 5.7 分割/取色/Base64 5 工具扩展
|- [x] 5.8 语言抽样脚本（zh + ja）
|- [x] 5.9 处理 FAIL 工具（分析+修复）
|- [x] 5.10 生成测试报告文档

**P6 — Lighthouse/CDP 诊断问题修复（共 4 个 Task）**
|- [x] 6.1 修复 cookie-consent.js 致命报错 (GA 加载阻断)
|- [x] 6.2 拷贝 Favicon 修复 404
|- [x] 6.3 编写 scripts/fix/fix_logos.js 批量注入图片宽高
|- [x] 6.4 修复 css/style.css 颜色对比度

**P7 — 修复语言切换器 Bug（共 1 个 Task）**
|- [x] 7.1 编写并执行 scripts/fix/fix_lang_switcher.js 批量修复全站语言切换器

**P8 — 首页 UX 与排版重构 (V3)（共 3 个 Task）**
|- [x] 8.1 更新 css/style.css 注入分类与 Quick Tags 样式
|- [x] 8.2 重构 index.html 标杆（分类网格、引入 Quick Tags、精简 Footer）
|- [x] 8.3 编写执行 scripts/fix/sync_homepage_layout.js 同步所有 7 种语言的首页结构

**Hotfix (违规修复追溯)（共 2 个 Task）**
|- [x] H.1 修复 .faq-item 缺失 padding 导致文字贴边的问题 (修复违规：未记录 Scope/SPEC，越权执行)
|- [x] H.2 补充同步 7 种语言首页的 Footer 结构并清理冗余 (修复违规：未记录 Scope/SPEC，越权执行)

**P1 — mcp-guide 多语言翻译（共 8 个 Task）**
- [x] 1.1 中文翻译
- [x] 1.2 日文翻译
- [x] 1.3 德文翻译
- [x] 1.4 法文翻译
- [x] 1.5 西班牙文翻译
- [x] 1.6 葡萄牙文翻译
- [x] 1.7 阿拉伯文翻译
- [x] 1.8 更新 Makefile + sitemap + 验证

**P0 — wasm-vips 替换 Canvas API（共 14 个 Task）**
|- [x] 0.1.1 npm 初始化 + 安装 wasm-vips
|- [x] 0.1.2 本地测试 HTML（wasm-vips 加载 + SharedArrayBuffer 验证）
|- [x] 0.1.3 wasm-vips resize POC（性能对比 Canvas）
|- [x] 0.1.4 验证 wasm-vips 的 AVIF/RAW codec
|- [x] 0.1.5 单线程 wasm-vips 性能对比
|- [x] 0.1.6 Vercel COOP/COEP header 验证
|- [x] 0.1.7 产出 POC 报告
|- [x] 0.2.1 创建 js/vips-loader.js
|- [x] 0.2.2 重写 compress 核心逻辑（wasm-vips）— v1: bf7d6c8 / v2(browser API fix): bd3c1b5
|- [x] 0.2.3 重写 resize 核心逻辑（wasm-vips）— via Claude Code (09fb6fa)
|- [x] 0.2.4 重写 split 核心逻辑（wasm-vips）— image-splitter via Claude Code (bc4ff19)
**Phase 0.3: 极速模式入口**
|- [x] 0.3.1 创建 fast-convert 完整页面（含交互逻辑）— via Claude Code (f0df6ab)
|- [x] 0.3.2 fast-convert 7 语言翻译 — via delegate_task (09ccd90)
|- [x] 0.3.3 首页入口链接更新 — 8 语言首页 (28d16f9)
|- [x] 0.3.4 更新 sitemap + feature_list — 329 URLs, tool-039

|**P0.5 — AVIF + RAW 支持（共 14 个 Task）**
|- [x] **0.5.0** GA 自托管 — 下载 gtag.js 到 js/，所有 106 个 HTML 改为同源引用 (c348449)
|- [x] **0.5.1** 创建 avif-to-png 工具页 — wasm-vips 解码 AVIF + 编码 PNG
|- [x] **0.5.2** 创建 png-to-avif 工具页 — 含"Fast Encoding"/"Maximum Compression"两套预设
|- [x] **0.5.3** 创建 jpg-to-avif 工具页 — fast/max 预设 + wasm-vips AVIF 编码
|- [x] **0.5.4** 创建 webp-to-avif 工具页 — fast/max 预设 + wasm-vips AVIF 编码
|- [x] **0.5.5a** zh 翻译（标杆）— 4 个 AVIF 工具页全部翻译完成 (fc2bb50)
|- [x] **0.5.5b** ja 翻译（串行）— 三步流水线，4 个 AVIF 工具页全部翻译完成 (420833a)
|- [x] **0.5.5c** de 翻译（串行）— 三步流水线，4 个 AVIF 工具页全部翻译完成 (a3c955a)
|- [x] **0.5.5d** fr 翻译（串行）— 三步流水线，4 个 AVIF 工具页全部翻译完成 (13a118d)
|- [x] **0.5.5e** es 翻译（串行）— 三步流水线，4 个 AVIF 工具页全部翻译完成 (620de38)
|- [x] **0.5.5f** pt 翻译（串行）— 三步流水线，4 个 AVIF 工具页全部翻译完成 (1ae1211)
|- [x] **0.5.5g** ar 翻译（RTL 处理，串行）— 三步流水线，4 个 AVIF 工具页全部翻译完成 (9bed40f)
|- [x] **0.5.6** 首页入口链接更新 — 8 首页 + footer 增加 AVIF 工具入口 (80c41e0)

### 其他待办

### RAW 支持 (方案 C：自编译 wasm-vips + libraw) — V2 规划

| Phase | Task | 内容 | 状态 |
|-------|------|------|------|
| 0.5-A | 0.5.0 | Docker 环境确认 + 标准构建验证 | ✅ |
| 0.5-A | 0.5.7 | 检查 libraw 版本 + 添加版本变量到 build.sh | ✅ |
| 0.5-A | 0.5.8 | 添加 libraw Emscripten 编译步骤到 build.sh | ✅ |
| 0.5-A | **0.5.9 (V2)** | **首次 RAW 构建 — 确保 Canon/Nikon/Sony/DNG 四家可靠** | **✅** |
| 0.5-A | 0.5.9a | 解决 WASM 内存不足 + 修复主流 RAW 解码（21 次测试全部通过） | ✅ |
| 0.5-A | 0.5.9b | 生成 RAW 兼容性清单 | ✅ |
| 0.5-A | 0.5.9c | 产出 RAW 构建和测试报告 | ✅ |
| 0.5-B | 0.5.10a | 修改 build.sh + meson.build（恢复多线程参数） | ✅ |
| 0.5-B | 0.5.10b | 执行 clean build（8 次迭代，libvips 内嵌 pthread，单线程不可行） | ✅ |
| 0.5-B | 0.5.10c | 替换 js/lib/ WASM + 验证（RAW load with libraw_r: true ✅） | ✅ |
| 0.5-B | 0.5.11 | 浏览器 RAW 解码页面测试 — Node.js 端 12/12 RAW 文件通过 ✅ 浏览器加载成功 ⚠️ headless Chrome SAB 限制 | ✅ |
| 0.5-B | 0.5.12 | 性能评估 + 决策 | ✅ |
| 0.5-C | 0.5.13 | raw-to-jpg 工具页 | ✅ |
| 0.5-C | 0.5.14 | raw-to-png 工具页 | ✅ |
| 0.5-C | 0.5.15 | raw-to-webp 工具页 | ✅ |
| 0.5-C | 0.5.16 | raw-to-avif 工具页 | ✅ |
| 0.5-D | 0.5.17a | zh raw-to-jpg | ✅ |
| 0.5-D | 0.5.17b | zh raw-to-png | ✅ |
| 0.5-D | 0.5.17c | zh raw-to-webp | ✅ |
| 0.5-D | 0.5.17d | zh raw-to-avif | ✅ |
| 0.5-D | 0.5.17e | ja raw-to-jpg | ✅ |
| 0.5-D | 0.5.17f | ja raw-to-png | ✅ |
| 0.5-D | 0.5.17g | ja raw-to-webp | ✅ |
| 0.5-D | 0.5.17h | ja raw-to-avif | ✅ |
| 0.5-D | 0.5.17i | de raw-to-jpg | ✅ |
| 0.5-D | 0.5.17j | de raw-to-png | ✅ |
| 0.5-D | 0.5.17k | de raw-to-webp | ✅ |
| 0.5-D | 0.5.17l | de raw-to-avif | ✅ |
| 0.5-D | 0.5.17m | fr raw-to-jpg | ✅ |
| 0.5-D | 0.5.17n | fr raw-to-png | ✅ |
| 0.5-D | 0.5.17o | fr raw-to-webp | ✅ |
| 0.5-D | 0.5.17p | fr raw-to-avif | ✅ |
| 0.5-D | 0.5.17q | es raw-to-jpg | ✅ |
| 0.5-D | 0.5.17r | es raw-to-png | ✅ |
| 0.5-D | 0.5.17s | es raw-to-webp | ✅ |
| 0.5-D | 0.5.17t | es raw-to-avif | ✅ |
| 0.5-D | 0.5.17u | pt raw-to-jpg | ✅ |
| 0.5-D | 0.5.17v | pt raw-to-png | ✅ |
| 0.5-D | 0.5.17w | pt raw-to-webp | ✅ |
| 0.5-D | 0.5.17x | pt raw-to-avif | ✅ |
| 0.5-D | 0.5.17y | ar raw-to-jpg (RTL) | ✅ |
| 0.5-D | 0.5.17z | ar raw-to-png (RTL) | ✅ |
| 0.5-D | 0.5.17aa | ar raw-to-webp (RTL) | ✅ |
| 0.5-D | 0.5.17ab | ar raw-to-avif (RTL) | ✅ |
| 0.5-E | 0.5.18 | 8 首页入口链接更新 | ✅ |
| 0.5-E | 0.5.19 | sitemap 扩容 + feature_list + Makefile + verify | ✅ |

- [x] **SEO 插件集成**：已完成 — GA (G-H72N80TEBW) 接入与自托管 gtag.js + cookie-consent.js 集成完毕
- [x] **Cookie 同意弹窗**：已完成 — js/cookie-consent.js + 8 首页集成 (2026-06-05)
- [x] **OG 图片**：已完成 — 生成 7 种语言的 OG 图片，并更新所有 HTML 页面的 meta 标签 (2026-06-06)
- [x] **FAQ 翻译报告**：已完成 — 审查 docs/reports/untranslated_faqs_report.json，未发现遗漏 (0 file)，报告已清理
- [x] **README 更新**：已完成 — 补充反映最新 Harness Engineering 目录结构的说明 (2026-06-06)
- [x] 多语言同步审计：确保 `ja`, `zh`, `de`, `fr`, `es`, `pt`, `ar`, `ko` 的页脚工具列表、底部信息区、SEO 等设置与主站对齐 (2026-05-25)
- [x] **新增韩语版本 (ko)**：打通路由、升级语言切换器、自动提取翻译注入 50 个 HTML，Sitemap 更新 (2026-06-08)
- [ ] **Facebook Cover Safe Zone Cropper (Phase 1)** — resize-image-for-facebook-cover 改为交互式工具 (9/16)
  - [x] A1 英文版 HTML 骨架 | A2 CSS 追加 | A3 SEO 头信息
  - [x] C1 3步教程 | C2 尺寸科普 | C3 FAQ + FAQPage JSON-LD
  - [x] B1 JS 上传模块（4种方式） | B2 JS 拖拽/缩放/边界约束
  - [x] B3 JS 安全区遮罩渲染（safe/desktop/mobile 模式 + 3x3 网格）
  - [x] B4 JS 沉浸式 UI 绘制（桌面端+移动端 Facebook UI 模拟）
  - [x] B5 JS 导出下载（loading状态 + JPEG quality 0.92 + 文件大小log）
  - [x] D1 JS 触控支持（touchstart/touchmove/touchend + 双指缩放）
  - [x] E1 编写 TEST-CASES-FACEBOOK-COVER.md（25 项测试用例）
  - [x] E2 浏览器逐项验证（19/19 可执行测试 PASS，6 项因 headless 限制跳过）
  - [x] E3 编写 TEST-REPORT-FACEBOOK-COVER.md
  - [x] F1 中文翻译（zh/resize-image-for-facebook-cover/index.html）
  - [x] F2 日语翻译（ja/resize-image-for-facebook-cover/index.html）
  - [x] F3 德语翻译（de/resize-image-for-facebook-cover/index.html）
  - [x] F4 法语翻译（fr/resize-image-for-facebook-cover/index.html）
  - [x] F5 西班牙语翻译（es/resize-image-for-facebook-cover/index.html）
  - [x] F6 葡萄牙语翻译（pt/resize-image-for-facebook-cover/index.html）
  - [x] F7 阿拉伯语翻译（ar/resize-image-for-facebook-cover/index.html, RTL）
  - [x] G1 sitemap 更新（seo/sitemap.xml + 根目录 sitemap.xml lastmod → 2026-06-08）
  - [x] G2 vercel.json 路由更新（EN + 多语言 regex 添加 resize-image-for-facebook-cover）
  - [x] G3 首页入口（7 语言首页 tool-item 卡片 + footer 列表）
  - [x] G4 端到端验证（8 语言页面加载、JS 语法、vercel.json、sitemap、首页入口）
  - [x] F2 日语翻译补完（G4 中发现 tagline/导航/hero/教程/尺寸/footer 遗漏，已补翻）
  - [x] G5 git commit & push

---

### **P9 — Instagram Image Splitter 工具（共 7 个 Task）**
| | Task | 状态 |
|-|------|------|
| | **Task 0** 基础设施目录创建 | ✅ |
| | **Task 1** HTML 英文主页面 | ✅ |
| | **Task 2** JS 核心引擎 | ✅ |
| | **Task 3** 裁剪框交互组件 | ✅ |
| | **Task 4** ZIP 导出 + 移动端降级 | ✅ |
| | **Task 5** 翻译 8 种语言（zh/ja/ko/de/fr/es/pt/ar，每语言独立委托串行） | ✅ |
| | **Task 6** vercel.json + Navbar 集成 | ✅ |
| | **Task 7** 终验（E2E） | ✅ |

---

## 已知问题

1. **Git 历史**：72 次提交，仅 master 分支，无 tag
2. **跨站点链接**：之前存在跨站点 footer 链接（已于 2026-05-25 移除，遵循哥飞 SEO 指导）
3. **语言切换器**：历史上有浏览器自动重定向问题（2026-05-26 修复为用户选择模式）
4. **测试覆盖率**：脚本目录下有一些审计/修复脚本，但缺少自动化集成测试

---

## 统计数据

| 指标 | 数值 |
|------|------|
| 工具总数 (EN) | 50 |
| 翻译语言 | 8 (zh/ja/de/fr/es/pt/ar/ko) |
| 翻译页面数 | 400 |
| 总页面数 | 460 |
| Sitemap URL 数 | 460 |
| Git 提交数 | 171 |

## Session 历史

### 2026-08-15 — 首轮长尾 SEO 优化 (Round 1, branch fm/picete-lt-round1-k1)
- [x] **新增 webp-to-jpg 工具页**：根 + 8 语言镜像（zh/ar/de/es/fr/ja/ko/pt），纯 Canvas 前端转换（无上传、无服务器），含 h2.hero-title、SoftwareApplication/BreadcrumbList/FAQPage JSON-LD、canonical + 10 行 hreflang、OG 对齐；注册进 config/pSEO-matrix.json + SLIDER_ELIGIBLE_TOOLS。
- [x] **CTR 标题优化**：resize-image-to-1080x1080/1200x630/1500x500/200x200/512x512/728x90 + resize-image-for-facebook-cover（根 + ar/es/de 等多语言镜像），标题与 GSC 实际搜索意图对齐（ASCII 尺寸、exact 尺寸描述），og:title/og:description 同步。
- [x] **内部链接 Related Tools 块**：webp-to-png / png-to-jpg / jpg-to-png 及其 8 语言镜像规范化到统一家族集合（png-to-jpg, jpg-to-png, webp-to-png, webp-to-jpg, resize-image, compress-image）；修复 self-link、语言镜像页 `../../` 深度错误（原本链到 EN 页）、补齐 webp-to-jpg 反向链接。
- [x] **站点卫生**：sitemap 白名单补 webp-to-jpg + instagram-image-splitter 并重新生成（313 → 460 URLs，seo/ 同步根）；robots.txt 移除指向 privacy-policy.html 的无效 Sitemap 行（根 + seo/）；补根路径 llms.txt 与 mcp.json（原 404）；Makefile lint-root-files 白名单加入 llms.txt/mcp.json。
- [x] **修复 9 个工具页 commit 冲突标记损坏**：7d75d5b 误提交未解决冲突标记（`<<<<<<< Updated upstream`）到 fast-convert / instagram-image-splitter / webp-to-avif / jpg-to-avif / png-to-avif / raw-to-*，已恢复为损坏前内容并统一 title/og:title。
- [x] **提交**：`d48d615` feat(webp-to-jpg) · `59fe41c` fix(pages) 冲突修复 · `bdfef48` fix(seo) CTR 标题 · `2014aac` fix(seo) 内链规范化 · `d027531` chore(seo) 站点卫生

### 2026-07-28 — avif-to-png 页面 merge 冲突修复 + CTR 优化
- [x] **修复 avif-to-png/index.html P0 级结构损坏**：文件被提交时含有未解决的 git merge 冲突标记（`<<<<<<<`/`=======`/`>>>>>>>`），导致双重 `<html>`、`<title>`、OG 标签，Google 无法正确解析。已解决冲突保留版本 B（关键词前置的 title），删除版本 A + 冲突标记共 651 行。
- [x] **优化 title/meta/OG 提升 CTR**：title 从 `AVIF to PNG - Free Online AVIF to PNG Converter | PicEte`（56c, 关键词重复）改为 `AVIF to PNG Converter - Free, No Upload, Private | PicEte`（57c），og:title/og:description 与 title/description 对齐。
|- [x] **提交**: `17c837c fix(seo): resolve avif-to-png merge conflict, optimize title/OG for CTR`
|- [x] **SPEC**: `specs/picete-avif-to-png-fix-spec.md`

### 2026-07-28 — PNG 压缩优化 Phase 0 (Task 0): 量化能力验证环境搭建
|- [x] **Task 0 — 生成测试 PNG + 验证页面**: 创建 4 张测试 PNG（渐变图 320×240/1920×1080、纯白/纯红 100×100），创建独立验证页面 `docs/reports/png-palette-verify.html`，含三项测试（colours 硬编码/Q-only 自动色数/keep=0 元数据剥离）和环境检测（SAB/crossOriginIsolated）。验证使用 `newFromBuffer` + `newFromSource` 浏览器 API 模式，含 try/finally 内存清理。
|- [x] **Phase 0 (手动)**: 浏览器验证 palette 量化可用，产出验证报告。
|- [x] **Phase 0.1**: Web Worker 架构层 (`js/vips-worker.js`) ✅
|- [x] **Phase 0.2**: PNG 压缩参数注入 + 自适应 Dither + 熔断机制 (`compress-image/index.html`) ✅
|- [x] **Phase 1**: 长尾目标大小页同步 (50/100/200/500KB) ✅
|- [x] **Phase 2**: FAQ 修正 + 压缩报告 UI ✅
