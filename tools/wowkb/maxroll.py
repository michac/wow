"""Export a maxroll.gg WoW guide → markdown, verbatim, for the KB.

maxroll.gg is a Remix app that ships the whole article in its server-rendered
`window.__remixContext` payload as WordPress **Gutenberg blocks** — so a single
plain HTTP GET is enough; no Playwright / headless browser needed. We pull the
JSON out of the HTML, walk the block tree, and render each block's `innerHTML`
to markdown with html2text (recursing through container blocks — tabs,
accordions, columns — whose text lives in `innerBlocks`, not the wrapper HTML).

**Fidelity first.** The point of this tool is to land the guide in the KB
*unedited*, so we distill on *read*, not on insert (distilling twice garbles).
So we go out of our way to keep what a naive html→text pass throws away:

  * **WoW entity IDs.** maxroll tags spells/traits/items/affixes with stable
    numeric IDs (`data-wow-id`, `data-wow-item`). We rewrite each into a
    Wowhead link (`spell=`/`item=`/`affix=`) so the ID survives — it's the most
    durable, most valuable part of the guide for a WoW KB.
  * **Planner embeds.** The `backend.maxroll.gg/wow/embed-tools/{talents,
    rotation,priority,paperdoll}=CODE` import strings are kept as labeled links.
  * **Images** (screenshots, BiS charts) are kept, not dropped.

Provenance + taxonomy are lifted straight from the payload — title, author,
publish/update dates, patch tag, class/spec, and content type — so `--kb` can
file the capture at knowledge/classes/<class>/<spec>/maxroll-<type>.md with
correct front matter, no slug-guessing.

Usage:
    uv run python -m wowkb.maxroll <url>            # → raw/maxroll/<slug>.md (scratch preview)
    uv run python -m wowkb.maxroll <url> --kb       # → knowledge/classes/<class>/<spec>/maxroll-<type>.md (verbatim, front matter)
    uv run python -m wowkb.maxroll <url> --kb --out <path>   # KB front matter, explicit path
    uv run python -m wowkb.maxroll <url> --json     # also dump the raw post JSON
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import html2text
import requests

from ._common import ROOT, save_raw

# A real browser UA — maxroll's edge is picky about obvious bots, and the SSR
# payload is only in the full HTML response.
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# Container blocks whose visible text lives in innerBlocks; the wrapper innerHTML
# is just chrome (empty divs) and must be ignored to avoid dropping content.
CONTAINER_BLOCKS = {
    "advgb/adv-tabs", "advgb/tab", "advgb/accordions", "advgb/accordion-item",
    "advgb/columns", "advgb/column", "core/columns", "core/column", "core/group",
}

# Purely decorative — no content worth carrying into the KB.
SKIP_BLOCKS = {"core/spacer", "core/separator", "maxroll/title-separator"}

# wow-<kind> span → Wowhead path. spell/trait/apexnode are all spell IDs.
WOWHEAD_TYPE = {
    "spell": "spell", "trait": "spell", "apexnode": "spell",
    "item": "item", "affix": "affix",
}
# <span class="wow-item" data-wow-item="250033:BONUS">Name</span>  (ID may carry a :bonus suffix)
WOW_SPAN = re.compile(
    r'<span class="wow-(spell|trait|item|affix|apexnode)"[^>]*'
    r'data-wow-(?:id|item)="(\d+)[^"]*"[^>]*>(.*?)</span>',
    re.S,
)
# The interactive planner import strings (talents / rotation / priority / paperdoll).
EMBED_URL = re.compile(r'(https://backend\.maxroll\.gg/wow/embed-tools/(\w+)=[\w-]+)')

# maxroll content-type taxonomy (metas) → KB filename suffix.
META_TO_TYPE = {"mythic+": "mplus", "raid": "raid", "leveling": "leveling", "pvp": "pvp"}

# The 13 WoW classes (slugified). maxroll's `classes` taxonomy lists class + spec
# but the ORDER is not consistent (DH is [class, spec], Warlock is [spec, class]),
# so we identify the class by membership here and treat the other term as the spec.
WOW_CLASSES = {
    "death-knight", "demon-hunter", "druid", "evoker", "hunter", "mage", "monk",
    "paladin", "priest", "rogue", "shaman", "warlock", "warrior",
}


def slugify(text: str) -> str:
    return re.sub(r"[^\w-]+", "-", text.lower()).strip("-")[:120] or "guide"


def _preserve_wow_entities(fragment: str) -> str:
    """Rewrite WoW spans → Wowhead <a> so their stable IDs survive html2text."""
    def repl(m):
        kind, wow_id, label = m.group(1), m.group(2), m.group(3)
        href = f"https://www.wowhead.com/{WOWHEAD_TYPE[kind]}={wow_id}"
        return f'<a href="{href}">{label}</a>'
    fragment = WOW_SPAN.sub(repl, fragment)
    fragment = EMBED_URL.sub(lambda m: f'<a href="{m.group(1)}">Maxroll {m.group(2)} import</a>', fragment)
    return fragment


def _html(fragment: str) -> str:
    """innerHTML → markdown, keeping links, images, and WoW IDs."""
    h = html2text.HTML2Text()
    h.ignore_images = False
    h.body_width = 0
    return h.handle(_preserve_wow_entities(fragment)).strip()


def _text(fragment: str) -> str:
    """innerHTML → single-line plain text (for tab / accordion headers)."""
    return re.sub(r"\s+", " ", _html(fragment)).strip().strip("#").strip()


def extract_remix_context(html: str) -> dict:
    """Pull the `window.__remixContext = {…};` object out of the page HTML."""
    m = re.search(r"window\.__remixContext\s*=\s*", html)
    if not m:
        sys.exit("error: no __remixContext in page — maxroll layout may have changed")
    start = html.index("{", m.end())
    depth, instr, esc = 0, None, False
    for i in range(start, len(html)):
        c = html[i]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == instr:
                instr = None
        elif c in "\"'":
            instr = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(html[start : i + 1])
    sys.exit("error: could not brace-match __remixContext object")


def find_post(ctx: dict) -> dict:
    """Locate the article post in the Remix loaderData (route key can vary)."""
    for route in ctx.get("state", {}).get("loaderData", {}).values():
        if isinstance(route, dict) and isinstance(route.get("post"), dict):
            return route["post"]
    sys.exit("error: no post found in loaderData — is this a maxroll guide URL?")


def render_block(block: dict, out: list) -> None:
    name = block.get("blockName")
    if name in SKIP_BLOCKS or name is None:
        return

    attrs = block.get("attributes") or {}
    inner = block.get("innerBlocks") or []

    # Tab / accordion items carry their label in attributes.header — surface it
    # as a bold lead-in so the section structure survives distillation.
    header = attrs.get("header") if isinstance(attrs, dict) else None
    if header:
        out.append(f"**{_text(header)}**\n")

    if name in CONTAINER_BLOCKS or (inner and not _html(block.get("innerHTML", ""))):
        for child in inner:
            render_block(child, out)
        return

    md = _html(block.get("innerHTML", ""))
    if md and not md.lstrip().startswith("[inplace_ad"):
        out.append(md + "\n")
    for child in inner:
        render_block(child, out)


def _tax(post: dict, key: str) -> list:
    return list((post.get("taxonomies") or {}).get(key) or [])


def render_body(post: dict) -> str:
    parts: list[str] = []
    for block in post.get("gutenbergBlock", []):
        render_block(block, parts)
    body = "\n".join(parts)
    body = re.sub(r"\*{3,}", "**", body)  # collapse stacked <strong><mark> nesting
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def detect_patch(post: dict, body: str) -> str | None:
    for t in _tax(post, "postTag"):
        m = re.search(r"\b(\d+\.\d+\.\d+)\b", t)
        if m:
            return m.group(1)
    m = re.search(r"patch\s+(\d+\.\d+\.\d+)", body, re.I)
    return m.group(1) if m else None


def kb_path(post: dict) -> Path:
    """knowledge/classes/<class>/<spec>/maxroll-<type>.md from the taxonomy."""
    classes = _tax(post, "classes")
    slugged = [slugify(c) for c in classes]
    known = [s for s in slugged if s in WOW_CLASSES]
    others = [s for s in slugged if s not in WOW_CLASSES]
    if len(known) != 1 or len(others) != 1:
        sys.exit(
            "error: --kb needs exactly one class + one spec, but got "
            f"{classes!r} — this may be a non-class guide; pass --out <path> instead"
        )
    cls, spec = known[0], others[0]
    metas = _tax(post, "metas")
    ctype = META_TO_TYPE.get(metas[0].lower(), slugify(metas[0])) if metas else "guide"
    return ROOT / "knowledge" / "classes" / cls / spec / f"maxroll-{ctype}.md"


def render_kb(post: dict, url: str, body: str) -> str:
    """Verbatim body under KB YAML front matter with attribution."""
    today = datetime.date.today().isoformat()
    patch = detect_patch(post, body)
    author = (post.get("author") or {}).get("name") or "unknown"
    fm = ["---", f"title: {post.get('title', url)}"]
    if patch:
        fm.append(f"patch: {patch}")
    fm += [
        f"fetched: {today}",
        f"reviewed: {today}",  # captured, not independently re-verified — see confidence
        "sources:",
        f"  - {url} (maxroll.gg, Tier 3)",
        "confidence: medium",
        "verbatim: true          # unedited external capture — distill on read, not on insert",
        "source: maxroll.gg",
        f"author: {author}",
    ]
    if post.get("modifiedIso"):
        fm.append(f"maxroll_updated: {post['modifiedIso']}   # source's last-modified (staleness signal)")
    fm.append("---")
    return "\n".join(fm) + "\n\n" + body + "\n"


def render_scratch(post: dict, url: str, body: str) -> str:
    """Lightweight header for raw/ scratch previews (no YAML front matter)."""
    today = datetime.date.today().isoformat()
    patch = detect_patch(post, body)
    lines = [f"# {post.get('title', url)}", "", f"- url: {url}",
             f"- source: maxroll.gg — {post.get('category', 'guide')}"]
    if (post.get("author") or {}).get("name"):
        lines.append(f"- author: {post['author']['name']}")
    if patch:
        lines.append(f"- patch: {patch}")
    if post.get("date"):
        lines.append(f"- published: {post['date']}")
    if post.get("modified"):
        iso = post.get("modifiedIso")
        lines.append(f"- updated: {post['modified']}" + (f" ({iso})" if iso else ""))
    lines += [f"- fetched: {today}", "", "---", "", body, ""]
    return "\n".join(lines)


def export(url: str, kb: bool, out: str | None, dump_json: bool) -> None:
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()
    post = find_post(extract_remix_context(resp.text))
    body = render_body(post)
    slug = post.get("slug") or slugify(urlparse(url).path.rsplit("/", 1)[-1])

    if kb:
        path = Path(out) if out else kb_path(post)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_kb(post, url, body), encoding="utf-8")
    elif out:
        path = Path(out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_scratch(post, url, body), encoding="utf-8")
    else:
        path = save_raw("maxroll", f"{slug}.md", render_scratch(post, url, body))
    print(path)

    if dump_json:
        print(save_raw("maxroll", f"{slug}.post.json", json.dumps(post, indent=2)))


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.maxroll", description=__doc__)
    p.add_argument("url")
    p.add_argument("--kb", action="store_true",
                   help="write verbatim into knowledge/classes/<class>/<spec>/ with front matter")
    p.add_argument("--out", help="explicit output path (overrides the default location)")
    p.add_argument("--json", action="store_true", help="also dump the raw post JSON")
    args = p.parse_args()
    export(args.url, args.kb, args.out, args.json)


if __name__ == "__main__":
    main()
