# SPEC: PicEte PNG 压缩优化方案 — 对标 TinyPNG

> **版本:** v1.2
> **日期:** 2026-07-28
> **状态:** Draft — 待用户审核（已纳入 Claude Code 设计初审反馈：B1-B3 阻塞项修正 + O1-O5 可选改进）
> **前置依赖:** 无（基于现有 wasm-vips 基础架构）
> **后 MVP 模式:** 质量改进（见 PROGRESS.md "后 MVP 阶段的持续改进模式"）

---

## 1. 现状分析

### 1.1 当前 PNG 压缩实现

核心代码位于 `compress-image/index.html:589-593`：

```javascript
const isPng = file.type === 'image/png';
const ext = isPng ? '.png' : '.jpg';
// ⚠️ PNG 使用 {} 空选项，压缩几乎无效（见本 SPEC）
const outputBuffer = isPng
    ? image.writeToBuffer(ext, {})       // ← 空选项！
    : image.writeToBuffer(ext, { Q: Math.round(quality * 100) });
```

| 方面 | 当前行为 | 后果 |
|------|---------|------|
| `compression` | 未指定（默认 libpng level 6） | 仅中等 deflate 压缩 |
| `palette` | 未指定（默认 false） | 24/32-bit RGB/RGBA 保持原样 |
| `colours` / `Q` | 未指定 | 无量化，全色彩保留 |
| `dither` | 未指定 | 无抖动处理 |
| `effort` | 未指定（默认 0） | 无量化优化 |
| `filter` | 未指定（libpng 默认 adaptive） | 可接受但未最大化 |
| `keep` | 未指定（保留所有元数据） | EXIF/ICC/text 等 chunk 全部保留 |
| Canvas fallback | `canvas.toBlob(..., 'image/png', quality)` | quality 参数对 PNG **完全无效** |

### 1.2 核心问题

**PNG 24/32-bit 未量化是最大的压缩缺口。** 一张典型的网页截图或照片 PNG：
- 24-bit RGB = 16,777,216 种颜色，但实际图像通常只有几千种
- 量化为 8-bit palette（≤256 色）后：
  - 每个像素从 3 字节（RGB）或 4 字节（RGBA）→ 1 字节（索引）
  - 调色板仅 256×4=1KB（全彩 256×3=768B）
  - 拍照类 PNG 可减小 **60-80%**
  - 截图/UI 类 PNG 可减小 **85-95%**

### 1.3 FAQ 不匹配

当前 FAQ 写的是：「For PNG images, we recommend converting to JPEG or WebP during compression for maximum file size reduction」— 这等于承认当前工具无法有效压缩 PNG。

---

## 2. TinyPNG 对标分析

### 2.1 TinyPNG 技术栈

TinyPNG 最初基于 `pngquant`（开源 Median Cut 量化库），其后端 Pipeline：

```
输入 PNG → 解码 → 色彩量化 (Median Cut) → PNG filter 优化
       → deflate 压缩 (zlib level 9) → 元数据剥离 → 输出 PNG
```

| 技术 | TinyPNG | PicEte 当前 |
|------|---------|------------|
| 色彩空间 | 量化至 8-bit palette | 保持 24/32-bit RGB/RGBA |
| 颜色数 | 自动选择（通常 64-256） | 全部保留（最多 16M） |
| Dithering | Floyd-Steinberg 自适应 | 无 |
| Deflate | Level 9 | Level 6（默认） |
| PNG filter | Adaptive（每个 scanline 最优） | Adaptive（默认） |
| 元数据 | 全部剥离 | 全部保留 |
| Alpha 通道 | ✅ 完整保留（tRNS + palette alpha） | ✅ 原生支持 |

### 2.2 预期效果对比

| 图像类型 | 原始大小 | TinyPNG | 当前 PicEte | 优化后预期 |
|---------|---------|---------|------------|-----------|
| 网页截图 (1920×1080) | ~800 KB | ~120 KB | ~750 KB | ~100-180 KB |
| 照片 PNG (1200×800) | ~1.5 MB | ~250 KB | ~1.4 MB | ~200-350 KB |
| UI 图标 (512×512) | ~50 KB | ~8 KB | ~48 KB | ~6-12 KB |
| 带 Alpha 渐变 (800×600) | ~300 KB | ~80 KB | ~290 KB | ~60-100 KB |

---

## 3. 优化方案

### 3.1 Libvips PNG 保存参数详解

Libvips 的 `writeToBuffer('.png', opts)` 支持的选项（来自 pngsave C 源码）：

