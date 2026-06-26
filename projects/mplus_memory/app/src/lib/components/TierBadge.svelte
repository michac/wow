<script>
  import { TIER_META } from "../ui.js";
  /** @type {{ tier: string }} */
  let { tier } = $props();
  let meta = $derived(TIER_META[tier] ?? TIER_META.flavor);
</script>

<span
  class="inline-flex items-center gap-1 rounded-full border border-[var(--tier)]/40 px-2 py-0.5 text-[11px] text-[var(--tier)]"
>
  {meta.emoji}
  {meta.label}
</span>
