#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');

function findHtmlFiles(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === 'scripts' || entry.name === 'config' || entry.name === 'docs') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...findHtmlFiles(full));
    } else if (entry.name.endsWith('.html')) {
      results.push(full);
    }
  }
  return results;
}

const htmlFiles = findHtmlFiles(ROOT);
let totalModified = 0;

for (const file of htmlFiles) {
  const original = fs.readFileSync(file, 'utf8');
  let content = original;

  // 1. var names
  content = content.replace(
    /"ar":\s*"العربية"\s*}/g,
    '"ar":"العربية","ko":"한국어"}'
  );

  // 2. <option value="ar">
  if (!content.includes('<option value="ko">')) {
    content = content.replace(
      /(<option\s+value="ar"[^>]*>العربية<\/option>)/g,
      '$1\n            <option value="ko">한국어</option>'
    );
  }

  // 3. var paths
  content = content.replace(
    /"ar":\s*"\/ar\/"\s*}/g,
    '"ar": "/ar/", "ko": "/ko/"}'
  );

  // 4. path.replace regex
  content = content.replace(
    "path.replace(/^\\/(zh|ja|de|fr|es|pt|ar)(?:\\/|$)/, '/')",
    "path.replace(/^\\/(zh|ja|de|fr|es|pt|ar|ko)(?:\\/|$)/, '/')"
  );

  // 5. hreflang tag
  if (!content.includes('hreflang="ko"')) {
    const arLinkMatch = content.match(/<link[^>]*hreflang="ar"[^>]*>/);
    if (arLinkMatch) {
      const arLink = arLinkMatch[0];
      const koLink = arLink.replace('hreflang="ar"', 'hreflang="ko"').replace('/ar/', '/ko/');
      content = content.replace(arLink, arLink + '\n    ' + koLink);
    }
  }

  if (content !== original) {
    fs.writeFileSync(file, content, 'utf8');
    totalModified++;
    console.log(`Updated: ${path.relative(ROOT, file)}`);
  }
}

console.log(`\nDone. ${totalModified} files updated out of ${htmlFiles.length}.`);
