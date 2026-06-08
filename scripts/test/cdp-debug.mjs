import { chromium } from 'playwright';

async function runTest() {
  console.log('Launching browser with GUI and DevTools...');
  const browser = await chromium.launch({ 
    headless: false,
    devtools: true
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  page.on('console', msg => {
    console.log(`[CONSOLE] [${msg.type()}] ${msg.text()}`);
  });
  
  page.on('pageerror', err => {
    console.error(`[PAGE ERROR] ${err.message}\n${err.stack}`);
  });

  page.on('worker', worker => {
    console.log(`[WORKER CREATED] ${worker.url()}`);
    worker.on('console', msg => {
      console.log(`[WORKER CONSOLE] ${msg.text()}`);
    });
    worker.on('error', err => {
      console.error(`[WORKER ERROR] ${err.message}\n${err.stack}`);
    });
  });

  page.on('request', req => {
    const url = req.url();
    console.log(`[REQ] ${req.method()} ${url}`);
  });

  page.on('requestfailed', req => {
    console.error(`[REQ FAILED] ${req.url()} - ${req.failure()?.errorText || 'unknown'}`);
  });

  page.on('response', res => {
    console.log(`[RES] ${res.status()} ${res.url()}`);
  });

  try {
    console.log('Navigating to https://picete.com/raw-to-jpg/ ...');
    await page.goto('https://picete.com/raw-to-jpg/', { waitUntil: 'load', timeout: 60000 });
    console.log('Page loaded. Running VipsLoader.load()...');
    
    // We will evaluate VipsLoader.load() and wait for 60 seconds to see console output
    const resultPromise = page.evaluate(async () => {
      try {
        console.log('Calling VipsLoader.load()...');
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

    // Wait for 40 seconds to see if it resolves or logs anything in DevTools
    console.log('Waiting 45 seconds for VipsLoader to initialize or log errors...');
    const result = await Promise.race([
      resultPromise,
      new Promise(resolve => setTimeout(() => resolve({ success: false, timeout: true }), 45000))
    ]);

    console.log('Result:', JSON.stringify(result, null, 2));

  } catch (err) {
    console.error('Error:', err);
  } finally {
    console.log('Keeping browser open for 15 more seconds before closing...');
    await page.waitForTimeout(15000);
    await browser.close();
  }
}

runTest();
