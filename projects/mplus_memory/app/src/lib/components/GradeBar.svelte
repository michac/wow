<script>
  /** Self-grade after the reveal. @type {{ ongrade: (g:string)=>void }} */
  let { ongrade } = $props();
  const grades = [
    { g: "again", label: "Again", cls: "border-wrong/40 bg-wrong/10 text-wrong/90" },
    { g: "hard", label: "Hard", cls: "border-line bg-surface-2 text-ink-soft" },
    { g: "good", label: "Good", cls: "border-line bg-surface-2 text-ink-soft" },
    { g: "easy", label: "Easy", cls: "border-correct/40 bg-correct/10 text-correct" },
  ];
</script>

<p class="mt-5 text-center text-xs text-ink-faint">how well did you know it?</p>
<div class="mt-2 grid grid-cols-4 gap-2 pb-4">
  {#each grades as { g, label, cls } (g)}
    <button
      class="rounded-xl border py-2.5 text-xs font-medium transition-transform active:scale-95 {cls}"
      onclick={() => ongrade(g)}
    >
      {label}
    </button>
  {/each}
</div>
