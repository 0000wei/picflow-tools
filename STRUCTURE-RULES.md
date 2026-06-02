# PicEte 项目结构规范

## 目录结构

```
picete/
├── config/              # 项目配置文件 (mcp.json 等)
├── docs/
│   ├── specs/           # SPEC 文档、计划文档
│   ├── reports/         # 测试报告、检查产出、分析报告
│   └── archive/         # 历史/归档文件
├── scripts/
│   ├── audit/           # 审计/检查脚本
│   ├── fix/             # 修复/补丁脚本
│   ├── og/              # OG 图片生成相关
│   └── legacy/          # 遗留/弃用脚本（保留参考）
├── seo/                 # SEO 相关文件 (sitemap.xml, robots.txt, llms.txt, favicon.ico)
├── {en,zh,pt,ar,...}/   # 语言目录（内容根，不移动）
├── vercel.json          # Vercel 部署配置（保留在根目录，Vercel 强制要求）
├── .gitignore
├── STRUCTURE-RULES.md   # 本文件
└── ...其他根级配置文件
```

## 核心原则

1. **不动线上 URL 路径** — HTML 文件固定在各自语言目录，不移动
2. **保留 git 历史** — 所有文件移动使用 `git mv` 而非 `mv`
3. **不修改 HTML 内容** — 只重组织文件位置
4. **vercel.json 必须留在根目录** — Vercel 部署强制从项目根目录读取

## 文件分类规则

| 类型 | 目标目录 | 示例 |
|------|----------|------|
| SPEC/计划 | `docs/specs/` | `*-SPEC.md`, `*plan*.txt` |
| 报告/测试产出 | `docs/reports/` | `*report*`, `TEST-*`, 分析性 HTML |
| 历史归档 | `docs/archive/` | 废弃/不再使用的文档 |
| 审计脚本 | `scripts/audit/` | `audit_*.py`, `scan_*.py`, `check_*.py` |
| 修复脚本 | `scripts/fix/` | `fix_*.py`, `fix_*.js` |
| OG 生成 | `scripts/og/` | `generate-og.*` |
| 遗留脚本 | `scripts/legacy/` | 不再维护但保留参考的脚本 |
| 配置 | `config/` | `mcp.json` 等 |
| SEO | `seo/` | `sitemap.xml`, `robots.txt` |

## 注意事项

- `.well-known/` 目录已在 `.gitignore` 中忽略（用于 Let's Encrypt 等验证）
- `__pycache__/` 已在 `.gitignore` 中忽略
- 新增脚本或文档请按上表放入对应目录
