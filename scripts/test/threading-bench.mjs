// threading-bench.mjs
// 单线程性能对比测试：Canvas (sharp) vs wasm-vips 多线程 vs wasm-vips 单线程
// Run: node scripts/test/threading-bench.mjs
//
// 设计说明：
//   - 每个 benchmark 跑 WARMUP + RUNS 次，取最后 RUNS 次求平均
//   - WARMUP=5 确保 WASM 首次编译/线程池初始化开销从测量中排除
//   - 测试顺序：多线程 → 单线程 → sharp (sharp 不受前序影响)
//   - vips.concurrency() 用于控制线程数 (getter/setter)
//   - 记录每个方法的平均耗时、标准差、输出文件大小

import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '../..');
const FIXTURES = resolve(PROJECT_ROOT, 'scripts/test/fixtures');
const INPUT_PATH = resolve(FIXTURES, 'test-photo.jpg');

const require = createRequire(import.meta.url);

const RUNS = 5;         // 正式测量次数
const WARMUP = 5;       // 预热次数（排除 WASM 编译/线程池初始化）

// 目标尺寸：800×600 → 400×300 (scale factor 0.5)
const TARGET_W = 400;
const TARGET_H = 300;
const SCALE = 0.5;

function padRight(s, n) { s = String(s ?? ''); return s.padEnd(n); }

