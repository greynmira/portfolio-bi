#!/usr/bin/env python3
"""Fourth round: three conceptually distinct lightbulb/sprout marks, per
explicit reference direction -- wider/shorter classic-bulb silhouette
(not an egg), a bold 2-leaf sprout as the focal point (not a tiny detail),
a minimal 2-ring socket, and no rays. Local box 130x110.

1. Minimal bulb + bold sprout -- traditional layout, fixed proportions
2. Continuous-line bulb -- the sprout visually grows out of the bulb's
   own contour rather than sitting separately inside it
3. Sprout-AS-filament -- the two leaves occupy the filament's role
   (the "idea + growth" concept merge), not a plant placed in a bulb
"""
import os

GREEN = "#0F4D3C"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
CX = 65.0


def wrap(*parts, sw="1.5"):
    body = "".join(parts)
    return (f'<g fill="none" stroke="{GREEN}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g>')


NECK_Y = 76.0


def classic_bulb(sw="1.5"):
    """Rounded top, clear shoulders, a graceful S-curve taper into the
    neck -- a classic bulb silhouette, not an egg and not a flat oval."""
    return (f'<path stroke-width="{sw}" d="M {CX},14 '
            f'C {CX-19},15 {CX-30},24 {CX-30},38 '
            f'C {CX-30},54 {CX-25},68 {CX-13},{NECK_Y:.0f} '
            f'L {CX+13},{NECK_Y:.0f} '
            f'C {CX+25},68 {CX+30},54 {CX+30},38 '
            f'C {CX+30},24 {CX+19},15 {CX},14 Z"/>')


def socket(sw="1.3"):
    """Two elegant curved rings, nothing else."""
    return (f'<g stroke-width="{sw}">'
            f'<path d="M {CX-16},{NECK_Y+6:.0f} Q {CX},{NECK_Y+9:.0f} {CX+16},{NECK_Y+6:.0f}"/>'
            f'<path d="M {CX-14},{NECK_Y+14:.0f} Q {CX},{NECK_Y+17:.0f} {CX+14},{NECK_Y+14:.0f}"/>'
            f'</g>')


# ---------------------------------------------------------------------
# 1. Minimal bulb + bold sprout: short centered stem, two large simple
#    almond leaves (not loops, not circles)
# ---------------------------------------------------------------------
def icon_1():
    branch = 60.0
    stem = f'<path stroke-width="1.1" d="M {CX},{NECK_Y:.0f} L {CX},{branch}"/>'
    # almond leaf: pointed at both ends, widest at the middle -- one bezier
    # bulge out, mirrored back in, per side
    def leaf(sign):
        tip = (CX + sign * 2, 34.0)
        return (f'<path stroke-width="1.0" d="M {CX},{branch} '
                f'C {CX+sign*13},{branch-2} {CX+sign*13},{tip[1]+8} {tip[0]},{tip[1]} '
                f'C {CX+sign*4},{tip[1]+8} {CX+sign*2},{branch-6} {CX},{branch} Z"/>')
    return wrap(classic_bulb(), socket(), stem, leaf(-1), leaf(1))


# ---------------------------------------------------------------------
# 2. Continuous-line bulb: the sprout's stem tangentially continues the
#    bulb's own inner contour -- grown FROM the bulb, not placed inside it
# ---------------------------------------------------------------------
def icon_2():
    bulb = (f'<path stroke-width="1.5" d="M {CX},14 '
            f'C {CX-19},15 {CX-30},24 {CX-30},38 '
            f'C {CX-30},54 {CX-25},68 {CX-13},{NECK_Y:.0f} '
            f'L {CX+13},{NECK_Y:.0f} '
            f'C {CX+25},68 {CX+30},54 {CX+30},38 '
            f'C {CX+30},24 {CX+19},15 {CX},14 '
            # continue the same stroke inward and up into the stem/sprout,
            # instead of starting a new disconnected path
            f'M {CX-13},{NECK_Y:.0f} C {CX-9},69 {CX-4},64 {CX},62 '
            f'C {CX+4},64 {CX+9},69 {CX+13},{NECK_Y:.0f}"/>')
    branch = 62.0
    def leaf(sign):
        tip = (CX + sign * 2, 33.0)
        return (f'<path stroke-width="1.0" d="M {CX},{branch} '
                f'C {CX+sign*14},{branch-3} {CX+sign*14},{tip[1]+7} {tip[0]},{tip[1]} '
                f'C {CX+sign*4},{tip[1]+8} {CX+sign*2},{branch-6} {CX},{branch} Z"/>')
    return wrap(bulb, socket(), leaf(-1), leaf(1))


# ---------------------------------------------------------------------
# 3. Sprout-AS-filament: the two leaves splay wider and taller, occupying
#    the filament's visual role at the bulb's center -- "ideas that grow"
#    rather than "a plant in a bulb"
# ---------------------------------------------------------------------
def icon_3():
    branch = 70.0
    top = 28.0
    stem = f'<path stroke-width="1.1" d="M {CX},{NECK_Y:.0f} L {CX},{branch}"/>'
    def leaf(sign):
        tip = (CX + sign * 3, top)
        return (f'<path stroke-width="1.05" d="M {CX},{branch} '
                f'C {CX+sign*19},{branch-4} {CX+sign*17},{top+10} {tip[0]},{tip[1]} '
                f'C {CX+sign*6},{top+9} {CX+sign*3},{branch-8} {CX},{branch} Z"/>')
    return wrap(classic_bulb(), socket(), stem, leaf(-1), leaf(1))


VARIANTS = [
    ("1", "Minimal bulb + bold sprout", icon_1),
    ("2", "Continuous-line bulb", icon_2),
    ("3", "Sprout-as-filament", icon_3),
]


def build_sheet():
    cell = 300
    label_h = 34
    w = cell * 3
    h = cell + label_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    parts.append(f'<rect width="{w}" height="{h}" fill="white"/>')
    for i, (letter, label, fn) in enumerate(VARIANTS):
        x0 = i * cell
        icon_scale = 2.2
        icon_offset_x = (cell - 130 * icon_scale) / 2
        icon_offset_y = (cell - 110 * icon_scale) / 2
        parts.append(f'<g transform="translate({x0+icon_offset_x},{icon_offset_y}) scale({icon_scale})">{fn()}</g>')
        parts.append(f'<text x="{x0+cell/2}" y="{cell+22}" text-anchor="middle" '
                      f'font-family="sans-serif" font-size="16" fill="#111">{letter}. {label}</text>')
        if i > 0:
            parts.append(f'<line x1="{x0}" y1="0" x2="{x0}" y2="{h}" stroke="#eee"/>')
    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    with open(os.path.join(OUT_DIR, "sheet4.svg"), "w") as f:
        f.write(build_sheet())
    for letter, label, fn in VARIANTS:
        single = f'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="330" viewBox="0 0 130 110">{fn()}</svg>'
        with open(os.path.join(OUT_DIR, f"icon4_{letter}.svg"), "w") as f:
            f.write(single)
    print("wrote sheet4.svg and icon4_1..3.svg")
