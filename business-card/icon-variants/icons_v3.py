#!/usr/bin/env python3
"""Third round of lightbulb-mark concepts. Every concept shares refined
sub-components built to spec (short integrated stem, larger organic
sprout, 3-ring socket, thin symmetric rays) and varies only the bulb
silhouette -- plus one explicit rays-vs-no-rays twin pair."""
import os

GREEN = "#0F4D3C"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def rays(cx=50, top_y=52, r_inner=36, r_outer=46, sw="1.05"):
    """5 thin symmetric rays: top, 2 upper-diagonal, 2 horizontal."""
    import math
    dirs = [(-90, 1.0), (-145, 1.0), (-35, 1.0), (180, 0.82), (0, 0.82)]
    lines = []
    for deg, scale in dirs:
        rad = math.radians(deg)
        x1 = cx + r_inner * scale * math.cos(rad)
        y1 = top_y + r_inner * scale * math.sin(rad)
        x2 = cx + r_outer * scale * math.cos(rad)
        y2 = top_y + r_outer * scale * math.sin(rad)
        lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    return f'<g stroke-width="{sw}">' + "".join(lines) + '</g>'


def socket(cx, neck_bottom_y, half_w, sw="1.15"):
    """3 evenly spaced floating rings, tapering slightly, rounded joins."""
    y1, y2, y3 = neck_bottom_y + 4, neck_bottom_y + 12, neck_bottom_y + 20
    w1, w2, w3 = half_w, half_w * 0.82, half_w * 0.62
    return (f'<g stroke-width="{sw}">'
            f'<line x1="{cx-w1:.1f}" y1="{y1}" x2="{cx+w1:.1f}" y2="{y1}"/>'
            f'<line x1="{cx-w2:.1f}" y1="{y2}" x2="{cx+w2:.1f}" y2="{y2}"/>'
            f'<line x1="{cx-w3:.1f}" y1="{y3}" x2="{cx+w3:.1f}" y2="{y3}"/>'
            f'</g>')


def stem_and_sprout(cx, neck_bottom_y, sw_stem="0.95", sw_leaf="0.85", scale=1.15):
    """Short stem integrated into the socket top + the proven twin-loop
    sprout (two clearly separate leaves, not a merged almond), scaled up
    ~15% from the version that read well previously."""
    branch = neck_bottom_y - 18
    # relative offsets from the branch point, lifted from the well-received
    # v10 sprout and scaled -- keeps two distinct loops, not a merged blob
    c1a, c1b, tip = (-5 * scale, 0), (-7 * scale, -5 * scale), (-4 * scale, -8.5 * scale)
    c2a, c2b = (-2 * scale, -10.5 * scale), (0, -7 * scale)
    stem = f'<path d="M {cx},{neck_bottom_y+6} L {cx},{branch:.1f}" stroke-width="{sw_stem}"/>'

    def leaf(sign):
        return (f'<path d="M {cx},{branch:.1f} '
                f'C {cx+sign*c1a[0]:.1f},{branch+c1a[1]:.1f} {cx+sign*c1b[0]:.1f},{branch+c1b[1]:.1f} '
                f'{cx+sign*tip[0]:.1f},{branch+tip[1]:.1f} '
                f'C {cx+sign*c2a[0]:.1f},{branch+c2a[1]:.1f} {cx+sign*c2b[0]:.1f},{branch+c2b[1]:.1f} '
                f'{cx},{branch:.1f} Z" stroke-width="{sw_leaf}"/>')

    return stem + leaf(-1) + leaf(1)


def wrap(*parts, sw="1.5"):
    body = "".join(parts)
    return (f'<g fill="none" stroke="{GREEN}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g>')


CX = 65


# G -- refined classic: gently wider/shorter bulb, softened shoulders, WITH rays
def bulb_g():
    return (f'<path stroke-width="1.5" d="M {CX},18 '
            f'C {CX-20},19 {CX-27},33 {CX-27},48 '
            f'C {CX-27},60 {CX-21},70 {CX-16},76 '
            f'L {CX+16},76 '
            f'C {CX+21},70 {CX+27},60 {CX+27},48 '
            f'C {CX+27},33 {CX+20},19 {CX},18 Z"/>')


