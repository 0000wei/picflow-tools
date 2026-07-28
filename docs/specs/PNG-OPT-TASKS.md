# PNG 压缩优化 — Phase Task 拆解与执行文档

> **对应 SPEC:** `docs/specs/PICETE-PNG-OPTIMIZATION-SPEC.md` (v1.2)
> **后 MVP 模式:** 质量改进 — 代码变更使用 `fix:` / `perf:` 前缀
> **日期:** 2026-07-28

---

## 1. 启动流程（Instructions / Lifecycle）

每次新 Session 或中断后恢复时执行：

```bash
cd /home/wu/桌面/picete
git log --oneline -3
grep -E "(最高优先级|阻塞项)" PROGRESS.md   # PROGRESS.md 无此行则跳过
bash scripts/init.sh 2>/dev/null || echo "无 init.sh"
```

## 2. WIP=1 规则（Scope）

- 一次只执行一个 Phase，严禁并行
- 每个 Phase 完成后：独立验证 → 审计 → 用户确认 → commit → 再继续
- 每个 Phase 的 commit 独立，不可合并

## 3. 执行回路（每 Task 都要遵循）

```
1. Hermes 编写委托上下文（prompt 文件）
2. 用户确认委托上下文
3. Claude Code 执行（cat prompt | claude -p --dangerously-skip-permissions, pty=true）
4. Hermes 独立验证（读取文件、grep、语法检查）
5. 验证通过 → 更新 PROGRESS.md → git add + commit
6. 验证不通过 → 修正委托上下文 → 重新委托
```

## 4. Task 列表

| # | Phase | Task 名称 | 前置依赖 | 类型 | 估计耗时 |
|---|-------|----------|---------|------|---------|
| 0 | Phase 0 | 验证脚本 HTML + 测试 PNG 生成 | 无 | JS/HTML 文件创建 | 20 min |
| — | Phase 0 (手动) | 浏览器 DevTools 运行验证 | Task 0 | 手动测试 | 15 min |
| 1 | Phase 0.1 | 创建 js/vips-worker.js 及 Worker 适配 | 无 | JS 文件创建 | 40 min |
| 2 | Phase 0.2 | 修改 compress-image/index.html 压缩逻辑 | Phase 0, 0.1 | HTML/JS 修改 | 40 min |
| 3 | Phase 1 | 同步 4 个目标大小压缩页 (50/100/200/500KB) | Phase 0.2 | HTML/JS 修改 | 30 min |
| 4 | Phase 2 | FAQ 修正 + 压缩报告 UI | Phase 0.2 | HTML 修改 | 20 min |

## 5. Task 详细定义

---

### Task 0 — Phase 0: 验证脚本 HTML + 测试 PNG 生成

#### ⚠️ 先读
- `docs/specs/PICETE-PNG-OPTIMIZATION-SPEC.md` (Phase 0 节, 验证脚本部分)
- `js/vips-loader.js` (了解 VipsLoader API)
- `compress-image/index.html:560-665` (了解当前 compressImages 函数结构)

#### 委托上下文

**做什么：**

1. 用 Python 生成 4 张测试 PNG 文件到 `images/` 目录：
   - `test-photo-320x240.png` — 320×240 渐变图（24-bit RGB）
   - `test-photo-1920x1080.png` — 1920×1080 渐变图（大图）
   - `test-solid-white.png` — 100×100 纯白单色图
   - `test-solid-red.png` — 100×100 纯红单色图

2. 创建独立的验证页面 `docs/reports/png-palette-verify.html`（非站点页面，放置于 docs/reports/）：
   - 内嵌完整验证脚本
   - 加载 VipsLoader → 依次加载 4 张测试 PNG → 运行三项测试
   - 测试 A: `{palette: true, colours: 64, Q: 80, effort: 7}` vs 默认 `{}`
   - 测试 B: `{palette: true, Q: 80, effort: 7}`（Q-only 不传 colours）vs 测试 A
   - 测试 C: `{palette: true, compression: 9, keep: 0}` 元数据剥离
   - 输出格式化为表格：文件、基线大小、colours=64 模式、Q-only 模式、节省率、keep=0 结果
   - 包含 SharedArrayBuffer 和 crossOriginIsolated 检测

**不做什么：**
- 不修改 `compress-image/index.html` 或任何现有页面
- 不修改 `vips-loader.js`
- 不要添加额外依赖

