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
      // 优先从 window.Vips（由 es6 module 或 script 设置）
      // 如果没有，尝试通过动态 import() 加载 es6 版本
      var Vips = window.Vips;
      if (!Vips) {
        try {
          // Try dynamic import of vips-es6.js
          Vips = (await import('/js/lib/vips-es6.js')).default;
          console.log('[VipsLoader] vips-es6 loaded via dynamic import');
        } catch (importErr) {
          throw new Error('vips.js not loaded — ensure <script src="/js/lib/vips.js"> is included. Dynamic import also failed: ' + importErr.message);
        }
      }

      var vips = await Vips();
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
