# 会话交接文档 — PicEte RAW WASM 加载问题

> 日期: 2026-06-05 14:00
> 项目: PicEte (picete.com)
> 路径: /home/wu/桌面/knowledge-base/06项目/哥飞建站/picete/

---

## 一、问题综述

用户无法在 RAW 工具页（raw-to-jpg/png/webp/avif）上传和转换 RAW 文件。
点击"Convert to JPG"按钮后，`VipsLoader.load()` 失败，30 秒超时后抛出 `VIPS_INIT_TIMEOUT`。

---

## 二、已修复的问题（3 个，全部已部署到生产环境）

### 修复 1: COOP/COEP header 未覆盖 RAW 工具 (commit `3965f9e`)

**问题：** vercel.json 的 header 规则 regex 只包含旧工具列表（resize-image, compress-image, avif-to-png 等），未包含 raw-to-jpg/png/webp/avif。

**修复：** 将 4 个 RAW 工具加入 regex。同时增加了多语言路径版本（/zh/raw-to-jpg/ 等）。

**验证：** `curl -sI https://picete.com/raw-to-jpg | grep -i cross-origin`
```
cross-origin-embedder-policy: credentialless
cross-origin-opener-policy: same-origin
```

### 修复 2: WASM 文件被 .gitignore 排除 (commit `2167b8f`)

**问题：** `.gitignore` 包含 `js/lib/vips*.wasm` 和 `js/lib/vips*.js`，导致 git 没有跟踪 WASM 文件。Vercel 部署后 `https://picete.com/js/lib/vips.js` 返回 404。

**修复：** `git add -f` 强制跟踪了 5 个文件：
- js/lib/vips.js (82KB) — Emscripten 胶水代码（非 ES6 版）
- js/lib/vips-es6.js (82KB) — ES module 版胶水代码
- js/lib/vips.wasm (5.8MB) — 核心 WASM（含 libraw）
- js/lib/vips-heif.wasm (3.1MB) — AVIF/HEIC 动态模块
- js/lib/vips-jxl.wasm (2.1MB) — JPEG XL 动态模块

**验证：** `curl -sI https://picete.com/js/lib/vips.js | head -1` → `HTTP/2 200`

### 修复 3: VipsLoader 缺少超时机制 (commit `2a812a7`)

**问题：** vips-loader.js 中 `Vips()` 调用没有超时。如果 WASM 初始化卡住，整个页面永久 pending。

**修复：** 在 vips-loader.js 的 load() 方法中，将 `var vips = await Vips();` 改为 Promise.race 模式：
```javascript
var initPromise = Vips();
var timeoutPromise = new Promise(function (_, reject) {
  setTimeout(function () { reject(new Error('VIPS_INIT_TIMEOUT')); }, 30000);
});
var vips = await Promise.race([initPromise, timeoutPromise]);
```

### 修复 4: COEP require-corp 改为 credentialless (commit `feee8ed`)

**问题：** require-corp 要求所有跨域资源设置 CORP 头，Worker 中加载 WASM 时触发额外限制。

**修复：** 将 vercel.json 中两处 `Cross-Origin-Embedder-Policy` 的值从 `require-corp` 改为 `credentialless`。credentialless 模式同样支持 SharedArrayBuffer，但不要求 Worker 的 CORP 头。

**验证：** `curl -sI https://picete.com/raw-to-jpg | grep -i embedder` → `cross-origin-embedder-policy: credentialless`

**已知：** 此修复部署后，VipsLoader.load() 仍然 VIPS_INIT_TIMEOUT。说明 Worker 内部的问题不完全是 COEP 引起的。

---

## 三、当前未解决的问题

### 问题描述
生产环境中 `VipsLoader.load()` 30 秒超时。`window.Vips` 函数存在（vips.js 已成功加载），但调用 `Vips()` 后 Promise 永远 pending。

### 当前行为
```
调用链：
  VipsLoader.load()
    → window.Vips 存在（来自 <script src="/js/lib/vips.js">）✅
    → const vips = await Vips()  // 这里卡住
      → Emscripten 初始化
        → 创建 Worker（new Worker 成功）
        → Worker 内部初始化失败（无信息错误）
        → 主线程 Atomics.wait 等待 Worker 就绪
        → 永远等不到 → 30 秒超时
```

### CDP 验证记录

| 时间 | 环境 | 操作 | 结果 |
|------|------|------|------|
| 12:53 | headless Chrome | 首次 CDP 连接生产环境 | `crossOriginIsolated: false` → 发现 COOP/COEP 未下发 |
| 12:56 | curl | 检查 header | 确认 vercel.json regex 缺失 RAW 工具 |
| 12:58 | Claude Code | 修复 vercel.json | commit + push |
| 13:00 | curl | 验证部署 | COOP/COEP header 生效 |
| 13:02 | headless Chrome | CDP 验证 | `crossOriginIsolated: true`, SAB: true, 但 VipsLoader.load() 动态 import 失败 |
| 13:05 | 分析 vips-loader.js | 发现动态 import 在 COEP 下失败 | 改为 `<script src="/js/lib/vips.js">` 方案 |
| 13:08 | Claude Code | 修改 raw-to-jpg + vips-loader.js | 超时，管理者直接 patch |
| 13:10 | 验证 | grep 确认修改正确 | vips.js 无 defer, vips-loader.js defer |
| 13:12 | commit + push | `2a812a7` | 部署 |
| 13:15 | 用户真实 Chrome | 运行 VipsLoader.load() | VIPS_INIT_TIMEOUT（30秒） |
| 13:18 | 用户提供 HAR 文件 | 分析 Network | 所有 WASM 文件 200（vips.wasm 5.8MB, heif 3.1MB, jxl 2.1MB） |
| 13:20 | 用户真实 Chrome | Worker 测试 | Worker 创建成功，抛出无信息错误 |
| 13:22 | headless Chrome | CDP Worker 测试 | Worker 创建成功，`WORKER_ERROR: undefined undefined undefined` |
| 13:25 | headless Chrome | fetch WASM 测试 | 主线程 fetch 5.8MB 成功；Worker 内 fetch 路径解析失败 |
| 13:28 | 决策 | 方向 A（单线程编译） | 查历史：9 次失败，libvips 内嵌 pthread |
| 13:30 | 决策 | 方向 D（COEP credentialless） | 改 vercel.json → commit + push |
| 13:35 | 用户真实 Chrome | 测试 | 仍然 VIPS_INIT_TIMEOUT |
| 13:40 | headless Chrome | CDP 验证 credentialless | `crossOriginIsolated: true`, Worker 仍然失败 |

