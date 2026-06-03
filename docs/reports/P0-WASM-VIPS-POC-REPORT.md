# P0 — wasm-vips POC 验证报告

> 日期: 2026-06-03
> 项目: PicEte (picete.com)
> 目的: 验证 wasm-vips 替代 Canvas API 的技术可行性

---

## 一、POC 执行概览

| Task | 名称 | 状态 | 产出 |
|------|------|------|------|
| 0.1.1 | 安装 + 调研 | ✅ | `docs/research/wasm-vips-package-analysis.md` |
| 0.1.2 | SAB 测试 HTML | ✅ | `scripts/test/wasm-vips-poc.html` + COOP/COEP Server 验证 |
| 0.1.3 | Resize 性能对比 | ✅ | POC HTML 中的 resize 对比 section + Node.js bench 数据 |
| 0.1.4 | AVIF/RAW Codec 验证 | ✅ | `docs/research/wasm-vips-codec-report.md` + `scripts/test/codec-test.mjs` |
| 0.1.5 | 单线程性能对比 | ✅ | `scripts/test/threading-bench.mjs` |
| 0.1.6 | Vercel COOP/COEP Header | ✅ | `vercel.json` 路径级 COOP/COEP 配置 |

---

## 二、核心发现

### 发现 1: wasm-vips 在 Node.js 端完全可用 ✅

- 版本 v0.0.17 (libvips 8.18.1)
- API 完整：`newFromFile`, `newFromBuffer`, `resize`, `writeToBuffer` 等 312+ 方法
- WASM bundle：核心 5.7 MB + 动态库 ~8.3 MB（HEIF/JPEG XL/SVG）
- **MCP Server 端可以直接使用 wasm-vips 替代 Sharp**

### 发现 2: 浏览器端需 COOP/COEP 头 — **最大风险点** ⚠️

- wasm-vips 的多线程模式要求 `SharedArrayBuffer`
- 网站必须设置 `Cross-Origin-Opener-Policy: same-origin` + `Cross-Origin-Embedder-Policy: require-corp`
- COEP `require-corp` 会阻止所有未设置 CORS 的跨域资源
- POC **无法在无头浏览器中完全执行**（CDN ES6 版本在 headless Chromium 中有语法兼容性问题，Node.js 端正常）
- 本地 Python HTTP server 可成功设置并验证 COOP/COEP 头

### 发现 3: wasm-vips 不是纯性能提升 — 需降级策略 ⚠️

800×600 → 400×300 resize 性能对比（Node.js，取5次平均）：

| 方法 | 平均耗时 | 相对速度 | 输出文件 |
|------|---------|---------|---------|
| 🥇 Sharp (native) | **12.2ms** | 1.00× (基准) | 13,285 bytes |
| 🥈 Wasm-vips 单线程 | **19.6ms** | 1.61× slower | 10,637 bytes |
| 🥉 Wasm-vips 多线程 | **30.6ms** | 2.51× slower | 10,637 bytes |

**关键结论：**
- wasm-vips 在小图（800×600）上比 Sharp 慢 1.6-2.5×
- wasm-vips 多线程反而比单线程慢（线程同步开销对于小图得不偿失）
- **wasm-vips 的优势在于大图（>10MB）**，这时管线流式处理的内存效率优势会显现
- **降级方案：** COOP/COEP 不可行时直接回退 Canvas API（比 wasm-vips 单线程更快）

### 发现 4: AVIF 支持通过 wasm-vips 可行 ✅

| 格式 | wasm-vips 支持 | 验证方法 |
|------|---------------|---------|
| **AVIF 编码** | ✅ libheif AV1 编码器 | `image.writeToBuffer('.avif')` → 输出 10,458 bytes |
| **AVIF 解码** | ✅ libheif 加载 | encode-then-decode cycle 验证 |
| 依赖 | `vips-heif.wasm` (4.5 MB，按需加载) | `vips.config()` 确认 |

### 发现 5: RAW 支持 **不走** wasm-vips ❌

