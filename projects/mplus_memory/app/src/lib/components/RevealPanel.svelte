<script>
  import TierBadge from "./TierBadge.svelte";
  import { humanizeSlug } from "../ui.js";
  /**
   * The rich reveal: Do (the action) → What's happening (mechanic detail) →
   * The mechanic (archetype glossary, teaching the alphabet on the back).
   * @type {{ card: any, archetype: any }}
   */
  let { card, archetype } = $props();
  let r = $derived(card.reveal);
</script>

<!-- spell + classification -->
<p class="display text-xl font-bold text-ink">{card.cue.spell}</p>
<div class="mt-2 flex flex-wrap items-center gap-2">
  <span class="rounded-md bg-[var(--tier)]/15 px-2.5 py-1 text-sm font-semibold text-[var(--tier)]">
    {humanizeSlug(card.answer)}
  </span>
  <TierBadge tier={r.tier} />
  {#if r.role && r.role !== "all"}
    <span class="rounded-full border border-line px-2 py-0.5 text-[11px] text-ink-faint">{r.role}</span>
  {/if}
</div>

<!-- DO: the primary action (this is the response the drill teaches) -->
<div class="mt-4 rounded-xl border border-[var(--tier)]/30 bg-[var(--tier)]/8 p-3.5">
  <p class="text-[11px] font-semibold uppercase tracking-wider text-[var(--tier)]">Do</p>
  <p class="mt-1 text-[15px] leading-relaxed text-ink">{r.response}</p>
</div>

<!-- WHAT'S HAPPENING: mechanic detail (omitted when the source had none) -->
{#if r.whatItDoes}
  <div class="mt-3">
    <p class="text-[11px] font-semibold uppercase tracking-wider text-ink-faint">What's happening</p>
    <p class="mt-1 text-sm leading-relaxed text-ink-soft">{r.whatItDoes}</p>
  </div>
{/if}

<!-- THE MECHANIC: the archetype glossary entry — the alphabet, taught on reveal -->
{#if archetype}
  <div class="mt-3 rounded-lg border border-line bg-surface/60 p-3">
    <p class="text-[11px] font-semibold uppercase tracking-wider text-ink-faint">
      The mechanic — {archetype.name}
    </p>
    <p class="mt-1 text-sm leading-relaxed text-ink-soft">
      <span class="font-medium text-ink">tell</span> · {archetype.tell}
    </p>
    <p class="mt-1.5 text-sm leading-relaxed text-ink-soft">
      <span class="font-medium text-ink">response</span> · {archetype.response}
    </p>
  </div>
{/if}

{#if r.lowConfidence}
  <p class="mt-3 text-[11px] leading-relaxed text-ink-faint">
    ⚠ single-sourced — re-verify against a second source before drilling hard.
  </p>
{/if}
