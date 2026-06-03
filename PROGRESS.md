# PicEte 项目进度

## 项目概述
PicEte 是一个在线图片处理工具站（picete.com），提供 37 个图片处理工具，支持 8 种语言（EN/ZH/JA/DE/FR/ES/PT/AR），部署在 Vercel 上。

---

## 已完成

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
|- [x] **0.5.0** GA 自托管 — 下载 gtag.js 到 js/，所有 106 个 HTML 改为同源引用 (b24b0c5)
|- [ ] 0.5.1 创建 avif-to-png 工具页
|- [ ] 0.5.2 创建 png-to-avif 工具页
|- [ ] 0.5.3 创建 jpg-to-avif 工具页
|- [ ] 0.5.4 创建 webp-to-avif 工具页
|- [ ] 0.5.5a zh 翻译（标杆）
|- [ ] 0.5.5b ja 翻译（串行）
|- [ ] 0.5.5c de 翻译（串行）
|- [ ] 0.5.5d fr 翻译（串行）
|- [ ] 0.5.5e es 翻译（串行）
|- [ ] 0.5.5f pt 翻译（串行）
|- [ ] 0.5.5g ar 翻译（RTL 处理，串行）
|- [ ] 0.5.6 首页入口链接更新 — 8 首页 + footer 增加 AVIF 工具入口
|- [ ] 0.5.7 更新 sitemap + feature_list

### 其他待办
- [ ] **GA 自托管**：COEP require-corp 会阻塞 googletagmanager.com，需下载 gtag.js 到本地 /js/ 目录并改为同源引用
- [ ] **SEO 插件集成**：当前无 analytics/Cookie 同意等
- [ ] **OG 图片**：检查各语言页面的 OG meta 标签是否指向正确的语言对应图片
- [ ] **性能优化**：检查大规模工具（extract-colors）的 client-side 性能
- [ ] **FAQ 翻译报告**：docs/reports/ 中存在 untranslated_faqs_report.json，需检查是否已修复
- [ ] **README 更新**：反映新目录结构

---

## 已知问题

1. **Git 历史**：72 次提交，仅 master 分支，无 tag
2. **跨站点链接**：之前存在跨站点 footer 链接（已于 2026-05-25 移除，遵循哥飞 SEO 指导）
3. **语言切换器**：历史上有浏览器自动重定向问题（2026-05-26 修复为用户选择模式）
4. **测试覆盖率**：脚本目录下有一些审计/修复脚本，但缺少自动化集成测试
5. **等待用户确认后 commit 的 SPEC 文档**：docs/specs/PICETE-OPTIMIZATION-PLAN-V2.md + docs/specs/PICETE-ROADMAP.md

---

## 统计数据

| 指标 | 数值 |
|------|------|
| 工具总数 (EN) | 40 |
| 翻译语言 | 7 (zh/ja/de/fr/es/pt/ar) |
| 翻译页面数 | 280 |
| 总页面数 | 329 |
| Sitemap URL 数 | 329 |
| Git 提交数 | 76 |
