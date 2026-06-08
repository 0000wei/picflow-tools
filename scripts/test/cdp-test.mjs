import { chromium } from 'playwright';

async function runTest() {
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: true });
  
  // Create context
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Set up console log listening
  page.on('console', msg => {
    console.log(`[BROWSER CONSOLE] [${msg.type()}] ${msg.text()}`);
  });
  
  page.on('pageerror', err => {
    console.error(`[BROWSER PAGE ERROR] ${err.message}\n${err.stack}`);
  });
  
  page.on('request', req => {
    const url = req.url();
    if (url.includes('vips') || url.includes('gtag') || url.includes('cookie')) {
      console.log(`[NETWORK REQ] ${req.method()} ${url}`);
    }
  });

  page.on('requestfailed', req => {
    console.error(`[NETWORK REQ FAILED] ${req.url()} - ${req.failure().errorText}`);
  });

  page.on('response', res => {
    const url = res.url();
    if (url.includes('vips') || url.includes('gtag') || url.includes('cookie')) {
      console.log(`[NETWORK RES] ${res.status()} ${url}`);
    }
  });

  try {
    console.log('Navigating to https://picete.com/raw-to-jpg/ ...');
    await page.goto('https://picete.com/raw-to-jpg/', { waitUntil: 'networkidle', timeout: 60000 });
    console.log('Page loaded.');

    console.log('Checking crossOriginIsolated and SharedArrayBuffer:');
    const compat = await page.evaluate(() => {
      return {
        crossOriginIsolated: window.crossOriginIsolated,
        SharedArrayBuffer: typeof window.SharedArrayBuffer !== 'undefined',
        VipsExists: typeof window.Vips !== 'undefined',
        VipsLoaderExists: typeof VipsLoader !== 'undefined'
      };
    });
    console.log('Compatibility in page:', JSON.stringify(compat, null, 2));

    console.log('Evaluating VipsLoader.load() in page context...');
    const result = await page.evaluate(async () => {
      try {
        console.log('[page evaluate] Calling VipsLoader.load()...');
        const vips = await VipsLoader.load();
        if (vips) {
          return { success: true, version: vips.version() };
        } else {
          return { success: false, error: VipsLoader.error };
        }
      } catch (e) {
        return { success: false, exception: e.message };
      }
    });

    console.log('VipsLoader.load() result:', JSON.stringify(result, null, 2));

  } catch (err) {
    console.error('Test execution failed:', err);
  } finally {
    console.log('Closing browser...');
    await browser.close();
  }
}

runTest();
