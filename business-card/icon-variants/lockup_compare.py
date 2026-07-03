#!/usr/bin/env python3
"""Places each of the 3 round-4 icon concepts above the real "Reimagined
by Mira" wordmark, in the actual card fonts, for in-context comparison.
Does not touch the live card files."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generate import SERIF, GREEN, TEXT  # noqa: E402
from icons_v4 import icon_1, icon_2, icon_3  # noqa: E402

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

VARIANTS = [("1", "Minimal bulb + bold sprout", icon_1),
            ("2", "Continuous-line bulb", icon_2),
            ("3", "Sprout-as-filament", icon_3)]


def build():
    cell_w, cell_h = 300, 260
    label_h = 30
    w = cell_w * 3
    h = cell_h + label_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    parts.append(f'<rect width="{w}" height="{h}" fill="white"/>')
    for i, (letter, label, fn) in enumerate(VARIANTS):
        x0 = i * cell_w
        cx = x0 + cell_w / 2
        icon_scale = 1.55
        icon_w = 130 * icon_scale
        icon_offset_x = cx - icon_w / 2
        icon_offset_y = 14
        parts.append(f'<g transform="translate({icon_offset_x},{icon_offset_y}) scale({icon_scale})">{fn()}</g>')
        name_y = 14 + 110 * icon_scale + 34
        parts.append(f'<text x="{cx}" y="{name_y}" text-anchor="middle" '
                      f'font-family="{SERIF}" font-size="21" font-weight="600" '
                      f'fill="{TEXT}">Reimagined by Mira</text>')
        parts.append(f'<text x="{cx}" y="{h-10}" text-anchor="middle" '
                      f'font-family="sans-serif" font-size="14" fill="#111">{letter}. {label}</text>')
        if i > 0:
            parts.append(f'<line x1="{x0}" y1="0" x2="{x0}" y2="{h}" stroke="#eee"/>')
    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    with open(os.path.join(OUT_DIR, "lockup_compare.svg"), "w") as f:
        f.write(build())
    print("wrote lockup_compare.svg")
