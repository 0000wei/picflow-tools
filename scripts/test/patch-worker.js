const fs = require('fs');
let code = fs.readFileSync('D:/knowledge-base/06项目/哥飞建站/picete/js/lib/vips.js', 'utf8');
code = code.replace(/a=new Worker\(a,\{name:"em-pthread"\}\);Kd\.push\(a\)/g, `a=new Worker(a,{name:"em-pthread"}); a.onerror = (e) => console.error("[WORKER ERROR]", e.message); Kd.push(a);`);
fs.writeFileSync('D:/knowledge-base/06项目/哥飞建站/picete/js/lib/vips.js', code);
console.log("Patched Worker creation");
