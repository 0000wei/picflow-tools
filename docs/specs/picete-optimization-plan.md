# PicEte (picete.com) 流量优化实施计划 — v7

> 基于 Harness Engineering (ISVSL) 框架重构。
> 基于调研报告 `/home/wu/桌面/knowledge-base/06项目/哥飞建站/picete/docs/specs/网站流量优化系统调研.md` 提取需求。
> 每个 Feature 通过实际扫描确认精确需求，而非凭报告推测。
> 日期: 2026-06-02
> 当前基线: `make status` → 44 complete / 0 partial / 0 planned

---

## 重要发现：调研报告数据已部分过时

```
英文工具页 JSON-LD       实际: ✅ 全部完整（报告结论❌）
多语言首页 JSON-LD       实际: ✅ 全部完整（报告结论❌）
多语言工具页 JSON-LD     实际: ⚠️ 部分语言缺失（22页ZERO/6页PARTIAL）
hreflang 配置            实际: ⚠️ ar/全缺，zh/混合缺失
```

F3~F6 实际需求比报告描述的小得多。

---

## 当前 Harness 状态

```
子系统        状态  文件
───────────────────────────────────────────────
指令 (I)      ✅   AGENTS.md + STRUCTURE-RULES.md
状态 (S)      ✅   PROGRESS.md + feature_list.json (44 complete)
验证 (V)      ✅   Makefile (verify / lint / status)
范围 (Scope)  ✅   WIP=1 规则
生命周期 (L)  ✅   scripts/init.sh + 会话结束 checklist
```

---

## Feature List（v7）

### F1 ✅ 已完成 — sitemap + robots 部署到根目录
- `curl https://picete.com/sitemap.xml` → 200 ✅
- `curl https://picete.com/robots.txt` → 200 ✅

### F2 ✅ 已完成 — 更新 feature_list.json 和 PROGRESS.md
- feature_list.json: 44 complete, 0 partial, 0 planned ✅
- PROGRESS.md: 待办列表已更新 ✅

### F8 ✅ 已完成（用户已处理）— GSC 提交 sitemap

---

### F3 — 补全多语言工具页 JSON-LD

**来源**: 调研报告第五节：结构化数据深度植入（SoftwareApplication + BreadcrumbList Schema）

**精确需求**: 每个工具页需要 2 个 JSON-LD 块：WebApplication + BreadcrumbList。核心工具（compress-image, png-to-jpg 等 12 个）还需要 FAQPage（3块）。

**缺失清单**（`python3 scripts/audit/scan_missing_schema.py` 扫描结果）：

| 语言 | 类型 | 数量 | 具体工具 |
|------|------|------|---------|
| ar | ZERO JSON-LD | 8 | compress-image, extract-colors, image-to-base64, jpg-to-webp, png-to-webp, resize-image, resize-image-to-1080x1080, webp-to-png |
| ja | ZERO JSON-LD | 8 | png-to-webp-for-wordpress, resize-image-to-1080x1080, resize-image-to-1200x630, resize-image-to-1920x1080, resize-image-to-800x800, split-image-into-3x3, split-image-into-4-parts, webp-to-png-for-website |
| fr | ZERO JSON-LD | 6 | compress-image-to-100kb, image-to-base64, resize-image-to-1080x1080, resize-image-to-1200x630, resize-image-to-1920x1080, resize-image-to-800x800 |
| fr | PARTIAL (only WebApp) | 1 | extract-colors |
| zh | PARTIAL (only WebApp) | 4 | resize-image-for-facebook-cover, resize-image-to-200x200, resize-image-to-250x250, resize-image-to-728x90 |
| de | PARTIAL (only WebApp) | 1 | resize-image-to-250x250 |
| es/pt | — | 0 | ✅ 无缺失 |

**动作**: 从对应英文工具页提取 JSON-LD 模板（WebApplication + BreadcrumbList），注入到缺失的语言版本中。PARTIAL 的只补 BreadcrumbList。

**JSON-LD 模板参数**（以 compress-image 为例）：
```json
{
  "WebApplication": {
    "@type": "WebApplication",
    "name": "Image Compressor Tool",
    "description": "Free online image compressor tool",
    "url": "https://picete.com/compress-image",
    "applicationCategory": "MultimediaApplication",
    "operatingSystem": "Any",
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
  },
  "BreadcrumbList": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://picete.com/"},
      {"@type": "ListItem", "position": 2, "name": "Image Compressor", "item": "https://picete.com/compress-image/"}
    ]
  }
}
```

每个工具页应自定义：`name`, `description`, `url`, BreadcrumbList 第二项的 `name` 和 `item`。

**验证**: `python3 scripts/audit/scan_missing_schema.py` → exit code 0（所有语言所有工具页 JSON-LD >= 2 块）

**子步骤（WIP=1，一个语言一个语言地做）**:
```
ar (8页ZERO) → ja (8页ZERO) → fr (7页) → zh (4页PARTIAL) → de (1页PARTIAL)
```

每完成一个语言：
1. `python3 scripts/audit/scan_missing_schema.py` 确认该语言无缺失
2. `git add -A && git commit -m "feat: add JSON-LD to {lang} tool pages"`
3. `git push`
4. `make verify && make lint && make status`

---

### F5 — 补全 hreflang 标签（多语言工具页 + ar/首页）

**来源**: 调研报告：国际化 SEO — 每个页面需配置 hreflang，明确告知搜索引擎各语言版本映射关系

