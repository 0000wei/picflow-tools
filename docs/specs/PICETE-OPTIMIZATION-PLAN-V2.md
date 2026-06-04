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

## Task 0.5.10: 翻译 mcp-guide 为中文

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

## Task 0.5.11: 翻译 mcp-guide 为日文

**委托内容：**
- 同上逻辑，翻译为日文
- `<html lang="ja">`
- 写入 `ja/mcp-guide/index.html`

**验证：** `grep -q 'lang="ja"' ja/mcp-guide/index.html`

---

## Task 0.5.12: 翻译 mcp-guide 为德文

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

## Phase 0.5-A.1: POC 验证（6 步，每步一个独立 Task）

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

## Phase 0.5-A.2: 渐进替换（4 rounds，每 round 一个 Task）

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

## Phase 0.5-A.3: 极速模式入口

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
- wasm-vips + Canvas 双路径（与 Phase 0.5-A.2 已替换的 compress/resize 工具相同的模式）
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
- PROGRESS.md 标记 Phase 0.5-A.3 完成

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

## 翻译方案: 三步流水线（所有 0.5.5 子任务共用）

**根因：** deepseek-chat 输出 token 上限不足以一次性生成 700 行翻译 HTML（失败率 75%）。纯文本翻译 JSON 输出仅 ~3000 tokens（成功率 100%）。

**因此采用提取→翻译→注入三步流水线：**

| 步 | 谁做 | 内容 | 耗时 | 输出 token |
|----|------|------|------|-----------|
| 1 | 管理者（脚本） | 从 EN HTML 提取所有需翻译文本为 JSON | 3s | 0（本地脚本） |
| 2 | 子代理（delegate_task） | 翻译 JSON 文本为目标语言 | ~18s | ~3000（不超限） |
| 3 | 管理者（脚本） | 从 EN HTML 复制副本，注入翻译文本 | 3s | 0（本地脚本） |

**关键规则（来自 0.5.5a 实践经验）：**
- Step 2 只翻译纯文本（标题、描述、FAQ、按钮、预设、alert 消息）——不操作 HTML/JS/CSS
- Step 3 基于 EN 模板（不是 zh 模板）注入——避免中日汉字混写问题
- Step 3 使用精确字符串匹配（正则或直接替换）——不依赖模糊匹配
- 每语言结束后抽样检查：标题、一条 FAQ、一个内容段落
- 如果某语言 Step 2 输出有质量问题，只重复 Step 2（Step 1 和 3 不变）

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
- 三步流水线翻译 4 个工具页为日文
- `<html lang="ja">`
- Canonical: `https://picete.com/ja/...`
- 写入 ja/avif-to-png/index.html 等

**内容段落翻译质量检查（管理者抽样）：**
- 标题正确
- 一条 FAQ Q&A 翻译合理
- 一个内容段落无中日混写
- JS alert 已翻译

---

## Task 0.5.5c: de 翻译（串行）

**委托内容：**
- 三步流水线翻译 4 个工具页为德文
- `<html lang="de">`
- Canonical: `https://picete.com/de/...`
- 写入 de/avif-to-png/index.html 等

**内容段落翻译质量检查（管理者抽样）：**
- 标题正确
- 一条 FAQ Q&A 翻译合理
- JS alert 已翻译

---

## Task 0.5.5d: fr 翻译（串行）

**委托内容：**
- 三步流水线翻译 4 个工具页为法文
- `<html lang="fr">`
- Canonical: `https://picete.com/fr/...`
- 写入 fr/avif-to-png/index.html 等

**内容段落翻译质量检查（管理者抽样）：**
- 标题正确
- 一条 FAQ Q&A 翻译合理
- JS alert 已翻译

---

## Task 0.5.5e: es 翻译（串行）

**委托内容：**
- 三步流水线翻译 4 个工具页为西班牙文
- `<html lang="es">`
- Canonical: `https://picete.com/es/...`
- 写入 es/avif-to-png/index.html 等

**内容段落翻译质量检查（管理者抽样）：**
- 标题正确
- 一条 FAQ Q&A 翻译合理
- JS alert 已翻译

---

## Task 0.5.5f: pt 翻译（串行）

**委托内容：**
- 三步流水线翻译 4 个工具页为葡萄牙文
- `<html lang="pt">`
- Canonical: `https://picete.com/pt/...`
- 写入 pt/avif-to-png/index.html 等

**内容段落翻译质量检查（管理者抽样）：**
- 标题正确
- 一条 FAQ Q&A 翻译合理
- JS alert 已翻译

---

## Task 0.5.5g: ar 翻译（RTL 处理，串行）

