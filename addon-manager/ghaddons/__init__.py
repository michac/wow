"""ghaddons — a minimal, GitHub-driven World of Warcraft addon manager.

Point it at a list of `owner/repo`s; it resolves each one's latest release
(or default-branch snapshot), unzips the addon folder(s) into the WoW
`Interface/AddOns` directory, and tracks versions so it can update/remove.

Stdlib only — no third-party dependencies.
"""

__version__ = "0.1.0"