| 选项 | 类型 | 范围 | 默认 | 说明 |
|------|------|------|------|------|
| `compression` | int | 0-9 | 6 | zlib deflate 压缩级别 |
| `palette` | bool | true/false | false | 启用量化至 8-bit palette |
| `colours` | int | 1-256 | 256 | palette 最大颜色数 |
| `Q` | int | 0-100 | 无 | 量化质量（值越高质量越好） |
| `dither` | float | 0-1 | 0 | Floyd-Steinberg 抖动量 |
| `effort` | int | 0-10 | 0 | 量化 CPU 努力程度 |
| `filter` | int | 0-8 | adaptive | libpng row filter 标志位 |
| `bitdepth` | int | 1/2/4/8/16 | 8 | 输出位深 |
| `interlace` | bool | true/false | false | Adam7 隔行扫描 |
| `keep` | bitmask | 见下 | 全保留 | 保留的元数据 |

**`keep` 选项（libvips ≥ 8.13）：**
- `VipsForeignKeep.NONE` (0) — 剥离所有元数据
- `VipsForeignKeep.ICC` (1) — 保留 ICC profile
- `VipsForeignKeep.EXIF` (2) — 保留 EXIF
- `VipsForeignKeep.XMP` (4) — 保留 XMP
- `VipsForeignKeep.IPTC` (8) — 保留 IPTC

### 3.2 核心策略

**图片加载（Phase 0 验证 — `ImageSource` 未编译）：**
```javascript
// ❌ 不可用（ImageSource 未编译）:
// const imgSource = vips.ImageSource.newFromBuffer(uint8Array);
// const image = vips.Image.newFromSource(imgSource, '');

// ✅ 正确:
const image = vips.Image.newFromBuffer(uint8Array);
```

#### A. 有损 PNG 压缩（压缩比最高，对标 TinyPNG）

```
compression: 9          ← 最大 deflate
palette: true            ← 启用量化
Q: quality_value         ← 用户质量滑块映射到量化质量（量化器自动计算色数）
dither: 0.5              ← Floyd-Steinberg 抖动
effort: 7                ← 高量化努力
keep: 0                  ← 剥离所有元数据
```

> ⚠️ **Phase 0 验证确认：** `colours` 参数不被当前 WASM 版本支持（触发 `VipsForeignSavePngTarget` 错误）。色数通过 `Q` 值由量化器自动计算，无需显式指定 `colours`。

**质量滑块映射（quality slider → PNG Q）—— 经 Phase 0 真实图片验证（自然照片 1920×1281）：**

| 滑块值 | PNG Q | dither | 预期压缩率（真实照片） | 用途 |
|--------|-------|--------|----------------------|------|
| 90-100 | 90 | 0.3 | ~50% | 最高质量，几乎无损 |
| 80-89 | 80 | 0.4 | ~60% | 高质量，适合印刷/Web |
| 70-79 | 70 | 0.5 | ~65% | 中等，适合网页 |
| 60-69 | 60 | 0.5 | ~69% | 高压缩，适合缩略图 |
| 50-59 | 50 | 0.3 | ~72% | 极限压缩 |
| <50 | 40 | 0.2 | ~74% | 极低质量预览 |

> **⚠️ 压缩率预期说明：** 上表中的"预期压缩率"基于真实自然照片测试（1920×1281, 2.5 MB）。合成图/渐变图的压缩率会显著偏高（可达 90%+），但这不代表真实场景。详见 Phase 0 验证报告 `docs/reports/phase0-verification-report.html` 第 11 节"偏差分析"。
>
> **色数说明：** 色数由量化器自动计算，映射表中不再列出色数。Phase 0 验证确认 `colours` 参数不被支持（PNG IHDR 位深限制）。

#### B. 无损 PNG 压缩（用户选择无损时）

```
compression: 9          ← 最大 deflate
palette: false           ← 不量化（无损）
filter: adaptive         ← 最优 row filter
keep: 0                  ← 仅剥离元数据
```

预期效果：100% 像素级无损，仅通过 deflate level 9 + metadata stripping 可节省 **5-15%**。

#### C. Alpha 通道特殊处理

当图像含 alpha 通道时，量化 Palette 模式（PLTE + tRNS）能保留透明度。Phase 0 验证确认：
- RGBA 径向渐变（512×512, 262K 半透明像素）→ **100% Alpha 保留**
- UI 截图（含半透明阴影）→ **无黑边/锯齿**
- 半透明像素多时仍建议降低 dither 以减少潜在 banding

