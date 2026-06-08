#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function findHtmlFiles(dir) {
  const results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name === 'node_modules') continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...findHtmlFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

function fixLogos(content) {
  // Fix broken self-closing from previous run: '/ width="116" height="32">' → ' width="116" height="32">'
  content = content.replace(/\/ width="116" height="32">/g, ' width="116" height="32">');
  content = content.replace(/\/ width="101" height="28">/g, ' width="101" height="28">');

  // Add width/height to logo-img tags that still lack them
  content = content.replace(
    /<img\b([^>]*class="[^"]*logo-img[^"]*"[^>]*)>/g,
    (match, attrs) => {
      if (/\bwidth\s*=/.test(attrs)) return match;
      return `<img${attrs} width="116" height="32">`;
    }
  );

  // Add width/height to footer-logo tags that still lack them
  content = content.replace(
    /<img\b([^>]*class="[^"]*footer-logo[^"]*"[^>]*)>/g,
    (match, attrs) => {
      if (/\bwidth\s*=/.test(attrs)) return match;
      return `<img${attrs} width="101" height="28">`;
    }
  );

  return content;
}

const rootDir = path.resolve(__dirname, '..', '..');
const htmlFiles = findHtmlFiles(rootDir);
let updated = 0;

for (const file of htmlFiles) {
  const original = fs.readFileSync(file, 'utf8');
  const fixed = fixLogos(original);
  if (fixed !== original) {
    fs.writeFileSync(file, fixed, 'utf8');
    console.log(`Updated: ${path.relative(rootDir, file)}`);
    updated++;
  }
}

console.log(`\nDone. Updated ${updated} of ${htmlFiles.length} HTML files.`);
