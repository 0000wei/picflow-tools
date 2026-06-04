# RAW 兼容性清单

> 更新时间：2026-06-04
> 技术方案：自编译 wasm-vips（v0.0.17）+ LibRaw（0.22.1），Emscripten WASM
> 核心 WASM bundle：~5.8MB
> 构建记录：`docs/reports/RAW-BUILD-LOG.md`

## 四家主流 — 已验证可靠

### Canon

| 格式 | 机型 | 结果 | 解码时间 | 输出 | 备注 |
|------|------|------|---------|------|------|
| CR2 | EOS 5D Mark IV (26MB, 5040×3360) | ✅ 稳定 | ~5s | 1.2MB JPEG | 21 次测试全部通过 |
| CR3 | EOS R6 (8.7MB, 6000×4000) | ✅ 稳定 | ~5s | 1.6MB JPEG | 大 XMP 元数据警告，不影响解码 |
| CR3 | EOS R6 (7.5MB) | ✅ 稳定 | ~12s | 1.1MB JPEG | 另一设置下的 CR3 文件 |

### Nikon

| 格式 | 机型 | 结果 | 解码时间 | 输出 | 备注 |
|------|------|------|---------|------|------|
| NEF | Z6 (26MB, 6064×4040) | ✅ 稳定 | ~7s | 1.9MB JPEG | 21 次测试全部通过 |
| NEF | Z6 (27MB) | ✅ 稳定 | ~6s | 2.4MB JPEG | 不同设置 |
| NEF | Z6 (30MB) | ✅ 稳定 | ~9s | 2.8MB JPEG | 最大 NEF 文件 |
| NEF | Z6 (27MB) | ✅ 稳定 | ~9s | 2.0MB JPEG | |

### Sony

| 格式 | 机型 | 结果 | 解码时间 | 输出 | 备注 |
|------|------|------|---------|------|------|
| ARW | α7III / ILCE-7M3 (24MB, 6024×4024) | ✅ 稳定 | ~5s | 2.3MB JPEG | 21 次测试全部通过 |
| ARW | α7III / ILCE-7M3 v4.01 (24MB) | ✅ 稳定 | ~5-10s | 1.0MB JPEG | 之前不稳定→修复（MAXIMUM_MEMORY 4GB） |
| ARW | α6000 / ILCE-6000 (24MB) | ✅ 稳定 | ~5s | 2.7MB JPEG | 另一 Sony 机身 |
| ARW | α7CM2 / ILCE-7CM2 v1.02 (66MB) | ⚠️ Node.js OOM | — | — | 文件过大（66MB），Node.js 默认内存限制导致进程被杀。非 wasm-vips 问题。加 `--max-old-space-size=8192` 后预期可解 |

### Adobe DNG

| 格式 | 来源 | 结果 | 解码时间 | 输出 | 备注 |
|------|------|------|---------|------|------|
| DNG | Canon EOS 350D 转换 (6MB) | ✅ 稳定 | ~2s | 845KB JPEG | 21 次测试全部通过 |

## 实验性格式（未验证）

以下格式被 libraw 支持但 **未经实际文件测试**。理论可解码，但不保证在所有压缩变体（有损/无损/未压缩）下正常工作。

| 品牌 | 格式 | 说明 |
|------|------|------|
| Canon | CRW | 早期 Canon 格式 |
| Nikon | NRW | Nikon 压缩 RAW |
| Sony | SRF, SR2 | 早期 Sony 格式 |
| Fujifilm | RAF | 含 X-Trans 传感器特殊排列 |
| Panasonic | RW2 | 含 L 卡口联盟 |
| Olympus | ORF | |
| Pentax | PEF, PTX | |
| Leica | RAW, RWL | |
| Sigma | X3F | Foveon 传感器特殊格式 |
| Hasselblad | 3FR | |
| Phase One | IIQ | |
| Kodak | KDC, DCR | |
| Minolta | MRW | |
| Samsung | SRW | |
| Mamiya | MEF | |
| Leaf | MOS | |
| Epson | ERF | |
| Casio | BAY | |
| RED | R3D | |
| Blackmagic | BRAW | |

## 已知限制

1. **大文件（>50MB）**：需要 Node.js `--max-old-space-size=8192` 或浏览器端足够内存。未在移动设备上测试。
2. **CR3 大 XMP 警告**：部分 CR3 文件解码时显示 `large XMP not saved` 警告，不影响输出质量。
3. **DNG 变体**：只测试了一种 Adobe DNG（Canon 转换）。线性 DNG、JPEG-in-DNG 等变体未测试。
4. **多文件连续解码**：WASM heap 碎片化——连续解码 6+ 个大 RAW 文件后可能需要 GC。已通过 ALLOW_MEMORY_GROWTH + MAXIMUM_MEMORY=4GB 缓解。
5. **仅 Node.js 验证**：浏览器端 WASM 加载 + RAW 解码尚未测试（Task 0.5.10）。

## 性能总结

| 格式 | 平均文件大小 | 平均解码时间 | 平均输出大小 |
|------|------------|------------|------------|
| CR2 | 26MB | 5s | 1.2MB |
| CR3 | 8MB | 8s | 1.4MB |
| NEF | 27MB | 7.5s | 2.3MB |
| ARW | 24MB | 6s | 2.0MB |
| DNG | 6MB | 2s | 0.8MB |
