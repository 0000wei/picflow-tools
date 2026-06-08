/**
 * Facebook Cover Safe Zone Cropper - Upload Module
 * Shared across all language versions
 *
 * This is a stub implementation - only basic upload and image display.
 * Overlays, drag/zoom, and touch interactions are added in later modules.
 */

var FB_Cover = (function() {
  'use strict';

  // Constants
  const CANVAS_WIDTH = 1200;
  const CANVAS_HEIGHT = 628;
  const MIN_SCALE = 0.25;
  const MAX_SCALE = 5.0;
  const DESKTOP_TOP = 155;
  const DESKTOP_HEIGHT = 312;
  const MOBILE_LEFT = 320;
  const MOBILE_WIDTH = 560;
  const SAFE_LEFT = 320;
  const SAFE_TOP = 155;
  const SAFE_WIDTH = 560;
  const SAFE_HEIGHT = 312;

  // State
  let state = {
    image: null,
    imgWidth: 0,
    imgHeight: 0,
    scale: 1,
    offsetX: 0,
    offsetY: 0,
    mode: 'safe',
    format: 'png',
    isDragging: false,
    dragStartX: 0,
    dragStartY: 0,
    dragOffsetX: 0,
    dragOffsetY: 0,
    lastTouchDist: 0
  };

  // DOM references
  let els = {};

  /**
   * Initialize the cropper
   */
  function init() {
    // Get DOM references
    els.uploadArea = document.getElementById('upload-area');
    els.fileInput = document.getElementById('file-input');
    els.canvasArea = document.getElementById('canvas-area');
    els.canvas = document.getElementById('main-canvas');
    els.zoomSlider = document.getElementById('zoom-slider');
    els.zoomValue = document.getElementById('zoom-value');
    els.downloadBtn = document.getElementById('download-btn');
    els.modeButtons = document.querySelectorAll('.preview-btn');
    els.formatRadios = document.querySelectorAll('input[name="format"]');

    // Set canvas size
    els.canvas.width = CANVAS_WIDTH;
    els.canvas.height = CANVAS_HEIGHT;

    // Set initial cursor
    els.canvas.style.cursor = 'grab';

    // Setup upload handlers
    setupUploadHandlers();

    // Setup drag and zoom handlers
    setupMouseDragHandlers();
    setupWheelZoomHandler();
    setupTouchHandlers();

    // Bind mode switching
    els.modeButtons.forEach(function(btn) {
      btn.addEventListener('click', function() {
        // Remove active from all buttons
        els.modeButtons.forEach(function(b) {
          b.classList.remove('active');
        });
        // Add active to clicked button
        this.classList.add('active');
        // Update state
        state.mode = this.getAttribute('data-mode');
        // Re-render
        render();
      });
    });

    // Bind format radio buttons
    els.formatRadios.forEach(function(radio) {
      radio.addEventListener('change', function() {
        state.format = this.value;
        render();
      });
    });

    // Bind download button
    els.downloadBtn.addEventListener('click', function() {
      els.downloadBtn.textContent = 'Generating...';
      els.downloadBtn.disabled = true;
      exportImage();
    });

    // Bind zoom slider
    els.zoomSlider.addEventListener('input', function() {
      const newScale = parseFloat(this.value) / 100;
      // Clamp
      const clampedScale = Math.min(Math.max(newScale, MIN_SCALE), MAX_SCALE);

      // Zoom centered at canvas center (600, 314)
      const centerX = CANVAS_WIDTH / 2;
      const centerY = CANVAS_HEIGHT / 2;

      // Calculate what point on the image is at the canvas center
      const imgCenterX = (centerX - state.offsetX) / state.scale;
      const imgCenterY = (centerY - state.offsetY) / state.scale;

      state.scale = clampedScale;

      // Recalculate offset so the same image point stays at center
      state.offsetX = centerX - imgCenterX * state.scale;
      state.offsetY = centerY - imgCenterY * state.scale;

      // Apply boundary constraints
      applyBoundaryConstraints();

      // Update zoom value display
      els.zoomValue.textContent = Math.round(state.scale * 100) + '%';

      render();
    });
  }

  /**
   * Setup upload event handlers
   */
  function setupUploadHandlers() {
    // Drag and drop handlers
    els.uploadArea.addEventListener('dragover', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.classList.add('highlight');
    });

    els.uploadArea.addEventListener('dragleave', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.classList.remove('highlight');
    });

    els.uploadArea.addEventListener('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.classList.remove('highlight');
      if (e.dataTransfer.files.length > 0) {
        loadImage(e.dataTransfer.files[0]);
      }
    });

    // File input change
    els.fileInput.addEventListener('change', function() {
      if (this.files.length > 0) {
        loadImage(this.files[0]);
      }
    });

    // Paste handler
    document.addEventListener('paste', function(e) {
      if (e.clipboardData && e.clipboardData.files.length > 0) {
        loadImage(e.clipboardData.files[0]);
      }
    });

    // Click to upload
    els.uploadArea.addEventListener('click', function() {
      els.fileInput.click();
    });
  }

  /**
   * Setup mouse drag handlers on the canvas
   */
  function setupMouseDragHandlers() {
    const canvas = els.canvas;

    canvas.addEventListener('mousedown', function(e) {
      e.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;

      state.isDragging = true;
      state.dragStartX = (e.clientX - rect.left) * scaleX;
      state.dragStartY = (e.clientY - rect.top) * scaleY;
      state.dragOffsetX = state.offsetX;
      state.dragOffsetY = state.offsetY;

      canvas.style.cursor = 'grabbing';
    });

    document.addEventListener('mousemove', function(e) {
      if (!state.isDragging) return;
      e.preventDefault();

      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;

      const mouseX = (e.clientX - rect.left) * scaleX;
      const mouseY = (e.clientY - rect.top) * scaleY;

      state.offsetX = state.dragOffsetX + (mouseX - state.dragStartX);
      state.offsetY = state.dragOffsetY + (mouseY - state.dragStartY);

      applyBoundaryConstraints();
      render();
    });

    document.addEventListener('mouseup', function(e) {
      if (!state.isDragging) return;
      state.isDragging = false;
      canvas.style.cursor = 'grab';
    });
  }

  /**
   * Setup mouse wheel zoom handler on the canvas
   */
  function setupWheelZoomHandler() {
    const canvas = els.canvas;

    canvas.addEventListener('wheel', function(e) {
      e.preventDefault();

      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;

      const mouseX = (e.clientX - rect.left) * scaleX;
      const mouseY = (e.clientY - rect.top) * scaleY;

      // Determine zoom direction and factor
      const delta = e.deltaY > 0 ? -0.05 : 0.05;
      const newScale = Math.min(Math.max(state.scale * (1 + delta), MIN_SCALE), MAX_SCALE);

      // Calculate what point on the image is at the mouse position
      const imgX = (mouseX - state.offsetX) / state.scale;
      const imgY = (mouseY - state.offsetY) / state.scale;

      state.scale = newScale;

      // Recalculate offset so the same image point stays under the mouse
      state.offsetX = mouseX - imgX * state.scale;
      state.offsetY = mouseY - imgY * state.scale;

      applyBoundaryConstraints();

      // Sync slider
      els.zoomSlider.value = Math.round(state.scale * 100);
      els.zoomValue.textContent = Math.round(state.scale * 100) + '%';

      render();
    }, { passive: false });
  }

  /**
   * Apply boundary constraints so the image never completely leaves the canvas
   */
  function applyBoundaryConstraints() {
    if (!state.image) return;

    const imageW = state.imgWidth * state.scale;
    const imageH = state.imgHeight * state.scale;

    // Horizontal: keep at least 1px of image visible
    if (imageW > CANVAS_WIDTH) {
      // Image is wider than canvas — constrain panning
      if (state.offsetX > 0) state.offsetX = 0;
      if (state.offsetX < CANVAS_WIDTH - imageW) state.offsetX = CANVAS_WIDTH - imageW;
    } else {
      // Image fits inside canvas — keep it centered
      state.offsetX = (CANVAS_WIDTH - imageW) / 2;
    }

    // Vertical: same logic
    if (imageH > CANVAS_HEIGHT) {
      if (state.offsetY > 0) state.offsetY = 0;
      if (state.offsetY < CANVAS_HEIGHT - imageH) state.offsetY = CANVAS_HEIGHT - imageH;
    } else {
      state.offsetY = (CANVAS_HEIGHT - imageH) / 2;
    }
  }

