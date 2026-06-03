# PicEte 专项优化计划 — 完整 SPEC + 执行计划 V2.2

## 执行顺序

```
P5 (测试闭环) → P1 (mcp-guide翻译) → P0 (wasm-vips) → P0.5 (AVIF+RAW)
```

## 分解原则

- 每个 Task = 子代理 2-5 分钟的聚焦工作
- Task 文件操作互不重叠（不碰同一文件）
- 以"可独立验证"为粒度边界

---

# P5: 工具测试闭环

## Task 5.1: 安装 Playwright

**委托内容：**
- `cd picete/ && npm init -y && npm install playwright`
- `npx playwright install chromium`

**验证：** `npx playwright --version` 正常

---

## Task 5.2: 生成 3 张测试图片

**委托内容：**
- 创建 `scripts/test/fixtures/` 目录
- 生成 3 张合法测试图片：
  - `test-photo.jpg`：用 Node.js 的 canvas 包或 sharp 生成一张 800×600 纯色 JPG（~200KB）
  - `test-logo.png`：生成 400×400 带透明 PNG（~100KB）
  - `test-webp.webp`：生成一张 WebP（~100KB）

**约束：** 图片文件必须可正常显示，不依赖网络下载

**验证：** `file scripts/test/fixtures/*` 识别 3 种不同格式

---

## Task 5.3: 写 resize-image 的 Playwright 测试

**委托内容：**
- 创建 `scripts/test/tool-test.mjs`
- 只写 resize-image 的测试：
  - 打开 `https://picete.com/resize-image/`
  - 上传 test-photo.jpg
  - 输入 600×400
  - 点击处理
  - 等待下载按钮出现
  - 验证：页面出现下载按钮
- 使用 Playwright 的 chromium 浏览器
- 记录 PASS/FAIL

**约束：** 只测 resize-image 这一个工具，验证框架可用

**验证：** `node scripts/test/tool-test.mjs` 运行后输出 PASS

---

## Task 5.4: 扩展 Playwright 测试（压缩类 7 工具）

**委托内容：**
- 在 `scripts/test/tool-test.mjs` 中增加 7 个压缩工具的测试：
  - compress-image（上传 + 拉质量到50 → 下载 → 输出体积 < 输入体积）
  - compress-image-to-50kb（上传大图 → 下载 → 输出 ≤ 50KB）
  - compress-image-to-100kb（同上 ≤ 100KB）
  - compress-image-to-200kb（同上 ≤ 200KB）
  - compress-image-to-500kb（同上 ≤ 500KB）
  - compress-jpg-to-100kb（上传 JPG → 输出 ≤ 100KB）
  - compress-jpg-to-200kb（上传 JPG → 输出 ≤ 200KB）

**约束：** 不修改已有测试代码，只新增

**验证：** 7 个压缩工具全部 PASS

---

## Task 5.5: 扩展 Playwright 测试（格式转换类 6 工具）

**委托内容：**
- 在 `scripts/test/tool-test.mjs` 中增加 6 个格式转换工具的测试：
  - png-to-jpg（上传 PNG → 输出扩展名 .jpg）
  - jpg-to-png（上传 JPG → 输出扩展名 .png）
  - webp-to-png（上传 WebP → 输出扩展名 .png）
  - png-to-webp（上传 PNG → 输出扩展名 .webp）
  - jpg-to-webp（上传 JPG → 输出扩展名 .webp）
  - batch-convert-png-to-jpg（上传 2 张 PNG → 输出 2 张 JPG）

**验证：** 6 个转换工具全部 PASS

---

## Task 5.6: 扩展 Playwright 测试（缩放类 12 工具）

**委托内容：**
- 在 `scripts/test/tool-test.mjs` 中增加 12 个缩放工具的测试：
  - resize-image-to-1080x1080, 1920x1080, 800x800, 1200x630, 512x512, 300x250, 600x600, 1500x500, 200x200, 250x250, 728x90, resize-image-for-facebook-cover
  - 每工具验证输出图片尺寸精确匹配

**验证：** 12 个缩放工具全部 PASS

---

## Task 5.7: 扩展 Playwright 测试（分割/取色/Base64 类 5 工具）

**委托内容：**
- 在 `scripts/test/tool-test.mjs` 中增加：
  - image-splitter（选 2×2 → 输出 4 张）
  - split-image-into-3x3（输出 9 张）
  - split-image-into-4-parts（输出 4 张）
  - extract-colors（输出显示 5+ 种颜色）
  - image-to-base64（输出以 data:image 开头）

