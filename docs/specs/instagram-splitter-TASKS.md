# Instagram Image Splitter — Task 拆解

> 基于 PRD V2.1（`docs/specs/instagram-splitter-PRD.html`）拆解为可执行的 Task。
> 本文件遵循 Harness Engineering（I.S.V.S.L）五子系统规范进行审计和修复。

---

## 1. 启动流程 — Instructions / Lifecycle

**每次执行前必须完成以下初始化步骤（Hermes 执行）：**

```
[ ] 运行 scripts/init.sh
[ ] 读取 STRUCTURE-RULES.md — 了解目录结构、文件分类原则
[ ] 读取 PROGRESS.md — 了解当前项目进展
[ ] 读取 feature_list.json — 了解现有功能清单
[ ] git log（最近 10 条）— 了解近期变更节奏
[ ] 确认无其他 WIP 在进程中
```

---

## 2. WIP=1 规则

**一次只能执行一个 Task。** Task 0 完成后，标记 PROGRESS + commit，然后才能开始 Task 1。严格串行，严禁并行推进不同 Task。

**Task 5（翻译）例外**：翻译 7 种语言可以用 `delegate_task` 并行执行（每个语言是一个独立子代理，不共享状态），但必须等 Task 4 完成后才能启动。

---

## 3. 执行回路（每个 Task 都要遵循）

```
1. Hermes 编写委托上下文（含：文件路径、约束、不做的事、验证标准）
2. Hermes 将委托上下文提交给执行者（Claude Code / 自己执行）
3. 执行者完成工作
4. 【必须】Hermes 独立验证产出文件（读取文件确认、非功能性的浏览器检查）
5. 验证通过 → 更新 PROGRESS.md（0延迟）→ git add + commit
6. 验证不通过 → 记录具体不符项 → 修正委托上下文 → 重新委托
```

---

## 4. Task 列表

| Task | 名称 | 依赖 | 执行者 | 验证方式 |
|------|------|------|--------|----------|
| 0 | 基础设施目录创建 | — | Hermes 直接执行 | 确认目录存在 |
| 1 | HTML 英文主页面 | Task 0 | Claude Code | Hermes 读取文件 + 浏览器打开检查骨架完整性 |
| 2 | JS 核心引擎 | Task 0 | Claude Code | Hermes 读取文件检查函数接口 + 语法检查 |
| 3 | 裁剪框交互组件 | Task 2 | Claude Code | Hermes 读取文件检查事件监听完整性 |
| 4 | ZIP 导出 + 移动端降级 | Task 2, 3 | Claude Code | Hermes 浏览器实操：上传图片→切割→下载 ZIP→解压检查命名和顺序 |
| 5 | 翻译 7 种语言 | Task 1, 4 | Claude Code × 7 并行 | Hermes 逐个打开翻译页面检查 hreflang + UI 文案 |
| 6 | vercel.json + Navbar 集成 | Task 1 | Hermes 直接执行 | 确认 vercel.json 内容 + 首页 Navbar 出现新链接 |
| 7 | 终验（End-to-End） | Task 0-6 全部完成 | Hermes 直接执行 | 逐一回归所有 AC，编写 TEST_REPORT.md |

---

## 5. Task 详细定义

---

### Task 0：基础设施目录创建

**执行者：** Hermes

**上下文加载：** 执行前先完成第 1 节的启动流程

**内容：**
1. 创建目录 `instagram-image-splitter/`
2. 在各语言目录下创建 `zh/instagram-image-splitter/`、`ja/...`、`de/...`、`fr/...`、`es/...`、`pt/...`、`ar/...`
3. 确认 `assets/js/tools/` 目录存在（如不存在则创建）
4. 确认 vercel.json 当前内容

**验证：** 所有目录创建完成后，`ls -d */instagram-image-splitter/` 确认 8 个目录存在

**完成后：** 更新 PROGRESS.md 的 Task 0 行 → `git add . && git commit -m "chore: init instagram-image-splitter directories"`

---

### Task 1：HTML 英文主页面

**执行者：** Claude Code

**文件路径：** `instagram-image-splitter/index.html`

