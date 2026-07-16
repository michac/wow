<script lang="ts">
  import { onMount, setContext } from "svelte";
  import type { IndexData, SpecData, TreeKind } from "./lib/types";
  import { BuildController } from "./lib/build.svelte";
  import { decodeLoadout, encodeLoadout, peekHeader } from "./lib/codec";
  import Tree from "./components/Tree.svelte";
  import ShareBox from "./components/ShareBox.svelte";
  import Tooltip from "./components/Tooltip.svelte";

  const BASE = import.meta.env.BASE_URL;

  // One stable controller for the app's lifetime; components read it via context.
  const controller = new BuildController();
  setContext("build", controller);

  let index = $state<IndexData | null>(null);
  let spec = $state<SpecData | null>(null);
  let classSlug = $state("mage");
  let specSlug = $state("arcane");
  let heroName = $state<string | null>(null);
  let activeTab = $state<TreeKind>("class");
  let error = $state<string | null>(null);

  // Node count for the currently selected tree of each kind (shown on tabs).
  function tabCount(kind: TreeKind): number {
    if (!spec) return 0;
    if (kind === "hero") return heroName ? (spec.trees.hero[heroName]?.nodes.length ?? 0) : 0;
    return spec.trees[kind].nodes.length;
  }

  const currentClass = $derived(
    index?.classes.find((c) => c.slug === classSlug) ?? null,
  );

  async function loadSpec(cls: string, spc: string) {
    spec = null;
    error = null;
    try {
      const res = await fetch(`${BASE}data/${cls}/${spc}.json`);
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      spec = await res.json();
      heroName = Object.keys(spec!.trees.hero)[0] ?? null;
      const budgets = index?.pointBudget ?? { class: 34, spec: 34, hero: 13 };
      controller.load(spec!, budgets, heroName);
    } catch (e) {
      error = `Failed to load ${cls}/${spc}: ${e}`;
    }
  }

  // --- URL hash share: #<class>/<spec>/<loadout-code> ---

  function parseHash(): { cls?: string; spc?: string; code?: string } {
    const [cls, spc, code] = location.hash.replace(/^#/, "").split("/");
    return { cls, spc, code };
  }

  // Find a class/spec slug pair for a loadout's specId (for pasted strings).
  function routeForSpecId(specId: number): { cls: string; spc: string } | null {
    for (const c of index?.classes ?? []) {
      const s = c.specs.find((sp) => sp.id === specId);
      if (s) return { cls: c.slug, spc: s.slug };
    }
    return null;
  }

  function codecError(e: unknown): string {
    return e instanceof Error ? e.message : String(e);
  }

  // Decode a code against the currently-loaded spec and apply it to the build.
  function applyCode(code: string): string | null {
    if (!spec) return "No spec loaded.";
    try {
      const decoded = decodeLoadout(code, spec);
      controller.applyBuild(decoded.build, decoded.heroName);
      heroName = controller.heroName;
      return null;
    } catch (e) {
      return codecError(e);
    }
  }

  // Route a pasted/linked code to the right spec, then apply it (ShareBox + hash).
  async function importCode(raw: string): Promise<string | null> {
    const code = raw.trim();
    if (!code) return "Paste a loadout string first.";
    let specId: number;
    try {
      specId = peekHeader(code).specId;
    } catch (e) {
      return codecError(e);
    }
    const route = routeForSpecId(specId);
    if (!route) return `No known spec matches this string (spec ${specId}).`;
    if (route.cls !== classSlug || route.spc !== specSlug) {
      classSlug = route.cls;
      specSlug = route.spc;
      await loadSpec(route.cls, route.spc);
    }
    return applyCode(code);
  }

  // Current build as a loadout code, recomputed reactively (encode reads the
  // SvelteMap + heroName). Null while no spec is loaded.
  const currentCode = $derived(
    spec ? encodeLoadout(spec, controller.build, { heroName: controller.heroName }) : null,
  );

  // Debounce-write the hash on build changes. replaceState (no history spam);
  // the equality guard makes the load→apply→encode→write cycle a no-op, so there
  // is no feedback loop (we only read the hash on mount, never on hashchange).
  let hashTimer: ReturnType<typeof setTimeout> | undefined;
  $effect(() => {
    const code = currentCode;
    if (!code) return;
    clearTimeout(hashTimer);
    const next = `#${classSlug}/${specSlug}/${code}`;
    hashTimer = setTimeout(() => {
      if (location.hash !== next) history.replaceState(null, "", next);
    }, 250);
  });

  onMount(async () => {
    try {
      const res = await fetch(`${BASE}data/index.json`);
      index = await res.json();
    } catch (e) {
      error = `Failed to load index: ${e}`;
      return;
    }

    // Route by the hash if it names a known class/spec; then decode the code.
    const { cls, spc, code } = parseHash();
    const known = index?.classes
      .find((c) => c.slug === cls)
      ?.specs.find((s) => s.slug === spc);
    if (cls && spc && known) {
      classSlug = cls;
      specSlug = spc;
    }
    await loadSpec(classSlug, specSlug);
    if (code) {
      const err = applyCode(code);
      if (err) error = `Could not load build from URL: ${err}`;
    }
  });

  // When the class changes, snap the spec to that class's first spec.
  function onClassChange(slug: string) {
    classSlug = slug;
    const first = index?.classes.find((c) => c.slug === slug)?.specs[0];
    if (first) {
      specSlug = first.slug;
      loadSpec(slug, first.slug);
    }
  }

  function onSpecChange(slug: string) {
    specSlug = slug;
    loadSpec(classSlug, slug);
  }
</script>

<header>
  <h1>Midnight Talent Calculator</h1>
  {#if index}
    <span class="badge" title="Data generated for this build"
      >patch {index.patch} · build {index.build}</span
    >
  {/if}
  {#if spec}
    <span class="hud">{controller.totalSpent}/{controller.totalBudget} pts</span>
    <button class="reset" onclick={() => controller.clearAll()}>Reset</button>
  {/if}
</header>

{#if error}
  <p class="error">{error}</p>
{/if}

{#if index && currentClass}
  <div class="controls">
    <label>
      Class
      <select
        value={classSlug}
        onchange={(e) => onClassChange(e.currentTarget.value)}
      >
        {#each index.classes as c}
          <option value={c.slug}>{c.name}</option>
        {/each}
      </select>
    </label>
    <label>
      Spec
      <select
        value={specSlug}
        onchange={(e) => onSpecChange(e.currentTarget.value)}
      >
        {#each currentClass.specs as s}
          <option value={s.slug}>{s.name}</option>
        {/each}
      </select>
    </label>
  </div>
{/if}

{#if spec}
  <ShareBox {controller} {spec} onImport={importCode} />
{/if}

{#if spec}
  <nav class="tabs">
    {#each ["class", "spec", "hero"] as const as kind}
      <button class:active={activeTab === kind} onclick={() => (activeTab = kind)}>
        {kind === "hero" ? "Hero" : kind === "spec" ? "Spec" : "Class"}
        <span class="tab-count">{tabCount(kind)}</span>
      </button>
    {/each}
  </nav>

  {#if activeTab === "hero" && Object.keys(spec.trees.hero).length > 1}
    <div class="hero-toggle">
      {#each Object.keys(spec.trees.hero) as h}
        <button
          class:active={h === heroName}
          onclick={() => {
            heroName = h;
            controller.setHero(h);
          }}
        >
          {h}
        </button>
      {/each}
    </div>
  {/if}

  <main>
    {#if activeTab === "class"}
      <Tree title="Class" kind="class" tree={spec.trees.class} />
    {:else if activeTab === "spec"}
      <Tree title="Spec" kind="spec" tree={spec.trees.spec} />
    {:else if heroName && spec.trees.hero[heroName]}
      <Tree title="Hero · {heroName}" kind="hero" tree={spec.trees.hero[heroName]} />
    {/if}
  </main>
{:else if !error}
  <p class="loading">Loading…</p>
{/if}

<Tooltip />
