"""Measure how much each style-lab candidate CHANGES over time once blurred.

    uv --directory ../../tools run python ../projects/smart-glo/tool/measure_motion.py

Why this exists. The lab answers "can I still see it" by eye. It cannot answer "is it
moving", because the page is looked at in screenshots and a screenshot pair is separated by
an uncontrolled interval — a 3s spin sampled 3s apart has moved nowhere. This renders the
same compositing offline at a controlled time step, so the number means something.

What it reports — TWO numbers, because they disagree and the disagreement is the finding.

**rate** is the mean absolute luminance difference between CONSECUTIVE blurred frames. It is
a derivative, so it rewards fast change and penalises slow change regardless of how large the
slow change eventually gets. The magnocellular pathway is genuinely transient-driven, so this
is the right axis for "did something just happen".

**swing** is the per-pixel max minus min across the whole period, averaged. It is an
amplitude, blind to rate. A 4s swell that moves a lot of light scores high here and low on
rate; a fast shimmer that moves little light does the opposite.

⚠ **Neither alone is the answer, and a candidate that wins one while losing the other is a
candidate whose behaviour you have to go and look at.** The breathing-plate designs are
exactly that case.

⚠ **It is a proxy and it has a known blind spot.** It cannot tell a change that draws the eye
from one that merely annoys, it treats a colour cycle and a moving blob as the same kind of
event when the periphery does not, and it says nothing about whether plain and urgent stay
TELLABLE APART — only about how much each one moves. Rank with it; decide by looking.
"""

import math
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_site as G

SIDE = 96          # render size, comfortably above the 56px the client draws
ECCENTRICITY = 12.0   # degrees off-axis; where the Essential viewer sits while you watch
                      # your character. The lab page carries the geometry this comes from.
# A ball DROPPED and left to settle: it starts AT its apex, then parabolic arcs whose height
# falls by BOB_E each hop and whose duration falls as its square root, then a rest. ⚠ These are
# the LAB's numbers (gen_site.py's LAB), not the addon's: nothing shipping bounces. Everything
# else on this page still comes out of `Look.lua`.
_LOOK = G.page_look()
BOB_SECONDS = _LOOK["lab"]["bounceSeconds"]
BOB_HEIGHT = _LOOK["lab"]["bounceHeight"]
BOB_E = _LOOK["lab"]["bounceE"]
BOB_HOPS = int(_LOOK["lab"]["bounceHops"])
BOB_REST = _LOOK["lab"]["bounceRest"]
# The chain of HALF-arcs — one fall for the drop, then a rise and a fall per bounce — mirroring
# glow.js and `Look.Bounce`'s ordered Translations.
_BOB_SEG = []
for _i in range(BOB_HOPS):
    _h = BOB_E ** _i
    _d = math.sqrt(_h) / 2
    if _i:
        _BOB_SEG.append((_h, _d, True))
    _BOB_SEG.append((_h, _d, False))
_BOB_TOTAL = sum(d for _, d, _up in _BOB_SEG)


def bounce(phase: float) -> float:
    span = 1 - BOB_REST
    if phase >= span:
        return 0.0
    x = phase / span * _BOB_TOTAL
    for h, d, up in _BOB_SEG:
        if x < d:
            t = x / d
            return h * (2 * t - t * t) if up else h * (1 - t * t)
        x -= d
    return 0.0
ICON_DEGREES = 0.9    # a CDM icon's angular size — a 40px icon at ~45 px/deg
# MAR(E) = MAR0 (1 + E/E2), the standard linear acuity falloff, sigma = half the minimum
# resolvable angle. This is the SAME model the style lab's slider uses; keep them together.
BLUR = ((1 + ECCENTRICITY / 2.3) / 60) / 2 / ICON_DEGREES * SIDE
# ⚠ The step must resolve the FASTEST motion, not just tile the slowest. At 0.25s the 0.45s
# pulse and the 0.56s bounce arc got two samples each and the rate column was measuring the
# sampler. 0.05s gives ~9 and ~11. PERIOD is a common multiple of every period in play —
# spin 3s, cycle 0.6s, pulse 0.45s, bounce 0.9s — so no candidate is judged on a partial
# cycle of its own animation.
PERIOD = 9.0
STEPS = 180


def solid(mask: Image.Image, rgb, size: int) -> Image.Image:
    """A mask over a solid fill — the same operation as SetVertexColor on a white master."""
    layer = Image.new("RGBA", (size, size), rgb + (0,))
    layer.putalpha(mask.resize((size, size), Image.LANCZOS))
    return layer


def rgba(fill: str, pair):
    if fill == "tint":
        return None                       # resolved per frame
    if fill == "a":
        return tuple(round(v * 255) for v in pair[0]) + (255,)
    if fill == "b":
        return tuple(round(v * 255) for v in pair[1]) + (255,)
    if fill.startswith("rgba"):
        parts = fill[fill.index("(") + 1:fill.index(")")].split(",")
        return (int(parts[0]), int(parts[1]), int(parts[2]), round(float(parts[3]) * 255))
    if fill == "#000":
        return (0, 0, 0, 255)
    return (255, 255, 255, 255)


def wave(phase, cross):
    hold = (1 - 2 * cross) / 2
    if phase < hold:
        return 0.0
    if phase < hold + cross:
        return (phase - hold) / cross
    if phase < 2 * hold + cross:
        return 1.0
    return 1 - (phase - 2 * hold - cross) / cross


