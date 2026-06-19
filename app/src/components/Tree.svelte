<script lang="ts">
  import { getContext } from "svelte";
  import type { SubTree, TreeKind } from "../lib/types";
  import { layoutTree } from "../lib/layout";
  import type { BuildController } from "../lib/build.svelte";
  import TalentNode from "./TalentNode.svelte";

  let {
    title,
    tree,
    kind,
  }: { title: string; tree: SubTree; kind: TreeKind } = $props();

  const controller = getContext<BuildController>("build");
  const layout = $derived(layoutTree(tree));
  const status = $derived(controller.treeStatus(kind));
  const over = $derived(status.spent > status.budget);
</script>

<section class="tree">
  <h2>
    {title}
    <span class="count" class:over>{status.spent}/{status.budget}</span>
  </h2>
  <div
    class="canvas"
    style="width: {layout.width}px; height: {layout.height}px;"
  >
    <svg
      class="edges"
      width={layout.width}
      height={layout.height}
      viewBox="0 0 {layout.width} {layout.height}"
    >
      {#each layout.edges as e}
        <line
          class:active={status.perNode.get(e.from)?.maxed}
          x1={e.x1}
          y1={e.y1}
          x2={e.x2}
          y2={e.y2}
        />
      {/each}
    </svg>
    {#each layout.placed as placed (placed.node.id)}
      <TalentNode
        {placed}
        {controller}
        nodeStatus={status.perNode.get(placed.node.id)}
      />
    {/each}
  </div>
</section>

<style>
  .tree {
    display: inline-block;
    vertical-align: top;
    margin: 0 12px 32px;
  }
  h2 {
    font-size: 14px;
    font-weight: 600;
    color: #c8a14a;
    margin: 0 0 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .count {
    color: #777;
    font-weight: 400;
  }
  .count.over {
    color: #e06c6c;
  }
  .canvas {
    position: relative;
  }
  .edges {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }
  .edges line {
    stroke: #4a4f5a;
    stroke-width: 2;
  }
  .edges line.active {
    stroke: #c8a14a;
    stroke-width: 2.5;
  }
</style>
