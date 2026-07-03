#!/usr/bin/env python3
"""Five alternative lightbulb+sprout logo sketches, local coord box 100x120.
Contact-sheet render for picking a direction; not wired into the card yet."""
import os

GREEN = "#0F4D3C"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def wrap(body, sw="2.2"):
    return f'''<g fill="none" stroke="{GREEN}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">
{body}
</g>'''


# A -- current card icon: round bulb, threaded base, 5 dash rays, twin-leaf sprout
def icon_a():
    return wrap('''
    <line x1="50" y1="6"  x2="50" y2="14"/>
    <line x1="27" y1="13" x2="32" y2="20"/>
    <line x1="73" y1="13" x2="68" y2="20"/>
    <line x1="16" y1="34" x2="24" y2="34"/>
    <line x1="84" y1="34" x2="76" y2="34"/>
    <path d="M 40,72 C 30,72 21,62 21,46 C 21,27 34,16 50,16
             C 66,16 79,27 79,46 C 79,62 70,72 60,72 Z"/>
    <path d="M 41,72 L 41,88 Q 41,93 46,93 L 54,93 Q 59,93 59,88 L 59,72"/>
    <line x1="42.5" y1="77" x2="57.5" y2="77"/>
    <line x1="42.5" y1="82" x2="57.5" y2="82"/>
    <line x1="42.5" y1="87" x2="57.5" y2="87"/>
    <path d="M 50,68 L 50,40" stroke-width="1.6"/>
    <path d="M 50,54 C 43,54 40,48 41,42 C 47,42 51,47 50,54 Z" stroke-width="1.4"/>
    <path d="M 50,58 C 57,58 60,52 59,46 C 53,46 49,51 50,58 Z" stroke-width="1.4"/>
    ''')


# B -- classic elongated Edison bulb, flat single-bar base, minimal 3-ray top fan
def icon_b():
    return wrap('''
    <line x1="50" y1="4"  x2="50" y2="13"/>
    <line x1="30" y1="10" x2="36" y2="18"/>
    <line x1="70" y1="10" x2="64" y2="18"/>
    <path d="M 44,76 C 32,73 24,61 25,45 C 26,24 36,14 50,14
             C 64,14 74,24 75,45 C 76,61 68,73 56,76 Z"/>
    <path d="M 43,76 L 43,84 L 57,84 L 57,76"/>
    <line x1="43" y1="89" x2="57" y2="89"/>
    <path d="M 50,70 L 50,38" stroke-width="1.5"/>
    <path d="M 50,52 C 42,52 39,45 40,38 C 47,38 51,44 50,52 Z" stroke-width="1.3"/>
    <path d="M 50,56 C 58,56 61,49 60,42 C 53,42 49,48 50,56 Z" stroke-width="1.3"/>
    ''')


# C -- modern geometric, rounded-square globe, flat bar base, no rays, single leaf
def icon_c():
    return wrap('''
    <rect x="24" y="16" rx="18" ry="18" width="52" height="58"/>
    <path d="M 40,74 L 40,86 Q 40,90 44,90 L 56,90 Q 60,90 60,86 L 60,74"/>
    <line x1="42" y1="80" x2="58" y2="80"/>
    <path d="M 50,68 L 50,44" stroke-width="1.6"/>
    <path d="M 50,50 C 43,50 39,44 40,37 C 47,37 51,43 50,50 Z" stroke-width="1.3"/>
    ''')


# D -- friendly modern, thicker stroke, dotted rays, bigger sprout
def icon_d():
    body = '''
    <circle cx="50" cy="10" r="1.6" fill="{c}" stroke="none"/>
    <circle cx="26" cy="19" r="1.6" fill="{c}" stroke="none"/>
    <circle cx="74" cy="19" r="1.6" fill="{c}" stroke="none"/>
    <circle cx="17" cy="42" r="1.6" fill="{c}" stroke="none"/>
    <circle cx="83" cy="42" r="1.6" fill="{c}" stroke="none"/>
    <path d="M 39,73 C 28,73 20,62 20,47 C 20,28 33,17 50,17
             C 67,17 80,28 80,47 C 80,62 72,73 61,73 Z"/>
    <path d="M 40,73 L 40,89 Q 40,94 45,94 L 55,94 Q 60,94 60,89 L 60,73"/>
    <line x1="41.5" y1="78" x2="58.5" y2="78"/>
    <line x1="41.5" y1="83.5" x2="58.5" y2="83.5"/>
    <path d="M 50,69 L 50,36" stroke-width="1.8"/>
    <path d="M 50,53 C 41,53 37,46 38,38 C 46,38 51,45 50,53 Z" stroke-width="1.6"/>
    <path d="M 50,58 C 59,58 63,51 62,43 C 54,43 49,50 50,58 Z" stroke-width="1.6"/>
    '''.format(c=GREEN)
    return wrap(body, sw="2.6")


# E -- ultra-minimal single-line bulb, dashed glow arc, tiny sprout
def icon_e():
    return wrap('''
    <path d="M 24,30 A 30,30 0 0 1 30,16" stroke-dasharray="1,5"/>
    <path d="M 76,30 A 30,30 0 0 0 70,16" stroke-dasharray="1,5"/>
    <path d="M 50,4 L 50,11" stroke-dasharray="1,5"/>
    <path d="M 41,71 C 30,71 22,60 22,45 C 22,26 34,15 50,15
             C 66,15 78,26 78,45 C 78,60 70,71 59,71 Z" stroke-width="1.8"/>
    <path d="M 42,71 L 42,90 L 58,90 L 58,71" stroke-width="1.8"/>
    <path d="M 50,66 L 50,42" stroke-width="1.3"/>
    <path d="M 50,54 C 44,54 41,49 42,44 C 47,44 51,48 50,54 Z" stroke-width="1.1"/>
    ''', sw="1.8")


VARIANTS = [
    ("A - current (round, threaded base, sprout)", icon_a),
    ("B - classic Edison (elongated, flat base)", icon_b),
    ("C - modern geometric (rounded square, no rays)", icon_c),
    ("D - friendly bold (thick stroke, dotted rays)", icon_d),
    ("E - ultra-minimal (dashed glow, single line)", icon_e),
]


def build_sheet():
    cols = 5
    cell = 200
    label_h = 26
    w = cell * cols
    h = cell + label_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    parts.append(f'<rect width="{w}" height="{h}" fill="white"/>')
    for i, (label, fn) in enumerate(VARIANTS):
        x0 = i * cell
        scale = (cell - 40) / 120.0
        tx = x0 + (cell - 100 * scale) / 2
        ty = 10
        parts.append(f'<g transform="translate({tx},{ty}) scale({scale})">{fn()}</g>')
        letter = label[0]
        parts.append(f'<text x="{x0+cell/2}" y="{h-8}" text-anchor="middle" '
                      f'font-family="sans-serif" font-size="14" fill="#111">{letter}</text>')
        if i > 0:
            parts.append(f'<line x1="{x0}" y1="0" x2="{x0}" y2="{h}" stroke="#eee" stroke-width="1"/>')
    parts.append('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build_sheet()
    with open(os.path.join(OUT_DIR, "sheet.svg"), "w") as f:
        f.write(svg)
    for i, (label, fn) in enumerate(VARIANTS):
        letter = label[0]
        single = f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="360" viewBox="0 0 100 120">{fn()}</svg>'
        with open(os.path.join(OUT_DIR, f"icon_{letter}.svg"), "w") as f:
            f.write(single)
    print("wrote sheet.svg and icon_A..E.svg")
