"""Shared helpers: repo paths, .env loading, OAuth client-credentials cache."""

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]  # repo root (wow/)
RAW = ROOT / "raw"

load_dotenv(ROOT / ".env")

_TOKEN_CACHE = RAW / ".tokens.json"


def env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        sys.exit(f"error: {name} is not set — copy .env.example to {ROOT / '.env'} and fill it in")
    return value


def get_oauth_token(name: str, token_url: str, client_id: str, client_secret: str) -> str:
    """Client-credentials token, cached in raw/.tokens.json until expiry."""
    cache = {}
    if _TOKEN_CACHE.exists():
        cache = json.loads(_TOKEN_CACHE.read_text())
    entry = cache.get(name)
    if entry and entry["expires_at"] > time.time() + 60:
        return entry["access_token"]

    resp = requests.post(
        token_url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    cache[name] = {
        "access_token": data["access_token"],
        "expires_at": time.time() + data.get("expires_in", 3600),
    }
    _TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
    _TOKEN_CACHE.write_text(json.dumps(cache))
    return cache[name]["access_token"]


def save_raw(subdir: str, filename: str, content: str) -> Path:
    out = RAW / subdir / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out