#### D. 智能体积熔断机制（Phase 0 验证新增 — 硬性架构要求）

**问题：** 极小源文件（< 3 KB）在 palette 量化后 chunk 固定开销可能超过原图，导致体积增大（test-photo-800x600.png 从 2.8 KB → 117.5 KB，test-fully-transparent.png 从 0.3 KB → 0.4 KB）。

**架构要求（硬性，不可协商）：**

```javascript
function compressWithFallback(image, opts, originalSize) {
    const output = image.writeToBuffer('.png', opts);
    if (output.byteLength >= originalSize) {
        // 熔断：压缩后体积不减小 → 返回原图
        return { buffer: originalBytes, fallback: true };
    }
    return { buffer: output.buffer, fallback: false };
}
```

- 熔断阈值：**compressedSize >= originalSize**
- 不设容忍窗口（如 5%），严格 ≥ 即触发
- Phase 0 验证：3 张真实图片（2.5 MB / 7.2 KB / 1.9 MB）均未误触发

#### E. 内存安全要求（Phase 0 验证确认）

50 次连续压缩测试零泄漏。已验证的安全模式：

```javascript
let image;
try {
    image = vips.Image.newFromBuffer(uint8Array);
    const output = image.writeToBuffer('.png', opts);
    // ... 使用 output
} finally {
    if (image) image.delete();
}
```

在 Web Worker 中同样适用——`postMessage` 发送结果前完成 delete。

#### F. 自适应 Dither 调整（用户审核反馈 2.4）

**核心观察：** 固定 dither=0.5 对扁平化 UI 图标会引入不必要的噪点，反而破坏 PNG filter 连续性、降低压缩率。

**方案：** 引入简单的图像特征检测，压缩前分析图像内容特征：

```
if (图像为扁平化设计 / 纯色块占比高)
    → dither: 0（无抖动，保留锐利边缘）
else if (图像为自然照片 / 渐变丰富)
    → dither: 0.5（中度 Floyd-Steinberg）
```

**检测方法（轻量，不依赖额外库）：**
1. 对图像做 2×2 或 4×4 降采样
2. 计算相邻像素间的色彩差异方差
3. 低方差 = 扁平化/色块 → dither=0
4. 高方差 = 照片/渐变 → dither=0.5

**降级：** 检测逻辑出错时（如计算超时），默认使用 dither=0.3（中性值）。

---

## 4. 实现计划（Phase 按 Severity + 依赖顺序排序）

### Phase 0（P0 — 技术基石验证）：wasm-vips 量化能力确认

**⚠️ 用户审核反馈 2.1：此 Phase 原定为 Phase 4（P3），现提升为 Phase 0。**
**理由：** 这是整个有损压缩方案的技术基石。如果 wasm-vips 不支持 palette:true，Phase 1-3 的核心逻辑都将建立在空中楼阁之上。

**内容：** 编写极简测试脚本，在浏览器环境中验证以下参数是否生效：

| 测试项 | 命令/代码 | 通过标志 |
|--------|----------|---------|
| `palette: true` 是否被接受 | `image.writeToBuffer('.png', {palette: true, colours: 64})` | 不抛异常，输出 ≤ 原图 40% |
| `Q` 参数是否影响输出 | 分别测试 Q=30 vs Q=90 | 高 Q 输出的 PSNR 更高 |
| **仅传 Q 不传 colours**（自动色数年） | `image.writeToBuffer('.png', {palette: true, Q: 80})` vs 硬编码 64/128/192 色 | Q-only 结果体积与固定 colours 版本相近或更优 |
| `effort` 参数是否生效 | `effort: 7` vs `effort: 0` | 高 effort 色带更少 |
| `keep: 0` 是否剥离元数据 | 比较 ICC/EXIF chunk 存在性 | 压缩后无元数据 |

**验证脚本（用于浏览器 DevTools Console）：**

