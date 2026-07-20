# ghaddons — a GitHub-driven WoW addon manager

CurseForge minus the catalog: give it a list of `owner/repo`s and it pulls each
one's latest release (or default-branch snapshot), unzips the addon folder(s)
into `Interface/AddOns/`, tracks versions, and updates/removes on demand.

**Stdlib only** — no pip install, no Node, no CurseForge account. Runs on the
system `python3` (3.11+). The GUI additionally needs Tk (see below).

## Why GitHub-driven

Most quality WoW addons publish releases on GitHub — many via the BigWigs
packager action, which produces a correctly-structured `.zip` per release.
`ghaddons` prefers that packaged asset, then falls back to the tagged source
zip, then to a default-branch snapshot (versioned by commit sha) for addons
that don't cut releases.

## Setup

```bash
cp config.example.json config.json      # then edit: set addons_dir + repos
```

`config.json` (gitignored — it can hold a token):

```json
{
  "addons_dir": "/mnt/c/Program Files (x86)/World of Warcraft/_retail_/Interface/AddOns",
  "token": "",
  "repos": ["BigWigsMods/BigWigs", "WeakAuras/WeakAuras2"]
}
```

- **`addons_dir`** — your live AddOns folder. **Either flavor works**: the WSL
  `/mnt/c/Program Files (x86)/...` path or the native Windows
  `C:\Program Files (x86)\...` one. They name the same folder but only one of
  them resolves on any given interpreter, so ghaddons translates whichever is in
  the config to whichever side it's running on. You never have to remember which
  shell wrote it.
- **`token`** — optional GitHub PAT. Empty = anonymous API (60 requests/hour,
  fine for a modest list). Also read from `$GITHUB_TOKEN`.

## CLI (works today)

```bash
cd addon-manager
python3 -m ghaddons.cli list                       # status of every configured repo
python3 -m ghaddons.cli add   Nevcairiel/Bartender4
python3 -m ghaddons.cli install --all              # install everything not yet installed
python3 -m ghaddons.cli update --all               # update only what's out of date
python3 -m ghaddons.cli update Nevcairiel/Bartender4
python3 -m ghaddons.cli remove Nevcairiel/Bartender4   # delete its installed folders
python3 -m ghaddons.cli rm     Nevcairiel/Bartender4   # drop from config, keep files
python3 -m ghaddons.cli path  "/mnt/c/.../Interface/AddOns"   # show/set AddOns dir
```

`list` marks each repo `ok` (up to date), `UPD` (update available), `--`
(not installed), or `ERR`.

### Running it from anywhere

`ghaddons` keeps `config.json` / `installed.json` next to its own package, not in
the current directory, so it doesn't care where you invoke it from — it only has
to be importable:

```bash
PYTHONPATH=~/code/fun/wow/addon-manager python3 -m ghaddons.cli update michac/CDMProbe
```

Use that form in per-addon deploy docs and scripts; it works first try from any
directory, from WSL or from Windows `python`. If you're already sitting in
`addon-manager/`, plain `python3 -m ghaddons.cli ...` is identical.

## Deploying an addon you're developing

For your own addons (`michac/CDMProbe`, `michac/wow-planner-state`,
`michac/BucketBinds`), **a `git push` does not reach the game.** ghaddons installs
from the **latest GitHub release**, so the deploy is always three steps:

```bash
# 1. bump ## Version: in the addon's .toc, commit, push
gh release create v0.6.0 --title v0.6.0 --repo michac/CDMProbe --notes "..."

# 2. pull it into Interface/AddOns
PYTHONPATH=~/code/fun/wow/addon-manager python3 -m ghaddons.cli update michac/CDMProbe

# 3. in-game
/reload
```

The release tag must match the `.toc` `## Version:` prefixed with `v` — that
pairing is what makes `ghaddons list` report `ok` instead of `UPD` forever. Each
addon repo's own `CLAUDE.md` carries the rest of its release checklist (syntax
check, schema bumps, smoke test).

## GUI (optional)

```bash
sudo apt install python3-tk     # one-time; WSLg renders the window on Windows 11
python3 -m ghaddons.gui
```

A single window: a table of your addons with installed/latest/status columns,
an "add repo" box, and Install/Update-all/Remove buttons. Network work runs off
the UI thread so it never freezes.

## How it decides what to install

1. `GET /repos/{owner}/{repo}/releases/latest` → prefer a retail `.zip` asset
   (skips Classic/Vanilla/BCC/… packages).
2. No packaged asset → the release's tagged **source** zip.
3. No releases at all → the **default branch** zip, versioned `branch@sha`.

On extract it finds addon folders by their `.toc` files (folder name = toc name
with any `_Mainline`/`-Vanilla`/… flavor suffix stripped), handling packaged
zips, single-addon source zips (with the `repo-hash/` wrapper), and multi-addon
suites. Installed folders are recorded in `installed.json` so updates replace
cleanly and removes are exact.

## Limits (it's deliberately basic)

- No dependency resolution between addons.
- Version compare is exact-match on tag/sha, not semver ordering.
- Deeply-nested vendored libraries that ship their own `.toc` at the archive
  top level could be mistaken for separate addons (rare with packaged releases).
- Not a mod — nothing runs inside WoW. Restart/`/reload` the client to load
  newly-installed addons.
```