function avg(arr) {
  if (arr.length === 0) return 0;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function stddev(arr, mean) {
  if (arr.length < 2) return 0;
  const variance = arr.reduce((sum, v) => sum + (v - mean) ** 2, 0) / (arr.length - 1);
  return Math.sqrt(variance);
}

/**
 * 一组 wasm-vips resize 基准测试
 */
async function runVipsBench(vips, inputBuf, conc, label) {
  vips.concurrency(conc);

  const total = WARMUP + RUNS;
  const allTimes = [];

  for (let i = 0; i < total; i++) {
    const t0 = performance.now();
    const img = vips.Image.newFromBuffer(inputBuf);
    const resized = img.resize(SCALE);
    const buf = resized.writeToBuffer('.jpg');
    const t1 = performance.now();
    allTimes.push({ elapsed: t1 - t0, size: buf.length });
    img.delete();
    resized.delete();
  }

  const measured = allTimes.slice(-RUNS);
  const vals = measured.map(r => r.elapsed);
  const mean = avg(vals);
  const std = stddev(vals, mean);
  const lastSize = measured[measured.length - 1].size;

  process.stdout.write(`  ${label} concurrency=${conc} ...`);
  process.stdout.write(` avg=${mean.toFixed(1)}ms`);

  return { times: vals, avgTime: mean, std, size: lastSize, concurrency: conc, raw: allTimes };
}

/**
 * Sharp 基准测试
 */
async function runSharpBench(inputBuf) {
  const sharp = require('sharp');
  const total = WARMUP + RUNS;
  const allTimes = [];

  for (let i = 0; i < total; i++) {
    const t0 = performance.now();
    const buf = await sharp(inputBuf).resize(TARGET_W, TARGET_H).jpeg({ quality: 85 }).toBuffer();
    const t1 = performance.now();
    allTimes.push({ elapsed: t1 - t0, size: buf.length });
  }

  const measured = allTimes.slice(-RUNS);
  const vals = measured.map(r => r.elapsed);
  const mean = avg(vals);
  const std = stddev(vals, mean);
  const lastSize = measured[measured.length - 1].size;

  process.stdout.write(`  Canvas (sharp) ... avg=${mean.toFixed(1)}ms`);

  return { times: vals, avgTime: mean, std, size: lastSize };
}

async function main() {
  console.log('='.repeat(72));
  console.log('  wasm-vips vs Canvas (sharp) — resize 性能对比');
  console.log('  ' + new Date().toISOString());
  console.log('='.repeat(72));
  console.log();

  // 1. 校验输入
  try {
    const sharp = require('sharp');
    const meta = await sharp(INPUT_PATH).metadata();
    console.log(`  📷 输入: ${meta.width}×${meta.height} JPEG`);
    console.log(`  🎯 输出: ${TARGET_W}×${TARGET_H} JPEG quality=85 (scale=${SCALE})`);
    console.log(`  📊 方法: 预热${WARMUP}次 + 测量${RUNS}次取平均`);
    console.log();
  } catch (e) {
    console.error('  ❌ 无法读取测试图片:', e.message);
    process.exit(1);
  }

  // 2. 初始化 wasm-vips
  console.log('  ⚙️  初始化 wasm-vips...');
  let vips;
  try {
    vips = await (require('wasm-vips')());
  } catch (e) {
    console.error('  ❌ wasm-vips 初始化失败:', e.message);
    process.exit(1);
  }

  const defaultConc = vips.concurrency();
  const configLines = vips.config().split('\n');
  const simdLine = configLines.find(l => l.includes('SIMD'));
  console.log(`     wasm-vips ${vips.version()} | concurrency=${defaultConc}`);
  console.log(`     ${simdLine || 'no SIMD info'}`);
  console.log();

  // 3. 读取输入 buffer (复用)
  const inputBuf = readFileSync(INPUT_PATH);

  // 4. 运行测试
  console.log('  运行基准测试...');
  console.log();

  // 顺序：多线程先跑（含 WASM 编译开销在预热中被排除）
  //       然后单线程，最后 sharp
  const resultB = await runVipsBench(vips, inputBuf, defaultConc, 'B');
  console.log(' |');
  const resultC = await runVipsBench(vips, inputBuf, 1, 'C');
  console.log(' |');
  const resultA = await runSharpBench(inputBuf);
  console.log();
  console.log();

  // 恢复 concurrency
  vips.concurrency(defaultConc);

  // 5. 对比表
  console.log('  ┌──────────────────────────┬───────────────┬──────────────────────┬────────────┐');
  console.log('  │ 方法                      │ 平均耗时(ms)   │ 输出大小(bytes)       │ 标准差(σ)   │');
  console.log('  ├──────────────────────────┼───────────────┼──────────────────────┼────────────┤');

  const methods = [
    { label: 'Canvas (sharp)',       a: resultA, note: 'node-addon (libvips C)' },
    { label: 'wasm-vips 多线程',      a: resultB, note: `${defaultConc} threads` },
    { label: 'wasm-vips 单线程',      a: resultC, note: '1 thread' },
  ];
  const fastest = Math.min(...methods.map(m => m.a.avgTime));
  const fastestSize = resultA.size; // sharp 的输出

  for (const m of methods) {
    const t = m.a.avgTime.toFixed(1);
    const sz = String(m.a.size).padStart(8);
    const s = m.a.std.toFixed(1);
    const ratio = (m.a.avgTime / fastest).toFixed(2);
    const bar = '█'.repeat(Math.round((m.a.avgTime / fastest) * 20));
    const label = m.label.padEnd(24);
    console.log(`  │ ${label} │ ${t}ms (${ratio}×) │ ${sz} bytes      │ ${s.padStart(6)}    │`);
  }

  console.log('  └──────────────────────────┴───────────────┴──────────────────────┴────────────┘');
  console.log();
  console.log(`  💡 最快: Canvas (sharp) = ${fastest.toFixed(1)}ms`);
  console.log();

  // 6. 详细分析
  console.log('  详细运行数据:');
  console.log('  ──────────────────────────────────────────────────────────────────────────────');

  for (const [label, result, conc] of [
    ['Canvas (sharp)', resultA, '-'],
    ['wasm-vips 多线程', resultB, defaultConc],
    ['wasm-vips 单线程', resultC, '1'],
  ]) {
    if (result.raw) {
      // 显示前几次（预热）的耗时
      const pre = result.raw.slice(0, WARMUP);
      const post = result.raw.slice(-RUNS);
      const preStr = pre.map(r => r.elapsed.toFixed(0)).join(' ');
      const postStr = post.map(r => r.elapsed.toFixed(1)).join(' ');
      const note = conc !== '-' ? ` (concurrency=${conc})` : '';
      console.log(`  ${label}${note}`);
      console.log(`    预热: ${preStr} ms`);
      console.log(`    测量: ${postStr} ms`);
    }
  }

  console.log();

  // 7. 结论
  console.log('  ====== 结论 ======');
  console.log();

  const ratioSingleVsSharp = resultC.avgTime / resultA.avgTime;
  const ratioMultiVsSharp  = resultB.avgTime / resultA.avgTime;
  const ratioMultiVsSingle = resultB.avgTime / resultC.avgTime;

  console.log(`  🏆 性能排行:`);
  const sorted = [...methods].sort((a, b) => a.a.avgTime - b.a.avgTime);
  sorted.forEach((m, i) => {
    const medal = ['🥇', '🥈', '🥉'][i] || '  ';
    console.log(`  ${medal} ${m.label.padEnd(22)}: ${m.a.avgTime.toFixed(1)}ms`);
  });

  console.log();
  console.log(`  🔬 详细对比:`);
  console.log(`     wasm-vips 单线程 vs Canvas (sharp): ${(ratioSingleVsSharp).toFixed(2)}× (${resultC.avgTime.toFixed(1)}/${resultA.avgTime.toFixed(1)})`);
  console.log(`     wasm-vips 多线程 vs Canvas (sharp): ${(ratioMultiVsSharp).toFixed(2)}× (${resultB.avgTime.toFixed(1)}/${resultA.avgTime.toFixed(1)})`);
  console.log(`     wasm-vips 多线程 vs 单线程:         ${(ratioMultiVsSingle).toFixed(2)}× (${resultB.avgTime.toFixed(1)}/${resultC.avgTime.toFixed(1)})`);
  console.log();

  // 降级方案判断
  console.log(`  🔄 降级方案评估 (非 SharedArrayBuffer 环境):`);
  if (resultC.avgTime <= resultA.avgTime * 1.5) {
    console.log(`     wasm-vips 单线程: ${resultC.avgTime.toFixed(1)}ms`);
    console.log(`     Canvas API:       ${resultA.avgTime.toFixed(1)}ms`);
    console.log(`     差距 ${(ratioSingleVsSharp).toFixed(2)}× — ✅ 可接受 (慢不到 50%)`);
  } else {
    console.log(`     wasm-vips 单线程: ${resultC.avgTime.toFixed(1)}ms (${(ratioSingleVsSharp).toFixed(1)}× slower)`);
    console.log(`     Canvas API:       ${resultA.avgTime.toFixed(1)}ms`);
    console.log(`     差距 ${(ratioSingleVsSharp).toFixed(1)}× — ⚠️ 降级方案性能不佳`);
    console.log(`     注意: Node.js 环境下 wasm-vips 通过 V8 的 WebAssembly + SharedArrayBuffer 实现多线程`);
    console.log(`     浏览器端如果无法启用 COOP/COEP，则 wasm-vips 只能运行单线程。`);
    console.log(`     但如果浏览器原生 Canvas API 可用，应优先使用 Canvas 而非 wasm-vips 单线程。`);
  }

  console.log();
  console.log('='.repeat(72));

  // 简短结论行 (用于 grep)
  console.log();
  console.log('THREADING_BENCH_RESULT');
  console.log(`sharp=${resultA.avgTime.toFixed(1)}ms`);
  console.log(`vips_multi=${resultB.avgTime.toFixed(1)}ms`);
  console.log(`vips_single=${resultC.avgTime.toFixed(1)}ms`);
  console.log(`ratio_single_vs_sharp=${ratioSingleVsSharp.toFixed(2)}`);
  console.log('END_THREADING_BENCH_RESULT');
}

main().catch(e => {
  console.error('\nFATAL:', e);
  process.exit(1);
});
