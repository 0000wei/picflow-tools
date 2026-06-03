# wasm-vips 包技术调研文档

> 调研时间：2026-06-03
> 调研目的：PicEte P0 — wasm-vips 替换 Canvas API POC 的第一步
> 包版本：0.0.17 | libvips 版本：8.18.1

---

## 1. 基本信息

| 属性 | 值 |
|------|-----|
| 包名 | `wasm-vips` |
| 版本 | 0.0.17 |
| 作者 | Kleis Auke Wolthuizen |
| 仓库 | https://github.com/kleisauke/wasm-vips |
| 许可证 | MIT |
| Node.js 最低版本 | >= 16.4.0 |
| npm 安装 | `npm install wasm-vips` |

libvips 在 wasm-vips 中已编译的依赖库版本（来自 `versions.json`）：

- libvips 8.18.1
- mozjpeg (0826579)
- libpng 1.6.55
- libwebp 1.6.0
- libtiff 4.7.1
- libheif 1.21.2
- libjxl 0.11.2
- librsvg / resvg 0.47.0
- aom 3.13.1
- highway 1.3.0
- lcms2 2.18
- glib 2.88.0
- Emscripten 5.0.3

---

## 2. 包文件结构

```
node_modules/wasm-vips/
├── lib/
│   ├── vips.js              # 浏览器 CJS 入口 (90 KB)
│   ├── vips-es6.js          # 浏览器 ESM 入口 (90 KB)
│   ├── vips-node.js         # Node.js CJS 入口 (96 KB)
│   ├── vips-node.mjs        # Node.js ESM 入口 (96 KB)
│   ├── vips.d.ts            # TypeScript 类型定义 (262 KB, 9401 行)
│   ├── vips.wasm            # 核心 WASM 模块 (5.7 MB)
│   ├── vips-heif.wasm       # HEIF 支持 WASM 动态库 (4.5 MB)
│   ├── vips-jxl.wasm        # JPEG XL 支持 WASM 动态库 (2.3 MB)
│   └── vips-resvg.wasm      # SVG 渲染支持 WASM 动态库 (1.5 MB)
├── package.json
├── README.md
├── LICENSE
├── THIRD-PARTY-NOTICES.md
└── versions.json
```

### WASM Bundle 大小汇总

| 文件 | 大小 | 说明 |
|------|------|------|
| `vips.wasm` | 5.7 MB | 核心 WASM（必需） |
| `vips-heif.wasm` | 4.5 MB | HEIF/AVIF 格式支持（按需加载） |
| `vips-jxl.wasm` | 2.3 MB | JPEG XL 格式支持（按需加载） |
| `vips-resvg.wasm` | 1.5 MB | SVG 渲染支持（按需加载） |

**加载策略：** `vips.wasm` 是核心，必须加载。`vips-heif.wasm` 和 `vips-jxl.wasm` 通过 `dynamicLibraries` 数组自动加载（默认即加载两者）。如果需要减少初始加载体积，可以通过配置跳过不需要的动态库。

---

## 3. export 结构

Node.js 入口（`require('wasm-vips')`）暴露一个名为 `Vips` 的 **async 工厂函数**：

```js
const Vips = require('wasm-vips');
// Vips 是一个 async function
console.log(typeof Vips); // 'function'
```

调用 `await Vips()` 后返回完整的 vips 实例对象，包含：

### 顶层 API

| 路径 | 类型 | 说明 |
|------|------|------|
| `vips.Image` | class | 核心图片处理类（312+ 实例方法） |
| `vips.version()` | function | 返回 libvips 版本号 (8.18.1) |
| `vips.concurrency()` | function | 获取/设置工作线程数 |
| `vips.emscriptenVersion()` | function | 返回 Emscripten 版本 |
| `vips.config()` | function | 返回 libvips 构建配置 |
| `vips.blockUntrusted()` | function | 阻止不可信操作 |
| `vips.operationBlock()` | function | 阻止指定类别的操作 |
| `vips.shutdown()` | function | 清理资源、关闭后台线程 |
| `vips.Cache` | class | 缓存控制 |
| `vips.Stats` | class | 统计信息 |
| `vips.Utils` | class | 工具函数 |
| `vips.Interpolate` | class | 插值器 |
| `vips.Connection` / `Source` / `Target` | class | I/O 抽象 |
| `vips.deletionQueue` | array | 待删除句柄队列 |

### 枚举值（编译写入 WASM，运行时自动注册）

- `BandFormat` — 像素格式（UCHAR, FLOAT, etc.）
- `BlendMode`, `Coding`, `Interpretation`, `Access`, `Extend`, `Direction`, `Align`, `Angle`, `Kernel`, `Size`, `Intent`, `Precision` 等 30+ 枚举

