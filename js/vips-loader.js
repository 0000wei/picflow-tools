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

      // 加载 wasm-vips（通过 Vips 全局变量，由 vips.js 设置）
      // vips.js 是 Emscripten 编译产物，加载后暴露全局 Vips 函数
      var Vips = window.Vips;
      if (!Vips) {
        // 如果 vips.js 通过 <script> 加载会自动设置 window.Vips
        throw new Error('vips.js not loaded — ensure <script src="/js/lib/vips.js"> is included');
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
