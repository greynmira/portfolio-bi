#!/usr/bin/env python3
"""Embeds a pHYs (physical pixel dimensions) chunk into a PNG so viewers/
print tools read the correct DPI, not just the raw pixel count."""
import struct
import sys
import zlib


def embed_dpi(path, dpi):
    ppm = round(dpi / 0.0254)  # pixels per meter
    with open(path, "rb") as f:
        data = f.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    ihdr_end = 8 + 8 + ihdr_len + 4  # sig + (len+type) + data + crc
    body = b"pHYs" + struct.pack(">IIB", ppm, ppm, 1)
    crc = zlib.crc32(body) & 0xFFFFFFFF
    chunk = struct.pack(">I", len(body) - 4) + body + struct.pack(">I", crc)
    new_data = data[:ihdr_end] + chunk + data[ihdr_end:]
    with open(path, "wb") as f:
        f.write(new_data)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        embed_dpi(p, 300)
        print("embedded 300 DPI in", p)
