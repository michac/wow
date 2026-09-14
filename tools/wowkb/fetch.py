"""Polite page fetch → markdown, to raw/pages/ or (with --kb) into the KB.

    uv run python -m wowkb.fetch <url>                 # → raw/pages/<slug>.md
    uv run python -m wowkb.fetch <url> --kb            # → knowledge/classes/<class>/<spec>/…
    uv run python -m wowkb.fetch <url> --kb --out PATH # explicit destination

**The KB door lands the page WHOLE**, `verbatim: true`, exactly as `wowkb.maxroll --kb`
does — the doctrine is distil on *read*, not on insert, because distilling twice garbles.
So this trims the page to its `<main>` element and stops. That is a semantic container
rather than a per-site selector, and on Icy Veins it drops 712 lines to 263 while keeping
the breadcrumb, the patch tag and every priority list.

⚠ **Tier 3.** `knowledge/addon-dev/sources.md` §0 and the game KB's `_meta/sources.md`
agree: a mature guide site shows *what works in practice*, never *what the rules are*, and
the APL and DB2 outrank it on anything they actually say. The front matter says
`confidence: medium` for that reason and it should stay there.
"""

import argparse
import datetime
import re
from pathlib import Path
from urllib.parse import urlparse

import html2text
import requests

from ._common import save_raw

UA = "wowkb/0.1 (personal knowledge base; respectful, low-volume)"


def slugify(url: str) -> str:
    parsed = urlparse(url)
    slug = re.sub(r"[^\w-]+", "-", f"{parsed.netloc}{parsed.path}").strip("-")
    return slug[:120] or "page"


REPO = Path(__file__).resolve().parents[2]
CLASSES = REPO / "knowledge" / "classes"

#: Slug word -> the `<type>` half of the KB filename. First match wins, so the more
#: specific words come first: a "rotation-cooldowns-abilities" page is a rotation.
KINDS = (
    ("rotation", "rotation"), ("talent", "talents"), ("stat", "stats"),
    ("bis", "gear"), ("gear", "gear"), ("consumable", "consumables"),
    ("mythic", "mythic-plus"), ("raid", "raid"), ("macro", "macros"),
    ("overview", "overview"), ("guide", "overview"),
)


def _main_only(html: str) -> str:
    """The page's `<main>`, or the whole thing when it has none."""
    lowered = html.lower()
    start, end = lowered.find("<main"), lowered.rfind("</main>")
    if start == -1 or end <= start:
        return html
    return html[start:end]


def _taxonomy(url: str):
    """class, spec and kind off the URL slug, or None when the slug does not say.

    Icy Veins spells it out -- `/wow/protection-paladin-pve-tank-rotation-...` -- so the
    class is whichever known class name appears and the spec is a directory that exists
    beside it. Anything else returns None and the caller asks for `--out` rather than
    guessing a path into the KB.
    """
    words = [w for w in re.split(r"[^a-z]+", urlparse(url).path.lower()) if w]
    classes = {d.name: d for d in CLASSES.iterdir() if d.is_dir()}
    for i, word in enumerate(words):
        folder = classes.get(word)
        if folder is None:
            continue
        for spec in (d.name for d in folder.iterdir() if d.is_dir()):
            if spec in words[max(0, i - 3):i + 4]:
                kind = next((k for w, k in KINDS if w in words or
                             any(w in x for x in words)), "overview")
                return word, spec, kind
    return None


def fetch(url: str, to_kb: bool = False, out=None) -> None:
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()

    h = html2text.HTML2Text()
    h.ignore_images = True
    h.body_width = 0
    body = h.handle(_main_only(resp.text) if to_kb else resp.text)

    match = re.search(r"<title[^>]*>(.*?)</title>", resp.text, re.S | re.I)
    title = match.group(1).strip() if match else url
    today = datetime.date.today().isoformat()

    if not to_kb:
        header = f"# {title}\n\n- url: {url}\n- fetched: {today}\n\n---\n\n"
        print(save_raw("pages", f"{slugify(url)}.md", header + body))
        return

    if out is None:
        found = _taxonomy(url)
        if found is None:
            raise SystemExit(f"cannot tell which spec {url} is about -- pass --out")
        cls, spec, kind = found
        host = urlparse(url).netloc.replace("www.", "").split(".")[0]
        out = CLASSES / cls / spec / f"{host}-{kind}.md"

    # The patch the page claims, so staleness reads off the front matter.
    patch = re.search(r"\b(\d+\.\d+(?:\.\d+)?)\b", title)
    front = "\n".join([
        "---",
        f"title: {title}",
        f"patch: {patch.group(1) if patch else 'unknown'}",
        f"fetched: {today}",
        f"reviewed: {today}",
        "sources:",
        f"  - {url}",
        "verbatim: true",
        "confidence: medium",
        "---",
        "",
    ])
    path = Path(out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front + body, encoding="utf-8")
    print(path)


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.fetch", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url")
    p.add_argument("--kb", action="store_true",
                   help="land it in knowledge/ with front matter instead of raw/pages/")
    p.add_argument("--out", help="explicit destination for --kb")
    args = p.parse_args()
    fetch(args.url, to_kb=args.kb, out=args.out)


if __name__ == "__main__":
    main()
