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
TEXT = "#111111"

SERIF = "EB Garamond"
SANS = "Montserrat"

SVG_HEAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="{win}in" height="{hin}in" viewBox="0 0 {w} {h}">\n'
).format(win=DOC_W / 72.0, hin=DOC_H / 72.0, w=DOC_W, h=DOC_H)


def lightbulb_icon(cx, top_y, width):
    """Lightbulb-with-sprout mark. Local box is 100x135 units: a graceful
    tapered (non-circular) globe, thin balanced rays, a floating tapered
    ring base, and a delicate twin-leaf filament -- refined line weights
    throughout for a premium, editorial feel rather than a stock glyph."""
    s = width / 100.0
    h = 135.0 * s
    tx = cx - width / 2.0
    ty = top_y
    return f'''  <g transform="translate({tx:.3f},{ty:.3f}) scale({s:.5f})"
     fill="none" stroke="{GREEN}" stroke-linecap="round" stroke-linejoin="round">
    <g stroke-width="1.1">
      <line x1="50" y1="12" x2="50" y2="1"/>
      <line x1="32" y1="19" x2="23" y2="9.5"/>
      <line x1="68" y1="19" x2="77" y2="9.5"/>
      <line x1="21" y1="52" x2="8" y2="52"/>
      <line x1="79" y1="52" x2="92" y2="52"/>
    </g>
    <path stroke-width="1.5" d="M 25,61
             C 25,37 35,20 50,20
             C 65,20 75,37 75,61
             C 75,79 68,91 60,97
             L 40,97
             C 32,91 25,79 25,61
             Z"/>
    <g stroke-width="1.3">
      <line x1="41" y1="103" x2="59" y2="103"/>
      <line x1="43" y1="109.5" x2="57" y2="109.5"/>
      <line x1="45.5" y1="116" x2="54.5" y2="116"/>
    </g>
    <path stroke-width="1.0" d="M 50,93 L 50,55"/>
    <path stroke-width="0.8" d="M 50,55 C 45,55 43,50 46,46.5 C 48,44.5 50,48 50,55 Z"/>
    <path stroke-width="0.8" d="M 50,55 C 55,55 57,50 54,46.5 C 52,44.5 50,48 50,55 Z"/>
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

    icon_top = 17.6   # positions the whole block to center in the trim box
    icon_svg, icon_h = lightbulb_icon(CENTER_X, icon_top, 45)
    svg.append(icon_svg)
    icon_bottom = icon_top + icon_h

    name_y = icon_bottom + 28
    svg.append(centered_text(CENTER_X, name_y, "Reimagined by Mira", SERIF, 23.5, TEXT, weight="600"))

    strategy_y = name_y + 17
    strategy_text = "CAREER STRATEGY"
    ls_em = 0.28
    font_size = 9.0
    text_w = text_width(strategy_text, SANS, font_size, weight="600", letter_spacing_em=ls_em)
    gap = 10
    line_len = 24
    svg.append(hline(CENTER_X - text_w / 2 - gap - line_len, strategy_y - 3, CENTER_X - text_w / 2 - gap))
    svg.append(hline(CENTER_X + text_w / 2 + gap, strategy_y - 3, CENTER_X + text_w / 2 + gap + line_len))
    svg.append(centered_text(CENTER_X, strategy_y, strategy_text, SANS, font_size, GREEN,
                              weight="600", letter_spacing_em=ls_em))

    tagline_y = strategy_y + 18
    svg.append(centered_text(CENTER_X, tagline_y, "Build Your Next Move.", SERIF, 12.5, GREEN, style="italic"))

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
    qr_module_size = 68.4          # 0.95in minimum
    # pad must clear a >=4-module quiet zone (QR spec) and exceed rx so the
    # rounded corner never clips into the finder-pattern squares
    pad = 12.0
    outline_size = qr_module_size + 2 * pad
    outline_x = (TRIM_X + TRIM_W) - SAFE - outline_size
    outline_y = SAFE_Y
    rx = 6

    qr_x = outline_x + pad
    qr_y = outline_y + pad
    qr_svg, n_modules = make_qr_svg("https://reimaginedbymira.com", GREEN, qr_x, qr_y, qr_module_size)

    svg.append(f'  <rect x="{outline_x:.3f}" y="{outline_y:.3f}" width="{outline_size:.3f}" height="{outline_size:.3f}" '
               f'rx="{rx}" fill="{WHITE}" stroke="{GREEN}" stroke-width="1.1"/>\n')
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
    cta_size = 5.8
    cta_ls = 0.02
    web_text = "REIMAGINEDBYMIRA.COM"
    web_size = 6.0
    web_ls = 0.02

    cta_text_x = circ_cx + circ_r + 5
    svg.append(left_text(cta_text_x, cta_y, cta_text, SANS, cta_size, GREEN,
                          weight="700", letter_spacing_em=cta_ls))

    cta_w = text_width(cta_text, SANS, cta_size, weight="700", letter_spacing_em=cta_ls)
    web_w = text_width(web_text, SANS, web_size, weight="600", letter_spacing_em=web_ls)
    vdiv_x = cta_text_x + cta_w + 7
    web_start = right_edge - web_w
    assert web_start - vdiv_x >= 4, f"CTA row overflow: gap={web_start - vdiv_x:.1f}"

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
