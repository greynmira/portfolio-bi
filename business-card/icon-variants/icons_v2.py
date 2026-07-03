#!/usr/bin/env python3
"""Six distinct lightbulb-mark concepts, each a different silhouette/detail
strategy -- not incremental tweaks of one idea. Local coordinate box for
every concept is 130x130 so proportions compare directly in the sheet."""
import os

GREEN = "#0F4D3C"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def g(body, sw="1.3"):
    return f'<g fill="none" stroke="{GREEN}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</g>'


# A -- literal brief: wide/short bulb, softened shoulders, flat-ish bottom,
#      6 rays (top/UL/UR/L/R/bottom), 2 rings, bigger centered short-stem sprout
def icon_a():
    return g('''
    <line x1="65" y1="16" x2="65" y2="4" stroke-width="1.1"/>
    <line x1="40" y1="22" x2="31" y2="12" stroke-width="1.1"/>
    <line x1="90" y1="22" x2="99" y2="12" stroke-width="1.1"/>
    <line x1="26" y1="46" x2="12" y2="46" stroke-width="1.1"/>
    <line x1="104" y1="46" x2="118" y2="46" stroke-width="1.1"/>
    <line x1="65" y1="103" x2="65" y2="116" stroke-width="1.1"/>
    <path d="M 65,20 C 42,21 29,34 29,49
             C 29,62 38,70 47,74
             L 83,74
             C 92,70 101,62 101,49
             C 101,34 88,21 65,20 Z"/>
    <line x1="51" y1="81" x2="79" y2="81" stroke-width="1.2"/>
    <line x1="54" y1="89" x2="76" y2="89" stroke-width="1.2"/>
    <path d="M 65,74 L 65,45" stroke-width="1.1"/>
    <path d="M 65,45 C 56,45 52,38 57,32 C 61,28 65,34 65,45 Z" stroke-width="1.0"/>
    <path d="M 65,45 C 74,45 78,38 73,32 C 69,28 65,34 65,45 Z" stroke-width="1.0"/>
    ''')


# B -- monoline ultra-minimal: one continuous contour, no rays, tiny dot-leaf
def icon_b():
    return g('''
    <path stroke-width="1.4" d="M 65,18
             C 44,18 32,32 32,48
             C 32,62 40,70 47,73
             L 47,84 L 83,84 L 83,73
             C 90,70 98,62 98,48
             C 98,32 86,18 65,18 Z"/>
    <path d="M 65,72 L 65,50" stroke-width="1.0"/>
    <path d="M 65,50 C 60,50 58,45 61,41 C 64,38 66,42 65,50 Z" stroke-width="0.8"/>
    <path d="M 65,50 C 70,50 72,45 69,41 C 66,38 64,42 65,50 Z" stroke-width="0.8"/>
    <line x1="55" y1="90" x2="75" y2="90" stroke-width="1.2"/>
    ''')


# C -- halo ring: wide bulb encircled by one thin offset ring instead of rays
def icon_c():
    return g('''
    <circle cx="65" cy="48" r="42" stroke-width="0.7" stroke-dasharray="1,6"/>
    <path stroke-width="1.3" d="M 65,22 C 45,22 33,35 33,49
             C 33,61 41,68 49,72
             L 81,72
             C 89,68 97,61 97,49
             C 97,35 85,22 65,22 Z"/>
    <line x1="52" y1="78" x2="78" y2="78" stroke-width="1.2"/>
    <line x1="55" y1="85" x2="75" y2="85" stroke-width="1.2"/>
    <path d="M 65,72 L 65,44" stroke-width="1.0"/>
    <path d="M 65,44 C 57,44 54,38 58,33 C 61,30 65,35 65,44 Z" stroke-width="0.9"/>
    <path d="M 65,44 C 73,44 76,38 72,33 C 69,30 65,35 65,44 Z" stroke-width="0.9"/>
    ''')


# D -- merged leaf-bulb: the globe's lower half itself tapers into a leaf
#      point, growth motif built into the silhouette rather than added on top
def icon_d():
    return g('''
    <line x1="65" y1="14" x2="65" y2="3" stroke-width="1.1"/>
    <line x1="37" y1="21" x2="27" y2="12" stroke-width="1.1"/>
    <line x1="93" y1="21" x2="103" y2="12" stroke-width="1.1"/>
    <path stroke-width="1.4" d="M 65,17
             C 40,18 27,33 28,49
             C 29,64 45,74 65,86
             C 85,74 101,64 102,49
             C 103,33 90,18 65,17 Z"/>
    <line x1="58" y1="93" x2="72" y2="93" stroke-width="1.2"/>
    ''')


