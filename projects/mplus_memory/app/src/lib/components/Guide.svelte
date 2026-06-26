<script>
  import { guideDungeons } from "../guide.js";
  import GuideDeck from "./GuideDeck.svelte";
  import ModeNav from "./ModeNav.svelte";

  // Guide Mode entry: a grid of the 8 dungeons; tap one to open its slide deck.
  // The open dungeon is component-local $state, and `lastSlug` remembers the
  // most recent pick so reopening Guide lands you back where you were.
  let openSlug = $state(null);
  let lastSlug = $state(null);

  let open = $derived(openSlug ? guideDungeons.find((d) => d.slug === openSlug) : null);

  function pick(slug) {
    openSlug = slug;
    lastSlug = slug;
  }
  const back = () => (openSlug = null);
</script>

<div
  class="phone tier-job"
  style="--dgn: {open ? open.hue : 'var(--color-dgn-mt)'}"
>
  <div class="screen">
    {#if open}
      <GuideDeck dungeon={open} onback={back} />
    {:else}
      <div class="appbar">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-ink-faint">Guide</span>
        <span class="font-mono text-xs text-ink-faint">{guideDungeons.length} dungeons</span>
      </div>

      <div class="px-5 pb-2 pt-1">
        <p class="text-sm leading-relaxed text-ink-soft">
          Tap through a dungeon like a deck of cards — boss by boss, lore and role
          tips at a glance. <span class="text-ink">Build the gist, then go Drill.</span>
        </p>
      </div>

      <div class="scroll flex-1 px-4 pb-4 pt-2">
        <div class="grid grid-cols-2 gap-2.5">
          {#each guideDungeons as d (d.slug)}
            <button
              class="rounded-xl border bg-surface px-3.5 py-4 text-left transition-transform active:scale-[0.98] {d.slug ===
              lastSlug
                ? 'border-[var(--dgn)]'
                : 'border-line'}"
              style="--dgn: {d.hue}"
              onclick={() => pick(d.slug)}
            >
              <span
                class="inline-block rounded-md bg-[var(--dgn)] px-2 py-0.5 font-mono text-[9px] font-bold uppercase tracking-[0.15em] text-bg"
              >
                {d.bosses.length} bosses
              </span>
              <p class="display mt-2 text-[15px] font-bold leading-tight text-ink">{d.name}</p>
              {#if d.location}
                <p class="mt-1 text-[10px] text-ink-faint">{d.location}</p>
              {/if}
            </button>
          {/each}
        </div>
      </div>
    {/if}

    <ModeNav mode="guide" />
  </div>
</div>
