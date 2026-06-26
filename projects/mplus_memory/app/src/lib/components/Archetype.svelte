<script>
  import { archetypes } from "../content.js";
  import ModeNav from "./ModeNav.svelte";

  // The "alphabet": 21 recurring mechanics. Letter chips drive home that this is
  // a small vocabulary you learn to automaticity, then every ability is "that's a…".
  const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let open = $state(null);
</script>

<div class="phone tier-job" style="--dgn: var(--color-dgn-mt)">
  <div class="screen">
    <div class="appbar">
      <span class="font-mono text-xs uppercase tracking-[0.2em] text-ink-faint">Alphabet</span>
      <span class="font-mono text-xs text-ink-faint">{archetypes.length} mechanics</span>
    </div>

    <div class="px-5 pb-2 pt-1">
      <p class="text-sm leading-relaxed text-ink-soft">
        Learn these to automaticity. Then every boss and trash ability is just
        <span class="text-ink">“that’s a frontal”</span> — eight dungeons collapse into a tiny set.
      </p>
    </div>

    <div class="scroll flex-1 px-4 pb-4">
      <div class="flex flex-col gap-2">
        {#each archetypes as a, i (a.slug)}
          {@const isOpen = open === a.slug}
          <button
            class="rounded-xl border border-line bg-surface px-3.5 py-3 text-left transition-colors hover:border-line/80"
            onclick={() => (open = isOpen ? null : a.slug)}
          >
            <div class="flex items-start gap-3">
              <span
                class="display mt-0.5 grid size-7 shrink-0 place-items-center rounded-md bg-surface-2 text-sm font-bold text-ink-soft"
              >
                {LETTERS[i] ?? "·"}
              </span>
              <div class="min-w-0 flex-1">
                <p class="display text-[15px] font-bold leading-tight text-ink">{a.name}</p>
                <p class="mt-0.5 text-[13px] leading-snug text-ink-soft">{a.blurb}</p>

                {#if isOpen}
                  <div class="mt-2.5 flex flex-col gap-1.5 border-t border-line pt-2.5">
                    <p class="text-[13px] leading-snug text-ink-soft">
                      <span class="font-medium text-ink">Tell</span> · {a.tell}
                    </p>
                    <p class="text-[13px] leading-snug text-ink-soft">
                      <span class="font-medium text-ink">Do</span> · {a.response}
                    </p>
                    <p class="text-[13px] leading-snug text-ink-soft">
                      <span class="font-medium text-ink">Stakes</span> · {a.consequence}
                    </p>
                    <p class="text-[12px] leading-snug text-ink-faint">{a.role}</p>
                  </div>
                {/if}
              </div>
            </div>
          </button>
        {/each}
      </div>
    </div>

    <ModeNav mode="archetypes" />
  </div>
</div>