# E -- faceted geometric: subtly angular shoulders (not a pure curve), restrained rays
def icon_e():
    return g('''
    <line x1="65" y1="15" x2="65" y2="4" stroke-width="1.1"/>
    <line x1="38" y1="24" x2="28" y2="16" stroke-width="1.1"/>
    <line x1="92" y1="24" x2="102" y2="16" stroke-width="1.1"/>
    <path stroke-width="1.4" d="M 65,19
             L 48,23 C 34,28 30,40 32,50
             C 34,62 44,70 51,74
             L 79,74
             C 86,70 96,62 98,50
             C 100,40 96,28 82,23 Z"/>
    <line x1="52" y1="81" x2="78" y2="81" stroke-width="1.2"/>
    <line x1="55" y1="88" x2="75" y2="88" stroke-width="1.2"/>
    <path d="M 65,74 L 65,47" stroke-width="1.0"/>
    <path d="M 65,47 C 57,47 54,41 58,36 C 61,33 65,38 65,47 Z" stroke-width="0.9"/>
    <path d="M 65,47 C 73,47 76,41 72,36 C 69,33 65,38 65,47 Z" stroke-width="0.9"/>
    ''')


# F -- ultra reduced mark: wide rounded bulb + tiny leaf mark, nothing else
def icon_f():
    return g('''
    <path stroke-width="1.4" d="M 65,20
             C 43,20 30,34 30,49
             C 30,63 39,71 48,75
             L 82,75
             C 91,71 100,63 100,49
             C 100,34 87,20 65,20 Z"/>
    <line x1="53" y1="83" x2="77" y2="83" stroke-width="1.2"/>
    <path d="M 65,75 L 65,52" stroke-width="1.0"/>
    <path d="M 65,52 C 58,52 55,46 59,41 C 62,38 65,43 65,52 Z" stroke-width="0.9"/>
    <path d="M 65,52 C 72,52 75,46 71,41 C 68,38 65,43 65,52 Z" stroke-width="0.9"/>
    ''')


VARIANTS = [
    ("A", "Literal brief (wide/short, 6 rays, 2 rings)", icon_a),
    ("B", "Monoline minimal (one contour, no rays)", icon_b),
    ("C", "Halo ring (dotted ring instead of rays)", icon_c),
    ("D", "Merged leaf-bulb (growth built into silhouette)", icon_d),
    ("E", "Faceted geometric (angular shoulders)", icon_e),
    ("F", "Ultra reduced (bulb + leaf mark only)", icon_f),
]


def build_sheet():
    cols = 3
    rows = 2
    cell = 260
    label_h = 34
    w = cell * cols
    h = (cell + label_h) * rows
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    parts.append(f'<rect width="{w}" height="{h}" fill="white"/>')
    for i, (letter, label, fn) in enumerate(VARIANTS):
        col = i % cols
        row = i // cols
        x0 = col * cell
        y0 = row * (cell + label_h)
        icon_scale = 1.8
        icon_offset = (cell - 130 * icon_scale) / 2
        parts.append(f'<g transform="translate({x0+icon_offset},{y0}) scale({icon_scale})">{fn()}</g>')
        parts.append(f'<text x="{x0+cell/2}" y="{y0+cell+22}" text-anchor="middle" '
                      f'font-family="sans-serif" font-size="15" fill="#111">{letter} — {label}</text>')
        if col > 0:
            parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+cell+label_h}" stroke="#eee"/>')
        if row > 0 and col == 0:
            parts.append(f'<line x1="0" y1="{y0}" x2="{w}" y2="{y0}" stroke="#eee"/>')
    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build_sheet()
    with open(os.path.join(OUT_DIR, "sheet2.svg"), "w") as f:
        f.write(svg)
    for letter, label, fn in VARIANTS:
        single = f'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="390" viewBox="0 0 130 130">{fn()}</svg>'
        with open(os.path.join(OUT_DIR, f"icon2_{letter}.svg"), "w") as f:
            f.write(single)
    print("wrote sheet2.svg and icon2_A..F.svg")
