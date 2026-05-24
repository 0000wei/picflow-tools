# PicEte 暗色模式重新设计方案

## 参考：ilovepalette.com 暗色模式配色
- bg: #0f1117（极深黑底）
- bg-secondary: #1a1d27（深蓝灰色卡片）
- border: #2a2d3a（柔和边框）
- text: #F9FAFB
- text-light: #D1D5DB

## 需要修改的文件
基础 CSS：`/home/wu/picete-site/css/style.css`
这套 CSS 被所有页面共享（inline 的 lang-switcher/theme-toggle 样式在各自 index.html 中）

### 改动 1：更新 :root 和 [data-theme="dark"] 的 CSS 变量

亮色模式保留不动（用户在亮色下已经看顺了），只改暗色部分。

### 改动 2：header 暗色背景 + 边框
PicEte 当前 header 暗色是纯 bg-secondary，应改为类似 ilovepalette 的 box-shadow 效果或更柔和的背景。

### 改动 3：hero 渐变
当前的 hero 渐变太生硬，用更柔和的。

### 改动 4：tool-item / card 暗色边框更淡
当前 #374151 偏灰，改为 #2a2d3a 更柔和。

### 改动 5：暗色模式 link 颜色
.nav-link 悬停用 primary-light #818CF8。

## 新暗色方案（picete-specific）
picete 的主色调是靛蓝 Indigo (#6366F1)，暗色下应使用对应的浅靛蓝：
- primary-color: #818CF8（亮色是深靛蓝 #6366F1，暗色用浅靛蓝保证可读性）
- primary-dark: #6366F1
- primary-light: #A5B4FC

背景色方案（参考 ilovepalette 的深色设计，但保留 picete 自己的风格）：
- bg: #0B1121（极深靛黑，配合 Indigo 主题色）
- bg-secondary: #151C2D（深靛蓝灰卡片）
- border: #1E293B（深蓝灰边框）
- text: #F1F5F9
- text-light: #94A3B8

注意：有一个 inline 的 `.lang-switcher select` 暗色样式和 `.theme-toggle` 样式，确认这些也一致。

## 执行步骤
1. 修改 css/style.css 中的 [data-theme="dark"] 部分
2. 如果需要调整其他硬编码颜色

注意：不要改动亮色模式的任何 CSS 变量。
