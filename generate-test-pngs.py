#!/usr/bin/env python3
import struct
import zlib
import os

def create_png(path, w, h):
    def chunk(ctype, data):
        c = ctype + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)  # 8-bit RGB
    raw = b''
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            r = int(255 * x / w)
            g = int(255 * y / h)
            b = 128
            raw += struct.pack('BBB', r, g, b)
    idat_data = zlib.compress(raw)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', ihdr))
        f.write(chunk(b'IDAT', idat_data))
        f.write(chunk(b'IEND', b''))
    size = os.path.getsize(path)
    print(f'  ✓ {path}: {w}×{h}, {size} bytes')

def create_solid_png(path, w, h, color):
    def chunk(ctype, data):
        c = ctype + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    raw = b''
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            raw += struct.pack('BBB', *color)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        idat_data = zlib.compress(raw)
        f.write(chunk(b'IHDR', ihdr))
        f.write(chunk(b'IDAT', idat_data))
        f.write(chunk(b'IEND', b''))
    size = os.path.getsize(path)
    print(f'  ✓ {path}: {w}×{h}, {size} bytes')

os.makedirs('images', exist_ok=True)
print('Generating test PNG images...')
create_png('images/test-photo-320x240.png', 320, 240)
create_png('images/test-photo-1920x1080.png', 1920, 1080)
create_solid_png('images/test-solid-white.png', 100, 100, (255, 255, 255))
create_solid_png('images/test-solid-red.png', 100, 100, (255, 0, 0))
print('Done!')
