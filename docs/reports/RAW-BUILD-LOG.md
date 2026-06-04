# RAW 支持 — 方案 C 构建记录

## 概述

**任务：** 自编译 wasm-vips（v0.0.17）+ libraw（0.22.1），启用 RAW 图像解码支持。

**最终结果：** ✅ 第 16 次构建成功，`vips.config()` 显示 `RAW load with libraw_r: true`

## 修改文件

### build.sh（自编译 wasm-vips）

位置：`scripts/raw-build/build.sh`（PicEte 项目内备份）
原版：`/tmp/wasm-vips/build.sh`（wasm-vips 克隆仓库）

### 修改总计

| 修改点 | 行号 | 说明 |
|--------|------|------|
| `VERSION_RAW=0.22.1` | ~191 | 版本变量 |
| `printf "raw": "${VERSION_RAW}"` | ~224 | versions.json 条目 |
| libraw 编译块（14 行） | ~520-566 | Emscripten 交叉编译 + pkg-config 生成 |
| `-Draw=enabled` | ~591 | vips meson 配置启用 raw |
| `ninja -C _build -j2` | ~592 | 限制并行度防 OOM |

## 构建历程

### Phase A：环境准备（Task 0.5.0）

| 尝试 | 问题 | 修复 |
|------|------|------|
| — | Docker 未安装 | `apt-get install docker.io` |
| — | Docker Hub 网络不可达 | 配置 Clash 代理到 Docker daemon |
| — | 容器内没有代理 | `--network host` + `-e HTTP_PROXY` |
| 1 | zlib-ng 下载失败 | 容器内需代理访问 GitHub |
| 2 | 标准构建成功 ✅ | — |

### Phase B：RAW 编译（Task 0.5.7-0.5.9）

`16 次构建，15 次失败`

| # | 问题 | 错误信息 | 修复 |
|---|------|---------|------|
| 1 | 标准构建（不改 build.sh） | `RAW load with libraw: false` | 确认 RAW 被禁用 ✅（预期行为） |
| 2 | CMakeLists.txt 不存在 | `source directory does not contain CMakeLists.txt` | 从 `LibRaw-cmake` 仓库下载 CMakeLists.txt |
| 3 | cmake 模块缺失 | `include could not find MacroBoolTo01.cmake` | 下载 3 个 cmake helper 模块 |
| 4 | cmake 目录不存在 | `curl: exit code 23`（写文件失败） | `mkdir -p cmake` |
| 5 | sed 破坏 CMake 嵌套 | `Flow control statements are not properly nested` | 改用自定义最小 CMakeLists.txt（cat heredoc） |
| 6 | GLOB 不递归子目录 | 库仅 17KB（只编译 2 个 .o） | `GLOB` → `GLOB_RECURSE` |
| 7 | 缓存跳过编译 | 旧 libraw_r.a 在 target 中，条件跳过 | `[ -f ... ]` → 强制 `rm -f` |
| 8 | shell 语法错误 | `syntax error near unexpected token )` | 删除`||(` 但保留结束 `)`；改成 `rm -f + (` |
| 9 | vips.pc 缓存 | meson 使用旧 vips.pc（无 RAW） | 强制删除 `vips.pc` |
| 10 | libraw 头文件路径 | `fatal error: 'libraw/libraw.h' file not found` | `install(FILES ... DESTINATION include/libraw)` |
| 11 | libraw 头文件内引用 | `fatal error: 'libraw_datastream.h' file not found` | `install(DIRECTORY libraw/ DESTINATION include/libraw FILES_MATCHING PATTERN "*.h")` |
| 12 | OOM | ninja 编译被 kill（exit code 255） | `ninja -C _build -j2` |
| 13-16 | 逐步修复上述问题 | | |
| **17** | **V2 第 1 次构建：MAXIMUM_MEMORY=2GB** | 21 次测试 18/3 通过。Sony α7III v4.01 ARW 3 次全失败 | WASM heap 碎片化——连续解码 6 个大文件后第 7 个失败 |
| **18** | **V2 第 2 次构建：MAXIMUM_MEMORY=4GB** | ✅ **21/21 全部通过**。Sony ARW 3/3 通过 | 扩大 WASM 最大内存后 heap 空间充足 |
| **19** | **最终验证：12 个 RAW 文件（含 66MB Sony ARW）** | 11/12 通过，66MB 需 `--max-old-space-size=8192` | 8.0s 解码 4.0MB JPEG |

## 关键修复总结

### 1. CMakeLists.txt