**验证：** 5 个工具全部 PASS

---

## Task 5.8: 写语言抽样测试脚本

**委托内容：**
- 创建 `scripts/test/lang-test.mjs`
- 对 zh 语言：curl 5 个工具页（resize-image, compress-image, png-to-jpg, image-splitter, extract-colors）→ 检查 HTTP 200
- 对 ja 语言：curl 5 个相同工具页 → 检查 HTTP 200
- 用 Playwright 打开 `zh/resize-image/` → 检查 page title 是中文、console 无报错
- 记录每页结果

**验证：** `node scripts/test/lang-test.mjs` 10 页全部 200，console 无报错

---

## Task 5.9: 处理 FAIL 工具（分析 + 修复）

**委托内容：**
- 读取 `node scripts/test/tool-test.mjs` 的输出结果
- 对每个 FAIL 的工具：
  1. 分析错误原因（缺 DOM 元素？代码 bug？网络问题？）
  2. 修改对应的工具页 index.html 或 js/main.js 修复
  3. 重跑测试确认 PASS
- 记录修复内容

**约束：** 只修改出 bug 的文件，不碰其他文件

**验证：** 修复后重跑全部 PASS

---

## Task 5.10: 生成测试报告文档

**委托内容：**
- 创建 `docs/reports/TOOL-TEST-REPORT.md`
- 表格格式：工具名 | 测试项 | 结果 PASS/FAIL | 备注
- 列出 20 个工具的测试结果
- 如果有 FAIL 已修复，备注"已修复"
- 创建 `docs/reports/TOOL-BUGS.md`（如果有 bug 记录）
- 更新 PROGRESS.md：P5 标记完成

**验证：** `make verify` 通过

---

# P1: mcp-guide 多语言翻译

## Task 1.1: 翻译 mcp-guide 为中文

**委托内容：**
- 读取 `mcp-guide/index.html`（179行）
- 翻译为中文：
  - `<html lang="zh">`
  - `<title>` 和 `<meta description>` 翻译
  - `<h1>` + 正文翻译，保留技术文档风格
  - `<code>` / `<pre>` 内容不翻译
  - JSON 配置片段不翻译
  - 底部链接路径改为 `/zh/`
  - `canonical link` 改为 `https://picete.com/zh/mcp-guide/`
- 写入 `zh/mcp-guide/index.html`
- `mkdir -p zh/mcp-guide/`

**验证：** `grep -q 'lang="zh"' zh/mcp-guide/index.html`

---

## Task 1.2: 翻译 mcp-guide 为日文

**委托内容：**
- 同上逻辑，翻译为日文
- `<html lang="ja">`
- 写入 `ja/mcp-guide/index.html`

**验证：** `grep -q 'lang="ja"' ja/mcp-guide/index.html`

---

## Task 1.3: 翻译 mcp-guide 为德文

**委托内容：**
- 同上，德文
- `<html lang="de">`
- 写入 `de/mcp-guide/index.html`

---

## Task 1.4: 翻译 mcp-guide 为法文

**委托内容：**
- 同上，法文
- `<html lang="fr">`
- 写入 `fr/mcp-guide/index.html`

---

## Task 1.5: 翻译 mcp-guide 为西班牙文

**委托内容：**
- 同上，西班牙文
- `<html lang="es">`
- 写入 `es/mcp-guide/index.html`

---

## Task 1.6: 翻译 mcp-guide 为葡萄牙文

**委托内容：**
- 同上，葡萄牙文
- `<html lang="pt">`
- 写入 `pt/mcp-guide/index.html`

---

## Task 1.7: 翻译 mcp-guide 为阿拉伯文

**委托内容：**
- 同上，阿拉伯文
- `<html lang="ar">`
- 写入 `ar/mcp-guide/index.html`
- 注意：阿拉伯文是 RTL 语言，但现有 mcp-guide 使用方向无关的 CSS，所以 style 不变，只需改文本内容

---

## Task 1.8: 更新 Makefile + sitemap + 验证

**委托内容：**
- 读取 `Makefile`，找到 `EN_ONLY := mcp-guide` 这一行，删除 mcp-guide
- 读取 `scripts/seo/generate-sitemap.sh`，增加 7 条 `/zh/mcp-guide/`, `/ja/mcp-guide/`… 路径
- 执行 `bash scripts/seo/generate-sitemap.sh` 重新生成 sitemap
- `make verify` 验证通过