**执行前 Hermes 准备工作：**
1. 先读取 `image-splitter/index.html` 的前 200 行，确认骨架结构的实际代码
2. 将确认后的骨架要点写入委托上下文

**委托上下文：**

在 `instagram-image-splitter/index.html` 创建一个 Instagram 全景图与网格切图工具页面。

**⚠️ 先读：** 请先读取 `/image-splitter/index.html` 的完整 `<head>` 和 `<body>` 开头部分（前 300行），然后严格按该骨架结构创建新页面。不要靠记忆——打开文件看实际代码。

**必须继承的骨架要素（从 `image-splitter/index.html` 读）：**
1. DOCTYPE + `<html lang="en">` + viewport meta
2. Google Analytics (`/js/gtag.js` + G-H72N80TEBW)
3. Canonical: `https://picete.com/instagram-image-splitter/`
4. hreflang 标签：en, zh, ja, de, fr, es, pt, ar（各8个），含 x-default
5. Open Graph meta（og:type, og:url, og:title, og:description, og:image）
6. Schema.org WebApplication + BreadcrumbList JSON-LD
7. favicon.svg + favicon.ico（路径 `../favicon.svg` / `../favicon.ico`）
8. `<link href="../css/style.css" rel="stylesheet">`
9. Theme toggle（🌙/☀️）— data-theme="dark" 属性切换，.sun-icon / .moon-icon 显示逻辑
10. Language switcher — `<select>` 含 8 种语言，调用 `switchLanguage()`
11. Header + Nav + Footer（参考 image-splitter 的 header 结构）
12. FAQ 区块 + FAQPage JSON-LD structured data，至少 5 个 Q&A

**页面标题：** `Free Instagram Image Splitter & Panorama Cropper | PicEte`
**Meta description：** `Split images for Instagram carousel or profile grid online for free. Panorama slicer, 3x3 grid maker, 4:5 carousel cutter. 100% free, runs in browser.`
**H1：** `Free Instagram Image Splitter & Panorama Cropper`

**UI 布局（严格遵循）：**

桌面端左右分栏，移动端（≤768px）上下分栏。CSS 用 `@media (max-width: 768px)` 断点。

**左侧/上方控制面板：**
- 模式切换：两个按钮 `[Carousel]` 和 `[Grid]`，选中态高亮
- 选择 Carousel 时显示：
  - 切片数量：range input 2~10，绑定显示当前值
  - 比例选择：两个按钮 `[4:5]` 和 `[1:1]`
- 选择 Grid 时显示：
  - 行数选择：下拉框 `3×1`、`3×2`、`3×3`、`3×4`
- 操作按钮：`[重置裁剪框]`、`[下载 ZIP]`
- 移动端 ZIP 按钮下方：`<div id="individual-save">`（初始隐藏）和提示文案
- 降采样提示区域：`<div id="downsample-notice">`（初始隐藏）

**右侧/下方工作台（Canvas 区域）：**
- `<input type="file" accept="image/*" id="fileInput">` + drop zone
- `<canvas id="editorCanvas">`
- 图片加载后原图区域半透明暗色覆盖、裁剪框内正常亮度

**CSS 样式约束：**
- 切割线：`box-shadow: inset 0 0 0 1px rgba(255,255,255,0.8), inset 0 0 0 2px rgba(0,0,0,0.5)`
- 适配 dark/light 主题（CSS variables）
- 响应式：≥769px 分栏（grid/flex），≤768px 上下排

**SEO 内容模块：**
- 发布指南段落
- FAQ 区块（5 个以上 Q&A）

**⚠️ 禁止修改：** 全局 `css/style.css`、现有的 `js/` 全局脚本。不要引入外部 CDN（JSZip 会在 Task 4 引入）。

**⚠️ 不做的事：** 不写 JS 逻辑（`instagram-splitter.js` 在 Task 2 写）。HTML 中只放 UI 结构和调用占位（`onclick="IGSplitter.someMethod()"`）。

**验证：** Claude Code 完成后，Hermes 会读取文件确认骨架完整性，并在浏览器打开检查。

---

### Task 2：JavaScript 核心引擎

