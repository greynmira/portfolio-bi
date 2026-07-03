#!/usr/bin/env python3
"""Converts print-ready.pdf (RGB, from rsvg-convert) into a PDF/X compliant
file (X-4 by default, X-1a also supported): CMYK color conversion, a
generic CMYK ICC output intent, explicit TrimBox/BleedBox on every page,
and pure K-only black text. Requires Ghostscript and qpdf.

Two Ghostscript quirks required workarounds, both found by inspecting the
actual output rather than trusting exit code 0:

1. -dBlackText=true (meant to force pure-black text to DeviceGray 0) has a
   content-stream optimizer bug in this Ghostscript version: it drops the
   color-reset operator for whatever vector/text element is drawn
   *immediately after* a black-text run, silently painting it black too
   (verified: it repainted our green "CAREER STRATEGY" and tagline black).
   Fix: convert with no black-text special-casing (colors all come out
   right, black just lands as a "rich black" of C72.2 M67.5 Y67.1 K88.2),
   then surgically replace that exact tuple with pure K in the decompressed
   content streams.

2. `-c "<</TrimBox[...] /BleedBox[...]>> setpagedevice"` before `-f
   input.pdf` does NOT apply custom page boxes when *transcoding* an
   existing PDF (as opposed to rendering fresh PostScript) -- gs just
   copies the source's MediaBox into TrimBox/BleedBox for every page,
   silently ignoring the setpagedevice call. And -dPDFX (needed to get gs
   to at least emit a BleedBox key at all) hard-pins the output to PDF 1.3
   regardless of -dCompatibilityLevel, which breaks real X-4 conformance
   (requires PDF 1.6+). Fix: run with -dPDFX so the box keys exist, patch
   their actual values directly in the decompressed content during the same
   QDF edit pass as the black-color fix, then use `qpdf --force-version` to
   correct the PDF version header afterward.
"""
import os
import re
import subprocess
import sys

from generate import BLEED, DOC_W, DOC_H
from make_print_ready import MARGIN, PAGE_W, PAGE_H

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

TRIM_BOX = (MARGIN + BLEED, MARGIN + BLEED,
            MARGIN + DOC_W - BLEED, MARGIN + DOC_H - BLEED)
BLEED_BOX = (MARGIN, MARGIN, MARGIN + DOC_W, MARGIN + DOC_H)

FLAVORS = {
    "x4": {"def_ps": "mira_pdfx4_def.ps", "pdf_version": "1.6", "out": "print-ready-x4.pdf"},
    "x1a": {"def_ps": "mira_pdfx_def.ps", "pdf_version": "1.3", "out": "print-ready-x1a.pdf"},
}

# The rich-black CMYK tuple Ghostscript's default_cmyk.icc profile produces
# for RGB(0,0,0) under the default rendering intent. Verified empirically
# (see docstring); if the profile or gs version changes this may need
# re-deriving by running the gs step alone and inspecting a `k`/`K` operator
# right before a text block that should be pure black.
RICH_BLACK_RE = re.compile(rb"0\.722 0\.675 0\.671 0\.882 ([kK])")
# 3 fills (front wordmark, back header, back benefit lines) + 2 strokes
# (the black crop marks make_print_ready.py draws on each of the 2 pages)
EXPECTED_BLACK_REPLACEMENTS = 5

# gs (via -dPDFX) writes TrimBox/BleedBox equal to the MediaBox for every
# page when transcoding; we overwrite those placeholder values below.
WRONG_BOX_RE = re.compile(
    rb"/(TrimBox|BleedBox) \[\s*0\s+0\s+312\s+204\s*\]"
)
EXPECTED_BOX_FIXES = 4  # 2 boxes x 2 pages


def run_ghostscript(src, dst, def_ps):
    pdfx_dir = os.path.join(OUT_DIR, "pdfx")
    icc_path = os.path.join(pdfx_dir, "default_cmyk.icc")

    # cwd=pdfx_dir so the relative ICCProfile filename in the def.ps resolves
    # under Ghostscript's SAFER sandbox (blocks absolute reads outside the
    # working directory unless explicitly permitted).
    cmd = [
        "gs", "-dPDFX", "-dBATCH", "-dNOPAUSE", "-dNOOUTERSAVE", "-dQUIET",
        f"--permit-file-read={icc_path}:{src}",
        f"--permit-file-write={dst}",
        "-dCompatibilityLevel=1.3",  # gs pins this under -dPDFX regardless; corrected after, for x4
        "-sColorConversionStrategy=CMYK",
        "-sProcessColorModel=DeviceCMYK",
        "-sOutputICCProfile=default_cmyk.icc",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={dst}",
        f"./{def_ps}",
        "-f", src,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=pdfx_dir)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)


def fix_black_and_boxes(cmyk_pdf, dst):
    qdf_path = cmyk_pdf + ".qdf.pdf"
    subprocess.run(["qpdf", "--qdf", "--object-streams=disable", cmyk_pdf, qdf_path], check=True)

    data = open(qdf_path, "rb").read()

    data, n_black = RICH_BLACK_RE.subn(rb"0 0 0 1 \1", data)
    if n_black != EXPECTED_BLACK_REPLACEMENTS:
        raise RuntimeError(
            f"expected {EXPECTED_BLACK_REPLACEMENTS} rich-black substitutions, made {n_black} "
            "-- Ghostscript/profile output likely changed, re-derive RICH_BLACK_RE"
        )

    def box_fix(m):
        name = m.group(1)
        box = TRIM_BOX if name == b"TrimBox" else BLEED_BOX
        return b"/" + name + f" [{box[0]} {box[1]} {box[2]} {box[3]}]".encode()

    data, n_box = WRONG_BOX_RE.subn(box_fix, data)
    if n_box != EXPECTED_BOX_FIXES:
        raise RuntimeError(
            f"expected {EXPECTED_BOX_FIXES} TrimBox/BleedBox fixes, made {n_box} "
            "-- Ghostscript output layout likely changed, re-derive WRONG_BOX_RE"
        )

    open(qdf_path, "wb").write(data)

    # editing stream/dict content by hand leaves the QDF's /Length markers
    # stale; fix-qdf (shipped with qpdf) recalculates them from the actual bytes
    fixed_path = qdf_path + ".fixed.pdf"
    with open(qdf_path, "rb") as f_in, open(fixed_path, "wb") as f_out:
        subprocess.run(["fix-qdf"], stdin=f_in, stdout=f_out, check=True)

    # re-normalize the repaired QDF back into a standard compressed PDF
    subprocess.run(["qpdf", fixed_path, dst], check=True)
    os.remove(qdf_path)
    os.remove(fixed_path)
    print(f"replaced {n_black} rich-black occurrences with pure K, fixed {n_box} page boxes")


def build(flavor):
    cfg = FLAVORS[flavor]
    src = os.path.join(OUT_DIR, "print-ready.pdf")
    intermediate = os.path.join(OUT_DIR, f"_print-ready-{flavor}-cmyk.pdf")
    boxed = os.path.join(OUT_DIR, f"_print-ready-{flavor}-boxed.pdf")
    dst = os.path.join(OUT_DIR, cfg["out"])

    run_ghostscript(src, intermediate, cfg["def_ps"])
    fix_black_and_boxes(intermediate, boxed)
    subprocess.run(["qpdf", f"--force-version={cfg['pdf_version']}", boxed, dst], check=True)
    os.remove(intermediate)
    os.remove(boxed)
    print(f"wrote {dst}")


def main():
    flavors = sys.argv[1:] or ["x4"]
    for flavor in flavors:
        build(flavor)


if __name__ == "__main__":
    main()
