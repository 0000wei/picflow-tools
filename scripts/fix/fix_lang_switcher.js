#!/usr/bin/env node

/**
 * Fix two bugs in the language switcher across all HTML files:
 *
 * 1. Regex bug: path.replace(/^\/(zh|ja|de|fr|es|pt|ar)\//, '/')
 *    → path.replace(/^\/(zh|ja|de|fr|es|pt|ar)(?:\/|$)/, '/')
 *    The original fails when the path has no trailing slash (e.g. "/zh").
 *
 * 2. Hardcoded domain: var paths = {"en":"https://picete.com/", ...}
 *    → var paths = {"en":"/", "zh":"/zh/", ...}
 *    So the switcher works in local dev, not just production.
 *
 * Idempotent — safe to run multiple times.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');

const REGEX_OLD = "path.replace(/^\\/(zh|ja|de|fr|es|pt|ar)\\//, '/')";
const REGEX_NEW = "path.replace(/^\\/(zh|ja|de|fr|es|pt|ar)(?:\\/|$)/, '/')";

const PATHS_OLD = 'var paths = {"en": "https://picete.com/", "zh": "https://picete.com/zh/", "ja": "https://picete.com/ja/", "de": "https://picete.com/de/", "fr": "https://picete.com/fr/", "es": "https://picete.com/es/", "pt": "https://picete.com/pt/", "ar": "https://picete.com/ar/"};';
const PATHS_NEW = 'var paths = {"en": "/", "zh": "/zh/", "ja": "/ja/", "de": "/de/", "fr": "/fr/", "es": "/es/", "pt": "/pt/", "ar": "/ar/"};';

function findHtmlFiles(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...findHtmlFiles(full));
    } else if (entry.name.endsWith('.html')) {
      results.push(full);
    }
  }
  return results;
}

let totalModified = 0;
let totalRegexFixes = 0;
let totalPathsFixes = 0;

const htmlFiles = findHtmlFiles(ROOT);

for (const file of htmlFiles) {
  const original = fs.readFileSync(file, 'utf8');
  let content = original;

  const hasRegex = content.includes(REGEX_OLD);
  if (hasRegex) {
    content = content.split(REGEX_OLD).join(REGEX_NEW);
    totalRegexFixes++;
  }

  const hasPaths = content.includes(PATHS_OLD);
  if (hasPaths) {
    content = content.split(PATHS_OLD).join(PATHS_NEW);
    totalPathsFixes++;
  }

  if (content !== original) {
    fs.writeFileSync(file, content, 'utf8');
    totalModified++;
    const rel = path.relative(ROOT, file);
    console.log(`Fixed: ${rel} (regex: ${hasRegex ? 1 : 0}, paths: ${hasPaths ? 1 : 0})`);
  }
}

console.log(`\nDone. ${totalModified} files modified (${totalRegexFixes} regex fixes, ${totalPathsFixes} paths fixes) out of ${htmlFiles.length} HTML files.`);
