<script>
  import DungeonIntroSlide from "./DungeonIntroSlide.svelte";
  import BossSlide from "./BossSlide.svelte";

  /**
   * The slide runner: an intro slide + one slide per boss, advanced by tap,
   * left/right swipe, or arrow keys. Read-only presentation — no timer, no
   * grading. Shows a progress label and a dot strip.
   * @type {{ dungeon: any, onback: () => void }}
   */
  let { dungeon, onback } = $props();

  // Slides: [intro, boss0, boss1, ...]. `i` is the active index.
  let slides = $derived([{ kind: "intro" }, ...dungeon.bosses.map((b) => ({ kind: "boss", boss: b }))]);
  let i = $state(0);

  // Reset to the intro whenever the dungeon changes.
  $effect(() => {
    dungeon.slug;
    i = 0;
  });

  const last = $derived(slides.length - 1);
  const next = () => { if (i < last) i += 1; };
  const prev = () => { if (i > 0) i -= 1; };

  function onkeydown(e) {
    if (e.key === "ArrowRight") next();
    else if (e.key === "ArrowLeft") prev();
    else if (e.key === "Escape") onback();
  }

  // Pointer-based horizontal swipe. Track the down-x; on up, a fast/long
  // horizontal drag flips the slide. Vertical drags fall through to scroll.
  let downX = null;
  let downY = null;
  function onpointerdown(e) {
    downX = e.clientX;
    downY = e.clientY;
  }
  function onpointerup(e) {
    if (downX === null) return;
    const dx = e.clientX - downX;
    const dy = e.clientY - downY;
    downX = downY = null;
    if (Math.abs(dx) < 45 || Math.abs(dx) < Math.abs(dy)) return; // not a horizontal swipe
    if (dx < 0) next();
    else prev();
  }

  // Boss-slide progress reads "Boss n / N"; the intro reads "Overview".
  let label = $derived(i === 0 ? "Overview" : `Boss ${i} / ${dungeon.bosses.length}`);
</script>

<svelte:window {onkeydown} />

<div class="appbar">
  <button class="text-sm text-ink-faint active:text-ink" onclick={onback} aria-label="Back to dungeons">
    ‹ Dungeons
  </button>
  <span class="font-mono text-xs text-ink-faint">{label}</span>
</div>

<!-- dot strip -->
<div class="flex items-center justify-center gap-1.5 pb-1 pt-0.5">
  {#each slides as _, s}
    <button
      class="h-1.5 rounded-full transition-all {s === i
        ? 'w-4 bg-[var(--dgn)]'
        : 'w-1.5 bg-line'}"
      onclick={() => (i = s)}
      aria-label={s === 0 ? "Overview" : `Boss ${s}`}
    ></button>
  {/each}
</div>

<!-- the slide surface: swipe + tap-right-half-to-advance -->
<div
  class="relative flex-1 overflow-hidden"
  {onpointerdown}
  {onpointerup}
>
  {#key i}
    <div class="absolute inset-0">
      {#if slides[i].kind === "intro"}
        <DungeonIntroSlide {dungeon} />
      {:else}
        <BossSlide boss={slides[i].boss} {dungeon} />
      {/if}
    </div>
  {/key}
</div>

<!-- prev / next controls -->
<div class="flex items-center justify-between gap-3 px-5 py-3">
  <button
    class="rounded-xl border border-line bg-surface-2 px-5 py-2.5 text-sm text-ink disabled:opacity-30"
    onclick={prev}
    disabled={i === 0}
  >
    ‹ Prev
  </button>
  <button
    class="flex-1 rounded-xl border border-line bg-[var(--dgn)]/15 px-5 py-2.5 text-sm font-medium text-ink active:bg-[var(--dgn)]/25 disabled:opacity-30"
    onclick={next}
    disabled={i === last}
  >
    {i === 0 ? "Start" : "Next"} ›
  </button>
</div>
