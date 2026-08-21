"""Generate a sparkler flipbook — a particle burst authored from a script, not vendored.

Part 4's rule for the render shelf: a shape no CC0 pack carries is generated, so it regenerates
rather than accumulating as binary mystery. That applies doubly to a particle effect, where the
alternative is a 4K EXR from an effects pack that nobody in this repo can reproduce or adjust.

The simulation is deliberately tiny and deterministic — a fixed seed, no physics library, and
every constant on screen here rather than in a token file, because this is the *source* of an
asset rather than a treatment. What comes out is a WHITE, ALPHA-SHAPED sheet, which is the one
property that matters downstream: `SetVertexColor` can then take it to any hue, and the render
shelf's tint guard passes it by construction instead of by luck.

Motion: particles launch from the centre on a jittered radial, decelerate, and fade. A few
"embers" persist longer and drift, because a burst where every particle dies at once reads as a
flash rather than as a sparkler.
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "projects" / "combat-assist" / "previews" / "assets" / "vfx"

SEED = 20260819           # fixed: the sheet must be identical on every machine and every re-run
PARTICLES = 46
SPEED = (0.85, 1.75)      # cell-widths per second — tuned so the fastest sparks reach the rim
DRAG = 2.1                # velocity decay, per second
LIFE = (0.55, 1.00)       # fraction of the flipbook a particle survives
EMBER_CHANCE = 0.28       # fraction that live to the end and drift
CORE_FRAMES = 0.22        # fraction of the book the central flash occupies
HEAD = (0.012, 0.026)     # spark head radius, cell-widths — small, or it reads as a blob
TRAIL = 0.055             # how far back the streak reaches, in units of `t`
SS = 4                    # supersample, for round dots at 64px


def _sheet(cols: int, rows: int, cell: int) -> tuple[Image.Image, int]:
    return Image.new("L", (cols * cell, rows * cell), 0), cols * rows


def sparkler(cols: int = 8, rows: int = 8, cell: int = 64) -> tuple[Image.Image, int]:
    rng = random.Random(SEED)
    sheet, frames = _sheet(cols, rows, cell)

    seeds = []
    for _ in range(PARTICLES):
        angle = rng.uniform(0, math.tau)
        seeds.append({
            "a": angle,
            "v": rng.uniform(*SPEED),
            "life": 1.0 if rng.random() < EMBER_CHANCE else rng.uniform(*LIFE),
            "r": rng.uniform(*HEAD),               # dot radius, cell-widths
            "drift": rng.uniform(-0.35, 0.35),     # curls the tail so it is not a starburst
        })

    big = cell * SS
    for i in range(frames):
        t = i / max(frames - 1, 1)
        frame = Image.new("L", (big, big), 0)
        draw = ImageDraw.Draw(frame)

        # The core flash: bright and brief. Without it the burst has no origin and the particles
        # read as arriving from off-screen rather than being thrown.
        if t < CORE_FRAMES:
            k = 1.0 - t / CORE_FRAMES
            rad = big * (0.05 + 0.16 * k)
            draw.ellipse([big / 2 - rad, big / 2 - rad, big / 2 + rad, big / 2 + rad],
                         fill=int(255 * k))

        for p in seeds:
            if t > p["life"]:
                continue

            # Integrated position under linear drag: closed form, so a frame does not depend on
            # how many frames preceded it and the sheet stays resolution-independent.
            def at(u: float) -> tuple[float, float]:
                reach = p["v"] * (1 - math.exp(-DRAG * u)) / DRAG
                ang = p["a"] + p["drift"] * u
                return (big / 2 + math.cos(ang) * reach * big,
                        big / 2 + math.sin(ang) * reach * big)

            fade = 1.0 - (t / p["life"]) ** 1.6
            if fade <= 0:
                continue
            x, y = at(t)

            # The streak. A sparkler is read from its TRAILS, not its dots -- a field of round
            # points reads as confetti. Drawn dimmer than the head so the spark still leads.
            back = at(max(t - TRAIL, 0.0))
            draw.line([back, (x, y)], fill=int(255 * fade * 0.55),
                      width=max(int(big * p["r"] * 1.1), 1))

            rad = big * p["r"] * (0.45 + 0.55 * fade)
            if rad >= 1:
                draw.ellipse([x - rad, y - rad, x + rad, y + rad], fill=int(255 * fade))

        frame = frame.filter(ImageFilter.GaussianBlur(big * 0.006))
        frame = frame.resize((cell, cell), Image.LANCZOS)
        sheet.paste(frame, ((i % cols) * cell, (i // cols) * cell))

    white = Image.new("L", sheet.size, 255)
    return Image.merge("RGBA", (white, white, white, sheet)), frames


def main() -> None:
    ap = argparse.ArgumentParser(prog="wowkb.sparkler", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="sparkler")
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--rows", type=int, default=8)
    ap.add_argument("--cell", type=int, default=64)
    args = ap.parse_args()

    sheet, frames = sparkler(args.cols, args.rows, args.cell)
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{args.name}.png"
    sheet.save(dest)
    (OUT / f"{args.name}.provenance.txt").write_text(
        f"{args.name}.png\n"
        f"  source      GENERATED by `python -m wowkb.sparkler` (seed {SEED})\n"
        f"  grid        {args.cols}x{args.rows} = {frames} frames\n"
        f"  cell        {args.cell}px -> sheet {sheet.size[0]}x{sheet.size[1]}\n"
        "  alpha       STRAIGHT, white RGB — the shape is in alpha ONLY, so SetVertexColor\n"
        "              reaches any hue and the render shelf's tint guard passes by construction.\n"
        "\nReproducible from this repo, unlike the vendored VFX sheets beside it: re-run the\n"
        "module to regenerate byte-identically, or edit its constants to change the effect.\n",
        encoding="utf-8")
    print(f"wrote {dest.relative_to(ROOT)} — {sheet.size[0]}x{sheet.size[1]}, "
          f"{args.cols}x{args.rows} = {frames} frames @ {args.cell}px")


if __name__ == "__main__":
    main()
