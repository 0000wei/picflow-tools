// ================================================================
// Phase 0 深度验证脚本 — Alpha 保留 + 画质评估 + colours 排查 + 内存测试
// 粘贴到 http://localhost:3000/compress-image/ 的 Console 运行
// ================================================================
(async () => {
  'use strict';
  const fmt = (b) => (b / 1024).toFixed(1) + ' KB';
  const pct = (a, b) => b ? ((b - a) / b * 100).toFixed(1) + '%' : '-';
  console.log('%c=== Phase 0 Deep Verification ===', 'font-size:16px;font-weight:bold');

  const vips = await VipsLoader.load();
  if (!vips) { console.error('❌ VipsLoader failed'); return; }
  console.log('✅ wasm-vips', vips.version(), '\n');

  // ========== Test images ==========
  const files = [
    { name: 'test-alpha-gradient.png',    type: 'alpha' },
    { name: 'test-fully-transparent.png', type: 'alpha' },
    { name: 'test-photo-800x600.png',     type: 'photo' },
    { name: 'test-photo-320x240.png',     type: 'photo' },
    { name: 'test-photo-1920x1080.png',   type: 'photo' },
  ];

  // ========== Helper: load + compress ==========
  async function loadAndCompress(name, opts) {
    const resp = await fetch('/images/' + name);
    const buf = await resp.arrayBuffer();
    const u8 = new Uint8Array(buf);
    let image;
    try {
      image = vips.Image.newFromBuffer(u8);
    } catch (e) {
      return { error: 'load failed: ' + e.message, origSize: buf.byteLength };
    }
    let result;
    try {
      const out = image.writeToBuffer('.png', opts);
      result = { error: null, origSize: buf.byteLength, compSize: out.byteLength, buffer: out.buffer };
    } catch (e) {
      result = { error: 'compress failed: ' + (e.message || String(e)), origSize: buf.byteLength };
    } finally {
      image.delete();
    }
    return result;
  }

  // ========== 1. ALPHA RETENTION TEST ==========
  console.log('\n%c=== 1. Alpha Channel Retention ===', 'font-weight:bold');

  // Load alpha images, compress, re-read to check alpha preservation
  for (const f of files.filter(f => f.type === 'alpha')) {
    const r = await loadAndCompress(f.name, { palette: true, Q: 80, effort: 7, compression: 9 });
    if (r.error) {
      console.log(`  ❌ ${f.name}: ${r.error}`);
      continue;
    }
    // Decode compressed result to count non-black transparent pixels
    const blob = new Blob([r.buffer], { type: 'image/png' });
    const url = URL.createObjectURL(blob);
    const img = await new Promise(res => { const i = new Image(); i.onload = () => res(i); i.src = url; });
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const data = ctx.getImageData(0, 0, img.width, img.height).data;
    URL.revokeObjectURL(url);

    // Count: fully transparent (alpha=0) vs semi-transparent (0<alpha<255) vs opaque (alpha=255)
    let total = data.length / 4;
    let transparent = 0, semi = 0, opaque = 0;
    for (let i = 3; i < data.length; i += 4) {
      if (data[i] === 0) transparent++;
      else if (data[i] < 255) semi++;
      else opaque++;
    }
    const hasAlpha = transparent > 0 || semi > 0;
    console.log(`  ${f.name}: ${fmt(r.origSize)} → ${fmt(r.compSize)} (${pct(r.compSize, r.origSize)})`);
    console.log(`    Alpha: transparent=${transparent} semi=${semi} opaque=${opaque}`);
    if (hasAlpha && (total - opaque) > 10) {
      console.log(`    ✅ Alpha preserved (${((total-opaque)/total*100).toFixed(1)}% non-opaque)`);
    } else if (hasAlpha) {
      console.log(`    ❌ ALPHA LOST — all pixels became opaque`);
    } else {
      console.log(`    ℹ️ No alpha expected`);
    }
  }

  // ========== 2. QUALITY ASSESSMENT (PSNR + SSIM) ==========
  console.log('\n%c=== 2. Quality Assessment (PSNR) ===', 'font-weight:bold');

  async function calcPSNR(origBytes, compressedBytes) {
    // Decode both to Canvas, compare pixel by pixel
    const decode = async (buf) => {
      const blob = new Blob([buf], { type: 'image/png' });
      const url = URL.createObjectURL(blob);
      const img = await new Promise(res => { const i = new Image(); i.onload = () => res(i); i.src = url; });
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      c.getContext('2d').drawImage(img, 0, 0);
      const d = c.getContext('2d').getImageData(0, 0, img.width, img.height).data;
      URL.revokeObjectURL(url);
      return { data: d, w: img.width, h: img.height };
    };
    const orig = await decode(origBytes);
    let image;
    try { image = vips.Image.newFromBuffer(new Uint8Array(origBytes)); } catch(e) { return { psnr: null, error: e.message }; }
    let compBuf, compSize;
    try {
      const out = image.writeToBuffer('.png', { palette: true, Q: 80, effort: 7 });
      compBuf = out.buffer; compSize = out.byteLength;
    } catch(e) { image.delete(); return { psnr: null, error: e.message }; }
    image.delete();
    const comp = await decode(compBuf);

    const minH = Math.min(orig.h, comp.h);
    const minW = Math.min(orig.w, comp.w);
    let mse = 0, pixels = 0;
    for (let y = 0; y < minH; y++) {
      for (let x = 0; x < minW; x++) {
        const oi = (y * orig.w + x) * 4;
        const ci = (y * comp.w + x) * 4;
        const dr = orig.data[oi] - comp.data[ci];
        const dg = orig.data[oi+1] - comp.data[ci+1];
        const db = orig.data[oi+2] - comp.data[ci+2];
        mse += dr*dr + dg*dg + db*db;
        pixels++;
      }
    }
    mse /= (pixels * 3);
    const psnr = mse > 0 ? 10 * Math.log10(255*255 / mse) : Infinity;
    return { psnr: psnr.toFixed(1), compSize, savings: pct(compSize, origBytes) };
  }

  for (const f of files) {
    const resp = await fetch('/images/' + f.name);
    const buf = await resp.arrayBuffer();
    const q = await calcPSNR(buf);
    if (q.error) {
      console.log(`  ${f.name}: ERROR — ${q.error}`);
    } else {
      const lbl = q.psnr >= 40 ? '✅ Excellent' : q.psnr >= 30 ? '⚠️ Good' : '❌ Poor';
      console.log(`  ${f.name}: ${fmt(buf.byteLength)} → ${fmt(q.compSize)} (${q.savings})  PSNR: ${q.psnr} dB  ${lbl}`);
    }
  }

  // ========== 3. COLOURS PARAMETER INVESTIGATION ==========
  console.log('\n%c=== 3. Colours Parameter Investigation ===', 'font-weight:bold');

  const testValues = [256, 128, 64, 32, 16, 8, 4, 2];
  const testFile = 'test-photo-320x240.png';
  const resp = await fetch('/images/' + testFile);
  const baseBuf = await resp.arrayBuffer();
  const baseU8 = new Uint8Array(baseBuf);

  function safeMsg(e) {
    const msg = e.message || String(e);
    if (Array.isArray(msg)) return msg.join(' | ').substring(0, 80);
    return msg.substring(0, 80);
  }

  for (const nCol of testValues) {
    let image;
    try { image = vips.Image.newFromBuffer(baseU8); } catch(e) { console.log(`  load failed`); continue; }
    try {
      const out = image.writeToBuffer('.png', { palette: true, colours: nCol, Q: 80, effort: 7 });
      console.log(`  colours=${nCol.toString().padStart(4)}: ✅  ${fmt(out.byteLength)} (${pct(out.byteLength, baseBuf.byteLength)})`);
    } catch(e) {
      console.log(`  colours=${nCol.toString().padStart(4)}: ❌  ${safeMsg(e)}`);
    } finally {
      image.delete();
    }
  }

  // Q-only (no colours) for comparison
  let image;
  try { image = vips.Image.newFromBuffer(baseU8); } catch(e) { console.log(`  load failed`); }
  if (image) {
    try {
      const out = image.writeToBuffer('.png', { palette: true, Q: 80, effort: 7 });
      console.log(`  Q-only  : ✅  ${fmt(out.byteLength)} (${pct(out.byteLength, baseBuf.byteLength)})`);
    } catch(e) {
      console.log(`  Q-only  : ❌  ${safeMsg(e)}`);
    } finally {
      image.delete();
    }
  }

  // ========== 4. MEMORY STRESS TEST ==========
  console.log('\n%c=== 4. Memory Stress Test (50 cycles) ===', 'font-weight:bold');

  let failures = 0;
  for (let i = 0; i < 50; i++) {
    let img;
    try {
      img = vips.Image.newFromBuffer(baseU8);
      const out = img.writeToBuffer('.png', { palette: true, Q: Math.min(90, 30 + i), effort: 7 });
      // Intentionally vary Q to simulate slider drag
      img.delete();
      img = null;
    } catch(e) {
      failures++;
      console.log(`  Cycle ${i}: ❌ ${safeMsg(e)}`);
    } finally {
      if (img) { try { img.delete(); } catch(_) {} }
    }
    if ((i+1) % 10 === 0) console.log(`  ${i+1}/50 cycles completed (${failures} failures)`);
  }
  console.log(`  Memory stress test: ${failures === 0 ? '✅ All 50/50 passed' : `⚠️ ${50-failures}/50 passed, ${failures} failures`}`);

  console.log('\n%c=== Verification Complete ===', 'font-size:16px;font-weight:bold');
  console.log('%cPlease copy ALL output above and send to the agent.', 'color:#6b7280');
})();