def icon_g():
    return wrap(rays(cx=CX, top_y=50, r_inner=32, r_outer=42), bulb_g(), socket(CX, 76, 15), stem_and_sprout(CX, 76))


# H -- G's twin, rays removed
def icon_h():
    return wrap(bulb_g(), socket(CX, 76, 15), stem_and_sprout(CX, 76))


# I -- soft squircle: rounder shoulders, flatter apex
def icon_i():
    b = (f'<path stroke-width="1.5" d="M {CX-11},19 '
         f'C {CX-22},21 {CX-28},34 {CX-28},48 '
         f'C {CX-28},60 {CX-22},70 {CX-17},76 '
         f'L {CX+17},76 '
         f'C {CX+22},70 {CX+28},60 {CX+28},48 '
         f'C {CX+28},34 {CX+22},21 {CX+11},19 '
         f'C {CX+6},17.5 {CX-6},17.5 {CX-11},19 Z"/>')
    return wrap(rays(cx=CX, top_y=50, r_inner=33, r_outer=43), b, socket(CX, 76, 16), stem_and_sprout(CX, 76))


# J -- gentle teardrop: rounder top, slightly more taper toward the socket
def icon_j():
    b = (f'<path stroke-width="1.5" d="M {CX},17 '
         f'C {CX-19},18 {CX-26},32 {CX-26},47 '
         f'C {CX-26},59 {CX-19},69 {CX-13},75 '
         f'L {CX+13},75 '
         f'C {CX+19},69 {CX+26},59 {CX+26},47 '
         f'C {CX+26},32 {CX+19},18 {CX},17 Z"/>')
    return wrap(rays(cx=CX, top_y=49, r_inner=31, r_outer=41), b, socket(CX, 75, 13), stem_and_sprout(CX, 75))


# K -- wide dome: pushed a bit wider still, rounder shoulders, shortest
def icon_k():
    b = (f'<path stroke-width="1.5" d="M {CX},21 '
         f'C {CX-23},22 {CX-30},35 {CX-30},48 '
         f'C {CX-30},58 {CX-24},67 {CX-18},72 '
         f'L {CX+18},72 '
         f'C {CX+24},67 {CX+30},58 {CX+30},48 '
         f'C {CX+30},35 {CX+23},22 {CX},21 Z"/>')
    return wrap(rays(cx=CX, top_y=52, r_inner=34, r_outer=44), b, socket(CX, 72, 17), stem_and_sprout(CX, 72, scale=1.1))


# L -- compact balanced: closest to prior proportions but corrected, thinnest strokes
def icon_l():
    b = (f'<path stroke-width="1.3" d="M {CX},19 '
         f'C {CX-18},20 {CX-25},33 {CX-25},47 '
         f'C {CX-25},58 {CX-19},68 {CX-14},74 '
         f'L {CX+14},74 '
         f'C {CX+19},68 {CX+25},58 {CX+25},47 '
         f'C {CX+25},33 {CX+18},20 {CX},19 Z"/>')
    return wrap(rays(cx=CX, top_y=50, r_inner=32, r_outer=41, sw="0.9"), b,
                socket(CX, 74, 13, sw="1.0"), stem_and_sprout(CX, 74, sw_stem="0.85", sw_leaf="0.75"), sw="1.3")


VARIANTS = [
    ("G", "Refined classic + rays", icon_g),
    ("H", "Refined classic, NO rays", icon_h),
    ("I", "Soft squircle", icon_i),
    ("J", "Gentle teardrop", icon_j),
    ("K", "Wide dome", icon_k),
    ("L", "Compact balanced (thinnest)", icon_l),
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
        icon_scale = 1.7
        icon_offset_x = (cell - 130 * icon_scale) / 2
        icon_offset_y = (cell - 120 * icon_scale) / 2
        parts.append(f'<g transform="translate({x0+icon_offset_x},{y0+icon_offset_y}) scale({icon_scale})">{fn()}</g>')
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
    with open(os.path.join(OUT_DIR, "sheet3.svg"), "w") as f:
        f.write(svg)
    for letter, label, fn in VARIANTS:
        single = f'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="360" viewBox="0 0 130 120">{fn()}</svg>'
        with open(os.path.join(OUT_DIR, f"icon3_{letter}.svg"), "w") as f:
            f.write(single)
    print("wrote sheet3.svg and icon3_G..L.svg")