**执行者：** Claude Code

**文件路径：** `/assets/js/tools/instagram-splitter.js`

**⚠️ 先读：** 读取 `instagram-image-splitter/index.html` 中 Canvas 元素的 ID、control 按钮的 ID 和 onclick 定义，确保 JS 接口与 HTML 绑定一致。

**内容：**
创建 Instagram 切图工具的核心处理逻辑。纯 Canvas 操作，浏览器端运行。

**全局 API（暴露到 `window.IGSplitter`）：**
- `init(canvasId)` — 传入 Canvas 元素 ID，初始化 Canvas 上下文
- `loadImage(file)` — 传入 File 对象
- `setMode('carousel'|'grid')`
- `setSlices(n)` — 切片数 2-10
- `setAspect('4:5'|'1:1')` — 仅 Carousel 模式
- `setGridRows(n)` — 1/2/3/4 行（Grid 模式）
- `resetCropper()` — 重置裁剪框居中
- `exportZip()` — JSZip 打包下载
- `exportIndividual()` — 逐张保存视图

**关键技术规格：**

1. **loadImage()：**
   - 用 `URL.createObjectURL(file)` → new Image()
   - 检查最长边 > 4096px → 离屏 Canvas 降采样，设 `isDownsampled=true`
   - 图片 < 300×300 → return error string
   - 如果之前有旧 URL → `URL.revokeObjectURL()` 释放
   - 计算 `cropScaleX = originalWidth / displayWidth`
   - 初始化裁剪框（居中，以短边为基准自适应填充）
   - 调用 render()

2. **render()：**
   - 清空 Canvas
   - 绘制原图（半透明暗覆盖 rgba(0,0,0,0.5)）
   - 用 clearRect 在裁剪框区域"挖出"正常亮度
   - 绘制切割线（双层阴影 + 1px 实线）
   - 每块切片内绘制白色编号数字

3. **calculateCropBox()：**
   - Carousel 4:5 → 整体比例 `(4*N) : 5`
   - Carousel 1:1 → `N : 1`
   - Grid → `3 : gridRows`

