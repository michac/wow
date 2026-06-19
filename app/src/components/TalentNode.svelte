<script lang="ts">
  import type { Placed } from "../lib/layout";
  import { NODE } from "../lib/layout";
  import type { BuildController } from "../lib/build.svelte";
  import type { NodeStatus } from "../lib/validate";
  import { tooltip } from "../lib/tooltip.svelte";

  let {
    placed,
    controller,
    nodeStatus,
  }: {
    placed: Placed;
    controller: BuildController;
    nodeStatus: NodeStatus | undefined;
  } = $props();

  const node = $derived(placed.node);
  const isChoice = $derived(node.type === "CHOICE");

  const selected = $derived(nodeStatus?.selected ?? false);
  const maxed = $derived(nodeStatus?.maxed ?? false);
  const available = $derived(nodeStatus?.available ?? false);
  // "budget" reason isn't visually locked — the node is reachable, just unafforded.
  const locked = $derived(
    nodeStatus?.reason === "gate" || nodeStatus?.reason === "prereq",
  );

  const rank = $derived(nodeStatus?.rank ?? 0);
  const max = $derived(nodeStatus?.maxRank ?? Math.max(...node.entries.map((e) => e.ranks)));
  // Which half of a CHOICE node is picked (reactive via the SvelteMap).
  const chosen = $derived(controller.build.get(node.id)?.choice ?? null);

  const label = $derived(node.entries.map((e) => e.name).join(" / "));

  // Per-entry icon-load failures → fall back to the gradient swatch (onerror).
  let iconFailed = $state<Record<number, boolean>>({});
  function onIconError(entryId: number) {
    iconFailed = { ...iconFailed, [entryId]: true };
  }
  function showIcon(e: { id: number; icon?: string | null }): boolean {
    return !!e.icon && !iconFailed[e.id];
  }

  // --- Tooltip routing (shared app-level Tooltip, driven by hover/focus) ---
  function openTip(e: MouseEvent | FocusEvent) {
    const x = "clientX" in e ? e.clientX : placed.cx;
    const y = "clientY" in e ? e.clientY : placed.cy;
    tooltip.show(node, nodeStatus, x, y);
  }
  function moveTip(e: MouseEvent) {
    tooltip.move(e.clientX, e.clientY);
  }
  function closeTip() {
    tooltip.hide();
  }

  // --- Click routing (shared by single nodes and choice halves) ---
  function onLeft(e: MouseEvent, choiceIndex = 0) {
    if (isChoice) {
      if (e.shiftKey && selected) controller.clearNode(node);
      else controller.pickChoice(node, choiceIndex);
      return;
    }
    if (e.shiftKey) {
      if (maxed) controller.clearNode(node);
      else controller.maxRank(node);
    } else {
      controller.addRank(node);
    }
  }

  function onRight(e: MouseEvent) {
    e.preventDefault();
    if (e.shiftKey) controller.clearNode(node);
    else controller.removeRank(node);
  }

  // Keyboard parity for single nodes: Enter/Space adds, Backspace/Delete removes.
  function onKey(e: KeyboardEvent) {
    if (isChoice) return;
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      if (e.shiftKey) controller.maxRank(node);
      else controller.addRank(node);
    } else if (e.key === "Backspace" || e.key === "Delete") {
      e.preventDefault();
      controller.removeRank(node);
    }
  }
</script>

<div
  class="node {node.type.toLowerCase()}"
  class:selected
  class:maxed
  class:available
  class:locked
  style="left: {placed.cx - NODE / 2}px; top: {placed.cy - NODE / 2}px;
         width: {NODE}px; height: {NODE}px;"
  role="button"
  tabindex="-1"
  oncontextmenu={onRight}
  onclick={(e) => !isChoice && onLeft(e)}
  onkeydown={onKey}
  onmouseenter={openTip}
  onmousemove={moveTip}
  onmouseleave={closeTip}
  onfocusin={openTip}
  onfocusout={closeTip}
