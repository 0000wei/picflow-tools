# P02: AVIF 编解码 + LibRaw-WASM RAW 支持 — 产品规格

> 基于研究报告《PicEte vs PicFlow 竞品分析》建议二，针对"格式转换能力差距"的专项优化计划。
> 遵循 Harness Engineering 方法论，WIP=1，一次只做一件事。

---

## 一、背景与目标

### 竞品差距

PicFlow 已具备：
- 30+ 常规格式 + 17 种相机 RAW 格式
- RAW→AVIF / RAW→WebP / RAW→JPG 等完整管线
- LibRaw-WASM 浏览器端解码（零上传）
- RAW 批量转换

PicEte 现状：
- 仅 3 个核心格式（JPG/PNG/WebP）+ 2 个派生格式（Base64）
- AVIF 支持：零
- RAW 支持：零
- 当前 Canvas API 无法解码 AVIF/RAW

### 战略目标

1. **与 PicFlow 同台竞争**：补齐 AVIF（下一代 Web 图像标准）编解码能力
2. **差异化超越**：不只是转换，而是提供"极速"与"极限压缩"两套预设
3. **截获高端流量**：通过 RAW 支持吸引摄影师、设计师群体，切入 PicFlow 的核心用户池
4. **为 MCP 生态铺路**：AVIF/RAW 支持 → MCP 工具 `get_deep_image_metadata` 可读取 EXIF/色彩空间

---

## 二、功能范围

### Feature A: AVIF 编解码支持（P0.5）

**核心转换工具（新增 4 个工具页）：**

| 新工具 | URL路径 | 输入→输出 |
|--------|---------|-----------|
| PNG to AVIF 转换 | `png-to-avif/` | PNG → AVIF |
| JPG to AVIF 转换 | `jpg-to-avif/` | JPG → AVIF |
| WebP to AVIF 转换 | `webp-to-avif/` | WebP → AVIF |
| AVIF to PNG 转换 | `avif-to-png/` | AVIF → PNG |

**两套压缩预设（每工具均提供）：**
- **极速模式**：编码速度优先，输出质量 80%，适用于日常 Web 使用
- **极限压缩模式**：文件体积优先，质量 50%，进一步压缩 30-50%

**AVIF 解码器选型：**
- 使用 `@saschazar/wasm-avif` 或 `libavif-wasm` 编译版
- 在浏览器端通过 WASM 解码 AVIF → Canvas/原始像素数据
- 编码使用 AVIF encoder WASM（输出 AVIF 文件）

**目标效果：**
- 相比 WebP，AVIF 极限压缩模式文件体积再减少 30-50%
- 相比 JPG，AVIP 在同样质量下文件体积减少 50%+
- 大图（>20MB）处理不下沉到 Node.js，保持纯前端

### Feature B: RAW 图像支持（P1）

**核心功能：** 在浏览器端解析专业相机 RAW 文件

**技术选型：** `libraw-wasm`（LibRaw 的 Emscripten 编译版）
- 支持 17+ 种相机 RAW 格式（CR2/NEF/ARW/DNG/RAF/ORF 等）
- 浏览器端解码，零上传
- 解码后渲染到 Canvas，再执行后续转换/编辑

**新增转换工具：**

| 新工具 | URL路径 | 输入→输出 |
|--------|---------|-----------|
| RAW to JPG | `raw-to-jpg/` | RAW → JPG |
| RAW to PNG | `raw-to-png/` | RAW → PNG |
| RAW to WebP | `raw-to-webp/` | RAW → WebP |
| RAW to AVIF | `raw-to-avif/` | RAW → AVIF（依赖 Feature A 完成） |

**目标流量词：**
- "raw to jpg converter"
- "convert cr2 to jpg"
- "nef to png"
- "raw image viewer online"
- "camera raw file converter"
- "sony arw to jpg"

---

## 三、禁止范围（Out of Scope）

此 SPEC 中不做：
- ❌ WASM-vips 全面替换 Canvas API（此为 P0 另一方向）
- ❌ 批量 RAW 转换 UI（多文件上传）
- ❌ EXIF 元数据可视化编辑器
- ❌ MCP 工具的 `get_deep_image_metadata` 扩展（交由将来的 MCP 深化计划）
- ❌ 编辑工作流化/预设系统
- ❌ 电商垂直套件

---

## 四、技术方案

### 4.1 AVIF 编码/解码管线

```
用户上传图片
    │
    ▼
Canvas API 解码输入格式 (JPG/PNG/WebP)
    │
    ▼
像素数据 → WASM AVIF Encoder → AVIF 文件
    │
    ▼
浏览器下载/预览

预设参数:
  - 极速: quality=80, speed=6 (最快编码)
  - 极限压缩: quality=50, speed=0 (最小体积)
```

**依赖评估：**
- `@saschazar/wasm-avif` ≈ 800KB WASM bundle
- 首次加载约 1-2s，缓存后即时
- 注意：AVIF 编码在浏览器端较慢，大图（>4000px）需加 loading 状态

### 4.2 RAW 解码管线

```
用户上传 RAW 文件 (.CR2/.NEF/.ARW/.DNG 等)
    │
    ▼
libraw-wasm 解码 → RGBA 像素数据
    │
    ▼
Canvas 渲染 → 后续转换/编辑操作
    │
    ▼
(可选) AVIF/WebP/JPG/PNG 编码输出
```

**依赖评估：**
- `libraw-wasm` ≈ 1.5-2MB WASM bundle
- 加载需 2-3s，可做 splash loading
- 解码速度：20MP RAW 约 0.5-1.5s（浏览器端）

