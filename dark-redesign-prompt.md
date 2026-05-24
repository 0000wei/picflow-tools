# 任务：重新设计 PicEte 暗色模式配色

## 当前问题
picete.com 的暗色模式配色不合理：
- bg-color (#111827) 和 bg-secondary (#1F2937) 色差太小，缺乏层次感
- 暗色下 primary-color 变成紫色 (#7C3AED)，与亮色的靛蓝 (#6366F1) 不协调
- 整体颜色偏灰蓝，不够精致

## 参考目标
ilovepalette.com 的暗色模式设计理念：
- 背景更黑更深：`--bg-color: #0f1117`，`--bg-secondary: #1a1d27`
- 边框柔和：`--border-color: #2a2d3a`（比灰色更有质感）
- 用 box-shadow 代替纯色背景做 header 分隔
- 深色背景下用浅色主题色保证可读性

## 新配色方案
由于 picete 亮色是 Indigo (#6366F1) 风格，暗色应延续靛蓝调性，而非紫色：

### CSS 变量变动（只改 [data-theme="dark"] 部分，不动 :root 亮色）

| 变量 | 当前 | 新值 |
|---|---|---|
| --bg-color | #111827 | #0B1121（深靛黑） |
| --bg-secondary | #1F2937 | #141D2E（深靛蓝灰卡片） |
| --border-color | #374151 | #1E293B（深蓝灰边框） |
| --text-color | #F9FAFB | #F1F5F9（略暖的白） |
| --text-light | #D1D5DB | #94A3B8（柔灰） |
| --primary-color | #7C3AED | #818CF8（浅靛蓝，亮色 #6366F1 的浅色版） |
| --primary-dark | #6D28D9 | #6366F1（亮色主色作为暗色的-primary-dark） |
| --primary-light | #8B5CF6 | #A5B4FC（更浅靛蓝用于hover） |
| --shadow-* | dark | 参考 ilovepalette 使用 rgba(255,255,255, 0.06) 风格的阴影 |

### 具体样式调整

1. **Header**：用 box-shadow 代替背景色
   ```css
   [data-theme="dark"] .header {
       background-color: rgba(20, 29, 46, 0.8);
       box-shadow: 0 1px 0 0 #1E293B;
   }
   ```

2. **Hero 渐变**：适配新背景色
   ```css
   [data-theme="dark"] .hero {
       background: linear-gradient(180deg, var(--bg-color) 0%, rgba(11, 17, 33, 0.95) 100%);
   }
   ```

3. **Upload area / Cards**：使用 rgba 背景保持透明质感
   ```css
   [data-theme="dark"] .upload-area {
       background-color: rgba(20, 29, 46, 0.6);
       border-color: var(--border-color);
   }
   ```

4. **Input fields**：暗色输入框用深背景
   ```css
   [data-theme="dark"] .input-group input,
   [data-theme="dark"] input[type="text"],
   [data-theme="dark"] input[type="number"],
   [data-theme="dark"] select {
       background-color: #0B1121;
       border-color: #1E293B;
   }
   ```

5. **Link hover**：用 primary-light
   ```css
   [data-theme="dark"] .nav-link:hover {
       color: var(--primary-light);
   }
   ```

6. **btn-secondary hover**：使用新 border-color 方案
   ```css
   [data-theme="dark"] .btn-secondary:hover {
       background-color: rgba(30, 41, 59, 0.8);
   }
   ```

7. **footer**：使用 bg-secondary
   ```css
   [data-theme="dark"] .footer {
       background-color: var(--bg-secondary);
   }
   ```

## 需要修改的文件
只修改：`/home/wu/picete-site/css/style.css`
（第22-216行之间，[data-theme="dark"] 部分。注意这个 CSS 用了 SCSS-like 嵌套语法 `& .xxx`）

## 注意事项
1. 亮色模式（:root）完全不动
2. 不要改动 lang-switcher 的 inline 暗色样式（在各个 index.html 里单独处理）
3. 修改后验证一下 text-on-bg 的对比度足够
4. 所有改动都在 css/style.css 里的 [data-theme="dark"] 块内
