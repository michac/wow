"""Generate SmartGlo/Media/*.tga from a Kenney source icon.

    uv --directory ../../tools run python ../projects/smart-glo/tool/gen_media.py

Two things this exists for. The shape is CENTRED in a square canvas, because a rotation
animation turns about the region's centre and an off-centre shape wobbles instead of
spinning. And the palette is baked one file per hue, because a band's inline texture escape
cannot be tinted at runtime: a colour escape reaches the band's TEXT and leaves the art full
white, and SetApplicationCount seals no VertexColor aspect to reach it through
(knowledge/addon-dev/security-taint-and-restricted-data.md §3.5).

`white` is the master the GATE uses, tinted with SetVertexColor to any value at all; the
named hues exist for the COUNT sink, which can only name a file.

Source art: Kenney "Board Game Icons" 1.1, CC0 (www.kenney.nl).
"""

import struct
from pathlib import Path

from PIL import Image

SOURCE = Path("/mnt/c/Users/mchris/Downloads/kenney_board-game-icons/PNG/Double (128px)/hexagon_outline.png")
OUT_DIR = Path(__file__).resolve().parents[1] / "addon" / "SmartGlo" / "Media"
SIDE = 64

PALETTE = {
    "white": (255, 255, 255),
    "yellow": (255, 209, 64),
    "red": (255, 82, 82),
    "green": (110, 231, 128),
    "blue": (96, 176, 255),
    "purple": (196, 132, 255),
    "orange": (255, 148, 64),
    "cyan": (94, 234, 232),
}


def squared(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    side = max(im.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    return canvas.resize((SIDE, SIDE), Image.LANCZOS)


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
    total = 0
    for name, rgb in PALETTE.items():
        total += write_tga(shape, rgb, OUT_DIR / f"hex-{name}.tga")
    print(f"wrote {len(PALETTE)} files, {total // 1024} KiB, into {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