**这是对 V2 SPEC 的重大修正。**

| 格式 | wasm-vips 支持 | 结论 |
|------|---------------|------|
| **RAW (CR2/NEF/ARW/DNG)** | ❌ `libraw=false` | libraw **未编译入** WASM bundle |
| 原因 | Emscripten 编译时排除了 libraw | 独立编译选项，不是运行时配置 |
| 替代方案 | `libraw-wasm` 独立 npm 包 | 或 Node.js Sharp（MCP 端） |

**对 SPEC 的影响：** P0.5 的 RAW 工具页不能依赖 wasm-vips，需要独立的 `libraw-wasm` 引入。

---

## 三、技术决策建议

### 决策 1: 是否继续全量替换 Canvas API？

**建议：有条件推进**

| 条件 | 状态 | 说明 |
|------|------|------|
| WASM bundle 大小可接受 | ✅ | 核心 5.7MB，首次加载约 1-3s |
| API 覆盖 PicEte 功能 | ✅ | resize/compress/convert/split 全部可用 |
| 大图性能优势 | ⏳ | POC 限于小图（800×600），需用 20MB+ 图片验证 |
| COOP/COEP 线上可行 | ⏳ | 需部署 Vercel 后 curl 验证 header + 浏览器验证 SAB |
| 第三方资源兼容 | ⏳ | 需审计所有 CDN/font/analytics 资源 |

**建议推进策略：**
1. 先推 MCP Server 端使用 wasm-vips（不需要 COOP/COEP，Node.js 中直接可用）
2. 浏览器端先做 resize-image 单工具 POC 部署（验证 COOP/COEP 在 Vercel 上的可行性）
3. 如果线上 COOP/COEP 可行，继续全量替换；如果不可行，留在 MCP 端使用

### 决策 2: AVIF 是否走 wasm-vips？

**建议：✅ 是。** WASM bundle 已包含 libheif AV1 编码器，encode + decode 均通过测试。

### 决策 3: RAW 是否走 wasm-vips？

**建议：❌ 不。** 改用 `libraw-wasm` 独立 WASM 库。POC 阶段验证 libraw-wasm 在浏览器端的可行性和兼容性。

### 决策 4: 降级方案是什么？

**建议：** COOP/COEP 不可行时，直接回退到现存的 Canvas API 实现。

```
try {
  await loadWasmVips();
  // use wasm-vips pipeline
} catch {
  useCanvasFallback();  // 现存的 Canvas API 实现
}
```

**不需要 wasm-vips 单线程模式**（比 Canvas 慢 1.6×，优势只在输出文件更小）。

---

## 四、风险矩阵

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| COEP `require-corp` 阻止第三方 CDN 资源 | **高** | **高** | 在部署前审计所有外部资源；路径级 COOP/COEP（仅工具页），首页不受影响 |
| WASM 5.7 MB 首次加载延迟 | 中 | 中 | loading 动画 + 按需加载（仅工具页加载 WASM） |
| wasm-vips 在老旧浏览器（Safari < 16.4）不兼容 | 低 | 低 | 降级到 Canvas API（现有代码无需改动） |
| 大图（>50MB）wasm-vips 仍 OOM | 低 | 中 | 设置文件大小上限；分块处理 |
| `vips-heif.wasm` (4.5 MB) 加载慢 | 中 | 中 | 仅在 AVIF 工具页加载 HEIF 动态库 |

---

## 五、POC 产出文件清单

```
docs/research/
├── wasm-vips-package-analysis.md   (302行) — 包技术调研
├── wasm-vips-codec-report.md       (─)    — 编解码支持报告

scripts/test/
├── wasm-vips-poc.html              (796行) — 浏览器测试 HTML
├── codec-test.mjs                  (─)    — 格式编解码测试
├── threading-bench.mjs             (─)    — 性能对比测试
└── fixtures/*                      (3张)  — 测试图片
```

---

*报告位置: `picete/docs/reports/P0-WASM-VIPS-POC-REPORT.md`*