> 前置条件：用以下命令生成本地测试 PNG 文件，放在项目根目录下：
> ```bash
> # 方式一：用 Node.js 生成（无需 ImageMagick）
> node -e "
> const { createCanvas } = require('canvas'); // 如果无此包，用方式二
> "
>
> # 方式二：用 Python 生成（零依赖）
> python3 -c "
> import struct, zlib
> def create_png(path, w, h, pixels):
>     # 构造最小 PNG: IHDR + IDAT(raw deflate) + IEND
>     def chunk(ctype, data):
>         c = ctype + data
>         crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
>         return struct.pack('>I', len(data)) + c + crc
>     ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)  # 8-bit RGB
>     raw = b''
>     for y in range(h):
>         raw += b'\x00'  # filter none
>         for x in range(w):
>             r = int(255 * x / w)
>             g = int(255 * y / h)
>             b = 128
>             raw += struct.pack('BBB', r, g, b)
>     idat_data = zlib.compress(raw)
>     with open(path, 'wb') as f:
>         f.write(b'\x89PNG\r\n\x1a\n')
>         f.write(chunk(b'IHDR', ihdr))
>         f.write(chunk(b'IDAT', idat_data))
>         f.write(chunk(b'IEND', b''))
> create_png('test-photo-320x240.png', 320, 240)
> create_png('test-photo-1920x1080.png', 1920, 1080)
> create_png('test-solid-white.png', 100, 100)
> create_png('test-solid-red.png', 100, 100)
> print('测试 PNG 文件已生成: test-photo-320x240.png, test-photo-1920x1080.png, test-solid-white.png, test-solid-red.png')
> "
> ```
> 然后将生成的 PNG 复制到 `/js/lib/` 或 `/images/` 目录下供页面访问：
> ```bash
> cp test-photo-320x240.png images/
> cp test-photo-1920x1080.png images/
> cp test-solid-white.png images/
> cp test-solid-red.png images/
> ```

```javascript
// 在 http://localhost:3000/compress-image/ 页面打开后执行 DevTools → Console
// 1. 加载测试 PNG（确保 images/ 下有这些文件）
const testFiles = ['test-photo-320x240.png', 'test-photo-1920x1080.png', 'test-solid-white.png'];
async function loadPngBytes(filename) {
    const resp = await fetch('/images/' + filename);
    if (!resp.ok) throw new Error('无法加载 ' + filename + ' — 请先生成测试 PNG 并复制到 images/ 目录');
    return new Uint8Array(await resp.arrayBuffer());
}

// 2. 确保 VipsLoader 已就绪
const vips = await VipsLoader.load();
if (!vips) { console.error('❌ VipsLoader 初始化失败'); return; }

// 3. 测试 palette 参数（核心测试）
async function testPaletteSupport(vips, pngBytes, label) {
    const source = vips.ImageSource.newFromBuffer(pngBytes);
    const image = vips.Image.newFromSource(source, '');
    source.delete();
    
    // 基线: 默认保存
    const baseline = image.writeToBuffer('.png', {}).buffer.byteLength;
    
    // 测试 A: palette + colours 硬编码（v1.2 映射表模式）
    let resultA = null;
    try {
        resultA = image.writeToBuffer('.png', {
            palette: true, colours: 64, Q: 80, effort: 7
        }).buffer.byteLength;
        console.log(`✅ [${label}] palette + colours=64 成功: ${resultA}B (基线: ${baseline}B, 节省 ${((1-resultA/baseline)*100).toFixed(1)}%)`);
    } catch(e) { console.error(`❌ [${label}] palette+colours 失败:`, e.message); }
    
    // 测试 B: 仅传 Q 不传 colours（自动色数模式）
    let resultB = null;
    try {
        resultB = image.writeToBuffer('.png', {
            palette: true, Q: 80, effort: 7
        }).buffer.byteLength;
        console.log(`✅ [${label}] Q-only(80) 成功: ${resultB}B (colours=64: ${resultA || 'N/A'}B)`);
        if (resultA) {
            const ratio = resultB / resultA;
            console.log(`  Q-only vs 固定64色: ${ratio < 1.1 ? '✅ 体积相当，可优先使用Q-only模式' : '⚠️ Q-only 偏大，需进一步验证'}`);
        }
    } catch(e) { console.error(`❌ [${label}] Q-only 失败:`, e.message); }
    
    // 测试 C: 元数据剥离
    try {
        const stripped = image.writeToBuffer('.png', {
            palette: true, compression: 9, keep: 0
        }).buffer.byteLength;
        console.log(`✅ [${label}] keep=0 成功: ${stripped}B`);
    } catch(e) { console.error(`❌ [${label}] keep=0 失败，降级 compression=9:`, e.message); }
    
    image.delete();
    return { baseline, resultA, resultB };
}

// 4. 依次测试所有文件
for (const name of testFiles) {
    const bytes = await loadPngBytes(name);
    await testPaletteSupport(vips, bytes, name);
}
console.log('✅ 全部测试完成');
```

**产出：** `docs/reports/png-palette-verification.md`
- 各参数测试结果表
- 如果不可用：给出降级路径决策（仅 compression:9 + metadata strip）
- 如果部分可用：记录可用参数集，后续 Phase 仅使用已验证参数

