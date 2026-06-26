<script>
  import { cueSubtitle } from "../ui.js";
  import { bossArt } from "../bossArt.js";
  /**
   * The hero block: a boss portrait (real journal render when we have one,
   * dungeon-tinted monogram otherwise) with the dungeon banner, caster name,
   * an optional one-line hint, and an optional correct/wrong status pill once
   * the card is answered.
   * @type {{ cue: any, height?: number, status?: null|"correct"|"wrong" }}
   */
  let { cue, height = 210, status = null } = $props();

  // Trash cards have no artKey → no art (falls back to the monogram below).
  let art = $derived(bossArt(cue.artKey));

  let monogram = $derived(
    cue.caster
      .split(/\s+/)
      .slice(0, 2)
      .map((w) => w[0])
      .join("")
      .toUpperCase(),
  );
</script>

<div class="relative shrink-0 overflow-hidden" style="height: {height}px">
  {#if art}
    <!-- real boss portrait (journal render) -->
    <img
      src={art}
      alt={cue.caster}
      class="absolute inset-0 size-full object-cover"
    />
  {:else}
    <!-- placeholder "portrait": dungeon-hued field + faded monogram -->
    <div
      class="absolute inset-0"
      style="background:
        radial-gradient(120% 90% at 70% 20%, color-mix(in oklch, var(--dgn) 55%, var(--color-bg)) 0%, var(--color-bg) 70%);"
    >
      <span
        class="display absolute right-4 top-1 select-none font-bold leading-none text-ink/10"
        style="font-size: {height * 0.9}px"
      >
        {monogram}
      </span>
    </div>
  {/if}
  <div class="hero-scrim absolute inset-0"></div>

  <div class="absolute inset-x-0 bottom-0 flex items-end justify-between p-5">
    <div>
      <span
        class="inline-block rounded-md bg-[var(--dgn)] px-2 py-0.5 font-mono text-[10px] font-bold uppercase tracking-[0.18em] text-bg"
      >
        {cue.dungeon}
      </span>
      <p class="display mt-1.5 text-3xl font-bold leading-none text-ink drop-shadow-lg">
        {cue.caster}
      </p>
      <p class="mt-1 text-[11px] text-ink-soft">{cueSubtitle(cue)}</p>
      <!-- one-line peg: reveal only (gated on `status`) so it can never give
           away the cue-phase classify answer -->
      {#if status && cue.hint}
        <p class="mt-1 text-[11px] italic text-ink-soft/80 drop-shadow">{cue.hint}</p>
      {/if}
    </div>

    {#if status}
      <span
        class="mb-1 inline-flex items-center gap-1.5 rounded-full bg-bg/60 px-2.5 py-1 text-[11px] font-medium backdrop-blur {status ===
        'correct'
          ? 'text-correct'
          : 'text-wrong'}"
      >
        <span
          class="size-1.5 rounded-full {status === 'correct' ? 'bg-correct' : 'bg-wrong'}"
        ></span>
        {status}
      </span>
    {/if}
  </div>
</div>