**验证：** `grep mcp-guide Makefile` 不显示 exclude；sitemap 包含 7 条 lang 路径

---

# P0: wasm-vips 替换 Canvas API

## Phase 0.1: POC 验证（6 步，每步一个独立 Task）

### Task 0.1.1: npm 初始化 + 安装 wasm-vips

**委托内容：**
- `cd picete/ && npm init -y`
- `npm install wasm-vips`
- 验证 `ls node_modules/wasm-vips/` 存在

**验证：** `npm ls wasm-vips` 显示版本号

---

### Task 0.1.2: 创建本地测试 HTML（加载 wasm-vips + SharedArrayBuffer 验证）

**委托内容：**
- 创建 `scripts/test/wasm-vips-poc.html`
- 用 `<script>` 引入 wasm-vips（CDN: jsDelivr）
- 用 Python HTTP server 启动（带 COOP/COEP 头）：`python3 -c "..."`（设置 `Cross-Origin-Opener-Policy: same-origin` 和 `Cross-Origin-Embedder-Policy: require-corp`）
- 在页面中验证：
  1. wasm-vips 加载成功
  2. `crossOriginIsolated` = true
  3. SharedArrayBuffer 可用
- 在页面上显示以上 3 个状态

**验证：** 打开页面，3 个状态全绿

---

### Task 0.1.3: wasm-vips resize POC（性能对比 Canvas）

**委托内容：**
- 在 `scripts/test/wasm-vips-poc.html` 中增加：
  - 上传一张测试图片
  - 用 wasm-vips 缩放到 800×600
  - 用 Canvas API 缩放到 800×600（已有逻辑）
  - 记录：处理时间、输出图片尺寸、内存
  - 显示对比结果（表格）

**验证：** wasm-vips 输出尺寸 = Canvas 输出尺寸

---

### Task 0.1.4: 验证 wasm-vips 的 AVIF/RAW codec

**委托内容：**
- 在 `scripts/test/wasm-vips-poc.html` 中增加：
  - 尝试用 wasm-vips 的 `Image.newFromBuffer()` 加载 AVIF 格式图片
  - 尝试编码输出 AVIF 文件
  - 尝试加载 .CR2 / .NEF 等 RAW 格式
  - 记录：哪些格式可解码、哪些不可
  - 如果不可，记录缺少的 codec 名称

**验证：** 记录 AVIF 编解码和 RAW 解码的状态（支持/不支持/部分支持）

---

### Task 0.1.5: 单线程 wasm-vips 性能对比

**委托内容：**
- 在 `scripts/test/wasm-vips-poc.html` 中增加：
  - 强制 wasm-vips 以单线程模式运行（无 SharedArrayBuffer 环境）
  - 缩放测试同 Task 0.1.3
  - 对比：Canvas API vs 单线程 wasm-vips vs 多线程 wasm-vips
  - 决策数据显示：如果单线程 ≤ Canvas，标记"降级不可行"

**验证：** 三列性能对比表可见

---

### Task 0.1.6: Vercel COOP/COEP header 验证

**委托内容：**
- 修改 `vercel.json`，在 headers 中增加路径级配置：
  ```
  /resize-image/*: Cross-Origin-Opener-Policy: same-origin
                    Cross-Origin-Embedder-Policy: require-corp
  ```
- 验证：`curl -I https://picete.com/resize-image/` → header 下发了
- 浏览器验证 SharedArrayBuffer 可用

**验证：** curl 返回 COOP/COEP header

---

### Task 0.1.7: 产出 POC 报告

**委托内容：**
- 汇总 Task 0.1.2-0.1.6 的结果
- 创建 `docs/reports/P0-WASM-VIPS-POC-REPORT.md`，包含：
  1. Canvas vs 单线程 wasm-vips vs 多线程 wasm-vips 性能对比表
  2. AVIF/RAW codec 打包验证结果（支持/不支持哪些格式）
  3. Vercel COOP/COEP 兼容性测试结果
  4. 技术决策：是否继续全量替换？需要哪些妥协？

**验证：** 报告包含 4 个部分，有数据支撑

---

## Phase 0.2: 渐进替换（4 rounds，每 round 一个 Task）

### Task 0.2.1: 创建 js/vips-loader.js

**委托内容：**
- 创建 `js/vips-loader.js`
- 功能：动态加载 wasm-vips WASM 文件
- 检测 `crossOriginIsolated` 状态
- 支持返回：wasm-vips instance 或 `null`（降级到 Canvas）
- 支持 CDN（jsDelivr）和本地两种加载路径
- 加载状态钩子：loading / ready / error

