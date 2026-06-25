<script>
  import { humanizeSlug } from "../ui.js";
  /**
   * The classify-the-archetype multiple choice. Before an answer every option is
   * neutral; after, every accepted slug (primary + also-valid) is colored correct
   * and a wrong pick is colored wrong. A multi-tag card has more than one right
   * answer, so several options can light green.
   * @type {{ options: string[], answer: string, alsoAccept?: string[], selected: string|null, onpick: (slug:string)=>void }}
   */
  let { options, answer, alsoAccept = [], selected, onpick } = $props();
  let answered = $derived(selected !== null);
  let accepted = $derived(new Set([answer, ...(alsoAccept ?? [])]));

  function classFor(slug) {
    if (!answered) return "border-line bg-surface-2 text-ink-soft active:scale-[0.98]";
    if (accepted.has(slug)) return "border-correct/50 bg-correct/12 text-correct";
    if (slug === selected) return "border-wrong/50 bg-wrong/12 text-wrong";
    return "border-line bg-surface-2 text-ink-faint opacity-60";
  }
</script>

<div class="mt-3 grid grid-cols-2 gap-2.5 pb-4">
  {#each options as slug (slug)}
    <button
      class="rounded-xl border px-3 py-3.5 text-sm transition-colors {classFor(slug)}"
      disabled={answered}
      onclick={() => onpick(slug)}
    >
      {humanizeSlug(slug)}
    </button>
  {/each}
</div>
