# PicEte 整体优化路线图 — 产品规划总览

> 基于《PicEte vs PicFlow 竞品分析报告》，结合当前项目状态（37 工具 + 8 语言，F1-F7 已完成），
> 按 Harness Engineering 方法论整理的全站优化路线图。

---

## 优化路线图总览

```
P0  ┌─────────────────────────────────┐  ● 底层算力升级 (wasm-vips)
    │                                  │  工作量: 大 | 3-4周
P0.5├─────────────────────────────────┤  ● AVIF 编解码 + RAW 支持 (已在推进)
    │                                  │  工作量: 大 | ~2周 (调研后) 
P1  ├─────────────────────────────────┤  ● mcp-guide 多语言
    │                                  │  工作量: 中 | 1-2天
P2  ├─────────────────────────────────┤  ● 编辑工作流化 (预设系统)
    │                                  │  工作量: 大 | 4-6周
P3  ├─────────────────────────────────┤  ● MCP 生态深化
    │                                  │  工作量: 中 | 2-3周
P4  ├─────────────────────────────────┤  ● 隐私承诺可视化 + OG 修复
    │                                  │  工作量: 小 | 1-2周
P5  └─────────────────────────────────┘  ● 工具交互测试闭环
                                          工作量: 中 | 2-3天
```

---

## P0: 底层算力升级 — WASM-vips 替换 Canvas API

### 现状
- GUI 前端：Canvas API（单线程，大图 OOM）
- MCP 服务端：Node.js Sharp 库（多线程，高性能）
- **两端算力二元性**：同样的操作在前端和后端走不同的技术路径

### 目标
用 `wasm-vips`（libvips 的 WASM 编译版）统一前端管线：
- 多线程处理（WASM 线程）
- 大图支持（>100MB）
- 与 MCP 端统一算力
- 迁移后 MCP Server 可复用同一套 WASM（或保留 Sharp 作为备选）

### 执行步骤

| 阶段 | 内容 | 工期 |
|------|------|------|
| **调研** | 评估 wasm-vips bundle 大小 (预估 2-3MB)、API 覆盖、集成成本 | 1-2天 |
| **POC** | 选取 resize-image 工具重写核心逻辑，对比 Canvas API 性能 | 2-3天 |
| **核心替换** | 压缩类（compress-image 系列）→ 缩放类（resize 系列）→ 分割类（split 系列）→ 取色类 | 2周 |
| **极速模式** | 首页新增极速转换入口，隐藏编辑选项，对标 PicFlow 体验 | 1周 |

**总工期**：3-4 周

### 风险
- wasm-vips 的 WASM bundle ≈ 2-3MB，首次加载时间较长
- 部分 Canvas 原生操作（如像素级取色）可能 wasm-vips 无直接 API 对应
- MCP Server 的 Sharp 保留还是也换 wasm-vips？——建议保留 Sharp，MCP 侧无 bundle 大小限制

---

## P0.5: AVIF 编解码 + LibRaw-WASM RAW 支持

详见 `docs/specs/P02-AVIF-RAW-SPEC.md`

**现已输出的 SPEC，你的确认后即可推进 Phase 1。**

---

## P1: mcp-guide 多语言翻译

### 现状
- mcp-guide/index.html 只有英文
- Makefile 中 `EN_ONLY := mcp-guide` 将其排除在多语言检查之外

### 方案
1. 为 zh/ja/de/fr/es/pt/ar 各生成 mcp-guide/index.html
2. 内容逐项翻译（MCP 指南 + AI 集成说明）
3. 调整 Makefile 的 EN_ONLY 排除规则（去掉 mcp-guide）
4. 更新 sitemap 生成脚本将其纳入 7 语言路径
5. sitemap URL 数扩容 7 条

### 执行策略
子代理并行翻译（7 语言 × 1 页）→ 验证 → sitemap 扩容 → commit & push

**工期**：1-2 天

---

## P2: 编辑工作流化（转换+智能预设）

### 战略背景
PicFlow 编辑功能贫乏（纯转换），PicEte 的编辑优势（像素级缩放、预设裁切、网格分割、主色调提取、目标体积靶向压缩）应转化为可串联的工作流。

### 具体方向

**2a. 可保存的预设系统**
- 用户配置：转 WebP + 缩放到 800px + 添加水印 + 压缩至 100KB
- 保存为预设（localStorage），一键批量应用
- 预设可以分享（Base64 编码预设配置 → URL 参数）

**2b. 电商垂直套件**
- 一键生成淘宝/Amazon/Shopify/拼多多各平台所需尺寸
- 白底图增强（自动移除背景阴影）
- 水印叠加（居中/右下角/平铺）

**2c. 社交媒体套件**
- 各平台封面图模板（Facebook 封面、Twitter Header、LinkedIn Banner、YouTube Thumbnail）
- 一键裁切+缩放+导出系列

**工期**：4-6 周（预设系统 2-3 周 + 电商套件 1-2 周 + 社交套件 1 周）

