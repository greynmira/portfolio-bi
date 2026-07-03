#!/usr/bin/env python3
"""Generates front.svg and back.svg for the Reimagined by Mira business card.

True vector output: hand-authored paths/text, no traced raster art.
Document units = points (1pt = 1/72in). Card = 3.75x2.25in with 0.125in bleed
on a 3.5x2in finished size.
"""
import os
import qrcode
from fontTools.ttLib import TTFont

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- font metrics (for exact text measurement / layout) ----
FONT_FILES = {
    ("Montserrat", "normal"): "/usr/share/fonts/truetype/montserrat/Montserrat-Regular.ttf",
    ("Montserrat", "500"): "/usr/share/fonts/truetype/montserrat/Montserrat-Medium.ttf",
    ("Montserrat", "600"): "/usr/share/fonts/truetype/montserrat/Montserrat-SemiBold.ttf",
    ("Montserrat", "700"): "/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf",
    ("EB Garamond", "normal"): "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Regular.ttf",
    ("EB Garamond", "600"): "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Bold.ttf",
    ("EB Garamond", "italic"): "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Italic.ttf",
}
_metrics_cache = {}


def _get_font_metrics(family, weight, style):
    key = (family, "italic" if style == "italic" else weight)
    if key not in FONT_FILES:
        key = (family, "normal")
    if key in _metrics_cache:
        return _metrics_cache[key]
    tt = TTFont(FONT_FILES[key])
    units_per_em = tt["head"].unitsPerEm
    cmap = tt.getBestCmap()
    hmtx = tt["hmtx"]
    glyph_set = tt.getGlyphSet()
    _metrics_cache[key] = (units_per_em, cmap, hmtx, glyph_set)
    return _metrics_cache[key]


def text_width(text, family, size, weight="normal", style="normal", letter_spacing_em=0.0):
    """Exact rendered width in points, using real glyph advance widths."""
    units_per_em, cmap, hmtx, _ = _get_font_metrics(family, weight, style)
    total_units = 0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            gname = cmap.get(ord(" "))
        total_units += hmtx[gname][0]
    width = total_units / units_per_em * size
    if letter_spacing_em and text:
        width += letter_spacing_em * size * len(text)
    return width


_ascent_descent_cache = {}


def ascent_descent(family, size, weight="normal", style="normal"):
    """Real ascent/descent (positive pt) at the given size, from hhea."""
    key = (family, weight, style)
    if key not in _ascent_descent_cache:
        k2 = (family, "italic" if style == "italic" else weight)
        if k2 not in FONT_FILES:
            k2 = (family, "normal")
        tt = TTFont(FONT_FILES[k2])
        units_per_em = tt["head"].unitsPerEm
        hhea = tt["hhea"]
        _ascent_descent_cache[key] = (hhea.ascent / units_per_em, -hhea.descent / units_per_em)
    a, d = _ascent_descent_cache[key]
    return a * size, d * size

# ---- geometry (points) ----
DOC_W, DOC_H = 270.0, 162.0        # 3.75in x 2.25in (bleed doc)
BLEED = 9.0                         # 0.125in
TRIM_X, TRIM_Y = BLEED, BLEED
TRIM_W, TRIM_H = DOC_W - 2 * BLEED, DOC_H - 2 * BLEED   # 252 x 144 = 3.5 x 2in
SAFE = 9.0                          # 0.125in safe margin inside trim
SAFE_X, SAFE_Y = TRIM_X + SAFE, TRIM_Y + SAFE
SAFE_W, SAFE_H = TRIM_W - 2 * SAFE, TRIM_H - 2 * SAFE   # 234 x 126
CENTER_X = DOC_W / 2

# ---- palette ----
WHITE = "#FFFFFF"
GREEN = "#0F4D3C"
TEXT = "#000000"   # pure K-only black for print (was #111111, a near-black gray)

SERIF = "EB Garamond"
SANS = "Montserrat"

SVG_HEAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="{win}in" height="{hin}in" viewBox="0 0 {w} {h}">\n'
).format(win=DOC_W / 72.0, hin=DOC_H / 72.0, w=DOC_W, h=DOC_H)


