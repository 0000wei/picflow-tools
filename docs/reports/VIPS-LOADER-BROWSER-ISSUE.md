# vips-loader.js 浏览器端加载问题

> 更新时间：2026-06-04
> 涉及 Task：0.5.10（浏览器 RAW 解码验证）

## 问题

`vips-loader.js` 无法在浏览器中加载自编译的 wasm-vips。所有页面通过 `vips-loader.js` 加载 wasm-vips，包括现有的 compress/resize/split 等工具页。

## 根因

`vips-loader.js` 依赖 `window.Vips` 全局变量来获取 Emscripten 编译的 Vips 工厂函数：

```javascript
var Vips = window.Vips;
if (!Vips) {
    throw new Error('vips.js not loaded — ensure <script src="/js/lib/vips.js"> is included');
}
var vips = await Vips();
```

npm 包 `wasm-vips` 自带的 `vips.js` 会设置 `window.Vips`，但自编译版本（Emscripten 标准输出）**不设置 `window.Vips`**，而是使用：
- CommonJS: `module.exports = Vips`
- AMD: `define([], () => Vips)`

在浏览器 `<script>` 标签上下文中，这两种导出方式都不会产生 `window.Vips`。

`vips-es6.js`（ES module 版本）需要用 `import` 导入，但 `vips-loader.js` 是传统 script，无法直接使用 `import`。

## 修复方案

让 `vips-loader.js` 内部通过动态 `<script type="module">` 加载 `vips-es6.js`，并接收其导出作为 `Vips` 工厂函数。具体：

1. 创建一个内联的 `<script type="module">` 标签
2. 在其中 `import Vips from '/js/lib/vips-es6.js'`
3. 将 `Vips` 赋值给 `window.Vips`（或通过 postMessage 传递给 loader）
4. 然后 loader 继续执行 `await Vips()`

这样所有现有工具页（compress-image、resize-image 等）不需要任何修改，用户零感知。

## 对用户的影响

| 用户场景 | 影响 |
|---------|------|
| 现有工具页（compress/resize/split） | 无感知（加载方式不变） |
| 未来的 RAW 工具页 | 无感知（同 vips-loader.js） |
| 加载速度 | 无明显变化（vips-es6.js 与 vips.js 大小相近） |
