# Task 0.2.5：取色/Base64 评估报告

**日期：** 2026-06-03
**状态：** ✅ 已完成评估，结论：不替换

## 评估范围

评估 `extract-colors/` 和 `image-to-base64/` 两个工具页是否适合替换为 wasm-vips。

## extract-colors（取色）

**当前实现逻辑：**
1. 将图片缩放至最长边 200px（Canvas `drawImage`）
2. 用 `ctx.getImageData()` 获取像素数组（~40,000 像素）
3. 纯 JS 实现 Median Cut 算法进行颜色量化
4. 展示调色板

**wasm-vips 替换可行性：**
- wasm-vips `getpoint()` 可以逐像素读取，但需要全图采样时仍需 JS 循环
- wasm-vips `histFind()` + `stats()` 提供统计信息但不提供取色算法
- Median Cut 量化完全是 JS 算法，与 wasm-vips 无关
- Canvas 只用于 `getImageData` 获取像素数组——这是 Canvas API 唯一擅长的场景
- 替换为 wasm-vips 没有性能优势（反而是 overhead：加载 10MB WASM 只为了获取原本 1ms 就能用 Canvas 拿到的像素数组）

**结论：❌ 不替换。** wasm-vips 在此场景无收益。

## image-to-base64（Base64 编码）

**当前实现逻辑：**
1. File API: 用 `FileReader.readAsDataURL(file)` 直接读取为 Base64 data URL
2. URL 模式: Fetch blob → `FileReader.readAsDataURL()`
3. 纯字符串操作：前缀开关、每 76 字符换行、字符计数

**wasm-vips 替换可行性：**
- 完全不涉及图片处理——只有文件读取 + 字符串格式化
- wasm-vips 的 `writeToBuffer()` 可以做内存→Buffer 转换，但 FileReader 本身就能直接产出 Base64
- 增加 wasm-vips 加载成本（10MB WASM、SharedArrayBuffer 要求）0 收益

**结论：❌ 不替换。** wasm-vips 与此工具无关。

## 综合结论

| 工具 | 替换评估 | 原因 |
|------|---------|------|
| extract-colors | ❌ 不替换 | Canvas `getImageData` 是唯一适合的像素读取方式 |
| image-to-base64 | ❌ 不替换 | 纯 FileReader + 字符串操作，wasm-vips 无相关性 |

Task 0.2.5 结束。Phase 0.2 至此完成：compress/resize/split 共 3 个核心工具替换为 wasm-vips，取色/Base64 保留 Canvas。
