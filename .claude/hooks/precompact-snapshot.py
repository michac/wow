#!/usr/bin/env python3
"""PreCompact: snapshot the whole working tree onto a ref no branch points at.

⚠ WHY THIS EXISTS. On 2026-08-23 a `git checkout --` run to undo one test edit destroyed a day
and a half of uncommitted work in `render-shelf.md` — ~1100 lines of prose that existed nowhere
else. The token block survived only because a generated preview happened to embed it verbatim.
Nothing in git could bring the rest back, because uncommitted work is not in git at all.

This does not commit anything and does not touch the index, the working tree, or any branch. It
writes a commit object from a THROWAWAY index and hangs it off `refs/snapshots/<stamp>`, which is
invisible to `git log`, `git status` and every branch operation — but is a real commit, so
`git show refs/snapshots/<stamp>:<path>` gets any file back exactly as it was.

Recover with:
    git for-each-ref refs/snapshots --sort=-creatordate --format='%(refname) %(creatordate:short)'
    git show refs/snapshots/<stamp>:projects/combat-assist/specs/render-shelf.md > /tmp/recovered.md

Compaction must never fail because of this, so every path exits 0.
"""
import json
import os
import subprocess
import sys
import tempfile
import time

KEEP = 40          # snapshots to retain; older ones are pruned each run


def git(*args, **kw):
    return subprocess.run(("git",) + args, capture_output=True, text=True, **kw)


def main():
    try:
        json.load(sys.stdin)          # drain the payload; nothing here needs it yet
    except Exception:
        pass

    root = git("rev-parse", "--show-toplevel")
    if root.returncode != 0:
        return
    cwd = root.stdout.strip()

    # Nothing changed since HEAD (tracked or untracked) → no snapshot, no ref, no noise.
    if not git("status", "--porcelain", cwd=cwd).stdout.strip():
        print("PreCompact: working tree clean, no snapshot needed")
        return

    stamp = time.strftime("%Y%m%d-%H%M%S")
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, "index"))
        # -A respects .gitignore, so the gitignored addon sub-repos stay out of it.
        if git("add", "-A", cwd=cwd, env=env).returncode != 0:
            return
        tree = git("write-tree", cwd=cwd, env=env)
        if tree.returncode != 0:
            return
        commit = git("commit-tree", tree.stdout.strip(), "-p", "HEAD",
                     "-m", f"pre-compact snapshot {stamp}", cwd=cwd, env=env)
        if commit.returncode != 0:
            return
        git("update-ref", f"refs/snapshots/{stamp}", commit.stdout.strip(), cwd=cwd)

    refs = git("for-each-ref", "refs/snapshots", "--sort=-creatordate",
               "--format=%(refname)", cwd=cwd).stdout.split()
    for old in refs[KEEP:]:
        git("update-ref", "-d", old, cwd=cwd)

    files = len(git("status", "--porcelain", cwd=cwd).stdout.strip().split("\n"))
    print(f"PreCompact: snapshotted {files} changed file(s) to refs/snapshots/{stamp}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:                      # never block a compaction
        print(f"PreCompact snapshot skipped: {exc}", file=sys.stderr)
