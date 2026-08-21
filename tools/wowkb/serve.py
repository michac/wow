"""Serve a directory of local HTML, rebuild it when its sources change, reload the browser.

The loop this closes: **edit the shelf → regenerate → look → tweak.** Without it, seeing a
one-token change to `specs/render-shelf.md` means a rebuild, a publish and a page load, which
is slow enough that nobody iterates and the look stays un-designed. With it, saving the doc is
the whole gesture.

Nothing here is specific to Combat Assist Plus — it serves a directory, watches paths, and runs
a command. Point it at any local HTML in this repo.

    uv run python -m wowkb.serve projects/combat-assist/previews \\
        --watch projects/combat-assist/specs \\
        --on-change "python -m wowkb.capart build --all"

Live reload is injected into **served** HTML responses only — the bytes on disk are never
touched, so the committed preview and anything published from it stay clean. `--no-reload`
turns injection off entirely.

Stdlib only, and deliberately dumb: mtime polling rather than inotify, because the watched
trees are small and a dependency-free tool is one that still runs in three years.
"""

import argparse
import os
import subprocess
import sys
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from ._common import ROOT

POLL_S = 0.5
SKIP_DIRS = {"__pycache__", "node_modules"}

# Injected before </body> (or appended). It reconnects on drop, so restarting the server or
# suspending the laptop does not leave a dead page that silently stops updating.
#
# ⚠ **It holds the stream only while the tab is VISIBLE, and that is not an optimisation.**
# An `EventSource` is a permanent HTTP connection, and browsers cap HTTP/1.1 at SIX per origin.
# A previous version connected on load and never let go, so six open preview tabs consumed every
# slot and the seventh request — including a plain page load — queued forever behind them. The
# failure mode is the worst kind: no error, no timeout, just `pending` in devtools and a server
# that answers `curl` instantly, which sends you looking at the page instead of the transport.
# Measured 2026-08-19 with two specs open across several reloads.
#
# Releasing the stream when the tab is hidden means background tabs cost nothing, so the budget
# is spent only on tabs actually being looked at. A tab reloads on becoming visible if it missed
# a rebuild while away, which is the behaviour you wanted from a background tab anyway.
RELOAD_JS = """
<script>
(function () {
  var gen = null, es = null;
  function connect() {
    if (es || document.visibilityState === "hidden") return;
    es = new EventSource("/__reload");
    es.onmessage = function (e) {
      if (gen === null) { gen = e.data; return; }
      if (e.data !== gen) location.reload();
    };
    es.onerror = function () { drop(); setTimeout(connect, 1000); };
  }
  function drop() { if (es) { es.close(); es = null; } }
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") drop(); else connect();
  });
  // `pagehide` rather than `unload`: it fires for the back/forward cache too, which `unload`
  // does not, and a bfcached page holding a stream is exactly the leak this is preventing.
  window.addEventListener("pagehide", drop);
  connect();
})();
</script>
"""


