<script>
  /**
   * A WoW-style cast bar: the fill sweeps left→right behind the spell name over
   * `duration` ms while `running`. Fires `ontimeout` once the cast completes
   * (the player ran out of time to classify). Remount per card via {#key}.
   * @type {{ spell: string, duration?: number, running?: boolean, ontimeout?: () => void }}
   */
  let { spell, duration = 7000, running = true, ontimeout } = $props();

  let progress = $state(0); // 0..1
  let remaining = $derived(Math.max(0, (duration * (1 - progress)) / 1000));

  $effect(() => {
    if (!running) return; // frozen (e.g. after an answer)
    let start;
    let fired = false;
    let raf = requestAnimationFrame(function tick(t) {
      if (start === undefined) start = t;
      progress = Math.min(1, (t - start) / duration);
      if (progress < 1) raf = requestAnimationFrame(tick);
      else if (!fired) {
        fired = true;
        ontimeout?.();
      }
    });
    return () => cancelAnimationFrame(raf);
  });
</script>

<p class="text-xs uppercase tracking-wider text-ink-faint">casting</p>
<div class="relative mt-1 h-14 overflow-hidden rounded-lg border border-[var(--tier)]/40 bg-surface">
  <div class="castbar-fill" style="width: {8 + progress * 92}%">
    <div class="castbar-shimmer"></div>
  </div>
  <div class="relative flex h-full items-center justify-between px-4">
    <span class="display text-xl font-bold text-ink drop-shadow">{spell}</span>
    <span class="font-mono text-xs text-ink-soft">{remaining.toFixed(1)}s</span>
  </div>
</div>
