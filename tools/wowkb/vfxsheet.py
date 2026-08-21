"""Normalise an external flipbook sheet into art cap can actually draw.

The render shelf's badge art is CC0 PNGs vendored whole, and its shapes are generated from a
script (`capart.shape_images`). Neither route fits a **VFX flipbook**: those arrive as 4K EXR or
huge TGA from effects packs, in float16 HDR, at grid sizes nothing in the client wants. This is
the third door — a documented, re-runnable conversion from a source sheet to a normalised one.

Three things it fixes, each of which is a real failure if skipped:

* **Power-of-two.** `capart._write_tga` refuses anything else, because the client wants it.
  A 6x6 grid of 682px cells is neither, so the grid is re-laid at a chosen cell size and the
  sheet padded out to the next power of two. The wasted region is transparent and the renderer
  never addresses it -- the frame count is carried alongside, not inferred from the sheet.
* **HDR -> 8 bit.** EXR channels here run 0..1 in float16 but are *scene-referred*: clipping
  them straight to 8 bit crushes the bloom that makes the effect read. Reinhard tonemap first.
* **Premultiplied alpha.** Effects packs commonly ship RGB already multiplied by alpha. The
  client's ADD blend wants that; `BLEND` does not. Which one a sheet is gets MEASURED and
  recorded rather than assumed, because guessing wrong looks like a dim halo and reads as
  "the art is bad" instead of "the blend is wrong".

Provenance is written beside the output. These sheets are NOT reproducible from this repo --
they come from a download -- so the note naming the source file is the only thing standing
between a future reader and an unexplained binary.
"""
from __future__ import annotations

import argparse
import sys
import math
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "projects" / "combat-assist" / "previews" / "assets" / "vfx"


def _pot(n: int) -> int:
    p = 1
    while p < n:
        p *= 2
    return p


def load_exr(path: Path, exposure: float) -> Image.Image:
    """EXR -> 8-bit RGBA, Reinhard-tonemapped at `exposure`."""
    import numpy as np
    import OpenEXR

    with OpenEXR.File(str(path)) as f:
        chans = f.channels()
        if "RGBA" in chans:
            a = np.asarray(chans["RGBA"].pixels, dtype="float32")
        else:
            planes = [np.asarray(chans[c].pixels, dtype="float32")
                      for c in ("R", "G", "B", "A") if c in chans]
            if len(planes) < 3:
                sys.exit(f"{path.name}: need RGB(A) channels, found {list(chans)}")
            if len(planes) == 3:
                planes.append(np.ones_like(planes[0]))
            a = np.stack(planes, axis=-1)
    rgb = a[..., :3] * exposure
    rgb = rgb / (1.0 + rgb)                      # Reinhard — keeps the bloom off the clip point
    rgb = np.clip(rgb ** (1 / 2.2), 0, 1)        # to sRGB
    alpha = np.clip(a[..., 3], 0, 1)
    out = np.concatenate([rgb, alpha[..., None]], axis=-1)
    return Image.fromarray((out * 255 + 0.5).astype("uint8"), "RGBA")


def alpha_report(img: Image.Image) -> str:
    """What the alpha channel actually is — measured, because guessing it looks like bad art.

    An EMPTY alpha is not a broken file. Effects packs ship additive "beauty" passes where
    luminance carries visibility and the alpha channel is unused, because the effect is meant to
    be drawn with ADD blend against black. Pasted into a BLEND pipeline it renders as nothing at
    all, which reads as a conversion bug rather than as a blend-mode mismatch -- so this names it.
    """
    import numpy as np
    a = np.asarray(img, dtype="float32") / 255.0
    if float(a[..., 3].max()) <= 0.004:
        return ("EMPTY — an additive beauty pass. Luminance carries visibility; use "
                "--alpha luminance to synthesise one, and draw it with ADD.")
    over = (a[..., :3].max(axis=-1) > a[..., 3] + 0.02)
    if float(over.mean()) < 0.005:
        return "PREMULTIPLIED — use ADD, or un-premultiply for BLEND"
    return "STRAIGHT — use BLEND"


def luminance_alpha(img: Image.Image) -> Image.Image:
    """Synthesise alpha from luminance, for an additive pass whose own alpha is empty.

    Rec. 709 luma, and the RGB is left ALONE rather than divided back out: the result is a
    premultiplied sheet, which is exactly what ADD blending wants and what the client will draw.
    """
    import numpy as np
    a = np.asarray(img, dtype="float32") / 255.0
    luma = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    a[..., 3] = np.clip(luma, 0, 1)
    return Image.fromarray((a * 255 + 0.5).astype("uint8"), "RGBA")


