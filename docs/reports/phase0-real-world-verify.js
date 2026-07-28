// ================================================================
// Phase 0 真实世界验证 — 自然照片/UI截图/预压缩图 + 熔断机制
// 粘贴到 http://localhost:3000/compress-image/ Console 运行
// ================================================================
(async () => {
  'use strict';
  const fmt = (b) => (b / 1024).toFixed(1) + ' KB';
  const pct = (a, b) => b > 0 ? ((b - a) / b * 100).toFixed(1) + '%' : '-';

  console.log('%c=== Phase 0 Real-world Verification ===', 'font-size:16px;font-weight:bold');

  const vips = await VipsLoader.load();
  if (!vips) { console.error('❌ VipsLoader failed'); return; }
  console.log('✅ wasm-vips', vips.version());

  // ========== 3 real test images ==========
  const files = [
    { name: 'real-nature-1920.png',     desc: '📷 自然风景照片(1920×1281)' },
    { name: 'real-ui-screenshot.png',   desc: '🖥️  UI 截图(1200×800, 含半透明阴影)' },
    { name: 'pre-compressed-by-tinypng.png', desc: '📦 已压缩过的 PNG(模拟二次压缩)' },
  ];

  // ========== Compression with fallback ==========
  async function compressSafe(name, opts) {
    const resp = await fetch('/images/' + name);
    const buf = await resp.arrayBuffer();
    const u8 = new Uint8Array(buf);
    let image;
    try { image = vips.Image.newFromBuffer(u8); }
    catch(e) { return { error: 'load failed: ' + e.message, origSize: buf.byteLength }; }

    try {
      const out = image.writeToBuffer('.png', opts);
      const compSize = out.byteLength;

      // ===== 熔断机制: if compressed ≥ original, return original =====
      if (compSize >= buf.byteLength) {
        console.log(`  ⚠️  ${name}: compressed(${fmt(compSize)}) ≥ original(${fmt(buf.byteLength)}) — FALLBACK to original`);
        return {
          error: null, origSize: buf.byteLength, compSize: buf.byteLength,
          fallback: true, buffer: buf,
          note: '熔断触发（压缩后≥原图，返回原图）'
        };
      }

      return {
        error: null, origSize: buf.byteLength, compSize,
        fallback: false, buffer: out.buffer,
        note: null
      };
    } catch(e) {
      return { error: 'compress failed: ' + ((e.message||'') + (e.message && e.message.join ? '|' + e.message.join('|') : '')).substring(0,80), origSize: buf.byteLength };
    } finally {
      image.delete();
    }
  }

  // ========== PSNR calculator ==========
  async function calcPSNR(origBytes, compBytes) {
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
    const comp = await decode(compBytes);
    const minH = Math.min(orig.h, comp.h);
    const minW = Math.min(orig.w, comp.w);
    let mse = 0, pixels = 0;
    for (let y = 0; y < minH; y++) {
      for (let x = 0; x < minW; x++) {
        const oi = (y * orig.w + x) * 4;
        const ci = (y * comp.w + x) * 4;
        // Only compare RGB (ignore alpha for UI screenshot)
        const dr = orig.data[oi] - comp.data[ci];
        const dg = orig.data[oi+1] - comp.data[ci+1];
        const db = orig.data[oi+2] - comp.data[ci+2];
        mse += dr*dr + dg*dg + db*db;
        pixels++;
      }
    }
    mse /= (pixels * 3);
    return mse > 0 ? (10 * Math.log10(255*255 / mse)).toFixed(1) : 'Infinity';
  }

  // ========== Run tests ==========
  console.log('\n' + '-'.repeat(70));
  console.log('Format: original → compressed | savings | PSNR | fallback | notes');
  console.log('-'.repeat(70));

  for (const f of files) {
    const resp = await fetch('/images/' + f.name);
    const origBuf = await resp.arrayBuffer();
    console.log(`\n${f.desc}`);
    console.log(`  原始大小: ${fmt(origBuf.byteLength)}`);

    // Test Q=80
    console.log(`  ── Q-only (Q=80)`);
    const r80 = await compressSafe(f.name, { palette: true, Q: 80, effort: 7, compression: 9 });
    if (r80.error) { console.log(`  ❌ ${r80.error}`); continue; }
    const save80 = pct(r80.compSize, r80.origSize);
    const psnr80 = r80.fallback ? '—' : await calcPSNR(origBuf, new Uint8Array(r80.buffer));
    console.log(`  ${fmt(r80.origSize)} → ${fmt(r80.compSize)} | ${save80} | PSNR: ${psnr80} dB | ${r80.fallback ? '⚠️ FALLBACK' : '✅ OK'}${r80.note ? ' | ' + r80.note : ''}`);

    // Test Q=60 (higher compression)
    const r60 = await compressSafe(f.name, { palette: true, Q: 60, effort: 7, compression: 9 });
    if (!r60.error) {
      const save60 = pct(r60.compSize, r60.origSize);
      const psnr60 = r60.fallback ? '—' : await calcPSNR(origBuf, new Uint8Array(r60.buffer));
      console.log(`  ── Q-only (Q=60) → ${save60} | PSNR: ${psnr60} dB | ${r60.fallback ? '⚠️ FALLBACK' : '✅ OK'}`);
    }

    // Test Q=40 (extreme)
    const r40 = await compressSafe(f.name, { palette: true, Q: 40, effort: 7, compression: 9 });
    if (!r40.error) {
      const save40 = pct(r40.compSize, r40.origSize);
      const psnr40 = r40.fallback ? '—' : await calcPSNR(origBuf, new Uint8Array(r40.buffer));
      console.log(`  ── Q-only (Q=40) → ${save40} | PSNR: ${psnr40} dB | ${r40.fallback ? '⚠️ FALLBACK' : '✅ OK'}`);
    }
  }

  // ========== Visual check: download gradient for banding inspection ==========
  console.log('\n' + '-'.repeat(70));
  console.log('🔍 视觉核查：下载以下文件检查色阶断层(Banding)');
  console.log('-'.repeat(70));
  console.log('  将以下链接在新标签页打开 → 右键保存 → 放大查看渐变区域');

  const gradResp = await fetch('/images/test-photo-320x240.png');
  const gradBuf = await gradResp.arrayBuffer();
  const gradU8 = new Uint8Array(gradBuf);
  let gradImg;
  try { gradImg = vips.Image.newFromBuffer(gradU8); } catch(e) {}
  if (gradImg) {
    try {
      const out = gradImg.writeToBuffer('.png', { palette: true, Q: 80, effort: 7 });
      const blob = new Blob([out.buffer], { type: 'image/png' });
      const url = URL.createObjectURL(blob);
      console.log(`  📥 Q-only(Q=80) compressed gradient: %c${url}`, 'color:#2563eb');
      console.log('  查看方法：打开链接 → 放大到 200% → 观察渐变是否有明显色阶');
    } catch(e) {
      console.log('  ❌ Failed to generate visual sample:', e.message);
    } finally {
      gradImg.delete();
    }
  }

  console.log('\n%c=== Verification Complete ===', 'font-size:14px;font-weight:bold');
  console.log('%c请将完整输出贴回给 agent', 'color:#6b7280');
})();
