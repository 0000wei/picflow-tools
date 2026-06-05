# Phase 0.8: 单线程 wasm-vips 编译与部署

## 问题根因

自编译的 wasm-vips 使用 Emscripten pthread（多线程）模式。在 COEP require-corp 环境下：
1. Worker 线程内 WASM 初始化失败（路径解析 + Atomics.wait 死锁）
2. 主线程 `Vips()` 永久等待 Worker 就绪
3. 30 秒超时后 VipsLoader 返回错误

## 解决方案

重新编译单线程版 wasm-vips（`-sUSE_PTHREADS=0`），不需要 Worker、SharedArrayBuffer，在 COEP require-corp 下正常工作。

## 实施步骤

### Step 1: 修改 build.sh（本地 + picete 备份）

文件: `/tmp/wasm-vips/build.sh` 和 `picete/scripts/raw-build/build.sh`

| 行 | 当前 | 改为 |
|----|------|------|
| 125 | `export RUSTFLAGS="... -Ctarget-feature=+atomics ..."` | 移除 `-Ctarget-feature=+atomics` |
| 130 | `COMMON_FLAGS="-Os -pthread"` | `COMMON_FLAGS="-Os"` |

### Step 2: 修改 meson.build

文件: `/tmp/wasm-vips/src/meson.build`

| 行 | 当前 | 改为 |
|----|------|------|
| 94-107 | web_link_args 含 `-sPTHREAD_POOL_SIZE=...` 和 `--use-preload-plugins` | 移除 PTHREAD_POOL_SIZE，移除环境限制（-sENVIRONMENT=web 保留） |
| 56-74 | main_link_args | 无需改动（ALLOW_MEMORY_GROWTH、MALLOC=mimalloc 等保留） |
| 114 | `--pre-js=@0@'.format(source_dir / 'workaround-cors-pre.js')` | 保留（单线程下也需要正确路径） |

### Step 3: 执行 clean build

```bash
cd /tmp/wasm-vips
sudo rm -rf build/deps build/target build/ccache build/emcache
git checkout -- build/
sg docker -c "docker run --rm --name wasm-vips-st --network host \
  -v /tmp/wasm-vips:/src \
  wasm-vips" 2>&1 | tee /tmp/build-st.log
```

### Step 4: 验证构建产物

```bash
ls -la /tmp/wasm-vips/lib/vips*.wasm /tmp/wasm-vips/lib/vips*.js
node -e "const v=require('/tmp/wasm-vips/lib/vips-node.js'); (async()=>{const vv=await v(); console.log(vv.config())})()"
```

关键检查：config() 输出应包含 `RAW load with libraw_r: true`。

### Step 5: 替换 js/lib/ 文件

```bash
cp /tmp/wasm-vips/lib/vips.wasm /tmp/wasm-vips/lib/vips.js \
   /tmp/wasm-vips/lib/vips-heif.wasm /tmp/wasm-vips/lib/vips-jxl.wasm \
   /tmp/wasm-vips/lib/vips-es6.js \
   picete/js/lib/
rm -f picete/js/lib/vips-resvg.wasm  # 新构建不产生
```

### Step 6: 恢复 vips-loader.js 的原始逻辑（移除 workaroundCors）

单线程版不需要 worker 相关兼容代码。将 Promise.race 超时保留（防御性设计），但移除 workaroundCors 相关的参数设置。

### Step 7: 验证 + 部署

```bash
cd picete && make verify
git add -f js/lib/*.wasm js/lib/*.js
git commit -m "build: rebuild wasm-vips in single-thread mode"
git push origin master
```

## 回退方案

如果单线程构建失败，回退到 npm wasm-vips v0.0.17（不含 libraw），RAW 工具页用 Canvas 降级路径显示提示信息。
