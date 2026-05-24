# 暗色模式切换修复任务

## 问题
picete.com 的暗色模式切换只在家首页 (index.html) 有效，所有子页面均缺少切换的 JavaScript 代码。用户点击 ☀️/🌙 按钮没有任何反应。

## 根 index.html 已有的正确代码（参考）
根 index.html 在第 527-545 行包含这个切换脚本：

```js
<script>
// Theme Toggle
(function(){
    var btn = document.getElementById('themeToggle');
    if(!btn) return;
    var t = localStorage.getItem('picete_theme');
    if(t) document.documentElement.setAttribute('data-theme', t);
    else if(window.matchMedia('(prefers-color-scheme: dark)').matches){
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('picete_theme', 'dark');
    }
    btn.onclick = function(){
        var cur = document.documentElement.getAttribute('data-theme');
        var next = cur === 'dark' ? '' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('picete_theme', next || 'light');
    };
})();
</script>
```

## 修复要求
1. 在所有子页面的 `</body>` 标签前（即最后一行 `</html>` 前）插入上述 JS 代码块
2. 注意 JS 必须用 `<script>` 标签包裹，放在 `</body>` 内部，`</body>` 标签前

## 需要修复的文件（共29个）
### 语言目录（7个）
- ar/index.html
- de/index.html
- es/index.html
- fr/index.html
- ja/index.html
- pt/index.html
- zh/index.html

### 工具页面（22个）
- compress-image/index.html
- compress-image-to-100kb/index.html
- compress-image-to-50kb/index.html
- compress-jpg-to-200kb/index.html
- extract-colors/index.html
- image-splitter/index.html
- image-to-base64/index.html
- jpg-to-png/index.html
- jpg-to-webp/index.html
- png-to-jpg-for-email/index.html
- png-to-jpg/index.html
- png-to-webp-for-wordpress/index.html
- png-to-webp/index.html
- resize-image/index.html
- resize-image-to-1080x1080/index.html
- resize-image-to-1200x630/index.html
- resize-image-to-1920x1080/index.html
- resize-image-to-800x800/index.html
- split-image-into-3x3/index.html
- split-image-into-4-parts/index.html
- webp-to-png-for-website/index.html
- webp-to-png/index.html

## 方法
用 sed 命令在每个文件的 `</body>` 标签前插入该 JS 块。所有文件都在 /home/wu/picete-site/ 目录下。

## 验证
修复后，用 grep 验证每个文件都有 'picete_theme' 字样出现（说明 JS 已插入）。
