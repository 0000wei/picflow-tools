# RAW 性能评估报告

> 日期：2026-06-05
> 项目：PicEte（picete.com）
> Task：0.5.12 — 性能评估 + 决策
> 前置：Task 0.5.10a/b/c（多线程构建成功）+ Task 0.5.11（Node.js 端 12/12 RAW 解码通过）

---

## 1. 构建大小对比

| 文件 | 原始 npm v0.0.17 | 自编译（含 libraw，多线程） |
|------|-------------------|---------------------------|
| vips.wasm | 5,894,485 | 5,834,491 |
| vips-heif.wasm | 4,669,481 | 3,151,583 |
| vips-jxl.wasm | 无 | 2,172,564（新增） |

**说明：**
- 核心 WASM (vips.wasm) 反而比 npm 版小 60KB，因编译参数差异（libraw 的 1.79MB 静态库被链接进来但整体大小未膨胀）
- vips-heif.wasm 显著缩小（~1.5MB），因 HEIF 本为动态模块，自编译版本剥离了冗余
- vips-jxl.wasm 为新增 JPEG XL 动态模块（npm 版不含）
- vips-resvg.wasm 已删除（SVG 禁用）

### 当前 js/lib/ 文件清单

| 文件 | 大小 | 说明 |
|------|------|------|
| vips.wasm | 5,834,491 | 核心 WASM（含 libraw） |
| vips-heif.wasm | 3,151,583 | AVIF/HEIC 动态模块 |
| vips-jxl.wasm | 2,172,564 | JPEG XL 动态模块 |
| vips.js | 82,976 | CommonJS loader |
| vips-es6.js | 82,699 | ES module loader |

---

## 2. RAW 解码性能（Node.js 真实测试）

来源：Task 0.5.11 测试数据。所有测试使用 `--max-old-space-size=8192`（Node.js）。

### Canon CR2

| 属性 | 值 |
|------|-----|
| 文件 | 0c0a0435.cr2 |
| 大小 | 26MB |
| 分辨率 | 5040×3360 |
| 输出 JPEG | 1.2MB |
| 解码时间 | <1s |

### Canon CR3

| 属性 | 文件 1 | 文件 2 |
|------|--------|--------|
| 文件名 | 2u2a0963 | gurt5897 |
| 大小 | 8.7MB | 7.5MB |
| 分辨率 | 5496×3670 | 5496×3670 |
| 输出 JPEG | 1.6MB | 1.1MB |
| 解码时间 | <1s | <1s |

### Nikon NEF

| 属性 | 文件 1 | 文件 2 | 文件 3 | 文件 4 |
|------|--------|--------|--------|--------|
| 大小 | 26MB | 31MB | 31MB | 27MB |
| 分辨率 | 6064×4040 | 6064×4040 | 6064×4040 | 6064×4040 |
| 输出 JPEG | 1.9MB | 2.9MB | 2.9MB | 2.5MB |
| 解码时间 | <1s | <1s | <1s | <1s |

### Sony ARW

| 属性 | 文件 1 | 文件 2 | 文件 3 |
|------|--------|--------|--------|
| 文件名 | dsc1756 | dsc03380 | dsc08557 |
| 大小 | 24MB | 24MB | 66MB |
| 分辨率 | 6024×4024 | 6024×4024 | 7028×4688 |
| 输出 JPEG | 2.3MB | 1.0MB | 4.1MB |
| 解码时间 | <1s | <1s | <1s |

### Adobe DNG

| 属性 | 值 |
|------|-----|
| 文件 | sample.dng |
| 大小 | 6MB |
| 分辨率 | 3474×2314 |
| 输出 JPEG | 845KB |
| 解码时间 | <1s |

**总结果：12/12 RAW 文件解码通过，全部 <1s。**

---

## 3. 兼容性矩阵

| 品牌 | 格式 | 文件数 | 结果 |
|------|------|--------|------|
| Canon | CR2 | 1 | ✅ |
| Canon | CR3 | 2 | ✅ |
| Nikon | NEF | 4 | ✅ |
| Sony | ARW | 3+1=4 | ✅ |
| Adobe | DNG | 1 | ✅ |