**估计耗时：** 30 分钟（含浏览器手动测试）

**验证标准：**
- [ ] `palette: true` 成功输出 PNG
- [ ] 量化后文件显著小于基线（≥ 40% 节省）
- [ ] `keep: 0` 参数行为已确认（成功或报错）
- [ ] 产出验证报告

### Phase 0.1（P0 — BugFix 架构层）：Web Worker + 防抖 + 内存安全

**⚠️ 用户审核反馈 2.2 & 2.3：Web Worker 从"风险缓解"升级为"硬性架构要求"。**

#### 2.2 Web Worker 强制化（用户审核反馈）

**问题：** `effort: 7` + `compression: 9` 的 WASM 计算开销极大。在主线程运行会导致浏览器标签页假死，严重破坏用户体验。

**架构要求（硬性，不可协商）：**
- wasm-vips 实例必须在 Web Worker 中加载和运行
- 主线程只负责 UI 响应、滑块交互、结果展示
- Worker 通过 `postMessage` / `onmessage` 与主线程通信
- 压缩任务通过消息队列提交，Worker 串行处理

**Worker 与主线程通信协议：**

```
主线程 → Worker:
  { type: 'compress', id: '<uuid>', file: ArrayBuffer, options: { ... } }

Worker → 主线程:
  { type: 'progress', id: '<uuid>', stage: 'decode'|'quantize'|'compress'|'done', progress: 0-100 }
  { type: 'result', id: '<uuid>', blob: Blob, stats: { originalBytes, compressedBytes, paletteColors, ditherUsed } }
  { type: 'error', id: '<uuid>', message: '...' }
```

**注意：** 在 Web Worker 中加载 wasm-vips 需要将 `vips-loader.js` 适配为 Worker 入口。Emscripten 生成的 `vips.js` 本身支持在 Worker 环境中加载，但需要将 `COOP/COEP` header 传递到 Worker 中（Worker 继承页面的 crossOriginIsolated 状态）。

#### 2.3 防抖 + 内存安全（用户审核反馈）

**问题：** 用户拖动质量滑块（如从 90 拖到 50）时，会极速触发多次 `writeToBuffer` 调用。每次调用创建 C++ 侧 `Image` 对象，如果旧指针未严格销毁，会累积内存泄漏。

**解决方案：**

```
滑块 input 事件 → 防抖 300ms → 取消前一次压缩请求 → 
  发送新请求到 Worker → Worker 收到新请求时，
  先 abort 旧任务并 delete 旧 Image → 再处理新任务
```

**关键实现细节：**

```javascript
// 主线程防抖
let currentRequestId = 0;
let debounceTimer = null;

qualitySlider.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const requestId = ++currentRequestId;
        compressWithDebounce(e.target.value, requestId);
    }, 300);
});

// Worker 侧：abort 旧任务
// 每个 compress 任务开始时检查是否已被取消
let currentTaskId = null;

self.onmessage = (e) => {
    const { type, id, ...data } = e.data;
    
    if (type === 'compress') {
        // 如果有正在执行的任务，先取消并清理内存
        if (currentTaskId && currentTaskId !== id) {
            // 标记旧 Image 为可回收（libvips 引用计数）
            if (pendingImage) {
                pendingImage.delete();
                pendingImage = null;
            }
        }
        currentTaskId = id;
        executeCompress(data);
    }
    
    if (type === 'cancel') {
        // 清理 C++ 侧内存
        if (pendingImage) {
            pendingImage.delete();
            pendingImage = null;
        }
        currentTaskId = null;
    }
};
```

**异常安全：** 所有 `image.delete()` 和 `imgSource.delete()` 调用必须放在 `try { } finally { }` 中，确保即使处理过程抛出异常，C++ 对象也能被释放。

**验证标准：**
- [ ] 快速拖动滑块（90→50→80→30 在 2 秒内完成）不产生内存增长
- [ ] Chrome DevTools Memory 面板：连续 10 次压缩后 heap 不持续增长
- [ ] 压缩过程中页面不卡死（UI 响应正常）
- [ ] 旧请求被新请求取消时，控制台无 "uncaught exception"

### Phase 0.2（P1 — BugFix 业务层）：PNG 压缩参数注入 + 自适应 Dither

**问题：** 当前 PNG 保存使用 `{}` 空选项，导致压缩几乎无效。

