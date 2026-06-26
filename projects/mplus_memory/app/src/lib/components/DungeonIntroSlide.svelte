<script>
  import { bossArt } from "../bossArt.js";

  /**
   * The deck's opening slide: dungeon name (display face), location, lore, and a
   * roster strip of boss portrait thumbnails — the "what am I about to tour".
   * @type {{ dungeon: any }}
   */
  let { dungeon } = $props();
</script>

<div class="screen-slide flex h-full flex-col px-5 pb-4 pt-6">
  <span
    class="inline-block self-start rounded-md bg-[var(--dgn)] px-2 py-0.5 font-mono text-[10px] font-bold uppercase tracking-[0.18em] text-bg"
  >
    Dungeon
  </span>
  <h1 class="display mt-2 text-4xl font-bold leading-none text-ink">{dungeon.name}</h1>
  {#if dungeon.location}
    <p class="mt-2 text-[12px] font-medium uppercase tracking-wider text-[var(--dgn)]">
      {dungeon.location}
    </p>
  {/if}

  <div class="scroll mt-4 flex-1">
    <p class="text-[13px] leading-relaxed text-ink-soft">{dungeon.lore}</p>

    <p class="mt-6 text-[11px] font-semibold uppercase tracking-wider text-ink-faint">
      {dungeon.bosses.length} bosses
    </p>
    <div class="mt-3 grid grid-cols-4 gap-2.5">
      {#each dungeon.bosses as b (b.slug)}
        {@const art = bossArt(b.artKey)}
        <div class="flex flex-col items-center gap-1">
          <div
            class="size-14 overflow-hidden rounded-full border-2 border-[var(--dgn)]/60 bg-surface"
          >
            {#if art}
              <img src={art} alt={b.name} class="size-full object-cover object-top" />
            {/if}
          </div>
          <span class="text-center text-[9px] leading-tight text-ink-faint">{b.name}</span>
        </div>
      {/each}
    </div>
  </div>

  <p class="mt-3 text-center text-[11px] text-ink-faint">Tap or swipe to begin →</p>
</div>
