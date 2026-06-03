// PicEte Language Sampling Test — zh + ja, 5 tools each
// Verifies: HTTP 200, translated title, no console errors
// Optional: zh/resize-image functional flow

import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FIXTURE = path.resolve(__dirname, 'fixtures', 'test-photo.jpg');
const BASE_URL = 'https://picete.com';

// Tools to sample per language
const TOOLS = [
  'resize-image',
  'compress-image',
  'png-to-jpg',
  'image-splitter',
  'extract-colors',
];

function fmt(tool, lang) {
  return `  ${lang === 'en' ? '' : lang + '/'}${tool}/`;
}

async function main() {
  let passed = 0;
  let failed = 0;

  function pass(msg) { console.log(`  PASS: ${msg}`); passed++; }
  function fail(msg) { console.log(`  FAIL: ${msg}`); failed++; }

  console.log('PicEte Language Sampling Test');
  console.log('=============================');
  console.log();

  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });

  // ---- Language page checks: zh ----
  console.log('--- zh (简体中文) ---');
  for (const tool of TOOLS) {
    const results = await checkLanguagePage(context, 'zh', tool);
    for (const r of results) {
      if (r.pass) pass(r.detail);
      else fail(r.detail);
    }
  }

  // ---- Language page checks: ja ----
  console.log();
  console.log('--- ja (日本語) ---');
  for (const tool of TOOLS) {
    const results = await checkLanguagePage(context, 'ja', tool);
    for (const r of results) {
      if (r.pass) pass(r.detail);
      else fail(r.detail);
    }
  }

  // ---- Functional test: zh/resize-image ----
  console.log();
  console.log('--- zh/resize-image functional test ---');
  const funcResults = await testZhResizeImage(context);
  for (const r of funcResults) {
    if (r.pass) pass(r.detail);
    else fail(r.detail);
  }

  await browser.close();

  // Summary
  console.log();
  console.log('=============================');
  console.log(`Results: ${passed} passed, ${failed} failed`);
  const verdict = failed === 0 ? 'PASS' : 'FAIL';
  console.log(`Verdict: ${verdict}`);
  process.exit(failed === 0 ? 0 : 1);
}

// Check a single language tool page
async function checkLanguagePage(context, lang, tool) {
  const results = [];
  const page = await context.newPage();

  // Collect console messages
  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });
  page.on('pageerror', err => {
    consoleErrors.push(`PAGE_ERROR: ${err.message}`);
  });

  const url = `${BASE_URL}/${lang}/${tool}/`;

  try {
    const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    // Check HTTP status
    const status = response.status();
    if (status === 200) {
      results.push({ name: `${lang}/${tool}/status`, pass: true, detail: `${lang}/${tool}/ → HTTP 200` });
    } else {
      results.push({ name: `${lang}/${tool}/status`, pass: false, detail: `${lang}/${tool}/ → HTTP ${status} (expected 200)` });
    }

    // Check page title
    const title = await page.title();
    if (lang === 'zh') {
      const hasChinese = /[\u4e00-\u9fff]/.test(title);
      results.push({
        name: `${lang}/${tool}/title`,
        pass: hasChinese,
        detail: hasChinese
          ? `${lang}/${tool}/ title: "${title}" — contains Chinese`
          : `${lang}/${tool}/ title: "${title}" — NO Chinese characters`
      });
    } else if (lang === 'ja') {
      const hasJapanese = /[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]/.test(title);
      results.push({
        name: `${lang}/${tool}/title`,
        pass: hasJapanese,
        detail: hasJapanese
          ? `${lang}/${tool}/ title: "${title}" — contains Japanese`
          : `${lang}/${tool}/ title: "${title}" — NO Japanese characters`
      });
    }

    // Check console errors
    const hasErrors = consoleErrors.length > 0;
    results.push({
      name: `${lang}/${tool}/console`,
      pass: !hasErrors,
      detail: hasErrors
        ? `${lang}/${tool}/ has ${consoleErrors.length} console error(s): ${consoleErrors.join('; ')}`
        : `${lang}/${tool}/ console: clean (no errors)`
    });

  } catch (err) {
    results.push({
      name: `${lang}/${tool}/error`,
      pass: false,
      detail: `${lang}/${tool}/ threw: ${err.message}`
    });
  } finally {
    await page.close();
  }

  return results;
}

// Functional test: zh/resize-image — upload, resize, verify download section
async function testZhResizeImage(context) {
  const results = [];
  const page = await context.newPage();

  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', err => {
    consoleErrors.push(`PAGE_ERROR: ${err.message}`);
  });

  const url = `${BASE_URL}/zh/resize-image/`;

  try {
    // Navigate
    const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    results.push({
      name: 'zh/resize-image/ functional: status',
      pass: response.status() === 200,
      detail: response.status() === 200
        ? `HTTP 200`
        : `HTTP ${response.status()}`
    });

    // Upload
    const fileInput = await page.$('#fileInput');
    if (!fileInput) throw new Error('#fileInput not found');
    await fileInput.setInputFiles(FIXTURE);
    await page.waitForSelector('#processingArea', { state: 'visible', timeout: 10000 });
    results.push({
      name: 'zh/resize-image/ functional: upload',
      pass: true,
      detail: 'Upload succeeded, processing area visible'
    });

    // Set dimensions
    await page.fill('#widthInput', '600');
    await page.fill('#heightInput', '400');
    results.push({
      name: 'zh/resize-image/ functional: dimensions',
      pass: true,
      detail: 'Width=600, Height=400 set'
    });

    // Click resize
    const resizeBtn = await page.$('#resizeBtn');
    if (!resizeBtn) throw new Error('#resizeBtn not found');
    await resizeBtn.click();
    results.push({
      name: 'zh/resize-image/ functional: click',
      pass: true,
      detail: 'Resize button clicked'
    });

    // Wait for download section
    await page.waitForSelector('#downloadSection', { state: 'visible', timeout: 15000 });
    results.push({
      name: 'zh/resize-image/ functional: download',
      pass: true,
      detail: 'Download section appeared — resize completed'
    });

    // Final console check
    results.push({
      name: 'zh/resize-image/ functional: console',
      pass: consoleErrors.length === 0,
      detail: consoleErrors.length === 0
        ? 'No console errors during functional flow'
        : `${consoleErrors.length} console error(s): ${consoleErrors.join('; ')}`
    });

  } catch (err) {
    results.push({
      name: 'zh/resize-image/ functional: error',
      pass: false,
      detail: `Error: ${err.message}`
    });
  } finally {
    await page.close();
  }

  return results;
}

main();
