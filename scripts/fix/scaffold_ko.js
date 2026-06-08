#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const KO_DIR = path.join(ROOT, 'ko');

if (!fs.existsSync(KO_DIR)) {
  fs.mkdirSync(KO_DIR);
}

// Files at root
const rootFiles = ['index.html', 'privacy-policy.html'];
for (const file of rootFiles) {
  const src = path.join(ROOT, file);
  const dest = path.join(KO_DIR, file);
  if (fs.existsSync(src)) {
    let content = fs.readFileSync(src, 'utf8');
    content = content.replace(/<html lang="en">/, '<html lang="ko">');
    // For canonical links like <link rel="canonical" href="https://picete.com/..." />
    content = content.replace(/<link rel="canonical" href="https:\/\/picete\.com\//g, '<link rel="canonical" href="https://picete.com/ko/');
    fs.writeFileSync(dest, content, 'utf8');
  }
}

// Tool directories
const excludeDirs = new Set(['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko', 'css', 'js', 'images', 'config', 'docs', 'scripts', 'seo', '.git', '__pycache__', 'node_modules', '.well-known', 'convert']);

for (const entry of fs.readdirSync(ROOT, { withFileTypes: true })) {
  if (entry.isDirectory() && !excludeDirs.has(entry.name)) {
    const srcIndex = path.join(ROOT, entry.name, 'index.html');
    if (fs.existsSync(srcIndex)) {
      const destDir = path.join(KO_DIR, entry.name);
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir);
      }
      let content = fs.readFileSync(srcIndex, 'utf8');
      content = content.replace(/<html lang="en">/, '<html lang="ko">');
      // Replace canonical link
      content = content.replace(/<link rel="canonical" href="https:\/\/picete\.com\//g, '<link rel="canonical" href="https://picete.com/ko/');
      fs.writeFileSync(path.join(destDir, 'index.html'), content, 'utf8');
    }
  }
}

console.log("Scaffolded ko/ directory.");
