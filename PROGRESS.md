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

### 设计与体验
- [x] 统一设计系统 + 响应式改进 + 跨工具一致性（2026-05-29）
- [x] 深色模式（深靛蓝黑色背景，暖色文本，logo 适配）
- [x] 语言选择器：用户选择而非自动重定向（SEO 友好）
- [x] AI 集成：MCP 指南页面 + 首页 AI 介绍区块
- [x] AI Toolz Dir 外链（独立 footer 行）

---

## 待办

### 高优先级
- [ ] **mcp-guide 多语言**：目前只有 EN 版本

### 中等优先级
- [ ] **工具交互测试**：验证所有 37 个工具在 Vercel 生产环境下的实际功能
- [ ] **SEO 插件集成**：当前无 analytics/Cookie 同意等
- [ ] **OG 图片**：检查各语言页面的 OG meta 标签是否指向正确的语言对应图片
- [ ] **性能优化**：检查大规模工具（extract-colors）的 client-side 性能

### 低优先级
- [ ] **FAQ 翻译报告**：docs/reports/ 中存在 untranslated_faqs_report.json，需检查是否已修复
- [ ] **README 更新**：反映新目录结构
- [ ] **测试计划**：docs/reports/TEST-PLAN.md 需要更新

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
| 工具总数 (EN) | 37 |
| 翻译语言 | 7 (zh/ja/de/fr/es/pt/ar) |
| 翻译页面数 | 266 |
| 总页面数 | 306 |
| Sitemap URL 数 | 313 |
| Git 提交数 | 73 |
