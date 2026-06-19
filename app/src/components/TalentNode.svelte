<script lang="ts">
  import type { Placed } from "../lib/layout";
  import { NODE } from "../lib/layout";
  import type { BuildController } from "../lib/build.svelte";
  import type { NodeStatus } from "../lib/validate";

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
  const title = $derived(buildTitle());
  function buildTitle(): string {
    const base = node.entries
      .map((e) => `${e.name}${e.ranks > 1 ? ` (${e.ranks} ranks)` : ""}`)
      .join("\n— or —\n");
    if (nodeStatus?.reason === "gate") {
      return `${base}\n\n🔒 Requires ${node.req} points spent in this tree`;
    }
    if (nodeStatus?.reason === "prereq") {
      return `${base}\n\n🔒 Requires its prerequisite talent`;
    }
    return base + (node.req ? `\n\nRequires ${node.req} points spent` : "");
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
  {title}
  role="button"
  tabindex="-1"
  oncontextmenu={onRight}
  onclick={(e) => !isChoice && onLeft(e)}
  onkeydown={onKey}
>
  <!-- Icon slug lands in Stage A; placeholder swatch for now. -->
  <div class="icon"></div>
  {#if isChoice}
    <!-- Two halves; clicking one picks that choiceIndex (swaps, never stacks). -->
    <button
      class="half left"
      class:picked={selected && chosen === 0}
      title={node.entries[0]?.name}
      onclick={(e) => onLeft(e, 0)}
      oncontextmenu={onRight}
      aria-label={node.entries[0]?.name}
    ></button>
    <button
      class="half right"
      class:picked={selected && chosen === 1}
      title={node.entries[1]?.name}
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
     nodes read as split. Placeholder gradient until Stage A supplies icons. */
  .icon {
    width: 100%;
    height: 100%;
    border-radius: inherit;
    background: radial-gradient(circle at 50% 38%, #3a3f4b, #181a20);
  }
  .node.choice .icon {
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
