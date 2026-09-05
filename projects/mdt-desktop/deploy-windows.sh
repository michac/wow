#!/usr/bin/env bash
# Publish the WPF viewer to its per-user Windows install and refresh the desktop shortcut.
#
# Development happens under WSL, where the whole solution builds and every test runs — but
# `MdtDesktop.App` can only RUN on Windows, so the thing you double-click is a published copy
# that goes stale the moment the app changes. This re-cuts it. Run it after touching App/.
#
# It needs the WINDOWS dotnet (the Linux SDK cannot emit a runnable WPF app), reached through
# WSL interop. Everything else in this project is built with the Linux `dotnet`.
set -euo pipefail

WIN_DOTNET="${WIN_DOTNET:-/mnt/c/Program Files/dotnet/dotnet.exe}"
[[ -x "$WIN_DOTNET" ]] || { echo "No Windows dotnet at: $WIN_DOTNET" >&2; exit 1; }

cd "$(dirname "$0")"

# Ask Windows for its own paths rather than assuming a user name or that OneDrive owns Desktop.
localappdata=$(cmd.exe /c 'echo %LOCALAPPDATA%' 2>/dev/null | tr -d '\r')
install_dir="${localappdata}\\Programs\\MdtDesktop"

echo "publishing to ${install_dir}"
"$WIN_DOTNET" publish src/MdtDesktop.App/MdtDesktop.App.csproj -c Release -o "$install_dir" | tail -2

# The shortcut is recreated every time: it is one COM call, and it repairs a link the user
# moved, renamed or deleted rather than silently leaving them without one.
pwsh.exe -NoProfile -ExecutionPolicy Bypass -Command '
  $target = "$env:LOCALAPPDATA\Programs\MdtDesktop\MdtDesktop.App.exe"
  # Desktop is wherever the shell says it is — OneDrive redirects it on this machine.
  $desktop = [Environment]::GetFolderPath("Desktop")
  $link = (New-Object -ComObject WScript.Shell).CreateShortcut("$desktop\MDT Desktop.lnk")
  $link.TargetPath = $target
  $link.WorkingDirectory = Split-Path $target
  $link.IconLocation = "$target,0"
  $link.Description = "Second-monitor Mythic+ route viewer"
  $link.Save()
  Write-Output "shortcut : $desktop\MDT Desktop.lnk"
' 2>&1 | tail -2
