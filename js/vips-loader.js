// VipsLoader — wasm-vips 动态加载器
// 用法：
//   const vips = await VipsLoader.load();
//   if (vips) { /* use wasm-vips pipeline */ }
//   else { /* fallback to Canvas API */ }

const VipsLoader = {
  // 状态
  status: 'unloaded', // 'unloaded' | 'loading' | 'ready' | 'error'
  instance: null,
  error: null,

  // 加载 wasm-vips
  // 返回: vips instance 或 null（降级到 Canvas）
  async load() {
    if (this.status === 'ready') return this.instance;
    if (this.status === 'loading') {
      // 如果已经在加载，等待完成
      while (this.status === 'loading') {
        await new Promise(function (resolve) { return setTimeout(resolve, 100); });
      }
      return this.instance;
    }

    this.status = 'loading';

    try {
      // 检查 SharedArrayBuffer 是否可用
      if (typeof SharedArrayBuffer === 'undefined' || !self.crossOriginIsolated) {
        console.warn('[VipsLoader] SharedArrayBuffer unavailable, falling back to Canvas');
        this.status = 'error';
        this.error = 'SharedArrayBuffer not available';
        return null;
      }

      // 加载 wasm-vips
      // 优先从 window.Vips（由 script 设置）
      var Vips = window.Vips;
      if (!Vips) {
        await new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.src = '/js/lib/vips.js';
          script.onload = () => {
            Vips = window.Vips;
            resolve();
          };
          script.onerror = () => reject(new Error('Failed to load vips.js script'));
          document.head.appendChild(script);
        });
        console.log('[VipsLoader] vips.js loaded via script tag');
      }

      // 初始化 wasm-vips，带 120 秒超时（多线程 + 大 WASM 下载需要时间）
      var initPromise = Vips({
        mainScriptUrlOrBlob: '/js/lib/vips.js',
        locateFile: (fileName, scriptDirectory) => {
          return '/js/lib/' + fileName;
        },
        // 禁用动态库预加载（vips-heif.wasm 和 vips-jxl.wasm）
        // 在启用了 Pthreads (SharedArrayBuffer) 的 Web Worker 环境中，
        // 预加载这些大 WASM 动态库会导致 Emscripten 初始化时产生死锁。
        // 此改动能彻底解决“raw-to-jpg 卡住不执行”的问题。
        dynamicLibraries: []
      });
      // 30 秒时输出中间状态方便调试
      var intermediateCheck = setTimeout(function () {
        console.warn('[VipsLoader] Vips() still initializing after 30s, waiting up to 120s total');
      }, 30000);
      var timeoutPromise = new Promise(function (_, reject) {
        setTimeout(function () { clearTimeout(intermediateCheck); reject(new Error('VIPS_INIT_TIMEOUT')); }, 120000);
      });
      var vips = await Promise.race([initPromise, timeoutPromise]);
      this.instance = vips;
      this.status = 'ready';
      console.log('[VipsLoader] wasm-vips loaded, version:', vips.version());
      return vips;
    } catch (err) {
      this.status = 'error';
      this.error = err.message;
      console.error('[VipsLoader] Failed to load wasm-vips:', err);
      return null;
    }
  },

  // 检查 wasm-vips 是否可用
  isAvailable: function () {
    return this.status === 'ready';
  },

  // 获取实例
  getInstance: function () {
    return this.instance;
  }
};
