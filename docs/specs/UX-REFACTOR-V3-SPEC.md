# SPEC: 首页 UX 架构升级 (UX-REFACTOR-V3)

## 1. 目标与背景
当前的首页存在信息过载、层级扁平、长尾工具曝光率极低的问题。本次 V3 架构升级的目的是通过模块化分类、引入“快速预设标签（Quick Tags）”，优化用户体验和点击转化率。

## 2. 核心页面结构调整

### 2.1 Hero 区域优化
保留当前的顶端综合上传区域，但为其增加简短提示，明确其为“全能处理工作台（All-in-one Editor）”。

### 2.2 工具网格（Tools Grid）分类重构
将原先扁平的 19 个核心工具分为三大视觉区块（使用二级标题 `<h3 class="category-title">` 隔开）：

**区块 A：🔥 核心与热门工具 (Core & Popular)**
1. 🚀 快速转换器 (Fast Convert)
2. 🗜️ 图片压缩 (Compress Image)
3. 📏 调整大小 (Resize Image)
4. 📐 PNG 转 JPG
5. 🖼️ JPG 转 PNG

**区块 B：🎨 图像编辑与创意 (Editing & Creative)**
1. 🧩 图片网格分割 (Image Splitter)
2. 🎨 调色板提取 (Extract Colors)
3. 📦 转 Base64 (Image to Base64)
4. 🖼️ Facebook 封面裁剪 (Resize for Facebook Cover)

**区块 C：🔄 高级格式转换 (Advanced Formats)**
1. WebP 系列 (WebP to PNG, PNG/JPG to WebP)
2. AVIF 系列 (4个工具)
3. RAW 系列 (4个工具)

### 2.3 唤醒沉睡的长尾工具（Quick Tags）
不再将 25 个长尾工具埋在 Footer 中。我们将采用**快捷标签 (Quick Tags)** 的方式，将它们挂载在对应的“母工具”卡片内部。

**样式参考：**
```html
<a href="compress-image/" class="tool-item">
    <div class="tool-icon">🗜️</div>
    <h3>图片压缩</h3>
    <p>减小文件大小</p>
    <div class="quick-tags">
        <span onclick="location.href='compress-image-to-50kb/'; event.preventDefault();">50KB</span>
        <span onclick="location.href='compress-image-to-100kb/'; event.preventDefault();">100KB</span>
    </div>
</a>
```
*(需通过 CSS 添加 `.category-title` 和 `.quick-tags` 的现代化样式，例如带圆角、悬浮高亮的微缩按钮)*

### 2.4 Footer 精简规范
- 移除 Footer 庞大且多余的“More Tools”栏目，使 Footer 回归简洁（保留 转换、编辑、关于、友情链接 四列）。
- 确保这套 Footer 在所有 8 种语言中完全对齐同步（通过后续的 `sync_footer_tools.js` 实现）。

## 3. 实施路径 (Harness Engineering)
1. 设计并编写 CSS 样式更新（修改 `css/style.css`）。
2. 更新英文版 `index.html`，完成 DOM 结构调整。
3. 编写 `scripts/fix/sync_homepage_layout.js` 自动化脚本，根据英文版 DOM 结构，通过匹配提取各语言的翻译标题，自动生成并覆盖全站 8 个首页，保证多语言完全同步。
