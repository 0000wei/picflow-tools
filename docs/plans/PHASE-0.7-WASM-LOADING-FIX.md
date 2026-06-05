# PicEte Phase 0.7: WASM 加载修复 & 生产环境验证计划

## 背景

### 1. 当前架构

所有需要 wasm-vips 的工具页（compress-image, resize-image, avif-to-png, raw-to-jpg 等）的 WASM 加载流程：

```
工具页 index.html
  └── <script src="/js/vips-loader.js">   ← 唯一引用
        └── VipsLoader.load()
              ├── 检查 crossOriginIsolated / SAB
              ├── 如果 window.Vips 存在 → 直接使用（但当前没有页面设置 window.Vips）
              └── 否则 → import('/js/lib/vips-es6.js')
                    └── Vips() 返回 wasm-vips 实例
```

### 2. 已发现的问题

**问题 A：`.gitignore` 排除了 WASM 文件（已修复 ✅）**
- 根因：`.gitignore` 包含 `js/lib/vips*.wasm` 和 `js/lib/vips*.js`
- 修复：`git add -f` 强制执行 + commit + push
- 状态：`https://picete.com/js/lib/vips.js` 现在返回 200

**问题 B：`vercel.json` 的 COOP/COEP header 未覆盖 RAW 工具（已修复 ✅）**
- 根因：regex 只包含旧工具列表
- 修复：加入 `raw-to-jpg|raw-to-png|raw-to-webp|raw-to-avif`，同时增加多语言版本
- 状态：`curl -I` 显示 `cross-origin-opener-policy: same-origin` 和 `cross-origin-embedder-policy: require-corp`

**问题 C：VipsLoader 的动态 import 在 COEP 环境下失败（未修复 ❌）**
- 根因：VipsLoader 第 43 行 `import('/js/lib/vips-es6.js')` 在 `Cross-Origin-Embedder-Policy: require-corp` 环境下失败
- 影响：所有工具页（compress, resize, avif, raw 等）在生产环境均无法加载 WASM
- CDP 验证结果：`typeof Vips = "function"`（手动注入 script 后可加载），但 VipsLoader 的动态 import 路径不通

**问题 D：headless Chrome 无法完成完整 WASM 初始化（已知限制 ⚠️）**
- 根因：headless Chrome 对 SharedArrayBuffer + 多线程 WASM 支持不完全
- SPEC 已记录（Task 0.5.11 第 1054 行）
- 影响：CDP 端到端测试无法在 headless 模式下完成

---

## 解决方案

### 方案一：页面直接引用 vips.js（替换动态 import）✅ 推荐

**原理：** 不再依赖动态 `import()`，而是在页面 `<head>` 中用 `<script src="/js/lib/vips.js" defer>` 预加载。VipsLoader 的第 39 行 `var Vips = window.Vips` 自然能找到已加载的库。

**改动量：**
1. `vips-loader.js`：第 40-48 行的动态 import fallback 可以保留（作为兜底），但不再是主要路径
2. 4 个 EN 工具页（raw-to-jpg/png/webp/avif）的 `<head>`：添加 `<script src="/js/lib/vips.js" defer>` 在 vips-loader.js 之前
3. 4 个已有工具页（avif-to-png, png-to-avif, jpg-to-avif, webp-to-avif）：同样需要添加（它们也是靠动态 import，同样在 COEP 环境下失败）
4. 28 个翻译页的 `<head>`：同样添加

**优点：**
- 改动简单，每页加一行 `<script>` 标签
- 不改变 VipsLoader 的返回接口（对业务代码无影响）
- 兼容降级路径：如果 script 加载失败（js/lib 文件不存在），VipsLoader 的动态 import 仍在

**缺点：**
- 需要改 36+ 个文件
- 每个页面都预加载 6MB WASM（但这对 wasm-vips 本身是 lazy init，`<script>` 只加载 JS bundle，不初始化 WASM）

**影响范围：** 所有 wasm-vips 工具页（36+ 页）

---

### 方案二：修正 VipsLoader 的 import 路径（不推荐）

**原理：** 找出动态 import 在 COEP 下失败的具体原因，调整 import URL 或加载方式。

**风险：**
- 这是 Emscripten 生成的 vips-es6.js 内部行为，外部无法控制
- 根本原因是 ES Module 动态 import + WASM 动态模块在 COEP require-corp 下的浏览器行为
- 调试成本高，且可能无解

---

### 方案三：服务端配置 .wasm 文件的 CORP header

