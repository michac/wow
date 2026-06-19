<script lang="ts">
  import type { SpecData } from "../lib/types";
  import type { BuildController } from "../lib/build.svelte";
  import { encodeLoadout } from "../lib/codec";

  let {
    controller,
    spec,
    onImport,
  }: {
    controller: BuildController;
    spec: SpecData | null;
    // Routes + applies a pasted code (peekHeader → loadSpec → decode → apply).
    // Resolves to an error message, or null on success.
    onImport: (code: string) => Promise<string | null>;
  } = $props();

  let pasted = $state("");
  let message = $state<{ text: string; ok: boolean } | null>(null);

  // The current build as an export string — recomputed reactively as the build
  // changes (encodeLoadout reads the SvelteMap). Empty until a spec is loaded.
  const exportCode = $derived(
    spec
      ? encodeLoadout(spec, controller.build, { heroName: controller.heroName })
      : "",
  );

  async function importPasted() {
    const err = await onImport(pasted);
    message = err
      ? { text: err, ok: false }
      : { text: "Build imported.", ok: true };
    if (!err) pasted = "";
  }

  async function copyExport() {
    try {
      await navigator.clipboard.writeText(exportCode);
      message = { text: "Export string copied to clipboard.", ok: true };
    } catch {
      message = { text: "Copy failed — select the box and copy manually.", ok: false };
    }
  }
</script>

<div class="share">
  <div class="row">
    <button class="copy" onclick={copyExport} disabled={!spec}>
      Copy export string
    </button>
    <input class="export" readonly value={exportCode} aria-label="Current build export string" />
  </div>
  <div class="row">
    <textarea
      class="paste"
      bind:value={pasted}
      placeholder="Paste a WoW talent import string here…"
      rows="2"
    ></textarea>
    <button class="import" onclick={importPasted} disabled={!pasted.trim()}>
      Import
    </button>
  </div>
  {#if message}
    <p class="msg" class:ok={message.ok} class:err={!message.ok}>{message.text}</p>
  {/if}
</div>

<style>
  .share {
    margin: 8px 0 4px;
    padding: 10px 12px;
    background: #14161c;
    border: 1px solid #2a2d36;
    border-radius: 6px;
  }
  .row {
    display: flex;
    gap: 8px;
    align-items: stretch;
    margin-bottom: 6px;
  }
  .row:last-of-type {
    margin-bottom: 0;
  }
  button {
    flex: 0 0 auto;
    background: #2a2d36;
    color: #f0e6d2;
    border: 1px solid #c8a14a;
    border-radius: 4px;
    padding: 4px 10px;
    cursor: pointer;
    font-size: 12px;
    white-space: nowrap;
  }
  button:disabled {
    opacity: 0.5;
    cursor: default;
    border-color: #5a5a5a;
  }
  .export,
  .paste {
    flex: 1 1 auto;
    background: #0d0f14;
    color: #b8bcc4;
    border: 1px solid #2a2d36;
    border-radius: 4px;
    padding: 4px 8px;
    font-family: ui-monospace, monospace;
    font-size: 11px;
    min-width: 0;
  }
  .paste {
    resize: vertical;
  }
  .msg {
    margin: 6px 0 0;
    font-size: 12px;
  }
  .msg.ok {
    color: #4ad17a;
  }
  .msg.err {
    color: #e06c6c;
  }
</style>