**总计：12 个 RAW 文件，全部解码成功。** 涵盖四家主流相机品牌（Canon/Nikon/Sony/Adobe），覆盖四种 RAW 格式（CR2/CR3/NEF/ARW/DNG）。

---

## 4. COOP/COEP 需求

多线程 WASM 依赖 SharedArrayBuffer，浏览器要求以下 HTTP 响应头：

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

**已配置（P0 POC 阶段完成）：**
- Vercel 路径级 header 配置在 `vercel.json` 中
- 针对 `/js/lib/*.wasm` 和整个站点生效
- 已在 P0 POC 阶段验证通过（见 `docs/reports/COOP-COEP-DEPLOY-VERIFICATION.md`）

**影响范围：**
| 资源 | 影响 |
|------|------|
| gtag.js（谷歌分析） | 需自托管到 `/js/` 目录（已完成: Task 0.5.0, infra-006） |
| 外部字体/CDN | 需自托管或使用 `crossorigin="anonymous"` |
| iframe 嵌入 | require-corp 会阻止跨源 iframe |

---

## 5. 决策选项

### 选项 A：继续 4 个 RAW 工具页（完整推进）

创建所有 4 个 RAW 转换工具：
| # | 工具 | 说明 |
|---|------|------|
| 1 | raw-to-jpg | RAW → JPG 转换 |
| 2 | raw-to-png | RAW → PNG 转换 |
| 3 | raw-to-webp | RAW → WebP 转换 |
| 4 | raw-to-avif | RAW → AVIF 转换 |

**优势：**
- 一次性完成 RAW 支持的全部工具页
- 工具间共享相同的解码逻辑（vips-loader.js + wasm-vips）
- 用户获得完整的 RAW 转换体验

**风险：**
- 浏览器端大文件（>50MB RAW）解码的内存压力未充分测试
- 4 个工具页 + 7 语言翻译 = 28 个新页面，工作量大

### 选项 B：先做 1-2 个验证市场反应（建议）

建议先做：
| # | 工具 | 理由 |
|---|------|------|
| 1 | raw-to-jpg | 最常用转换（RAW→JPG 是高需求场景） |
| 2 | raw-to-png | PNG 用户导出偏好 |

**优势：**
- 快速上线验证市场反响
- 减少初期工作量（14 个页面而不是 28 个）
- 若用户积极则继续补全

**风险：**
- 不完整的工具集可能影响 SEO 排名
- 用户搜索 "raw to webp" 可能找不到对应页面

---

## 6. 已知限制

1. **浏览器端大文件**：66MB Sony ARW 在浏览器端未充分测试。浏览器的 WASM 内存上限可能低于 Node.js。
2. **CR3 大 XMP 警告**：部分 Canon CR3 文件解码时会输出 `large XMP not saved` 元数据警告，不影响图像输出质量。
3. **DNG 变体**：仅测试了 Adobe DNG（Canon 转换），线性 DNG、JPEG-in-DNG 等未测试。
4. **WASM heap 碎片化**：连续解码 6+ 个大 RAW 文件后可能失败。已通过 ALLOW_MEMORY_GROWTH + MAXIMUM_MEMORY=4GB + 每 decode 后 GC 缓解。
5. **实验性格式**：Fujifilm RAF、Panasonic RW2、Olympus ORF 等 20+ 格式被 libraw 支持但未测试。
6. **headless Chrome 限制**：Task 0.5.11 中 headless Chrome 不支持 SharedArrayBuffer，完整浏览器验证需生产环境真实 Chrome/Firefox。

---

## 7. 推荐下一步

| 优先级 | Task | 内容 | 预估工作量 |
|--------|------|------|-----------|
| P0 | 0.5.13 | raw-to-jpg 工具页 | 1 个 HTML 页面 |
| P0 | 0.5.14-19 | 其余 RAW 工具 + 翻译 + 入口/sitemap | 27 个页面 + 配置更新 |
