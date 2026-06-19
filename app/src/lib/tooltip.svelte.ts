// App-level hovered-node signal driving the single floating Tooltip component
// (one tooltip, not one per node). TalentNode publishes the hovered node + the
// cursor anchor; Tooltip reads it. The title/reason text helper lives here too
// so node and tooltip share one source of truth (replacing TalentNode's old
// native-title buildTitle()).
import type { TalentNode } from "./types";
import type { NodeStatus } from "./validate";

export interface TooltipData {
  node: TalentNode;
  status: NodeStatus | undefined;
  x: number; // cursor anchor, viewport coords
  y: number;
}

class TooltipState {
  current = $state<TooltipData | null>(null);

  show(node: TalentNode, status: NodeStatus | undefined, x: number, y: number): void {
    this.current = { node, status, x, y };
  }
  move(x: number, y: number): void {
    if (this.current) this.current = { ...this.current, x, y };
  }
  hide(): void {
    this.current = null;
  }
}

export const tooltip = new TooltipState();

/**
 * The gate/prereq/req line for a node, given its current status. `locked` marks
 * the reasons a node can't take a point right now (shown with a lock); a plain
 * `Requires N points spent` is informational. Returns null when there's nothing
 * to say. Shared by the tooltip (and previously TalentNode's title).
 */
export function reasonLine(
  node: TalentNode,
  status: NodeStatus | undefined,
): { text: string; locked: boolean } | null {
  if (status?.reason === "gate") {
    return { text: `Requires ${node.req} points spent in this tree`, locked: true };
  }
  if (status?.reason === "prereq") {
    return { text: "Requires its prerequisite talent", locked: true };
  }
  if (node.req) {
    return { text: `Requires ${node.req} points spent`, locked: false };
  }
  return null;
}