**原理：** 在 Vercel 上为 .wasm 文件添加 `Cross-Origin-Resource-Policy: cross-origin` 头。

**现状：** 同源请求本不需要 CORP 头，所以这不会解决 ES Module import 的问题。且 vercel.json 已经配置了 .wasm 的 CORS（之前测试 `vips.wasm` 返回 `access-control-allow-origin: *`）。

---

## 实施计划（选项 C → A）

### 实施注意（极易踩坑的工程细节）

#### 1. defer 的执行时序与 Emscripten currentScript 限制
必须使用**非 defer** 加载 vips.js，因为 Emscripten 生成的胶水代码依赖 `document.currentScript.src` 来定位同目录下的 WASM 和 Worker 文件。defer 脚本中 `document.currentScript` 为 null。

```html
<script src="/js/lib/vips.js"></script>              ← 同步加载（Emscripten 需要 currentScript）
<script src="/js/vips-loader.js" defer></script>      ← defer（VipsLoader 在 vips.js 之后执行）
```

vips.js 只有几十 KB JS 胶水代码，**不会触发 WASM 下载**（WASM 在调用 Vips() 时才下载），同步加载对首屏性能影响极小。

#### 2. Emscripten 相对路径寻址
vips.js（胶水代码）初始化时会自动在同目录下寻找 `vips.wasm` 和潜在 Worker 文件。
确保 Vercel 产物中 `vips.wasm` 和 `vips.js` 在**同一目录** `/js/lib/`，且没有被 Vercel Rewrite 规则干扰。当前已验证 `https://picete.com/js/lib/vips.js` 200，`vips.wasm` 200。

#### 3. 超时机制的正确实现
使用 `Promise.race` 而非 setTimeout + 标志位：

```js
const initVips = Vips();
const timeout = new Promise((_, reject) =>
  setTimeout(() => reject(new Error('VIPS_INIT_TIMEOUT')), 30000)
);
const vipsInstance = await Promise.race([initVips, timeout]);
```

#### 4. Headless Chrome 的局限性
headless Chrome 在 WASM + Web Worker 多线程场景下经常静默挂起。如果 CDP 验证卡在 Promise pending 状态超过 30 秒，**立即切换到真实桌面 Chrome + DevTools**，不要恋战。

---

### C-1: 修改 vips-loader.js（加超时 + 确保 window.Vips 优先）

| 步骤 | 内容 | 文件数 | 耗时 |
|------|------|--------|------|
| 1 | `vips-loader.js`：在 load() 方法中，将动态 import 改为优先使用 window.Vips（当前逻辑已有，但需要确保 Vips() 被调用时加入超时机制） | 1 | 5 分钟 |
| 2 | **4 个 EN 工具页**（avif-to-png, png-to-avif, jpg-to-avif, webp-to-avif）：在 `<head>` 中添加 `<script src="/js/lib/vips.js" defer>` | 4 | 5 分钟 |
| 3 | **4 个 RAW EN 工具页**（raw-to-jpg/png/webp/avif）：同样添加 | 4 | 5 分钟 |
| 4 | **28 个翻译页**：通过脚本批量添加 `<script src="/js/lib/vips.js" defer>` 到所有语言版本的对应工具页 | 28 | 5 分钟 |
| 5 | **4 个已存在的翻译工具页**（avif-to-png 等 AVIF 翻译页）：同样添加 | 28 | 5 分钟 |
| 6 | vips-loader.js 增加超时机制：Vips() 调用超过 30 秒标记为 error 并返回 null（避免页面永久卡住） | 1 | 5 分钟 |
| 7 | commit + push → 触发 Vercel 部署 | — | 2 分钟 |
| 8 | CDP 验证：确认 crossOriginIsolated + SAB + Vips() 初始化成功 | — | 10 分钟 |
| 9 | **真实浏览器验证**：在桌面 Chrome 中上传一个 DNG 文件测试完整 RAW→JPG 流程 | — | 用户协作 |
| **合计** | **36+ 文件** | | **~42 分钟** |

---

## 选项

**A. 方案一全部执行**（推荐）——覆盖所有 wasm-vips 工具页，一次修复所有工具的生产环境 WASM 加载

**B. 只修复 RAW 工具页**——缩小范围，先让用户能上传 RAW，其他工具（avif/compress/resize）后续再修

**C. 先验证方案一在小范围可行**——只改 raw-to-jpg 一个文件 + 加超时，CDP 验证通过后再铺开

你倾向哪个？
