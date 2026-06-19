// Shapes of the static data emitted by scripts/build-data.ts (Stage B).

export type NodeType = "ACTIVE" | "PASSIVE" | "CHOICE";

export interface Entry {
  id: number;
  name: string;
  spell: number;
  ranks: number;
  choice: number;
  // Stage A (python, later) will add:
  icon?: string;
  desc?: string;
}

export interface TalentNode {
  id: number;
  type: NodeType;
  x: number;
  y: number;
  serial: number | null;
  req: number;
  prereq: number[];
  entries: Entry[];
}

export interface SubTree {
  nodes: TalentNode[];
}

// The export-string hero-tree selector: a type-3 node whose 2-bit choice index
// picks the active hero tree. `choices[i]` is the hero-tree name for choice i.
export interface HeroSelector {
  serial: number;
  choices: string[];
}

export interface SpecData {
  class: string;
  classId: number;
  spec: string;
  specId: number;
  treeId: number;
  patch: string;
  build: string;
  // Loadout-codec facts (Stage B passthrough of talents.py _codec_meta).
  // `serialCount` = the full class-wide serial walk length (every node slot the
  // game encodes, not just this spec's slice). `grantedSerials` = auto-granted
  // (selected-but-not-purchased) slots. `heroSelector` = the hero-tree picker.
  serialCount: number;
  grantedSerials: number[];
  heroSelector: HeroSelector | null;
  trees: {
    class: SubTree;
    spec: SubTree;
    hero: Record<string, SubTree>;
  };
}

export interface IndexSpec {
  slug: string;
  name: string;
  id: number;
  treeId: number;
  heroTrees: string[];
}

export interface IndexClass {
  slug: string;
  name: string;
  id: number;
  specs: IndexSpec[];
}

export interface IndexData {
  patch: string;
  build: string;
  fetched: string;
  pointBudget: { class: number; spec: number; hero: number };
  classes: IndexClass[];
}

export type TreeKind = "class" | "spec" | "hero";
