# SPEC - 多语言首页 Footer 同步与布局对齐

## 诊断
1. 所有的 7 种语言首页（如 `zh/index.html`）的 `<h4>更多工具</h4>` (More Tools) 栏目均为空，缺失了英文版中的 25 个长尾工具。
2. 本地化版本中的 `Resize for Facebook Cover` 工具被错误地放在了工具网格区（Tools Grid）和“图片转换” Footer 下，与英文版不一致。

## 修复任务 (Task 8.1)
- 编写 Node.js 脚本 `scripts/fix/sync_footer_tools.js`。
- 将 `Resize for Facebook Cover` 从所有的本地化首页的工具网格中剔除。
- 从翻译版的 "图片转换" 分类 Footer 中剔除 `Resize for Facebook Cover`。
- 将英文首页 "More Tools" 中的 26 个工具列表作为基准。对于 7 种本地化语言，通过抓取对应本地化工具页（如 `zh/compress-image-to-50kb/index.html`）的 JSON-LD 中的 `name` 属性（或 `<title>`）获取翻译名称，动态生成 `<li><a href="/{lang}/{tool}/">{name}</a></li>` 格式的 HTML。
- 将生成的 HTML 注入到所有 7 个语言首页的对应 "More Tools"（更多工具）栏目中。

## 执行方式
遵循 Harness Engineering：
- 由 Hermes 编写此 SPEC。
- 由 Hermes 委托 Claude Code 执行写入和注入。
- 由 Hermes 进行独立验证（`git diff`）后 Commit。
