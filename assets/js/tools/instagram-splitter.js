/**
 * Instagram Image Splitter
 * Canvas-based image splitter for Instagram carousel and grid posts.
 * Pure frontend, no external dependencies.
 *
 * (c) PicEte — https://picete.com
 */
const IGSplitter = (function () {
  'use strict';

  /* ======================================================
   *  State
   * ====================================================== */
  const state = {
    image: null,
    canvas: null,
    ctx: null,
    mode: 'carousel',
    slices: 4,
    ratio: '4:5',
    gridLayout: '3x3',
    cropper: { x: 0, y: 0, w: 0, h: 0 },
    originalWidth: 0,
    originalHeight: 0,
    displayWidth: 0,
    displayHeight: 0,
    isDownsampled: false,
    cropScaleX: 1,
    cropScaleY: 1
  };

  let _oldObjectURL = null;

  /* ======================================================
   *  Helpers
   * ====================================================== */

  /**
   * Parse grid layout string, e.g. '3x3' → { cols, rows }
   */
  function parseGridLayout (layout) {
    const parts = layout.split('x');
    return { cols: parseInt(parts[0], 10), rows: parseInt(parts[1], 10) };
  }

  /**
   * Get aspect-ratio as a number (width / height).
   */
  function getRatioValue (ratioStr) {
    const parts = ratioStr.split(':');
    return parseInt(parts[0], 10) / parseInt(parts[1], 10);
  }

  /**
   * Recalculate the crop box so it is centred on the image.
   * The crop box's aspect ratio is determined by state.ratio,
   * and the shorter axis is used as the base dimension.
   */
  function recalculateCropBox () {
    if (!state.image) return;

    const ratioVal = getRatioValue(state.ratio);
    let cw, ch;

    if (state.displayWidth / state.displayHeight > ratioVal) {
      // Image is wider than target → height is the short edge
      ch = state.displayHeight;
      cw = ch * ratioVal;
    } else {
      // Image is taller than target → width is the short edge
      cw = state.displayWidth;
      ch = cw / ratioVal;
    }

    state.cropper.x = (state.displayWidth - cw) / 2;
    state.cropper.y = (state.displayHeight - ch) / 2;
    state.cropper.w = cw;
    state.cropper.h = ch;
  }

  /* ======================================================
   *  Render
   * ====================================================== */

  function render () {
    if (!state.image || !state.canvas || !state.ctx) return;

    const canvas = state.canvas;
    const ctx = state.ctx;
    const img = state.image;

    // --- Canvas sizing ---
    const workbench = document.getElementById('workbench');
    const wbRect = workbench.getBoundingClientRect();
    const padding = 32; // px padding inside workbench

    const availW = wbRect.width - padding;
    const availH = wbRect.height - padding;

    // Fit the image into the available space, preserving aspect ratio
    const imgAspect = state.displayWidth / state.displayHeight;
    let dispW, dispH;

    if (availW / availH > imgAspect) {
      dispH = availH;
      dispW = dispH * imgAspect;
    } else {
      dispW = availW;
      dispH = dispW / imgAspect;
    }

    dispW = Math.floor(dispW);
    dispH = Math.floor(dispH);

    // Update canvas dimensions
    canvas.width = dispW;
    canvas.height = dispH;

    // Recalculate crop-box in display coordinates if display size changed
    // We need to scale the existing cropper proportionally
    const oldDispW = state.displayWidth || dispW;
    const oldDispH = state.displayHeight || dispH;

    if (state.displayWidth > 0 && state.displayHeight > 0) {
      const sx = dispW / oldDispW;
      const sy = dispH / oldDispH;
      state.cropper.x *= sx;
      state.cropper.y *= sy;
      state.cropper.w *= sx;
      state.cropper.h *= sy;
    }

    state.displayWidth = dispW;
    state.displayHeight = dispH;

    // Recalculate crop box if this is the first render
    if (state.cropper.w === 0 || state.cropper.h === 0) {
      recalculateCropBox();
    } else {
      // Clamp cropper within image bounds
      state.cropper.x = Math.max(0, Math.min(state.cropper.x, state.displayWidth - state.cropper.w));
      state.cropper.y = Math.max(0, Math.min(state.cropper.y, state.displayHeight - state.cropper.h));
      state.cropper.w = Math.min(state.cropper.w, state.displayWidth);
      state.cropper.h = Math.min(state.cropper.h, state.displayHeight);
    }

    // --- Draw ---
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Draw the full image
    ctx.drawImage(img, 0, 0, state.originalWidth, state.originalHeight,
                  0, 0, dispW, dispH);

    // 2. Semi-transparent dark overlay *except* the crop region
    ctx.fillStyle = 'rgba(0,0,0,0.55)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 3. Clear the crop region so the original pixels show through
    ctx.save();
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = 'rgba(0,0,0,1)';
    ctx.fillRect(state.cropper.x, state.cropper.y, state.cropper.w, state.cropper.h);
    ctx.restore();

    // Now draw the crop region on top so it is fully visible
    ctx.drawImage(img,
      0, 0, state.originalWidth, state.originalHeight,
      0, 0, dispW, dispH);

    // 4. Redraw the overlay, then punch out the crop region
    // Simpler approach: re-draw the image, then overlay around the crop

    // Actually, a cleaner method: draw image, draw overlay, punch crop with
    // compositing, then draw image again clipped to crop region.
    // We've already done that above via destination-out.
    // Now draw the crop area's image content bright again:
    ctx.save();
    ctx.beginPath();
    ctx.rect(state.cropper.x, state.cropper.y, state.cropper.w, state.cropper.h);
    ctx.clip();
    ctx.drawImage(img, 0, 0, state.originalWidth, state.originalHeight,
                  0, 0, dispW, dispH);
    ctx.restore();

    // 5. Draw split lines + numbers

    const c = state.cropper;

    if (state.mode === 'carousel') {
      drawCarouselLines(ctx, c);
    } else {
      drawGridLines(ctx, c);
    }

    // 6. Draw crop border
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.strokeRect(c.x, c.y, c.w, c.h);
  }

  /**
   * Draw vertical split lines for carousel mode.
   */
  function drawCarouselLines (ctx, c) {
    const n = state.slices;
    if (n < 2) return;

    const sliceH = c.h / n;

    ctx.strokeStyle = 'rgba(255,255,255,0.85)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);

    for (let i = 1; i < n; i++) {
      const y = c.y + sliceH * i;
      ctx.beginPath();
      ctx.moveTo(c.x, y);
      ctx.lineTo(c.x + c.w, y);
      ctx.stroke();
    }

    ctx.setLineDash([]);

    // Numbers (top-left of each slice)
    ctx.fillStyle = 'rgba(255,255,255,0.9)';
    ctx.font = 'bold 14px system-ui, sans-serif';
    ctx.textBaseline = 'top';
    ctx.textAlign = 'left';

    for (let i = 0; i < n; i++) {
      const y = c.y + sliceH * i + 6;
      ctx.fillText(String(i + 1), c.x + 6, y);
    }
  }

  /**
   * Draw grid split lines for grid mode.
   */
  function drawGridLines (ctx, c) {
    const layout = parseGridLayout(state.gridLayout);
    const cols = layout.cols;
    const rows = layout.rows;

    const cellW = c.w / cols;
    const cellH = c.h / rows;

    ctx.strokeStyle = 'rgba(255,255,255,0.85)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);

    // Vertical lines
    for (let i = 1; i < cols; i++) {
      const x = c.x + cellW * i;
      ctx.beginPath();
      ctx.moveTo(x, c.y);
      ctx.lineTo(x, c.y + c.h);
      ctx.stroke();
    }

    // Horizontal lines
    for (let i = 1; i < rows; i++) {
      const y = c.y + cellH * i;
      ctx.beginPath();
      ctx.moveTo(c.x, y);
      ctx.lineTo(c.x + c.w, y);
      ctx.stroke();
    }

    ctx.setLineDash([]);

    // Numbers
    ctx.fillStyle = 'rgba(255,255,255,0.9)';
    ctx.font = 'bold 14px system-ui, sans-serif';
    ctx.textBaseline = 'top';
    ctx.textAlign = 'left';

    let idx = 1;
    for (let r = 0; r < rows; r++) {
      for (let col = 0; col < cols; col++) {
        const x = c.x + cellW * col + 6;
        const y = c.y + cellH * r + 6;
        ctx.fillText(String(idx), x, y);
        idx++;
      }
    }
  }

  /* ======================================================
   *  Mouse / Drag handling for crop box
   * ====================================================== */

  let _isDragging = false;
  let _dragOffsetX = 0;
  let _dragOffsetY = 0;

  function setupCanvasMouseEvents () {
    const canvas = state.canvas;
    if (!canvas) return;

    canvas.addEventListener('mousedown', onMouseDown);
    canvas.addEventListener('mousemove', onMouseMove);
    canvas.addEventListener('mouseup', onMouseUp);
    canvas.addEventListener('mouseleave', onMouseUp);

    // Touch support
    canvas.addEventListener('touchstart', onTouchStart, { passive: false });
    canvas.addEventListener('touchmove', onTouchMove, { passive: false });
    canvas.addEventListener('touchend', onTouchEnd, { passive: false });
  }

  function getCanvasCoords (clientX, clientY) {
    const rect = state.canvas.getBoundingClientRect();
    const scaleX = state.canvas.width / rect.width;
    const scaleY = state.canvas.height / rect.height;
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY
    };
  }

  function onMouseDown (e) {
    const pt = getCanvasCoords(e.clientX, e.clientY);
    startDrag(pt.x, pt.y);
  }

  function onMouseMove (e) {
    const pt = getCanvasCoords(e.clientX, e.clientY);
    if (_isDragging) {
      doDrag(pt.x, pt.y);
    } else {
      updateCursor(pt.x, pt.y);
    }
  }

  function onMouseUp () {
    _isDragging = false;
    state.canvas.style.cursor = 'default';
  }

  function onTouchStart (e) {
    e.preventDefault();
    const touch = e.touches[0];
    const pt = getCanvasCoords(touch.clientX, touch.clientY);
    startDrag(pt.x, pt.y);
  }

  function onTouchMove (e) {
    e.preventDefault();
    if (!_isDragging) return;
    const touch = e.touches[0];
    const pt = getCanvasCoords(touch.clientX, touch.clientY);
    doDrag(pt.x, pt.y);
  }

  function onTouchEnd () {
    _isDragging = false;
  }

  function startDrag (px, py) {
    const c = state.cropper;
    if (px >= c.x && px <= c.x + c.w && py >= c.y && py <= c.y + c.h) {
      _isDragging = true;
      _dragOffsetX = px - c.x;
      _dragOffsetY = py - c.y;
      state.canvas.style.cursor = 'grabbing';
    }
  }

  function doDrag (px, py) {
    const c = state.cropper;
    let nx = px - _dragOffsetX;
    let ny = py - _dragOffsetY;

    // Clamp
    nx = Math.max(0, Math.min(nx, state.displayWidth - c.w));
    ny = Math.max(0, Math.min(ny, state.displayHeight - c.h));

    c.x = nx;
    c.y = ny;

    render();
  }

  function updateCursor (px, py) {
    const c = state.cropper;
    if (px >= c.x && px <= c.x + c.w && py >= c.y && py <= c.y + c.h) {
      state.canvas.style.cursor = 'grab';
    } else {
      state.canvas.style.cursor = 'default';
    }
  }

  /* ======================================================
   *  Public API
   * ====================================================== */

  /**
   * init(canvasId)
   * Initialise the canvas, bind file input and drag-and-drop events.
   */
  function init (canvasId) {
    state.canvas = document.getElementById(canvasId);
    if (!state.canvas) {
      console.error('IGSplitter: Canvas element not found:', canvasId);
      return;
    }
    state.ctx = state.canvas.getContext('2d');

    // Hide canvas initially — shown after image is loaded
    state.canvas.style.display = 'none';

    // File input
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
      fileInput.addEventListener('change', function (e) {
        if (e.target.files && e.target.files[0]) {
          loadImage(e.target.files[0]);
        }
      });
    }

    // Upload area drag-and-drop
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) {
      uploadArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
      });
      uploadArea.addEventListener('dragleave', function () {
        uploadArea.classList.remove('dragover');
      });
      uploadArea.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
          loadImage(e.dataTransfer.files[0]);
        }
      });
    }

    // Click on upload area triggers file input
    if (uploadArea && fileInput) {
      uploadArea.addEventListener('click', function () {
        fileInput.click();
      });
    }

    // Setup mouse/touch drag events
    setupCanvasMouseEvents();

    // Handle window resize
    window.addEventListener('resize', function () {
      if (state.image) render();
    });
  }

  /**
   * loadImage(file)
   * Validate, optionally downsample, initialise crop box, and render.
   */
  function loadImage (file) {
    if (!file || !file.type.match('image/')) return;

    // Release previous object URL
    if (_oldObjectURL) {
      URL.revokeObjectURL(_oldObjectURL);
    }

    _oldObjectURL = URL.createObjectURL(file);

    const img = new Image();
    img.onload = function () {
      state.image = img;
      state.originalWidth = img.naturalWidth;
      state.originalHeight = img.naturalHeight;
      state.isDownsampled = false;
      state.cropScaleX = 1;
      state.cropScaleY = 1;

      let ow = img.naturalWidth;
      let oh = img.naturalHeight;

      // Downsample if longest edge > 4096
      const maxDim = Math.max(ow, oh);
      if (maxDim > 4096) {
        const scale = 4096 / maxDim;
        ow = Math.round(ow * scale);
        oh = Math.round(oh * scale);
        state.isDownsampled = true;
        state.cropScaleX = img.naturalWidth / ow;
        state.cropScaleY = img.naturalHeight / oh;
      }

      state.displayWidth = ow;
      state.displayHeight = oh;

      // Minimum dimension check
      if (Math.min(ow, oh) < 300) {
        alert('Image too small — minimum dimension is 300px.');
        return;
      }

      // Show / hide UI
      document.getElementById('workspaceEmpty').style.display = 'none';
      state.canvas.style.display = 'block';

      // Show downsample notice
      const notice = document.getElementById('downsampleNotice');
      if (notice) {
        notice.style.display = state.isDownsampled ? 'block' : 'none';
      }

      // Initial centred crop
      recalculateCropBox();

      // Render
      render();
    };

    img.src = _oldObjectURL;
  }

  /**
   * setMode(mode)
   * Switch between 'carousel' and 'grid'.
   */
  function setMode (mode) {
    if (mode !== 'carousel' && mode !== 'grid') return;
    state.mode = mode;

    // Toggle control panels
    const carouselCtrl = document.getElementById('carouselControls');
    const gridCtrl = document.getElementById('gridControls');

    if (carouselCtrl) {
      carouselCtrl.classList.toggle('active', mode === 'carousel');
    }
    if (gridCtrl) {
      gridCtrl.classList.toggle('active', mode === 'grid');
    }

    // Toggle mode buttons
    const modeBtns = document.querySelectorAll('.mode-btn');
    modeBtns.forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-mode') === mode);
    });

    // Recalculate crop box and render
    if (state.image) {
      recalculateCropBox();
      render();
    }
  }

  /**
   * setSlices(value)
   * Set number of carousel slices.
   */
  function setSlices (value) {
    state.slices = parseInt(value, 10) || 4;
    const display = document.getElementById('sliceCountDisplay');
    if (display) {
      display.textContent = state.slices;
    }
    if (state.image) render();
  }

  /**
   * setRatio(ratio)
   * Set aspect ratio for carousel mode ('4:5' or '1:1').
   */
  function setRatio (ratio) {
    if (ratio !== '4:5' && ratio !== '1:1') return;
    state.ratio = ratio;

    // Toggle ratio buttons
    const ratioBtns = document.querySelectorAll('.ratio-btn');
    ratioBtns.forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-ratio') === ratio);
    });

    if (state.image) {
      recalculateCropBox();
      render();
    }
  }

  /**
   * setGrid(value)
   * Set grid layout (e.g. '3x3', '3x1', '3x2', '3x4').
   */
  function setGrid (value) {
    state.gridLayout = value;
    if (state.image) {
      recalculateCropBox();
      render();
    }
  }

  /**
   * resetCrop()
   * Reset the crop box to its centred initial position.
   */
  function resetCrop () {
    if (!state.image) return;
    recalculateCropBox();
    render();
  }

  /**
   * exportZip()
   * Placeholder — log to console.
   */
  function exportZip () {
    console.log('exportZip() — not yet implemented');
  }

  /**
   * exportIndividual()
   * Placeholder — log to console.
   */
  function exportIndividual () {
    console.log('exportIndividual() — not yet implemented');
  }

  /* ======================================================
   *  Exports
   * ====================================================== */

  return {
    init: init,
    loadImage: loadImage,
    setMode: setMode,
    setSlices: setSlices,
    setRatio: setRatio,
    setGrid: setGrid,
    resetCrop: resetCrop,
    exportZip: exportZip,
    exportIndividual: exportIndividual
  };
})();
