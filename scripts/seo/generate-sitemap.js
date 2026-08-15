#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const SITEMAP_FILE = path.join(ROOT, 'seo', 'sitemap.xml');
const BASE_URL = 'https://picete.com';
const TODAY = new Date().toISOString().split('T')[0];

const EXCLUDE_DIRS = new Set(['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko', 'css', 'js', 'images', 'config', 'docs', 'scripts', 'seo', '.git', '__pycache__', '.well-known', 'convert', 'node_modules']);
const LANG_CODES = ['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar', 'ko'];

const longTailRegex = /^(batch-convert-png-to-jpg|compress-image|compress-image-for-email|compress-image-for-website|compress-image-for-wordpress|compress-image-to-100kb|compress-image-to-200kb|compress-image-to-500kb|compress-image-to-50kb|compress-jpg-to-100kb|compress-jpg-to-200kb|extract-colors|fast-convert|image-splitter|instagram-image-splitter|image-to-base64|jpg-to-png|jpg-to-png-for-instagram|jpg-to-webp|mcp-guide|png-to-jpg|png-to-jpg-for-email|png-to-webp|png-to-webp-for-wordpress|resize-image|resize-image-for-facebook-cover|resize-image-to-1080x1080|resize-image-to-1200x630|resize-image-to-1500x500|resize-image-to-1920x1080|resize-image-to-200x200|resize-image-to-250x250|resize-image-to-300x250|resize-image-to-512x512|resize-image-to-600x600|resize-image-to-728x90|resize-image-to-800x800|split-image-into-3x3|split-image-into-4-parts|webp-to-png|webp-to-png-for-website|webp-to-jpg|avif-to-png|png-to-avif|jpg-to-avif|webp-to-avif|raw-to-jpg|raw-to-png|raw-to-webp|raw-to-avif)$/;

let xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;

function addUrl(loc, changefreq, priority) {
  xml += `  <url>\n    <loc>${loc}</loc>\n    <lastmod>${TODAY}</lastmod>\n    <changefreq>${changefreq}</changefreq>\n    <priority>${priority}</priority>\n  </url>\n`;
}

// 1. EN homepage
addUrl(`${BASE_URL}/`, 'daily', '1.0');

// 2. EN tool pages
for (const entry of fs.readdirSync(ROOT, { withFileTypes: true })) {
  if (entry.isDirectory() && !EXCLUDE_DIRS.has(entry.name)) {
    if (fs.existsSync(path.join(ROOT, entry.name, 'index.html'))) {
      if (longTailRegex.test(entry.name)) {
        addUrl(`${BASE_URL}/${entry.name}/`, 'weekly', '0.9');
      }
    }
  }
}

// 3. EN privacy policy
if (fs.existsSync(path.join(ROOT, 'privacy-policy.html'))) {
  addUrl(`${BASE_URL}/privacy-policy.html`, 'weekly', '0.9');
}

// 4. Language homepages & tool pages
for (const lang of LANG_CODES) {
  const langDir = path.join(ROOT, lang);
  if (fs.existsSync(langDir)) {
    addUrl(`${BASE_URL}/${lang}/`, 'daily', '1.0');
    for (const entry of fs.readdirSync(langDir, { withFileTypes: true })) {
      if (entry.isDirectory() && fs.existsSync(path.join(langDir, entry.name, 'index.html'))) {
        addUrl(`${BASE_URL}/${lang}/${entry.name}/`, 'weekly', '0.9');
      }
    }
  }
}

xml += `</urlset>\n`;
fs.writeFileSync(SITEMAP_FILE, xml, 'utf8');

const count = xml.split('<loc>').length - 1;
console.log(`✅ sitemap generated: ${SITEMAP_FILE}`);
console.log(`   Total URLs: ${count}`);
