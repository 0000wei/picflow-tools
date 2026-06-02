# PicEte 已知问题修复方案

## 问题清单

| # | 问题 | 类型 | 影响 |
|---|------|------|------|
| 1 | convert/ 有 113 个空 stub 目录，无 index.html，线上暴露 404 | 阻断 | 搜索引擎可能收录空路径 |
| 2 | sitemap 只收录了 16/37 个多语言工具页（缺 21 个）+ 缺 7 个语言首页 | SEO | 37% 翻译页未被索引 |
| 3 | privacy-policy 只有英文 | 合规 | 多语言用户看不到隐私政策 |

---

## 方案

### 方案 A — 最小修复（推荐）

| Task | 动作 | 验证 |
|------|------|------|
| 1-A | 删除 convert/ 目录（113 个空 stub 从未实现，git rm -r） | ls convert/ 报不存在 |
| 2-A | 补全 sitemap：添加 7 个语言首页 + 21 个缺失的多语言工具 URL | make verify 通过 |
| 3-A | 复制 privacy-policy.html 到 7 个语言目录（翻訳不要，纯通知页） | ls zh/privacy-policy.html 等 |

**工作量**：3 个 Task，约 10 分钟。
**缺点**：sitemap 手动维护，下次加工具得再改。

### 方案 B — 方案 A + sitemap 生成脚本

在 A 的基础上，新增一个脚本：

| Task | 动作 | 验证 |
|------|------|------|
| 1-B | 同上 A | 同上 |
| 2-B | 创建 scripts/seo/generate-sitemap.sh，遍历根目录工具目录 + 所有语言目录，自动生成完整 sitemap.xml | 脚本输出 == 152+7+21=180 URLs |
| 3-B | 同 A | 同 A |
| 4-B | 运行脚本替换 sitemap.xml | make lint 检测 sitemap 格式合法 |

**工作量**：4 个 Task，约 20 分钟。
**优点**：以后加工具只需 `make sitemap` 一键更新。

### 方案 C — 只修阻断问题

| Task | 动作 | 验证 |
|------|------|------|
| 1-C | 删除 convert/ | ls convert/ 不存在 |
| 2-C | sitemap 加 7 个语言首页 | sitemap 有 picete.com/zh/ 等 |
| 3-C | privacy-policy 放后 | 不处理 |

**优点**：最快，约 5 分钟。
**缺点**：隐私政策依然缺失，sitemap 仍不完整。
