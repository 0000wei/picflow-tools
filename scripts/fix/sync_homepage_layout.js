/**
 * sync_homepage_layout.js
 *
 * Syncs the <section id="tools"> layout from the root index.html (English)
 * to all 7 localized versions (zh, ja, de, fr, es, pt, ar).
 *
 * What it does:
 * 1. Extracts the English tools section structure (categories, ordering, quick-tags)
 * 2. Extracts translated tool names/descriptions from each locale
 * 3. Rebuilds each locale's tools section matching the English layout
 * 4. Preserves locale-specific URLs and translated text
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const LOCALES = ['zh', 'ja', 'de', 'fr', 'es', 'pt', 'ar'];

// Category title translations
const CATEGORY_TITLES = {
  en: {
    '🔥 Core & Popular': '🔥 Core & Popular',
    '🎨 Editing & Creative': '🎨 Editing & Creative',
    '🔄 Advanced Formats': '🔄 Advanced Formats',
  },
  zh: {
    '🔥 Core & Popular': '🔥 核心热门工具',
    '🎨 Editing & Creative': '🎨 编辑与创意',
    '🔄 Advanced Formats': '🔄 高级格式',
  },
  ja: {
    '🔥 Core & Popular': '🔥 人気のコアツール',
    '🎨 Editing & Creative': '🎨 編集＆クリエイティブ',
    '🔄 Advanced Formats': '🔄 高度なフォーマット',
  },
  de: {
    '🔥 Core & Popular': '🔥 Kern- & Beliebte Tools',
    '🎨 Editing & Creative': '🎨 Bearbeitung & Kreativität',
    '🔄 Advanced Formats': '🔄 Erweiterte Formate',
  },
  fr: {
    '🔥 Core & Popular': '🔥 Outils Populaires',
    '🎨 Editing & Creative': '🎨 Édition & Créativité',
    '🔄 Advanced Formats': '🔄 Formats Avancés',
  },
  es: {
    '🔥 Core & Popular': '🔥 Herramientas Populares',
    '🎨 Editing & Creative': '🎨 Edición y Creatividad',
    '🔄 Advanced Formats': '🔄 Formatos Avanzados',
  },
  pt: {
    '🔥 Core & Popular': '🔥 Ferramentas Populares',
    '🎨 Editing & Creative': '🎨 Edição e Criatividade',
    '🔄 Advanced Formats': '🔄 Formatos Avançados',
  },
  ar: {
    '🔥 Core & Popular': '🔥 الأدوات الأساسية والشائعة',
    '🎨 Editing & Creative': '🎨 التحرير والإبداع',
    '🔄 Advanced Formats': '🔄 التنسيقات المتقدمة',
  },
};

// Quick-tag label translations
const QUICKTAG_LABELS = {
  en: {
    '50KB': '50KB', '100KB': '100KB', '200KB': '200KB', '500KB': '500KB',
    'JPG to 100KB': 'JPG to 100KB', 'JPG to 200KB': 'JPG to 200KB',
    'For Email': 'For Email', 'For Website': 'For Website',
    'For WordPress': 'For WordPress',
    '1080×1080': '1080×1080', '1920×1080': '1920×1080',
    '512×512': '512×512', '800×800': '800×800',
    '1200×630': '1200×630', '300×250': '300×250',
    '600×600': '600×600', '1500×500': '1500×500',
    '200×200': '200×200', '250×250': '250×250',
    '728×90': '728×90',
    'For Instagram': 'For Instagram', 'Batch Convert': 'Batch Convert',
    'WordPress': 'WordPress',
    '3×3 Grid': '3×3 Grid', '4 Parts': '4 Parts',
  },
  zh: {
    '50KB': '50KB', '100KB': '100KB', '200KB': '200KB', '500KB': '500KB',
    'JPG to 100KB': 'JPG 100KB', 'JPG to 200KB': 'JPG 200KB',
    'For Email': '邮件', 'For Website': '网站', 'For WordPress': 'WordPress',
    '1080×1080': '1080×1080', '1920×1080': '1920×1080',
    '512×512': '512×512', '800×800': '800×800',
    '1200×630': '1200×630', '300×250': '300×250',
    '600×600': '600×600', '1500×500': '1500×500',
    '200×200': '200×200', '250×250': '250×250',
    '728×90': '728×90',
    'For Instagram': 'Instagram', 'Batch Convert': '批量转换',
    'WordPress': 'WordPress',
    '3×3 Grid': '3×3 网格', '4 Parts': '4 等分',
  },
  ja: {
    '50KB': '50KB', '100KB': '100KB', '200KB': '200KB', '500KB': '500KB',
    'JPG to 100KB': 'JPG 100KB', 'JPG to 200KB': 'JPG 200KB',
    'For Email': 'メール用', 'For Website': 'Web用', 'For WordPress': 'WordPress',
    '1080×1080': '1080×1080', '1920×1080': '1920×1080',
    '512×512': '512×512', '800×800': '800×800',
    '1200×630': '1200×630', '300×250': '300×250',
    '600×600': '600×600', '1500×500': '1500×500',
    '200×200': '200×200', '250×250': '250×250',
    '728×90': '728×90',
    'For Instagram': 'Instagram', 'Batch Convert': '一括変換',
    'WordPress': 'WordPress',
    '3×3 Grid': '3×3 グリッド', '4 Parts': '4分割',
  },
  de: {
    '50KB': '50KB', '100KB': '100KB', '200KB': '200KB', '500KB': '500KB',
    'JPG to 100KB': 'JPG 100KB', 'JPG to 200KB': 'JPG 200KB',
    'For Email': 'E-Mail', 'For Website': 'Website', 'For WordPress': 'WordPress',
    '1080×1080': '1080×1080', '1920×1080': '1920×1080',
    '512×512': '512×512', '800×800': '800×800',
    '1200×630': '1200×630', '300×250': '300×250',
    '600×600': '600×600', '1500×500': '1500×500',
    '200×200': '200×200', '250×250': '250×250',
    '728×90': '728×90',
    'For Instagram': 'Instagram', 'Batch Convert': 'Stapelkonvertierung',
    'WordPress': 'WordPress',
    '3×3 Grid': '3×3 Raster', '4 Parts': '4 Teile',
  },
  fr: {
    '50KB': '50KB', '100KB': '100KB', '200KB': '200KB', '500KB': '500KB',
    'JPG to 100KB': 'JPG 100KB', 'JPG to 200KB': 'JPG 200KB',
    'For Email': 'E-mail', 'For Website': 'Site web', 'For WordPress': 'WordPress',
    '1080×1080': '1080×1080', '1920×1080': '1920×1080',
    '512×512': '512×512', '800×800': '800×800',
    '1200×630': '1200×630', '300×250': '300×250',
    '600×600': '600×600', '1500×500': '1500×500',
    '200×200': '200×200', '250×250': '250×250',
    '728×90': '728×90',
    'For Instagram': 'Instagram', 'Batch Convert': 'Conversion par lot',
    'WordPress': 'WordPress',
    '3×3 Grid': 'Grille 3×3', '4 Parts': '4 parties',
  },
  es: {
    '50KB': '50KB', '100KB': '100KB', '200KB': '200KB', '500KB': '500KB',
    'JPG to 100KB': 'JPG 100KB', 'JPG to 200KB': 'JPG 200KB',
    'For Email': 'Email', 'For Website': 'Web', 'For WordPress': 'WordPress',
    '1080×1080': '1080×1080', '1920×1080': '1920×1080',
    '512×512': '512×512', '800×800': '800×800',
    '1200×630': '1200×630', '300×250': '300×250',
    '600×600': '600×600', '1500×500': '1500×500',
    '200×200': '200×200', '250×250': '250×250',
    '728×90': '728×90',
    'For Instagram': 'Instagram', 'Batch Convert': 'Conversión por lotes',
    'WordPress': 'WordPress',
    '3×3 Grid': 'Cuadrícula 3×3', '4 Parts': '4 partes',
  },
  pt: {
    '50KB': '50KB', '100KB': '100KB', '200KB': '200KB', '500KB': '500KB',
    'JPG to 100KB': 'JPG 100KB', 'JPG to 200KB': 'JPG 200KB',
    'For Email': 'Email', 'For Website': 'Site', 'For WordPress': 'WordPress',
    '1080×1080': '1080×1080', '1920×1080': '1920×1080',
    '512×512': '512×512', '800×800': '800×800',
    '1200×630': '1200×630', '300×250': '300×250',
    '600×600': '600×600', '1500×500': '1500×500',
    '200×200': '200×200', '250×250': '250×250',
    '728×90': '728×90',
    'For Instagram': 'Instagram', 'Batch Convert': 'Conversão em lote',
    'WordPress': 'WordPress',
    '3×3 Grid': 'Grade 3×3', '4 Parts': '4 partes',
  },
  ar: {
    '50KB': '50KB', '100KB': '100KB', '200KB': '200KB', '500KB': '500KB',
    'JPG to 100KB': 'JPG 100KB', 'JPG to 200KB': 'JPG 200KB',
    'For Email': 'البريد', 'For Website': 'الموقع', 'For WordPress': 'WordPress',
    '1080×1080': '1080×1080', '1920×1080': '1920×1080',
    '512×512': '512×512', '800×800': '800×800',
    '1200×630': '1200×630', '300×250': '300×250',
    '600×600': '600×600', '1500×500': '1500×500',
    '200×200': '200×200', '250×250': '250×250',
    '728×90': '728×90',
    'For Instagram': 'Instagram', 'Batch Convert': 'تحويل دفعي',
    'WordPress': 'WordPress',
    '3×3 Grid': 'شبكة 3×3', '4 Parts': '4 أجزاء',
  },
};

/**
 * Extract the tools section from HTML string.
 * Returns the section HTML or null.
 */
