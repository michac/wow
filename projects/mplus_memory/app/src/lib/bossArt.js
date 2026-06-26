/**
 * bossArt.js — the boss-portrait resolver, extracted from DungeonFrame so the
 * Guide deck and the Drill/Test frame share one source of truth.
 *
 * Maps an `artKey` (`<dungeonSlug>__<bossSlug>`) to its bundled webp URL, keyed
 * by filename stem. Vite hashes the asset, so there's no path coupling — the
 * stem is the contract. Both `content.json` (via build-content.mjs) and
 * `adventure-guide.json` (via advguide.py) emit the same `<dungeon>__<boss>`
 * convention, and `bossart.py` writes the files with it.
 */
const artUrls = import.meta.glob("../assets/bosses/*.webp", {
  eager: true,
  query: "?url",
  import: "default",
});

const artByKey = Object.fromEntries(
  Object.entries(artUrls).map(([path, url]) => [
    path.split("/").pop().replace(/\.webp$/, ""),
    url,
  ]),
);

/** @param {string|null|undefined} key → bundled webp URL, or null when missing. */
export const bossArt = (key) => (key ? artByKey[key] || null : null);
