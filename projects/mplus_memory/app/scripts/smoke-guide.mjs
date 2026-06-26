/**
 * smoke-guide.mjs — headless mount test for Guide Mode. Boots the bundle, sets
 * the persisted mode to "guide", confirms the dungeon picker renders, opens a
 * dungeon, and walks the deck (intro → boss slide → mechanics). Dev-only.
 */
import { Window } from "happy-dom";
import { readdirSync } from "node:fs";
import { resolve } from "node:path";

const win = new Window({ url: "http://localhost/wow/" });
for (const k of [
  "window", "document", "navigator", "localStorage", "sessionStorage",
  "HTMLElement", "Element", "Node", "Text", "Comment", "DocumentFragment",
  "customElements", "getComputedStyle", "CSS", "location", "history",
  "MutationObserver", "Event", "CustomEvent", "DOMParser", "PointerEvent",
]) {
  if (win[k] !== undefined) globalThis[k] = win[k];
}
globalThis.requestAnimationFrame = (cb) => setTimeout(() => cb(performance.now()), 16);
globalThis.cancelAnimationFrame = (id) => clearTimeout(id);

// Land directly in Guide mode.
win.localStorage.setItem(
  "mplus.trainer.v1",
  JSON.stringify({ version: 1, schedule: {}, settings: { mode: "guide" }, stats: {} }),
);
win.document.body.innerHTML = `<div id="app"></div>`;

const assert = (cond, msg) => {
  if (!cond) { console.error("  ✗ " + msg); process.exit(1); }
  console.log("  ✓ " + msg);
};
const text = () => win.document.body.textContent || "";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const distAssets = resolve(import.meta.dirname, "../dist/assets");
const entry = readdirSync(distAssets).find((f) => f.endsWith(".js"));
await import(resolve(distAssets, entry));
await sleep(50);

assert(win.document.querySelector(".phone"), "phone shell mounted");
assert(/Guide/.test(text()), "Guide app bar rendered");
assert(/8 dungeons/.test(text()), "dungeon count shown");

// pick a dungeon tile (a button inside the picker grid carrying "bosses")
const tiles = [...win.document.querySelectorAll(".grid-cols-2 button")];
assert(tiles.length === 8, `8 dungeon tiles rendered (got ${tiles.length})`);
tiles.find((b) => /Skyreach/.test(b.textContent))?.click();
await sleep(40);

assert(/Overview/.test(text()), "deck opened on the overview slide");
assert(/Tap or swipe to begin/.test(text()), "intro slide rendered");

// advance to the first boss slide via the Start/Next button
const startBtn = [...win.document.querySelectorAll("button")].find((b) =>
  /Start/.test(b.textContent),
);
assert(startBtn, "Start button present on intro");
startBtn.click();
await sleep(40);
assert(/Boss 1 \//.test(text()), "advanced to boss 1");
assert(/your role/.test(text()), "role tips header rendered");

// open the Mechanics expander
const mechBtn = [...win.document.querySelectorAll("button")].find((b) =>
  /^Mechanics ·/.test(b.textContent.trim()),
);
assert(mechBtn, "Mechanics expander present");
mechBtn.click();
await sleep(30);

// back out to the dungeon grid
const backBtn = [...win.document.querySelectorAll("button")].find((b) =>
  /Dungeons/.test(b.textContent),
);
backBtn?.click();
await sleep(30);
assert(/8 dungeons/.test(text()), "returned to the dungeon picker");

console.log("\n  ✓ guide smoke test passed\n");
process.exit(0);