function setupTouchHandlers() {
  var canvas = els.canvas;

  canvas.addEventListener('touchstart', function(e) {
    e.preventDefault();
    var rect = canvas.getBoundingClientRect();
    var scaleX = canvas.width / rect.width;
    var scaleY = canvas.height / rect.height;

    if (e.touches.length === 1) {
      // Single finger drag - same as mousedown
      state.isDragging = true;
      state.dragStartX = (e.touches[0].clientX - rect.left) * scaleX;
      state.dragStartY = (e.touches[0].clientY - rect.top) * scaleY;
      state.dragOffsetX = state.offsetX;
      state.dragOffsetY = state.offsetY;
    } else if (e.touches.length === 2) {
      // Two finger pinch - measure initial distance
      var dx = e.touches[0].clientX - e.touches[1].clientX;
      var dy = e.touches[0].clientY - e.touches[1].clientY;
      state.lastTouchDist = Math.hypot(dx, dy);
    }
  }, { passive: false });

  canvas.addEventListener('touchmove', function(e) {
    e.preventDefault();
    var rect = canvas.getBoundingClientRect();
    var scaleX = canvas.width / rect.width;
    var scaleY = canvas.height / rect.height;

    if (e.touches.length === 1 && state.isDragging) {
      // Single finger drag
      var touchX = (e.touches[0].clientX - rect.left) * scaleX;
      var touchY = (e.touches[0].clientY - rect.top) * scaleY;
      state.offsetX = state.dragOffsetX + (touchX - state.dragStartX);
      state.offsetY = state.dragOffsetY + (touchY - state.dragStartY);
      applyBoundaryConstraints();
      render();
    } else if (e.touches.length === 2) {
      // Two finger pinch zoom
      var dx = e.touches[0].clientX - e.touches[1].clientX;
      var dy = e.touches[0].clientY - e.touches[1].clientY;
      var dist = Math.hypot(dx, dy);
      if (state.lastTouchDist > 0) {
        var scaleFactor = dist / state.lastTouchDist;
        var newScale = Math.min(Math.max(state.scale * scaleFactor, MIN_SCALE), MAX_SCALE);

        // Calculate pinch center on canvas
        var cx = ((e.touches[0].clientX + e.touches[1].clientX) / 2 - rect.left) * scaleX;
        var cy = ((e.touches[0].clientY + e.touches[1].clientY) / 2 - rect.top) * scaleY;

        // Anchor: what point on the image is at the pinch center
        var imgX = (cx - state.offsetX) / state.scale;
        var imgY = (cy - state.offsetY) / state.scale;

        state.scale = newScale;

        // Recalculate offset so the same image point stays under the pinch center
        state.offsetX = cx - imgX * state.scale;
        state.offsetY = cy - imgY * state.scale;

        applyBoundaryConstraints();

        // Sync slider and display
        els.zoomSlider.value = Math.round(state.scale * 100);
        els.zoomValue.textContent = Math.round(state.scale * 100) + '%';
      }
      state.lastTouchDist = dist;
      render();
    }
  }, { passive: false });

  canvas.addEventListener('touchend', function(e) {
    e.preventDefault();
    state.isDragging = false;
    state.lastTouchDist = 0;
  }, { passive: false });
}
  /**
   * Draw 3x3 grid lines (only for safe mode)
   */
  function drawGrid(ctx) {
    const gridColor = 'rgba(255,255,255,0.3)';
    ctx.save();
    ctx.strokeStyle = gridColor;
    ctx.lineWidth = 1;

    // Two horizontal lines: y = CANVAS_HEIGHT/3 * 1, CANVAS_HEIGHT/3 * 2
    const hStep = CANVAS_HEIGHT / 3;
    ctx.beginPath();
    ctx.moveTo(0, hStep);
    ctx.lineTo(CANVAS_WIDTH, hStep);
    ctx.moveTo(0, hStep * 2);
    ctx.lineTo(CANVAS_WIDTH, hStep * 2);

    // Two vertical lines: x = CANVAS_WIDTH/3 * 1, CANVAS_WIDTH/3 * 2
    const vStep = CANVAS_WIDTH / 3;
    ctx.moveTo(vStep, 0);
    ctx.lineTo(vStep, CANVAS_HEIGHT);
    ctx.moveTo(vStep * 2, 0);
    ctx.lineTo(vStep * 2, CANVAS_HEIGHT);

    ctx.stroke();
    ctx.restore();
  }

  /**
   * Draw safe zone overlay - four semi-transparent rectangles covering non-safe areas
   */
  function drawSafeOverlay(ctx) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,0.55)';

    // Top: (0,0) to (1200, 155)
    ctx.fillRect(0, 0, CANVAS_WIDTH, SAFE_TOP);
    // Bottom: (0, 467) to (1200, 628)
    ctx.fillRect(0, SAFE_TOP + SAFE_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT - SAFE_TOP - SAFE_HEIGHT);
    // Left: (0, 155) to (320, 467)
    ctx.fillRect(0, SAFE_TOP, SAFE_LEFT, SAFE_HEIGHT);
    // Right: (880, 155) to (1200, 467)
    ctx.fillRect(SAFE_LEFT + SAFE_WIDTH, SAFE_TOP, CANVAS_WIDTH - SAFE_LEFT - SAFE_WIDTH, SAFE_HEIGHT);

    // Safe zone border
    ctx.strokeStyle = '#6366F1';
    ctx.lineWidth = 2;
    ctx.strokeRect(SAFE_LEFT, SAFE_TOP, SAFE_WIDTH, SAFE_HEIGHT);

    ctx.restore();
  }

  /**
   * Draw immersive Facebook desktop UI
   */
  function drawFBDesktopUI(ctx) {
    ctx.save();

    // Background: dark mask top and bottom
    ctx.fillStyle = '#0F0F11';
    ctx.fillRect(0, 0, CANVAS_WIDTH, DESKTOP_TOP);
    ctx.fillRect(0, DESKTOP_TOP + DESKTOP_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT - DESKTOP_TOP - DESKTOP_HEIGHT);

    // Top bar (0,0) to (1200,40)
    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.fillRect(0, 0, CANVAS_WIDTH, 40);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 15px sans-serif';
    ctx.fillText('←  Alex Johnson', 15, 26);
    ctx.fillStyle = '#1877F2';
    ctx.font = '13px sans-serif';
    ctx.fillText('📷  Edit Cover Photo', 1000, 26);

    // Bottom gradient bar
    const grad = ctx.createLinearGradient(0, CANVAS_HEIGHT - 80, 0, CANVAS_HEIGHT);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(1, 'rgba(0,0,0,0.7)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, CANVAS_HEIGHT - 80, CANVAS_WIDTH, 80);

    // Profile picture circle (80px diameter)
    const avX = 30;
    const avY = CANVAS_HEIGHT - 90 + 30;
    const avR = 40;
    ctx.beginPath();
    ctx.arc(avX + avR, avY + avR, avR, 0, Math.PI * 2);
    const avGrad = ctx.createRadialGradient(avX + avR - 8, avY + avR - 8, 5, avX + avR, avY + avR, avR);
    avGrad.addColorStop(0, '#667eea');
    avGrad.addColorStop(1, '#764ba2');
    ctx.fillStyle = avGrad;
    ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.font = '36px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('👤', avX + avR, avY + avR + 12);
    ctx.textAlign = 'left';

    // Name
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 16px sans-serif';
    ctx.fillText('Alex Johnson', 120, 575);

    // Action buttons
    ctx.font = '13px sans-serif';
    ctx.fillText('👍  Like', 180, 590);
    ctx.fillText('💬  Comment', 330, 590);
    ctx.fillText('🔗  Share', 520, 590);

    // Tab bar
    ctx.fillStyle = '#18191A';
    ctx.fillRect(0, 588, CANVAS_WIDTH, 22);
    ctx.fillStyle = '#B0B3B8';
    ctx.font = '13px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Posts · About · Photos · More', 600, 604);
    ctx.textAlign = 'left';

    ctx.restore();
  }

  /**
   * Draw immersive Facebook mobile UI
   */
  function drawFBMobileUI(ctx) {
    ctx.save();

    // Left and right dark masking
    ctx.fillStyle = '#0F0F11';
    ctx.fillRect(0, 0, MOBILE_LEFT, CANVAS_HEIGHT);
    ctx.fillRect(MOBILE_LEFT + MOBILE_WIDTH, 0, CANVAS_WIDTH - MOBILE_LEFT - MOBILE_WIDTH, CANVAS_HEIGHT);

    // Status bar (320,0) to (879,44)
    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.fillRect(MOBILE_LEFT, 0, MOBILE_WIDTH, 44);
    ctx.fillStyle = '#ffffff';
    ctx.font = '14px sans-serif';
    ctx.fillText('11:30', 340, 28);

    // Signal bars
    ctx.fillRect(810, 16, 4, 8);
    ctx.fillRect(816, 12, 4, 12);
    ctx.fillRect(822, 8, 4, 16);

    // Battery icon
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1;
    ctx.strokeRect(840, 14, 18, 10);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(842, 16, 10, 6);

    // Navigation bar (320,44) to (879,88)
    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.fillRect(MOBILE_LEFT, 44, MOBILE_WIDTH, 44);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 16px sans-serif';
    ctx.fillText('facebook', 340, 72);
    ctx.font = '16px sans-serif';
    ctx.fillText('🔍', 830, 72);
    ctx.fillText('🔔', 855, 72);

    // Profile picture
    const avX = MOBILE_LEFT + (MOBILE_WIDTH - 80) / 2;
    const avY = CANVAS_HEIGHT - 90 + 30;
    const avR = 40;
    ctx.beginPath();
    ctx.arc(avX + avR, avY + avR, avR, 0, Math.PI * 2);
    const avGrad = ctx.createRadialGradient(avX + avR - 8, avY + avR - 8, 5, avX + avR, avY + avR, avR);
    avGrad.addColorStop(0, '#667eea');
    avGrad.addColorStop(1, '#764ba2');
    ctx.fillStyle = avGrad;
    ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.font = '36px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('👤', avX + avR, avY + avR + 12);

    // Bottom action bar
    const grad2 = ctx.createLinearGradient(MOBILE_LEFT, CANVAS_HEIGHT - 65, MOBILE_LEFT, CANVAS_HEIGHT);
    grad2.addColorStop(0, 'rgba(0,0,0,0)');
    grad2.addColorStop(1, 'rgba(0,0,0,0.7)');
    ctx.fillStyle = grad2;
    ctx.fillRect(MOBILE_LEFT, CANVAS_HEIGHT - 65, MOBILE_WIDTH, 65);

    ctx.font = '18px sans-serif';
    ctx.fillText('👍', 380, 600);
    ctx.fillText('💬', 500, 600);
    ctx.fillText('↗️', 610, 600);

    ctx.textAlign = 'left';
    ctx.restore();
  }

  /**
   * Load an image file
   * @param {File} file - The image file to load
   */
  function loadImage(file) {
    if (!file) return;

    // Validate file type
    if (!file.type.match(/(jpeg|png|webp)/)) {
      alert('Please select a valid image file (JPG, PNG, or WebP).');
      return;
    }

    // Warn about large files
    if (file.size > 20 * 1024 * 1024) {
      alert('File is larger than 20MB. Processing may be slow.');
    }

    // Load image
    const img = new Image();
    img.src = URL.createObjectURL(file);

    img.onload = function() {
      // Update state
      state.image = img;
      state.imgWidth = img.width;
      state.imgHeight = img.height;

      // Calculate scale to cover canvas
      state.scale = Math.max(CANVAS_WIDTH / img.width, CANVAS_HEIGHT / img.height);

      // Center image
      state.offsetX = (CANVAS_WIDTH - img.width * state.scale) / 2;
      state.offsetY = (CANVAS_HEIGHT - img.height * state.scale) / 2;

      // Update UI
      els.uploadArea.style.display = 'none';
      els.canvasArea.style.display = 'block';

      els.zoomSlider.value = Math.round(state.scale * 100);
      els.zoomValue.textContent = Math.round(state.scale * 100) + '%';

      // Render
      render();
    };

    img.onerror = function() {
      alert('Failed to load image. Please try another file.');
    };
  }

  /**
   * Render the image on canvas with overlays
   */
  function render() {
    if (!state.image) return;

    const canvas = els.canvas;
    const ctx = canvas.getContext('2d');

    // Clear canvas
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // Draw image
    ctx.drawImage(
      state.image,
      state.offsetX,
      state.offsetY,
      state.imgWidth * state.scale,
      state.imgHeight * state.scale
    );

    // Draw overlays based on mode
    if (state.mode === 'safe') {
      drawGrid(ctx);
      drawSafeOverlay(ctx);
    } else if (state.mode === 'desktop') {
      drawFBDesktopUI(ctx);
    } else if (state.mode === 'mobile') {
      drawFBMobileUI(ctx);
    }
  }

  /**
   * Export the current canvas as an image file (STUB - no overlays)
   * This will export just the raw image at current zoom/position
   */
  function exportImage() {
    try {
      if (!state.image) return;

      // Create offscreen canvas for export
      const exportCanvas = document.createElement('canvas');
      exportCanvas.width = CANVAS_WIDTH;
      exportCanvas.height = CANVAS_HEIGHT;
      const ctx = exportCanvas.getContext('2d');

      // Draw image at current offset and scale
      ctx.drawImage(
        state.image,
        state.offsetX,
        state.offsetY,
        state.imgWidth * state.scale,
        state.imgHeight * state.scale
      );

      // Note: No overlays are drawn - this exports only the raw image

      // Determine MIME type
      const mimeType = state.format === 'png' ? 'image/png' : 'image/jpeg';
      const extension = state.format === 'png' ? 'png' : 'jpg';

      // JPEG quality parameter
      const quality = state.format === 'jpg' ? 0.92 : undefined;

      // Export to blob and download
      exportCanvas.toBlob(function(blob) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'facebook-cover.' + extension;
        link.click();
        URL.revokeObjectURL(url);

        // Log file size
        console.log('Exported facebook cover: ' + Math.round(blob.size / 1024) + ' KB');

        // Restore download button
        var btn = document.getElementById('download-btn');
        if (btn) {
          btn.textContent = 'Download Facebook Cover Photo';
          btn.disabled = false;
        }
      }, mimeType, quality);
    } catch (err) {
      alert('Export failed: ' + err.message);

      // Restore download button on failure
      var btn = document.getElementById('download-btn');
      if (btn) {
        btn.textContent = 'Download Facebook Cover Photo';
        btn.disabled = false;
      }
    }
  }

  /**
   * Reset the cropper to initial state
   */
  function reset() {
    // Reset state
    state = {
      image: null,
      imgWidth: 0,
      imgHeight: 0,
      scale: 1,
      offsetX: 0,
      offsetY: 0,
      mode: 'safe',
      format: 'png',
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      dragOffsetX: 0,
      dragOffsetY: 0,
      lastTouchDist: 0
    };

    // Reset UI
    els.uploadArea.style.display = 'block';
    els.canvasArea.style.display = 'none';

    els.zoomSlider.value = 100;
    els.zoomValue.textContent = '100%';

    // Clear canvas
    const canvas = els.canvas;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // Reset file input
    els.fileInput.value = '';

    // Reset mode buttons
    els.modeButtons.forEach(function(btn) {
      btn.classList.remove('active');
      if (btn.getAttribute('data-mode') === 'safe') {
        btn.classList.add('active');
      }
    });

    // Reset format radios
    els.formatRadios.forEach(function(radio) {
      if (radio.value === 'png') {
        radio.checked = true;
      }
    });
  }

  // Exposed API
  return {
    init: init,
    loadImage: loadImage,
    exportImage: exportImage,
    reset: reset
  };

})();

// Auto-initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('main-canvas')) {
    FB_Cover.init();
  }
});
