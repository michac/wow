<script>
  import { store } from "../store.svelte.js";
  import { bossArt } from "../bossArt.js";
  import { ROLE_TIP_KEY, bracketSegments } from "../guide.js";
  import AbilityAccordion from "./AbilityAccordion.svelte";

  /**
   * The core deck slide: a boss portrait hero, name + lore, role tips (the
   * player's own role emphasised), and a non-modal "Mechanics" expander over
   * the journal ability tree. Read-only — no timer, no grading.
   * @type {{ boss: any, dungeon: any }}
   */
  let { boss, dungeon } = $props();

  let art = $derived(bossArt(boss.artKey));

  // Player's role drives the emphasised tip list; the other two sit behind a
  // toggle. Default DPS (store default). Roles with no journal tips are skipped.
  let myRole = $derived(store.settings.role ?? "dps");
  let myKey = $derived(ROLE_TIP_KEY[myRole] ?? "Damage Dealers");

  const ROLE_ORDER = ["Tanks", "Healers", "Damage Dealers"];
  let primary = $derived({ key: myKey, tips: boss.roleTips?.[myKey] ?? [] });
  let others = $derived(
    ROLE_ORDER.filter((k) => k !== myKey && boss.roleTips?.[k]?.length).map((k) => ({
      key: k,
      tips: boss.roleTips[k],
    })),
  );

  let showOthers = $state(false);
  let showMechanics = $state(false);

  // Reset the per-slide expanders whenever the boss changes (slide advances).
  $effect(() => {
    boss.slug;
    showOthers = false;
    showMechanics = false;
  });

  const ROLE_LABEL = { Tanks: "Tank", Healers: "Healer", "Damage Dealers": "DPS" };
</script>

<div class="screen-slide flex h-full flex-col">
  <!-- Portrait hero: framed from the top so the face never crops (phones are
       portrait → spend the vertical headroom). -->
  <div class="relative shrink-0 overflow-hidden" style="height: 46%">
    {#if art}
      <img
        src={art}
        alt={boss.name}
        class="absolute inset-0 size-full object-cover object-top"
      />
    {:else}
      <div
        class="absolute inset-0"
        style="background: radial-gradient(120% 90% at 70% 20%, color-mix(in oklch, var(--dgn) 55%, var(--color-bg)) 0%, var(--color-bg) 70%);"
      ></div>
    {/if}
    <div class="hero-scrim absolute inset-0"></div>

    <div class="absolute inset-x-0 bottom-0 p-5">
      <span
        class="inline-block rounded-md bg-[var(--dgn)] px-2 py-0.5 font-mono text-[10px] font-bold uppercase tracking-[0.18em] text-bg"
      >
        {dungeon.name}
      </span>
      <p class="display mt-1.5 text-3xl font-bold leading-none text-ink drop-shadow-lg">
        {boss.name}
      </p>
    </div>
  </div>

  <!-- Lore + role tips scroll under the hero -->
  <div class="scroll flex-1 px-5 pb-4 pt-3">
    <p class="text-[13px] leading-relaxed text-ink-soft">{boss.lore}</p>

    <!-- Role tips, player's role first and big -->
    <div class="mt-4">
      <p class="text-[11px] font-semibold uppercase tracking-wider text-[var(--dgn)]">
        {ROLE_LABEL[primary.key]} · your role
      </p>
      {#if primary.tips.length}
        <ul class="mt-2 flex flex-col gap-2">
          {#each primary.tips as tip}
            <li class="rounded-lg border border-line bg-surface px-3 py-2.5 text-[13px] leading-snug text-ink">
              {#each bracketSegments(tip) as seg}{#if seg.bold}<strong
                    class="font-semibold text-[var(--dgn)]">{seg.t}</strong>{:else}{seg.t}{/if}{/each}
            </li>
          {/each}
        </ul>
      {:else}
        <p class="mt-2 text-[12px] italic text-ink-faint">
          No {ROLE_LABEL[primary.key]}-specific notes for this boss.
        </p>
      {/if}

      {#if others.length}
        <button
          class="mt-3 text-[12px] font-medium text-ink-faint active:text-ink-soft"
          onclick={() => (showOthers = !showOthers)}
        >
          {showOthers ? "Hide" : "Show"} other roles ▾
        </button>
        {#if showOthers}
          <div class="mt-2 flex flex-col gap-3">
            {#each others as grp}
              <div>
                <p class="text-[11px] font-semibold uppercase tracking-wider text-ink-faint">
                  {ROLE_LABEL[grp.key]}
                </p>
                <ul class="mt-1.5 flex flex-col gap-1.5">
                  {#each grp.tips as tip}
                    <li class="rounded-lg border border-line/60 bg-surface/60 px-3 py-2 text-[12px] leading-snug text-ink-soft">
                      {#each bracketSegments(tip) as seg}{#if seg.bold}<strong
                            class="font-semibold text-ink">{seg.t}</strong>{:else}{seg.t}{/if}{/each}
                    </li>
                  {/each}
                </ul>
              </div>
            {/each}
          </div>
        {/if}
      {/if}
    </div>

    <!-- Mechanics: one tap deeper into the resolved ability tree (non-modal) -->
    {#if boss.abilities?.length}
      <div class="mt-5">
        <button
          class="flex w-full items-center justify-between rounded-lg border border-line bg-surface-2 px-3 py-2.5 text-[13px] font-medium text-ink active:bg-surface"
          onclick={() => (showMechanics = !showMechanics)}
          aria-expanded={showMechanics}
        >
          <span>Mechanics · {boss.abilities.length}</span>
          <span class="text-ink-faint transition-transform" class:rotate-180={showMechanics}>▾</span>
        </button>
        {#if showMechanics}
          <div class="mt-2">
            <AbilityAccordion abilities={boss.abilities} />
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div>
