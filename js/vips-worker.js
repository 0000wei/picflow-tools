// vips-worker.js — wasm-vips PNG compression Web Worker
// 专用于 PNG 压缩，支持任务取消和内存安全

// Worker 状态
let vips = null;
let currentTaskId = null;
let pendingImage = null;

// 加载 wasm-vips（Worker 内无法使用 VipsLoader——它依赖 DOM）
async function initVips() {
  try {
    // 检查 SharedArrayBuffer 是否可用
    if (typeof SharedArrayBuffer === 'undefined' || !self.crossOriginIsolated) {
      throw new Error('SharedArrayBuffer unavailable, Web Worker requires COOP/COEP headers');
    }

    // 使用 importScripts 加载 vips.js（Worker 环境）
    importScripts('/js/lib/vips.js');

    // 初始化 wasm-vips
    const Vips = self.Vips;
    if (!Vips) {
      throw new Error('Vips factory not found after loading vips.js');
    }

    vips = await Vips({
      mainScriptUrlOrBlob: '/js/lib/vips.js',
      locateFile: (fileName, scriptDirectory) => {
        return '/js/lib/' + fileName;
      },
      // 禁用动态库预加载（避免 Pthreads 死锁）
      dynamicLibraries: []
    });

    console.log('[vips-worker] wasm-vips loaded, version:', vips.version());
    self.postMessage({ type: 'ready' });
  } catch (err) {
    console.error('[vips-worker] Failed to initialize wasm-vips:', err);
    // 不发送 ready 消息，主线程会检测初始化失败
    throw err;
  }
}

// 取消当前任务并清理内存
function abortCurrentTask() {
  if (pendingImage) {
    pendingImage.delete();
    pendingImage = null;
  }
  currentTaskId = null;
}

// 执行压缩任务
async function executeCompress(id, fileBuffer, options) {
  let image;
  try {
    const uint8Array = new Uint8Array(fileBuffer);
    image = vips.Image.newFromBuffer(uint8Array);
    pendingImage = image;

    // 发送进度（解码完成）
    self.postMessage({ type: 'progress', id, stage: 'decode', progress: 33 });

    // 执行压缩
    const output = image.writeToBuffer('.png', options);

    // 发送进度（压缩完成）
    self.postMessage({ type: 'progress', id, stage: 'compress', progress: 100 });

    // 构造 Blob
    const blob = new Blob([output.buffer], { type: 'image/png' });

    self.postMessage({
      type: 'result',
      id,
      blob: blob,
      stats: {
        originalBytes: fileBuffer.byteLength,
        compressedBytes: blob.size
      }
    }, [blob]); // 使用 Transferable 对象优化性能
  } catch (err) {
    // 错误消息格式化（libvips 错误可能是数组）
    const errorMessage = (err.message && Array.isArray(err.message)
      ? err.message.join(' | ')
      : (err.message || String(err)));

    self.postMessage({
      type: 'error',
      id,
      message: errorMessage
    });
  } finally {
    // 确保 C++ 对象被释放
    if (image) {
      image.delete();
      image = null;
    }
    pendingImage = null;
    if (currentTaskId === id) {
      currentTaskId = null;
    }
  }
}

// 消息处理
self.onmessage = async (e) => {
  const { type, id, file, options } = e.data;

  if (type === 'compress') {
    // 如果 vips 未初始化，等待初始化
    if (!vips) {
      try {
        await initVips();
      } catch (initErr) {
        self.postMessage({
          type: 'error',
          id,
          message: 'Failed to initialize wasm-vips: ' + initErr.message
        });
        return;
      }
    }

    // 如果有正在执行的旧任务，清理内存
    if (currentTaskId && currentTaskId !== id) {
      abortCurrentTask();
    }
    currentTaskId = id;

    await executeCompress(id, file, options);
  }

  if (type === 'cancel') {
    if (!id || id === currentTaskId) {
      abortCurrentTask();
    }
  }
};

// 初始化 wasm-vips
initVips().catch((err) => {
  console.error('[vips-worker] Initialization failed:', err);
});
