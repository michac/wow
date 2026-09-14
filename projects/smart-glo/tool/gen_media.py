"""Generate SmartGlo/Media/*.tga — the mark from a Kenney source icon, the plate from the mark.

    uv --directory ../../tools run python ../projects/smart-glo/tool/gen_media.py

One file, and one reason for the shape. The mark is CENTRED in a square canvas because a
rotation animation turns about the region's centre and an off-centre shape wobbles instead
of spinning.

⚠ **One hue is all there is, and that follows from the occluder.** `white` is the master
every mark is drawn from, tinted at runtime with SetVertexColor. Baking a file per hue was
right while a count's mark was drawn AS a band's inline texture escape, which cannot be
tinted (a colour escape reaches the band's TEXT and leaves the art full white, and
SetApplicationCount seals no VertexColor aspect to reach it through —
knowledge/addon-dev/security-taint-and-restricted-data.md §3.5). The count sink now draws
the subject's own cropped icon as an OCCLUDER over that same white master, so the escape
carries no hue at all and nothing but `Look.MASTER` is ever named by filename.

⚠ **The plate is derived from the MARK, not from the source.** `SOURCE` is a Windows Downloads
path outside the repo, so anything that depends on it cannot be rebuilt without re-downloading
it; `hex-fill` is the mark's own alpha flood-filled from the centre, which needs nothing but the
file beside it.

⚠ **The plate's translucency is BAKED IN, and `PLATE_ALPHA` is read out of `Look.lua`** rather
than written here. It has to be in the art: `SetVertexColor`'s fourth argument and `SetAlpha`
are one channel, so the alpha write that says whether a plate is drawn at all would clobber a
translucency set at build `[client 2026-09-11]`. Reading the constant keeps one number in one
place, and a rename fails this build rather than shipping a stale plate.

Source art: Kenney "Board Game Icons" 1.1, CC0 (www.kenney.nl).
"""

import re
import struct
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

SOURCE = Path("/mnt/c/Users/mchris/Downloads/kenney_board-game-icons/PNG/Double (128px)/hexagon_outline.png")
ADDON = Path(__file__).resolve().parents[1] / "addon" / "SmartGlo"
OUT_DIR = ADDON / "Media"
SIDE = 64


def plate_alpha() -> float:
    """`Look.PLATE_ALPHA`, from the source of truth. A rename is a build failure, not a silently
    stale file — the same contract `tool/gen_site.py`'s `read_look` keeps."""
    text = (ADDON / "Look.lua").read_text()
    m = re.search(r"^Look\.PLATE_ALPHA\s*=\s*([\d.]+)", text, re.M)
    if m is None:
        raise SystemExit("gen_media.py is stale: Look.PLATE_ALPHA is gone from Look.lua")
    return float(m.group(1))

# The hue names the rule language offers live in Look.lua's PALETTE and in
# wowkb.smartglo's COLORS; they are TINTS applied to this one master, never files.
PALETTE = {
    "white": (255, 255, 255),
}


def squared(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    side = max(im.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return canvas.resize((SIDE, SIDE), Image.LANCZOS)


def flooded(shape: Image.Image, alpha: float) -> Image.Image:
    """The outline's own alpha, flooded solid from the centre, then scaled to `alpha`.

    ⚠ The flood runs on a COPY OF THE ALPHA, never on a blank canvas: the stroke is the only
    thing that stops it, and on a blank canvas it fills the whole square.
    ⚠ `thresh` is not optional either. The stroke's inner edge is anti-aliased, so an
    exact-match fill halts on the first partially-opaque pixel and leaves a ring of soft alpha
    unfilled — a visible seam between plate and stroke. 200 crosses that edge and still stops
    inside the stroke proper. `lighter` puts the stroke back over the fill, so the plate is the
    whole hexagon and not only its interior."""
    a = shape.split()[3]
    inside = a.copy()
    ImageDraw.floodfill(inside, (a.width // 2, a.height // 2), 255, thresh=200)
    filled = ImageChops.lighter(inside, a)
    out = shape.copy()
    out.putalpha(filled.point(lambda v: round(v * alpha)))
    return out


def write_tga(image: Image.Image, rgb, path: Path) -> int:
    px = image.load()
    data = bytearray()
    for y in range(SIDE):
        for x in range(SIDE):
            data += bytes((rgb[2], rgb[1], rgb[0], px[x, y][3]))
    header = struct.pack("<BBBHHBHHHHBB", 0, 0, 2, 0, 0, 0, 0, 0, SIDE, SIDE, 32, 0x28)
    path.write_bytes(header + bytes(data))
    return len(header) + len(data)


def main() -> int:
    if not SOURCE.exists():
        print(f"error: source art not found at {SOURCE}")
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shape = squared(SOURCE)
    total, files = 0, 0
    for name, rgb in PALETTE.items():
        total += write_tga(shape, rgb, OUT_DIR / f"hex-{name}.tga")
        files += 1
    # White here too: the plate's HUE is `Look.PLATE_RGB`, applied at runtime in three
    # arguments. Only the translucency is baked, and only because the alpha channel is spoken
    # for.
    total += write_tga(flooded(shape, plate_alpha()), (255, 255, 255),
                       OUT_DIR / "hex-fill.tga")
    files += 1
    print(f"wrote {files} files, {total // 1024} KiB, into {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