**验证：** `node -e "require('./js/vips-loader.js')"` 不报错（语法检查）

---

### Task 0.2.2: 重写 compress-image 核心逻辑（用 wasm-vips）

**委托内容：**
- 读取 `js/main.js` 中的 `processImage()` 和 `compressImage()` 函数
- 创建 `js/vips-tools/compress.js`
- 用 wasm-vips 的 shrink/jpegsave/pngsave/webpsave 实现压缩
- 保持与原有函数相同的输入/输出接口
- 在 compress-image 系列 7 个工具页中引用新逻辑（添加 `<script src="/js/vips-loader.js">` 和 `<script src="/js/vips-tools/compress.js">`）
- 保持 Canvas 降级路径

**验证：** 打开 compress-image 工具，上传图片 → 压缩 → 下载 → 输出体积 ≤ 目标

---

### Task 0.2.3: 重写 resize-image 核心逻辑（用 wasm-vips）

**委托内容：**
- 创建 `js/vips-tools/resize.js`
- 用 wasm-vips 实现缩放
- 保持输入/输出接口一致
- 引用到 resize-image 系列 12 个工具页
- 保持 Canvas 降级路径

**验证：** 打开 resize-image 工具，上传 → 输入 800×600 → 下载 → 输出尺寸 800×600

---

### Task 0.2.4: 重写 split-image 核心逻辑（用 wasm-vips）

**委托内容：**
- 创建 `js/vips-tools/split.js`
- 用 wasm-vips 实现图片分割（crop + 多文件输出）
- 引用到 3 个分割工具页
- 保持 Canvas 降级路径

**验证：** 上传 → 3×3 分割 → 输出 9 张图片

---

### Task 0.2.5: 评估 extract-colors 和 image-to-base64

**委托内容：**
- 评估 wasm-vips 能否替代 Canvas 做取色和 Base64 编码
- 取色：wasm-vips 的 histogram/ stats API 是否比 Canvas getImageData 快
- Base64：wasm-vips 输出的 buffer 直接转 base64 是否更简洁
- 决策记录到 `docs/reports/P0-CANVAS-REPLACEMENT-DECISIONS.md`
- 如果决策是保留 Canvas，记录原因

**验证：** 决策文档存在，有性能数据支持

---

## Phase 0.3: 极速模式入口

### Task 0.3.1: 创建 fast-convert 完整页面（含交互逻辑）

**委托内容：**
- 创建 `fast-convert/index.html`
- 完整交互逻辑一次性实现（不是骨架+填逻辑两步——已验证 Claude Code 一个 prompt 可完成 ~80 行插入级别的工作）
- 复用现有工具页的代码模式（参照 compress-image/index.html 的交互结构）
- 极简 UI：文件拖放区 + 输出格式下拉（JPG/PNG/WebP）+ 质量滑块 + 缩放输入（宽/高）+ 处理按钮 + 下载按钮
- 标题："Fast Image Converter"
- 描述："Convert, resize and compress images in seconds. No upload, no signup."
- 引用 js/vips-loader.js（wasm-vips 路径）
- 引用 js/vips-loader.js（wasm-vips 路径，已存在）
- 引用 js/main.js 的公共 UI 函数（formatSize、reset 等，如果适用）
- wasm-vips + Canvas 双路径（与 Phase 0.2 已替换的 compress/resize 工具相同的模式）
- 格式转换：JPG/PNG/WebP 互转（通过 writeToBuffer 的 ext 参数）
- 缩放：image.resize(scale, { kernel: 'linear' })
- 压缩：writeToBuffer('.jpg', { Q: quality })
- 降级路径：wasm-vips 不可用时 Canvas 回退（与已有工具一致的 fallback 模式）
- 输出：下载按钮 + 文件大小显示
- 无编辑功能（不展示预览 grid、颜色提取等）

**验证：** 上传 → 选 WebP → 缩放 800px → 处理 → 下载 .webp

---

### Task 0.3.2: fast-convert 7 语言翻译

**委托内容：**
- 读取 `fast-convert/index.html`（Task 0.3.1 完成后的版本）
- 翻译为 7 语言：zh/ja/de/fr/es/pt/ar
- 子代理并行翻译（不碰同一文件）
- 阿拉伯文特殊处理：加 `dir="rtl"`
- 保持代码块/配置片段不翻译

