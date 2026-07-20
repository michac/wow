"""Core logic: resolve versions, download, install, update, remove.

No GUI, no CLI here — this module is pure so it can be tested headlessly and
driven by either the CLI (`ghaddons.cli`) or the Tk GUI (`ghaddons.gui`).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

API = "https://api.github.com"
UA = "ghaddons/0.1 (+https://github.com/)"

# .toc files can carry a game-flavor suffix (Foo_Mainline.toc, Foo-Vanilla.toc).
# The WoW addon folder name is the stem with that suffix stripped.
FLAVORS = {
    "mainline", "standard", "retail",
    "vanilla", "classic",
    "tbc", "bcc",
    "wrath", "wotlkc",
    "cata",
    "mists", "mop",
}


# --------------------------------------------------------------------------- #
# Config + manifest (both plain JSON, editable by hand or by the GUI)
# --------------------------------------------------------------------------- #
DEFAULT_ADDONS_DIR = (
    "/mnt/c/Program Files (x86)/World of Warcraft/_retail_/Interface/AddOns"
)


def normalize_addons_dir(raw: str) -> str:
    """Accept the AddOns path in either flavor and return the one that resolves
    on the interpreter actually running.

    The same WoW install has two names: `C:\\...` from native Windows Python and
    `/mnt/c/...` from WSL. Whichever form is sitting in config.json, only one of
    them exists on any given run — so a config written on one side used to make
    the other side fail with a bare "AddOns directory not found". Translating
    here means `python3 -m ghaddons.cli update <repo>` works first try from
    either shell, and nobody has to remember which one wrote the config.
    """
    s = (raw or "").strip()
    if not s:
        return s
    on_windows = os.name == "nt"
    m = re.match(r"^([A-Za-z]):[\\/](.*)$", s)          # C:\Foo\Bar  or  C:/Foo/Bar
    if m and not on_windows:
        return "/mnt/{}/{}".format(m.group(1).lower(), m.group(2).replace("\\", "/"))
    m = re.match(r"^/mnt/([A-Za-z])/(.*)$", s)          # /mnt/c/Foo/Bar
    if m and on_windows:
        return "{}:\\{}".format(m.group(1).upper(), m.group(2).replace("/", "\\"))
    return s


@dataclass
class Config:
    addons_dir: str = DEFAULT_ADDONS_DIR
    repos: list[str] = field(default_factory=list)
    token: str = ""  # optional GitHub PAT; raises the 60/hr anon rate limit

    @classmethod
    def load(cls, path: Path) -> "Config":
        if path.exists():
            d = json.loads(path.read_text())
            return cls(
                addons_dir=normalize_addons_dir(d.get("addons_dir", DEFAULT_ADDONS_DIR)),
                repos=list(d.get("repos", [])),
                token=d.get("token", "") or os.environ.get("GITHUB_TOKEN", ""),
            )
        return cls(token=os.environ.get("GITHUB_TOKEN", ""))

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {"addons_dir": self.addons_dir, "repos": self.repos, "token": self.token},
                indent=2,
            )
        )


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def save_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2))


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
def _req(url: str, token: str = "", accept: str = "application/vnd.github+json"):
    headers = {"User-Agent": UA, "Accept": accept}
    # Only authenticate calls to the API host; asset/codeload redirects to S3
    # can reject an unexpected Authorization header.
    if token and url.startswith(API):
        headers["Authorization"] = f"Bearer {token}"
    return urllib.request.Request(url, headers=headers)


def _api_json(url: str, token: str = "") -> dict | list:
    with urllib.request.urlopen(_req(url, token), timeout=30) as r:
        return json.load(r)


# --------------------------------------------------------------------------- #
# Version resolution
# --------------------------------------------------------------------------- #
@dataclass
class Resolved:
    version: str          # release tag, or "branch@shortsha"
    download_url: str
    source: str           # "release-asset" | "release-source" | "branch"
    published: str = ""


def _pick_asset(assets: list[dict]) -> dict | None:
    """Prefer a retail .zip asset; skip Classic/Vanilla/BCC packages."""
    zips = [a for a in assets if a.get("name", "").lower().endswith(".zip")]
    if not zips:
        return None
    bad = ("classic", "vanilla", "bcc", "tbc", "wrath", "wotlk", "cata", "mists")
    retail = [a for a in zips if not any(b in a["name"].lower() for b in bad)]
    return (retail or zips)[0]


def resolve(repo: str, token: str = "") -> Resolved:
    """Figure out what to download for `owner/repo`.

    Preference order: a packaged .zip asset on the latest release → the
    release's tagged source zip → the default branch's source zip.
    """
    owner_repo = repo.strip().strip("/")
    try:
        rel = _api_json(f"{API}/repos/{owner_repo}/releases/latest", token)
        asset = _pick_asset(rel.get("assets", []))
        if asset:
            return Resolved(
                version=rel.get("tag_name") or asset["name"],
                download_url=asset["browser_download_url"],
                source="release-asset",
                published=rel.get("published_at", ""),
            )
        # Release exists but ships no packaged zip → grab its tagged source.
        return Resolved(
            version=rel.get("tag_name", "latest"),
            download_url=f"https://codeload.github.com/{owner_repo}/zip/refs/tags/{rel.get('tag_name')}",
            source="release-source",
            published=rel.get("published_at", ""),
        )
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    # No releases at all → default branch snapshot, versioned by commit sha.
    meta = _api_json(f"{API}/repos/{owner_repo}", token)
    branch = meta.get("default_branch", "main")
    commit = _api_json(f"{API}/repos/{owner_repo}/commits/{branch}", token)
    sha = (commit.get("sha") or "")[:7]
    return Resolved(
        version=f"{branch}@{sha}" if sha else branch,
        download_url=f"https://codeload.github.com/{owner_repo}/zip/refs/heads/{branch}",
        source="branch",
        published=(commit.get("commit", {}).get("committer", {}) or {}).get("date", ""),
    )


# --------------------------------------------------------------------------- #
# Install / extract
# --------------------------------------------------------------------------- #
def _addon_name_from_toc(stem: str) -> str:
    for sep in ("-", "_"):
        if sep in stem:
            head, tail = stem.rsplit(sep, 1)
            if tail.lower() in FLAVORS:
                return head
    return stem


def _dirs(p: Path) -> list[Path]:
    return [c for c in p.iterdir() if c.is_dir() and c.name != "__MACOSX"]


def _tocs(p: Path) -> list[Path]:
    return [c for c in p.iterdir() if c.is_file() and c.suffix.lower() == ".toc"]


def _plan_addon_folders(extract_root: Path) -> list[tuple[str, Path]]:
    """Return [(addon_name, source_folder)] to copy into AddOns/.

    Handles three archive shapes: a packaged zip (addon folders at top level),
    a single-addon source zip (one wrapper dir whose contents include the .toc),
    and a multi-addon source zip (wrapper dir of addon subfolders).
    """
    root = extract_root
    # Descend through single-directory wrappers until we hit tocs or a fan-out.
    while not _tocs(root) and len(_dirs(root)) == 1:
        root = _dirs(root)[0]

    tocs = _tocs(root)
    if tocs:
        # root itself is the addon (source-zip single-addon repo).
        return [(_addon_name_from_toc(tocs[0].stem), root)]
    # Otherwise each immediate subdir that carries a .toc is its own addon.
    return [(sub.name, sub) for sub in _dirs(root) if _tocs(sub)]


def _copy_addon(src: Path, dest_dir: Path, name: str) -> None:
    target = dest_dir / name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(src, target, ignore=shutil.ignore_patterns("__MACOSX", ".git"))


def download(url: str, dest: Path, token: str = "") -> None:
    with urllib.request.urlopen(_req(url, token, accept="application/octet-stream"), timeout=120) as r:
        dest.write_bytes(r.read())


def install(repo: str, cfg: Config, manifest: dict) -> dict:
    """Download + install (or update) `repo`. Returns the manifest entry.

    Mutates `manifest` in place; caller is responsible for persisting it.
    """
    res = resolve(repo, cfg.token)
    addons_dir = Path(cfg.addons_dir)
    if not addons_dir.exists():
        raise FileNotFoundError(f"AddOns directory not found: {addons_dir}")

    with tempfile.TemporaryDirectory(prefix="ghaddons-") as tmp:
        tmp = Path(tmp)
        zip_path = tmp / "addon.zip"
        download(res.download_url, zip_path, cfg.token)
        extract_dir = tmp / "x"
        extract_dir.mkdir()
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)

        plan = _plan_addon_folders(extract_dir)
        if not plan:
            raise ValueError(f"No .toc found in {repo}'s archive — not a WoW addon?")

        # Replacing an existing install: clear its old folders first so renamed
        # or removed subfolders don't linger.
        old = manifest.get(repo, {}).get("folders", [])
        for name in old:
            stale = addons_dir / name
            if stale.exists():
                shutil.rmtree(stale)

        installed = []
        for name, src in plan:
            _copy_addon(src, addons_dir, name)
            installed.append(name)

    entry = {
        "version": res.version,
        "source": res.source,
        "folders": installed,
        "published": res.published,
    }
    manifest[repo] = entry
    return entry


def remove(repo: str, cfg: Config, manifest: dict) -> list[str]:
    """Delete a repo's installed folders and drop it from the manifest."""
    addons_dir = Path(cfg.addons_dir)
    removed = []
    for name in manifest.get(repo, {}).get("folders", []):
        target = addons_dir / name
        if target.exists():
            shutil.rmtree(target)
            removed.append(name)
    manifest.pop(repo, None)
    return removed


# --------------------------------------------------------------------------- #
# Status (what the UI/CLI list renders)
# --------------------------------------------------------------------------- #
@dataclass
class Status:
    repo: str
    installed: str = ""
    latest: str = ""
    state: str = ""       # not-installed | up-to-date | update-available | error
    folders: list[str] = field(default_factory=list)
    error: str = ""


def status_for(repo: str, cfg: Config, manifest: dict) -> Status:
    entry = manifest.get(repo, {})
    installed = entry.get("version", "")
    s = Status(repo=repo, installed=installed, folders=entry.get("folders", []))
    try:
        res = resolve(repo, cfg.token)
        s.latest = res.version
        if not installed:
            s.state = "not-installed"
        elif installed == res.version:
            s.state = "up-to-date"
        else:
            s.state = "update-available"
    except Exception as e:  # noqa: BLE001 — surface, don't crash the whole list
        s.state = "error"
        s.error = str(e)
    return s
