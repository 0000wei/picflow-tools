# PicEte Phase 0.6: 项目收尾与质量提升计划

## 说明

Phase 0.5（RAW+AVIF 支持）95 个 Task 全部完成，$ make verify$ 全通过。
以下是在 PROGRESS.md"其他待办"中记录的遗留项，经重新审计后的实际状态和执行计划。

---

## 待办审计结果

| # | 原待办 | 审计结果 | 实际状态 |
|---|--------|---------|---------|
| 1 | GA 自托管 | js/gtag.js 已存在（542KB），所有英文首页/工具页/多语言页引用 `/js/gtag.js`，无 googletagmanager.com 外部引用 | ✅ **已完成**（标记过时，应从待办移除） |
| 2 | SEO 插件集成 | seo/ 目录已有 sitemap.xml / robots.txt / llms.txt / favicon.ico/svg。无 analytics/Cookie 同意弹窗 | ⏳ 功能需求，非 Bug |
| 3 | OG 图片 | 所有语言首页的 og:image 都指向 `https://picete.com/images/og-image.png`——同一张图片，未按语言区分 | ⏳ 可优化项 |
| 4 | 性能优化 extract-colors | extract-colors 页面 863 行，当前用 Canvas getImageData 实现，无 wasm-vips 替换（Phase 0.2.5 决策保留 Canvas） | ✅ **已决策**（标记过时） |
| 5 | FAQ 翻译报告 | `docs/reports/` 下无 `untranslated_faqs_report.json` 文件 | ⏳ 文件不存在，需确认是否仍需 |
| 6 | README 更新 | README 描述了旧版功能（PNG↔JPG、WebP 等），未包含 AVIF 和 RAW 工具 | ⏳ 需要更新 |

**结论：** 6 项待办中 2 项已完成/过时，4 项需处理。

---

## Plan 0.6: 项目收尾与质量提升（4 Task）

### Task 0.6.1: PROGRESS.md 清理 + 统计更新 ⭐ 优先执行

**目标：** 移走过时的待办项，更新项目统计数据。

**委托内容：**
- 移走"GA 自托管"待办（已完成）
- 移走"性能优化 extract-colors"待办（已决策）
- 更新统计数据：
  - Sitemap URL 数：329 → 393
  - 工具总数 (EN)：40
  - 翻译页面数：280
  - 总页面数：393
  - Git 提交数：更新到当前

**验证：** `make verify` 通过

**预计耗时：** 10 分钟

---

### Task 0.6.2: 更新 README

**目标：** README 反映当前项目状态。

**委托内容：**
- 更新 features 列表，增加：
  - AVIF 工具集（avif-to-png、png-to-avif、jpg-to-avif、webp-to-avif）
  - RAW 工具集（raw-to-jpg、raw-to-png、raw-to-webp、raw-to-avif）
- 更新工具总数（40 EN 工具）
- 增加"多语言"章节（7 种语言）
- 更新 tech stack 章节（wasm-vips + libraw）

**不做的：**
- 不修改 AGENTS.md / STRUCTURE-RULES.md
- 不修改目录结构

**验证：** `cat README.md` 包含 RAW/AVIF 工具名

**预计耗时：** 5 分钟

---

### Task 0.6.3: OG 图片国际化检查

**目标：** 确认多语言页面的 OG meta 标签是否需要语言特定的 OG 图片。

**委托内容：**
- 检查 8 个首页（en + zh/ja/de/fr/es/pt/ar）的 og:image URL
- 当前所有语言使用同一张 og-image.png
- 评估是否需要为各语言定制 OG 图片（推荐用同一张——Facebook/Twitter 等平台不翻译图片文本，og-image.png 仅含 PicEte logo + 品牌名，不需要多语言版）
- 如需定制，生成方案

**验证：** OG 图片决策文档或确认不用改

**预计耗时：** 5 分钟

---

### Task 0.6.4: Cookie 同意弹窗

**目标：** 增加 GDPR 兼容的 Cookie 同意（语言自适应）。

**委托内容：**
- 创建 `js/cookie-consent.js`（轻量级内联实现，无外部依赖）
- 添加 Cookie 同意弹窗 HTML 到所有 8 个首页
- 弹窗文本使用对应语言
- 记录用户选择（localStorage）
- Google Analytics（gtag.js）仅在用户同意后加载

**注意：** 当前所有页面已直接引用 `/js/gtag.js`——如果添加 cookie 同意功能，需要：
1. 从 html `<head>` 移除非必要的 gtag.js 加载
2. 改为用户同意后才动态加载

**验证：** 打开首页可见 Cookie 弹窗，点击同意后 gtag 启动

**预计耗时：** 20 分钟

---

## 执行顺序

| 顺序 | Task | 说明 |
|------|------|------|
| **1** ⭐ | **0.6.1 PROGRESS 清理** | 文档准确性最优先——清理过时项、更新统计 |
| 2 | 0.6.2 README 更新 | 快赢 |
| 3 | 0.6.3 OG 图片检查 | 评估即可 |
| 4 | 0.6.4 Cookie 同意 | 最耗时但合规必要 |

---

*计划文档位置: `picete/docs/plans/PHASE-0.6-REMAINING.md`*
