// Pure, framework-free talent-tree validation. No Svelte imports — this module
// is the correctness core (gates, prereqs, choice exclusivity, budget, cascade
// prune) and is unit-tested directly (validate.test.ts).
import type { TalentNode } from "./types";

// One selected node's state. `rank` is points poured in (choice = 1); `choice`
// is which of a CHOICE node's two entries is picked (0/1, ignored otherwise).
export interface NodeState {
  rank: number;
  choice: number;
}

export type Build = Map<number, NodeState>;

export type LockReason = "gate" | "prereq" | "budget";

export interface NodeStatus {
  selected: boolean;
  rank: number;
  maxRank: number;
  maxed: boolean;
  available: boolean; // a point can legally be added right now
  reason?: LockReason; // why a non-maxed node can't take a point
}

export interface TreeStatus {
  spent: number;
  budget: number;
  perNode: Map<number, NodeStatus>;
}

// Max points a node can hold. CHOICE entries are ranks:1, so this is 1 for them.
export function maxRank(node: TalentNode): number {
  return Math.max(...node.entries.map((e) => e.ranks));
}

// Build an id→node lookup once per tree; the validation helpers key off it.
export function indexNodes(nodes: TalentNode[]): Map<number, TalentNode> {
  return new Map(nodes.map((n) => [n.id, n]));
}

// Total points spent in a tree = sum of rank over its selected nodes.
export function pointsSpent(nodes: TalentNode[], build: Build): number {
  let total = 0;
  for (const node of nodes) total += build.get(node.id)?.rank ?? 0;
  return total;
}

// A parent "satisfies" a prereq edge only when fully ranked (rank === its max).
// This is the Dragonflight+ rule and is deliberately isolated — it's the single
// assumption to re-confirm against a real export string in milestone 4.
export function isParentSatisfied(parent: TalentNode, build: Build): boolean {
  const rank = build.get(parent.id)?.rank ?? 0;
  return rank > 0 && rank === maxRank(parent);
}

// OR semantics: a node unlocks if ANY listed prereq is fully ranked. No prereqs
// (or only prereqs whose nodes the data pipeline dropped) = no edge constraint.
export function isPrereqMet(
  node: TalentNode,
  byId: Map<number, TalentNode>,
  build: Build,
): boolean {
  if (!node.prereq || node.prereq.length === 0) return true;
  const known = node.prereq
    .map((pid) => byId.get(pid))
    .filter((p): p is TalentNode => p != null);
  if (known.length === 0) return true;
  return known.some((p) => isParentSatisfied(p, build));
}

// Gate: locked until at least `req` points are spent in the same tree.
export function isGateMet(node: TalentNode, spent: number): boolean {
  return spent >= node.req;
}

// Can one more point go into this node right now?
export function canAdd(
  node: TalentNode,
  byId: Map<number, TalentNode>,
  build: Build,
  spent: number,
  budget: number,
): boolean {
  const rank = build.get(node.id)?.rank ?? 0;
  if (rank >= maxRank(node)) return false; // already full
  if (spent >= budget) return false; // tree budget exhausted
  if (!isGateMet(node, spent)) return false;
  if (!isPrereqMet(node, byId, build)) return false;
  return true;
}

// Per-tree view consumed by the UI: spent/budget plus a status for every node.
export function computeTreeStatus(
  nodes: TalentNode[],
  build: Build,
  budget: number,
): TreeStatus {
  const byId = indexNodes(nodes);
  const spent = pointsSpent(nodes, build);
  const perNode = new Map<number, NodeStatus>();
  for (const node of nodes) {
    const rank = build.get(node.id)?.rank ?? 0;
    const mr = maxRank(node);
    const selected = rank > 0;
    const maxed = selected && rank >= mr;
    const available = canAdd(node, byId, build, spent, budget);
    let reason: LockReason | undefined;
    if (!available && !maxed) {
      if (!isGateMet(node, spent)) reason = "gate";
      else if (!isPrereqMet(node, byId, build)) reason = "prereq";
      else if (spent >= budget) reason = "budget";
    }
    perNode.set(node.id, { selected, rank, maxRank: mr, maxed, available, reason });
  }
  return { spent, budget, perNode };
}

// Fixpoint prune: after any removal, repeatedly unselect every selected node
// that now fails its gate or prereq until nothing changes — refunding the whole
// transitively-orphaned downstream chain. Mutates `build` in place. Trees are
// ≤~45 nodes so the repeated full sweep is free.
export function prune(
  nodes: TalentNode[],
  byId: Map<number, TalentNode>,
  build: Build,
): void {
  let changed = true;
  while (changed) {
    changed = false;
    const spent = pointsSpent(nodes, build);
    for (const node of nodes) {
      const rank = build.get(node.id)?.rank ?? 0;
      if (rank <= 0) continue;
      if (!isGateMet(node, spent) || !isPrereqMet(node, byId, build)) {
        build.delete(node.id);
        changed = true;
      }
    }
  }
}
