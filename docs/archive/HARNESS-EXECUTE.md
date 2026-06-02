# PicEte 项目重构 — Claude Code 执行指令

## 原则

1. **不动线上 URL 路径** — 英文工具目录（resize-image/、compress-image/ 等）保持在根目录
2. **只做分类整理和移动** — 不修改任何 index.html 内部内容
3. **用 git mv 进行所有移动** — 保留文件历史

## 执行步骤

### Step 1: 删除跨项目污染

删除 `06项目/` 目录（它不属于 picete 仓库）：

```bash
git rm -r 06项目/
```

### Step 2: 创建目标目录结构

```bash
mkdir -p docs/specs docs/reports docs/archive
mkdir -p scripts/audit scripts/fix scripts/og scripts/legacy
mkdir -p config seo
```

### Step 3: 移动 SPEC / 计划文档到 docs/specs/

```bash
git mv ar-batch-convert-SPEC.md docs/specs/
git mv picete-ar-translation-SPEC.md docs/specs/
git mv picete-zh-translation-SPEC.md docs/specs/
git mv picete-longtail-v2-SPEC.md docs/specs/
git mv pt-resize-facebook-cover-SPEC.md docs/specs/
git mv longtail-plan.txt docs/specs/
```

### Step 4: 移动报告/测试产出到 docs/reports/

```bash
git mv full-test-report.html docs/reports/
git mv verification_report.txt docs/reports/
git mv untranslated_faqs_report.json docs/reports/
git mv TEST-PLAN.md docs/reports/
git mv PROJECT-OVERVIEW.html docs/reports/
git mv submit-to-directories.html docs/reports/
```

### Step 5: 移动历史文件到 docs/archive/

```bash
git mv launch-copy.html docs/archive/
git mv og-render.html docs/archive/
git mv prompt.md docs/archive/
git mv screenprint-filter-spec.md docs/archive/
```

### Step 6: 移动脚本到 scripts/ 分类

审计/扫描类：
```bash
git mv audit_ar_pages.py scripts/audit/
git mv check_english_sentences.py scripts/audit/
git mv comprehensive_scan.py scripts/audit/
git mv extract_unique_faqs.py scripts/audit/
git mv get_exact_paths.py scripts/audit/
git mv scan_faqs.py scripts/audit/
git mv scan_untranslated_faqs.py scripts/audit/
git mv scan_faqs_simple.sh scripts/audit/
git mv verify_site_translations.py scripts/audit/
```

修复类：
```bash
git mv fix_faq_translation_gaps.py scripts/fix/
git mv fix_remaining_faqs.py scripts/fix/
git mv fix_untranslated_faqs.py scripts/fix/
git mv fix-dark-langswitcher.py scripts/fix/
git mv picete-lang-redirect-fix.js scripts/fix/
```

OG 生成：
```bash
git mv generate-og.py scripts/og/
git mv generate-og.js scripts/og/
```

一次性/遗留脚本：
```bash
git mv final_report.py scripts/legacy/
git mv precise_report.py scripts/legacy/
```

### Step 7: 移动配置文件到 config/

```bash
git mv vercel.json config/
git mv mcp.json config/
```

### Step 8: 移动 SEO 文件到 seo/

```bash
git mv sitemap.xml seo/
git mv robots.txt seo/
git mv llms.txt seo/
git mv favicon.ico seo/
```

### Step 9: 清理零散文件

```bash
git rm AI-MEMORY.md
```

### Step 10: 更新 .gitignore

在 `.gitignore` 中添加：

```
__pycache__/
.well-known/
```

### Step 11: 创建项目结构规范文件

创建 `STRUCTURE-RULES.md` 文件，内容如下——这就是项目的"Harness 地图"：

```markdown
# PicEte 项目结构规范

## 目录职责

| 目录 | 用途 | 规则 |
|------|------|------|
| 工具目录 | 英文网站页面 | 每个工具一个子目录，保持在根目录 |
| zh/ ja/ de/ fr/ es/ pt/ ar/ | 多语言翻译 | 目录结构与英文工具镜像 |
| css/ | 全局样式 | style.css |
| js/ | 全局 JS | 仅共享脚本 |
| docs/specs/ | 项目计划和 SPEC | 所有 *SPEC*.md、*plan*.txt |
| docs/reports/ | 项目报告和分析产出 | *report*.*, TEST-PLAN.md |
| docs/archive/ | 历史文件 | 确认不再需要的遗留文件 |
| scripts/audit/ | 审计/扫描脚本 | scan_*.py, audit_*.py, check_*.py |
| scripts/fix/ | 修复脚本 | fix_*.py, fix_*.js |
| scripts/og/ | OG 图片生成 | generate-og.* |
| scripts/legacy/ | 一次性脚本 | 不会再运行的 legacy 脚本 |
| config/ | 部署配置 | vercel.json, mcp.json |
| seo/ | SEO 文件 | sitemap.xml, robots.txt, llms.txt, favicon.ico |

## 规则

1. 根目录仅允许: README.md, STRUCTURE-RULES.md, .gitignore, vercel.json
2. 所有新工具页建在根目录（保持当前模式）
3. 所有 SPEC / 计划文档放 docs/specs/
4. 所有脚本放 scripts/，按用途分 audit/fix/og/legacy
5. 不允许在根目录放 Python 脚本或散落文件
6. `__pycache__/` 和 `.well-known/` 必须被 gitignore
7. 不再需要的文件先移 docs/archive/，确认后再删除

## 添加新工具

1. 在根目录创建 `<tool-name>/index.html`
2. 在 docs/specs/ 添加对应的 SPEC
3. 在各语言目录创建对翻译页面
4. 更新 seo/sitemap.xml
```

### Step 12: 提交

```bash
git add -A
git commit -m "refactor: 按 Harness Engineering 重构项目结构

- 删除 06项目/ 目录（跨项目污染，不属于本仓库）
- 创建 docs/specs/ docs/reports/ docs/archive/ 归档文档
- 创建 scripts/audit/ scripts/fix/ scripts/og/ scripts/legacy/ 分类脚本
- 创建 config/ seo/ 分离配置和 SEO 文件
- 更新 .gitignore (__pycache__/ .well-known/)
- 添加 STRUCTURE-RULES.md 作为项目结构规范
- 移除 AI-MEMORY.md（内容已在记忆系统中）

根目录从 45+ 散落文件减少到 3 个核心文件。"
```
