// Reactive build controller. One stable instance lives for the app's lifetime
// (created in App, shared via setContext/getContext) so components read the
// current build without prop-drilling. All the *rules* live in validate.ts;
// this layer is just reactive state + mutations that re-prune after every edit.
import { SvelteMap } from "svelte/reactivity";
import type { SpecData, TalentNode, TreeKind } from "./types";
import {
  type Build,
  type NodeState,
  type TreeStatus,
  canAdd,
  computeTreeStatus,
  indexNodes,
  maxRank,
  pointsSpent,
  prune,
} from "./validate";

export type Budgets = { class: number; spec: number; hero: number };

// Resolved tree context for a node: its sibling list, id lookup, and budget.
interface TreeCtx {
  nodes: TalentNode[];
  byId: Map<number, TalentNode>;
  budget: number;
}

export class BuildController {
  // SvelteMap so in-place mutations trigger reactivity in templates.
  build = new SvelteMap<number, NodeState>();
  spec = $state<SpecData | null>(null);
  heroName = $state<string | null>(null);
  budgets = $state<Budgets>({ class: 31, spec: 30, hero: 11 });

  // Rebuilt on each load(); not reactive (only changes when spec changes, which
  // already drives reactivity through `spec`).
  private classCtx: TreeCtx | null = null;
  private specCtx: TreeCtx | null = null;
  private heroCtx: Record<string, TreeCtx> = {};
  private nodeIndex = new Map<number, TreeCtx>();

  // Reset for a freshly fetched spec while keeping this controller (and the
  // context handle) stable across spec switches.
  load(spec: SpecData, budgets: Budgets, heroName: string | null): void {
    this.spec = spec;
    this.budgets = budgets;
    this.heroName = heroName;
    this.build.clear();

    this.nodeIndex = new Map();
    const mk = (nodes: TalentNode[], budget: number): TreeCtx => {
      const ctx: TreeCtx = { nodes, byId: indexNodes(nodes), budget };
      for (const n of nodes) this.nodeIndex.set(n.id, ctx);
      return ctx;
    };
    this.classCtx = mk(spec.trees.class.nodes, budgets.class);
    this.specCtx = mk(spec.trees.spec.nodes, budgets.spec);
    this.heroCtx = {};
    for (const [name, sub] of Object.entries(spec.trees.hero)) {
      this.heroCtx[name] = mk(sub.nodes, budgets.hero);
    }
  }

  private isChoice(node: TalentNode): boolean {
    return node.type === "CHOICE";
  }

  // --- Mutations (each re-prunes its tree; recompute is reactive) ---

  addRank(node: TalentNode): void {
    const ctx = this.nodeIndex.get(node.id);
    if (!ctx) return;
    if (this.isChoice(node)) {
      this.pickChoice(node, 0);
      return;
    }
    const spent = pointsSpent(ctx.nodes, this.build);
    if (!canAdd(node, ctx.byId, this.build, spent, ctx.budget)) return;
    const st = this.build.get(node.id);
    this.build.set(node.id, { rank: (st?.rank ?? 0) + 1, choice: st?.choice ?? 0 });
    prune(ctx.nodes, ctx.byId, this.build);
  }

  maxRank(node: TalentNode): void {
    const ctx = this.nodeIndex.get(node.id);
    if (!ctx) return;
    if (this.isChoice(node)) {
      this.pickChoice(node, this.build.get(node.id)?.choice ?? 0);
      return;
    }
    const target = maxRank(node);
    // Add one rank at a time so each step honours gate/prereq/budget.
    for (;;) {
      const cur = this.build.get(node.id)?.rank ?? 0;
      if (cur >= target) break;
      const spent = pointsSpent(ctx.nodes, this.build);
      if (!canAdd(node, ctx.byId, this.build, spent, ctx.budget)) break;
      this.build.set(node.id, { rank: cur + 1, choice: 0 });
    }
    prune(ctx.nodes, ctx.byId, this.build);
  }

  removeRank(node: TalentNode): void {
    const ctx = this.nodeIndex.get(node.id);
    if (!ctx) return;
    const st = this.build.get(node.id);
    if (!st || st.rank <= 0) return;
    if (st.rank <= 1) this.build.delete(node.id);
    else this.build.set(node.id, { rank: st.rank - 1, choice: st.choice });
    prune(ctx.nodes, ctx.byId, this.build);
  }

  clearNode(node: TalentNode): void {
    const ctx = this.nodeIndex.get(node.id);
    if (!ctx) return;
    if (!this.build.has(node.id)) return;
    this.build.delete(node.id);
    prune(ctx.nodes, ctx.byId, this.build);
  }

  // Pick (or swap to) one half of a CHOICE node — never stacks both.
  pickChoice(node: TalentNode, choiceIndex: number): void {
    const ctx = this.nodeIndex.get(node.id);
    if (!ctx) return;
    const st = this.build.get(node.id);
    if (st) {
      // Already selected — swapping halves doesn't change the point count.
      if (st.choice !== choiceIndex) {
        this.build.set(node.id, { rank: st.rank, choice: choiceIndex });
      }
      return;
    }
    const spent = pointsSpent(ctx.nodes, this.build);
    if (!canAdd(node, ctx.byId, this.build, spent, ctx.budget)) return;
    this.build.set(node.id, { rank: 1, choice: choiceIndex });
    prune(ctx.nodes, ctx.byId, this.build);
  }

  clearAll(): void {
    this.build.clear();
  }

  // Switch the active hero tree, refunding the deselected subtree so only one
  // hero tree ever counts toward the build.
  setHero(name: string): void {
    if (this.heroName === name) return;
    this.heroName = name;
    for (const [hname, ctx] of Object.entries(this.heroCtx)) {
      if (hname === name) continue;
      for (const n of ctx.nodes) this.build.delete(n.id);
    }
  }

  private ctxFor(kind: TreeKind): TreeCtx | null {
    if (kind === "class") return this.classCtx;
    if (kind === "spec") return this.specCtx;
    return this.heroName ? (this.heroCtx[this.heroName] ?? null) : null;
  }

  // Reactive per-tree status for templates (reads `build`).
  treeStatus(kind: TreeKind): TreeStatus {
    const ctx = this.ctxFor(kind);
    if (!ctx) return { spent: 0, budget: this.budgets[kind], perNode: new Map() };
    return computeTreeStatus(ctx.nodes, this.build, ctx.budget);
  }

  // Total points across class + spec + the active hero subtree (header HUD).
  get totalSpent(): number {
    let total = 0;
    if (this.classCtx) total += pointsSpent(this.classCtx.nodes, this.build);
    if (this.specCtx) total += pointsSpent(this.specCtx.nodes, this.build);
    const hero = this.heroName ? this.heroCtx[this.heroName] : null;
    if (hero) total += pointsSpent(hero.nodes, this.build);
    return total;
  }

  get totalBudget(): number {
    return this.budgets.class + this.budgets.spec + this.budgets.hero;
  }
}