**验证：** `curl -I https://picete.com/zh/fast-convert/` HTTP 200

---

### Task 0.3.3: 首页入口链接更新

**委托内容：**
- 在英文首页 `index.html` 底部工具列表中增加 fast-convert 入口链接
- 参考现有工具链接的 HTML 结构（定位到首页底部工具网格区域）
- 在所有 7 个语言版本的首页（`zh/index.html`、`ja/index.html` 等）增加对应翻译的入口链接
- 在导航/顶部菜单（如果存在）增加 fast-convert 入口
- 只添加链接，不修改其他内容

**验证：** curl 8 个路径（index 首页）检查 fast-convert 链接存在

---

### Task 0.3.4: 更新 sitemap + feature_list

**委托内容：**
- sitemap 扩容：增加 fast-convert/ + 7 语言版 = 8 条 URL
- 运行 `bash scripts/seo/generate-sitemap.sh`
- feature_list.json 增加条目（按照现有编号延续，参考 P0.5 Task 0.5.8 的格式）
- PROGRESS.md 标记 Phase 0.3 完成

**验证：** `make verify` 通过，sitemap 包含 8 条 fast-convert 路径

---

# P0.5: AVIF + RAW 支持

## 战略背景

**重要发现（2026-06-03 POC Task 0.1.4 验证）：** wasm-vips v0.0.17 的 WASM 编译版中：

| 格式 | wasm-vips 支持情况 | 结论 |
|------|-------------------|------|
| **AVIF** | ✅ libheif AV1 编码器已编译入 WASM，encode + decode 均通过 | wasm-vips 落地后 AVIF 能力是"白送的" |
| **RAW** | ❌ libraw **未编译入** WASM bundle。`vips.config()` 显示 `RAW load with libraw: false` | RAW 需要独立的解码方案 |

**因此，P0.5 的技术方案分为两条路径：**

```
AVIF 路径:  wasm-vips 统一管线（libheif AV1）
RAW 路径:  libraw-wasm 独立 WASM（或 Node.js Sharp 用于 MCP 端）
```

### AVIF 方案（沿用 V2 假设，已验证可行）

AVIF 的编解码能力通过 wasm-vips 的 libheif 模块实现：
- 编码：`image.writeToBuffer('.avif')` 输出 AVIF 文件（已测试通过，800×600 图片输出 10.2KB）
- 解码：wasm-vips 可直接打开 AVIF 文件并读取像素数据
- 两套预设：极速（quality=80, speed=6）和极限压缩（quality=50, speed=0）

### RAW 方案（需修正 V2 假设）

wasm-vips 不包含 libraw，RAW 解码需要独立实现：

**方案 A（推荐）：libraw-wasm**
- npm 包 `libraw-wasm`（LibRaw 的独立 WASM 编译）
- 浏览器端解码 CR2/NEF/ARW/DNG 等 RAW 格式
- 解码后像素数据传给 wasm-vips 或 Canvas 渲染
- 需要独立加载额外的 WASM bundle（~2MB）
- 参考：https://www.npmjs.com/package/libraw-wasm

**方案 B：Node.js Sharp（MCP 端）**
- MCP Server 用 Sharp 原生解码 RAW
- 浏览器端用 Canvas 回退

**方案 C：自编译 wasm-vips 加入 libraw**
- 从源码编译 wasm-vips，在 Emscripten 构建中启用 libraw
- 技术门槛高，但可统一管线
- 适合 P0 长期规划

**POC 阶段决策：** POC 完成后根据 RAW 工具页的优先级决定是 A/B/C。

---

## Task 0.5.1: 创建 avif-to-png 工具页（第一个 AVIF 工具）

**委托内容：**
- 创建 `avif-to-png/index.html`
- 参照 `png-to-jpg/index.html` 的交互模式
- 标题："AVIF to PNG Converter"
- 文件拖放区 + 处理按钮 + 下载
- 使用 js/main.js 的通用逻辑
- 注意：依赖 wasm-vips 解码 AVIF → Canvas 渲染 → PNG 输出

**验证：** 浏览器打开可见 UI

---

## Task 0.5.2: 创建 png-to-avif 工具页

**委托内容：**
- 创建 `png-to-avif/index.html`
- 标题："PNG to AVIF Converter"
- 含"极速"和"极限压缩"两套预设的文字标签
- 参照格式转换工具页模板

---

## Task 0.5.3: 创建 jpg-to-avif + webp-to-avif 工具页