LibRaw 官方不维护 CMake 支持。CMakeLists.txt 在独立的 [LibRaw-cmake](https://github.com/LibRaw/LibRaw-cmake) 仓库。

**最佳做法：** 不用 LibRaw-cmake 的 CMakeLists.txt（含复杂的 LCMS/ZLIB/JPEG 依赖检测，Emscripten 下会失败）。直接用自定义最小 CMakeLists.txt：

```cmake
cmake_minimum_required(VERSION 3.0)
project(LibRaw C CXX)
set(CMAKE_CXX_STANDARD 11)
option(DISABLE_DNG "Disable DNG support" OFF)
file(GLOB_RECURSE LIBRAW_SOURCES src/*.cpp libraw/*.cpp internal/*.cpp)
add_definitions(-DLIBRAW_NOTHREADS -DNO_LCMS -DDISABLE_JPEG)
if(DISABLE_DNG)
  add_definitions(-DDISABLE_DNG)
endif()
add_library(libraw_r STATIC ${LIBRAW_SOURCES})
target_include_directories(libraw_r PUBLIC .)
install(TARGETS libraw_r DESTINATION lib)
install(DIRECTORY libraw/ DESTINATION include/libraw
  FILES_MATCHING PATTERN "*.h")
install(FILES libraw_r.pc.in DESTINATION lib/pkgconfig)
```

### 2. 头文件安装

vips 的 `dcrawload.c` 通过 `#include <libraw/libraw.h>` 引用 LibRaw。LibRaw 的 `libraw.h` 内部引用 `libraw_datastream.h`（相对路径）。

**正确安装方式：**
```cmake
install(DIRECTORY libraw/ DESTINATION include/libraw
  FILES_MATCHING PATTERN "*.h")
```
这将 `libraw/` 下的所有 `.h` 文件安装到 `include/libraw/`。

### 3. pkg-config 文件

LibRaw 源码包中的 `libraw_r.pc.in` 是 autotools 模板，cmake 不会处理它。需要手动创建 `.pc` 文件：

```bash
cat > "$TARGET/lib/pkgconfig/libraw_r.pc" << PCEOF
prefix=$TARGET
libdir=\${prefix}/lib
includedir=\${prefix}/include
Name: libraw_r
Description: Raw image decoder library (Emscripten)
Version: $VERSION_RAW
Libs: -L\${libdir} -lraw_r
Cflags: -I\${includedir}
PCEOF
```

### 4. 缓存管理

wasm-vips 的 build.sh 使用 `[ -f "$TARGET/lib/pkgconfig/xxx.pc" ]` 跳过已编译的依赖。跨构建时 target 目录不清除，导致跳过带 RAW 的 vips 重编译。

**修复：** 在 libraw 编译块前强制删除旧的缓存：

```bash
rm -f "$TARGET/lib/libraw_r.a" "$TARGET/lib/pkgconfig/libraw_r.pc"
rm -f "$TARGET/lib/pkgconfig/vips.pc"
```

### 5. OOM 防护

Emscripten 编译 386 个文件（vips + 依赖）时可能耗尽内存（8GB，swap 满）。

**修复：** 限制并行度 `ninja -C _build -j2`（原为默认的 `nproc=4`）。

## 产物

| 文件 | 大小 | 说明 |
|------|------|------|
| `vips.wasm` | 5.84MB | 核心 WASM（含 libraw） |
| `vips-heif.wasm` | 3.15MB | AVIF/HEIC 动态模块 |
| `vips-jxl.wasm` | 2.17MB | JPEG XL 动态模块 |
| `vips-resvg.wasm` | 1.16MB | SVG 动态模块 |
| `libraw_r.a` | 1.79MB | LibRaw 静态库（仅 Emscripten target） |

## 容器构建命令

```bash
sg docker -c "docker run --rm --name wasm-vips-raw --network host \
  -v /tmp/wasm-vips:/src \
  -e HTTP_PROXY=http://127.0.0.1:7897 \
  -e HTTPS_PROXY=http://127.0.0.1:7897 \
  wasm-vips"
```

关键参数：
- `--network host`：容器使用宿主机网络栈（Clash 代理可达）
- `-e HTTP_PROXY=http://127.0.0.1:7897`：代理配置（Clash 端口）
- `-v /tmp/wasm-vips:/src`：挂载 wasm-vips 仓库到容器内

## 测试验证

```bash
# Node.js 验证 RAW 支持
node -e "const v=require('/tmp/wasm-vips/lib/vips-node.js'); \
  (async()=>{const vv=await v(); console.log(vv.config())})()" \
  | grep -i raw

# 预期输出：RAW load with libraw_r: true
```

## 环境依赖

| 依赖 | 版本 | 说明 |
|------|------|------|
| Docker | 29.1.3 | 容器化构建环境 |
| Clash Verge | — | 代理，端口 7897 |
| wasm-vips | v0.0.17 | 构建目标 |
| LibRaw | 0.22.1 | RAW 解码库 |
| Emscripten | 5.0.7 | 由 Docker 镜像提供 |
| emscripten/emsdk | 5.0.7 | Docker 基础镜像 |
| 磁盘空间 | >20GB | 构建中间文件 ~8GB |
| 内存 | >4GB | 建议 8GB+（否则 -j2） |