#### 验证标准
- [ ] `images/test-photo-320x240.png` 存在且为有效 PNG（`file images/test-photo-320x240.png` 返回 PNG）
- [ ] `images/test-photo-1920x1080.png` 存在
- [ ] `images/test-solid-white.png` 存在
- [ ] `images/test-solid-red.png` 存在
- [ ] `docs/reports/png-palette-verify.html` 存在
- [ ] 验证页面包含所有 3 项测试（A/B/C）（grep -c '测试 A\\|测试 B\\|测试 C'）

---

### Task 1 — Phase 0.1: 创建 Web Worker + 防抖 + 内存安全

#### ⚠️ 先读
- `compress-image/index.html`（全文，理解当前流程）
- `js/vips-loader.js`（理解 wasm-vips 加载方式）
- SPEC Phase 0.1 节（Worker 通信协议、防抖 cancel 模式）

#### 委托上下文

**做什么：**

创建 `js/vips-worker.js` — 专用于 PNG 压缩的 Web Worker，实现以下协议：

**Worker 接收消息格式：**
```javascript
{ type: 'compress', id: '<uuid>', file: ArrayBuffer, options: { palette, colours, Q, dither, effort, compression, keep } }
{ type: 'cancel', id: '<uuid>' }
```

**Worker 发送消息格式：**
```javascript
{ type: 'progress', id: '<uuid>', stage: 'decode'|'quantize'|'compress'|'done', progress: 0-100 }
{ type: 'result', id: '<uuid>', blob: Blob, stats: { originalBytes, compressedBytes } }
{ type: 'error', id: '<uuid>', message: '...' }
```

**核心逻辑：**
1. Worker 内部加载 wasm-vips（self.importScripts 加载 vips-loader.js，或直接加载 js/lib/vips.js）
2. 收到 compress 消息时：
   - 如果有正在执行的旧任务且 id 不同 → 调用旧 Image 的 delete() 清理
   - 解码 file (ArrayBuffer) → ImageSource → Image
   - 按 options 参数调用 writeToBuffer
   - 将结果 Blob 和统计 postMessage 回主线程
   - try/finally 确保 image.delete() 和 source.delete() 一直执行
3. 收到 cancel 消息时：
   - 如果 id 匹配当前任务 → 立即清理并标记取消
4. 所有 delete() 调用放在 try/finally 中

**异常安全要求：**
```javascript
let currentImage = null;
let currentSource = null;
try {
    currentSource = vips.ImageSource.newFromBuffer(bytes);
    currentImage = vips.Image.newFromSource(currentSource, '');
    // ... 处理
} finally {
    if (currentImage) { currentImage.delete(); currentImage = null; }
    if (currentSource) { currentSource.delete(); currentSource = null; }
}
```

**不做什么：**
- 不修改任何 HTML 文件
- 不修改 vips-loader.js

#### 验证标准
- [ ] `js/vips-worker.js` 存在
- [ ] `node --check js/vips-worker.js` 通过
- [ ] 包含 compress/cancel 消息处理
- [ ] 所有 delete() 在 try/finally 中（`grep -c 'finally' js/vips-worker.js` ≥ 1）
- [ ] 支持 `currentTaskId` 取消机制（`grep -c 'currentTaskId' js/vips-worker.js` ≥ 1）

---

### Task 2 — Phase 0.2: PNG 压缩参数注入 + 自适应 Dither

#### ⚠️ 先读
- `compress-image/index.html`（全文，理解所有流程节点）
- `js/vips-worker.js`（了解 Worker 通信协议）
- `js/vips-loader.js`（了解 wasm-vips 加载）
- SPEC §3.2-A（质量映射表）、§3.2-D（自适应 Dither）

#### 委托上下文

**做什么：**

修改 `compress-image/index.html` 中的压缩逻辑：

**1. 内嵌 inline Web Worker 初始化（在 <script> 底部新增）：**
```javascript
// 在现有压缩脚本区域（约 560-665 行）之后追加
// 不要删除现有代码——新增一个 worker 路径，保留 Canvas fallback
const compressionWorker = new Worker('/js/vips-worker.js');
```

**2. 修改 compressImages() 函数：**
- 在尝试 VipsLoader.load() 后，如果 vips 可用：
  - 发送消息到 compressionWorker 而非直接调用 writeToBuffer
  - 实现 300ms debounce 防抖（仅对 slider 触发，批量压缩按按钮时不禁抖）
  - 使用 requestId 递增计数，Worker 返回结果时检查 id 是否仍匹配
- Canvas fallback 路径保持不变

