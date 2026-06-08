import { chromium } from "playwright";

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  page.on("console", msg => console.log("[BROWSER CONSOLE]", msg.text()));
  
  await page.goto("http://localhost:3000/raw-to-jpg/");
  console.log("Navigated");
  
  await page.setInputFiles("#fileInput", "rawtest/dsc1756.arw");
  console.log("File uploaded");
  
  await page.click("#convertBtn");
  console.log("Convert clicked, waiting...");
  
  try {
      await page.waitForSelector('.download-item', { timeout: 30000 });
      console.log("SUCCESS: download item appeared");
      const kb = await page.$eval('.download-item p', el => el.textContent);
      console.log("File size:", kb);
  } catch (e) {
      console.log("FAILURE: timed out waiting for download item");
  }
  
  await browser.close();
})();
