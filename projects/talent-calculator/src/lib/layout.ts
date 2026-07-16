// Turn a subtree's raw (already 0-based per tree) node coords into pixel
// positions, and derive prereq edges for the SVG layer.
import type { SubTree, TalentNode } from "./types";

export const SCALE = 0.17; // raw units → px (600 raw ≈ 102px spacing)
export const NODE = 44; // node box size, px
export const PAD = 28; // padding around the tree, px

export interface Placed {
  node: TalentNode;
  cx: number; // center x, px
  cy: number; // center y, px
}

export interface Edge {
  from: number; // source (prereq) node id — used to light the edge when ranked
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface Layout {
  placed: Placed[];
  edges: Edge[];
  width: number;
  height: number;
}

export function layoutTree(tree: SubTree): Layout {
  const placed: Placed[] = tree.nodes.map((node) => ({
    node,
    cx: node.x * SCALE + PAD + NODE / 2,
    cy: node.y * SCALE + PAD + NODE / 2,
  }));

  const byId = new Map<number, Placed>();
  for (const p of placed) byId.set(p.node.id, p);

  const edges: Edge[] = [];
  for (const p of placed) {
    for (const reqId of p.node.prereq) {
      const from = byId.get(reqId);
      if (!from) continue; // prereq node dropped by the pipeline — skip
      edges.push({ from: reqId, x1: from.cx, y1: from.cy, x2: p.cx, y2: p.cy });
    }
  }

  const maxX = placed.length ? Math.max(...placed.map((p) => p.cx)) : 0;
  const maxY = placed.length ? Math.max(...placed.map((p) => p.cy)) : 0;
  return {
    placed,
    edges,
    width: maxX + NODE / 2 + PAD,
    height: maxY + NODE / 2 + PAD,
  };
}
