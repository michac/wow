<script>
  import { dungeons } from "../content.js";
  import {
    store,
    setRole,
    setScope,
    setTierFloor,
    toggleDungeon,
    resetProgress,
  } from "../store.svelte.js";
  /** @type {{ onclose: () => void }} */
  let { onclose } = $props();

  const roles = [
    { id: "all", label: "All" },
    { id: "dps", label: "DPS" },
    { id: "healer", label: "Healer" },
    { id: "tank", label: "Tank" },
  ];

  const scopes = [
    { id: "both", label: "Both" },
    { id: "boss", label: "Bosses" },
    { id: "trash", label: "Trash" },
  ];

  // Priority floor: keep the chosen tier and everything above it in consequence.
  // Ordered high→low stakes; "all" lifts the floor entirely. Emoji match the
  // app's tier color spine (🔴 wipe → ⚪ flavor).
  const floors = [
    { id: "all", label: "All", hint: "every tier" },
    { id: "job", label: "Job+", hint: "🔵 job + above" },
    { id: "death", label: "Death+", hint: "🟠 death + 🔴 wipe" },
    { id: "wipe", label: "Wipe", hint: "🔴 group wipes only" },
  ];
</script>

<div class="absolute inset-0 z-20 flex flex-col bg-bg/95 backdrop-blur">
  <div class="appbar">
    <span class="font-mono text-xs uppercase tracking-[0.2em] text-ink-faint">Settings</span>
    <button class="text-sm text-ink-soft hover:text-ink" onclick={onclose}>done ✕</button>
  </div>

  <div class="scroll flex-1 px-5 pt-2">
    <p class="text-[11px] font-semibold uppercase tracking-wider text-ink-faint">Role</p>
    <div class="mt-2 grid grid-cols-4 gap-2">
      {#each roles as r (r.id)}
        <button
          class="rounded-lg border py-2 text-xs font-medium transition-colors {store.settings.role ===
          r.id
            ? 'border-ink/50 bg-surface-2 text-ink'
            : 'border-line bg-surface text-ink-faint'}"
          onclick={() => setRole(r.id)}
        >
          {r.label}
        </button>
      {/each}
    </div>
    <p class="mt-2 text-[11px] leading-relaxed text-ink-faint">
      You're DPS — leave it on DPS to drill only your job, or widen to All.
    </p>

    <p class="mt-5 text-[11px] font-semibold uppercase tracking-wider text-ink-faint">Scope</p>
    <div class="mt-2 grid grid-cols-3 gap-2">
      {#each scopes as s (s.id)}
        <button
          class="rounded-lg border py-2 text-xs font-medium transition-colors {store.settings.scope ===
          s.id
            ? 'border-ink/50 bg-surface-2 text-ink'
            : 'border-line bg-surface text-ink-faint'}"
          onclick={() => setScope(s.id)}
        >
          {s.label}
        </button>
      {/each}
    </div>
    <p class="mt-2 text-[11px] leading-relaxed text-ink-faint">
      Drill boss kits and trash together, or grind one in isolation when prepping a key.
    </p>

    <p class="mt-5 text-[11px] font-semibold uppercase tracking-wider text-ink-faint">Priority</p>
    <div class="mt-2 grid grid-cols-4 gap-2">
      {#each floors as f (f.id)}
        <button
          class="rounded-lg border py-2 text-xs font-medium transition-colors {store.settings
            .tierFloor === f.id
            ? 'border-ink/50 bg-surface-2 text-ink'
            : 'border-line bg-surface text-ink-faint'}"
          onclick={() => setTierFloor(f.id)}
        >
          {f.label}
        </button>
      {/each}
    </div>
    <p class="mt-2 text-[11px] leading-relaxed text-ink-faint">
      Raise the floor to drill only higher-stakes mechanics — {floors.find(
        (f) => f.id === store.settings.tierFloor,
      )?.hint}.
    </p>

    <p class="mt-5 text-[11px] font-semibold uppercase tracking-wider text-ink-faint">Dungeons</p>
    <div class="mt-2 flex flex-col gap-1.5 pb-6">
      {#each dungeons as d (d.slug)}
        {@const on = store.settings.enabledDungeons.includes(d.slug)}
        <button
          class="flex items-center justify-between rounded-lg border px-3 py-2.5 text-left text-sm transition-colors {on
            ? 'border-line bg-surface-2 text-ink'
            : 'border-line/50 bg-surface text-ink-faint'}"
          style="--dgn: {d.hue}"
          onclick={() => toggleDungeon(d.slug)}
        >
          <span class="flex items-center gap-2.5">
            <span class="size-2.5 rounded-full" style="background: var(--dgn); opacity: {on ? 1 : 0.3}"
            ></span>
            {d.name}
          </span>
          <span class="font-mono text-[11px] {on ? 'text-[var(--dgn)]' : 'text-ink-faint'}">
            {on ? "on" : "off"}
          </span>
        </button>
      {/each}
    </div>

    <button
      class="mb-6 w-full rounded-lg border border-wrong/40 bg-wrong/10 py-2.5 text-xs font-medium text-wrong/90"
      onclick={() => {
        if (confirm("Wipe all spaced-repetition progress?")) resetProgress();
      }}
    >
      Reset all progress
    </button>
  </div>
</div>
