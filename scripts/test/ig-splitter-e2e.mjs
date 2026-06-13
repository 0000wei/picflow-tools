import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FIXTURE = path.resolve(__dirname, 'fixtures', 'test-photo.jpg');
const BASE_URL = 'https://picete.com';
const LANGUAGES = ['en', 'zh', 'ja', 'ko', 'de', 'fr', 'es', 'pt', 'ar'];

async function main() {
  console.log('PicEte Playwright Smoke Test: Instagram Image Splitter');
  console.log('======================================================');

  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  
  let passed = 0;
  let failed = 0;
  function pass(msg) { console.log(`  PASS: ${msg}`); passed++; }
  function fail(msg) { console.log(`  FAIL: ${msg}`); failed++; }

  for (const lang of LANGUAGES) {
    const urlPath = lang === 'en' ? '/instagram-image-splitter/' : `/${lang}/instagram-image-splitter/`;
    const url = `${BASE_URL}${urlPath}`;
    console.log(`\nTesting ${lang.toUpperCase()}: ${url}`);

    const page = await context.newPage();
    try {
      const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      if (response.status() === 200) {
        pass(`HTTP 200`);
      } else {
        fail(`HTTP ${response.status()}`);
      }

      const title = await page.title();
      if (title.length > 0) pass(`Title exists: ${title}`);
      else fail(`Missing title`);

      const fileInput = await page.$('#fileInput');
      if (fileInput) {
        await fileInput.setInputFiles(FIXTURE);
        await page.waitForTimeout(2000); // wait for canvas drawing
        pass('Image uploaded to canvas');

        const downloadPromise = page.waitForEvent('download', { timeout: 15000 }).catch(() => null);
        const downloadBtn = await page.$('.btn-download');
        if (downloadBtn) {
            await downloadBtn.click();
            const download = await downloadPromise;
            if (download) {
                const name = download.suggestedFilename();
                if (name.endsWith('.zip')) {
                    pass(`ZIP Downloaded successfully: ${name}`);
                } else {
                    fail(`Downloaded file is not a ZIP: ${name}`);
                }
            } else {
                fail('No download triggered within timeout');
            }
        } else {
            fail('.btn-download not found');
        }
      } else {
        fail('#fileInput not found');
      }

    } catch (err) {
      fail(`Exception: ${err.message}`);
    } finally {
      await page.close();
    }
  }

  await browser.close();
  
  console.log('\n======================================================');
  console.log(`Results: ${passed} passed, ${failed} failed`);
  process.exit(failed === 0 ? 0 : 1);
}

main();
