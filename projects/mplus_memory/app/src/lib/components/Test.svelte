<script>
  import { store, recordReview, setMode } from "../store.svelte.js";
  import { gradeFromLatency } from "../srs.js";
  import { archetype, dungeons } from "../content.js";
  import { buildTestQueue } from "../session.js";
  import { tierClass, humanizeSlug } from "../ui.js";
  import { DURATION } from "../timing.js";

  import DungeonFrame from "./DungeonFrame.svelte";
  import CastBar from "./CastBar.svelte";
  import OptionGrid from "./OptionGrid.svelte";
  import RevealPanel from "./RevealPanel.svelte";
  import NextButton from "./NextButton.svelte";
  import ModeNav from "./ModeNav.svelte";

  // Test is a self-contained intro/assessment: a blocked, in-order pass through
  // ONE dungeon. Its dungeon choice is component-local (a $state below), kept off
  // store.settings.enabledDungeons so it never clobbers Drill's pool. Role is
  // inherited from the global setting.

  // "setup" → pick a dungeon · "run" → the one-shot pass · "report" → score card.
  let stage = $state("setup");
  let dungeonSlug = $state(null);

  // run state (mirrors Drill, minus the requeue)
  let queue = $state([]);
  let idx = $state(0);
  let phase = $state("cue"); // "cue" | "reveal"
  let selected = $state(null);
  let wasCorrect = $state(false);
  let timedOut = $state(false);
  let castProgress = $state(0);
  let elapsedMs = $state(0);

  // honest assessment ledger — one entry per card, raw correctness (no SRS leniency)
  let results = $state([]);

  let current = $derived(queue[idx] ?? null);
  let dungeon = $derived(dungeons.find((d) => d.slug === dungeonSlug) ?? null);

  function start(slug) {
    dungeonSlug = slug;
    queue = buildTestQueue({
      dungeonSlug: slug,
      filters: { role: store.settings.role },
    });
    idx = 0;
    results = [];
    resetCard();
    stage = "run";
  }

  function resetCard() {
    phase = "cue";
    selected = null;
    wasCorrect = false;
    timedOut = false;
    castProgress = 0;
    elapsedMs = 0;
  }

  function pick(slug) {
    if (phase !== "cue") return;
    elapsedMs = castProgress * DURATION;
    selected = slug;
    wasCorrect = slug === current.answer;
    phase = "reveal";
  }

  function onTimeout() {
    if (phase !== "cue") return;
    elapsedMs = DURATION; // ran out the clock → miss
    selected = ""; // no pick
    wasCorrect = false;
    timedOut = true;
    phase = "reveal";
  }

  // One shot: record the raw outcome, seed the SRS (intro framing), advance
  // permanently. No requeue on a miss — that's the whole point of a "test".
  function next() {
    results = [
      ...results,
      {
        card: current,
        outcome: timedOut ? "timeout" : wasCorrect ? "correct" : "wrong",
        pick: selected,
        elapsedMs,
      },
    ];
    recordReview(current.id, gradeFromLatency(wasCorrect, elapsedMs, DURATION), wasCorrect);
    idx += 1;
    if (idx >= queue.length) stage = "report";
    else resetCard();
  }

  // ---- report derivations ----
  let total = $derived(results.length);
  let correct = $derived(results.filter((r) => r.outcome === "correct").length);
  let misses = $derived(results.filter((r) => r.outcome !== "correct"));

  // Weakest spot: the archetype the player whiffed most. The "alphabet" framing
  // makes this more useful than a per-segment peg ("you're shaky on this letter").
  let weakest = $derived.by(() => {
    if (!misses.length) return null;
    const tally = new Map();
    for (const m of misses) {
      const slug = m.card.answer;
      tally.set(slug, (tally.get(slug) ?? 0) + 1);
    }
    let top = null;
    for (const [slug, n] of tally) if (!top || n > top.n) top = { slug, n };
    return top;
  });

  let weakestLabel = $derived(
    weakest ? (archetype(weakest.slug)?.name ?? humanizeSlug(weakest.slug)).toLowerCase() : "",
  );

  function retake() {
    stage = "setup";
    dungeonSlug = null;
  }
</script>

