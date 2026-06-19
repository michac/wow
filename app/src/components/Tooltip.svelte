<script lang="ts">
  import { tooltip, reasonLine } from "../lib/tooltip.svelte";

  const data = $derived(tooltip.current);
  const node = $derived(data?.node ?? null);
  const reason = $derived(node ? reasonLine(node, data?.status) : null);

  // Offset from the cursor, flipping toward the viewport interior near an edge so
  // the box never spills off-screen. Sizes are generous estimates — exact layout
  // isn't critical, just keeping it visible.
  const OFF = 16;
  const W = 280;
  const H = 200;
  const left = $derived.by(() => {
    if (!data) return 0;
    const x = data.x + OFF;
    return x + W > window.innerWidth ? Math.max(8, data.x - OFF - W) : x;
  });
  const top = $derived.by(() => {
    if (!data) return 0;
    const y = data.y + OFF;
    return y + H > window.innerHeight ? Math.max(8, window.innerHeight - H - 8) : y;
  });
</script>

{#if data && node}
  <div class="tooltip" style="left: {left}px; top: {top}px; max-width: {W}px;">
    {#each node.entries as e, i (e.id)}
      {#if i > 0}<div class="or">— or —</div>{/if}
      <div class="entry">
        <div class="name">
          {e.name}
          {#if e.ranks > 1}<span class="ranks">({e.ranks} ranks)</span>{/if}
        </div>
        {#if e.desc}<div class="desc">{e.desc}</div>{/if}
      </div>
    {/each}
    {#if reason}
      <div class="reason" class:locked={reason.locked}>
        {#if reason.locked}🔒 {/if}{reason.text}
      </div>
    {/if}
  </div>
{/if}

<style>
  .tooltip {
    position: fixed;
    z-index: 100;
    pointer-events: none;
    background: #0d0f14f2;
    border: 1px solid #c8a14a;
    border-radius: 6px;
    padding: 8px 10px;
    color: #d8d8d8;
    font-size: 12px;
    line-height: 1.4;
    box-shadow: 0 4px 16px #000a;
  }
  .entry + .entry {
    margin-top: 4px;
  }
  .name {
    font-weight: 600;
    color: #f0e6d2;
  }
  .ranks {
    font-weight: 400;
    color: #c8a14a;
  }
  .desc {
    margin-top: 3px;
    color: #b8bcc4;
    white-space: pre-wrap;
  }
  .or {
    margin: 5px 0;
    text-align: center;
    color: #777;
    font-size: 10px;
    letter-spacing: 0.05em;
  }
  .reason {
    margin-top: 6px;
    padding-top: 5px;
    border-top: 1px solid #2a2d36;
    color: #9aa;
  }
  .reason.locked {
    color: #e0a85a;
  }
</style>