**3. PNG 参数构建逻辑：**
```javascript
function getPngOptions(quality) {
    const isLossless = document.getElementById('losslessToggle')?.checked || false;
    if (isLossless) {
        return { compression: 9, palette: false, keep: 0 };
    }
    // 映射表
    let Q, dither;
    if (quality >= 90)      { Q = 90; dither = 0.3; }
    else if (quality >= 80) { Q = 80; dither = 0.4; }
    else if (quality >= 70) { Q = 70; dither = 0.5; }
    else if (quality >= 60) { Q = 60; dither = 0.5; }
    else if (quality >= 50) { Q = 50; dither = 0.3; }
    else                    { Q = 40; dither = 0.2; }
    return { palette: true, compression: 9, Q, dither, effort: 7, keep: 0 };
}
```

**4. 自适应 Dither（在 Worker 处理前由主线程计算）：**
```javascript
function detectImageType(imageData) {
    // 4×4 降采样，计算色彩差异方差
    const step = Math.max(1, Math.floor(Math.sqrt(imageData.width * imageData.height) / 4));
    let totalDiff = 0, samples = 0;
    for (let y = 0; y < imageData.height; y += step) {
        for (let x = 0; x < imageData.width; x += step) {
            const i = (y * imageData.width + x) * 4;
            const dr = imageData.data[i] - imageData.data[i + 4] || 0;
            const dg = imageData.data[i + 1] - imageData.data[i + 5] || 0;
            const db = imageData.data[i + 2] - imageData.data[i + 6] || 0;
            totalDiff += Math.sqrt(dr*dr + dg*dg + db*db);
            samples++;
        }
    }
    const avgDiff = totalDiff / samples;
    return avgDiff < 30 ? 'flat' : 'photo';  // 阈值可调
}
// 在构建 options 时覆盖 dither:
// const imgType = detectImageType(...);
// if (imgType === 'flat') options.dither = 0;
```

**5. UI 新增：无损模式开关**
在 compression-options 区域（约 317-334 行）的 "压缩强度" 控件下方追加：
```html
<div class="lossless-toggle" style="margin-top: 0.75rem;">
    <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
        <input type="checkbox" id="losslessToggle">
        <span style="font-size: 0.875rem;">无损模式（仅剥离元数据 + 最大压缩）</span>
    </label>
</div>
```

**注意：**
- 批量压缩（多个文件同时压缩）不走 debounce，直接用按钮触发
- 只有实时预览/单文件压缩走 debounce
- Canvas fallback 路径完全不动

**不做什么：**
- 不修改 `js/vips-loader.js`
- 不删除 Canvas API 降级路径
- 不做对比滑块（那是 Phase 2）

#### 验证标准
- [ ] `compress-image/index.html` 包含 `<script src="/js/vips-worker.js">` 或 Worker 初始化
- [ ] `compress-image/index.html` 包含 `getPngOptions()` 函数（grep -c 'getPngOptions'）
- [ ] `compress-image/index.html` 包含 `detectImageType()` 函数（grep -c 'detectImageType'）
- [ ] 无损模式 toggle 存在（grep -c 'losslessToggle'）
- [ ] 300ms debounce 逻辑存在（grep -c 'debounce\\|setTimeout.*300'）
- [ ] Node.js 语法检查通过：`node -e "require('fs').readFileSync('compress-image/index.html','utf8')"` — 实际上 HTML 无法 node --check，用 grep 确认主要函数存在即可
- [ ] Canvas fallback 仍然存在（grep -c 'compressWithCanvas' ≥ 1）

---

### Task 3 — Phase 1: 长尾目标大小压缩页同步

#### ⚠️ 先读
- `compress-image/index.html`（修改后的版本，了解 getPngOptions 等公共函数）
- `compress-image-to-50kb/index.html`（了解当前结构）
- `compress-image-to-100kb/index.html`
- `compress-image-to-200kb/index.html`
- `compress-image-to-500kb/index.html`

#### 委托上下文

**做什么：**

对 4 个目标大小压缩页做与 compress-image 相同的改造：
- `compress-image-to-50kb/index.html`
- `compress-image-to-100kb/index.html`
- `compress-image-to-200kb/index.html`
- `compress-image-to-500kb/index.html`

**改动点：**
1. 添加 `<script src="/js/vips-worker.js">` 引用（每个页面）
2. 将原有的 Canvas-only 压缩逻辑改为 Worker 路径
3. 实现自适应质量调整循环：从最高质量开始尝试量化，逐步降低 Q/色数直到目标大小达成
4. 保留 Canvas fallback

**自适应循环（伪代码）：**
```javascript
async function compressToTarget(file, targetBytes) {
    const vips = await VipsLoader.load();
    if (!vips) return fallbackToCanvas(file);
    
    for (let q = 90; q >= 30; q -= 10) {
        const options = getPngOptions(q);
        // 发送到 Worker 压缩
        const result = await compressWithWorker(file, options);
        if (result.size <= targetBytes) return result;
    }
    // 如果最低质量仍超目标，返回最低质量的结果
    return finalResult;
}
```

