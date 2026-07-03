#!/usr/bin/env bash
# Launch the ghaddons GUI as a native Windows app from WSL.
#
# WSLg is disabled on this box (guiApplications=false in .wslconfig), so there's
# no Linux display server for `python3 -m ghaddons.gui`. Instead we run the Tk
# GUI under *native Windows* Python (pythonw.exe) and let it render on the
# Windows desktop. Windows Python bundles tkinter and ghaddons is stdlib-only,
# so no venv/deps are needed. Start-Process fully detaches it from this shell.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
win_script="$(wslpath -w "$here/run_gui.pyw")"
powershell.exe -NoProfile -Command "Start-Process pythonw -ArgumentList '$win_script'"
echo "Launched ghaddons GUI (native Windows pythonw): $win_script"
