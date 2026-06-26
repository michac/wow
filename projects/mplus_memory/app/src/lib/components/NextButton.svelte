<script>
  /**
   * One-tap reveal advance. A short feedback line above the button reflects the
   * outcome — correct, wrong, or timed out — since the grade is now inferred and
   * no longer asked of the player.
   * @type {{ onnext: () => void, wasCorrect: boolean, timedOut: boolean }}
   */
  let { onnext, wasCorrect, timedOut } = $props();
</script>

<p
  class="mt-5 text-center text-xs {wasCorrect ? 'text-correct' : 'text-wrong'}"
>
  {#if wasCorrect}
    ✓ Nailed it
  {:else if timedOut}
    ⏱ Ran out of time
  {:else}
    ✗ Not quite
  {/if}
</p>
<div class="mt-2 pb-4">
  <button
    class="w-full rounded-xl border border-line bg-surface-2 px-5 py-3 text-sm font-medium text-ink transition-transform active:scale-95"
    onclick={onnext}
  >
    Next
  </button>
</div>
