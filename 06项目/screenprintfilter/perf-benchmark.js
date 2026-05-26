/**
 * ScreenPrintFilter Performance Benchmark
 * 
 * Runs inside a real Chromium browser via Puppeteer.
 * Tests the actual halftone algorithm by injecting a test harness.
 * Measures: full render time for various param/input size combos.
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const ITERATIONS = 5;
const SIZES = [
  { w: 400, h: 300, label: '400x300' },
  { w: 600, h: 450, label: '600x450' },
  { w: 800, h: 600, label: '800x600' },
];
const PARAM_SETS = [
  { label: 'Fine (4px, 1.0x)', dotSize: 4, spacing: 1.0, contrast: 50, brightness: 0, shape: 'circle', angle: 0 },
  { label: 'Medium (8px, 1.2x)', dotSize: 8, spacing: 1.2, contrast: 50, brightness: 0, shape: 'circle', angle: 0 },
  { label: 'Bold (12px, 1.2x)', dotSize: 12, spacing: 1.2, contrast: 50, brightness: 0, shape: 'circle', angle: 0 },
  { label: 'Max (30px, 2.0x)', dotSize: 30, spacing: 2.0, contrast: 50, brightness: 0, shape: 'circle', angle: 0 },
];

// Generate a test image (gradient + shapes) as data URL
function generateTestImage(w, h) {
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d');

  const gradient = ctx.createLinearGradient(0, 0, w, h);
  gradient.addColorStop(0, '#000');
  gradient.addColorStop(0.3, '#333');
  gradient.addColorStop(0.5, '#888');
  gradient.addColorStop(0.7, '#ccc');
  gradient.addColorStop(1, '#fff');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, w, h);

  ctx.fillStyle = '#555';
  ctx.fillRect(Math.floor(w * 0.2), Math.floor(h * 0.2), Math.floor(w * 0.3), Math.floor(h * 0.3));
  ctx.beginPath();
  ctx.arc(Math.floor(w * 0.7), Math.floor(h * 0.4), Math.floor(w * 0.15), 0, Math.PI * 2);
  ctx.fill();

  return canvas.toDataURL();
}

// OLD algorithm: on-the-fly getImageData per cell
function runOld(srcDataUrl, w, h, params) {
  const srcImg = new Image();
  srcImg.src = srcDataUrl;

  const srcCanvas = document.createElement('canvas');
  srcCanvas.width = w;
  srcCanvas.height = h;
  const srcCtx = srcCanvas.getContext('2d');
  srcCtx.drawImage(srcImg, 0, 0);

  const outCanvas = document.createElement('canvas');
  outCanvas.width = w;
  outCanvas.height = h;
  const outCtx = outCanvas.getContext('2d');

  // Halftone
  const dotSize = params.dotSize;
  const spacing = params.spacing;
  const gridSize = dotSize * spacing;

  outCtx.fillStyle = '#FFFFFF';
  outCtx.fillRect(0, 0, w, h);
  outCtx.fillStyle = '#000000';

  const cellArea = gridSize * gridSize;
  const maxDotArea = Math.PI * Math.pow(dotSize / 2, 2);

  for (let y = -gridSize; y < w + gridSize; y += gridSize) {
    for (let x = -gridSize; x < h + gridSize; x += gridSize) {
      const sampleX = (x / w) * w;
      const sampleY = (y / h) * h;

      if (sampleX < 0 || sampleX >= w || sampleY < 0 || sampleY >= h) continue;

      // On-the-fly getImageData (OLD way)
      const sx = Math.max(0, Math.min(Math.floor(sampleX - 1.5), w - 3));
      const sy = Math.max(0, Math.min(Math.floor(sampleY - 1.5), h - 3));
      const sw = Math.min(3, w - sx);
      const sh = Math.min(3, h - sy);
      const pixelData = srcCtx.getImageData(sx, sy, sw, sh).data;
      let sum = 0;
      let count = 0;
      for (let i = 0; i < pixelData.length; i += 4) { sum += pixelData[i]; count++; }
      const pixelBrightness = count > 0 ? sum / count : 128;

      const normalizedBrightness = pixelBrightness / 255;
      const targetCoverage = 1 - normalizedBrightness;
      const coverageRatio = Math.min(targetCoverage * cellArea / maxDotArea, 1);
      const dotRadius = Math.sqrt(coverageRatio) * (dotSize / 2);

      if (dotRadius > 0.5) {
        outCtx.beginPath();
        outCtx.arc(x + gridSize / 2, y + gridSize / 2, dotRadius, 0, Math.PI * 2);
        outCtx.fill();
      }
    }
  }
}

// NEW algorithm: pre-computed brightness array
function runNew(srcDataUrl, w, h, params) {
  const srcImg = new Image();
  srcImg.src = srcDataUrl;

  const srcCanvas = document.createElement('canvas');
  srcCanvas.width = w;
  srcCanvas.height = h;
  const srcCtx = srcCanvas.getContext('2d');
  srcCtx.drawImage(srcImg, 0, 0);

  const outCanvas = document.createElement('canvas');
  outCanvas.width = w;
  outCanvas.height = h;
  const outCtx = outCanvas.getContext('2d');

  // Pre-compute brightness array (once)
  const imageData = srcCtx.getImageData(0, 0, w, h);
  const data = imageData.data;
  const brightness = new Uint8Array(w * h);
  for (let i = 0; i < w * h; i++) {
    const idx = i * 4;
    brightness[i] = Math.round(0.299 * data[idx] + 0.587 * data[idx + 1] + 0.114 * data[idx + 2]);
  }

  const dotSize = params.dotSize;
  const spacing = params.spacing;
  const gridSize = dotSize * spacing;

  outCtx.fillStyle = '#FFFFFF';
  outCtx.fillRect(0, 0, w, h);
  outCtx.fillStyle = '#000000';

  const cellArea = gridSize * gridSize;
  const maxDotArea = Math.PI * Math.pow(dotSize / 2, 2);

  for (let y = -gridSize; y < w + gridSize; y += gridSize) {
    for (let x = -gridSize; x < h + gridSize; x += gridSize) {
      const sampleX = (x / w) * w;
      const sampleY = (y / h) * h;

      if (sampleX < 0 || sampleX >= w || sampleY < 0 || sampleY >= h) continue;

      // Fast lookup from pre-computed array (NEW way)
      const half = 1;
      const sx = Math.max(0, Math.min(Math.floor(sampleX - half), w - 3));
      const sy = Math.max(0, Math.min(Math.floor(sampleY - half), h - 3));
      const sw = Math.min(3, w - sx);
      const sh = Math.min(3, h - sy);
      let sum = 0;
      let count = 0;
      for (let row = 0; row < sh; row++) {
        const start = (sy + row) * w + sx;
        for (let col = 0; col < sw; col++) {
          sum += brightness[start + col];
          count++;
        }
      }
      const pixelBrightness = count > 0 ? sum / count : 128;

      const normalizedBrightness = pixelBrightness / 255;
      const targetCoverage = 1 - normalizedBrightness;
      const coverageRatio = Math.min(targetCoverage * cellArea / maxDotArea, 1);
      const dotRadius = Math.sqrt(coverageRatio) * (dotSize / 2);

      if (dotRadius > 0.5) {
        outCtx.beginPath();
        outCtx.arc(x + gridSize / 2, y + gridSize / 2, dotRadius, 0, Math.PI * 2);
        outCtx.fill();
      }
    }
  }
}

// Measure one run
function timeIt(fn, src, w, h, params) {
  const t0 = performance.now();
  fn(src, w, h, params);
  return performance.now() - t0;
}


// ============================================================
// Main benchmark runner
// ============================================================
async function runBenchmarks() {
  const results = [];

  for (const size of SIZES) {
    console.log(`\n=== Size: ${size.label} ===`);

    const src = generateTestImage(size.w, size.h);

    for (const params of PARAM_SETS) {
      const gridCount = Math.ceil((size.h + params.dotSize * params.spacing) / (params.dotSize * params.spacing)) *
        Math.ceil((size.w + params.dotSize * params.spacing) / (params.dotSize * params.spacing));

      // Warmup
      for (let i = 0; i < 2; i++) {
        runOld(src, size.w, size.h, params);
        runNew(src, size.w, size.h, params);
      }

      // Timed runs
      let oldTimes = [];
      let newTimes = [];
      for (let i = 0; i < ITERATIONS; i++) {
        oldTimes.push(timeIt(runOld, src, size.w, size.h, params));
        newTimes.push(timeIt(runNew, src, size.w, size.h, params));
      }

      const oldAvg = oldTimes.reduce((a, b) => a + b, 0) / oldTimes.length;
      const newAvg = newTimes.reduce((a, b) => a + b, 0) / newTimes.length;
      const speedup = oldAvg / newAvg;

      console.log(`  ${params.label} (${gridCount} grids): Old ${oldAvg.toFixed(0)}ms -> New ${newAvg.toFixed(0)}ms (${speedup.toFixed(1)}x)`);

      results.push({
        size: size.label,
        params: params.label,
        gridPoints: gridCount,
        oldAvgMs: Math.round(oldAvg),
        newAvgMs: Math.round(newAvg),
        speedup: speedup.toFixed(1),
      });
    }
  }

  // Summary HTML table
  console.log('\n\n=== PERFORMANCE SUMMARY TABLE ===');
  console.log('Size       | Params           | Grids  | Old(ms) | New(ms) | Speedup');
  console.log('----------|------------------|--------|---------|---------|--------');
  for (const r of results) {
    console.log(
      `${r.size.padEnd(10)} | ${r.params.padEnd(16)} | ${String(r.gridPoints).padStart(6)} | ` +
      `${String(r.oldAvgMs).padStart(7)} | ${String(r.newAvgMs).padStart(7)} | ${r.speedup}x`
    );
  }

  return results;
}

// Expose for page context
window.runBenchmarks = runBenchmarks;