def regrid(src: Image.Image, cols: int, rows: int, cell: int,
           pack: int = 0, every: int = 1) -> tuple[Image.Image, int, int]:
    """Re-lay a cols x rows sheet at `cell` px onto a power-of-two sheet.

    ⚠ **Power-of-two padding, not resolution, is what costs.** A 6x6 grid of 64px cells is
    384x384 and pads to 512x512 — a third of the texture wasted, and the same third paid again
    as base64 in every preview that embeds it. So two levers, both about layout rather than
    quality:

    * `pack` re-lays the frames into a different column count. Frames are an ordered sequence, so
      30 of them fit an 8x4 grid (512x256) just as well as the source's 5x6 (which pads to
      512x512) — half the pixels for identical output.
    * `every` keeps 1 frame in N. A 64-frame fire loop at 30fps is over two seconds of detail
      nobody watching a 56px icon can resolve; halving it halves the sheet.

    Returns the sheet, the frame count, and the COLUMN COUNT it was laid out at — the caller
    cannot assume the source grid survived.
    """
    w, h = src.size
    cw, ch = w / cols, h / rows
    keep = [i for i in range(cols * rows) if i % every == 0]
    out_cols = pack or cols
    out_rows = math.ceil(len(keep) / out_cols)
    # Each dimension padded to a power of two INDEPENDENTLY: `_write_tga` wants both PoT, not a
    # square, and forcing a square costs a 16x4 sheet three quarters of its texture memory.
    out = Image.new("RGBA", (_pot(out_cols * cell), _pot(out_rows * cell)), (0, 0, 0, 0))
    for n, i in enumerate(keep):
        c, r = i % cols, i // cols
        box = (round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch))
        frame = src.crop(box).resize((cell, cell), Image.LANCZOS)
        out.paste(frame, ((n % out_cols) * cell, (n // out_cols) * cell))
    return out, len(keep), out_cols


def main() -> None:
    ap = argparse.ArgumentParser(prog="wowkb.vfxsheet", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("--name", required=True, help="output stem under previews/assets/vfx/")
    ap.add_argument("--cols", type=int, required=True)
    ap.add_argument("--rows", type=int, required=True)
    ap.add_argument("--cell", type=int, default=64, help="normalised cell size in px")
    ap.add_argument("--exposure", type=float, default=1.0, help="EXR only, pre-tonemap gain")
    ap.add_argument("--pack", type=int, default=0,
                    help="re-lay frames at this column count (0 = keep the source grid)")
    ap.add_argument("--every", type=int, default=1, help="keep 1 frame in N")
    ap.add_argument("--alpha", choices=("keep", "luminance"), default="keep",
                    help="'luminance' synthesises alpha for an additive pass with none")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        sys.exit(f"no such file: {src}")
    img = load_exr(src, args.exposure) if src.suffix.lower() == ".exr" \
        else Image.open(src).convert("RGBA")

    if args.alpha == "luminance":
        img = luminance_alpha(img)
    sheet, frames, out_cols = regrid(img, args.cols, args.rows, args.cell,
                                     args.pack, args.every)
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{args.name}.png"
    sheet.save(dest)

    alpha = alpha_report(sheet)
    note = OUT / f"{args.name}.provenance.txt"
    note.write_text(
        f"{args.name}.png\n"
        f"  source      {src}\n"
        f"  source size {img.size[0]}x{img.size[1]}\n"
        f"  grid        source {args.cols}x{args.rows}, kept 1 in {args.every} -> "
        f"{out_cols} cols x {math.ceil(frames / out_cols)} rows = {frames} frames\n"
        f"  cell        {args.cell}px -> sheet {sheet.size[0]}x{sheet.size[1]} "
        f"(power-of-two; unused cells are transparent and never addressed)\n"
        f"  alpha       {alpha}{' (SYNTHESISED from luminance)' if args.alpha == 'luminance' else ''}\n"
        f"  exposure    {args.exposure} (EXR tonemap gain; ignored for LDR sources)\n"
        "\nNOT reproducible from this repo: the source is a local download. Re-run\n"
        "`python -m wowkb.vfxsheet` against the same file to regenerate.\n",
        encoding="utf-8")

    print(f"wrote {dest.relative_to(ROOT)} — {sheet.size[0]}x{sheet.size[1]}, "
          f"{out_cols}x{math.ceil(frames / out_cols)} = {frames} frames @ {args.cell}px")
    print(f"      alpha {alpha}")


if __name__ == "__main__":
    main()
