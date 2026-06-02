# 项目 Prompt

你是一个出海建站全栈开发者，现在要创建一个图片在线工具网站。按以下要求生成。

## 网站定位
- 名称：PicFlow（图片在线处理工具）
- 核心功能：图片格式转换 + 图片缩放
- 变现方式：Adsense 广告
- 技术栈：纯 HTML/CSS/JS 静态站，可直接部署到 Vercel

## 目标关键词
目标在搜索引擎（谷歌）中获取以下关键词的排名：
- "image converter"、"image converter online"、"convert image to webp"、"png to jpg"、"webp to png"、"resize image online"、"image resizer"
- "image compressor"、"compress image online"

## SEO 要求（非常重要）
遵循哥飞出海的 SEO 原则：

1. **每个页面聚焦一个关键词**：首页聚焦 "image converter"，每个子功能页聚焦对应关键词
2. **TDH 完整**：每个页面必须写完整的 Title、Description、H1，且包含目标关键词
3. **关键词密度 3-5%**：页面正文中自然融入关键词
4. **内链网络**：每个页面底部有"其他工具"链接列表，互相链接
5. **Alt 属性**：所有图片写 Alt
6. **面包屑导航**：面包屑
7. **Sitemap**：生成 sitemap.xml
8. **robots.txt**：生成 robots.txt
9. **Schema.org 结构化数据**：在首页加入 WebApplication 结构化数据
10. **Open Graph 标签**：每个页面有 og:title、og:description

## 页面结构

### 首页 (index.html)
- 英雄区：大标题 "Online Image Converter & Resizer — Free" 和副标题
- 主要工具区（核心）：
  1. 图片上传区域（拖放 + 点击选择）
  2. 格式选择（源格式检测，目标格式下拉：PNG/JPEG/WebP/AVIF/GIF）
  3. 质量滑块（1-100）
  4. 是否调整尺寸的开关 → 展开宽度/高度输入（px），保持比例锁定
  5. "Convert" 按钮
- 预览区（转换前/后并排对比）：显示大小、尺寸对比
- 下载按钮
- 功能描述区：每个功能独立描述（对应长尾关键词）

### 子页面
为每个长尾词创建独立内页：
1. /png-to-jpg/ (index.html)
2. /jpg-to-png/ (index.html)
3. /webp-to-png/ (index.html)
4. /png-to-webp/ (index.html)
5. /jpg-to-webp/ (index.html)
6. /resize-image/ (index.html)
7. /compress-image/ (index.html)

每个子页面结构：
- H1 包含精确关键词（如 "Convert PNG to JPG Online Free"）
- 工具区（直接使用首页的转换功能，预填格式）
- 详细说明文章（300-500字，含关键词自然分布）
- 内链到其他工具页面
- FAQ 区域（用 Schema FAQ结构化数据）

### 通用布局
- 顶部导航栏：Logo + 工具分类下拉菜单 + 所有工具链接
- 内容区
- 侧边栏广告位
- 底部版权 + 隐私政策链接
- Google Analytics 代码位

## 技术实现细节

### 图片处理（用 Canvas API）
```
- 图片通过 <input type="file"> 或拖放加载到 Canvas
- 格式转换：canvas.toBlob(callback, 'image/webp', quality)
- 缩放：canvas drawImage 重新采样
- 所有处理在浏览器端完成，不上传服务器
```

### CSS 风格
- 现代极简设计
- 主色：#6366F1 紫色调
- 响应式设计（移动端优先）
- 暗色/亮色模式切换

### 广告位预留
- 工具区上方 1 个横幅
- 内容区中间 1 个内嵌
- 底部 1 个
- 使用样式占位（以后替换 Adsense 代码）

## 外部引用
- Google Fonts（Inter 字体）
- Font Awesome（图标）
- Google Analytics（占位）

## 部署要求
- 所有文件是静态的，可直接在 Vercel/Netlify 部署
- 生成 vercel.json 配置文件
- 确保所有路径是相对路径

请开始生成完整的项目。先创建目录结构，然后生成每个文件。