**委托内容：**
- 三步流水线翻译 4 个工具页为阿拉伯文
- `<html lang="ar">` + `dir="rtl"`
- Canonical: `https://picete.com/ar/...`
- 写入 ar/avif-to-png/index.html 等
- 确保 RTL 布局正常

**内容段落翻译质量检查（管理者抽样）：**
- 标题正确
- 一条 FAQ Q&A 翻译合理
- JS alert 已翻译
- 页面包含 `dir="rtl"`

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

# RAW 支持 — 方案 C（自编译 wasm-vips + libraw）

## 决策背景

2026-06-03 用户决策：
| 选择 | 结论 |
|------|------|
| RAW 方案 | C（自编译 wasm-vips 加入 libraw）- 最后突破 |
| AVIF/RAW 优先级 | 先做 AVIF 并完成，RAW 后续 |

**AVIF 方案（Phase 0.5-A.5）已于 2026-06-03 全部完成。** 以下是 RAW 的完整执行计划。

## 技术可行性

wasm-vips v0.0.17 的 Emscripten 构建中，有两处禁用 RAW 的编译选项：
1. 第 274 行：`--disable-raw-api` — glib 编译时禁用 raw API
2. 第 534 行：`-Draw=disabled` — libvips 编译时禁用 raw 支持

**方案 C 需要：**
1. 从源码编译 wasm-vips（Docker 构建，Emscripten 工具链）
2. 修改 build.sh：移除 `--disable-raw-api` 和 `-Draw=disabled`
3. 加入 libraw 依赖
4. 生成自定义 `vips.wasm`，替换 js/lib/ 下的文件

## 禁止范围（Out of Scope）

- ❌ 不做 libraw-wasm 独立方案（方案 A）——除非方案 C 验证失败
- ❌ 不做 MCP Sharp 后端解码（方案 B）
- ❌ RAW 批量转换 UI
- ❌ EXIF 元数据可视化编辑器
- ❌ MCP 工具的扩展

## 实现阶段

### Phase 0.5-A：环境准备与调研（4 个 Task）

#### Task 0.5.7: 检查 libraw 版本 + 添加版本变量到 build.sh

**目标：** 确认 libraw 版本并添加到 build.sh 版本变量区，不涉及编译。

**委托内容：**
- 确认 libraw 最新稳定版（搜索 GitHub releases：`https://github.com/LibRaw/LibRaw/releases`）
- 在 build.sh 的版本变量区（~第 178-200 行的 `VERSION_*` 区域）新增一行：
  ```bash
  VERSION_RAW=0.21.3    # https://github.com/LibRaw/LibRaw
  ```
- 在依赖清单函数（~第 205-225 行的 `dep_versions_json()`）中新增：
  ```bash
  printf "  \"raw\": \"${VERSION_RAW}\",\n";
  ```

**不做的：**
- 不改 `--disable-raw-api` 和 `-Draw=disabled`
- 不添加编译步骤
- 不启动构建

**验证：** `grep 'VERSION_RAW' /tmp/wasm-vips/build.sh` 返回新版本行

**预计耗时：** 5 分钟

---

#### Task 0.5.8: 添加 libraw Emscripten 编译步骤到 build.sh（第一版）

**目标：** 在 build.sh 中添加 libraw 的交叉编译代码块，参照 libheif 的已有模式。

**委托内容：**
- 在 build.sh 中、其他依赖编译块之后（在 libheif 编译块之后，vips 编译之前）添加 libraw 编译块：
  ```bash
  [ -f "$TARGET/lib/pkgconfig/libraw_r.pc" ] || (
    stage "Compiling libraw"
    mkdir $DEPS/raw
    curl -Ls https://github.com/LibRaw/LibRaw/archive/refs/tags/$VERSION_RAW.tar.gz | tar xzC $DEPS/raw --strip-components=1
    cd $DEPS/raw
    # 参照 libheif 的 emcmake 模式
    emcmake cmake -B_build -S. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$TARGET \
      -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF -DCMAKE_C_FLAGS="$CFLAGS -O3" \
      -DCMAKE_CXX_FLAGS="$CXXFLAGS -O3"
    make -C _build install
  )
  ```

**注意：** 这个编译块是第一版尝试。cmake 参数可能需要根据构建失败日志调整。

**不做的：**
- 不改 `--disable-raw-api` 和 `-Draw=disabled`（下次 Task 改）
- 不启动构建

**验证：** `grep -c 'Compiling libraw' /tmp/wasm-vips/build.sh` ≥ 1

**预计耗时：** 10 分钟

---