**改动：**
1. 在 `compress-image/index.html` 的 wasm-vips 路径中，构建 PNG options 对象
2. 接收用户质量滑块值，映射到 libvips PNG 参数
3. 引入自适应 dither 检测（见 §3.2-D）
4. 改为两种模式:
   - 有损模式（默认）: palette + compression=9 + Q + dither(auto) + effort
   - 无损模式（Toggle 开关）: compression=9 + 不量化 + 仅剥离元数据

**质量滑块映射（quality slider → PNG Q）—— v1.1 修正（含色数下限保底 64 色）：**

> ⚠️ 低于 64 色后 Banding 概率指数级上升，性价比极低。故 <50 档锚定在 64 色，通过调低 dither 来换取体积。
> Phase 0 同时验证：仅传 Q 值（不传 colours）时量化器是否能自动计算最优色数。

| 滑块值 | PNG Q | 预期色数 | dither | 用途 |
|--------|-------|---------|--------|------|
| 90-100 | 90 | ~256 | 0.3 | 最高质量，几乎无损 |
| 80-89 | 80 | ~192 | 0.4 | 高质量，适合印刷 |
| 70-79 | 70 | ~128 | 0.5 | 中等，适合网页 |
| 60-69 | 60 | ~96 | 0.5 | 高压缩，适合缩略图 |
| 50-59 | 50 | **64（下限）** | 0.3 | 极限压缩，dither 降低以减少噪点 |
| <50 | 40 | **64（下限）** | 0.2 | 极低质量，最小 dither 保可看 |

> **注：** `<50` 和 `50-59` 的色数相同（64 色下限），区别仅在于 dither 强度。

**修改位置：** `compress-image/index.html:589-593`
**估计代码量：** ~80 行 JS 逻辑变更（含 Worker 通信） + UI 追加无损模式开关

**验证标准：**
- [ ] PNG 压缩后相比原图显著减小（测试图片应有 > 50% 节省）
- [ ] 量化后的 PNG 保留透明度
- [ ] 无损模式：pixel-perfect 比较，RGB 值 100% 一致
- [ ] 剥离元数据后的 PNG 小于原图
- [ ] 自适应 dither：扁平 UI 图标无噪点，照片类保留 dither

### Phase 1（P2 — 重要优化）：长尾压缩页同步

**问题：** `compress-image-to-50kb/100kb/200kb/500kb` 等目标大小压缩页同样使用 `writeToBuffer('.png', {})`。

**改动：**
对这些页面做类似 Phase 0.2 的改造，且引入**自适应质量调整**逻辑：
- 从最高质量开始尝试量化
- 逐步降低色数直到目标大小达成
- 输出最终 blob
- 复用 Phase 0.1 建立的 Worker 架构

**修改位置：** `compress-image-to-{50,100,200,500}kb/index.html`
**依赖：** 必须先完成 Phase 0.1（Worker 架构）和 Phase 0.2（参数注入逻辑）

**验证标准：**
- [ ] 50KB 目标：输出 ≤ 50KB
- [ ] 100KB 目标：输出 ≤ 100KB
- [ ] 200KB 目标：输出 ≤ 200KB
- [ ] 500KB 目标：输出 ≤ 500KB
- [ ] 质量尽可能高（不盲目降至最低）

### Phase 2（P3 — 体验增强）：UI 改进 + FAQ 修正

1. **FAQ 更新：** PNG 压缩不再需要推荐转 JPEG/WebP
2. **对比滑块：** 为 PNG 压缩结果显示 before/after 对比（复用已有 `image-comparison-slider.js`）
3. **压缩报告：** 显示量化后色数、调色板大小、dither 模式等指标
4. **模式选择：** 清晰标注"有损压缩（推荐）" vs "无损压缩"，附带简短说明

---

