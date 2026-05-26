/**
 * ScreenPrintFilter Performance Benchmark Runner
 * 
 * Uses Puppeteer (ESM) to run the benchmark in a real Chromium browser.
 * Measures: old (per-cell getImageData) vs new (pre-computed brightness array)
 *
 * Usage: node perf-benchmark-puppeteer.mjs
 */

import puppeteer from 'puppeteer';

const ITERATIONS = 5;
const SIZES = [
  { w: 400, h: 300, label: '400x300' },
  { w: 600, h: 450, label: '600x450' },
  { w: 800, h: 600, label: '800x600' },
];
const PARAM_SETS = [
  { label: 'Fine (4px,1.0x)', dotSize: 4, spacing: 1.0 },
  { label: 'Medium (8px,1.2x)', dotSize: 8, spacing: 1.2 },
  { label: 'Bold (12px,1.2x)', dotSize: 12, spacing: 1.2 },
  { label: 'Max (30px,2.0x)', dotSize: 30, spacing: 2.0 },
];

const BENCHMARK_CODE = `
const ITERATIONS = ${ITERATIONS};
const SIZES = ${JSON.stringify(SIZES)};
const PARAM_SETS = ${JSON.stringify(PARAM_SETS)};

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
  return canvas;
}

function getPixelBrightnessOld(srcCtx, x, y, w, h) {
  const sx = Math.max(0, Math.min(Math.floor(x - 1.5), w - 3));
  const sy = Math.max(0, Math.min(Math.floor(y - 1.5), h - 3));
  const sw = Math.min(3, w - sx);
  const sh = Math.min(3, h - sy);
  const pixelData = srcCtx.getImageData(sx, sy, sw, sh).data;
  let sum = 0, count = 0;
  for (let i = 0; i < pixelData.length; i += 4) { sum += pixelData[i]; count++; }
  return count > 0 ? sum / count : 128;
}

function runOld(srcCanvas, w, h, ds, sp) {
  const srcCtx = srcCanvas.getContext('2d');
  const outCanvas = document.createElement('canvas');
  outCanvas.width = w;
  outCanvas.height = h;
  const outCtx = outCanvas.getContext('2d');

  const gridSize = ds * sp;
  outCtx.fillStyle = '#FFFFFF';
  outCtx.fillRect(0, 0, w, h);
  outCtx.fillStyle = '#000000';

  const cellArea = gridSize * gridSize;
  const maxDotArea = Math.PI * Math.pow(ds / 2, 2);

  for (let y = -gridSize; y < h + gridSize; y += gridSize) {
    for (let x = -gridSize; x < w + gridSize; x += gridSize) {
      const sx = (x / w) * w, sy = (y / h) * h;
      if (sx < 0 || sx >= w || sy < 0 || sy >= h) continue;

      const pb = getPixelBrightnessOld(srcCtx, sx, sy, w, h);
      const nb = pb / 255;
      const cr = Math.min((1 - nb) * cellArea / maxDotArea, 1);
      const r = Math.sqrt(cr) * (ds / 2);

      if (r > 0.5) {
        outCtx.beginPath();
        outCtx.arc(x + gridSize/2, y + gridSize/2, r, 0, Math.PI * 2);
        outCtx.fill();
      }
    }
  }
}

function runNew(srcCanvas, w, h, ds, sp) {
  const srcCtx = srcCanvas.getContext('2d');
  const outCanvas = document.createElement('canvas');
  outCanvas.width = w;
  outCanvas.height = h;
  const outCtx = outCanvas.getContext('2d');

  // Pre-compute brightness array (one-time cost)
  const imageData = srcCtx.getImageData(0, 0, w, h);
  const data = imageData.data;
  const brightness = new Uint8Array(w * h);
  for (let i = 0; i < w * h; i++) {
    brightness[i] = Math.round(0.299 * data[i*4] + 0.587 * data[i*4+1] + 0.114 * data[i*4+2]);
  }

  const gridSize = ds * sp;
  outCtx.fillStyle = '#FFFFFF';
  outCtx.fillRect(0, 0, w, h);
  outCtx.fillStyle = '#000000';

  const cellArea = gridSize * gridSize;
  const maxDotArea = Math.PI * Math.pow(ds / 2, 2);

  for (let y = -gridSize; y < h + gridSize; y += gridSize) {
    for (let x = -gridSize; x < w + gridSize; x += gridSize) {
      const sx = (x / w) * w, sy = (y / h) * h;
      if (sx < 0 || sx >= w || sy < 0 || sy >= h) continue;

      // Lookup from pre-computed array instead of getImageData
      const half = 1;
      const px = Math.max(0, Math.min(Math.floor(sx - half), w - 3));
      const py = Math.max(0, Math.min(Math.floor(sy - half), h - 3));
      const pw = Math.min(3, w - px);
      const ph = Math.min(3, h - py);
      let sum = 0, count = 0;
      for (let row = 0; row < ph; row++) {
        const start = (py + row) * w + px;
        for (let col = 0; col < pw; col++) { sum += brightness[start + col]; count++; }
      }
      const pb = count > 0 ? sum / count : 128;

      const nb = pb / 255;
      const cr = Math.min((1 - nb) * cellArea / maxDotArea, 1);
      const r = Math.sqrt(cr) * (ds / 2);

      if (r > 0.5) {
        outCtx.beginPath();
        outCtx.arc(x + gridSize/2, y + gridSize/2, r, 0, Math.PI * 2);
        outCtx.fill();
      }
    }
  }
}

async function run() {
  const results = [];

  for (const size of SIZES) {
    const src = generateTestImage(size.w, size.h);

    for (const p of PARAM_SETS) {
      // Warmup
      for (let i = 0; i < 2; i++) {
        runOld(src, size.w, size.h, p.dotSize, p.spacing);
        runNew(src, size.w, size.h, p.dotSize, p.spacing);
      }

      let oldTimes = [], newTimes = [];
      for (let i = 0; i < ITERATIONS; i++) {
        const t0 = performance.now(); runOld(src, size.w, size.h, p.dotSize, p.spacing);
        oldTimes.push(performance.now() - t0);

        const t2 = performance.now(); runNew(src, size.w, size.h, p.dotSize, p.spacing);
        newTimes.push(performance.now() - t2);
      }

      const oldAvg = oldTimes.reduce((a, b) => a + b, 0) / oldTimes.length;
      const newAvg = newTimes.reduce((a, b) => a + b, 0) / newTimes.length;

      const gridCount = Math.ceil((size.h + p.dotSize * p.spacing) / (p.dotSize * p.spacing)) *
        Math.ceil((size.w + p.dotSize * p.spacing) / (p.dotSize * p.spacing));

      results.push({
        size: size.label,
        params: p.label,
        grids: gridCount,
        oldMs: Math.round(oldAvg),
        newMs: Math.round(newAvg),
        speedup: (oldAvg / newAvg).toFixed(1),
      });

      await new Promise(r => setTimeout(r, 50));
    }
  }

  return results;
}

run();
`;

