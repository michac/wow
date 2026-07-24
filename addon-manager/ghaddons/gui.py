"""Minimal Tkinter desktop UI — a CurseForge-shaped window over the same core.

Run:  python -m ghaddons.gui
Needs Tk:  sudo apt install python3-tk   (WSLg renders it on Windows 11)

Network work runs on a worker thread; results are marshalled back to the Tk
thread through a queue drained by `after()`, so the window never freezes.
"""

from __future__ import annotations

import queue
import threading

import tkinter as tk
from tkinter import messagebox, ttk

from . import manager as m
from .paths import CONFIG_PATH, MANIFEST_PATH

STATE_LABEL = {
    "up-to-date": "✓ up to date",
    "update-available": "⬆ update",
    "not-installed": "· not installed",
    "error": "⚠ error",
}


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cfg = m.Config.load(CONFIG_PATH)
        self.manifest = m.load_manifest(MANIFEST_PATH)
        self.q: queue.Queue = queue.Queue()

        root.title("ghaddons — GitHub addon manager")
        root.geometry("760x460")

        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="Add repo:").pack(side="left")
        self.entry = ttk.Entry(top, width=32)
        self.entry.pack(side="left", padx=4)
        self.entry.bind("<Return>", lambda _e: self.add_repo())
        ttk.Button(top, text="Add", command=self.add_repo).pack(side="left")
        ttk.Button(top, text="Refresh", command=self.refresh).pack(side="right")

        cols = ("repo", "installed", "latest", "state")
        self.tree = ttk.Treeview(root, columns=cols, show="headings", selectmode="extended")
        for c, w in zip(cols, (300, 140, 140, 130)):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8)

        btns = ttk.Frame(root, padding=8)
        btns.pack(fill="x")
        ttk.Button(btns, text="Install / Update", command=self.install_selected).pack(side="left")
        ttk.Button(btns, text="Update all", command=self.update_all).pack(side="left", padx=4)
        ttk.Button(btns, text="Remove", command=self.remove_selected).pack(side="left")
        ttk.Button(btns, text="Remove from list", command=self.forget_selected).pack(side="left", padx=4)

        self.status = tk.StringVar(value=f"AddOns: {self.cfg.addons_dir}")
        ttk.Label(root, textvariable=self.status, relief="sunken", anchor="w").pack(fill="x", side="bottom")

        self.reload_rows()
        self.root.after(100, self._drain)
        self.refresh()

    # -- rendering -------------------------------------------------------- #
    def reload_rows(self):
        self.tree.delete(*self.tree.get_children())
        for repo in self.cfg.repos:
            entry = self.manifest.get(repo, {})
            self.tree.insert("", "end", iid=repo,
                             values=(repo, entry.get("version", "-"), "…", ""))

    def _set(self, repo, installed=None, latest=None, state=None):
        if repo not in self.tree.get_children():
            return
        vals = list(self.tree.item(repo, "values"))
        if installed is not None:
            vals[1] = installed
        if latest is not None:
            vals[2] = latest
        if state is not None:
            vals[3] = STATE_LABEL.get(state, state)
        self.tree.item(repo, values=vals)

    def _selected(self):
        return list(self.tree.selection())

    # -- worker plumbing -------------------------------------------------- #
    def _bg(self, fn):
        threading.Thread(target=fn, daemon=True).start()

    def _drain(self):
        try:
            while True:
                fn = self.q.get_nowait()
                fn()
        except queue.Empty:
            pass
        self.root.after(100, self._drain)

    def _post(self, fn):
        self.q.put(fn)

    # -- actions ---------------------------------------------------------- #
    def add_repo(self):
        repo = self.entry.get().strip().strip("/")
        if not repo or repo in self.cfg.repos:
            return
        self.cfg.repos.append(repo)
        self.cfg.save(CONFIG_PATH)
        self.entry.delete(0, "end")
        self.reload_rows()
        self.refresh()

    def forget_selected(self):
        for repo in self._selected():
            if repo in self.cfg.repos:
                self.cfg.repos.remove(repo)
        self.cfg.save(CONFIG_PATH)
        self.reload_rows()

    def refresh(self):
        self.status.set("Checking versions…")

        def work():
            # Re-read the manifest from disk first, so a deploy done OUTSIDE this
            # GUI (`ghaddons update` / `wowkb.addon release`, which write
            # installed.json) is reflected.  Without this the GUI keeps its
            # launch-time snapshot of "installed" and shows a stale
            # update-available forever, even though the files are already deployed.
            self.manifest = m.load_manifest(MANIFEST_PATH)
            for repo in list(self.cfg.repos):
                s = m.status_for(repo, self.cfg, self.manifest)
                self._post(lambda r=repo, s=s: self._set(
                    r, installed=s.installed or "-",
                    latest=(s.latest or (s.error[:30] if s.state == "error" else "-")),
                    state=s.state))
            self._post(lambda: self.status.set(f"AddOns: {self.cfg.addons_dir}"))

        self._bg(work)

    def _install_many(self, repos):
        def work():
            for repo in repos:
                self._post(lambda r=repo: self.status.set(f"Installing {r}…"))
                try:
                    entry = m.install(repo, self.cfg, self.manifest)
                    m.save_manifest(MANIFEST_PATH, self.manifest)
                    self._post(lambda r=repo, e=entry: self._set(
                        r, installed=e["version"], latest=e["version"], state="up-to-date"))
                except Exception as e:  # noqa: BLE001
                    self._post(lambda r=repo, e=e: (
                        self._set(r, state="error"),
                        self.status.set(f"{r}: {e}")))
            self._post(lambda: self.status.set(f"AddOns: {self.cfg.addons_dir}"))

        self._bg(work)

    def install_selected(self):
        sel = self._selected()
        if sel:
            self._install_many(sel)

    def update_all(self):
        todo = [r for r in self.cfg.repos
                if str(self.tree.item(r, "values")[3]).startswith("⬆")]
        if todo:
            self._install_many(todo)
        else:
            self.status.set("Nothing to update.")

    def remove_selected(self):
        sel = self._selected()
        if not sel:
            return
        if not messagebox.askyesno("Remove", f"Delete installed files for:\n{', '.join(sel)}?"):
            return
        for repo in sel:
            m.remove(repo, self.cfg, self.manifest)
        m.save_manifest(MANIFEST_PATH, self.manifest)
        self.refresh()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
