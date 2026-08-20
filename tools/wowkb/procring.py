"""Generate a CIRCULAR proc glow — Blizzard's effect, measured, then rebuilt as a ring.

Blizzard ships no circular proc glow: `ui-hud-actionbar-proc-loop-flipbook` traces a rounded
SQUARE, because it is drawn around an action button. cap's promotion sits on a round badge, so
the shape has to change — and a ring cropped out of square art looks like exactly that.

**Every constant below was measured off the real sheet rather than guessed**, because the first
four attempts at this failed on characteristics nobody had written down:

    per-frame energy      min 917 / max 982 — a ratio of 1.07
    interior (centre 12x12)  exactly 0.0
    radial profile        soft ramp OUTWARD over ~9px, hard cut INWARD over ~3px
    band centre           ~17% of the cell in from the edge, ~20% of the cell wide

Three consequences, and each one is a thing a hand-authored imitation gets wrong:

* **It does not pulse.** A 7% energy variation is not a breathe. The life in it is *internal*:
  hot spots travelling around the rim at essentially constant total brightness. Every earlier
  lab entry breathed, which is why none of them read like this one.
* **It never touches the icon.** The interior measures a flat zero, so the art under it stays
  completely legible. A glow that dims what it is pointing at has taken information away.
* **The falloff is asymmetric.** Soft outward, hard inward — light SPILLING OFF an edge, rather
  than a ring drawn on top of one. Symmetric falloff reads as a painted donut.

Output is white with the shape in alpha, so unlike Blizzard's baked gold it can be taken to any
hue with `SetVertexColor` — which is the one way this beats the original.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "projects" / "combat-assist" / "previews" / "assets" / "vfx"

# --- measured off ui-hud-actionbar-proc-loop-flipbook, 2026-08-19 (see module docstring) ------
BAND_R = 0.656          # band centre, as a fraction of the half-cell (21px of 32)
OUT_SIGMA = 0.145       # outward falloff — the ~9px bloom
IN_SIGMA = 0.048        # inward falloff — the ~3px cut
FLOOR = 0.30            # the rim never goes fully dark between hot spots
# Travelling hot spots: (angular frequency, revolutions per loop, amplitude). Integer pairs, so
# the book is seamless in BOTH angle and time — frame N wraps to frame 0 exactly.
HARMONICS = ((3, 1, 0.42), (5, -2, 0.24), (8, 3, 0.14))
SS = 2                  # supersample; the ring is smooth, so it needs less than the sparkler


def _pot(n: int) -> int:
    p = 1
    while p < n:
        p *= 2
    return p


def ring_frames(frames: int, cell: int) -> list[np.ndarray]:
    big = cell * SS
    y, x = np.mgrid[0:big, 0:big].astype("float32")
    c = (big - 1) / 2
    nx, ny = (x - c) / c, (y - c) / c
    r = np.sqrt(nx * nx + ny * ny)
    theta = np.arctan2(ny, nx)

    # The asymmetric radial band: a gaussian with two different widths either side of the peak.
    d = r - BAND_R
    radial = np.where(d >= 0,
                      np.exp(-(d * d) / (2 * OUT_SIGMA ** 2)),
                      np.exp(-(d * d) / (2 * IN_SIGMA ** 2)))

    out = []
    for i in range(frames):
        t = i / frames
        ang = np.full_like(theta, FLOOR)
        for freq, rev, amp in HARMONICS:
            ang = ang + amp * (1 + np.cos(freq * theta - 2 * math.pi * rev * t)) / 2
        f = radial * ang
        peak = f.max()
        if peak > 0:
            f = np.clip(f / peak, 0, 1)
        out.append(f)

    # Hold TOTAL energy flat across the book, which is the measured behaviour (ratio 1.07) and
    # the thing that separates "alive" from "blinking". Normalising per frame would also flatten
    # the hot spots, so it is the SUM that is levelled, never the shape.
    sums = np.array([f.sum() for f in out])
    return [f * float(sums.mean() / s) for f, s in zip(out, sums)]


def sheet(frames: int = 32, cols: int = 8, cell: int = 64) -> tuple[Image.Image, int]:
    rows = math.ceil(frames / cols)
    canvas = Image.new("L", (_pot(cols * cell), _pot(rows * cell)), 0)
    for i, f in enumerate(ring_frames(frames, cell)):
        img = Image.fromarray((np.clip(f, 0, 1) * 255 + 0.5).astype("uint8"), "L")
        img = img.resize((cell, cell), Image.LANCZOS)
        canvas.paste(img, ((i % cols) * cell, (i // cols) * cell))
    white = Image.new("L", canvas.size, 255)
    return Image.merge("RGBA", (white, white, white, canvas)), frames


def main() -> None:
    ap = argparse.ArgumentParser(prog="wowkb.procring", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="procring")
    ap.add_argument("--frames", type=int, default=32)
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--cell", type=int, default=64)
    args = ap.parse_args()

    img, frames = sheet(args.frames, args.cols, args.cell)
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{args.name}.png"
    img.save(dest)
    rows = math.ceil(frames / args.cols)
    (OUT / f"{args.name}.provenance.txt").write_text(
        f"{args.name}.png\n"
        f"  source      GENERATED by `python -m wowkb.procring`\n"
        f"  modelled on Blizzard `ui-hud-actionbar-proc-loop-flipbook` (atlas 2476), whose\n"
        f"              radial profile, interior clearance and per-frame energy were MEASURED\n"
        f"              2026-08-19 and are the constants in the module.\n"
        f"  grid        {args.cols} cols x {rows} rows = {frames} frames\n"
        f"  cell        {args.cell}px -> sheet {img.size[0]}x{img.size[1]}\n"
        "  alpha       STRAIGHT, white RGB — shape in alpha ONLY, so SetVertexColor reaches any\n"
        "              hue. This is the one way it beats the original, which is baked gold.\n"
        "  loop        seamless in angle AND time: harmonics use integer frequency/revolution\n"
        "              pairs, so the last frame wraps to the first exactly.\n"
        "\nReproducible from this repo. Re-run the module to regenerate byte-identically.\n",
        encoding="utf-8")
    print(f"wrote {dest.relative_to(ROOT)} — {img.size[0]}x{img.size[1]}, "
          f"{args.cols}x{rows} = {frames} frames @ {args.cell}px")


if __name__ == "__main__":
    main()
