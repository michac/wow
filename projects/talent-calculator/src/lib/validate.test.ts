import { describe, expect, test } from "bun:test";
import type { TalentNode, NodeType } from "./types";
import {
  type Build,
  canAdd,
  computeTreeStatus,
  indexNodes,
  isParentSatisfied,
  isPrereqMet,
  maxRank,
  pointsSpent,
  prune,
} from "./validate";

// Minimal synthetic node factory — only the fields validation reads.
function n(
  id: number,
  opts: {
    ranks?: number;
    req?: number;
    prereq?: number[];
    type?: NodeType;
    choice?: boolean;
  } = {},
): TalentNode {
  const ranks = opts.ranks ?? 1;
  const entries = opts.choice
    ? [
        { id: id * 10, name: `${id}a`, spell: 0, ranks: 1, choice: 0 },
        { id: id * 10 + 1, name: `${id}b`, spell: 0, ranks: 1, choice: 1 },
      ]
    : [{ id: id * 10, name: `${id}`, spell: 0, ranks, choice: 0 }];
  return {
    id,
    type: opts.type ?? (opts.choice ? "CHOICE" : "PASSIVE"),
    x: 0,
    y: 0,
    serial: null,
    req: opts.req ?? 0,
    prereq: opts.prereq ?? [],
    entries,
  };
}

const build = (...pairs: [number, number, number?][]): Build =>
  new Map(pairs.map(([id, rank, choice]) => [id, { rank, choice: choice ?? 0 }]));

describe("gate", () => {
  const gated = n(2, { req: 8 });

  test("locked below the threshold, unlocked at it", () => {
    const byId = indexNodes([gated]);
    expect(canAdd(gated, byId, new Map(), 7, 31)).toBe(false); // 7 < 8
    expect(canAdd(gated, byId, new Map(), 8, 31)).toBe(true); // exactly 8
    expect(canAdd(gated, byId, new Map(), 20, 31)).toBe(true);
  });

  test("status reports the gate reason", () => {
    const status = computeTreeStatus([gated], new Map(), 31);
    expect(status.perNode.get(2)?.available).toBe(false);
    expect(status.perNode.get(2)?.reason).toBe("gate");
  });
});

describe("prereq (OR, fully-ranked)", () => {
  const a = n(1, { ranks: 2 });
  const b = n(2, { ranks: 1 });
  const c = n(3, { prereq: [1, 2] }); // unlocks when A OR B is full
  const nodes = [a, b, c];
  const byId = indexNodes(nodes);

  test("partial parent does not satisfy", () => {
    expect(isParentSatisfied(a, build([1, 1]))).toBe(false); // 1/2
    expect(isPrereqMet(c, byId, build([1, 1]))).toBe(false);
  });

  test("any one fully-ranked parent unlocks", () => {
    expect(isParentSatisfied(a, build([1, 2]))).toBe(true); // 2/2
    expect(isPrereqMet(c, byId, build([1, 2]))).toBe(true);
    expect(isPrereqMet(c, byId, build([2, 1]))).toBe(true); // via B instead
  });

  test("no prereq = always met", () => {
    expect(isPrereqMet(a, byId, new Map())).toBe(true);
  });
});

describe("choice node", () => {
  const choice = n(1, { choice: true });
  const byId = indexNodes([choice]);

  test("counts as one point and maxRank 1", () => {
    expect(maxRank(choice)).toBe(1);
    expect(pointsSpent([choice], build([1, 1, 0]))).toBe(1);
  });

  test("a picked choice is fully ranked (satisfies prereqs) and can't stack", () => {
    expect(isParentSatisfied(choice, build([1, 1, 1]))).toBe(true);
    // rank already at max → no further point can be added (swap, not stack)
    expect(canAdd(choice, byId, build([1, 1, 0]), 1, 31)).toBe(false);
  });
});

describe("budget", () => {
  const node = n(1);
  const byId = indexNodes([node]);

  test("rejected when the tree is at cap", () => {
    expect(canAdd(node, byId, new Map(), 31, 31)).toBe(false);
    const status = computeTreeStatus([node], new Map(), 0);
    expect(status.perNode.get(1)?.reason).toBe("budget");
  });
});

describe("cascade prune", () => {
  test("removing a root refunds the whole prereq chain transitively", () => {
    const r = n(1);
    const g = n(2, { prereq: [1] });
    const d = n(3, { prereq: [2] });
    const nodes = [r, g, d];
    const byId = indexNodes(nodes);
    const b = build([1, 1], [2, 1], [3, 1]); // legal chain R→G→D

    b.delete(1); // remove the root point
    prune(nodes, byId, b);
    expect(b.has(2)).toBe(false); // G refunded (parent gone)
    expect(b.has(3)).toBe(false); // D refunded transitively
  });

  test("un-filling a multi-rank parent refunds its dependents", () => {
    const r = n(1, { ranks: 2 });
    const g = n(2, { prereq: [1] });
    const nodes = [r, g];
    const byId = indexNodes(nodes);
    const b = build([1, 2], [2, 1]); // R is 2/2 → G legal

    b.set(1, { rank: 1, choice: 0 }); // drop R to 1/2 (no longer full)
    prune(nodes, byId, b);
    expect(b.get(1)?.rank).toBe(1); // R itself stays
    expect(b.has(2)).toBe(false); // G refunded — parent not fully ranked
  });

  test("dropping below a gate threshold refunds the gated node", () => {
    const a = n(1);
    const c = n(3);
    const g = n(4, { req: 3 }); // needs 3 points in tree
    const nodes = [a, c, g];
    const byId = indexNodes(nodes);
    // A + C + G = 3 points total → gate satisfied (G counts itself)
    const b = build([1, 1], [3, 1], [4, 1]);
    prune(nodes, byId, b);
    expect(b.has(4)).toBe(true);

    b.delete(1); // now C + G = 2 < 3
    prune(nodes, byId, b);
    expect(b.has(4)).toBe(false); // gated node refunded
  });
});
