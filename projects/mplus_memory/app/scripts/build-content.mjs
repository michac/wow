#!/usr/bin/env bun
/**
 * build-content.mjs — KB markdown → src/content.json
 *
 * Parses the curated knowledge base into the trainer's content layer:
 *   - knowledge/systems/mechanic-archetypes.md  → archetypes[] (the 21-slug alphabet)
 *   - knowledge/endgame/mythic-plus/<dungeon>.md → dungeons[] (route, bosses, trash)
 *   - one card per boss/trash ability row        → cards[]   (the locked card shape)
 *
 * Then asserts coverage: every card's answer archetype must be one of the 21
 * canonical slugs, or the build fails. Prints a coverage report.
 *
 * Run from the app dir:  bun run scripts/build-content.mjs
 */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, "../../../.."); // app/ -> mplus_memory -> projects -> repo
const KB = resolve(REPO, "knowledge");
const OUT = resolve(__dirname, "../src/content.json");

// ── design knobs (curated, not derived) ─────────────────────────────────────
// One hue per dungeon, rotated around the wheel so the eight read as distinct.
// Stored on each dungeon and applied inline as the `--dgn` knob in the UI.
const DUNGEON_HUE = {
  "magisters-terrace": "oklch(0.70 0.16 320)", // arcane magenta
  "maisara-caverns": "oklch(0.72 0.13 175)", // teal cavern
  "nexus-point-xenas": "oklch(0.70 0.15 275)", // indigo nexus
  "windrunner-spire": "oklch(0.74 0.14 150)", // emerald
  "algethar-academy": "oklch(0.78 0.13 85)", // bronze
  "seat-of-the-triumvirate": "oklch(0.64 0.17 300)", // void purple
  "skyreach": "oklch(0.80 0.11 215)", // sky cyan
  "pit-of-saron": "oklch(0.83 0.06 250)", // frost steel
};

// Dungeon files to ingest (excludes season-1-overview.md).
const DUNGEON_SLUGS = Object.keys(DUNGEON_HUE);

const TIER_BY_EMOJI = { "🔴": "wipe", "🟠": "death", "🔵": "job", "⚪": "flavor" };

// ── small text helpers ──────────────────────────────────────────────────────

/** Strip inline markdown to plain text: bold/italic/code/links → their text. */
function stripMd(s) {
  return s
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1") // [text](url) -> text
    .replace(/\*\*([^*]+)\*\*/g, "$1") // **bold** -> bold
    .replace(/\*([^*]+)\*/g, "$1") // *italic* -> italic
    .replace(/`([^`]+)`/g, "$1") // `code` -> code
    .replace(/_([^_]+)_/g, "$1") // _em_ -> em
    .trim();
}

/** Slugify a display string into a stable id component. */
function slugify(s) {
  return stripMd(s)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/** First tier emoji found in a cell → canonical tier slug. */
function tierFromCell(cell) {
  for (const [emoji, tier] of Object.entries(TIER_BY_EMOJI)) {
    if (cell.includes(emoji)) return tier;
  }
  return "flavor"; // safest default; no untiered rows exist in the corpus
}

/** A trash row is single-sourced if it carries a "(… only)" inline flag. */
function isSingleSourced(cell) {
  return /\([^)]*only\)/i.test(cell);
}

/** Split a markdown table row "| a | b | c |" into trimmed cells. */
function splitRow(line) {
  const t = line.trim().replace(/^\|/, "").replace(/\|$/, "");
  return t.split("|").map((c) => c.trim());
}

function isTableRow(line) {
  return line.trim().startsWith("|");
}

function isSeparatorRow(line) {
  return /^\s*\|?[\s:|-]+\|?\s*$/.test(line) && line.includes("-");
}

// ── front matter ────────────────────────────────────────────────────────────

function parseFrontMatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/);
  const fm = { body: text };
  if (!m) return fm;
  fm.body = text.slice(m[0].length);
  for (const line of m[1].split("\n")) {
    const kv = line.match(/^(\w[\w-]*):\s*(.*)$/);
    if (kv) fm[kv[1]] = kv[2].trim();
  }
  return fm;
}

// ── archetypes ──────────────────────────────────────────────────────────────

/**
 * Parse mechanic-archetypes.md. Each archetype is a `## \`slug\`` block followed
 * by a "**Name** — desc" line and a set of "- **Field:** value" bullets.
 */