### 4.3 文件组织

```
picete/
├── raw-to-jpg/          ← 新工具目录
│   ├── index.html       ← EN 版本
│   └── script.js        ← RAW 解码 + 转换逻辑
├── raw-to-png/
├── raw-to-webp/
├── raw-to-avif/
├── png-to-avif/
├── jpg-to-avif/
├── webp-to-avif/
├── avif-to-png/
├── js/
│   ├── avif-encoder.js  ← AVIF 编码 WASM 封装
│   ├── avif-decoder.js  ← AVIF 解码 WASM 封装
│   └── raw-decoder.js   ← libraw-wasm 封装
├── zh/raw-to-jpg/       ← 多语言镜像
├── ja/raw-to-jpg/
├── ... 其余语言同理
```

### 4.4 多语言

8 种语言（EN/ZH/JA/DE/FR/ES/PT/AR）全部覆盖。按照已有翻译流程：
1. EN 版本开发完成
2. 并行委托 7 个子代理完成翻译

---

## 五、实现阶段

### Phase 1: AVIF 编解码（WIP=1）

| 步 | 内容 | 预计工期 |
|----|------|---------|
| 1.1 | 调研 WASM AVIF 编解码库（测试 bundle 大小/兼容性/性能） | 1天 |
| 1.2 | 封装 `avif-encoder.js` + `avif-decoder.js` | 1天 |
| 1.3 | 开发 png-to-avif 工具页（含两套预设 UI） | 0.5天 |
| 1.4 | 开发 jpg-to-avif / webp-to-avif 工具页 | 0.5天 |
| 1.5 | 开发 avif-to-png 工具页 | 0.5天 |
| 1.6 | 多语言翻译（7 种语言 × 4 页） | 1天 |
| 1.7 | 更新 sitemap + robots + feature_list + PROGRESS | 0.5天 |
| **小计** | **AVIF Phase** | **~5天** |

### Phase 2: RAW 解码支持（WIP=1）

| 步 | 内容 | 预计工期 |
|----|------|---------|
| 2.1 | 调研 libraw-wasm bundle + 编译/配置 | 1天 |
| 2.2 | 封装 `raw-decoder.js`（支持 17 种 RAW 格式解码） | 2天 |
| 2.3 | 开发 raw-to-jpg 工具页 | 0.5天 |
| 2.4 | 开发 raw-to-png / raw-to-webp 工具页 | 0.5天 |
| 2.5 | 开发 raw-to-avif 工具页（依赖 Phase 1 完成） | 0.5天 |
| 2.6 | 多语言翻译（7 种语言 × 4 页） | 1天 |
| 2.7 | 更新 sitemap + feature_list + PROGRESS | 0.5天 |
| 2.8 | 首页新增 RAW 支持宣传区块 + 安全指示器 | 0.5天 |
| **小计** | **RAW Phase** | **~6.5天** |

**总计：约 11.5 个工作日（含调研）**

---

## 六、验证标准

### AVIF 验证

- [ ] WASM AVIF encoder 成功加载（console 无报错）
- [ ] png-to-avif：上传 PNG → 选择预设 → 输出 AVIF 文件可下载
- [ ] jpg-to-avif：同上
- [ ] webp-to-avif：同上
- [ ] avif-to-png：上传 AVIF → 输出 PNG 可打开
- [ ] 极速模式 vs 极限压缩：文件体积差异显著（>30%）
- [ ] 3MB+ 图片处理无 OOM
- [ ] 8 种语言页面正常渲染

### RAW 验证

- [ ] libraw-wasm 成功加载
- [ ] raw-to-jpg：上传 .CR2 → 输出 JPG 可打开
- [ ] raw-to-png：上传 .NEF → 输出 PNG
- [ ] raw-to-webp：上传 .ARW → 输出 WebP
- [ ] raw-to-avif：上传 .DNG → 输出 AVIF
- [ ] 至少支持 5 种常见 RAW 格式（CR2/NEF/ARW/DNG/RAF）
- [ ] 20MP RAW 解码 < 3s
- [ ] 8 种语言页面正常渲染

---

## 七、风险评估

| 风险 | 概率 | 影响 | 缓解方案 |
|------|------|------|----------|
| libraw-wasm 编译版本过大（>3MB） | 中 | 高 | 动态加载，仅 RAW 页面才加载；或考虑 WebCodecs API 部分替代 |
| AVIF 编码在浏览器端过慢 | 中 | 中 | 增加 loading 动画；大图分块处理 |
| Canvas API 无法处理超大 RAW 文件（>50MP） | 中 | 中 | 提示文件上限；或降采样预览 |
| 部分浏览器不支持 WASM | 低 | 高 | 优雅降级：提示"请更新浏览器" |
| MCP Server 若要用 AVIF/RAW 功能需依赖 WASM | 低 | 中 | MCP 端可使用 Sharp 原生库（非 WASM），无需改造 |

---

## 八、决策点

开始前需要你确认：

1. **Phase 1（AVIF）先跑还是两阶段一起？** — 建议先 AVIF，技术路径更短、见效更快
2. **是否优先做 raw-to-jpg 一个工具验证**？ — 确认 WASM 可行后再铺开 4 个 RAW 工具
3. **首页要不要增加"支持 AVIF/RAW"的宣传横幅？** — 放在 Phase 2 末尾
4. **sitemap 更新策略**：一次性扩容还是每步更新？
