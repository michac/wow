<script>
  import { setMode } from "../store.svelte.js";
  /** @type {{ mode: string }} */
  let { mode } = $props();

  // Phase-3 modes are live; Phase-4 modes show in the nav but are disabled.
  const items = [
    { id: "drill", icon: "◎", label: "Drill", on: true },
    { id: "archetypes", icon: "⬡", label: "Alphabet", on: true },
    { id: "route", icon: "⌁", label: "Route", on: false },
    { id: "dashboard", icon: "▦", label: "Stats", on: false },
    { id: "browse", icon: "⬚", label: "Browse", on: false },
  ];
</script>

<nav class="navbar">
  {#each items as it (it.id)}
    <button
      class="flex flex-col items-center gap-0.5 {it.on
        ? mode === it.id
          ? 'text-ink'
          : 'text-ink-faint hover:text-ink-soft'
        : 'cursor-not-allowed text-ink-faint/40'}"
      disabled={!it.on}
      title={it.on ? it.label : `${it.label} — Phase 4`}
      onclick={() => it.on && setMode(it.id)}
    >
      <span class="text-base leading-none">{it.icon}</span>
      <span>{it.label}</span>
    </button>
  {/each}
</nav>