4. **exportZip()：**
   - 遍历每张切片，从显示坐标裁剪，还原到原始坐标
   - `toDataURL('image/jpeg', 0.92)`
   - PNG 透明图→先 fillRect(#FFFFFF)
   - 命名：`picete-carousel-1.jpg` 或 `picete-grid-1.jpg`
   - Grid 模式：左上角=1，右下角=行数×3
   - JSZip → zip.generateAsync → 触发下载

5. **exportIndividual()：**
   - 每张切片生成 `<img>` → 追加到 `#individual-save` 区域

**边界条件：**
- 极端比例（10:1 panoroma）→ 裁剪框不超过图片边界
- 图片 < 300×300 → return 错误字符串
- 切片数变化 → 重新计算裁剪框

**验证：** Hermes 读取 `instagram-splitter.js` 文件，确认所有 API 函数存在，语法无错误。

---

### Task 3：裁剪框交互组件

**执行者：** Claude Code

**文件路径：** 追加到 `/assets/js/tools/instagram-splitter.js`

**⚠️ 先读：** 读取当前 `instagram-splitter.js` 末尾，确认 `window.IGSplitter` 已暴露的对象结构和 `render()` 函数签名。

**委托上下文：**

在 `IGSplitter` 对象内添加鼠标和触摸交互。

**事件监听（在 init() 中注册）：**
- mousedown / mousemove / mouseup（canvas 上）
- mouseleave（防卡住）
- touchstart / touchmove / touchend（{ passive: false }）

**拖拽平移：**
- 裁剪框内部按下 → 进入拖拽状态
- 裁剪框不超出图片边界
- cursor: grab → dragging

**四角缩放：**
- 每个角 8px 圆形 handle
- 拖拽时强制同比缩放
- 最小尺寸 50×50px
- 缩放后在图片边界内

**重置：** `resetCropper()` 居中复原

**验证：** Hermes 读取文件确认事件监听绑定正确、handle 绘制逻辑存在。

---

### Task 4：ZIP 导出 + 移动端降级视图

**执行者：** Claude Code

**文件路径：** 修改 `instagram-image-splitter/index.html` 和追加 `/assets/js/tools/instagram-splitter.js`

**⚠️ 先读：** 读取当前 `instagram-splitter/index.html` 的结构已有哪些按钮和区域，读取当前 `instagram-splitter.js` 末尾。

**委托上下文：**

**HTML 修改（index.html）：**
1. 在 `<head>` 末尾添加：`<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>`
2. 在 "下载 ZIP" 按钮下方增加：
   - `#individual-save` 区域（初始 display:none）
   - 提示文案 `<p id="mobile-hint">`（初始 display:none）

**JS 修改（instagram-splitter.js）：**
- `exportZip()`: loading 状态（禁用按钮+文字"打包中..."）→ JSZip 打包 → 触发下载 → 恢复按钮
- `exportIndividual()`: 遍历切片 → 创建 `<img>` → 追加到 `#individual-save`
- 移动端检测：`window.matchMedia('(max-width: 768px)')` → 显示 `#mobile-hint`

**验证标准（AC-2 & AC-3）：**
- ZIP 内文件命名 `picete-carousel-1.jpg`
- ZIP 无嵌套文件夹
- Grid 模式左上角=1，右下角=行数×3
- 768px 断点触发降级视图

---

### Task 5：翻译 8 种语言（每个语言一个独立的 delegate_task，串行执行）

**执行者：** Claude Code × 8（每个语言一个 delegate_task）

**语言列表：** zh, ja, ko, de, fr, es, pt, ar（共 8 种翻译语言 + 英文源文件不动）

**文件路径：** `[lang]/instagram-image-splitter/index.html`

**⚠️ 关键：**
- 每个 delegate_task **只翻译一种语言**。不要合并语言
- **串行执行**：完成一个语言的验证+commit 后，再开始下一个
- 执行顺序：zh → ja → ko → de → fr → es → pt → ar（ar 最后，因为需要 rtl 特殊处理）

**每个委托上下文的模板（每次调用时替换 `[LANG]` 和 `[LANG_NAME]`）：**

```
## 任务
基于英文源文件 `/instagram-image-splitter/index.html`，创建 [LANG_NAME] 翻译版本。

## ⚠️ 先读
读取 `instagram-image-splitter/index.html` 的完整内容。

## 输出文件
`[LANG]/instagram-image-splitter/index.html`

## 翻译规则
1. 所有 UI 文案、FAQ、SEO 内容区块全部翻译为 [LANG_NAME]
2. URL 路径：文件放在 `[LANG]/instagram-image-splitter/index.html`，路径结构照搬英文
3. `<html lang="[LANG]">`
4. Canonical：`https://picete.com/[LANG]/instagram-image-splitter/`
5. hreflang 标签保持完整 9 语言列表（en, zh, ja, ko, de, fr, es, pt, ar，含 x-default）
6. OG title / description 翻译
7. Schema.org JSON-LD 中的 name/description 翻译
8. FAQ JSON-LD 中的 Question/AcceptedAnswer 翻译
9. 页面内的 FAQ 区块（details/summary）文案同步翻译

## 特殊处理
- **ar（阿拉伯语）**：页面添加 `dir="rtl"` 属性
- **JS 逻辑不动**：不修改任何 JS 代码
- **CSS 不动**：不修改任何 CSS
- **HTML 结构不动**：只改文案和属性值（lang, canonical, hreflang, og:title/description 等）
- **hreflang 中的非当前语言条目不动**：不要改其他语言的 hreflang href 值

## ⚠️ 禁止
- 不改 JS 代码
- 不改 CSS
- 不改 HTML 结构（div 层级、class 名称、id 名称）
- 不改任何 hreflang 中其他语言的 href 值
```

**验证标准（每个语言翻译完成后 Hermes 检查）：**
- 页面打开后渲染正确，文案为对应语言
- Language switcher 中当前语言高亮可切换
- Theme toggle 正常工作
- Canonical URL 指向正确的语言路径
- hreflang 标签完整（9 种 + x-default）
- ar 页面有 `dir="rtl"`
- JS 功能不受影响（onclick、Canvas 等仍在）

---

### Task 6：vercel.json + Navbar 集成

**执行者：** Hermes

**⚠️ 先读：** 读取当前 `vercel.json` 和首页 `index.html`（Navbar 部分）

**vercel.json 修改：**
1. 在 `headers` 数组的 COEP/COOP 规则中添加 `instagram-image-splitter` 路径（参考 `image-splitter` 的模式）
2. 如果 PicEte 有 SPA rewrite fallback 机制，确保新工具路径正确

**Navbar 集成：**
在首页的 "Social Media Tools" 下拉菜单中添加 `<a href="/instagram-image-splitter/">Instagram Image Splitter</a>`

**验证：** 确认 `vercel.json` 格式正确（`python3 -c "import json; json.load(open('vercel.json'))"`），Navbar 链接存在。

---

### Task 7：终验（End-to-End Verification）

**执行者：** Hermes

**内容：** 验证所有 AC + 集成检查。

**AC 回归验证：**

| AC | 验证方式 | 结果 |
|----|----------|------|
| AC-1 宽高比精度 | 浏览器打开 → 上传图片 → Carousel 4:5×4片 → 浏览器 Console 量取 Canvas 选框宽高比是否 = 16:5（误差≤1px） | [ ] |
| AC-2 ZIP 命名/顺序 | 浏览器操作 → 下载 ZIP → 解压检查文件命名 | [ ] |
| AC-3 移动端降级 | DevTools 切 768px 以下 → 检查逐张保存视图出现 | [ ] |
| AC-4 切割完整性 | 导出图片拼接还原 → 与原图裁剪框区域像素级对比 | [ ] |
| AC-5 网格正方形 | Grid 3×3 → 导出图片每张量宽高比是否 1:1（误差≤1px） | [ ] |
| AC-6 单张 ≤ 800KB | 导出图片检查文件大小 | [ ] |

**集成检查：**
- [ ] 首页 Navbar 出现 Instagram Image Splitter 链接
- [ ] 链接点击后跳转到 `/instagram-image-splitter/` 并正常渲染
- [ ] Theme toggle 在 Dark/Light 下都正常工作
- [ ] Language switcher 切换语言后跳转到正确翻译页面
- [ ] ar 页面 RTL 布局正常
- [ ] 8 种语言页面全部可访问，无 404

**产出：** `docs/reports/instagram-splitter-TEST-REPORT.md`

**完成后：** 更新 PROGRESS.md（标记所有 Task 完成）→ 更新 feature_list.json → `git add . && git commit -m "feat: instagram image splitter tool"` → `git push`

---

## 6. 会话结束清理

终验完成后执行：
```
[ ] git status — 检查未跟踪/未暂存文件
[ ] git add + git commit — 提交所有工作（含 PROGRESS.md 更新）
[ ] git push — 推送至远程
[ ] 检查根目录整洁：无临时文件
[ ] 确认 AGENTS.md / STRUCTURE-RULES.md / vercel.json 未被误改
```

---

## 7. Harness 审计对照表

| 子系统 | 违规 | 修复措施 |
|--------|------|----------|
| Instructions | 缺少先读源文件指令 | Task 1-6 统一加 "⚠️ 先读" 步骤 |
| Instructions | 缺少 AGENTS.md 初始化 | 第 1 节启动流程 |
| State | 缺少 PROGRESS.md 更新 | 每 Task 结束步骤包含 PROGRESS 更新 |
| State | 缺少 git checkpoint | 每 Task 结束步骤包含 git add + commit |
| State | 缺少 feature_list.json 更新 | Task 7 终验包含 feature_list 更新 |
| Verification | 缺少 Hermes 独立验证 | 第 3 节执行回路 + 每 Task 独立验证方式 |
| Verification | 缺少端到端终验 | 新增 Task 7 |
| Scope | 缺少 WIP=1 声明 | 第 2 节 WIP=1 规则 |
| Lifecycle | 缺少会话初始化 | 第 1 节启动流程 |
| Lifecycle | 缺少会话结束清理 | 第 6 节清理清单 |
