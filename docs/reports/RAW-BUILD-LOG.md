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

### V3 (2026-06-04): 单线程尝试失败 → 多线程 clean build 成功 + RAW 文件解码验证

| # | 构建 | 问题 | 修复 |
|---|------|------|------|
| 1 | 单线程 -pthread 去掉 | `bash --disable-svg: invalid option` — CLI 参数传给 bash 非 build.sh | `SVG=false` 直接在 build.sh 设置 |
| 2 | 同上 | `mkdir: cannot create directory /src/build/deps` — 无父目录 | `mkdir $DEPS` → `mkdir -p $DEPS` |
| 3 | 同上 | `Cannot find emscripten-cross.ini` — `rm -rf build/` 删了 git 追踪文件 | 只删 build/deps build/target，保留 *.ini |
| 4 | 同上 | `MacroBoolTo01: Unknown CMake command` — LibRaw-cmake 不兼容 | 自定义最小 CMakeLists.txt（cat heredoc） |
| 5 | 同上 | `Dependency libraw_r not found` — 无 .pc 文件 | 手动 cp .a + 生成 .pc 文件 |
| 6 | 同上 | `--shared-memory is disallowed by plugin_registry.cc.o` — side module 链接 | `MODULES=true`（恢复） |
| 7 | 同上 | `mimalloc-mt` / `dlmalloc-mt` 多线程链接 → `gcancellable.c.o` 无 atomics | 恢复 `-sMALLOC=mimalloc` |
| 8 | 同上 | `__wasm_longjmp` 缺失 — WASM_EH 与传统异常不兼容 | 恢复 `WASM_EH=true` |
| **9** | **多线程 clean build** | — | **✅ exit 0，`RAW load with libraw_r: true`** |
| **10** | **浏览器 RAW 解码测试** | **Node.js: ✅ 12/12 RAW 文件解码通过。浏览器头: ✅ vips.js 加载成功，但 headless Chrome 不支持 SharedArrayBuffer** | 需 Vercel 部署后浏览器端验证 |

### 关键发现：libvips 内嵌 pthread API，单线程不可行

libvips 源码（通过 wasm-vips Emscripten patch）包含 `pthread_setattr_default_np` 等 pthread API 调用。Emscripten 仅在 `-pthread` 模式下提供这些符号。因此 **没有 -pthread 时无法链接 libvips**。必须使用多线程模式。

多线程 WASM 的依赖链必须一致地使用 `-pthread` 编译，且：
1. 在 vips meson setup 前清理依赖 .pc 文件中的 `-pthread`（避免 meson 传播冲突到 JS bindings）
2. 在 JS bindings meson setup 前清理 vips.pc 的 `-pthread`
3. SVG=false（跳过 resvg 的 Rust 编译）
4. Emscripten emcache 必须在 start 时清空（确保 -mt 运行时库全部用 atomics 重建）

### Bundle 大小（多线程）

| 文件 | V2（多线程含 libraw） | V3（多线程含 libraw） | 说明 |
|------|---------------------|---------------------|------|
| vips.wasm | 5,836,003 | 5,834,491 | 核心 WASM |
| vips-heif.wasm | 3,151,583 | 3,151,583 | AVIF 动态模块 |
| vips-jxl.wasm | — | 2,172,564 | JXL 动态模块 |

### Task 0.5.11 浏览器测试结果

- ✅ Node.js 端：12/12 RAW 文件全部通过（Canon CR2/CR3, Nikon NEF, Sony ARW, Adobe DNG）
- ✅ 浏览器：vips-es6.js 动态加载成功
- ⚠️ 浏览器端 RAW 上传→解码→预览验证：因 headless Chrome 不支持 SharedArrayBuffer 无法完成
- ⏩ 浏览器端验证需 Vercel 生产部署后使用真实 Chrome/Firefox 桌面版完成

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