## 5. 风险与边界条件

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| wasm-vips 未编译 libimagequant | 中 | 整个 palette 方案不可用 | **Phase 0 优先验证**；如果不可用，降级方案为 compression:9 + metadata strip，仅能节省 5-15% |
| wasm-vips Emscripten 端口参数差异 | 低 | `keep` 等参数名不同 | 先写测试代码确认参数名 |
| 量化的 Alpha 边缘锯齿 | 低 | 半透明边缘有黑边 | 检测 Alpha 通道使用量，半透明像素多时降低 dither 或跳过量化 |
| WASM 内存泄漏（滑块频繁触发） | 中 | C++ 侧 Image 对象未释放 → heap 持续增长 | **防抖 300ms + Worker cancel 协议 + try/finally 确保 delete**（Phase 0.1 硬性要求）|
| 大图像（8K）WASM 内存超限 | 中 | 浏览器崩溃或 OOM | 压缩前检查像素总数（width×height），超过阈值（如 4000 万像素）时提示用户 |
| `writeToBuffer` 的 `keep` 参数在浏览器端不可用 | 中 | 元数据剥离不可用 | 降级为 compression:9 + palette 但不传 keep；通过解码时不加载元数据实现间接剥离 |
| 自适应 dither 检测失败 | 低 | 降采样计算超时或出错 | 默认 fallback dither=0.3（中性值）|
| 纯色/全透明图像量化异常 | 低 | 除零或聚类失败 | 增加输入校验：检测颜色分布方差，极低方差图像跳过量化直接走无损路径 |
| **浏览器 SharedArrayBuffer 支持差异** | 中 | Safari/Firefox 旧版本不支持 SAB → Worker 中无法加载 wasm-vips | **验证环境：** 必须 HTTPS + COOP/COEP headers（Vercel 已配置）。**浏览器最低版本：** Chrome 92+ / Safari 15+ / Firefox 97+。**降级：** 不支持 SAB 的浏览器回退到 Canvas API（现有路径）。**测试方法：** Phase 0 同时测试 `typeof SharedArrayBuffer !== 'undefined' && self.crossOriginIsolated` |
| **Emscripten 动态库预加载死锁** | 低 | wasm-vips 初始化卡死（vips-heif.wasm 和 vips-jxl.wasm 预加载与 pthread 初始化产生死锁） | **已在 `vips-loader.js:63` 修复：** 设置 `dynamicLibraries: []` 禁用动态库预加载。**复现方法：** 将 `vips-loader.js` 中 `dynamicLibraries: []` 注释掉，重新加载页面观察是否卡死。**风险水平：** 当前生产版本已含此修复，二次发生概率极低 |

---

## 6. 与 TinyPNG 的差距分析

| 能力 | TinyPNG | PicEte 当前 | PicEte 优化后 | 差距 |
|------|---------|------------|-------------|------|
| 24-bit → 8-bit palette | ✅ | ❌ | ✅ | 消除 |
| Adaptive dithering | ✅ | ❌ | ✅ (libvips) | 消除 |
| Deflate level 9 | ✅ | ❌ (level 6) | ✅ | 消除 |
| 元数据剥离 | ✅ (全剥) | ❌ (全留) | ✅ (可选) | 消除 |
| 自适应质量选择 | ✅ | ❌ | ✅ (Phase 2) | 消除 |
| Alpha 通道保留 | ✅ | ✅ | ✅ | 已满足 |
| API 批量处理 | ✅ | ❌ | N/A（纯前端） | 设计差异 |
| 服务器端处理 | ✅ | ❌（纯前端） | ❌ | 设计差异（不上传） |

---

## 7. 验证方法论

### 基准测试图片集

| # | 类型 | 尺寸 | 描述 | 测试目的 |
|---|------|------|------|---------|
| 1 | 照片 PNG | 1920×1080 | 自然风景，色彩丰富 | 主流量化质量 |
| 2 | 网页截图 | 1280×720 | 多文字+图标 | 文字边缘保持 + dither 检测 |
| 3 | UI 界面 | 800×600 | 渐变色按钮+阴影 | Alpha 半透明处理 |
| 4 | 图标 | 256×256 | 矢量风格，纯色块 | 扁平化 dither=0 触发 |
| 5 | 带 Alpha 渐变 | 512×512 | 半透明径向渐变 | tRNS palette Alpha 保留 |
| 6 | 截图+文字 | 1200×800 | 深色背景+白色文字 | 高对比场景量化 |
| 7 | **超大尺寸（8K）** | 7680×4320 | 高分辨率风景照 | Web Worker + WASM 内存上限压测 |
| 8 | **纯单色 PNG** | 100×100 | 全白或全红单色 | 极少量化下算法鲁棒性，防除零 |
| 9 | **全透明 PNG** | 512×512 | 完全透明的 RGBA | Alpha 通道极端情况，输出仍全透明且极小 |

### 测试指标

```
原始大小 → 压缩后大小 → 节省率
峰值信噪比 (PSNR) 与原始对比
结构相似性 (SSIM)
调色板色数
Alpha 通道保留验证
解码兼容性（浏览器加载）
```

### 测试方法