def lightbulb_icon(cx, top_y, width, with_rays=False):
    """Lightbulb-with-sprout mark, round 3. Local box is 130x120 units: a
    properly rounded (not elongated) globe with soft shoulders, a compact
    stem integrated into a 3-ring socket, and an enlarged twin-leaf
    filament. Rays are optional (with_rays=True) -- the no-rays default
    reads cleaner and more editorial; the ray version signals "idea" more
    literally. Both were compared side by side before picking the default.
    """
    LOCAL_W, LOCAL_H = 130.0, 120.0
    LCX = 65.0
    s = width / LOCAL_W
    h = LOCAL_H * s
    tx = cx - width / 2.0
    ty = top_y

    neck_bottom = 76.0
    branch = neck_bottom - 18
    globe = f'''<path stroke-width="1.5" d="M {LCX},18
             C {LCX-20},19 {LCX-27},33 {LCX-27},48
             C {LCX-27},60 {LCX-21},70 {LCX-16},76
             L {LCX+16},76
             C {LCX+21},70 {LCX+27},60 {LCX+27},48
             C {LCX+27},33 {LCX+20},19 {LCX},18 Z"/>'''
    socket = f'''<g stroke-width="1.15">
      <line x1="{LCX-15}" y1="{neck_bottom+4}" x2="{LCX+15}" y2="{neck_bottom+4}"/>
      <line x1="{LCX-12.3}" y1="{neck_bottom+12}" x2="{LCX+12.3}" y2="{neck_bottom+12}"/>
      <line x1="{LCX-9.3}" y1="{neck_bottom+20}" x2="{LCX+9.3}" y2="{neck_bottom+20}"/>
    </g>'''
    stem = f'<path stroke-width="0.95" d="M {LCX},{neck_bottom+6} L {LCX},{branch}"/>'
    # twin-loop filament, ~15% larger than the previous round
    leaf_l = (f'<path stroke-width="0.85" d="M {LCX},{branch} '
              f'C {LCX-5.75},{branch} {LCX-8.05},{branch-5.75} {LCX-4.6},{branch-9.775} '
              f'C {LCX-2.3},{branch-12.075} {LCX},{branch-8.05} {LCX},{branch} Z"/>')
    leaf_r = (f'<path stroke-width="0.85" d="M {LCX},{branch} '
              f'C {LCX+5.75},{branch} {LCX+8.05},{branch-5.75} {LCX+4.6},{branch-9.775} '
              f'C {LCX+2.3},{branch-12.075} {LCX},{branch-8.05} {LCX},{branch} Z"/>')
    rays = ""
    if with_rays:
        rays = f'''<g stroke-width="1.05">
      <line x1="{LCX}" y1="18" x2="{LCX}" y2="8"/>
      <line x1="{LCX-22.6}" y1="27.4" x2="{LCX-29.4}" y2="19.5"/>
      <line x1="{LCX+22.6}" y1="27.4" x2="{LCX+29.4}" y2="19.5"/>
      <line x1="{LCX-32}" y1="50" x2="{LCX-42}" y2="50"/>
      <line x1="{LCX+32}" y1="50" x2="{LCX+42}" y2="50"/>
    </g>'''

    return f'''  <g transform="translate({tx:.3f},{ty:.3f}) scale({s:.5f})"
     fill="none" stroke="{GREEN}" stroke-linecap="round" stroke-linejoin="round">
    {rays}
    {globe}
    {socket}
    {stem}
    {leaf_l}
    {leaf_r}
  </g>
''', h


def centered_text(x, y, text, font_family, size, color, weight="normal",
                   style="normal", letter_spacing_em=0.0, extra=""):
    ls = letter_spacing_em * size
    ls_attr = f' letter-spacing="{ls:.3f}"' if ls else ""
    # visually re-center: letter-spacing adds trailing space after the last glyph
    dx = -ls / 2.0 if ls else 0.0
    return (f'  <text x="{x + dx:.3f}" y="{y:.3f}" text-anchor="middle" '
            f'font-family="{font_family}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{color}"{ls_attr}{extra}>{text}</text>\n')


def left_text(x, y, text, font_family, size, color, weight="normal",
              style="normal", letter_spacing_em=0.0, extra=""):
    ls = letter_spacing_em * size
    ls_attr = f' letter-spacing="{ls:.3f}"' if ls else ""
    return (f'  <text x="{x:.3f}" y="{y:.3f}" text-anchor="start" '
            f'font-family="{font_family}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{color}"{ls_attr}{extra}>{text}</text>\n')


