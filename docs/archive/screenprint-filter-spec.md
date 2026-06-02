# screenprintfilter.com — 技术规格

## 参考站点
- Pippit.ai dot silkscreen filter: 视频版半色调网点效果
- 我们做：图片版，效果更丰富

## 核心算法：Halftone Dots（半色调网点）

### 基本原理
1. 读取图片每个像素的亮度（灰度值）
2. 将图片划分为网格（cell grid）
3. 每个格子里画一个圆点，圆点大小 = f(该区域平均灰度)
   - 越暗的区域 → 点越大（甚至连成一片）
   - 越亮的区域 → 点越小（甚至消失）
4. 白色背景，黑色网点（或其他颜色组合）

### 参数控制
| 参数 | 默认值 | 范围 | 说明 |
|---|---|---|---|
| Dot Size | 8px | 2-30px | 最大圆点直径（网格大小） |
| Dot Spacing | 1.2x | 1.0-2.0x | 点间距倍率 |
| Contrast | 50% | 0-100% | 处理前的对比度增强 |
| Brightness | 0% | -50~+50% | 处理前的亮度调整 |
| Dot Shape | circle | circle/square/diamond/line | 点形状 |
| Angle | 45° | 0-360° | 点阵旋转角度 |
| Foreground Color | #000000 | 任意 | 点的颜色 |
| Background Color | #FFFFFF | 任意 | 背景色 |
| Output Size | same | 原图/自定义 | 输出图片尺寸 |

### 可选增强功能
- **双色印刷**: 两种颜色的网点叠加（类似旧式双色印刷）
- **CMYK 四色分色**: 经典丝网印刷四色分色输出（高级模式）
- **边缘增强**: 处理前做边缘检测，保留更多细节

## 技术栈
- 纯 HTML + CSS + Canvas JS（无后端）
- 所有处理在浏览器本地完成
- Logo：复用 PicEte 的 SVG 风格，修改配色
- 部署：Vercel

## 页面结构
### 首页 (index.html)
1. 顶部：Logo + 导航
2. Hero: 标题 + 一句话描述 + 上传区域（拖拽/点击上传）
3. 效果预览区：原图 / 效果图并排对比
4. 参数控制面板（右侧或下方）
5. 下载按钮
6. 效果示例画廊（展示不同参数组合的效果图）
7. FAQ
8. Footer

### AI 友好文件
- llms.txt
- .well-known/ai-plugin.json
- .well-known/llms.txt
- head 中加 link rel

## SEO
- Google Analytics G-H72N80TEBW（跟 PicEte 共用）
- Bing Webmaster
- 页面 title + meta description 优化

## 配色方案（参考丝网印刷风格）
- 主色：黑色 + 白色（经典丝印）
- 强调色：#FF4500（橙红，丝网印刷油墨感）
- 背景：#F5F0EB（微暖白，纸张质感）
