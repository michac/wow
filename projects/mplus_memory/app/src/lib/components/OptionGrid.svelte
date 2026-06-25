<script>
  import { humanizeSlug } from "../ui.js";
  /**
   * The classify-the-archetype multiple choice. Before an answer every option is
   * neutral; after, the chosen one and the correct one are colored.
   * @type {{ options: string[], answer: string, selected: string|null, onpick: (slug:string)=>void }}
   */
  let { options, answer, selected, onpick } = $props();
  let answered = $derived(selected !== null);

  function classFor(slug) {
    if (!answered) return "border-line bg-surface-2 text-ink-soft active:scale-[0.98]";
    if (slug === answer) return "border-correct/50 bg-correct/12 text-correct";
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
