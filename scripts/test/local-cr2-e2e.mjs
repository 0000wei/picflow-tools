import { chromium } from "playwright";
import fs from "fs";

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  page.on("console", msg => console.log("[BROWSER CONSOLE]", msg.text()));
  
  await page.goto("http://localhost:3000/raw-to-jpg/");
  console.log("Navigated");
  
  const buffer = fs.readFileSync("rawtest/dsc1756.arw");
  
  await page.evaluate(async (buf) => {
    window.testConvert = async function() {
        const vips = await VipsLoader.load();
        const uint8Array = new Uint8Array(buf);
        vips.FS.writeFile("test.arw", uint8Array);
        
        try {
            const img = vips.Image.newFromFile("test.arw");
            console.log("Loader used for ARW:", img.get("vips-loader"));
            // Get size
            console.log("Image width:", img.width, "height:", img.height);
        } catch(e) {
            console.log("Failed:", e.message);
        }
    };
  }, Array.from(buffer));
  
  await page.evaluate(`window.testConvert()`);
  
  await page.waitForTimeout(2000);
  await browser.close();
})();
