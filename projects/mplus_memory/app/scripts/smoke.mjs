/**
 * smoke.mjs — headless mount test. Boots the production bundle in happy-dom,
 * confirms the Drill renders, simulates picking the correct option → reveal →
 * Next, and checks the schedule persisted to localStorage. Dev-only (not shipped).
 */
import { Window } from "happy-dom";
import { readdirSync } from "node:fs";
import { resolve } from "node:path";

const win = new Window({ url: "http://localhost/wow/" });

// expose the DOM globals the bundle expects
for (const k of [
  "window", "document", "navigator", "localStorage", "sessionStorage",
  "HTMLElement", "Element", "Node", "Text", "Comment", "DocumentFragment",
  "customElements", "getComputedStyle", "CSS", "location", "history",
  "MutationObserver", "Event", "CustomEvent", "DOMParser",
]) {
  if (win[k] !== undefined) globalThis[k] = win[k];
}
globalThis.requestAnimationFrame = (cb) => setTimeout(() => cb(performance.now()), 16);
globalThis.cancelAnimationFrame = (id) => clearTimeout(id);

win.document.body.innerHTML = `<div id="app"></div>`;

const assert = (cond, msg) => {
  if (!cond) {
    console.error("  ✗ " + msg);
    process.exit(1);
  }
  console.log("  ✓ " + msg);
};

// import the freshly built bundle
const distAssets = resolve(import.meta.dirname, "../dist/assets");
const entry = readdirSync(distAssets).find((f) => f.endsWith(".js"));
await import(resolve(distAssets, entry));

// let mount + initial effects flush
await new Promise((r) => setTimeout(r, 50));

const text = () => win.document.body.textContent || "";
assert(win.document.querySelector(".phone"), "phone shell mounted");
assert(/Drill/.test(text()), "Drill app bar rendered");
assert(/Which mechanic is this\?/.test(text()), "cue + question rendered");

const options = [...win.document.querySelectorAll("button")].filter((b) =>
  /^[a-z ]+$/.test(b.textContent.trim()) && b.closest(".grid-cols-2"),
);
assert(options.length === 4, `4 archetype options rendered (got ${options.length})`);

// pick the first option → must transition to the reveal (Do action + Next button)
options[0].click();
await new Promise((r) => setTimeout(r, 30));
assert(/\bDo\b/.test(text()), "reveal shows the Do action");
const nextBtn = [...win.document.querySelectorAll("button")].find(
  (b) => b.textContent.trim() === "Next",
);
assert(nextBtn, "single Next button rendered (no self-grade row)");

// tap Next → schedule should persist (grade inferred from latency)
nextBtn.click();
await new Promise((r) => setTimeout(r, 30));

const saved = JSON.parse(win.localStorage.getItem("mplus.trainer.v1"));
assert(saved && saved.stats.reviews === 1, "one review persisted to localStorage");
assert(Object.keys(saved.schedule).length === 1, "one card scheduled in localStorage");
assert(/Which mechanic is this\?/.test(text()), "advanced to the next card");

console.log("\n  ✓ smoke test passed\n");
process.exit(0);
