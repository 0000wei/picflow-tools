# SPEC - Lighthouse/CDP 诊断问题修复

## 概述
通过 CDP 模式对 picete.com 进行了系统测试，发现 4 项核心问题，其中最致命的是 JS 报错阻断了 Google Analytics 的加载。本阶段必须严格按照 Harness Engineering 方法执行。

## Task 1: 修复 cookie-consent.js 致命报错
- **目标**：修复因为 `<head>` 加载时 `document.body` 为 null 导致的异常。
- **验证**：修改后，`init` 中的 `showBanner` 必须等待 `DOMContentLoaded`。不应污染其他代码。
- **I/S/V/Scope/L 审计**：修改完毕后验证功能。

## Task 2: 修复 Favicon 404
- **目标**：将 `seo/favicon.ico` 和 `seo/favicon.svg` 复制到根目录。
- **约束**：保留 `seo/` 下的原文件备份。

## Task 3: 编写并执行 fix_logos.js 批量替换
- **目标**：向全站 HTML（约 383 页）的 `logo-img` 和 `footer-logo` 注入 `width` 和 `height` 以解决 CLS/Unsized Images 警告。
- **约束**：脚本必须放置在 `scripts/fix/fix_logos.js`！执行替换后确保 `width="116" height="32"` 和 `width="101" height="28"` 注入正确且无重复。

## Task 4: 修复 CSS 对比度
- **目标**：解决 Lighthouse 的 Color Contrast 警告。
- **约束**：修改 `css/style.css`，调整 `--primary-color` 为 `#4F46E5`，`--primary-dark` 为 `#4338CA`。
