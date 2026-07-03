"""Windows launcher for the ghaddons GUI.

Run this under *native Windows* Python (``pythonw.exe``) from WSL so the Tk
window renders on the Windows desktop. WSLg is disabled on this box
(``guiApplications=false`` in .wslconfig), so the Linux ``python3 -m
ghaddons.gui`` path has no display server — but Windows Python ships tkinter
and ghaddons is stdlib-only, so it Just Works as a native window.

Invoke by full path (works even though the source lives on the WSL fs, e.g.
``\\wsl.localhost\<distro>\...\addon-manager\run_gui.pyw``); the sys.path
bootstrap below means cwd is irrelevant.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghaddons.gui import main  # noqa: E402

if __name__ == "__main__":
    main()