---

## P3: MCP 生态深化

### 战略背景
MCP 集成是 PicEte 的唯一绝对优势——PicFlow 完全不具备此能力。应在 PicFlow 反应过来之前抢占开发者心智。

### 建议的 MCP 工具扩展

| 新工具 | 功能 | 优先级 |
|--------|------|--------|
| `get_deep_image_metadata` | 探测色彩空间、EXIF、DPI、色深 | 高 |
| `compress_to_target_dynamic` | AI 指令自动逼近目标体积（"压缩到 80KB 以内"） | 高 |
| `batch_convert` | 多文件批量转换 | 中 |
| `generate_thumbnail` | 从任意格式生成缩略图（含 RAW） | 中 |

**MCP→GUI 预览闭环：**
- MCP 服务端处理后自动生成由 PicEte 托管的加密在线预览画廊短链接
- 打通代码终端与 Web 展示的壁垒
- 示例：开发者终端运行 `compress image.png to 100KB` → 返回预览链接 → 浏览器打开

### 工期
2-3 周（核心 3 个新工具 2 周 + 预览闭环 1 周）

---

## P4: 品牌信任可视化 + 小修小补

### 战略背景
PicFlow 在页面显著位置显示"瑞士制造""GDPR 合规""本机处理"等信任符号。PicEte 也在本地处理，但未将此转化为可视化信任资产。

### 具体任务

**4a. "本机处理中"安全指示器**
- 工具页顶部动态状态条："✓ 图像正在您的浏览器中处理，数据不会上传到服务器"
- 使用绿色脉冲动画增强视觉可信度
- 设计参考：类似 HTTPS 锁图标，但更醒目

**4b. OG 标签修复**
- 检查 8 语言各页面的 OG meta 标签是否指向正确的语言对应图片
- 确保社交媒体分享时正确显示标题 + 描述 + 缩略图

**4c. Cookie 同意弹窗 + analytics**
- 简单 Cookie 同意横幅（非 GDPR 必需但提升可信度）
- 接入 Google Analytics 或 Plausible（轻量）

### 工期
1-2 周（安全指示器 3 天 + OG 修复 1 天 + Cookie/analytics 3-5 天）

---

## P5: 工具交互测试闭环

### 现状
- 37 个工具 + 8 语言全部部署
- 但从未系统性地在 Vercel 线上环境测试过每个工具的实际功能
- Harness Engineering 强制要求验证闭环

### 方案

| 工具类别 | 测试项 | 测试方式 |
|---------|--------|---------|
| 转换类 (6个) | 上传图片 → 点击转换 → 下载结果 → 检查格式 | 真实文件上传 |
| 压缩类 (7个) | 上传 → 靶向压缩 → 验证输出体积 ≤ 目标值 | 自动化脚本 + 手工 |
| 缩放类 (12个) | 上传 → 输入尺寸 → 验证输出尺寸精确匹配 | 自动化脚本 + 手工 |
| 分割类 (3个) | 上传 → 分割 → 验证数量+尺寸 | 手工 |
| 取色类 (1个) | 上传 → 验证提取颜色数量+准确性 | 手工 |
| Base64 (1个) | 上传 → 验证输出为 data: URI | 手工 |

### 产出
- `docs/reports/TOOL-TEST-REPORT.md` — 每个工具 + 每个语言的测试结果
- 修复发现的问题
- Bug 追踪：新增 feature_list items 标记为 bug

### 工期
2-3 天（自动化脚本 1 天 + 手工验证 + 修复 1-2 天）

---

## 执行顺序建议

你之前已经确认了 P0.5（AVIF + RAW）优先。以下是推荐的全局顺序：

```
Now     → P0.5  AVIF + RAW          (你已确认方向)
Next    → P5    工具测试闭环         (了解现状后再决定其他方向)
        → P1    mcp-guide 多语言    (小任务，顺手做完)
Near    → P0    wasm-vips 替换     (大工程，需 POC 验证)
        → P4    品牌信任            (小修小补，可穿插)
Future  → P3    MCP 深化           (依赖 AVIF/RAW 基础)
        → P2    编辑工作流化        (最大工程，等基础稳固后)
```

---

## 附：与 feature_list.json 的映射

| 方向 | 新增 feature ID | 预估新增 tools |
|------|----------------|---------------|
| AVIF 编解码 | tool-039 ~ 042 | png-to-avif, jpg-to-avif, webp-to-avif, avif-to-png |
| RAW 支持 | tool-043 ~ 046 | raw-to-jpg, raw-to-png, raw-to-webp, raw-to-avif |
| mcp-guide 多语言 | infra-004 | 每个语言 1 页 = 7 pages |
| 预设系统 | tool-047 | — |
| 电商套件 | tool-048 ~ 050 | 3-5 页 |
| MCP 工具扩展 | tool-051 ~ 053 | — |
| 安全指示器 | ui-001 | — |

---

*文档位置: `docs/specs/PICETE-ROADMAP.md`*