>
  <!-- Real icons (Blizzard media URLs) with a gradient-swatch fallback. CHOICE
       nodes show each half's icon side by side. -->
  <div class="icon">
    {#if isChoice}
      {#each node.entries as e (e.id)}
        <div class="icon-half">
          {#if showIcon(e)}
            <img src={e.icon} alt={e.name} loading="lazy" onerror={() => onIconError(e.id)} />
          {:else}
            <div class="swatch choice"></div>
          {/if}
        </div>
      {/each}
    {:else if showIcon(node.entries[0])}
      <img
        src={node.entries[0].icon}
        alt={label}
        loading="lazy"
        onerror={() => onIconError(node.entries[0].id)}
      />
    {:else}
      <div class="swatch"></div>
    {/if}
  </div>
  {#if isChoice}
    <!-- Two halves; clicking one picks that choiceIndex (swaps, never stacks). -->
    <button
      class="half left"
      class:picked={selected && chosen === 0}
      onclick={(e) => onLeft(e, 0)}
      oncontextmenu={onRight}
      aria-label={node.entries[0]?.name}
    ></button>
    <button
      class="half right"
      class:picked={selected && chosen === 1}
      onclick={(e) => onLeft(e, 1)}
      oncontextmenu={onRight}
      aria-label={node.entries[1]?.name}
    ></button>
  {/if}
  <span class="pips">{rank}/{max}</span>
  <span class="name">{label}</span>
</div>

<style>
  .node {
    position: absolute;
    box-sizing: border-box;
    border: 2px solid #5a5a5a;
    cursor: pointer;
    color: #d8d8d8;
  }
  .node:hover {
    border-color: #c8a14a;
    z-index: 2;
  }
  .node.passive {
    border-radius: 50%;
  }
  .node.active {
    border-radius: 6px;
  }
  .node.choice {
    border-radius: 6px;
  }
  /* Fill clips to the node's shape, so circles read as circles and choice
     nodes read as split. Real icons (img) with a gradient-swatch fallback. */
  .icon {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border-radius: inherit;
    overflow: hidden;
    display: flex;
  }
  .icon :global(img) {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  .icon-half {
    width: 50%;
    height: 100%;
    overflow: hidden;
  }
  .swatch {
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 50% 38%, #3a3f4b, #181a20);
  }
  .swatch.choice {
    background: linear-gradient(135deg, #3a3f4b 0 48%, #5a4a2a 52% 100%);
  }

  /* --- Build states --- */
  .node.selected {
    border-color: #c8a14a;
  }
  .node.selected .icon {
    filter: brightness(1.35) saturate(1.2);
  }
  .node.maxed {
    border-color: #4ad17a;
  }
  .node.maxed .icon {
    filter: brightness(1.3) saturate(1.2);
    box-shadow: inset 0 0 0 2px #4ad17a55;
  }
  .node.available:not(.selected) {
    cursor: pointer;
  }
  .node.locked {
    cursor: not-allowed;
  }
  .node.locked .icon {
    filter: grayscale(1) brightness(0.45);
  }
  .node.locked:hover {
    border-color: #7a3b3b;
  }

  /* Clickable halves overlaying a choice node. */
  .half {
    position: absolute;
    top: 0;
    width: 50%;
    height: 100%;
    border: none;
    background: none;
    padding: 0;
    cursor: inherit;
  }
  .half.left {
    left: 0;
  }
  .half.right {
    right: 0;
  }
  .half.picked {
    background: #c8a14a44;
    box-shadow: inset 0 0 0 1px #c8a14a;
  }

  .pips {
    position: absolute;
    bottom: -3px;
    right: -3px;
    font-size: 9px;
    line-height: 1;
    padding: 1px 3px;
    background: #000c;
    border: 1px solid #5a5a5a;
    border-radius: 4px;
    pointer-events: none;
  }
  .node.selected .pips {
    border-color: #c8a14a;
    color: #f0e6d2;
  }
  .node.maxed .pips {
    border-color: #4ad17a;
    color: #cfeede;
  }
  /* Single-line, truncated; full name (and ranks/gate) is in the hover title.
     Goes icon-first once Stage A lands and the label can shrink or drop. */
  .name {
    position: absolute;
    top: calc(100% + 3px);
    left: 50%;
    transform: translateX(-50%);
    max-width: 92px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 10px;
    line-height: 1.05;
    text-align: center;
    pointer-events: none;
    color: #aab;
    text-shadow: 0 1px 2px #000;
  }
</style>
