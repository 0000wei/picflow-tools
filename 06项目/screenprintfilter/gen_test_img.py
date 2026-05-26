import struct, zlib

def make_png(w, h):
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    raw = b''
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            v = int((x/w) * 255 + (y/h) * 255) // 2
            raw += bytes([v, v, v])
    compressed = zlib.compress(raw)
    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')

with open('/home/wu/screenprintfilter-com/test-perf.png', 'wb') as f:
    f.write(make_png(400, 300))
print('done')
