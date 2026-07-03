#!/usr/bin/env python3
"""Converts print-ready.pdf (RGB, from rsvg-convert) into a PDF/X-1a:2001
file: CMYK color conversion, a generic CMYK ICC output intent, explicit
TrimBox/BleedBox on every page, and pure K-only black text. Requires
Ghostscript and qpdf.

Note on the black-text step: Ghostscript's own -dBlackText=true flag forces
pure-black text to render as DeviceGray 0, but it has a content-stream
optimizer bug in this Ghostscript version -- it drops the color-reset
operator for whatever vector/text element is drawn *immediately after* a
black-text run, silently painting it black too (verified: it repainted our
green "CAREER STRATEGY" and tagline black). So instead we run the CMYK
conversion with no black-text special-casing at all (which converts our
text colors correctly, just with black going through the ICC profile as a
"rich black" of C72.2 M67.5 Y67.1 K88.2), then surgically replace that
exact, deterministic rich-black tuple with pure K (0 0 0 1) in the
decompressed content streams. This is more reliable than trusting
Ghostscript's built-in black preservation.
"""
import os
import re
import subprocess

from generate import BLEED, DOC_W, DOC_H
from make_print_ready import MARGIN, PAGE_W, PAGE_H

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

TRIM_BOX = (MARGIN + BLEED, MARGIN + BLEED,
            MARGIN + DOC_W - BLEED, MARGIN + DOC_H - BLEED)
BLEED_BOX = (MARGIN, MARGIN, MARGIN + DOC_W, MARGIN + DOC_H)

# The rich-black CMYK tuple Ghostscript's default_cmyk.icc profile produces
# for RGB(0,0,0) under the default rendering intent. Verified empirically
# (see docstring); if the profile or gs version changes this may need
# re-deriving by running the gs step alone and inspecting a `k`/`K` operator
# right before a text block that should be pure black.
RICH_BLACK_RE = re.compile(rb"0\.722 0\.675 0\.671 0\.882 ([kK])")
# 3 fills (front wordmark, back header, back benefit lines) + 2 strokes
# (the black crop marks make_print_ready.py draws on each of the 2 pages)
EXPECTED_BLACK_REPLACEMENTS = 5


def run_ghostscript(src, dst):
    pdfx_dir = os.path.join(OUT_DIR, "pdfx")
    icc_path = os.path.join(pdfx_dir, "default_cmyk.icc")

    box_ps = (f"<</TrimBox[{TRIM_BOX[0]} {TRIM_BOX[1]} {TRIM_BOX[2]} {TRIM_BOX[3]}]"
              f" /BleedBox[{BLEED_BOX[0]} {BLEED_BOX[1]} {BLEED_BOX[2]} {BLEED_BOX[3]}]>> setpagedevice")

    # cwd=pdfx_dir so the relative ICCProfile filename in mira_pdfx_def.ps
    # resolves under Ghostscript's SAFER sandbox (blocks absolute reads
    # outside the working directory unless explicitly permitted)
    cmd = [
        "gs", "-dPDFX", "-dBATCH", "-dNOPAUSE", "-dNOOUTERSAVE", "-dQUIET",
        f"--permit-file-read={icc_path}:{src}",
        f"--permit-file-write={dst}",
        "-dCompatibilityLevel=1.3",
        "-sColorConversionStrategy=CMYK",
        "-sProcessColorModel=DeviceCMYK",
        "-sOutputICCProfile=default_cmyk.icc",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={dst}",
        "./mira_pdfx_def.ps",
        "-c", box_ps,
        "-f", src,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=pdfx_dir)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)


def fix_black_and_finalize(cmyk_pdf, dst):
    qdf_path = cmyk_pdf + ".qdf.pdf"
    subprocess.run(["qpdf", "--qdf", "--object-streams=disable", cmyk_pdf, qdf_path], check=True)

    data = open(qdf_path, "rb").read()
    data, n = RICH_BLACK_RE.subn(rb"0 0 0 1 \1", data)
    if n != EXPECTED_BLACK_REPLACEMENTS:
        raise RuntimeError(
            f"expected {EXPECTED_BLACK_REPLACEMENTS} rich-black substitutions, made {n} "
            "-- Ghostscript/profile output likely changed, re-derive RICH_BLACK_RE"
        )
    open(qdf_path, "wb").write(data)

    # editing stream content by hand leaves the QDF's /Length markers stale;
    # fix-qdf (shipped with qpdf) recalculates them from the actual bytes
    fixed_path = qdf_path + ".fixed.pdf"
    with open(qdf_path, "rb") as f_in, open(fixed_path, "wb") as f_out:
        subprocess.run(["fix-qdf"], stdin=f_in, stdout=f_out, check=True)

    # re-normalize the repaired QDF back into a standard compressed PDF
    subprocess.run(["qpdf", fixed_path, dst], check=True)
    os.remove(qdf_path)
    os.remove(fixed_path)
    print(f"replaced {n} rich-black occurrences with pure K")


def main():
    src = os.path.join(OUT_DIR, "print-ready.pdf")
    intermediate = os.path.join(OUT_DIR, "_print-ready-x1a-cmyk.pdf")
    dst = os.path.join(OUT_DIR, "print-ready-x1a.pdf")

    run_ghostscript(src, intermediate)
    fix_black_and_finalize(intermediate, dst)
    os.remove(intermediate)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
