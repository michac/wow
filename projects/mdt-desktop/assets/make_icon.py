#!/usr/bin/env python3
"""Generate MDT Desktop's deterministic, size-aware Windows icon."""

from __future__ import annotations

import io
import struct
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
SIZES = (16, 32, 48, 64, 128, 256)


def _scaled_points(points: list[tuple[float, float]], scale: float) -> list[tuple[int, int]]:
    return [(round(x * scale), round(y * scale)) for x, y in points]


def _bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 32,
) -> list[tuple[float, float]]:
    points = []
    for index in range(steps + 1):
        t = index / steps
        u = 1.0 - t
        points.append(
            (
                u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
            )
        )
    return points


def render_icon(size: int) -> Image.Image:
    """Render one icon size; small sizes intentionally use simpler geometry."""
    oversample = 4
    canvas_size = size * oversample
    scale = canvas_size / 16.0
    image = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    def box(coords: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
        return tuple(round(value * scale) for value in coords)  # type: ignore[return-value]

    # Rounded badge: transparent corners keep the silhouette clean on any taskbar.
    draw.rounded_rectangle(
        box((0.35, 0.35, 15.65, 15.65)),
        radius=round(3.15 * scale),
        fill="#130D25",
        outline="#5A3A78",
        width=max(1, round(0.65 * scale)),
    )

    # One broad, irregular floor-plan silhouette. At 16px it stays a single mass;
    # larger sizes gain two chamber cuts that suggest a dungeon map without noise.
    dungeon = [
        (2.2, 10.0), (3.4, 10.0), (3.4, 6.9), (5.1, 6.9),
        (5.1, 4.7), (8.1, 4.7), (8.1, 2.6), (12.7, 2.6),
        (13.8, 3.8), (13.8, 7.0), (11.8, 7.0), (11.8, 9.2),
        (9.0, 9.2), (9.0, 11.4), (6.7, 11.4), (6.7, 13.5),
        (3.0, 13.5), (2.2, 12.6),
    ]
    draw.polygon(_scaled_points(dungeon, scale), fill="#2B1B49")

    if size >= 32:
        draw.line(
            _scaled_points([(3.7, 10.0), (6.7, 10.0), (6.7, 7.3)], scale),
            fill="#432762",
            width=max(1, round(0.38 * scale)),
        )
        draw.line(
            _scaled_points([(8.2, 5.0), (11.7, 5.0), (11.7, 6.8)], scale),
            fill="#432762",
            width=max(1, round(0.38 * scale)),
        )

    # A single readable route: dark keyline, pale-gold path, then three ordered
    # pull nodes. Unequal node sizes communicate progression without text.
    route = _bezier((3.35, 12.05), (3.1, 8.0), (12.9, 10.0), (12.15, 3.75))
    route_px = _scaled_points(route, scale)
    path_width = 1.45 if size <= 16 else 1.25
    draw.line(
        route_px,
        fill="#090612",
        width=max(1, round((path_width + 0.72) * scale)),
        joint="curve",
    )
    draw.line(
        route_px,
        fill="#FFC247",
        width=max(1, round(path_width * scale)),
        joint="curve",
    )

    nodes = [
        ((3.35, 12.05), 1.25, "#E88924"),
        ((8.10, 8.05), 1.40, "#F6A82D"),
        ((12.15, 3.75), 1.65, "#FFD45A"),
    ]
    for (x, y), radius, color in nodes:
        draw.ellipse(
            box((x - radius, y - radius, x + radius, y + radius)),
            fill=color,
            outline="#090612",
            width=max(1, round(0.52 * scale)),
        )

    # Tiny dark centers keep the dots distinct from the connecting route.
    center_radius = 0.33 if size <= 16 else 0.38
    for (x, y), _, _ in nodes:
        draw.ellipse(
            box((x - center_radius, y - center_radius, x + center_radius, y + center_radius)),
            fill="#21112F",
        )

    return image.resize((size, size), Image.Resampling.LANCZOS)


def write_ico(path: Path, images: list[Image.Image]) -> None:
    """Pack exact, independently rendered PNG frames into a Windows ICO."""
    payloads: list[bytes] = []
    for image in images:
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=False)
        payloads.append(buffer.getvalue())

    header_size = 6 + 16 * len(images)
    offset = header_size
    entries = []
    for image, payload in zip(images, payloads, strict=True):
        width, height = image.size
        entries.append(
            struct.pack(
                "<BBBBHHII",
                0 if width == 256 else width,
                0 if height == 256 else height,
                0,
                0,
                1,
                32,
                len(payload),
                offset,
            )
        )
        offset += len(payload)

    path.write_bytes(
        struct.pack("<HHH", 0, 1, len(images))
        + b"".join(entries)
        + b"".join(payloads)
    )


def verify_ico(path: Path) -> None:
    with Image.open(path) as icon:
        actual = set(icon.ico.sizes())
        expected = {(size, size) for size in SIZES}
        assert actual == expected, f"ICO sizes differ: expected {expected}, got {actual}"
        for size in SIZES:
            frame = icon.ico.getimage((size, size))
            frame.load()
            assert frame.size == (size, size)


def main() -> None:
    images = [render_icon(size) for size in SIZES]
    images[-1].save(ROOT / "icon.png", format="PNG", optimize=False)
    write_ico(ROOT / "icon.ico", images)
    verify_ico(ROOT / "icon.ico")
    print("Generated icon.png and icon.ico with sizes: " + ", ".join(map(str, SIZES)))


if __name__ == "__main__":
    main()