### 关键诊断发现

1. **vips.js 是 Emscripten pthread（多线程）编译的**。这是 wasm-vips 的官方构建方式（参见 meson.build 第 94-107 行）。多线程版本依赖 Worker 线程来进行 WASM 初始化。

2. **Worker 创建本身成功**，`new Worker('/js/lib/vips.js', {name:'em-pthread'})` 返回 Worker 对象。

3. **Worker 在初始化时立即抛出未捕获错误**，没有任何 filename/lineno 信息（`undefined:undefined: undefined`）。这意味着错误发生在 Worker 的全局作用域执行的早期阶段——可能在 Emscripten 运行时初始化 WASM 导入对象或访问 WebAssembly 模块时。

4. **Worker 内 fetch 相对路径失败**：`fetch('/js/lib/vips.wasm')` 在 Worker 中返回 `Failed to parse URL from /js/lib/vips.wasm`，因为 Worker 的 location 是 Blob URL 而非页面 URL。Emscripten 生成的 Worker 代码使用 `self.location.href` 来解析 WASM 路径，在 Worker 中这是 Blob URL。

5. **单线程编译历史**：曾经尝试过 9 次，结论是"单线程不可行（libvips 内嵌 pthread API 调用）"。heif/jxl 动态模块的 meson 链接命令会自动追加 `-pthread` 和 `--shared-memory`，与单线程模式冲突。

6. **COEP credentialless 没有解决问题**：Worker 内部错误不是 COEP 导致的，而是路径解析和 WASM 初始化本身的问题。

---

## 四、未提交的修改

```
 M AGENTS.md              ← 新增"严格遵循 Harness Engineering"一句话
 M js/vips-loader.js      ← 30 秒 Promise.race 超时
?? docs/plans/PHASE-0.8-SINGLE-THREAD-BUILD.md   ← 计划文档（未完成）
```

---

## 五、下一步方向

### 方向 1（推荐优先尝试）: Vips() 传入 locateFile 参数

Emscripten 生成的胶水代码支持通过 options 参数传入 `locateFile` 回调函数。
在 vips-loader.js 的 load() 方法中修改调用方式：

```javascript
var vips = await Vips({
  locateFile: function(path) {
    return 'https://picete.com/js/lib/' + path;
  }
});
```

这个参数会影响：
- WASM 文件搜索路径（vips.wasm → 绝对 URL）
- 动态模块搜索路径（vips-heif.wasm, vips-jxl.wasm → 绝对 URL）

**之前尝试过但当时 COEP 还是 require-corp**，CDP 测试超时。现在 COEP 是 credentialless，环境不同，值得再试。

**工作量：** 改 1 个文件（vips-loader.js），5 分钟。
**验证：** 部署后在真实 Chrome 中运行 VipsLoader.load()。

### 方向 2: 自编译单线程版

再次尝试在 build.sh 中设 `-sUSE_PTHREADS=0` 编译单线程版。

**挑战：** 之前 9 次失败。但当时可能有些参数配置可以优化。
**工作量：** 30-60 分钟构建，不确定性高。

### 方向 3: 回退到 npm wasm-vips v0.0.17

npm 版是单线程的，已通过 POC 验证。但不含 libraw，RAW 无法解码。

**使用场景：** 如果方向 1 和 2 都失败，可以先用 npm 版让非 RAW 工具正常工作，RAW 工具页显示"当前浏览器不支持 RAW 解码"提示。

---

## 六、下一 Session 启动命令

```bash
cd /home/wu/桌面/knowledge-base/06项目/哥飞建站/picete
bash scripts/init.sh          # 健康检查 + git log + git status
make verify                   # 确认项目完整性
cat SESSION-HANDOFF-2026-06-05.md  # 读交接文档
```

---

## 七、关键链接

| 资源 | 路径 |
|------|------|
| 首页 | https://picete.com/ |
| RAW JPG 工具 | https://picete.com/raw-to-jpg/ |
| WASM 加载器 | https://picete.com/js/vips-loader.js |
| vips.js (胶水代码) | https://picete.com/js/lib/vips.js (200) |
| vips.wasm (核心) | https://picete.com/js/lib/vips.wasm (200, 5.8MB) |
| 编译脚本 | /tmp/wasm-vips/build.sh (备份在 picete/scripts/raw-build/) |
| 编译配置 | /tmp/wasm-vips/src/meson.build |
| Docker 镜像 | wasm-vips:latest (4.5GB) |

---

## 八、Session 结束时 git 操作

```bash
# 提交未完成的修改
git add AGENTS.md js/vips-loader.js docs/plans/PHASE-0.8-SINGLE-THREAD-BUILD.md
git commit -m "chore: session handoff — Harness Engineering statement + VipsLoader timeout + build plan"
git push origin master
```

**注意：** `SESSION-HANDOFF-2026-06-05.md` **不提交到 git**，只作为本地交接文件。