#### Task 0.5.9: 首次 RAW 构建 — 重新规划（V2）

**目标：** 自编译 wasm-vips + libraw，确保 **Canon/Nikon/Sony/Adobe DNG 四家主流 RAW 格式可靠解码**。

**2026-06-04 复盘（V1 失败原因）：**
1. 验证标准只检查了 `vips.config()` 字符串，没有用实际 RAW 文件测试
2. ARW（Sony α7III）存在不稳定问题：同一相机不同 ARW 文件有时能解有时不能
3. DNG 受网络限制未及时验证
4. 误将"一次成功"当作"问题已修复"

**V2 拆解为以下 Task：**

---

#### Task 0.5.9a: 解决 WASM 内存不足 + 修复主流 RAW 解码

**目标：** 确保 Canon CR2/CR3、Nikon NEF、Sony ARW、Adobe DNG 全部解码成功，且结果稳定。

**委托内容：**
1. **内存修复**（已验证可行）：在 `src/meson.build` 中添加：
   ```
   '-sALLOW_MEMORY_GROWTH',
   '-sMAXIMUM_MEMORY=2GB',
   ```
2. **稳定性修复**：排查并修复 vladhdv_dsc03380.arw（Sony α7III v4.01）解码不稳定的根因
   - 分别测试 3 次该文件，记录每次的 decode 时间和输出大小
   - 如果 JS heap 不足，尝试在 Node.js 中 `--max-old-space-size=8192`
   - 如果 wasm-vips 的内存碎片化，尝试在每次 decode 后 GC（`global.gc()` 需 `--expose-gc`）
   - 如果问题是特定固件版本的 ARW 压缩差异，记录到已知限制
3. **构建并测试以下 RAW 文件**（每文件跑 3 次，取最差结果）：

   | 品牌 | 文件 | 大小 | 要求 |
   |------|------|------|------|
   | Canon | 0c0a0435.cr2 | 26MB | 3 次均成功 |
   | Canon | CR3 | 8.7MB | 3 次均成功 |
   | Nikon | NEF (Z6) | 26MB | 3 次均成功 |
   | Nikon | NEF (other) | 27MB | 3 次均成功 |
   | Sony | dsc1756.arw | 24MB | 3 次均成功 |
   | Sony | vladhdv_dsc03380.arw | 24MB | 3 次均成功 |
   | Adobe | sample.dng | 6MB | 3 次均成功 |

**硬性验证标准：** 以上 7 个文件各跑 3 次，21 次测试全部 PASS
**如果任何文件失败：** 记录失败模式和频率，更新以上清单

**预计耗时：** 1-2 次构建 + 稳定性排查

---

#### Task 0.5.9b: 生成 RAW 兼容性清单

**目标：** 明确记录 4 家主流的兼容状态 + 其他格式的实验性标注。

**委托内容：**
1. 用 `node scripts/test/raw-decoding-test.mjs` 跑所有可用 RAW 测试文件
2. 生成兼容性矩阵表格（格式模板）：

   | 品牌 | 格式 | 已验证机型 | 结果 | 稳定性 | 备注 |
   |------|------|-----------|------|--------|------|
   | Canon | CR2 | EOS 5D Mark IV | ✅ | 稳定 | — |
   | Canon | CR3 | EOS R6 | ✅ | 稳定 | — |
   | Nikon | NEF | Z6 | ✅ | 稳定 | — |
   | Sony | ARW | α7III (ILCE-7M3) | ⚠️ | 不稳定 | v4.01 固件有时失败 |
   | Adobe | DNG | Canon EOS 350D 转换 | ✅ | 稳定 | — |

3. **实验性格式标签：** 以下格式标记为"实验性（未验证）"：RAF, RW2, ORF, PEF, PTX, RAW, RWL, X3F, 3FR, IIQ, KDC, DCR, MRW, SRW, MEF, MOS, ERF, BAY, R3D, BRAW
4. 将兼容性矩阵写入 `docs/reports/RAW-COMPATIBILITY.md`

**验证：** 兼容性报告文件存在且格式完整

**预计耗时：** 30 分钟

---

#### Task 0.5.9c: 产出 RAW 构建和测试报告

**目标：** 汇总全部构建和测试经验，产出完整文档。

**委托内容：**
1. 更新 `docs/reports/RAW-BUILD-LOG.md` — 追加 V2 构建的迭代记录
2. 创建 `docs/reports/RAW-POC-REPORT.md` — 正式 POC 报告，包含：
   - 技术方案：自编译 wasm-vips + libraw
   - 构建统计：总迭代次数、关键修复点
   - 兼容性矩阵（引用 RAW-COMPATIBILITY.md）
   - 性能数据：各格式解码时间、输出质量
   - 已知限制：不稳定的机型/固件、不支持的特殊格式
   - bundle 大小变化：5.89MB → ~5.8MB

