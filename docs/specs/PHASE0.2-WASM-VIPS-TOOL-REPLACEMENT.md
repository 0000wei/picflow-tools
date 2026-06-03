# Phase 0.2: wasm-vips Tool Core Logic Replacement

> **创建日期:** 2026-06-03（补写）
> **状态:** Task 0.2.1 ✅, 0.2.2 ✅ (已修复浏览器API), 0.2.3-0.2.5 ⏳

## 背景

PicEte 当前所有工具页使用 Canvas API 进行图片处理。Canvas 的限制包括：无损格式（PNG/WebP）无压缩率控制、JPEG 质量调节不精确、大图处理受限。wasm-vips POC（Phase 0.0）已验证其在 Node.js 端可用。

## 范围

### 替换清单

| Task | 目标工具页 | 替换内容 | 状态 |
|------|-----------|---------|------|
| 0.2.1 | — | 创建 `js/vips-loader.js`（共享加载器） | ✅ `9589b57` |
| 0.2.2 | `compress-image/` | `compressImages()` 核心逻辑 | ✅ `bf7d6c8` + `bd3c1b5`（API修复） |
| 0.2.3 | `resize-image/` | `resizeImages()` 核心逻辑 | ⏳ |
| 0.2.4 | `split-image/` | `splitImage()` 核心逻辑 | ⏳ |
| 0.2.5 | color-picker / base64 | 评估是否替换 | ⏳ |

### 禁止范围

- 不修改 UI 展示代码（display, format, download 函数）
- 不修改文件上传/预览逻辑
- 不修改多语言文件（只修改英文根目录工具页）

## 技术方案

### 浏览器端 wasm-vips API（已验证通过）

```
vips.ImageSource.newFromBuffer(uint8Array)  → ImageSource
vips.Image.newFromSource(source, '')         → Image
image.writeToBuffer('.jpg', { Q: 85 })       → Uint8Array
image.writeToBuffer('.png')                   → Uint8Array
source.delete()   // 必须手动释放
image.delete()    // 必须手动释放
```

**与 Node.js 的差异（容易踩坑）：**
- Node.js: `vips.Image.newFromBuffer(buf)` — 浏览器端**不存在**
- 浏览器: `vips.ImageSource.newFromBuffer(buf)` + `vips.Image.newFromSource(source, '')`
- 必须手动调用 `.delete()` 释放 WASM 内存，否则泄漏

### WASM bundle 情况

| 文件 | 大小 | 来源 | git? |
|------|------|------|------|
| `js/lib/vips.js` | 89KB | `node_modules/wasm-vips/lib/vips.js` | ❌ .gitignore |
| `js/lib/vips.wasm` | 5.7MB | `node_modules/wasm-vips/lib/vips.wasm` | ❌ .gitignore |
| `js/lib/vips-heif.wasm` | 4.5MB | `node_modules/wasm-vips/lib/vips-heif.wasm` | ❌ .gitignore |

部署时从 `node_modules/` 复制（Vercel build 阶段）。

## 验证标准

每个 Task 必须验证：
1. ✅ `<script src="/js/vips-loader.js">` 在 `<head>` 中
2. ✅ `VipsLoader.load()` 调用
3. ✅ 浏览器端正确的 API（`ImageSource.newFromBuffer` + `newFromSource`）
4. ✅ Canvas 降级路径保留
5. ✅ UI 函数未修改（通过 grep 确认原函数名引用计数）
6. ✅ `make verify` + `make lint` 通过
7. ✅ git commit 范围干净（只改目标文件）
8. ✅ 无 WASM 二进制文件混入 commit

## 风险评估

| 风险 | 概率 | 缓解 |
|------|------|------|
| 浏览器端 API 与 Node.js 不同 | **已确认** | ✅ 已修复 compress-image，后续 Task 预见性写入正确的 API |
| 手动 delete() 遗漏导致 WASM 内存泄漏 | 中 | 代码 review 时确认每个路径都有 delete |
| COOP/COEP header 在CDN缓存下不生效 | 已解决 | COOP-COEP-DEPLOY-VERIFICATION.md 已确认通过 |
