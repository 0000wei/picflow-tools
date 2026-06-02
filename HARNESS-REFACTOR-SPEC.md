# PicEte 项目重构方案

用 Harness Engineering 的方法论来重构 PicEte 项目本身的结构。
不是把课程内容搬进网站，而是用这套工程方法让项目变规范。

---

## 一、问题诊断

### 根目录乱象

```
picete/ (根目录)
├── 42 个工具目录          ← 和项目文件混在一起
├── zh/ ja/ de/ fr/ es/ pt/ ar/  ← 8 个语言目录
├── 45 个散落的文件        ← *.py *.md *.html *.js *.json *.txt *.sh *.ico
├── css/ js/ images/       ← 资源目录
├── 06项目/               ← 错放了兄弟项目
├── __pycache__/           ← Python 缓存（不应被版本控制）
└── .git/
```

### 五大问题

1. **目录结构无分层** — 42 个工具目录 + 8 个语言目录 + 45 个零散文件全部在根目录，没有任何子目录来区分"什么是什么"
2. **临时/分析脚本和线上文件混在一起** — `audit_ar_pages.py`、`fix_untranslated_faqs.py`、`comprehensive_scan.py` 这些临时分析脚本和 `index.html`、`compress-image/index.html` 这些线上文件没有任何隔离
3. **SPEC 文件和线上文件混在一起** — `picete-longtail-v2-SPEC.md`、`ar-batch-convert-SPEC.md` 这些计划性文档和 `vercel.json`、`sitemap.xml` 混在一起
4. **跨项目污染** — `06项目/` 目录（mockupshot、screenprintfilter）错放在 picete 仓库下，不属于这里
5. **无废弃文件清理** — `launch-copy.html`、`og-render.html`、`prompt.md` 等明显是历史遗留，不知道还能不能删

---

## 二、重构方案

### 2.1 目标结构

```
picete/
├── src/                          # 网站代码
│   ├── en/                       # 英文工具页（现根目录工具）
│   │   ├── index.html
│   │   ├── resize-image/
│   │   ├── compress-image/
│   │   ├── png-to-jpg/
│   │   ├── ...（42 个工具）
│   │   └── privacy-policy.html
│   ├── zh/ ja/ de/ fr/ es/ pt/ ar/  # 多语言
│   ├── css/
│   └── js/
│
├── docs/                         # 项目文档
│   ├── specs/                    # 所有的 SPEC / 计划文档
│   │   ├── picete-longtail-v2-SPEC.md
│   │   ├── picete-zh-translation-SPEC.md
│   │   └── ...
│   ├── reports/                  # 项目报告、分析产出
│   │   ├── full-test-report.html
│   │   └── verification_report.txt
│   └── archive/                  # 历史文件，确定不再需要但保留
│       ├── prompt.md
│       ├── launch-copy.html
│       └── ...
│
├── scripts/                      # 工具/分析脚本
│   ├── audit/
│   │   ├── audit_ar_pages.py
│   │   ├── check_english_sentences.py
│   │   └── scan_faqs.py
│   ├── fix/
│   │   ├── fix_untranslated_faqs.py
│   │   ├── fix_faq_translation_gaps.py
│   │   └── fix-dark-langswitcher.py
│   ├── og/
│   │   └── generate-og.py
│   └── legacy/                   # 一次性的、不会再用的脚本
│       ├── comprehensive_scan.py
│       ├── final_report.py
│       └── ...
│
├── config/                       # 配置和部署文件
│   ├── vercel.json
│   └── mcp.json
│
├── seo/                          # SEO 相关
│   ├── sitemap.xml
│   ├── robots.txt
│   ├── llms.txt
│   └── favicon.ico
│
├── .gitignore                    # __pycache__/ 不应存在
├── README.md
└── HARNNESS-RULES.md             # 本项目的结构规范
```

### 2.2 清理步骤

**Step 1: 移出跨项目污染**
- `06项目/mockupshot/` → 属于 `/home/wu/桌面/knowledge-base/06项目/哥飞建站/mockupshot/`
- `06项目/screenprintfilter/` → 属于对应的项目目录

**Step 2: 创建 src/en/ 把英文工具页移入**
- 根目录下的 `resize-image/`、`compress-image/`、`png-to-jpg/` 等 42 个工具目录
- 根目录下的 `index.html`
- 根目录下的 `privacy-policy.html`

**Step 3: 创建 docs/ 分类归档**
- `specs/` — 所有 `*SPEC*.md`、`*plan*.txt` 文件
- `reports/` — 所有 `*report*.html`、`*report*.txt` 文件
- `archive/` — `launch-copy.html`、`og-render.html`、`prompt.md` 等不确定是否需要但先保留的历史文件

**Step 4: 创建 scripts/ 分类归档**
- `audit/` — 扫描/审计脚本
- `fix/` — 修复脚本
- `og/` — OG 图片生成
- `legacy/` — 一次性脚本

**Step 5: 创建 config/ + seo/**
- `config/` — vercel.json、mcp.json
- `seo/` — sitemap.xml、robots.txt、llms.txt、favicon.ico

**Step 6: 更新 .gitignore**
- 添加 `__pycache__/`
- 添加 `.well-known/`

### 2.3 结构规范（写入 HARNNESS-RULES.md）

```markdown
# PicEte 项目结构规范

## 目录职责

| 目录 | 用途 | 规则 |
|------|------|------|
| src/en/ | 英文网站文件 | 每个工具一个子目录，含 index.html |
| src/zh/ (等) | 多语言翻译 | 目录结构与 src/en/ 镜像 |
| src/css/ | 全局样式 | style.css |
| src/js/ | 全局 JS | 仅共享脚本 |
| docs/ | 项目文档 | 不含任何线上文件 |
| scripts/ | 工具脚本 | 不含 SPEC / 报告 |
| config/ | 部署配置 | vercel.json、mcp.json |
| seo/ | SEO 文件 | sitemap.xml、robots.txt |

## 规则

1. 根目录不允许放文件（仅允许 README.md 和本规范）
2. 所有新工具页建在 src/en/ 下
3. 所有 SPEC / 计划文档放 docs/specs/
4. 所有脚本放 scripts/，按用途分 audit/fix/og/legacy
5. 不允许在网站目录中放 Python 脚本
6. `__pycache__/` 必须 gitignore
7. 不再需要的文件先移 archive/，确认后删除
```