**验证：** 2 份报告文件存在且内容完整

**预计耗时：** 30 分钟

---

### Phase 0.5-B：浏览器端验证（3 个 Task）

#### Task 0.5.10: 单线程 WASM 编译（方案 B）

**背景：** 之前的多线程（pthread）版本在浏览器中创建 6 个 worker 线程，CPU 满载且加载卡死。经诊断：Emscripten 多线程 WASM 依赖 SharedArrayBuffer + COOP/COEP 头，且需内置降级检测。单线程版本不依赖 worker，加载稳定且兼容更广的浏览器环境。对于单张图片解码场景，单线程性能足够。

**目标：** 重新编译 wasm-vips（单线程模式，不含 -pthread），验证 RAW 解码在浏览器中可用。

**委托内容：**
1. **修改 `src/meson.build`**：
   - 移除 pthread 相关编译参数（`-pthread`、`-sALLOW_MEMORY_GROWTH`、`-sMAXIMUM_MEMORY`）
   - 确保 `-sMALLOC=mimalloc` 保留（单线程也受益于此）
   - 确保 INITIAL_MEMORY 设为 1GB（大 RAW 文件解码需要）

2. **修改 `build.sh` 中的环境变量**：
   - 确保 `ENVIRONMENT=web`（不需要 Node.js 版本）
   - 移除 `CFLAGS` 和 `CXXFLAGS` 中的 `-pthread -fwasm-exceptions`

3. **重新构建**：
   ```bash
   rm -f /tmp/wasm-vips/build/target/lib/pkgconfig/vips.pc
   sg docker -c "docker run --rm --name wasm-vips-single --network host \
     -v /tmp/wasm-vips:/src \
     -e HTTP_PROXY=http://127.0.0.1:7897 \
     -e HTTPS_PROXY=http://127.0.0.1:7897 \
     wasm-vips"
   ```

4. **替换 js/lib/ 下的文件**：
   - `vips.wasm`、`vips-heif.wasm`、`vips-jxl.wasm`、`vips-resvg.wasm`
   - `vips.js`、`vips-es6.js`

5. **验证**：
   - `make verify` 通过
   - `vips-loader.js` 加载后 `window.Vips` 可用
   - `crossOriginIsolated` 不再是硬性要求

**验证：** `node -e "const v=require('/tmp/wasm-vips/lib/vips-node.js'); (async()=>{const vv=await v(); console.log(vv.config())})()"` 显示 `RAW load with libraw_r: true`

**预计耗时：** 1-2 次构建（30-60 分钟/次）

---

#### Task 0.5.11: 浏览器 RAW 解码页面测试

**前置条件：** Task 0.5.10 完成

**委托内容：**
1. 启动本地 HTTP server（带 COOP/COEP header）
2. 打开浏览器测试页面 `scripts/test/raw-decoding-poc.html`
3. 用 CDP 或手动方式验证：
   - wasm-vips 加载成功 ✅（显示 ready 状态）
   - RAW support 确认 ✅
   - 上传 CR2/NEF/ARW/DNG 文件能解码并显示预览图
4. 记录：解码时间、输出质量、浏览器兼容性

**验证：** 浏览器中 RAW 文件上传后可见预览图

**预计耗时：** 1 小时

---

#### Task 0.5.12: 性能评估 + 决策

**前置条件：** Task 0.5.11 完成

**委托内容：**
1. 对比单线程 vs 之前多线程的 RAW 解码性能
2. 确认 bundle 大小变化（预期单线程版本更小）
3. 记录 COOP/COEP 依赖变化（单线程不再需要）
4. 决策：继续 4 个 RAW 工具页？还是先做 1-2 个验证市场反应？
5. 更新 PROGRESS.md + feature_list.json

**验证：** 决策文档记录完成

**预计耗时：** 30 分钟

---

### Phase 0.5-C：工具页 + 翻译 + 入口（待 0.5.12 决策后启动）

#### Task 0.5.13: raw-to-jpg 工具页（第一个 RAW 工具）

**前置条件：** Task 0.5.12 决策通过

**委托内容：**
- 创建 `raw-to-jpg/index.html`
- 参照 `png-to-jpg/index.html` 的交互模式
- 标题："RAW to JPG Converter"
- 标注支持的 RAW 格式（引用兼容性矩阵）
- wasm-vips 解码 RAW + writeToBuffer('.jpg')
- 引用 js/vips-loader.js
- 大文件显示 loading 状态（WASM 解码可能需要几秒）

