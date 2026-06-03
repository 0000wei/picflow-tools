#!/usr/bin/env bash
# ============================================================
# generate-sitemap.sh — auto-generate sitemap.xml for PicEte
#
# Scans root-level tool directories (those with index.html),
# and all 7 language mirrors (zh/ ja/ de/ fr/ es/ pt/ ar/).
# Outputs to seo/sitemap.xml
# ============================================================
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SITEMAP_FILE="${PROJECT_ROOT}/seo/sitemap.xml"
BASE_URL="https://picete.com"
TODAY="$(date +%Y-%m-%d)"

# Directories to exclude at root level
EXCLUDE_DIRS="zh|ja|de|fr|es|pt|ar|css|js|images|config|docs|scripts|seo|.git|__pycache__|.well-known|convert"

# Language codes (7 languages)
LANG_CODES="zh ja de fr es pt ar"

# Start XML
cat > "${SITEMAP_FILE}" << XMLHEADER
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
XMLHEADER

# ----------------------------------------------------------
# 1. EN homepage
# ----------------------------------------------------------
cat >> "${SITEMAP_FILE}" << EOF
  <url>
    <loc>${BASE_URL}/</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
EOF

# ----------------------------------------------------------
# 2. EN tool pages — directories with index.html at root level
#    (excluding language dirs and other non-tool dirs)
# ----------------------------------------------------------
for dir in "${PROJECT_ROOT}"/*/; do
  dirname="$(basename "${dir}")"
  # Skip if in exclude list or if no index.html
  echo "${dirname}" | grep -qE "^(css|js|images|config|docs|scripts|seo|.git|__pycache__|.well-known|convert|zh|ja|de|fr|es|pt|ar)$" && continue
  [ -f "${dir}/index.html" ] || continue

  # Check if it's a long-tail page (has hyphens beyond the base tool name pattern)
  # Base tools: single-purpose tools
  # Long-tail: more specific variants
  case "${dirname}" in
    batch-convert-png-to-jpg|compress-image|compress-image-for-email|compress-image-for-website|compress-image-for-wordpress|compress-image-to-100kb|compress-image-to-200kb|compress-image-to-500kb|compress-image-to-50kb|compress-jpg-to-100kb|compress-jpg-to-200kb|extract-colors|image-splitter|image-to-base64|jpg-to-png|jpg-to-png-for-instagram|jpg-to-webp|mcp-guide|png-to-jpg|png-to-jpg-for-email|png-to-webp|png-to-webp-for-wordpress|resize-image|resize-image-for-facebook-cover|resize-image-to-1080x1080|resize-image-to-1200x630|resize-image-to-1500x500|resize-image-to-1920x1080|resize-image-to-200x200|resize-image-to-250x250|resize-image-to-300x250|resize-image-to-512x512|resize-image-to-600x600|resize-image-to-728x90|resize-image-to-800x800|split-image-into-3x3|split-image-into-4-parts|webp-to-png|webp-to-png-for-website)
      cat >> "${SITEMAP_FILE}" << EOF
  <url>
    <loc>${BASE_URL}/${dirname}/</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
EOF
      ;;
  esac
done

# ----------------------------------------------------------
# 3. EN privacy-policy (static page at root)
# ----------------------------------------------------------
if [ -f "${PROJECT_ROOT}/privacy-policy.html" ]; then
  cat >> "${SITEMAP_FILE}" << EOF
  <url>
    <loc>${BASE_URL}/privacy-policy.html</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
EOF
fi

# ----------------------------------------------------------
# 4. Language homepages and mirrored tool pages
# ----------------------------------------------------------
for lang in ${LANG_CODES}; do
  lang_dir="${PROJECT_ROOT}/${lang}"
  [ -d "${lang_dir}" ] || continue

  # Language homepage
  cat >> "${SITEMAP_FILE}" << EOF
  <url>
    <loc>${BASE_URL}/${lang}/</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
EOF

  # Language tool subdirectories
  for dir in "${lang_dir}"/*/; do
    [ -f "${dir}/index.html" ] || continue
    subdir="$(basename "${dir}")"
    cat >> "${SITEMAP_FILE}" << EOF
  <url>
    <loc>${BASE_URL}/${lang}/${subdir}/</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
EOF
  done
done

# ----------------------------------------------------------
# Close XML
# ----------------------------------------------------------
echo "</urlset>" >> "${SITEMAP_FILE}"

# Count URLs
URL_COUNT=$(grep -c '<loc>' "${SITEMAP_FILE}")
echo "✅ sitemap generated: ${SITEMAP_FILE}"
echo "   Total URLs: ${URL_COUNT}"
