const fs = require('fs');
let code = fs.readFileSync('D:/knowledge-base/06项目/哥飞建站/picete/js/lib/vips.js', 'utf8');

// Patch worker postMessage
code = code.replace(/postMessage\(([^)]+)\)/g, function(match, p1) {
  return `(function(){
    try { console.log("[WORKER POSTMESSAGE intercept]", JSON.stringify(` + p1 + `)); } catch(e) { console.log("[WORKER POSTMESSAGE intercept] <circular/unstringifiable>"); }
    return postMessage(` + p1 + `);
  })()`;
});

fs.writeFileSync('D:/knowledge-base/06项目/哥飞建站/picete/js/lib/vips.js', code);
console.log("Patched postMessage in vips.js");