**验证：** `make verify` 通过

**预计耗时：** 1 小时

---

#### Task 0.5.14 — 0.5.19: raw-to-png / raw-to-webp / raw-to-avif + 7 语言翻译 + 入口/sitemap

（与 AVIF Phase 0.5 复用相同模式，待 0.5.13 完成后依次推进）

---

#### Task 0.5.12: 性能评估 + 决策

**委托内容：**
- 汇总 Phase 0.5-B 的测试数据：解码速度、bundle 大小、兼容性
- 决策：继续 4 个 RAW 工具页？还是先做 1-2 个验证市场反应？
- 更新 PROGRESS.md + feature_list.json

**验证：** 决策文档记录完成

**预计耗时：** 0.5 天

---

### Phase 0.5-C：工具页（4 个 Task，每个独立）

#### Task 0.5.13: raw-to-jpg 工具页

**委托内容：**
- 创建 `raw-to-jpg/index.html`
- 参照 `avif-to-png/index.html` 的交互模式
- 标题："RAW to JPG Converter"
- 标注支持的 RAW 格式列表（CR2, NEF, ARW, DNG, RW2, ORF）
- wasm-vips 解码 RAW + writeToBuffer('.jpg')（Canvas 降级路径）
- 引用 js/vips-loader.js
- 使用 js/main.js 的通用逻辑

**验证：** `make verify` 通过，页面可见 UI

**预计耗时：** 1 小时

---

#### Task 0.5.14: raw-to-png 工具页

- 参照 Task 0.5.13
- wasm-vips 解码 RAW + writeToBuffer('.png')

**预计耗时：** 1 小时

---

#### Task 0.5.15: raw-to-webp 工具页

- wasm-vips 解码 RAW + writeToBuffer('.webp')

**预计耗时：** 1 小时

---

#### Task 0.5.16: raw-to-avif 工具页

- wasm-vips 解码 RAW + writeToBuffer('.avif', { Q: quality })
- 依赖 AVIF 编码能力（已验证）

**预计耗时：** 1 小时

---

### Phase 0.5-D：翻译（7 个 Task，串行）

复用 AVIF 的三步流水线方案（详见上文"翻译方案: 三步流水线"）。

顺序：zh → ja → de → fr → es → pt → ar（ar 需 dir="rtl"）

每语言 4 个工具页（raw-to-jpg / raw-to-png / raw-to-webp / raw-to-avif）。

**预计总耗时：** ~30 分钟/语言 = 3.5 小时

---

### Phase 0.5-E：入口 + sitemap（1 个 Task）

#### Task 0.5.17: 首页入口 + sitemap + feature_list

**委托内容：**
- 8 首页（en + 7 语言）tool grid + footer 增加 RAW 工具入口
- sitemap 扩容 +32 条（4 RAW 工具 × 8 语言）
- feature_list.json 增加 4 个 RAW 工具条目
- Makefile EN_ONLY 处理
- PROGRESS.md 标记 Phase 完成

**验证：** `make verify` 通过，sitemap 包含 RAW URL

**预计耗时：** 30 分钟

---

## 总计

| Phase | Task 数 | 工期估计 |
|-------|---------|---------|
| 0 — 环境/编译 | 2 | 2-3 天（含编译等待） |
| 1 — 验证 | 3 | 1-2 天 |
| 2 — 工具页 | 4 | 1-2 天 |
| 3 — 翻译 | 7 | ~3.5 小时 |
| 4 — 入口/sitemap | 1 | 30 分钟 |
| **合计** | **17** | **~5-8 天** |

## 风险评估

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 自编译 wasm-vips 依赖问题（libraw 编译失败） | 中 | 高 | 回退方案 A（libraw-wasm） |
| 编译后 bundle 过大（>10MB） | 中 | 中 | 评估浏览器首次加载时间，考虑懒加载 |
| RAW 解码速度过慢（>5s 每张） | 低 | 中 | 增加降采样策略，预览图用小尺寸 |
| 新 vips.wasm 与现有 COOP/COEP 配置冲突 | 低 | 高 | P0 POC 已验证 COOP/COEP 路径级配置有效 |
| Docker 环境不可用或无 root 权限 | 低 | 高 | 方案 A 回退，绕开 Docker 依赖 |

---

*文档位置: `picete/docs/specs/PICETE-OPTIMIZATION-PLAN-V2.md`*
*更新: 2026-06-03 V2.4 — 新增 RAW 支持（方案 C）执行计划，17 个 Task 细粒度拆解*
