import fs from 'fs';
import path from 'path';

const baseDir = process.cwd();
const dirs = ['en', 'zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar'];
const tools = ['raw-to-jpg', 'raw-to-png', 'raw-to-webp', 'raw-to-avif'];

const target1 = `            const uint8Array = new Uint8Array(await file.arrayBuffer());
            const image = vips.Image.newFromBuffer(uint8Array, '');
            if (!image) {`;

const repl1 = `            const uint8Array = new Uint8Array(await file.arrayBuffer());
            
            // Write to MEMFS so vips can use the file extension hint (e.g., .arw)
            const safeName = file.name.replace(/[^a-zA-Z0-9.-]/g, '_');
            const virtualFile = 'temp_' + Date.now() + '_' + safeName;
            
            let image;
            try {
                vips.FS.writeFile(virtualFile, uint8Array);
                image = vips.Image.newFromFile(virtualFile);
            } catch (err) {
                try { vips.FS.unlink(virtualFile); } catch (e) {}
                throw err;
            }

            if (!image) {
                vips.FS.unlink(virtualFile);`;

const target2 = `            } finally {
                image.delete();
            }`;

const repl2 = `            } finally {
                image.delete();
                vips.FS.unlink(virtualFile);
            }`;

for (const lang of dirs) {
    for (const tool of tools) {
        let p = path.join(baseDir, tool, 'index.html');
        if (lang !== 'en') p = path.join(baseDir, lang, tool, 'index.html');
        
        if (fs.existsSync(p)) {
            let content = fs.readFileSync(p, 'utf8');
            if (content.includes("const image = vips.Image.newFromBuffer(uint8Array, '');")) {
                content = content.replace(target1, repl1);
                content = content.replace(target2, repl2);
                fs.writeFileSync(p, content, 'utf8');
                console.log('Patched', p);
            } else {
                console.log('Skipped or already patched', p);
            }
        }
    }
}