### Image 类的关键方法

#### 静态工厂方法
- `vips.Image.newFromFile(path)` — 从文件加载（Node.js）
- `vips.Image.newFromBuffer(buffer, options)` — 从内存加载（浏览器场景）
- `vips.Image.newFromMemory(data, width, height, bands, format)` — 从原始像素数据
- `vips.Image.newFromSource(source)` — 从 Source 对象
- `vips.Image.newFromArray(array, scale)` — 从数组常量创建（如卷积核）
- `vips.Image.newMatrix(width, height)` — 从矩阵
- `vips.Image.thumbnail(path/url, width)` — 生成缩略图
- `vips.Image.thumbnailBuffer(buffer, width)` — 从 buffer 生成缩略图
- `vips.Image.black(width, height)` — 创建黑色图像
- 格式专用加载：`jpegload`, `pngload`, `webpload`, `gifload`, `heifload`, `jxlload`, `svgload`, `tiffload` 等（均支持 buffer/source 变体）

#### 实例方法（PicEte 相关）

**几何变换：**
- `image.resize(scale, options?)` — 缩放
- `image.scale(options?)` — 按比例缩放
- `image.thumbnailImage(width, options?)` — 缩略图
- `image.crop(left, top, width, height)` — 裁剪
- `image.smartcrop(width, height, options?)` — 智能裁剪
- `image.rotate(angle, options?)` — 旋转
- `image.flip(direction)` — 翻转
- `image.flipHor()` / `image.flipVer()` — 水平/垂直翻转

**色彩处理：**
- `image.colourspace(space, options?)` — 色彩空间转换

**滤镜：**
- `image.gaussblur(sigma, options?)` — 高斯模糊
- `image.sharpen(options?)` — 锐化
- `image.conv(mask, options?)` — 任意卷积

**输出：**
- `image.writeToBuffer(formatString)` — 输出到 Uint8Array（关键 API）
- `image.writeToFile(path)` — 写入文件
- `image.writeToMemory()` — 写入内存

---

## 4. 浏览器要求

### 4.1 WebAssembly SIMD（必需）

wasm-vips 要求浏览器支持 WebAssembly SIMD（单指令多数据流），这是 Baseline 2023 的一部分。

| 浏览器 | 最低版本 | 说明 |
|--------|----------|------|
| Chrome | 91+ | V8 引擎 |
| Firefox | 89+ | SpiderMonkey 引擎 |
| Safari | 16.4+ | JavaScriptCore 引擎 (WebKit 615.1.17) |
| Edge | 91+ | Chromium 内核 |
| Node.js | 16.4.0+ | — |
| Deno | 1.9.0+ | — |

**对 PicEte 的影响：** 当前 PicEte 使用 Canvas API，兼容性更广。wasm-vips 会放弃对老旧浏览器的支持（主要是 iOS < 16.4，Safari < 16.4）。

### 4.2 SharedArrayBuffer + 跨域隔离（必需）

wasm-vips 的多线程实现依赖 `SharedArrayBuffer` API。

**网站必须设置以下 HTTP 头：**（同时作用于主文档和 `vips*.js` 脚本）

```http
Cross-Origin-Embedder-Policy: require-corp
Cross-Opener-Opener-Policy: same-origin
```

**对 PicEte 的影响：**
- 当前 picete.com 部署在 Vercel，需要在 `vercel.json` 中添加 headers 配置
- COEP/COOP 配置会限制跨域资源加载 — 所有外部资源（如分析脚本、字体）必须显式设置 CORS 或 `Cross-Origin-Resource-Policy: cross-origin`
- 如果无法启用跨域隔离，wasm-vips 提供了 `workaroundCors: true` 配置选项（参见 issue #12），但可能有性能降级

### 4.3 显式资源管理（可选）

示例代码中使用 `using` 关键字（TC39 Stage 3）进行资源管理：
```js
using im = vips.Image.newFromFile('owl.jpg');
```

如果不转译，需要：
- Chrome / Edge：默认支持
- Firefox / Safari：需要标志启用
- Node.js：`--js-explicit-resource-management` CLI 标志

**替代方案：** 可以手动调用 `im.delete()` 或 `im.deleteLater()`，不强制使用 `using`。

---

## 5. CDN 可用性

`wasm-vips` 已发布到 npm，理论上可通过以下 CDN 加载：

### jsDelivr
```
https://cdn.jsdelivr.net/npm/wasm-vips@0.0.17/lib/vips-es6.js
https://cdn.jsdelivr.net/npm/wasm-vips@0.0.17/lib/vips.wasm
```

### unpkg
```
https://unpkg.com/wasm-vips@0.0.17/lib/vips-es6.js
https://unpkg.com/wasm-vips@0.0.17/lib/vips.wasm
```

