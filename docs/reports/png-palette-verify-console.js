// =====================================================
// PNG Palette Quantization Verification Script
// 粘贴到 http://localhost:3000/compress-image/ 的 Console 运行
// =====================================================
(async () => {
  'use strict';

  console.log('=== PNG Palette Quantization Verification ===\n');

  // 1. 环境检测
  console.log('Environment:');
  console.log(`  SharedArrayBuffer: ${typeof SharedArrayBuffer !== 'undefined' ? '✅' : '❌'}`);
  console.log(`  crossOriginIsolated: ${self.crossOriginIsolated ? '✅' : '❌'}`);

  // 2. 加载 VipsLoader
  const vips = await VipsLoader.load();
  if (!vips) {
    console.error('❌ VipsLoader failed:', VipsLoader.error);
    return;
  }
  console.log(`\n✅ wasm-vips loaded, version: ${vips.version()}\n`);

  // 3. 测试图片
  const files = ['test-photo-320x240.png', 'test-photo-1920x1080.png', 'test-solid-white.png', 'test-solid-red.png'];

  const header = `| ${'File'.padEnd(28)} | ${'Original'.padEnd(10)} | ${'Baseline'.padEnd(10)} | ${'Test A(col=64)'.padEnd(14)} | ${'Save A'.padEnd(8)} | ${'Test B(Q-only)'.padEnd(14)} | ${'Save B'.padEnd(8)} | ${'Test C(keep=0)'.padEnd(14)} | Notes`;
  const sep = '|' + '-'.repeat(30) + '|' + '-'.repeat(12) + '|' + '-'.repeat(12) + '|' + '-'.repeat(16) + '|' + '-'.repeat(10) + '|' + '-'.repeat(16) + '|' + '-'.repeat(10) + '|' + '-'.repeat(16) + '|' + '-'.repeat(30);
  console.log(header);
  console.log(sep);

  for (const name of files) {
    try {
      const resp = await fetch('/images/' + name);
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      const buf = await resp.arrayBuffer();
      const u8 = new Uint8Array(buf);
      const src = vips.ImageSource.newFromBuffer(u8);
      const img = vips.Image.newFromSource(src, '');
      src.delete();
      const origKB = (buf.byteLength / 1024).toFixed(1);

      // 基线
      let baseline = null, bsKB = '-';
      try { baseline = img.writeToBuffer('.png', {}).buffer.byteLength; bsKB = (baseline / 1024).toFixed(1); } catch(e) { }

      // A: palette + colours=64
      let a = null, aKB = '-', aPct = '-';
      try {
        a = img.writeToBuffer('.png', { palette: true, colours: 64, Q: 80, effort: 7 }).buffer.byteLength;
        aKB = (a / 1024).toFixed(1);
        if (baseline) aPct = ((baseline - a) / baseline * 100).toFixed(1) + '%';
      } catch(e) { aKB = 'ERR'; }

      // B: Q-only
      let b = null, bKB = '-', bPct = '-';
      try {
        b = img.writeToBuffer('.png', { palette: true, Q: 80, effort: 7 }).buffer.byteLength;
        bKB = (b / 1024).toFixed(1);
        if (baseline) bPct = ((baseline - b) / baseline * 100).toFixed(1) + '%';
      } catch(e) { bKB = 'ERR'; }

      // C: keep=0
      let c = null, cKB = '-';
      try {
        c = img.writeToBuffer('.png', { palette: true, compression: 9, keep: 0 }).buffer.byteLength;
        cKB = (c / 1024).toFixed(1);
      } catch(e) { cKB = 'ERR'; }

      img.delete();

      // Notes
      let notes = '';
      if (a === null) notes = 'palette NOT supported ❌';
      else if (b !== null && a !== null) notes = (b / a < 1.1) ? 'Q-only ≈ colours=64 ✅' : `Q-only ${(b/a).toFixed(2)}x ⚠️`;
      else if (b === null && a !== null) notes = 'Q-only FAILED ⚠️';
      if (c === null) notes += (notes ? ' | ' : '') + 'keep=0 FAILED ⚠️';

      console.log(`| ${name.padEnd(28)} | ${origKB.padEnd(10)} | ${bsKB.padEnd(10)} | ${aKB.padEnd(14)} | ${aPct.padEnd(8)} | ${bKB.padEnd(14)} | ${bPct.padEnd(8)} | ${cKB.padEnd(14)} | ${notes}`);
    } catch(e) {
      console.log(`| ${name.padEnd(28)} | LOAD FAILED: ${e.message}`);
    }
  }

  console.log('\n=== Verification Complete ===');
})();
