"""Box-downscale an 8-bit RGBA/RGB PNG by an integer factor using only the stdlib.

No Pillow, no ImageMagick, no network. Useful for turning a 2x screenshot
(2400x1260) into a social card at 1x (1200x630) with real downsampling instead
of a browser resize, which can shift layout.

Usage
    python3 tools/downscale.py <src.png> <dst.png> [factor=2]
"""
import struct
import sys
import zlib


def read_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat, w = 8, b"", None
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            w, h, depth, colour = struct.unpack(">IIBB", body[:10])
            assert depth == 8 and colour in (2, 6), (depth, colour)
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
    channels = 4 if colour == 6 else 3
    raw = zlib.decompress(idat)
    stride = w * channels
    rows, prev = [], bytearray(stride)
    p = 0
    for _ in range(h):
        ftype = raw[p]
        line = bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        if ftype == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif ftype == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                b = prev[i]
                c = prev[i - channels] if i >= channels else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        rows.append(bytes(line))
        prev = line
    return w, h, channels, rows


def write_png(path, w, h, channels, rows):
    colour = 6 if channels == 4 else 2
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(tag, body):
        return (struct.pack(">I", len(body)) + tag + body
                + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))

    out = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, colour, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(out)


def downscale(src, dst, factor):
    w, h, ch, rows = read_png(src)
    nw, nh = w // factor, h // factor
    out = []
    area = factor * factor
    for y in range(nh):
        strips = [rows[y * factor + k] for k in range(factor)]
        line = bytearray(nw * ch)
        for x in range(nw):
            base = x * factor * ch
            for c in range(ch):
                total = 0
                for s in strips:
                    for k in range(factor):
                        total += s[base + k * ch + c]
                line[x * ch + c] = total // area
        out.append(bytes(line))
    write_png(dst, nw, nh, ch, out)
    return nw, nh


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("usage: downscale.py <src.png> <dst.png> [factor=2]")
    factor = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    width, height = downscale(sys.argv[1], sys.argv[2], factor)
    print(f"{sys.argv[2]}: {width}x{height} (factor {factor})")
