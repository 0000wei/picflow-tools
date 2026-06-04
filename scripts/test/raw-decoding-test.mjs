/**
 * RAW Decoding Test
 *
 * Verifies that the self-compiled wasm-vips with libraw support
 * can decode real camera RAW files (CR2, NEF, DNG).
 *
 * Usage: node scripts/test/raw-decoding-test.mjs
 */

import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const VIPS_PATH = '/tmp/wasm-vips/lib/vips-node.js';
const FIXTURES_DIR = path.resolve(__dirname, 'fixtures');

const RAW_EXTENSIONS = ['.cr2', '.cr3', '.nef', '.nrw', '.dng', '.orf', '.rw2', '.arw', '.srw', '.raf', '.pef', '.x3f'];

const fmtBytes = (bytes) => {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
};

const fmtTime = (ms) => {
  if (ms < 1000) return `${ms.toFixed(0)}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
};

async function main() {
  console.log(`\nLoading wasm-vips from: ${VIPS_PATH}\n`);

  // Load the self-compiled wasm-vips (async factory function)
  let VipsFactory, vips;
  try {
    const require = createRequire(import.meta.url);
    VipsFactory = require(VIPS_PATH);
    // It's exported as default or as the module itself
    if (typeof VipsFactory !== 'function') {
      VipsFactory = VipsFactory.default || VipsFactory;
    }
    // Instantiate the module (returns a promise)
    vips = await VipsFactory();
  } catch (err) {
    console.error(`FAILED to load/instantiate wasm-vips: ${err.message}`);
    process.exit(1);
  }

  console.log(`wasm-vips loaded successfully (version: ${vips.version || 'unknown'})`);
  console.log(`Image.newFromFile available: ${typeof vips.Image?.newFromFile}`);

  // Find RAW test files
  const rawFiles = fs.readdirSync(FIXTURES_DIR)
    .filter(f => RAW_EXTENSIONS.includes(path.extname(f).toLowerCase()))
    .map(f => path.join(FIXTURES_DIR, f))
    .sort();

  if (rawFiles.length === 0) {
    console.error('No RAW files found in fixtures directory.');
    process.exit(1);
  }

  console.log(`Found ${rawFiles.length} RAW file(s) to test.\n`);

  // Test results
  const results = [];

  for (const filePath of rawFiles) {
    const fileName = path.basename(filePath);
    const fileSize = fs.statSync(filePath).size;
    const ext = path.extname(fileName).toLowerCase().slice(1).toUpperCase();

    console.log(`  Processing: ${fileName} (${fmtBytes(fileSize)})`);

    let status = 'FAIL';
    let decodeMs = 0;
    let outputSize = 0;
    let errorMsg = '';

    try {
      const start = performance.now();

      // Load RAW file via wasm-vips (uses libraw under the hood)
      const image = vips.Image.newFromFile(filePath);

      // Write as JPEG
      const jpegBuffer = image.writeToBuffer('.jpg', { Q: 85 });
      const totalTime = performance.now() - start;
      decodeMs = totalTime;
      outputSize = jpegBuffer.length;

      // Validate JPEG output
      if (jpegBuffer.length < 100) {
        status = 'FAIL';
        errorMsg = `Output too small: ${jpegBuffer.length} bytes`;
      } else if (jpegBuffer[0] === 0xFF && jpegBuffer[1] === 0xD8) {
        status = 'OK';

        // Save the output JPEG for visual verification
        const outPath = path.join(FIXTURES_DIR, `${path.basename(fileName, path.extname(fileName))}.jpg`);
        fs.writeFileSync(outPath, jpegBuffer);
      } else {
        status = 'FAIL';
        errorMsg = 'Output is not valid JPEG (no FF D8 header)';
      }

      // Clean up
      if (typeof image.close === 'function') image.close();
    } catch (err) {
      status = 'FAIL';
      errorMsg = err.message;
    }

    results.push({
      file: fileName,
      ext,
      size: fileSize,
      decodeMs,
      outputSize,
      status,
      error: errorMsg,
    });

    if (status === 'OK') {
      console.log(`  -> OK (decode: ${fmtTime(decodeMs)}, output: ${fmtBytes(outputSize)})`);
    } else {
      console.log(`  -> FAIL: ${errorMsg}`);
    }
    console.log('');
  }

  // Print summary table
  console.log('=== RAW Decoding Test ===');
  console.log('File'.padEnd(25) + '| Size'.padEnd(10) + '| Decode'.padEnd(10) + '| Output'.padEnd(10) + '| Status');
  console.log('-'.repeat(65));

  let okCount = 0;
  let failCount = 0;

  for (const r of results) {
    const sizeStr = fmtBytes(r.size);
    const timeStr = r.status === 'OK' ? fmtTime(r.decodeMs) : '-';
    const outStr = r.status === 'OK' ? fmtBytes(r.outputSize) : '-';
    const statusIcon = r.status === 'OK' ? 'OK' : 'FAIL';

    console.log(
      r.file.padEnd(25) +
      sizeStr.padStart(10) +
      timeStr.padStart(10) +
      outStr.padStart(10) +
      statusIcon.padStart(8)
    );

    if (r.status === 'OK') okCount++;
    else failCount++;
  }

  console.log('-'.repeat(65));
  console.log(`Total: ${results.length} | Pass: ${okCount} | Fail: ${failCount}`);

  // Exit with appropriate code
  if (okCount >= 2) {
    console.log('\nPASS: At least 2 RAW formats decoded successfully.');
    process.exit(0);
  } else {
    console.log('\nFAIL: Fewer than 2 RAW formats decoded successfully.');
    process.exit(1);
  }
}

main().catch(err => {
  console.error(`Unhandled error: ${err.message}`);
  process.exit(1);
});
