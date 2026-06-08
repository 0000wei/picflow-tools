/**
 * Sync footer across all language homepages.
 * EN footer is the canonical structure; lang footers get rebuilt
 * with translated texts extracted from their existing files.
 */
const fs = require('fs');
const path = require('path');

const rootDir = path.join(__dirname, '..', '..');
const langs = ['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar'];

// Canonical tool slugs from EN footer (source of truth)
const tools = {
  conversion: [
    'png-to-jpg', 'jpg-to-png', 'webp-to-png', 'png-to-webp',
    'jpg-to-webp', 'fast-convert', 'avif-to-png', 'png-to-avif',
    'jpg-to-avif', 'webp-to-avif', 'raw-to-jpg', 'raw-to-png',
    'raw-to-webp', 'raw-to-avif'
  ],
  editing: [
    'resize-image', 'compress-image', 'image-splitter',
    'extract-colors', 'image-to-base64'
  ]
};

const enText = {
  'png-to-jpg': 'PNG to JPG', 'jpg-to-png': 'JPG to PNG',
  'webp-to-png': 'WebP to PNG', 'png-to-webp': 'PNG to WebP',
  'jpg-to-webp': 'JPG to WebP', 'fast-convert': 'Fast Image Converter',
  'avif-to-png': 'AVIF to PNG', 'png-to-avif': 'PNG to AVIF',
  'jpg-to-avif': 'JPG to AVIF', 'webp-to-avif': 'WebP to AVIF',
  'raw-to-jpg': 'RAW to JPG', 'raw-to-png': 'RAW to PNG',
  'raw-to-webp': 'RAW to WebP', 'raw-to-avif': 'RAW to AVIF',
  'resize-image': 'Image Resizer', 'compress-image': 'Image Compressor',
  'image-splitter': 'Image Grid Splitter', 'extract-colors': 'Color Palette Extractor',
  'image-to-base64': 'Image to Base64',
  'privacy-policy': 'Privacy Policy', 'mcp-guide': 'MCP Guide'
};

function extractLinkMap(footerHtml) {
  const map = {};
  const re = /<a\s[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/g;
  let m;
  while ((m = re.exec(footerHtml)) !== null) {
    const href = m[1];
    const text = m[2].trim();
    let slug = href.replace(/^\.\.\//, '').replace(/^\//, '').replace(/\/$/, '').replace(/\.html$/, '');
    slug = slug.replace(/^(zh|ja|de|fr|es|pt|ar)\//, '');
    if (!map[slug]) map[slug] = text;
  }
  return map;
}

function extractLogoDesc(footerHtml) {
  const m = footerHtml.match(/<p>([^<]+)<\/p>/);
  return m ? m[1].trim() : 'Professional online image processing tools';
}

function extractCopyright(footerHtml) {
  const m = footerHtml.match(/<div class="footer-bottom">[\s\S]*?<p>([\s\S]*?)<\/p>/);
  return m ? m[1].trim() : '&copy; 2024 PicEte. All rights reserved.';
}

function extractHeaders(footerHtml) {
  const headers = [];
  const re = /<h4[^>]*>([^<]+)<\/h4>/g;
  let m;
  while ((m = re.exec(footerHtml)) !== null) {
    headers.push(m[1].trim());
  }
  return headers;
}

function toolLink(lang, slug, linkMap) {
  const text = linkMap[slug] || enText[slug] || slug;
  if (slug === 'privacy-policy') {
    return `<li><a href="/privacy-policy.html">${text}</a></li>`;
  }
  return `<li><a href="/${lang}/${slug}/">${text}</a></li>`;
}

function buildFooter(lang, linkMap, logoDesc, copyright, headers) {
  const convHeader = headers[0] || 'Image Conversion';
  const editHeader = headers[1] || 'Image Editing';
  const aboutHeader = headers[2] || 'About';
  const link = (slug) => toolLink(lang, slug, linkMap);

  let lines = [
    '    <footer class="footer">',
    '        <div class="container">',
    '            <div class="footer-content">',
    '                <div class="footer-section">',
    `                    <img src="/images/picete-logo.svg" alt="PicEte" class="footer-logo" loading="lazy" width="101" height="28">`,
    `                    <p>${logoDesc}</p>`,
    '                </div>',
    '                <div class="footer-section">',
    `                    <h4>${convHeader}</h4>`,
    '                    <ul>',
    ...tools.conversion.map(s => `                        ${link(s)}`),
    '                    </ul>',
    '                </div>',
    '                <div class="footer-section">',
    `                    <h4>${editHeader}</h4>`,
    '                    <ul>',
    ...tools.editing.map(s => `                        ${link(s)}`),
    '                    </ul>',
    '                </div>',
    '                <div class="footer-section">',
    `                    <h4>${aboutHeader}</h4>`,
    '                    <ul>',
    `                        ${link('privacy-policy')}`,
    `                        ${link('mcp-guide')}`,
    '                    </ul>',
    '                </div>',
    '            </div>',
    '            <div class="footer-bottom">',
    `                <p>${copyright}</p>`,
    '            </div>',
    '            <div style="text-align:center;padding:8px 0;font-size:12px;color:#666;border-top:1px solid #eee">',
    '                <a href="https://www.aitoolzdir.com" target="_blank" style="color:#666;text-decoration:none">AI Toolz Dir</a>',
    '            </div>',
    '        </div>',
    '    </footer>',
  ];
  return lines.join('\n');
}

for (const lang of langs) {
  const langPath = path.join(rootDir, lang, 'index.html');
  if (!fs.existsSync(langPath)) {
    console.log(`Skipping ${lang}: file not found`);
    continue;
  }

  const langHtml = fs.readFileSync(langPath, 'utf8');
  const footerMatch = langHtml.match(/<footer class="footer">[\s\S]*?<\/footer>/);
  if (!footerMatch) {
    console.log(`Skipping ${lang}: footer not found`);
    continue;
  }

  const linkMap = extractLinkMap(footerMatch[0]);
  const logoDesc = extractLogoDesc(footerMatch[0]);
  const copyright = extractCopyright(footerMatch[0]);
  const headers = extractHeaders(footerMatch[0]);

  console.log(`\n${lang}: headers=[${headers.join(', ')}] links=${Object.keys(linkMap).length}`);

  const newFooter = buildFooter(lang, linkMap, logoDesc, copyright, headers);
  const newHtml = langHtml.replace(/<footer class="footer">[\s\S]*?<\/footer>/, newFooter);

  fs.writeFileSync(langPath, newHtml, 'utf8');
  console.log(`  Updated!`);
}

console.log('\nDone!');