function parseArchetypes(md) {
  const { body } = parseFrontMatter(md);
  const archetypes = [];
  // Split on "## `slug`" headings.
  const blocks = body.split(/^## `([a-z0-9-]+)`\s*$/m);
  // blocks[0] is the preamble; then [slug, content, slug, content, ...]
  for (let i = 1; i < blocks.length; i += 2) {
    const slug = blocks[i];
    const content = blocks[i + 1];
    const nameLine = content.match(/^\s*\*\*(.+?)\*\*\s*[—-]\s*(.+?)\s*$/m);
    const field = (label) => {
      const re = new RegExp(`^- \\*\\*${label}:?\\*\\*\\s*(.+?)\\s*$`, "m");
      const m = content.match(re);
      return m ? stripMd(m[1]) : "";
    };
    archetypes.push({
      slug,
      name: nameLine ? stripMd(nameLine[1]) : slug,
      blurb: nameLine ? stripMd(nameLine[2]) : "",
      tell: field("Tell"),
      response: field("Response"),
      consequence: field("Consequence"),
      role: field("Role"),
      examples: field("Examples"),
      diagramIdea: field("Diagram idea"),
    });
  }
  return archetypes;
}

// ── dungeon parsing ─────────────────────────────────────────────────────────

/**
 * Boss display name only. Encounter ids live in a `<!-- enc:NNN -->` marker
 * (stripped at the h3 capture). Defensively also drops a legacy trailing id
 * paren — "Degentrius (2662)", "Crawth (journal 2495)", "L'ura (enc 1982)" —
 * so a stray provenance id can never reach a card again.
 */
function cleanBossName(heading) {
  return stripMd(
    heading
      .replace(/<!--.*?-->/g, "")
      .replace(/\s*\((?:[a-z][\w-]*\s+)?\d+\)\s*$/i, "")
      .trim(),
  );
}

function parseRoute(lines) {
  const route = [];
  for (const raw of lines) {
    const m = raw.match(/^\s*(\d+)\.\s+(.*)$/);
    if (!m) continue;
    const text = stripMd(m[2]);
    const bold = m[2].match(/\*\*(.+?)\*\*/);
    route.push({
      step: Number(m[1]),
      title: bold ? stripMd(bold[1]) : text.split(/[.—]/)[0].trim(),
      text,
    });
  }
  return route;
}

/**
 * Walk a dungeon file line-by-line, tracking the current ## section and the
 * current ### heading, harvesting boss tables, trash tables, and the route.
 */
function parseDungeon(slug, md) {
  const { body, ...fm } = parseFrontMatter(md);
  const name = (fm.title || slug).split("—")[0].split(" - ")[0].trim();
  const lowFile = (fm.confidence || "").toLowerCase() === "low";

  const lines = body.split("\n");
  const dungeon = {
    slug,
    name,
    hue: DUNGEON_HUE[slug],
    patch: fm.patch || "",
    confidence: fm.confidence || "",
    route: [],
    bosses: [],
    trash: [],
  };

  let section = null; // current ## heading text
  let heading = null; // current ### heading text
  let routeLines = [];
  let bossesByName = new Map();

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    const h2 = line.match(/^##\s+(.+?)\s*$/);
    if (h2 && !line.startsWith("###")) {
      section = h2[1].trim();
      heading = null;
      continue;
    }
    const h3 = line.match(/^###\s+(.+?)\s*$/);
    if (h3) {
      // Drop the `<!-- enc:NNN -->` provenance marker so it never reaches a
      // boss name or trash wing label.
      heading = h3[1].replace(/<!--.*?-->/g, "").trim();
      continue;
    }

    if (section === "Route") {
      routeLines.push(line);
      continue;
    }

    // Table detection: a header row whose first non-empty cells we recognise.
    if (isTableRow(line) && i + 1 < lines.length && isSeparatorRow(lines[i + 1])) {
      const header = splitRow(line).map((c) => c.toLowerCase());
      // consume rows
      const rows = [];
      let j = i + 2;
      for (; j < lines.length; j++) {
        if (!isTableRow(lines[j]) || isSeparatorRow(lines[j])) break;
        rows.push(splitRow(lines[j]));
      }
      i = j - 1; // advance outer loop past the table

      const col = (cells, key) => {
        const idx = header.indexOf(key);
        return idx >= 0 && idx < cells.length ? cells[idx] : "";
      };

      if (section === "Bosses" && header.includes("ability") && header.includes("do")) {
        const bossName = cleanBossName(heading || name);
        if (!bossesByName.has(bossName)) {
          const b = { name: bossName, slug: slugify(bossName), abilities: [] };
          bossesByName.set(bossName, b);
          dungeon.bosses.push(b);
        }
        const boss = bossesByName.get(bossName);
        for (const cells of rows) {
          const spell = stripMd(col(cells, "ability"));
          if (!spell) continue;
          const tierCell = col(cells, "tier");
          // Algeth'ar boss rows carry a stray 6th cell = role (header has 5 cols).
          const roleCell = cells.length > header.length ? cells[header.length] : "";
          boss.abilities.push({
            spell,
            whatItDoes: stripMd(col(cells, "what it does")),
            response: stripMd(col(cells, "do")),
            archetype: slugify(col(cells, "archetype")),
            tier: tierFromCell(tierCell),
            role: roleCell ? stripMd(roleCell) : null,
            lowConfidence: lowFile,
          });
        }
      } else if (section === "Trash" && header.includes("mob") && header.includes("ability")) {
        const seeDoKey = header.find((h) => h.includes("see")) || "see → do";
        for (const cells of rows) {
          const mob = stripMd(col(cells, "mob"));
          const spell = stripMd(col(cells, "ability"));
          if (!mob || !spell) continue;
          const seeDoRaw = col(cells, seeDoKey);
          const [see, doIt] = splitSeeDo(seeDoRaw);
          dungeon.trash.push({
            wing: heading || "Trash",
            mob,
            spell,
            whatItDoes: see,
            response: doIt,
            archetype: slugify(col(cells, "archetype")),
            tier: tierFromCell(col(cells, "tier")),
            role: stripMd(col(cells, "role")) || null,
            lowConfidence: lowFile || isSingleSourced(seeDoRaw),
          });
        }
      }
      continue;
    }
  }

  dungeon.route = parseRoute(routeLines);
  return dungeon;
}

/** Drop inline source-provenance flags; lowConfidence already captures them. */
function dropSourceFlags(s) {
  return s
    .replace(/\([^)]*only\)/gi, "")
    .replace(/\(detail differs by source\)/gi, "")
    .replace(/\s{2,}/g, " ")
    .trim();
}

/** Split a trash "See → Do" cell into [what-you-see, what-you-do]. */
function splitSeeDo(cell) {
  const clean = dropSourceFlags(stripMd(cell));
  const idx = clean.indexOf("→");
  if (idx === -1) return ["", clean];
  return [clean.slice(0, idx).trim(), clean.slice(idx + 1).trim()];
}

// ── deterministic per-card option set ───────────────────────────────────────

// xmur3 string hash → 32-bit seed; mulberry32 PRNG. Deterministic per id.
function seedFrom(str) {
  let h = 1779033703 ^ str.length;
  for (let i = 0; i < str.length; i++) {
    h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  return (h ^= h >>> 16) >>> 0;
}
function mulberry32(a) {
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function shuffle(arr, rnd) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** answer + 3 deterministic distractors, shuffled deterministically per id. */
function buildOptions(id, answer, allSlugs) {
  const rnd = mulberry32(seedFrom(id));
  const pool = allSlugs.filter((s) => s !== answer);
  const distractors = shuffle(pool, rnd).slice(0, 3);
  return shuffle([answer, ...distractors], rnd);
}

// ── card assembly ───────────────────────────────────────────────────────────

function buildCards(dungeons, allSlugs) {
  const cards = [];
  const seen = new Set();

  const push = (dungeon, casterKind, caster, segment, ab) => {
    let id = `${dungeon.slug}::${slugify(caster)}::${slugify(ab.spell)}`;
    if (seen.has(id)) id = `${id}::${cards.length}`;
    seen.add(id);
    cards.push({
      id,
      cue: {
        dungeon: dungeon.name,
        dungeonSlug: dungeon.slug,
        dungeonHue: dungeon.hue,
        segment,
        caster,
        casterKind,
        spell: ab.spell,
      },
      promptType: "classify",
      answer: ab.archetype,
      reveal: {
        whatItDoes: ab.whatItDoes,
        response: ab.response,
        tier: ab.tier,
        role: ab.role,
        lowConfidence: ab.lowConfidence,
      },
      options: buildOptions(id, ab.archetype, allSlugs),
    });
  };

  for (const d of dungeons) {
    for (const boss of d.bosses) {
      for (const ab of boss.abilities) push(d, "boss", boss.name, boss.name, ab);
    }
    for (const t of d.trash) {
      push(d, "trash", t.mob, t.wing, t);
    }
  }
  return cards;
}

// ── main ────────────────────────────────────────────────────────────────────

function main() {
  const archetypes = parseArchetypes(
    readFileSync(resolve(KB, "systems/mechanic-archetypes.md"), "utf8"),
  );
  const slugSet = new Set(archetypes.map((a) => a.slug));
  const allSlugs = archetypes.map((a) => a.slug);

  const dungeons = DUNGEON_SLUGS.map((slug) =>
    parseDungeon(slug, readFileSync(resolve(KB, `endgame/mythic-plus/${slug}.md`), "utf8")),
  );

  const cards = buildCards(dungeons, allSlugs);

  // ── coverage assertion (the Phase-2 guarantee) ──
  const misses = [];
  for (const c of cards) {
    if (!slugSet.has(c.answer)) misses.push({ id: c.id, answer: c.answer });
  }

  // ── report ──
  const perArchetype = {};
  for (const s of allSlugs) perArchetype[s] = 0;
  for (const c of cards) perArchetype[c.answer] = (perArchetype[c.answer] || 0) + 1;

  const bossCount = dungeons.reduce((n, d) => n + d.bosses.length, 0);
  const bossCards = cards.filter((c) => c.cue.casterKind === "boss").length;
  const trashCards = cards.filter((c) => c.cue.casterKind === "trash").length;

  console.log("\n  M+ Trainer — content build\n  " + "─".repeat(40));
  console.log(`  archetypes : ${archetypes.length}`);
  console.log(`  dungeons   : ${dungeons.length}`);
  console.log(`  bosses     : ${bossCount}`);
  console.log(`  cards      : ${cards.length}  (boss ${bossCards} · trash ${trashCards})`);
  console.log("\n  per-dungeon:");
  for (const d of dungeons) {
    const dc = cards.filter((c) => c.cue.dungeonSlug === d.slug).length;
    console.log(
      `    ${d.name.padEnd(26)} bosses ${String(d.bosses.length).padStart(2)} · trash ${String(d.trash.length).padStart(2)} · cards ${String(dc).padStart(3)} · route ${d.route.length}`,
    );
  }
  console.log("\n  per-archetype card counts:");
  for (const s of allSlugs) {
    console.log(`    ${s.padEnd(20)} ${perArchetype[s]}`);
  }

  if (misses.length) {
    console.error(`\n  ✗ COVERAGE FAILURE — ${misses.length} card(s) reference an unknown archetype:`);
    for (const m of misses) console.error(`      ${m.id}  →  "${m.answer}"`);
    console.error(`\n  Canonical slugs (${allSlugs.length}): ${allSlugs.join(", ")}\n`);
    process.exit(1);
  }

  const out = {
    meta: {
      generated: "build-content.mjs",
      patch: dungeons[0]?.patch || "",
      archetypeCount: archetypes.length,
      dungeonCount: dungeons.length,
      cardCount: cards.length,
    },
    archetypes,
    dungeons,
    cards,
  };
  mkdirSync(dirname(OUT), { recursive: true });
  writeFileSync(OUT, JSON.stringify(out, null, 2) + "\n");
  console.log(`\n  ✓ all ${cards.length} cards resolve to canonical archetypes`);
  console.log(`  ✓ wrote ${OUT.replace(REPO + "/", "")}\n`);
}

main();