{#if stage === "run" && current}
  <!-- RUN: same cue→cast-bar→reveal→Next loop as Drill, one-shot -->
  <div class="phone {tierClass(current.reveal.tier)}" style="--dgn: {current.cue.dungeonHue}">
    <div class="screen">
      <div class="appbar">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-ink-faint">Test</span>
        <span class="font-mono text-xs text-ink-faint">{idx + 1} / {queue.length}</span>
      </div>
      <div class="mx-5 mb-1 h-1 rounded-full bg-surface-2">
        <div
          class="h-1 rounded-full bg-ink-faint transition-all"
          style="width: {queue.length ? (idx / queue.length) * 100 : 0}%"
        ></div>
      </div>

      <DungeonFrame
        cue={current.cue}
        height={phase === "reveal" ? 150 : 210}
        status={phase === "reveal" ? (wasCorrect ? "correct" : "wrong") : null}
      />

      {#key current.id}
        {#if phase === "cue"}
          <div class="scroll flex-1 px-5 pt-5">
            <CastBar
              spell={current.cue.spell}
              duration={DURATION}
              running={phase === "cue"}
              ontimeout={onTimeout}
              bind:progress={castProgress}
            />
            <p class="mt-6 text-sm text-ink-soft">Which mechanic is this?</p>
            <OptionGrid options={current.options} answer={current.answer} {selected} onpick={pick} />
          </div>
        {:else}
          <div class="scroll {wasCorrect ? 'fx-correct' : 'fx-wrong'} flex-1 px-5 pt-4">
            <RevealPanel card={current} archetype={archetype(current.answer)} />
            <NextButton onnext={next} {wasCorrect} {timedOut} />
          </div>
        {/if}
      {/key}

      <ModeNav mode="test" />
    </div>
  </div>
{:else}
  <!-- SETUP + REPORT share a neutral frame, tinted by the chosen dungeon -->
  <div class="phone tier-job" style="--dgn: {dungeon ? dungeon.hue : 'var(--color-dgn-mt)'}">
    <div class="screen">
      <div class="appbar">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-ink-faint">Test</span>
        <span class="font-mono text-xs text-ink-faint">role · {store.settings.role}</span>
      </div>

      {#if stage === "report"}
        <!-- REPORT: honest score card -->
        <div class="scroll flex-1 px-5 pb-4 pt-2">
          <p class="text-sm leading-relaxed text-ink-soft">
            {dungeon ? dungeon.name : ""} — one-shot pass.
          </p>

          <div class="mt-4 rounded-xl border border-line bg-surface p-4 text-center">
            <p class="display text-4xl font-bold text-ink">{correct} <span class="text-ink-faint">/ {total}</span></p>
            <p class="mt-2 text-sm text-ink-soft">
              {#if weakest}
                Shaky on {dungeon ? dungeon.name : "this dungeon"}'s {weakestLabel}s.
              {:else}
                Clean pass — no misses.
              {/if}
            </p>
          </div>

          {#if misses.length}
            <p class="mt-5 text-[11px] font-semibold uppercase tracking-wider text-ink-faint">
              Missed casts
            </p>
            <div class="mt-2 flex flex-col gap-2">
              {#each misses as m (m.card.id)}
                <div class="rounded-lg border border-line bg-surface px-3 py-2.5">
                  <p class="text-[11px] text-ink-faint">{m.card.cue.segment}</p>
                  <p class="text-sm font-medium text-ink">{m.card.cue.spell}</p>
                  <p class="mt-1 text-[13px] leading-snug text-ink-soft">
                    {#if m.outcome === "timeout"}
                      <span class="text-wrong">timed out</span>
                    {:else}
                      <span class="text-wrong">{humanizeSlug(m.pick)}</span>
                    {/if}
                    <span class="text-ink-faint"> → </span>
                    <span class="text-correct">{humanizeSlug(m.card.answer)}</span>
                  </p>
                </div>
              {/each}
            </div>
          {/if}

          <div class="mt-6 flex gap-2.5">
            <button
              class="flex-1 rounded-xl border border-line bg-surface-2 px-5 py-2.5 text-sm text-ink"
              onclick={retake}
            >
              Retake
            </button>
            <button
              class="flex-1 rounded-xl border border-line bg-surface-2 px-5 py-2.5 text-sm text-ink"
              onclick={() => setMode("drill")}
            >
              Back to Drill
            </button>
          </div>
        </div>
      {:else}
        <!-- SETUP: pick one dungeon -->
        <div class="px-5 pb-2 pt-1">
          <p class="text-sm leading-relaxed text-ink-soft">
            A single in-order pass through one dungeon — boss by boss, one shot each.
            <span class="text-ink">Build the gist, then graduate to Drill.</span>
          </p>
        </div>
        <div class="scroll flex-1 px-4 pb-4">
          <div class="grid grid-cols-2 gap-2.5">
            {#each dungeons as d (d.slug)}
              <button
                class="rounded-xl border border-line bg-surface px-3.5 py-4 text-left transition-transform active:scale-[0.98]"
                style="--dgn: {d.hue}"
                onclick={() => start(d.slug)}
              >
                <span
                  class="inline-block rounded-md bg-[var(--dgn)] px-2 py-0.5 font-mono text-[9px] font-bold uppercase tracking-[0.15em] text-bg"
                >
                  M+
                </span>
                <p class="display mt-2 text-[15px] font-bold leading-tight text-ink">{d.name}</p>
              </button>
            {/each}
          </div>
        </div>
      {/if}

      <ModeNav mode="test" />
    </div>
  </div>
{/if}