class Watcher:
    """Poll mtimes over the watched paths; run the command and bump a generation on change."""

    def __init__(self, paths: list[Path], command: str | None):
        self.paths = paths
        self.command = command
        self.generation = 0
        self._event = threading.Event()
        self._lock = threading.Lock()

    def snapshot(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for path in self.paths:
            if path.is_file():
                try:
                    out[str(path)] = path.stat().st_mtime
                except OSError:
                    pass
                continue
            for dirpath, dirnames, filenames in os.walk(path):
                dirnames[:] = [d for d in dirnames
                               if not d.startswith(".") and d not in SKIP_DIRS]
                for fn in filenames:
                    if fn.startswith("."):
                        continue
                    fp = os.path.join(dirpath, fn)
                    try:
                        out[fp] = os.stat(fp).st_mtime
                    except OSError:
                        pass
        return out

    def bump(self) -> None:
        with self._lock:
            self.generation += 1
        self._event.set()
        self._event.clear()

    def wait(self, timeout: float) -> bool:
        return self._event.wait(timeout)

    def run(self) -> None:
        """The watch thread. Daemonized, so Ctrl-C at the server is the only exit."""
        prev = self.snapshot()
        while True:
            time.sleep(POLL_S)
            cur = self.snapshot()
            if cur == prev:
                continue
            changed = sorted(set(cur) ^ set(prev)
                             | {k for k in set(cur) & set(prev) if cur[k] != prev[k]})
            prev = cur
            self.on_change(changed)

    def on_change(self, changed: list[str]) -> None:
        for path in changed[:4]:
            print(f"  changed  {_rel(Path(path))}")
        if len(changed) > 4:
            print(f"  changed  … and {len(changed) - 4} more")
        if self.command:
            proc = subprocess.run(self.command, shell=True, cwd=ROOT / "tools",
                                  capture_output=True, text=True)
            for stream in (proc.stdout, proc.stderr):
                for line in stream.splitlines():
                    print(f"  | {line}")
            status = "ok" if proc.returncode == 0 else f"FAILED (exit {proc.returncode})"
            print(f"  rebuild  {status}")
        # Bump either way. On a failed rebuild the page on disk is the last good one, and a
        # reloaded stale page next to a visible error in the terminal beats a dead tab.
        self.bump()


class Handler(SimpleHTTPRequestHandler):
    """Static files, plus `/__reload` and the injected client."""

    watcher: Watcher
    inject: bool

    # SimpleHTTPRequestHandler guesses `text/html` with NO charset, so a UTF-8 page served
    # straight off disk gets decoded as latin-1 and every `·` in it becomes `Â·`. The injected
    # path already sets the charset; without this, turning injection off would silently change
    # how the page reads, which is exactly the kind of difference a preview must not have.
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".htm": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".md": "text/plain; charset=utf-8",
        ".svg": "image/svg+xml",
    }

    def log_message(self, fmt, *args):  # quieter than the default one-line-per-asset
        if self.path != "/__reload":
            sys.stderr.write("  %s %s\n" % (self.command, self.path))

    def do_GET(self):  # noqa: N802 — BaseHTTPRequestHandler's naming
        if self.path.split("?")[0] == "/__reload":
            return self._stream()
        if self.inject and self._is_html():
            return self._send_html()
        return super().do_GET()

    # ---- live reload

    #: Backstop for the connection budget described on RELOAD_JS. The client releases its stream
    #: when hidden, but a crashed tab or a browser that never fires `pagehide` would still strand
    #: one. Streams are capped and the OLDEST evicted, so the newest tab — the one being looked
    #: at — always gets a slot. Below the browser's own limit of 6 on purpose.
    MAX_STREAMS = 4
    _streams: list = []
    _streams_lock = threading.Lock()

    def _stream(self) -> None:
        token = object()
        with Handler._streams_lock:
            Handler._streams.append(token)
            while len(Handler._streams) > Handler.MAX_STREAMS:
                Handler._streams.pop(0)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            while True:
                with Handler._streams_lock:
                    if token not in Handler._streams:
                        return          # evicted: let the client reconnect if it still cares
                self.wfile.write(f"data: {self.watcher.generation}\n\n".encode())
                self.wfile.flush()
                self.watcher.wait(15.0)  # also a keep-alive tick
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            with Handler._streams_lock:
                if token in Handler._streams:
                    Handler._streams.remove(token)

    def _is_html(self) -> bool:
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        return path.is_file() and path.suffix.lower() in {".html", ".htm"}

    def _send_html(self) -> None:
        """Serve HTML with the reload client spliced in — on the wire, never on disk."""
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        try:
            body = path.read_bytes()
        except OSError:
            return self.send_error(404, "File not found")
        script = RELOAD_JS.encode()
        lower = body.lower()
        cut = lower.rfind(b"</body>")
        body = body[:cut] + script + body[cut:] if cut != -1 else body + script
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _resolve(arg: str) -> Path:
    """Accept a path relative to the cwd or to the repo root, so any directory works."""
    p = Path(arg)
    if p.exists():
        return p.resolve()
    alt = ROOT / arg
    if alt.exists():
        return alt.resolve()
    sys.exit(f"error: no such path: {arg}")


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.serve", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("directory", help="directory to serve")
    p.add_argument("--watch", action="append", default=[], metavar="PATH",
                   help="file or directory to watch (repeatable); defaults to DIRECTORY")
    p.add_argument("--on-change", metavar="CMD",
                   help="shell command to run on change, from tools/ (e.g. a capart build)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--open", metavar="FILE", help="print a direct URL to this file in DIRECTORY")
    p.add_argument("--no-reload", action="store_true",
                   help="serve the bytes as they are — no live-reload injection")
    args = p.parse_args()
    # A long-running server's stdout is block-buffered the moment it is piped or teed, which
    # swallows the URL banner and every rebuild line until exit — the opposite of a live loop.
    sys.stdout.reconfigure(line_buffering=True)

    served = _resolve(args.directory)
    if not served.is_dir():
        sys.exit(f"error: not a directory: {args.directory}")
    watched = [_resolve(w) for w in args.watch] or [served]

    watcher = Watcher(watched, args.on_change)
    if args.on_change:
        print(f"building  {args.on_change}")
        watcher.on_change([])

    handler = partial(Handler, directory=str(served))
    Handler.watcher = watcher
    Handler.inject = not args.no_reload

    threading.Thread(target=watcher.run, daemon=True).start()

    try:
        httpd = ThreadingHTTPServer((args.host, args.port), handler)
    except OSError as exc:
        sys.exit(f"error: cannot bind {args.host}:{args.port} — {exc}")
    httpd.daemon_threads = True

    base = f"http://{args.host}:{args.port}"
    print(f"\nserving   {_rel(served)}")
    for w in watched:
        print(f"watching  {_rel(w)}")
    print(f"reload    {'injected into served HTML' if Handler.inject else 'off'}")
    print(f"\n  {base}/{args.open or ''}\n")
    print("Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
