# AGENTS.md — PicEte

> 50 行入口文件。给地图，不给百科。

## 项目定位

**PicEte** = 免费在线图片处理工具站（picete.com）。浏览器内完成格式转换/缩放/压缩/分割/取色/Base64，纯前端零上传。静态站点，Vercel 部署。

## 快速链接

- [STRUCTURE-RULES.md](./STRUCTURE-RULES.md) ← 目录结构/文件命名规则（必读）
- [vercel.json](./vercel.json) — 部署配置
- [README.md](./README.md) — 产品简介

## 新会话启动流程

每次新会话，按此顺序加载上下文：

0. **`bash scripts/init.sh`** — 一键启动（文件健康检查 + git log + git status）
1. **STRUCTURE-RULES.md** — 目录结构、文件分类原则
2. **PROGRESS.md** — 当前进展、已完成/进行中/待办（如不存在则跳过）
3. **feature_list.json** — 功能清单/需求列表（如不存在则跳过）
4. **git log**（最近 10 条）— 了解近期变更节奏
5. **AGENTS.md** — 本文件（会话指令）

## 运行/验证

项目是纯静态站点，无需构建步骤：

```bash
# 方式一：Python 内置 HTTP 服务器（推荐，零依赖）
cd /path/to/picete && python3 -m http.server 3000

# 方式二：Vercel 本地预览（需安装 Vercel CLI）
vercel dev

# 方式三：npx serve
npx serve .
```

验证：打开浏览器访问 `http://localhost:3000`，检查首页和各语言页面正常渲染，图片工具功能可用。

部署：`git push` 到 master → Vercel 自动部署到 https://picete.com。

## WIP=1 规则

**一次只做一个 feature。** 完成一个功能/改动 → commit → push → 确认部署 → 再开始下一个。严禁并行开发。

当前 WIP 状态记录在 PROGRESS.md（如存在）。

## 会话结束清理清单

结束会话前执行：

- [ ] `git status` — 检查未跟踪/未暂存文件
- [ ] `git add` + `git commit` — 提交当前工作（含 PROGRESS.md 更新）
- [ ] `git push` — 推送至远程
- [ ] 检查根目录整洁：无垃圾文件（.tmp, .trash, 大文件等）
- [ ] 确认根目录下 AGENTS.md / STRUCTURE-RULES.md / vercel.json 等关键文件未被误删

## 跨语言目录

当前支持：en (根目录), zh, ja, es, pt, fr, de, ar

每种语言一套完整页面。新增语言 = 新建目录 + 翻译内容 + vercel.json 无需修改。