**不做什么：**
- 不做 UI 改造（对比滑块等）
- 不修改 compress-image/index.html
- 不添加无损模式开关到目标大小页（保持简洁）

#### 验证标准
- [ ] 4 个页面都引用了 vips-worker.js（`grep -c 'vips-worker'` = 4）
- [ ] 4 个页面都有 `compressToTarget` 或等效的自适应循环函数
- [ ] 50KB 页面能产出 ≤ 50KB 的 PNG（浏览器测试）
- [ ] 100KB 页面能产出 ≤ 100KB 的 PNG
- [ ] 200KB 同上
- [ ] 500KB 同上

---

### Task 4 — Phase 2: FAQ 修正 + 压缩报告 UI

#### ⚠️ 先读
- `compress-image/index.html`（当前 FAQ 部分，约 436-459 行）
- SPEC §1.3 (FAQ 不匹配)

#### 委托上下文

**做什么：**

1. **FAQ 修正（EN + 所有语言）**
   修改 `compress-image/index.html` 中第 3 条 FAQ：
   - 当前：`"For PNG images, we recommend converting to JPEG or WebP during compression for maximum file size reduction"`
   - 改为：`"Our tool uses smart color quantization for PNG images, reducing 24-bit PNGs to efficient 8-bit palette format with full transparency support. This typically reduces PNG file sizes by 60-80% with minimal visible quality loss. You can also enable lossless mode which strips metadata and applies maximum compression without any quality loss."`
   
   **注意：这需要在所有语言版本（zh/ja/de/fr/es/pt/ar/ko）同步更新。** 每个语言的修改内容只是翻译上述英文文案。但本 Task 仅修改 EN 版本（compress-image/index.html）。多语言翻译留待后续。

2. **压缩报告信息**
   在下载区域（约 342-369 行）的 "Compression Complete!" 面板中追加：
   ```html
   <div class="compression-stats" style="margin-top: 0.5rem; display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.8rem; color: var(--text-light);">
       <span>Mode: <strong id="modeDisplay">Lossy</strong></span>
       <span>Palette: <strong id="paletteDisplay">—</strong> colors</span>
       <span>Dither: <strong id="ditherDisplay">—</strong></span>
   </div>
   ```
   并在压缩结果显示时更新对应的 `modeDisplay` / `paletteDisplay` / `ditherDisplay`。

**不做什么：**
- 不比之前做对比滑块（那是另一个 feature）
- 不修改其他语言版本
- 不做大范围 UI 重构

#### 验证标准
- [ ] 第 3 条 FAQ 不再包含 "convert to JPEG or WebP"（grep -c 'convert to JPEG or WebP' 应为 0）
- [ ] 第 3 条 FAQ 包含 "quantization" 和 "60-80%" 或等价表述
- [ ] 压缩报告区域包含 `id="modeDisplay"`、`id="paletteDisplay"`、`id="ditherDisplay"` 三个新元素
- [ ] JS 中更新了 modeDisplay/paletteDisplay/ditherDisplay 的 textContent

---

## 6. 会话结束清理

每个 Phase 完成后：
```bash
git status
git add <phase-specific-files> PROGRESS.md
git commit -m "fix(png): Phase X — <描述>"
git push
# 检查根目录整洁
```

## 7. Harness 合规对照表

| # | 检查项 | 状态 | 说明 |
|---|-------|------|------|
| I1 | 先读源文件 | ✅ | 每 Task 显式列出先读文件列表 |
| I2 | 项目上下文 | ✅ | SPEC v1.2 作为唯一授权源 |
| S1 | PROGRESS.md 即时更新 | ⏳ | 每 Task 完成时更新 |
| S2 | Git checkpoint 每 Task 一次 | ⏳ | 每 Phase 独立 commit |
| S3 | 特征清单更新 | N/A | 后 MVP 模式，仅 PROGRESS 更新 |
| V1 | Hermes 独立验证 | ⏳ | 每 Task 后 grep/语法检查 |
| V2 | 端到端终验 | ⏳ | 最后一个 Task 后浏览器验证 |
| Sc | WIP=1 规则 | ✅ | 显式声明 |
| L1 | 会话初始化 | ✅ | §1 启动流程已列 |
| L2 | 会话结束清理 | ✅ | §6 清理清单已列 |
| MM | Hermes 不写功能代码 | ⏳ | 全部委托 Claude Code |