### CDN 使用注意事项

1. **WASM 文件必须与 JS 入口同域或正确配置 CORS** — `vips.js` 使用相对路径加载 `vips.wasm`，因此从 CDN 加载时 JS 和 WASM 必须从同一个 CDN 域名提供服务且路径关系保持一致。

2. **动态库加载问题** — `vips-jxl.wasm` 和 `vips-heif.wasm` 作为 `dynamicLibraries` 自动加载，它们同样使用相对路径解析。可以从 CDN 根 URL 提供服务，或通过 `locateFile` 回调自定义路径。

3. **跨域隔离头** — 即使使用 CDN，主站点仍需要设置 COOP/COEP 头。CDN 提供的 `vips*.wasm` 文件需要设置正确的 CORS 头或 `Cross-Origin-Resource-Policy: cross-origin`。

4. **PicEte 推荐方案** — 由于 WASM 文件较大（核心 5.7 MB），**建议自托管在 Vercel 的 /lib/ 目录下**，而不是依赖 CDN。这样可以确保相对路径加载不出问题，也避免 CDN 缓存版本不一致。

---

## 6. Node.js 使用方式

```js
// CommonJS
const Vips = require('wasm-vips');
const vips = await Vips();
console.log(vips.version()); // '8.18.1'

// ES Modules
import Vips from 'wasm-vips';
const vips = await Vips();
```

初始化配置可传入 Emscripten 模块选项：
```js
const vips = await Vips({
  print: (msg) => console.log('[vips]', msg),
  printErr: (msg) => console.error('[vips]', msg),
  locateFile: (url) => '/custom/path/' + url,
  workaroundCors: false,
  dynamicLibraries: ['vips-jxl.wasm', 'vips-heif.wasm'], // 默认
});
```

---

## 7. 浏览器使用方式

### 传统 Script 标签
```html
<script src="lib/vips.js"></script>
<script>
  const vips = await Vips();
</script>
```

### ES Module
```html
<script type="module">
  import Vips from './lib/vips-es6.js';
  const vips = await Vips();
</script>
```

### 关键实现细节（来自 vips.js 源码分析）

- `vips.js` 是 Emscripten 编译产物，使用 IIFE 模式，返回一个 async 工厂函数
- 入口自动检测浏览器环境 (`globalThis.window`) 和 Web Worker 环境
- WASM 通过 `fetch(url, { credentials: 'same-origin' })` 加载，失败时回退到 `XMLHttpRequest`
- 使用 Web Workers 池实现多线程（`navigator.hardwareConcurrency` 决定线程数，上限 6）
- 通过 `postMessage` 在 worker 和主线程间通信

---

## 8. 对 PicEte 的关键影响

| 方面 | 评估 |
|------|------|
| **性能** | ✅ 显著提升 — wasm-vips 使用 libvips 的 C++ 原生 pipeline，多线程并行处理，比 Canvas API 快数倍到数十倍 |
| **内存** | ✅ 更低 — pipeline 流式处理，不需将完整解压图像保留在内存中 |
| **功能覆盖** | ✅ 完全覆盖 — 格式转换/缩放/压缩/裁剪/旋转/翻转/取色都可实现 |
| **浏览器兼容** | ⚠️ 放弃 < Chrome 91 / < Safari 16.4 支持（需确认目标用户） |
| **部署复杂度** | ⚠️ 需要设置 COOP/COEP 头（Vercel vercel.json 配置） |
| **包体积** | ⚠️ 核心 WASM 5.7 MB，总 WASM ~14 MB，初始加载时间增加 |
| **Canvas 取色** | 取色功能可能需要保留 Canvas API 作为备选，或使用 wasm-vips 的 `writeToMemory()` 获取像素数据后自行绘制 |

---

## 9. 注意事项 / 已知问题

1. **wasm-vips 仍处于早期开发阶段**（v0.0.17），API 可能发生变化。跟踪 Issue #1。
2. **`using` 语法**是可选功能，非必需。可以手动调用 `delete()`。
3. **图片格式支持**由 WASM 动态库决定。如果不需要 HEIF/JPEG XL 支持，可以设置 `dynamicLibraries: []` 减少加载体积。
4. **Text / SVG 渲染**：`vips-resvg.wasm` 用于 SVG 渲染和文本处理，如果不需要可以排除。
5. **调试输出**：可以通过 `print` / `printErr` 配置选项捕获 libvips 的日志。
6. **线程模型**：wasm-vips 使用 Emscripten pthread 实现多线程，Workers 由 `vips.js` 内部管理。Worker 的加载需要 `vips.js` 自身 URL 可解析。
