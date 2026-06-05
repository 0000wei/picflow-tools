# P5: 工具交互测试闭环 — 执行计划 SPEC

> 遵循 Harness Engineering：写 SPEC → 用户确认 → 分任务委托 → 验证 → 报告
> Manager Mode：我（Hermes）负责规划、委托、验证，Claude Code 负责执行

---

## 一、任务分解

将 P5 拆解为 4 个子任务，按依赖顺序：

```
Task 1: 测试环境 + 测试图片
  │
  ▼
Task 2: Playwright 测试脚本（核心 20 个 EN 工具）
  │
  ▼
Task 3: 语言抽样验证（zh + ja 各 5 个工具）
  │
  ▼
Task 4: 测试报告 + bug 修复
```

### Task 1: 测试环境搭建 + 测试图片准备

**目标：** 建立可重复的自动化测试环境

**内容：**
1. 安装 Playwright：`npm init -y && npm install playwright`
2. 下载 Chromium：`npx playwright install chromium`
3. 创建测试图片 fixtures（3 张真实图片）：
   - `scripts/test/fixtures/test-photo.jpg` （~200KB，真实照片）
   - `scripts/test/fixtures/test-logo.png` （~100KB，带透明背景）
   - `scripts/test/fixtures/test-webp.webp` （~100KB，WebP 格式）
4. 验证图片可以正常加载到浏览器

**产出：**
- `package.json` (playwright 依赖)
- `scripts/test/fixtures/` (3 张测试图)

---

### Task 2: Playwright 测试脚本 — 核心 20 个 EN 工具

**目标：** 针对核心 20 个 EN 工具的自动化测试脚本，每工具验证功能正常

**测试覆盖表：**

| # | 工具 | 测试操作 | 验证标准 |
|---|------|---------|---------|
| 1 | resize-image | 上传 → 输入 800x600 → 处理 → 下载 | 输出尺寸 = 800x600 |
| 2 | compress-image | 上传 → 拖质量到50 → 处理 → 下载 | 输出体积 < 输入体积 |
| 3 | compress-image-to-100kb | 上传大图 → 处理 → 下载 | 输出体积 ≤ 100KB |
| 4 | compress-image-to-50kb | 同上 | 输出体积 ≤ 50KB |
| 5 | png-to-jpg | 上传 PNG → 选 JPG → 处理 | 输出扩展名 .jpg |
| 6 | jpg-to-png | 上传 JPG → 选 PNG → 处理 | 输出扩展名 .png |
| 7 | webp-to-png | 上传 WebP → 选 PNG → 处理 | 输出扩展名 .png |
| 8 | png-to-webp | 上传 PNG → 选 WebP → 处理 | 输出扩展名 .webp |
| 9 | jpg-to-webp | 上传 JPG → 选 WebP → 处理 | 输出扩展名 .webp |
| 10 | resize-image-to-1080x1080 | 上传 → 处理 | 输出尺寸 = 1080x1080 |
| 11 | resize-image-to-1920x1080 | 上传 → 处理 | 输出尺寸 = 1920x1080 |
| 12 | resize-image-to-800x800 | 上传 → 处理 | 输出尺寸 = 800x800 |
| 13 | image-splitter | 上传 → 选 2x2 → 处理 | 输出 = 4 张图片 |
| 14 | split-image-into-3x3 | 上传 → 处理 | 输出 = 9 张图片 |
| 15 | split-image-into-4-parts | 上传 → 处理 | 输出 = 4 张图片 |
| 16 | extract-colors | 上传 → 处理 | 输出显示 5+ 种颜色 |
| 17 | image-to-base64 | 上传 → 处理 | 输出以 data:image 开头 |
| 18 | batch-convert-png-to-jpg | 上传 2 张 PNG → 处理 | 输出 2 张 JPG |
| 19 | compress-image-to-200kb | 上传大图 → 处理 | 输出体积 ≤ 200KB |
| 20 | compress-image-to-500kb | 上传大图 → 处理 | 输出体积 ≤ 500KB |

**脚本文件：** `scripts/test/tool-test.mjs`

**技术方案：**
- 使用 Playwright CDP 或直接 `page.goto('https://picete.com/TOOL_PATH')`
- 用 `page.setInputFiles()` 上传测试图片
- 填写参数（尺寸、质量等）
- 点击处理按钮
- 等待下载/输出
- 用 `page.evaluate()` 或文件下载监听验证结果
- 记录每个工具是 PASS / FAIL / SKIP
- 运行命令：`node scripts/test/tool-test.mjs`

---

### Task 3: 语言抽样验证 — zh + ja

**目标：** 验证多语言版本的工具页在前端功能上与 EN 一致（前端逻辑语言无关，但需确认页面加载无 404/js 报错）

**抽样规则：**
- zh（母语）：抽 5 个典型工具（缩放/压缩/转换/分割/取色各 1 个）
- ja（小语种，曾有 stub 页面历史）：抽 5 个相同工具

**测试内容：**
1. 页面 HTTP 200 OK（curl 或 Playwright 导航）
2. 页面标题和按钮文本使用目标语言
3. JS 执行无 console error
4. 选 1 个工具核实功能正常（选 resize-image，因为各语言版本用的是同一个 js/main.js）

**脚本文件：** `scripts/test/lang-test.mjs`

---

### Task 4: 测试报告 + bug 修复

**目标：** 汇总测试结果，发现 bug 则修复

**产出：**
1. `docs/reports/TOOL-TEST-REPORT.md` — 完整测试报告（表格式，含每工具的 PASS/FAIL/SKIP）
2. `docs/reports/TOOL-BUGS.md` — Bug 记录（每 bug：工具、描述、复现步骤、修复方案、状态）
3. 修复发现的 bug（delegate 新 task 给 Claude Code 修复）
4. 根据测试结果更新 `feature_list.json`（如果有 tool 需要标记修复或问题）
5. 更新 `PROGRESS.md` (P5 标记完成)

---

## 二、委托执行计划

### 执行顺序

```
Task 1 → Task 2 → 验证 Task 2 → Task 3 → 验证 Task 3 → Task 4
```

- Task 1 和 Task 2 有依赖（需先有测试图片）
- Task 3 和 Task 2 无依赖（不同页面），但建议 Task2 先确认核心功能
- Task 4 依赖前三个任务全部完成

### Manager Mode 规则

1. **每个 Task 委托一个独立的 Claude Code 子代理**
2. 委托时不使用 `git add -A`，只 add 本 Task 修改的文件
3. 不创建临时脚本（helper 脚本必须放在 `scripts/` 下）
4. 我（Hermes）必须独立验证每个 Task 的产出，不信任自报告
5. 验证通过后再启动下一个 Task

---

## 三、验证标准

- [ ] Task 1: 3 张测试图片就位，Playwright 可启动浏览器
- [ ] Task 2: 20 个 EN 工具的测试脚本运行无报错
- [ ] Task 2: 每工具输出 PASS/FAIL（0 个 CRASH）
- [ ] Task 3: zh/ja 各 5 页 HTTP 200，无 JS console error
- [ ] Task 3: 1 个工具功能验证正常
- [ ] Task 4: 测试报告格式完整
- [ ] Task 4: FAIL 工具有对应的 bug 记录和修复方案
- [ ] 全局：`make verify` + `make lint` 通过
