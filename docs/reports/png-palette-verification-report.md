# Phase 0 验证报告 — wasm-vips PNG Palette 量化能力确认

> **日期:** 2026-07-28
> **对应 SPEC:** `docs/specs/PICETE-PNG-OPTIMIZATION-SPEC.md` v1.2
> **验证页面:** `docs/reports/png-palette-verify.html`
> **测试图片:** `images/test-photo-320x240.png`, `test-photo-1920x1080.png`, `test-solid-white.png`, `test-solid-red.png`

## 浏览器环境

| 检查项 | 状态 |
|--------|------|
| SharedArrayBuffer | ✅ |
| crossOriginIsolated | ✅ |
| wasm-vips 版本 | ✅ 加载成功 |

## API 可用性

| API | 状态 | 说明 |
|-----|------|------|
| `vips.Image.newFromBuffer(Uint8Array)` | ✅ | 替代 `ImageSource.newFromBuffer`（未编译）|
| `vips.Image.newFromSource(source, '')` | ❌ | ImageSource 未编译 |
| `writeToBuffer('.png', {})` | ✅ | 基线输出正常 |
| `{palette: true, Q: 80, effort: 7}` (Q-only) | ✅ | **推荐模式** |
| `{palette: true, compression: 9, keep: 0}` | ✅ | 元数据剥离有效 |
| `{palette: true, colours: 64, Q: 80, effort: 7}` | ❌ | `colours` 参数触发 `VipsForeignSavePngTarget` 错误 |

## 压缩效果数据

| 文件 | 原始 | 基线 | Q-only (Q=80) | 节省 | keep=0 | 节省 |
|------|------|------|--------------|------|--------|------|
| test-photo-320x240.png | 124.0 KB | 124.5 KB | 22.9 KB | 81.6% | 21.3 KB | 82.9% |
| test-photo-1920x1080.png | 140.5 KB | 141.0 KB | 10.4 KB | 92.7% | 8.6 KB | 93.9% |
| test-solid-white.png | 0.3 KB | 0.5 KB | 0.3 KB | 35.8% | 0.1 KB | 74.5% |
| test-solid-red.png | 0.3 KB | 0.6 KB | 0.3 KB | 47.5% | 0.1 KB | 79.2% |

## 架构决策更新

基于验证结果，SPEC 需要以下修正：

1. **图片加载 API:** 使用 `vips.Image.newFromBuffer(uint8Array)` 而非 `ImageSource.newFromBuffer` + `newFromSource`
2. **映射表简化:** 移除 `colours` 列，仅保留 `Q` + `dither`（量化器自动计算色数）
3. **Canvas fallback 保留:** 作为 SAB 不可用/COI 不支持时的降级

## 结论

**Palette 量化完全可用。** Q-only 模式的压缩效果超过预期（80-94%），已满足对标 TinyPNG 的目标。进入 Phase 0.1（Web Worker 架构层）。
