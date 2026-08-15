# PicEte - Free Online Image Tools

[![PicEte Screenshot](https://picete.com/og-image.png)](https://picete.com/)

**PicEte** is a free online image processing toolkit. Convert, resize, compress, and edit images directly in your browser — no upload required.

## ✨ Features

- **Format Converter** — PNG ↔ JPG, WebP ↔ PNG, JPG ↔ WebP, WebP ↔ JPG
- **Image Resizer** — Resize to any dimensions
- **Image Compressor** — Reduce file size while keeping quality
- **Image Grid Splitter** — Split images into grid tiles
- **Color Palette Extractor** — Extract colors from any image
- **Image to Base64** — Convert images to base64 strings
- **AVIF Converter** — Convert between AVIF, PNG, JPG, and WebP formats
- **RAW Photo Converter** — Convert camera RAW files (CR2, NEF, ARW, DNG) to JPG, PNG, WebP, and AVIF
- **Fast Image Converter** — One-click batch convert, resize, and compress

## 🔒 Privacy First

All processing happens locally in your browser using wasm-vips (libvips compiled to WebAssembly with libheif, libraw, and libjxl). Your images never leave your device.

## 🌐 Multi-Language

Available in 8 languages: 中文 (zh), 日本語 (ja), Deutsch (de), Français (fr), Español (es), Português (pt), العربية (ar), 한국어 (ko). Language selection is user-driven, no automatic redirect — SEO-friendly.

## 🚀 Live Demo

[https://picete.com/](https://picete.com/)

## 📦 Tech Stack

Vanilla JavaScript, HTML5 Canvas, wasm-vips (libvips + libheif + libraw WebAssembly), no frameworks.

## 📂 Project Structure (Harness Engineering)

This project strictly follows the Harness Engineering methodology:
- `config/`: Configuration files and rules (e.g., `feature_list.json`).
- `docs/`: Project documentation, specifications (`specs/`), and reports (`reports/`).
- `scripts/`: Maintenance, build, and test scripts.
- `seo/`: SEO-related assets and generators.
- `js/lib/`: WebAssembly binaries and loader scripts.
- `{lang}/`: Localized pages for each supported language.
