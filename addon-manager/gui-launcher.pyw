"""Windowless launcher for the ghaddons GUI, for a Windows desktop shortcut.

Run under Windows `pythonw.exe` (bundled, has Tk). Self-locating: it adds its own
directory to sys.path so `import ghaddons` works no matter the launch cwd, then
hands off to the package GUI entrypoint. Lives on the WSL filesystem; Windows
reaches it via the \\wsl.localhost UNC path.

    pythonw.exe "\\wsl.localhost\<distro>\...\addon-manager\gui-launcher.pyw"
"""

import os
import runpy
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
runpy.run_module("ghaddons.gui", run_name="__main__")