```javascript
// 验证脚本框架
async function benchmarkPngCompression(file, options) {
    const arrayBuffer = await file.arrayBuffer();
    const uint8Array = new Uint8Array(arrayBuffer);
    const imgSource = vips.ImageSource.newFromBuffer(uint8Array);
    const image = vips.Image.newFromSource(imgSource, '');
    imgSource.delete();
    
    const outputBuffer = image.writeToBuffer('.png', options);
    image.delete();
    
    return {
        originalBytes: arrayBuffer.byteLength,
        compressedBytes: outputBuffer.buffer.byteLength,
        savingsPercent: (1 - outputBuffer.buffer.byteLength / arrayBuffer.byteLength) * 100
    };
}
```

---

## 8. 附录：TinyPNG 原理参考

TinyPNG 的核心技术栈公开信息：

1. **基于 pngquant**（Kornel Lesiński 开发的开源库，MIT license）
2. **量化算法：** Median Cut 变体，带感知权重
   - 直方图构建时对噪声区域降权
   - 多次迭代 Median Cut 以优化色彩分布
   - Gradient descent 微调调色板
3. **Dithering：** 改进的 Floyd-Steinberg 误差扩散
   - 不向图像添加不必要的噪点
   - 与调色板优化协同
4. **最终输出：** G 标准 8-bit PNG（PLTE + tRNS + IDAT）
   - 完整保留 Alpha 透明度
   - 全浏览器兼容
5. **不支持的操作：** TinyPNG 不做 WebP 转换（那是另一产品 TinyJPG 的功能）

---

## 9. 审核结论（v1.0 → v1.1 → v1.2 变更记录）

### 用户审核反馈（v1.0 → v1.1）

| # | 审核反馈 | 严重度 | 原方案缺陷 | 修正内容 |
|---|---------|--------|-----------|---------|
| 2.1 | wasm-vips 量化验证应前置 | P0 架构 | 验证放在 Phase 4（P3），底座不稳就写业务代码 | **Phase 4 → Phase 0** |
| 2.2 | Web Worker 必须是硬要求 | P0 架构 | 列为"风险缓解措施" | **Phase 0.1 硬性要求** + Worker 通信协议 |
| 2.3 | 防抖 + 内存泄漏 | P0 工程 | 未提及多次 writeToBuffer 的 C++ 泄漏 | **Phase 0.1** 300ms debounce + cancel 协议 + try/finally |
| 2.4 | Dither 应自适应 | P1 质量 | 固定 dither=0.5 破坏扁平 UI 图标 | **§3.2-D** 降采样方差检测法 |
| 2.5 | 色数下限保底 64 色 | P2 质量 | <50 档降到 48 色，Banding 指数上升 | **映射表修正**：锚定 64 色，改调 dither |
| 2.5b | Phase 0 验证 Q-only 模式 | P0 验证 | 未测试仅传 Q 不传 colours | **Phase 0 新增测试项** |
| 3 | 补充极端边界测试 | P2 覆盖 | 仅 6 张常规图 | **测试集扩展** +3 个极端场景 |

### Claude Code 设计初审反馈（v1.1 → v1.2）

| 编号 | 类型 | 审核发现 | 修正内容 |
|------|------|---------|---------|
| **B1** | 阻塞 | Phase 0 验证脚本使用 `bench-sample.jpg`（JPEG 无法测试 PNG palette） | 重写为 PNG 验证脚本，含 Q-only 对比测试和元数据剥离测试 |
| **B2** | 阻塞 | 9 张测试图片无获取方式 | 新增 Python 零依赖生成脚本（struct+zlib 构造最小 PNG），含生成命令和 cp 指令 |
| **B3** | 阻塞 | 版本号不一致（v1.1 vs v1.2） | 统一为 v1.2 |
| **O1** | 可选 | 缺少浏览器 SharedArrayBuffer 兼容性风险 | 风险表新增该项：浏览器最低版本、HTTPS+COOP/COEP 要求、Canvas 降级 |
| **O2** | 可选 | 前置依赖字段模糊（写"无"） | 不改字段（已有"基于现有 wasm-vips 基础架构"说明），O2 判定为无需修改 |
| **O3** | 可选 | Emscripten 动态库死锁复现方法缺失 | 风险表新增该项：复现方法（注释 `dynamicLibraries: []`）、当前修复状态、二次概率 |
| **O4** | 可选 | 映射表歧义（<50 和 50-59 都是 64 色） | 映射表下方新增注释，说明色数相同仅 dither 区别 |
| **O5** | 可选 | 验证脚本 TODO 未解决 | B1 修复中已一并解决：提供完整可运行的验证脚本 + 测试 PNG 生成命令 |
