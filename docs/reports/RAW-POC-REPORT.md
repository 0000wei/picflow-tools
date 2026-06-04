# RAW 支持 POC 报告

> 日期：2026-06-04
> 项目：PicEte（picete.com）
> 技术方案：自编译 wasm-vips（v0.0.17）+ LibRaw（0.22.1）

## 1. 技术方案

### 方案选择：C（自编译 wasm-vips 加入 libraw）

| 对比 | 方案 A（libraw-wasm） | 方案 B（MCP Sharp） | **方案 C（自编译）** |
|------|---------------------|-------------------|-------------------|
| 路径 | 独立 WASM bundle | 服务端解码 | **统一 wasm-vips 管线** |
| Bundle | +2MB 独立 WASM | 无 | **5.8MB（含所有 codec）** |
| 浏览器端 | ✅ 可用 | ❌ 需 MCP | **✅ 可用** |
| 维护 | 2 个 WASM 版本 | 服务端依赖 | **1 个 WASM 版本** |

### 构建环境

| 依赖 | 版本 | 说明 |
|------|------|------|
| Docker | 29.1.3 | 容器化 Emscripten 构建 |
| wasm-vips | v0.0.17 | 上游仓库 |
| LibRaw | 0.22.1 | RAW 解码库（GitHub tag） |
| Emscripten | 5.0.7 | 由 Docker 镜像 `emscripten/emsdk:5.0.7` 提供 |
| Clash Verge | — | 代理（Docker Hub 国内不可达） |

### 构建命令

```bash
sg docker -c "docker run --rm --name wasm-vips-raw --network host \
  -v /tmp/wasm-vips:/src \
  -e HTTP_PROXY=http://127.0.0.1:7897 \
  -e HTTPS_PROXY=http://127.0.0.1:7897 \
  wasm-vips"
```

## 2. 构建统计

| 指标 | V1（第 1-16 次） | V2（第 17-19 次） |
|------|-----------------|-----------------|
| 构建次数 | 16 | 3 |
| 成功 | 1（config 通过） | 3（2 次 config + 1 次 21/21） |
| 失败原因 | CMake/头文件/缓存/OOM 等 | heap 碎片化（2GB→4GB） |
| **总迭代** | **19 次构建** | |
| **总耗时** | **~12 小时**（含编译等待） | |

### 关键修复点

按修复顺序：

1. Docker 代理配置（Clash → daemon）
2. 自定义最小 CMakeLists.txt（替代 LibRaw-cmake）
3. GLOB → GLOB_RECURSE（递归源文件）
4. 头文件安装路径修正（include/libraw/）
5. pkg-config 文件生成
6. 缓存管理（强制删除 vips.pc）
7. 并行度限制（ninja -j2 防 OOM）
8. **ALLOW_MEMORY_GROWTH + MAXIMUM_MEMORY=4GB**（核心修复）

## 3. 兼容性矩阵

| 品牌 | 格式 | 文件数 | 全部通过 | 平均解码时间 | 输出质量 |
|------|------|--------|---------|------------|---------|
| Canon | CR2 | 1 | ✅ | 5s | 1.2MB JPEG (5040×3360) |
| Canon | CR3 | 2 | ✅ | 5-12s | 1.4MB JPEG (6000×4000) |
| Nikon | NEF | 4 | ✅ | 6-9s | 2.3MB JPEG (6064×4040) |
| Sony | ARW | 4 | ✅ | 5-10s | 2.0MB JPEG (6024×4024) |
| Adobe | DNG | 1 | ✅ | 2s | 845KB JPEG |

完整兼容性矩阵见 `docs/reports/RAW-COMPATIBILITY.md`。

21 次重复测试（7 文件 × 3 轮）全部通过。

## 4. 性能数据

### 按格式

| 格式 | 最小 | 最大 | 平均解码 |
|------|------|------|---------|
| CR2 | 26MB → 1.2MB | 26MB → 1.2MB | 5.3s |
| CR3 | 7.5MB → 1.1MB | 8.7MB → 1.6MB | 8.4s |
| NEF | 26MB → 1.9MB | 30MB → 2.8MB | 7.6s |
| ARW | 24MB → 1.0MB | 66MB → 4.0MB | 6.5s |
| DNG | 6MB → 845KB | 6MB → 845KB | 2.1s |

### Bundle 大小

| 文件 | 原始（npm v0.0.17） | 自编译（含 libraw） | 变化 |
|------|-------------------|------------------|------|
| vips.wasm | 5,894,485 | 5,836,003 | **-58KB（更小）** |
| vips-heif.wasm | 4,669,481 | 3,151,583 | 动态模块 |

核心 WASM 没有因加入 libraw 而膨胀（libraw 的 1.8MB 静态库被链接到核心 WASM 中，但整体大小反而略降，因为编译优化参数差异）。

## 5. 已知限制

1. **WASM heap 碎片化**：连续解码 6+ 个大 RAW 文件后可能失败。已通过 `ALLOW_MEMORY_GROWTH` + `MAXIMUM_MEMORY=4GB` + 每 decode 后 GC 缓解。
2. **大文件（>50MB）浏览器端**：66MB ARW 在 Node.js 中需 `--max-old-space-size=8192`。浏览器端内存限制更严格，未测试。
3. **CR3 大 XMP 警告**：`large XMP not saved` 不影响输出质量。
4. **DNG 变体**：只测试了 Adobe DNG（Canon 转换），未测试线性 DNG、JPEG-in-DNG 等。
5. **浏览器端未验证**：Node.js 端通过，但浏览器端的 COOP/COEP + WASM 加载 + 大文件解码尚未测试（Task 0.5.10）。
6. **实验性格式未测试**：20 种格式（RAF/RW2/ORF/PEF/X3F 等）标记为实验性。

## 6. 后续规划

| Task | 内容 | 依赖 |
|------|------|------|
| 0.5.10 | 浏览器 RAW 解码验证（替换 js/lib/ WASM） | Node.js 验证通过 |
| 0.5.11 | raw-to-jpg 工具页（第一个 RAW 工具） | 浏览器验证通过 |
| 0.5.12+ | 其余工具页 + 翻译 + 入口 | — |
