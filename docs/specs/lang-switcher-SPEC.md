# SPEC - 修复语言切换器 Bug

## 诊断
1. 语言切换正则 `path.replace(/^\/(zh|ja|de|fr|es|pt|ar)\//, '/')` 在路径没有斜杠结尾（如 `/zh`）时匹配失效，导致切换其他语言时变成拼接路径如 `/ja/zh`。
2. JS 字典中硬编码了域名 `https://picete.com/`，导致本地环境测试时切换语言直接跳转至线上。

## 修复任务 (Task 7.1)
- 编写修复脚本 `scripts/fix/fix_lang_switcher.js`。
- 读取项目中所有的 `.html` 文件。
- 将 `path.replace(/^\/(zh|ja|de|fr|es|pt|ar)\//, '/')` 替换为 `path.replace(/^\/(zh|ja|de|fr|es|pt|ar)(?:\/|$)/, '/')`。
- 将 `var paths = {"en": "https://picete.com/", ...}` 替换为相对路径：`var paths = {"en": "/", "zh": "/zh/", "ja": "/ja/", "de": "/de/", "fr": "/fr/", "es": "/es/", "pt": "/pt/", "ar": "/ar/"};`。
- 保证脚本幂等并执行该脚本。

## 执行方式
遵循 Harness Engineering：
- 由 Hermes 编写此 SPEC。
- 由 Hermes 通过 Claude Code CLI 执行任务。
- 由 Hermes 进行独立验证后 Commit。
