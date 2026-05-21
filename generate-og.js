const { createCanvas } = require('canvas');
const fs = require('fs');

const W = 1200, H = 630;
const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

// Background
const grad = ctx.createLinearGradient(0, 0, W, H);
grad.addColorStop(0, '#0f172a');
grad.addColorStop(1, '#1e293b');
ctx.fillStyle = grad;
ctx.fillRect(0, 0, W, H);

// Grid dots
ctx.fillStyle = '#334155';
ctx.globalAlpha = 0.3;
for (let x = 60; x < W; x += 120)
  for (let y = 60; y < H; y += 120) {
    ctx.beginPath();
    ctx.arc(x, y, 2, 0, Math.PI * 2);
    ctx.fill();
  }
ctx.globalAlpha = 1;

// Decorative shapes
ctx.strokeStyle = '#08adff';
ctx.globalAlpha = 0.15;
ctx.lineWidth = 1;
roundRect(ctx, 80, 80, 80, 80, 16);
ctx.stroke();
roundRect(ctx, 1040, 470, 80, 80, 16);
ctx.stroke();
ctx.globalAlpha = 0.1;
ctx.beginPath();
ctx.arc(1100, 160, 20, 0, Math.PI * 2);
ctx.stroke();
ctx.beginPath();
ctx.arc(100, 530, 14, 0, Math.PI * 2);
ctx.stroke();
ctx.globalAlpha = 1;

// Logo text - "PicEte"
ctx.font = 'bold 60px system-ui, -apple-system, sans-serif';
ctx.textAlign = 'center';
ctx.textBaseline = 'bottom';
ctx.fillStyle = '#e2e8f0';
ctx.fillText('Pic', 530, 290);
ctx.fillStyle = '#08adff';
ctx.fillText('Ete', 670, 290);

// Tagline
ctx.font = '28px system-ui, -apple-system, sans-serif';
ctx.textBaseline = 'top';
ctx.fillStyle = '#94a3b8';
ctx.fillText('Free Online Image Processing Tools', 600, 340);

// Feature pills
const pills = [
  { label: 'Format Converter', x: 415 },
  { label: 'Image Resizer', x: 600 },
  { label: 'Compressor', x: 785 },
];
const pillY = 400;
for (const p of pills) {
  ctx.fillStyle = '#1e293b';
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 1;
  roundRect(ctx, p.x - 60, pillY, 120, 30, 15);
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = '#cbd5e1';
  ctx.font = '14px system-ui, -apple-system, sans-serif';
  ctx.textBaseline = 'middle';
  ctx.fillText(p.label, p.x, pillY + 15);
}

// URL
ctx.fillStyle = '#08adff';
ctx.font = 'bold 17px system-ui, -apple-system, sans-serif';
ctx.textBaseline = 'top';
ctx.fillText('picete.com', 600, 490);

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

const buf = canvas.toBuffer('image/png');
fs.writeFileSync('/home/wu/picete-site/images/og-image.png', buf);
console.log(`OG Image created: ${(buf.length / 1024).toFixed(1)} KB`);
