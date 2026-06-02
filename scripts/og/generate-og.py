#!/usr/bin/env python3
"""Generate OG image (1200x630 PNG) for PicEte."""
from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1200, 630
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Background gradient
for y in range(H):
    t = y / H
    r = int(15 + t * 15)  # 0x0f -> 0x1e
    g = int(23 + t * 20)
    b = int(42 + t * 17)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Grid dots
for x in range(60, W, 120):
    for y in range(60, H, 120):
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(51, 65, 85, 76))

# Decorative shapes
draw.rounded_rectangle([80, 80, 160, 160], radius=16, outline=(8, 173, 255, 38), width=1)
draw.rounded_rectangle([1040, 470, 1120, 550], radius=16, outline=(96, 165, 250, 38), width=1)
draw.arc([1080, 140, 1120, 180], 0, 360, fill=(8, 173, 255, 25), width=1)
draw.arc([86, 516, 114, 544], 0, 360, fill=(96, 165, 250, 25), width=1)

# Try to use system fonts
font_paths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]
try:
    bold_font = ImageFont.truetype(font_paths[0], 60)
    reg_font = ImageFont.truetype(font_paths[1], 28)
    small_font = ImageFont.truetype(font_paths[1], 14)
    url_font = ImageFont.truetype(font_paths[0], 17)
except:
    bold_font = ImageFont.load_default()
    reg_font = bold_font
    small_font = bold_font
    url_font = bold_font

# "Pic" in light
draw.text((420, 180), "Pic", fill=(226, 232, 240), font=bold_font)
# "Ete" in blue
draw.text((540, 180), "Ete", fill=(8, 173, 255), font=bold_font)

# Tagline
draw.text((600, 320), "Free Online Image Processing Tools", fill=(148, 163, 184), font=reg_font, anchor='mt')

# Feature pills
pill_data = [
    ('Format Converter', 390),
    ('Image Resizer', 600),
    ('Compressor', 810),
]
pill_y = 400
for text, cx in pill_data:
    # pill background
    x0, y0 = cx - 65, pill_y
    x1, y1 = cx + 65, pill_y + 28
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    # text
    tw = draw.textlength(text, font=small_font)
    tx = cx - tw // 2
    draw.text((tx, pill_y + 5), text, fill=(203, 213, 225), font=small_font)

# URL
draw.text((600, 500), "picete.com", fill=(8, 173, 255), font=url_font, anchor='mt')

output_path = '/home/wu/picete-site/images/og-image.png'
img.save(output_path)
print(f'OG Image saved: {output_path} ({(os.path.getsize(output_path) / 1024):.1f} KB)')