def right_text(x, y, text, font_family, size, color, weight="normal",
               style="normal", letter_spacing_em=0.0, extra=""):
    ls = letter_spacing_em * size
    ls_attr = f' letter-spacing="{ls:.3f}"' if ls else ""
    return (f'  <text x="{x:.3f}" y="{y:.3f}" text-anchor="end" '
            f'font-family="{font_family}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{color}"{ls_attr}{extra}>{text}</text>\n')


def hline(x1, y, x2, color=GREEN, width=0.75):
    return f'  <line x1="{x1:.3f}" y1="{y:.3f}" x2="{x2:.3f}" y2="{y:.3f}" stroke="{color}" stroke-width="{width}"/>\n'


def vline(x, y1, y2, color=GREEN, width=0.75):
    return f'  <line x1="{x:.3f}" y1="{y1:.3f}" x2="{x:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-width="{width}"/>\n'


# =========================================================================
# FRONT
# =========================================================================
def build_front():
    svg = [SVG_HEAD]
    svg.append(f'  <rect x="0" y="0" width="{DOC_W}" height="{DOC_H}" fill="{WHITE}"/>\n')

    icon_top = 30.7   # re-centers the shorter overall block in the trim box
    icon_svg, icon_h = lightbulb_icon(CENTER_X, icon_top, 62)  # +20% (was 52)
    svg.append(icon_svg)
    icon_bottom = icon_top + icon_h

    name_y = icon_bottom + 5   # lockup tightened further (was 16)
    svg.append(centered_text(CENTER_X, name_y, "Reimagined by Mira", SERIF, 26.25, TEXT, weight="600"))  # +5%

    strategy_y = name_y + 17
    strategy_text = "CAREER STRATEGY"
    ls_em = 0.28 * 0.88 * 0.9   # tracking reduced a further ~10%
    font_size = 9.0
    text_w = text_width(strategy_text, SANS, font_size, weight="600", letter_spacing_em=ls_em)
    gap = 10
    line_len = 32   # lengthened a further ~15% (was 28)
    svg.append(hline(CENTER_X - text_w / 2 - gap - line_len, strategy_y - 3, CENTER_X - text_w / 2 - gap))
    svg.append(hline(CENTER_X + text_w / 2 + gap, strategy_y - 3, CENTER_X + text_w / 2 + gap + line_len))
    svg.append(centered_text(CENTER_X, strategy_y, strategy_text, SANS, font_size, GREEN,
                              weight="600", letter_spacing_em=ls_em))

    tagline_y = strategy_y + 18
    svg.append(centered_text(CENTER_X, tagline_y, "Build Your Next Move.", SERIF, 11.9, GREEN, style="italic"))  # -5%

    svg.append('</svg>\n')
    return "".join(svg)


# =========================================================================
# BACK
# =========================================================================
def make_qr_svg(url, module_color, box_x, box_y, box_size):
    qr = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    n = len(matrix)
    cell = box_size / n
    parts = []
    for r, row in enumerate(matrix):
        run_start = None
        for c, val in enumerate(row + [False]):
            if val and run_start is None:
                run_start = c
            elif not val and run_start is not None:
                x = box_x + run_start * cell
                y = box_y + r * cell
                w = (c - run_start) * cell
                parts.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{cell:.3f}" fill="{module_color}"/>')
                run_start = None
    return "  " + "\n  ".join(parts) + "\n", n


