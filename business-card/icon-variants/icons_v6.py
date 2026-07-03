#!/usr/bin/env python3
"""Sixth round: strip the badge treatment entirely (no ring, no sparkles,
no literal bold M) and rebuild the bulb itself thinner/softer/wider with a
simplified 2-3 ring socket, per explicit direction. Three lockups, varying
only the interior "filament":
1. Bulb only -- no interior mark at all, purely symbolic
2. Bulb + custom abstract filament -- two asymmetric curved lines evoking
   a spark/perspective-lines mark, not literal plant or letter
3. Bulb + M-as-filament -- the M is redrawn as a thin thread-weight zigzag
   (same stroke width as the bulb itself), not a bold filled letterform,
   so it reads as a filament coil first and a monogram second
"""
import os

GREEN = "#0F4D3C"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
CX = 70.0
STROKE = 3.0   # thin, ~15% lighter than the last round's 3.6-5.6 range


def wrap(*parts, sw=None):
    sw = sw or STROKE
    body = "".join(parts)
    return (f'<g fill="none" stroke="{GREEN}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g>')


def bulb(sw=None):
    """Softer shoulders, wider body, thinner neck -- one continuous taper,
    ~15% larger and thinner-stroked than the badge-mark bulb."""
    sw = sw or STROKE
    return (f'<path stroke-width="{sw}" d="M {CX},12 '
            f'C {CX-30},13 {CX-42},30 {CX-42},50 '
            f'C {CX-42},70 {CX-30},86 {CX-15},96 '
            f'C {CX-13},99 {CX-12},101 {CX-12},104 '
            f'L {CX+12},104 '
            f'C {CX+12},101 {CX+13},99 {CX+15},96 '
            f'C {CX+30},86 {CX+42},70 {CX+42},50 '
            f'C {CX+42},30 {CX+30},13 {CX},12 Z"/>')


def socket(sw=None):
    """2 thin curved rings, generous spacing -- simplified from the
    previous filled-bar socket."""
    sw = sw or STROKE * 0.85
    return (f'<g stroke-width="{sw}">'
            f'<path d="M {CX-15},112 Q {CX},116 {CX+15},112"/>'
            f'<path d="M {CX-12},124 Q {CX},128 {CX+12},124"/>'
            f'</g>')


# ---------------------------------------------------------------------
# 1. Bulb only -- no filament, purely symbolic
# ---------------------------------------------------------------------
def icon_1():
    return wrap(bulb(), socket())


# ---------------------------------------------------------------------
# 2. Bulb + custom abstract filament: two asymmetric curved lines rising
#    from a shared base, one short and direct, one longer and arcing --
#    reads as a spark or a subtle perspective/growth mark, not a plant
# ---------------------------------------------------------------------
def icon_2():
    base = (CX, 92)
    filament = (
        f'<path stroke-width="{STROKE*0.8}" d="M {base[0]},{base[1]} '
        f'C {base[0]-2},78 {base[0]-14},64 {base[0]-16},46"/>'
        f'<path stroke-width="{STROKE*0.8}" d="M {base[0]},{base[1]} '
        f'C {base[0]+3},74 {base[0]+8},58 {base[0]+6},38"/>'
    )
    return wrap(bulb(), socket(), filament)


# ---------------------------------------------------------------------
# 3. Bulb + M-as-filament: a thin thread-weight zigzag (same weight as
#    the bulb stroke), not a bold filled letter -- filament first,
#    monogram second
# ---------------------------------------------------------------------
def icon_3():
    m = (f'<path stroke-width="{STROKE*0.78}" d="M {CX-17},92 '
         f'L {CX-17},46 L {CX},70 L {CX+17},46 L {CX+17},92"/>')
    return wrap(bulb(), socket(), m)


VARIANTS = [
    ("1", "Bulb only", icon_1),
    ("2", "Bulb + abstract filament", icon_2),
    ("3", "Bulb + M-as-filament", icon_3),
]


def build_sheet():
    cell = 260
    label_h = 32
    w = cell * 3
    h = cell + label_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    parts.append(f'<rect width="{w}" height="{h}" fill="white"/>')
    for i, (letter, label, fn) in enumerate(VARIANTS):
        x0 = i * cell
        icon_scale = 1.7
        icon_w = 140 * icon_scale
        icon_h = 116 * icon_scale
        icon_offset_x = x0 + (cell - icon_w) / 2
        icon_offset_y = (cell - icon_h) / 2
        parts.append(f'<g transform="translate({icon_offset_x},{icon_offset_y}) scale({icon_scale})">{fn()}</g>')
        parts.append(f'<text x="{x0+cell/2}" y="{cell+22}" text-anchor="middle" '
                      f'font-family="sans-serif" font-size="15" fill="#111">{letter}. {label}</text>')
        if i > 0:
            parts.append(f'<line x1="{x0}" y1="0" x2="{x0}" y2="{h}" stroke="#eee"/>')
    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    with open(os.path.join(OUT_DIR, "sheet6.svg"), "w") as f:
        f.write(build_sheet())
    for letter, label, fn in VARIANTS:
        single = f'<svg xmlns="http://www.w3.org/2000/svg" width="420" height="348" viewBox="0 0 140 116">{fn()}</svg>'
        with open(os.path.join(OUT_DIR, f"icon6_{letter}.svg"), "w") as f:
            f.write(single)
    print("wrote sheet6.svg and icon6_1..3.svg")
