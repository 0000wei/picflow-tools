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

## Manager Mode（角色分工）

本项目采用 Hermes Agent 作为管理者，Claude Code CLI 作为执行者：

| 角色 | 职责 | 工具 |
|------|------|------|
| **Hermes（管理者）** | 规划任务 → 编写委托上下文 → 监督执行 → 独立验证产出 | `delegate_task` / 手动写 prompt |
| **Claude Code（执行者）** | 按照委托上下文完成编码/文件修改 | `claude -p --dangerously-skip-permissions` |

**执行流程：**
1. Hermes 从 SPEC 中选取一个 Task
2. Hermes 编写精确的委托上下文（含约束、不做的、验证标准）
3. 委托 Claude Code 执行（`claude -p --dangerously-skip-permissions "..."`）
4. Claude Code 完成后，Hermes 独立验证（不信任自报告）
5. 验证通过后标记 Task 完成，继续下一个

**不做的：**
- Hermes 不直接写功能代码（验证脚本/测试脚本除外）
- Hermes 不使用 delegate_task（Hermes 子代理）替代 Claude Code 执行编码任务

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
