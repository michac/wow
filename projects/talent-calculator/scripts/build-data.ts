/**
 * Stage B — web compaction (runs on Bun, no network).
 *
 * Reads the committed, patch-versioned talent DB the python pipeline emits
 * (knowledge/classes/<class>/<spec>/talents.json) and writes the static assets
 * the app fetches at runtime:
 *
 *   static/data/index.json          specs list + meta + point budgets
 *   static/data/<class>/<spec>.json compact per-spec graph
 *
 * Pure local transform: numeric fields are normalized from strings to ints and
 * node coordinates are offset to a 0-based per-tree box. Icons (full Blizzard
 * media URLs) and descriptions ride inline on each entry once Stage A (python
 * `talents enrich`) has populated talents.json; point budgets come from Stage A′
 * (TraitCurrencySource, resolved at the level cap).
 *
 * Run:  bun run build-data   (wired as `prebuild` in package.json)
 */
import { mkdir, writeFile, readFile, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";

const APP_DIR = join(import.meta.dir, "..");
const REPO_ROOT = join(APP_DIR, "..");
const KB_CLASSES = join(REPO_ROOT, "knowledge", "classes");
const OUT_DIR = join(APP_DIR, "static", "data");

// Fallback only when talents.json predates Stage A′ (no `budgets`), so the app
// still builds pre-enrichment. Live data carries real level-cap budgets from
// TraitCurrencySource (Midnight level 90: class 34 + spec 34 + hero 13).
const FALLBACK_BUDGET = { class: 34, spec: 34, hero: 13 };

type Budgets = { class: number; spec: number; hero: number };

type RawEntry = {
  entry_id: string;
  talent: string;
  spell_id: number;
  max_ranks: string | number;
  choice_index: number;
  // Stage A enrichment (inline, optional pre-enrichment).
  icon?: string | null;
  desc?: string;
};
type RawNode = {
  node_id: number;
  type: "ACTIVE" | "PASSIVE" | "CHOICE";
  row: number | string;
  col: number | string;
  x: number;
  y: number;
  serial_order: number | "";
  req_points: number;
  prereq_node_ids: number[];
  entries: RawEntry[];
};
type HeroSelector = { serial: number; choices: string[] };
type RawSpec = {
  class: string;
  class_id: number;
  spec: string;
  spec_id: number;
  tree_id: number;
  patch: string;
  build: string;
  source: string;
  serial_count: number;
  granted_serials: number[];
  hero_selector: HeroSelector | null;
  level_cap?: number;
  budgets?: Budgets;
  trees: {
    class: RawNode[];
    spec: RawNode[];
    hero: Record<string, RawNode[]>;
  };
};

type Node = {
  id: number;
  type: RawNode["type"];
  x: number;
  y: number;
  serial: number | null;
  req: number;
  prereq: number[];
  entries: {
    id: number;
    name: string;
    spell: number;
    ranks: number;
    choice: number;
    icon: string | null;
    desc: string;
  }[];
};

function titleCase(slug: string): string {
  return slug
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

/** Offset every node's x/y so the tree's top-left sits at (0,0). Keeps raw scale. */
function compactNodes(nodes: RawNode[]): Node[] {
  if (nodes.length === 0) return [];
  const minX = Math.min(...nodes.map((n) => n.x));
  const minY = Math.min(...nodes.map((n) => n.y));
  return nodes.map((n) => ({
    id: n.node_id,
    type: n.type,
    x: n.x - minX,
    y: n.y - minY,
    serial: n.serial_order === "" ? null : Number(n.serial_order),
    req: Number(n.req_points) || 0,
    prereq: n.prereq_node_ids ?? [],
    entries: n.entries.map((e) => ({
      id: Number(e.entry_id),
      name: e.talent,
      spell: e.spell_id,
      ranks: Number(e.max_ranks) || 1,
      choice: Number(e.choice_index) || 0,
      icon: e.icon ?? null,
      desc: e.desc ?? "",
    })),
  }));
}

async function main() {
  const glob = new Bun.Glob("*/*/talents.json");
  const specs: RawSpec[] = [];
  for await (const rel of glob.scan(KB_CLASSES)) {
    specs.push(JSON.parse(await readFile(join(KB_CLASSES, rel), "utf8")));
  }
  specs.sort((a, b) =>
    a.class.localeCompare(b.class) || a.spec.localeCompare(b.spec),
  );
  if (specs.length === 0) {
    throw new Error(`no talents.json found under ${KB_CLASSES}`);
  }

  // fresh output dir
  if (existsSync(OUT_DIR)) await rm(OUT_DIR, { recursive: true });
  await mkdir(OUT_DIR, { recursive: true });

  // meta: patch/build are shared across specs; fetched from the fetch manifest if present.
  const { patch, build } = specs[0];

  // Point budgets are global (shared currencies) and identical across specs, so
  // the first spec's Stage A′ block is authoritative. Fall back if absent.
  const pointBudget: Budgets = specs[0].budgets ?? FALLBACK_BUDGET;
  if (!specs[0].budgets) {
    console.warn(
      `no budgets in talents.json — using fallback ${JSON.stringify(FALLBACK_BUDGET)}; run \`talents build\` after Stage A′`,
    );
  }
  let fetched = "";
  const manifestPath = join(REPO_ROOT, "raw", "talents-manifest.json");
  if (existsSync(manifestPath)) {
    fetched = JSON.parse(await readFile(manifestPath, "utf8")).fetched ?? "";
  }

  // group specs by class for index.json
  const byClass = new Map<string, RawSpec[]>();
  for (const s of specs) {
    (byClass.get(s.class) ?? byClass.set(s.class, []).get(s.class)!).push(s);
  }
  const classes = [...byClass.entries()].map(([slug, members]) => ({
    slug,
    name: titleCase(slug),
    id: members[0].class_id,
    specs: members.map((s) => ({
      slug: s.spec,
      name: titleCase(s.spec),
      id: s.spec_id,
      treeId: s.tree_id,
      heroTrees: Object.keys(s.trees.hero),
    })),
  }));

  const index = {
    patch,
    build,
    fetched,
    pointBudget,
    classes,
  };
  await writeFile(
    join(OUT_DIR, "index.json"),
    JSON.stringify(index, null, 2) + "\n",
  );

  // per-spec compact graph
  let nodeCount = 0;
  for (const s of specs) {
    const compact = {
      class: s.class,
      classId: s.class_id,
      spec: s.spec,
      specId: s.spec_id,
      treeId: s.tree_id,
      patch: s.patch,
      build: s.build,
      // Loadout-codec facts (see tools/wowkb/talents.py _codec_meta): the full
      // class-wide serial walk length, auto-granted slots, and the hero selector.
      serialCount: s.serial_count,
      grantedSerials: s.granted_serials ?? [],
      heroSelector: s.hero_selector ?? null,
      trees: {
        class: { nodes: compactNodes(s.trees.class) },
        spec: { nodes: compactNodes(s.trees.spec) },
        hero: Object.fromEntries(
          Object.entries(s.trees.hero).map(([name, nodes]) => [
            name,
            { nodes: compactNodes(nodes) },
          ]),
        ),
      },
    };
    nodeCount +=
      compact.trees.class.nodes.length +
      compact.trees.spec.nodes.length +
      Object.values(compact.trees.hero).reduce(
        (a, t) => a + t.nodes.length,
        0,
      );
    const out = join(OUT_DIR, s.class, `${s.spec}.json`);
    await mkdir(dirname(out), { recursive: true });
    await writeFile(out, JSON.stringify(compact) + "\n");
  }

  console.log(
    `Stage B: ${specs.length} specs, ${classes.length} classes, ${nodeCount} nodes → ${OUT_DIR}`,
  );
  console.log(`patch ${patch} build ${build}${fetched ? ` fetched ${fetched}` : ""}`);
}

main();