def build_back():
    svg = [SVG_HEAD]
    svg.append(f'  <rect x="0" y="0" width="{DOC_W}" height="{DOC_H}" fill="{WHITE}"/>\n')

    left_x = SAFE_X + 2
    right_edge = TRIM_X + TRIM_W - SAFE - 2  # 250 with SAFE=9 setup below

    # -- QR block (top right) --
    qr_module_size = 68.4 * 1.09   # 0.95in minimum, +9%
    # pad must clear a >=4-module quiet zone (QR spec) and exceed rx so the
    # rounded corner never clips into the finder-pattern squares
    pad = 12.0
    outline_size = qr_module_size + 2 * pad
    outline_x = right_edge - outline_size   # right edge now shares the same grid line as the CTA row/website
    outline_y = SAFE_Y + 3   # nudged down to optically center against the copy block
    rx = 6

    qr_x = outline_x + pad
    qr_y = outline_y + pad
    qr_svg, n_modules = make_qr_svg("https://reimaginedbymira.com", GREEN, qr_x, qr_y, qr_module_size)

    svg.append(f'  <rect x="{outline_x:.3f}" y="{outline_y:.3f}" width="{outline_size:.3f}" height="{outline_size:.3f}" '
               f'rx="{rx}" fill="{WHITE}" stroke="{GREEN}" stroke-width="0.56"/>\n')  # -30% from 0.8
    svg.append(qr_svg)

    # -- header (two lines) --
    header_y1 = SAFE_Y + 12
    header_y2 = header_y1 + 13
    svg.append(left_text(left_x, header_y1, "Most career advice", SANS, 10.5, TEXT, weight="500"))
    svg.append(left_text(left_x, header_y2, "focuses on what to do.", SANS, 10.5, TEXT, weight="500"))

    italic_y = header_y2 + 15
    svg.append(left_text(left_x, italic_y, "I focus on how to think.", SERIF, 12, GREEN, style="italic"))

    divider1_y = italic_y + 9
    svg.append(hline(left_x, divider1_y, left_x + 50.4, width=0.9))

    b_y1 = divider1_y + 15
    b_y2 = b_y1 + 13
    b_y3 = b_y2 + 13
    svg.append(left_text(left_x, b_y1, "Gain perspective.", SANS, 9.5, TEXT))
    svg.append(left_text(left_x, b_y2, "Build a strategy.", SANS, 9.5, TEXT))
    svg.append(left_text(left_x, b_y3, "Move forward with clarity.", SANS, 9.5, TEXT))

    # -- bottom divider (full width within safe area) --
    bottom_divider_y = TRIM_Y + TRIM_H - SAFE - 18
    svg.append(hline(SAFE_X, bottom_divider_y, TRIM_X + TRIM_W - SAFE, width=0.9))

    # -- CTA row --
    cta_y = bottom_divider_y + 13
    circ_r = 5
    circ_cx = left_x + circ_r
    circ_cy = cta_y - 3.0
    svg.append(f'  <circle cx="{circ_cx:.3f}" cy="{circ_cy:.3f}" r="{circ_r}" fill="{GREEN}"/>\n')
    # white arrow
    ax = circ_cx
    ay = circ_cy
    svg.append(f'  <g stroke="{WHITE}" stroke-width="1.0" stroke-linecap="round" stroke-linejoin="round" fill="none">\n')
    svg.append(f'    <line x1="{ax-2.2:.3f}" y1="{ay:.3f}" x2="{ax+2.0:.3f}" y2="{ay:.3f}"/>\n')
    svg.append(f'    <path d="M {ax+0.1:.3f},{ay-2.1:.3f} L {ax+2.2:.3f},{ay:.3f} L {ax+0.1:.3f},{ay+2.1:.3f}"/>\n')
    svg.append('  </g>\n')

    cta_text = "BOOK YOUR FREE DISCOVERY CALL"
    # cta_size held at 5.5 (not shrunk further) to protect legibility -- see
    # note in the polish-pass summary about this row being width-constrained
    cta_size = 5.5
    cta_ls = 0.02
    web_text = "REIMAGINEDBYMIRA.COM"
    web_size = 6.3   # held at last round's size -- see polish-pass note on this row
    web_ls = 0.02

    cta_text_x = circ_cx + circ_r + 13   # arrow-to-text gap widened again (was 12, +1)
    svg.append(left_text(cta_text_x, cta_y, cta_text, SANS, cta_size, GREEN,
                          weight="700", letter_spacing_em=cta_ls))

    cta_w = text_width(cta_text, SANS, cta_size, weight="700", letter_spacing_em=cta_ls)
    web_w = text_width(web_text, SANS, web_size, weight="600", letter_spacing_em=web_ls)
    vdiv_x = cta_text_x + cta_w + 7
    web_start = right_edge - web_w
    assert web_start - vdiv_x >= 1, f"CTA row overflow: gap={web_start - vdiv_x:.1f}"

    svg.append(vline(vdiv_x, cta_y - 7.0, cta_y + 2.2, width=0.8))
    svg.append(right_text(right_edge, cta_y, web_text, SANS, web_size, GREEN,
                           weight="600", letter_spacing_em=web_ls))

    svg.append('</svg>\n')
    return "".join(svg)


if __name__ == "__main__":
    front = build_front()
    back = build_back()
    with open(os.path.join(OUT_DIR, "front.svg"), "w") as f:
        f.write(front)
    with open(os.path.join(OUT_DIR, "back.svg"), "w") as f:
        f.write(back)
    print("wrote front.svg, back.svg")