def frame(style, backdrop, masks, look, pair, t, urgent):
    """One composited tile at time `t` — the same transform chain glow.js applies."""
    tile = backdrop.copy()
    # Urgent may run its own clock — a RATE on the shared phase, so urgent glows stay locked
    # to each other while drifting against plain ones. Mirrors glow.js.
    u = t * (style.get("urgentRate", 1.0) if urgent else 1.0)
    hue = wave((u % look["cycleSeconds"]) / look["cycleSeconds"], look["cycleCross"])
    tint = tuple(round(255 * (pair[0][i] + (pair[1][i] - pair[0][i]) * hue))
                 for i in range(3)) + (255,)
    spin = (u % look["spinSeconds"]) / look["spinSeconds"] * look["spinDegrees"]
    p = (t % look["pulseSeconds"]) / look["pulseSeconds"]
    ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * x)
    pulse = 1 + (look["pulseScale"] - 1) * (ease(p * 2) if p < 0.5 else ease((1 - p) * 2))

    for spec in style["layers"]:
        scale = spec.get("scale", 1.0)
        if spec.get("breathe"):
            amp, secs = spec["breathe"]
            scale *= 1 + amp * math.sin(2 * math.pi * t / secs)
        mode = "none" if spec.get("still") else style.get("urgentMotion", "pulse")
        if urgent and mode == "pulse":
            scale *= pulse
        size = max(2, round(SIDE * look["fraction"] * scale))

        # A layer's own `cycle` replaces the palette's endpoints on the SAME shared wave.
        if spec.get("cycle"):
            lo, hi_ = spec["cycle"]
            fill = tuple(round(255 * (lo[i] + (hi_[i] - lo[i]) * hue))
                         for i in range(3)) + (255,)
        else:
            fill = rgba(spec["fill"], pair) or tint
        angle = spin * spec.get("spin", 1)
        art = solid(masks[spec["mask"]].rotate(-angle, Image.BICUBIC), fill[:3], size)
        if fill[3] != 255:
            art.putalpha(art.split()[3].point(lambda v: v * fill[3] // 255))
        # `fade` mirrors glow.js: [minAlpha, seconds]; a period of 0 is a fixed dim.
        if spec.get("fade"):
            lo, secs = spec["fade"]
            a = lo if not secs else lo + (1 - lo) * (
                0.5 + 0.5 * math.sin(2 * math.pi * t / secs))
            art.putalpha(art.split()[3].point(lambda v: round(v * a)))

        # `rotate(θ) translateX(d)` puts the layer d along the ROTATED x axis.
        off = spec.get("orbit", 0) * size
        cx = (SIDE - size) / 2 + off * math.cos(math.radians(angle))
        cy = (SIDE - size) / 2 + off * math.sin(math.radians(angle))
        # Screen-space vertical, in percent of the layer's own size, matching glow.js.
        if urgent and mode == "bob":
            cy -= BOB_HEIGHT * size * bounce((t % BOB_SECONDS) / BOB_SECONDS)
        tile.alpha_composite(art, (round(cx), round(cy)))
    return tile.convert("L").filter(ImageFilter.GaussianBlur(BLUR))


def main() -> int:
    look = _LOOK
    pair = [look["palette"][n] for n in look["cycles"][look["default"]]]
    masks = {p.stem: Image.open(p).convert("RGBA").split()[3]
             for p in G.OUT.glob("hex-*.png")}
    masks.update({p.stem: Image.open(p).convert("RGBA").split()[3]
                  for p in list(G.OUT.glob("tri-*.png")) + list(G.OUT.glob("dot-*.png"))})
    backdrops = [Image.open(G.OUT / G.icon_name(sid)).convert("RGBA")
                 .resize((SIDE, SIDE), Image.LANCZOS) for sid, _, _ in G.BACKDROPS]

    print(f"at {ECCENTRICITY:g} deg off-axis (sigma {BLUR:.2f}px at {SIDE}px), "
          f"{STEPS} samples over {PERIOD:g}s\n"
          f"⚠ rate is per-{PERIOD / STEPS:.2f}s step — comparable WITHIN this table only, "
          f"never across runs with a different step. swing is step-independent.\n")
    print(f"{'style':48}{'plain rate':>11}{'plain swing':>13}"
          f"{'urgent rate':>13}{'urgent swing':>14}")
    rows = []
    for style in G.STYLES:
        scores = {}
        for urgent in (False, True):
            total, n, swings = 0.0, 0, []
            for bd in backdrops:
                prev, lo, hi = None, None, None
                for i in range(STEPS + 1):
                    cur = list(frame(style, bd, masks, look, pair,
                                     i * PERIOD / STEPS, urgent).getdata())
                    if prev is not None:
                        total += sum(abs(a - b) for a, b in zip(cur, prev)) / len(cur)
                        n += 1
                        lo = [min(a, b) for a, b in zip(lo, cur)]
                        hi = [max(a, b) for a, b in zip(hi, cur)]
                    else:
                        lo = hi = cur
                    prev = cur
                swings.append(sum(h - l for h, l in zip(hi, lo)) / len(lo))
            scores[urgent] = (total / n, sum(swings) / len(swings))
        rows.append((scores[False], style["name"], scores[True]))

    for plain, name, urgent in sorted(rows, reverse=True):
        print(f"{name:48}{plain[0]:11.2f}{plain[1]:13.2f}"
              f"{urgent[0]:13.2f}{urgent[1]:14.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
