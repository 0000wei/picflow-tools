# Task 0.6.3: OG 图片国际化检查

## 项目
PicEte -- 纯静态图片工具站 (picete.com)

## 评估结果

### 当前状态
所有 400 个页面（EN + 7 语言）的 og:image 都指向同一张：
`https://picete.com/images/og-image.png`

og-image.png 为 1200×630px，20KB PNG。

### 决策：不需要多语言 OG 图片

理由：
1. **平台行为：** Facebook / Twitter / WhatsApp / Telegram 等社交平台**不翻译 OG 图片中的文本**。即使为各语言生成各自的 og-image，平台显示的还是原始图片内容。
2. **图片内容：** 当前 og-image.png 仅包含 PicEte logo + 品牌名，无需要翻译的文本。多语言版无法提供额外价值。
3. **标准做法：** 主流网站（如 Vercel / Notion / Linear）均使用单一 OG 图片覆盖所有语言版本。
4. **性能：** 使用同一张图片避免额外 7 × 20KB = 140KB 的图片存储和 CDN 缓存分摊。

### 不做
- 不修改任何 HTML 文件中的 og:image 标签
- 不生成多语言 OG 图片

### 验证
grep "og:image" /home/wu/桌面/knowledge-base/06项目/哥飞建站/picete/index.html
→ https://picete.com/images/og-image.png
