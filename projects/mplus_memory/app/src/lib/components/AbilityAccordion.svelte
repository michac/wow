<script>
  import { bracketSegments } from "../guide.js";
  import Self from "./AbilityAccordion.svelte";

  /**
   * One-open-at-a-time accordion over the journal ability tree. Headers are
   * ability names; expanding reveals the resolved description and, recursively,
   * any child abilities indented under their parent — exactly the journal nest.
   * @type {{ abilities: any[], depth?: number }}
   */
  let { abilities, depth = 0 } = $props();

  let open = $state(null); // index of the single open row, or null
  const toggle = (i) => (open = open === i ? null : i);
</script>

<div class="flex flex-col gap-1.5" style={depth > 0 ? "margin-left: 0.85rem" : ""}>
  <!-- key by index: the journal tree has duplicate names AND repeated/null
       spellIds (e.g. Emberdawn's two "Burning Gale" rows), so position is the
       only stable key for this static, render-once list. -->
  {#each abilities as a, i (i)}
    <div
      class="overflow-hidden rounded-lg border border-line bg-surface {depth > 0
        ? 'border-l-2 border-l-[var(--dgn)]'
        : ''}"
    >
      <button
        class="flex w-full items-center justify-between gap-2 px-3 py-2 text-left active:bg-surface-2"
        onclick={() => toggle(i)}
        aria-expanded={open === i}
      >
        <span class="text-[13px] font-medium leading-snug text-ink">{a.name}</span>
        <span class="shrink-0 text-ink-faint transition-transform" class:rotate-180={open === i}>▾</span>
      </button>

      {#if open === i}
        <div class="border-t border-line/60 px-3 py-2.5">
          {#if a.text}
            <p class="text-[13px] leading-relaxed text-ink-soft">
              {#each bracketSegments(a.text) as seg}{#if seg.bold}<strong
                    class="font-semibold text-ink">{seg.t}</strong>{:else}{seg.t}{/if}{/each}
            </p>
          {:else}
            <p class="text-[12px] italic text-ink-faint">No description.</p>
          {/if}

          {#if a.children?.length}
            <div class="mt-2.5">
              <Self abilities={a.children} depth={depth + 1} />
            </div>
          {/if}
        </div>
      {/if}
    </div>
  {/each}
</div>
