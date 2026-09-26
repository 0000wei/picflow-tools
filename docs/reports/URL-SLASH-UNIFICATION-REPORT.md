# URL 斜杠自指冲突修复报告 (picete-url-fix-k7)

日期: 2026-09-26 · 分支: `fm/picete-url-fix-k7`

## 问题

`vercel.json` 自 2026-07-28 起配置 `cleanUrls: true` / `trailingSlash: false`:
斜杠 URL(`https://picete.com/png-to-jpg/`)返回 **308** 跳转到无斜杠版(200)。
但 sitemap/canonical/og:url/hreflang/JSON-LD/页内内链全部声明斜杠版,
形成「声明权威版 = 会跳走的 URL」自相矛盾(GSC: `/png-to-jpg` "URL is unknown to Google",
`/resize-image-to-512x512` 被判 "Alternate page with proper canonical tag")。

## 修复方向

统一为**无斜杠**(与实际 200 服务一致)。未改动 vercel.json 语义、URL scheme、
title/meta/内容、页面增删。根目录 `/` 与 `https://picete.com/` 保持斜杠(即首页权威形式)。

## 生成来源修复(防再发)

| 文件 | 修复 |
|------|------|
| `scripts/seo/generate-sitemap.js` | 3 处 `<loc>` 模板去掉尾部斜杠(工具页/语言首页/语言工具页) |
| `scripts/seo/generate-sitemap.sh` | 同上 3 处 |
| `scripts/build/pSEO_matrix_generator.py` | canonical、hreflang(含 x-default)、BreadcrumbList `home_url`/`tool_url` 共 5 个 URL 构造点 |
| `scripts/audit/verify_seo_matrix.py` | `expected_canonical` 期望值同步为无斜杠 |

## 一次性统一修复

- 新增 `scripts/fix/fix_trailing_slash_urls.py`: 对全部在服 HTML(459 矩阵页 + wordpress-plugin
  + 9 语言首页 + privacy-policy)与 `llms.txt` 做 4 类规则替换:
  绝对 URL 尾斜杠、引号包裹的根相对路径尾斜杠、括号内路径尾斜杠、首页 JSON-LD `"url"` 归一为
  `https://picete.com/`。共 **10,997 处替换 / 461 个内容文件**(460 HTML + llms.txt;
  git 全量变更 468 modified + 3 new,含双份 sitemap 与 4 个生成器脚本)。
- 重新生成 sitemap(`node scripts/seo/generate-sitemap.js`)并同步根副本(460 URLs)。

## 验证(本地镜像服务器,复刻 Vercel 语义)

新增 `scripts/audit/verify_url_serving.py`: 起本地静态服务,`/x/`→308、`/x`→服务 `x/index.html`、
不跟随重定向逐项实测。**结果: PASS**

1. **sitemap.xml 全部 `<loc>` HTTP 实测**: 460/460 直接 200,零 308/301。
2. **抽样 29 页(≥20)canonical == 实际 200 服务 URL(无斜杠)**:
   覆盖首页(en/zh/es/ar/pt/ko/de)、avif/webp 转换页(avif-to-png、webp-to-avif、jpg-to-avif、
   webp-to-jpg、png-to-webp)、尺寸页(512x512、800x800、1920x1080)、splitter 页
   (image-splitter、3x3、4-parts、instagram)、本地化工具页(zh/de/es/ar/pt/ko/ja/fr 各 1)。
   每页同时校验: og:url == canonical、hreflang 10 条(含 x-default)完整且互相声明一致、
   集群内每个 alternate HTTP 实测直接 200、JSON-LD `SoftwareApplication.url`/
   `BreadcrumbList.item` 同 canonical。
3. **斜杠 URL 语义验证**: `/png-to-jpg/` → 308 → `/png-to-jpg` → 200(与线上一致)。
4. **全站残留扫描**: 在服 HTML 中斜杠声明残留 = 0(`docs/specs/*.html` 内部规格文档的
   正文描述除外,非 SEO 声明,按约束 4 不动)。相对内链 `href="/x/"` 残留 = 0。
5. **回归**: `python3 scripts/audit/verify_seo_matrix.py` — canonical 检查全部通过;
   仅剩 5 个 **修复前已存在** 的 wordpress-plugin 结构缺口(该页从未注入 hreflang/JSON-LD,
   `git diff` 确认本次只改了它的 canonical/og:url 两行)。按约束 4 不补 hreflang/schema。
6. `make verify` / `make lint` 通过。

## 遗留(不在本任务范围)

- `wordpress-plugin` 页缺 hreflang + JSON-LD(先于本任务存在,修复属页面结构改动)。
- es/pt/ko 语言首页 BreadcrumbList position-1 指向站点根而非语言首页(zh/ja/de 指向语言首页,
  历史不一致;两者均为直接 200,无斜杠冲突,按约束 4 不动)。