function extractToolsSection(html) {
  const match = html.match(/<section[^>]*\bid\s*=\s*["']tools["'][^>]*>[\s\S]*?<\/section>/);
  return match ? match[0] : null;
}

/**
 * Extract tool items from a tools section HTML.
 * Returns Map: slug → { icon, name, description }
 */
function extractToolItems(toolsSectionHtml) {
  const items = new Map();
  const itemRegex = /<a[^>]*class\s*=\s*["'][^"']*tool-item[^"']*["'][^>]*>([\s\S]*?)<\/a>/gi;
  let match;

  while ((match = itemRegex.exec(toolsSectionHtml)) !== null) {
    const fullLink = match[0];
    const inner = match[1];

    const hrefMatch = fullLink.match(/href\s*=\s*["']([^"']+)["']/);
    if (!hrefMatch) continue;
    const href = hrefMatch[1];

    const slug = href.replace(/^\/(zh|ja|de|fr|es|pt|ar)\//, '').replace(/\/$/, '');

    // Extract icon (emoji between div/span)
    const iconMatch = inner.match(/tool-icon[^>]*>([^<]*)/);
    const icon = iconMatch ? iconMatch[1].trim() : '';

    // Extract name (h3 text or span.tool-name)
    const nameMatch = inner.match(/tool-name[^>]*>([^<]*)/) || inner.match(/<h3[^>]*>([\s\S]*?)<\/h3>/);
    const name = nameMatch ? nameMatch[1].trim() : '';

    // Extract description (p text or span.tool-desc)
    const descMatch = inner.match(/tool-desc[^>]*>([^<]*)/) || inner.match(/<p[^>]*>([\s\S]*?)<\/p>/);
    const desc = descMatch ? descMatch[1].trim() : '';

    items.set(slug, { icon, name, description: desc });
  }

  return items;
}

/**
 * Parse English tools section to extract canonical structure.
 * Returns array of { type: 'category'|'tool', ... }
 */
function parseEnglishStructure(toolsSectionHtml) {
  const structure = [];
  // Split by category-title or tool-item links
  const categoryRegex = /<h3[^>]*class\s*=\s*["'][^"']*category-title[^"']*["'][^>]*>([\s\S]*?)<\/h3>/gi;
  const linkRegex = /<a[^>]*href\s*=\s*["']([^"']+)["'][^>]*class\s*=\s*["'][^"']*tool-item[^"']*["'][^>]*>([\s\S]*?)<\/a>/gi;

  // Build a combined index of category titles and tool items
  const elements = [];

  let catMatch;
  while ((catMatch = categoryRegex.exec(toolsSectionHtml)) !== null) {
    elements.push({
      index: catMatch.index,
      type: 'category',
      title: catMatch[1].trim(),
    });
  }

  while ((match = linkRegex.exec(toolsSectionHtml)) !== null) {
    const href = match[1];
    const inner = match[2];
    const slug = href.replace(/\/$/, '');

    // Extract icon
    const iconMatch = inner.match(/tool-icon[^>]*>([^<]*)/);
    const icon = iconMatch ? iconMatch[1].trim() : '';

    // Extract name
    const nameMatch = inner.match(/<h3[^>]*>([\s\S]*?)<\/h3>/);
    const name = nameMatch ? nameMatch[1].trim() : '';

    // Extract description
    const descMatch = inner.match(/<p[^>]*>([\s\S]*?)<\/p>/);
    const desc = descMatch ? descMatch[1].trim() : '';

    // Extract quick-tags
    const quickTags = [];
    const tagRegex = /<span[^>]*onclick\s*=\s*["'][^"']*location\.href\s*=\s*'([^']*)'[^>]*>([^<]*)<\/span>/gi;
    let tagMatch;
    while ((tagMatch = tagRegex.exec(inner)) !== null) {
      quickTags.push({
        label: tagMatch[2].trim(),
        href: tagMatch[1].replace(/\/$/, ''),
      });
    }

    elements.push({
      index: match.index,
      type: 'tool',
      slug,
      icon,
      name,
      description: desc,
      quickTags,
    });
  }

  // Sort by position in the HTML
  elements.sort((a, b) => a.index - b.index);

  return elements;
}

/**
 * Generate a tool item HTML string for a given locale.
 */
function generateToolItem(slug, localeToolInfo, enToolInfo, quickTags, locale) {
  const info = localeToolInfo || enToolInfo;
  const href = `/${locale}/${slug}/`;
  const icon = info.icon || enToolInfo.icon;
  const name = info.name || enToolInfo.name;
  const desc = info.description || enToolInfo.description;

  let html = `\t\t\t\t<a href="${href}" class="tool-item">\n`;
  html += `\t\t\t\t\t<div class="tool-icon">${icon}</div>\n`;
  html += `\t\t\t\t\t<h3>${name}</h3>\n`;
  html += `\t\t\t\t\t<p>${desc}</p>\n`;

  if (quickTags && quickTags.length > 0) {
    const labels = QUICKTAG_LABELS[locale] || QUICKTAG_LABELS.en;
    html += '\t\t\t\t\t<div class="quick-tags">\n';
    for (const tag of quickTags) {
      const label = labels[tag.label] || tag.label;
      const tagHref = `/${locale}/${tag.href}/`;
      html += `\t\t\t\t\t\t<span onclick="event.stopPropagation();location.href='${tagHref}'">${label}</span>\n`;
    }
    html += '\t\t\t\t\t</div>\n';
  }

  html += '\t\t\t\t</a>';
  return html;
}

/**
 * Generate the full tools section for a locale.
 */
function generateToolsSection(structure, localeTools, locale) {
  const categoryTitles = CATEGORY_TITLES[locale] || CATEGORY_TITLES.en;

  const lines = [];
  lines.push('\t<section id="tools" class="tools-section">');
  lines.push('\t\t<div class="container">');

  // Section title: reuse from existing locale section title if available
  const sectionTitle = localeTools._sectionTitle || 'Professional Image Tools';
  lines.push(`\t\t\t<h2 class="section-title">${sectionTitle}</h2>`);
  lines.push('\t\t\t<div class="tools-grid">');

  for (const el of structure) {
    if (el.type === 'category') {
      const title = categoryTitles[el.title] || el.title;
      lines.push(`\t\t\t\t<h3 class="category-title">${title}</h3>`);
    } else if (el.type === 'tool') {
      const toolInfo = localeTools.get(el.slug);
      lines.push(generateToolItem(el.slug, toolInfo, el, el.quickTags, locale));
    }
  }

  lines.push('\t\t\t</div>');
  lines.push('\t\t</div>');
  lines.push('\t</section>');

  return lines.join('\n');
}

/**
 * Extract section title from a tools section.
 */
function extractSectionTitle(toolsSectionHtml) {
  const match = toolsSectionHtml.match(/<h2[^>]*class\s*=\s*["'][^"']*section-title[^"']*["'][^>]*>([\s\S]*?)<\/h2>/);
  return match ? match[1].trim() : null;
}

// --- Main ---

function main() {
  console.log('=== sync_homepage_layout.js ===\n');

  // 1. Read English root index.html
  const enPath = path.join(ROOT, 'index.html');
  const enHtml = fs.readFileSync(enPath, 'utf-8');
  const enToolsSection = extractToolsSection(enHtml);

  if (!enToolsSection) {
    console.error('ERROR: Could not find <section id="tools"> in root index.html');
    process.exit(1);
  }

  console.log('Extracted English tools section (' + enToolsSection.length + ' chars)');

  // 2. Parse English structure
  const enStructure = parseEnglishStructure(enToolsSection);
  const categories = enStructure.filter(e => e.type === 'category');
  const tools = enStructure.filter(e => e.type === 'tool');
  console.log(`Found ${categories.length} categories, ${tools.length} tools`);

  // 3. Process each locale
  for (const locale of LOCALES) {
    const localePath = path.join(ROOT, locale, 'index.html');
    if (!fs.existsSync(localePath)) {
      console.warn(`SKIP: ${locale}/index.html not found`);
      continue;
    }

    const localeHtml = fs.readFileSync(localePath, 'utf-8');
    const localeToolsSection = extractToolsSection(localeHtml);

    if (!localeToolsSection) {
      console.warn(`SKIP: No <section id="tools"> in ${locale}/index.html`);
      continue;
    }

    // Extract existing translated tool info
    const localeToolItems = extractToolItems(localeToolsSection);
    const sectionTitle = extractSectionTitle(localeToolsSection);
    if (sectionTitle) {
      localeToolItems._sectionTitle = sectionTitle;
    }

    console.log(`\n[${locale}] Found ${localeToolItems.size} existing tool items`);

    // Generate new tools section
    const newToolsSection = generateToolsSection(enStructure, localeToolItems, locale);

    // Replace old tools section in locale HTML
    const newHtml = localeHtml.replace(
      /<section[^>]*\bid\s*=\s*["']tools["'][^>]*>[\s\S]*?<\/section>/,
      newToolsSection
    );

    if (newHtml === localeHtml) {
      console.warn(`[${locale}] WARNING: No replacement occurred`);
      continue;
    }

    fs.writeFileSync(localePath, newHtml, 'utf-8');
    console.log(`[${locale}] Updated ${localePath}`);
  }

  console.log('\nDone!');
}

main();