(async () => {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu'],
  });

  const page = await browser.newPage();
  await page.goto('about:blank');

  console.log('Running benchmarks...\n');
  const results = await page.evaluate(BENCHMARK_CODE);

  console.log('\n========================================================');
  console.log('           SCREENPRINTFILTER PERFORMANCE BENCHMARK');
  console.log('           (Old: per-cell getImageData vs New: precomputed array)');
  console.log('========================================================\n');

  console.log('Size       | Params           | Grids   | Old(ms) | New(ms) | Speedup');
  console.log('-----------|------------------|---------|---------|---------|--------');
  for (const r of results) {
    console.log(
      `${r.size.padEnd(10)} | ${r.params.padEnd(16)} | ${String(r.grids).padStart(7)} | ` +
      `${String(r.oldMs).padStart(7)} | ${String(r.newMs).padStart(7)} | ${r.speedup}x`
    );
  }

  const totalOld = results.reduce((s, r) => s + r.oldMs, 0);
  const totalNew = results.reduce((s, r) => s + r.newMs, 0);
  console.log('-----------|------------------|---------|---------|---------|--------');
  console.log(
    `TOTAL      |                  |         | ${String(totalOld).padStart(7)} | ${String(totalNew).padStart(7)} | ${(totalOld / totalNew).toFixed(1)}x`
  );

  await browser.close();
  console.log('\nDone.');
})();