**精确需求**: 每个工具页需要在 `<head>` 中包含 10 条 `<link rel="alternate" hreflang="..." href="...">` 标签：
- 7 个语言: zh, ja, de, fr, es, pt, ar
- 1 个英文: en
- 2 个 x-default: en fallback

**实际扫描结果**:

| 范围 | hreflang 数量 | 状态 |
|------|-------------|------|
| 英文首页 (/) | 10条 | ✅ 完整 |
| zh/ja/de/fr/es/pt 首页 | 10条 | ✅ 完整 |
| ar/index.html | 0条 | ❌ **缺失** |
| 英文工具页 (compress-image) | 10条 | ✅ 完整 |
| ja/ 各工具页 | 10条 | ✅ 完整 |
| zh/ 各工具页 | 22页=9条, 15页=0条 | ❌ **缺失** |
| ar/ 各工具页 | 10页=0条 | ❌ **缺失** |

**缺失汇总**:
- ar/index.html: 0 条 hreflang
- ar/ 各工具页: 10 个与 JSON-LD 缺失高度重叠的页面，全部 0 条
- zh/ 各工具页: 15 个页面 0 条，22 个页面 9 条（缺 1 条 x-default，即 `<link rel="alternate" hreflang="x-default" href="https://picete.com/">`）

**动作**:
1. ar/index.html: 从任意完整首页复制 hreflang 块（比如 pt/index.html），替换语言代码
2. ar/ 缺失的工具页: 修复 JSON-LD 时一并补全 hreflang（两者缺失高度重叠）
3. zh/ 工具页:
   - 9 条的 22 页 + 0 条的 15 页：统一复制完整 10 条
   - 注意：0 条的 15 页中有部分是 JSON-LD PARTIAL 页面，hreflang 修复应与 JSON-LD 修复合并执行

**验证**: 每个修复后的页面 `grep -c 'hreflang' <path>` 应输出 10

---

### F6 — 首页图片懒加载

**来源**: 调研报告：Core Web Vitals 加载速度是排名因素

**精确需求**: 首页 `<head>` 部分有 2 个 `<img>` 标签：
1. `src="images/picete-logo.svg"` — header logo（第 97 行附近）
2. `src="images/picete-logo.svg"` — footer logo（第 565 行附近）

**动作**: 给这 2 个 `<img>` 标签加上 `loading="lazy"`

**验证**:
```bash
grep -c 'loading="lazy"' index.html  # 应输出 2
```

---

### F7 — 内部链接网络

**来源**: 调研报告：页面主题相关性串联，帮助搜索引擎爬虫发现全站页面

**需求 1 — 首页 footer "More Tools" 补充**:
首页 footer 有 4 个 section：
- Image Conversion（5个链接：png-to-jpg, jpg-to-png, webp-to-png, png-to-webp, jpg-to-webp）
- Image Editing（5个链接：resize-image, compress-image, image-splitter, extract-colors, image-to-base64）
- About（1个链接：privacy-policy）
- **More Tools（当前为空 `<ul></ul>`）**

**动作**: 在 More Tools section 补充剩余 29 个长尾工具的链接（分批，比如压缩长尾页 + 尺寸长尾页 + 其他）。如：
```html
<ul>
  <li><a href="compress-image-to-50kb/">Compress to 50KB</a></li>
  <li><a href="compress-image-to-100kb/">Compress to 100KB</a></li>
  ...
  <li><a href="resize-image-to-1080x1080/">Resize to 1080×1080</a></li>
  ...
</ul>
```

**验证**:
```bash
curl -s https://picete.com/ | grep -oP 'href="[^"]*/"' | sort -u | wc -l
```
应 > 当前数量（当前 footer 只链了 12 个工具）。

---

## 执行顺序

```
F3 (多语言JSON-LD) → F5 (hreflang) → F6 (懒加载) → F7 (内部链接)
```

### 合并建议
F3 和 F5 的缺失高度重叠（ar/ 的 JSON-LD 缺失和 hreflang 缺失是同一批页面）。建议：

1. **先 F3 ar (8页)**: 注入 JSON-LD + 同步补 hreflang（8页+首页）
2. **F3 ja (8页)**: 只注入 JSON-LD（hreflang 已完整）
3. **F3 fr (7页)**: 注入 JSON-LD + 补 hreflang（如果也需要）
4. **F3 zh (4页)**: 补 BreadcrumbList + hreflang（15页0条+22页9条）
5. **F3 de (1页)**: 补 BreadcrumbList + 检查 hreflang
6. **F6**: 2个loading="lazy"（5秒）
7. **F7**: More Tools 填链接

---

## 执行规则（基于 Harness Engineering）

### 1. WIP=1
一次只做**一个 Feature**。每个 Feature 内按语言逐个做，做一页验证一页。

### 2. 每次开工前
```bash
bash scripts/init.sh        # 健康检查
make status                 # 确认当前状态
```

### 3. 每次完成后
```bash
make verify                 # 项目完整性
make lint                   # 代码质量
python3 scripts/audit/scan_missing_schema.py  # JSON-LD 检查
# 然后 git add → commit → push
```

### 4. 验证 = 完成
每个 Feature 的证据必须是可重现的外部命令输出（curl、grep、make output、python3 扫描脚本）。

### 5. 更新 PROGRESS.md
每个 Feature 完成后更新 PROGRESS.md + feature_list.json。Status 升级只能通过验证命令通过来实现。
