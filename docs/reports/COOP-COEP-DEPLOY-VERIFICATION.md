# COOP/COEP 部署验证报告

> 日期: 2026-06-03
> 项目: PicEte (picete.com)
> 目的: 验证 wasm-vips 所需的 COOP/COEP HTTP 头在 Vercel 上的可用性

---

## 一、执行过程

| Task | 内容 | 结果 |
|------|------|------|
| D.1 | 修正 vercel.json 配置语法 | ✅ Vercel 兼容的 regex pattern |
| D.2 | push 到 GitHub 触发 Vercel 部署 | ✅ 多次 push + 空 commit 强制重部署 |
| D.3 | curl 验证线上 COOP/COEP header | ✅ 13/13 工具页全通过 |
| D.4 | 验证根因——之前配置不生效的原因 | ✅ **移除 builds 配置后生效** |
| D.5 | 第三方资源兼容性审计 | ✅ 仅 GA 需处理 |

---

## 二、验证结果

### COOP/COEP Header 覆盖

| 页面 | COOP | COEP | 说明 |
|------|------|------|------|
| `/resize-image` | ✅ same-origin | ✅ require-corp | 13 个工具页全覆盖 |
| `/compress-image` | ✅ same-origin | ✅ require-corp | |
| `/png-to-jpg` | ✅ same-origin | ✅ require-corp | |
| `/jpg-to-png` | ✅ same-origin | ✅ require-corp | |
| `/webp-to-png` | ✅ same-origin | ✅ require-corp | |
| `/png-to-webp` | ✅ same-origin | ✅ require-corp | |
| `/jpg-to-webp` | ✅ same-origin | ✅ require-corp | |
| `/image-splitter` | ✅ same-origin | ✅ require-corp | |
| `/extract-colors` | ✅ same-origin | ✅ require-corp | |
| `/image-to-base64` | ✅ same-origin | ✅ require-corp | |
| `/batch-convert-png-to-jpg` | ✅ same-origin | ✅ require-corp | |
| `/split-image-into-3x3` | ✅ same-origin | ✅ require-corp | |
| `/split-image-into-4-parts` | ✅ same-origin | ✅ require-corp | |
| `/`（首页） | ❌ 无 | ❌ 无 | 正确——首页不需要 WASM |
| `/mcp-guide` | ❌ 无 | ❌ 无 | 正确——文档页不需要 WASM |

---

## 三、之前配置不生效的根因

**根因：vercel.json 中的 builds 配置与 headers 配置冲突。**

之前 vercel.json 包含了显式的 `builds` 配置：
```json
"builds": [
  { "src": "**/*.html", "use": "@vercel/static" },
  ...
]
```

当显式声明 `@vercel/static` builder 时，Vercel 采用静态文件托管模式，**不处理 vercel.json 中的 headers 配置**。

**解决方案：移除 builds 配置，让 Vercel 自动检测站点类型。**

```json
{
  "version": 2,
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(resize-image|compress-image|...工具列表...)(/.*)?",
      "headers": [
        { "key": "Cross-Origin-Opener-Policy", "value": "same-origin" },
        { "key": "Cross-Origin-Embedder-Policy", "value": "require-corp" }
      ]
    }
  ]
}
```

**关键配置参数：**
- `cleanUrls: true` — 移除 `.html` 扩展名，标准化 URL
- `trailingSlash: false` — 移除尾部斜杠，避免 308 跳转中丢失 header
- source regex 使用 `(/.*)?` 后缀匹配 `resize-image`、`resize-image/` 和 `resize-image/index.html`

---

## 四、第三方资源兼容性审计

### 当前页面加载的外部资源

| 资源 | URL | 状态 | 说明 |
|------|-----|------|------|
| Google Analytics | `www.googletagmanager.com/gtag/js` | ⚠️ 需处理 | COEP require-corp 会阻塞第三方脚本 |
| 跨站 Footer 链接 | `ilovepalette.com`, `mockupshot.online` | ✅ 安全 | 只是 `<a>` 链接，不加载资源 |
| 同站 hreflang 链接 | `picete.com/zh/...` 等 | ✅ 安全 | 同源 |

### GA 解决方案

**方案 A（推荐）：自托管 GA 脚本**
```bash
curl -o js/gtag.js https://www.googletagmanager.com/gtag/js?id=G-H72N80TEBW
```
将工具页中的 `src="https://www.googletagmanager.com..."` 改为 `src="/js/gtag.js"`
- 优点：完全同源，COEP 兼容
- 缺点：需定期更新 gtag.js

**方案 B：仅在首页保留 GA**
- 首页无 COEP，GA 正常工作
- 工具页不加载 GA

---

## 五、wasm-vips 浏览器端可行性结论

| 维度 | 状态 | 说明 |
|------|------|------|
| COOP/COEP Header | ✅ **已验证可行** | Vercel 静态站点支持 |
| SAB 可用性 | ✅ 由 COOP/COEP 自动启用 | 浏览器收到 header 后自动开启 |
| GA 兼容性 | ⚠️ 需解决 | 建议 GA 脚本自托管 |
| 首页不受影响 | ✅ 首页无 COEP | 首页不加载 WASM，不需要隔离 |

**结论：可以推进 Phase 0.2（wasm-vips 渐进替换），但需先处理 GA 自托管。**

---

*报告位置: `picete/docs/reports/COOP-COEP-DEPLOY-VERIFICATION.md`*