**委托内容：**
- 创建 `jpg-to-avif/index.html`
- 创建 `webp-to-avif/index.html`
- 参照 Task 0.5.2

---

## Task 0.5.4: 创建 raw-to-jpg + raw-to-png 工具页

**委托内容：**
- 创建 `raw-to-jpg/index.html`（标题："RAW to JPG Converter"）
- 创建 `raw-to-png/index.html`
- 描述："Convert camera RAW files (CR2, NEF, ARW, DNG) to JPG/PNG"
- **技术方案：** RAW 解码不走 wasm-vips（libraw 未编译入 WASM），而是使用独立的 `libraw-wasm` npm 包
- 前端的 RAW 解码流程：上传 RAW → libraw-wasm 解码 → Canvas/WebGL 渲染 → 输出
- 标注支持的 RAW 格式列表（至少：CR2, NEF, ARW, DNG, RW2, ORF）

**验证：** 页面可见，标注支持的 RAW 格式列表

---

## Task 0.5.5: 创建 raw-to-webp + raw-to-avif 工具页

**委托内容：**
- 创建 `raw-to-webp/index.html`
- 创建 `raw-to-avif/index.html`
- 参照格式转换工具页模板
- RAW 解码同样使用 `libraw-wasm`，输出后编码为 WebP/AVIF 可通过 wasm-vips 完成（AVIF 编码走 libheif）

---

## Task 0.5.5a: zh 翻译（标杆）

**委托内容：**
- 翻译 avif-to-png / png-to-avif / jpg-to-avif / webp-to-avif 共 4 页的中文版本
- zh 翻译为质量标杆
- 写入 zh/avif-to-png/index.html 等

**验证：** curl zh/avif-to-png/ HTTP 200

---

## Task 0.5.5b: ja 翻译（串行）

**委托内容：**
- 翻译 4 个工具页为日文
- `<html lang="ja">`
- 写入 ja/avif-to-png/index.html 等

---

## Task 0.5.5c: de 翻译（串行）

**委托内容：**
- 翻译 4 个工具页为德文
- 写入 de/avif-to-png/index.html 等

---

## Task 0.5.5d: fr 翻译（串行）

**委托内容：**
- 翻译 4 个工具页为法文
- 写入 fr/avif-to-png/index.html 等

---

## Task 0.5.5e: es 翻译（串行）

**委托内容：**
- 翻译 4 个工具页为西班牙文
- 写入 es/avif-to-png/index.html 等

---

## Task 0.5.5f: pt 翻译（串行）

**委托内容：**
- 翻译 4 个工具页为葡萄牙文
- 写入 pt/avif-to-png/index.html 等

---

## Task 0.5.5g: ar 翻译（RTL 处理，串行）

**委托内容：**
- 翻译 4 个工具页为阿拉伯文
- `<html lang="ar">` + `dir="rtl"`
- 确保 RTL 布局正常

---

## Task 0.5.6: 首页入口链接更新

**委托内容：**
- sitemap 扩容 8 × 8 = 64 条
- feature_list.json 增加 8 个条目：
  - tool-039: png-to-avif
  - tool-040: jpg-to-avif
  - tool-041: webp-to-avif
  - tool-042: avif-to-png
  - tool-043: raw-to-jpg
  - tool-044: raw-to-png
  - tool-045: raw-to-webp
  - tool-046: raw-to-avif
  - 每个 status: "complete"（标注需要 wasm-vips 支持）
- 首页底部增加"支持 AVIF" / "支持 RAW"宣传区

**验证：** `make verify` 通过，sitemap 包含新 URL

---

# 全局验证标准

每条 Task 结束后，Hermes 执行：

- [ ] `make verify` 通过
- [ ] `make lint` 通过
- [ ] `git status --short` 确认只含本 Task 文件
- [ ] 验证产出是否存在（curl/ls/read_file 独立验证）
- [ ] 不信任自报告

# 禁止行为

- ❌ `git add -A` — 只 add 本 Task 修改的文件
- ❌ 创建临时脚本在根目录 — 临时脚本放 `scripts/legacy/`
- ❌ 修改英文原版工具页的 UI/内容
- ❌ 跨 Task 修改未分配的文件

---

*文档位置: `picete/docs/specs/PICETE-OPTIMIZATION-PLAN-V2.md`*
*更新: 2026-06-03 V2.3 — 修正 RAW 方案（wasm-vips 不含 libraw），改为 libraw-wasm 独立方案*
