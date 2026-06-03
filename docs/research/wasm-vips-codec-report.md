# wasm-vips Codec Support Report

> **Date:** 2026-06-03
> **Package:** wasm-vips v0.0.17
> **libvips version:** 8.18.1
> **Test script:** `scripts/test/codec-test.mjs`

---

## Summary

| Aspect | Status | Detail |
|--------|--------|--------|
| **AVIF** | ✅ **Supported** | Encode + decode via libheif (AV1 codec) |
| **RAW (Camera RAW)** | ❌ **Not supported** | libraw NOT compiled into WASM bundle |
| **HEIC (HEVC/H.265)** | ❌ **Not supported** | libheif compiled without HEVC encoder |
| **JPEG-XL** | ✅ **Supported** | Via `vips-jxl.wasm` dynamic module |
| **SVG** | ✅ **Config says supported** | Via `vips-resvg.wasm` dynamic module (test decode failed — may need SVG file path load) |

---

## AVIF — Detailed Findings

- **AVIF encode:** ✅ Works via `image.writeToBuffer('.avif')` — encodes with AV1 compression
- **AVIF decode:** ✅ Works — encoded AVIF buffer can be decoded back via `Image.newFromBuffer()`
- **Output size:** 10.2 KB (800×600 test photo) — significantly smaller than JPEG (35.1 KB) or WebP (27.9 KB)
- **Encode time:** ~4 seconds (AV1 encoding is slow in WASM)
- **Backend:** libheif (loaded from `vips-heif.wasm` dynamic module)

## RAW (Camera RAW) — Detailed Findings

| Format | Extension | Status | Notes |
|--------|-----------|--------|-------|
| Canon RAW | `.cr2` | ❌ | libraw=false in vips.config() |
| Nikon RAW | `.nef` | ❌ | libraw=false in vips.config() |
| Sony RAW | `.arw` | ❌ | libraw=false in vips.config() |
| Adobe DNG | `.dng` | ❌ | libraw=false in vips.config() |
| Panasonic RAW | `.rw2` | ❌ | libraw=false in vips.config() |
| Olympus RAW | `.orf` | ❌ | libraw=false in vips.config() |

**Root cause:** The wasm-vips Emscripten build excluded `libraw` to reduce WASM bundle size. `vips.config()` explicitly shows `"RAW load with libraw: false"`.

**Impact:** Camera RAW formats (CR2, NEF, ARW, DNG, RW2, ORF) **cannot be loaded or decoded** by the WASM bundle. Users would need client-side RAW decoding via other libraries (e.g., `dcraw` or `raw.js` in-browser) before passing decoded pixel data to wasm-vips.

---

## Full Format Support Table

| Format | Encode | Decode | Size (800×600) | Time | Notes |
|--------|--------|--------|----------------|------|-------|
| JPEG | ✅ | ✅ | 35.1 KB | 939 ms | libjpeg |
| PNG | ✅ | ✅ | 723.7 KB | 155 ms | libpng |
| WebP | ✅ | ✅ | 27.9 KB | 146 ms | libwebp |
| AVIF | ✅ | ✅ | 10.2 KB | 4026 ms | libheif (AV1), slow |
| TIFF | ✅ | ✅ | 1406.5 KB | 6 ms | libtiff-4, uncompressed |
| BMP | ❌ | — | — | — | BMP save not compiled in |
| GIF | ✅ | — | 289.7 KB | 792 ms | cgif for save |
| HEIC (HEVC) | ❌ | — | — | — | libheif without HEVC encoder |
| JPEG-XL | ✅ | ✅ | 28.9 KB | 1018 ms | vips-jxl.wasm dynamic mod. |
| SVG (resvg) | — | ✅ (config) | — | — | vips-resvg.wasm loaded |
| ICO | ❌ | — | — | — | Not supported |
| PDF | — | ❌ | — | — | pdfium/poppler not compiled |
| CR2 (RAW) | — | ❌ | — | — | libraw=false |
| NEF (RAW) | — | ❌ | — | — | libraw=false |
| ARW (RAW) | — | ❌ | — | — | libraw=false |
| DNG (RAW) | — | ❌ | — | — | libraw=false |
| RW2 (RAW) | — | ❌ | — | — | libraw=false |
| ORF (RAW) | — | ❌ | — | — | libraw=false |

---

## WASM Dynamic Module Layout

The wasm-vips package uses Emscripten dynamic linking to load codec support on demand:

| WASM File | Size | Purpose |
|-----------|------|---------|
| `vips.wasm` | 5.9 MB | Core libvips + basic codecs (JPEG, PNG, TIFF, WebP, GIF) |
| `vips-heif.wasm` | 4.7 MB | HEIC/AVIF load/save via libheif |
| `vips-jxl.wasm` | 2.3 MB | JPEG-XL load/save via libjxl |
| `vips-resvg.wasm` | 1.5 MB | SVG load via resvg |

The dynamic modules are loaded automatically on vips initialization:
```javascript
n.dynamicLibraries = ["vips-jxl.wasm", "vips-heif.wasm"];
```

---

## Recommendations for PicEte

1. **AVIF is fully usable** — implement AVIF encode/decode in PicEte (consider slow encode time: ~4s for 800×600)
2. **RAW is NOT available** — remove RAW-related features from the UI or implement client-side RAW decoding separately
3. **HEIC (iPhone photos)** — not supported for decode; users must convert to JPEG/PNG before uploading
4. **JPEG-XL is available** — can be offered as an output format
5. **SVG load needs further testing** — may need file-based loading instead of buffer-based

---

## Test Validation

To reproduce:
```bash
node scripts/test/codec-test.mjs
```

Expected output last 20 lines:
```
[5] Summary:

  AVIF:
    Encode: ✅  (via libheif AV1 encoder — size: 10458 bytes)
    Decode: ✅  (encode-then-decode cycle)
  RAW (Camera RAW formats):
    ❌ ALL RAW formats unsupported — libraw was NOT compiled into the WASM bundle.
       vips.config() confirms: "RAW load with libraw: false"
       Affected formats: .cr2, .nef, .arw, .dng, .rw2, .orf
...
```
