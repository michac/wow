"""Polite page fetch → markdown, saved to raw/pages/.

Usage:
    uv run python -m wowkb.fetch https://www.icy-veins.com/wow/weekly-to-do-list
"""

import argparse
import datetime
import re
from urllib.parse import urlparse

import html2text
import requests

from ._common import save_raw

UA = "wowkb/0.1 (personal knowledge base; respectful, low-volume)"


def slugify(url: str) -> str:
    parsed = urlparse(url)
    slug = re.sub(r"[^\w-]+", "-", f"{parsed.netloc}{parsed.path}").strip("-")
    return slug[:120] or "page"


def fetch(url: str) -> None:
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=60)
    resp.raise_for_status()

    h = html2text.HTML2Text()
    h.ignore_images = True
    h.body_width = 0
    body = h.handle(resp.text)

    title_match = re.search(r"<title[^>]*>(.*?)</title>", resp.text, re.S | re.I)
    title = title_match.group(1).strip() if title_match else url
    header = (
        f"# {title}\n\n"
        f"- url: {url}\n"
        f"- fetched: {datetime.date.today().isoformat()}\n\n---\n\n"
    )
    out = save_raw("pages", f"{slugify(url)}.md", header + body)
    print(out)


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.fetch", description=__doc__)
    p.add_argument("url")
    fetch(p.parse_args().url)


if __name__ == "__main__":
    main()
