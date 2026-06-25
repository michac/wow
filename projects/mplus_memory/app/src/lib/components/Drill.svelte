<script>
  import { untrack } from "svelte";
  import { store, recordReview } from "../store.svelte.js";
  import { gradeFromLatency } from "../srs.js";
  import { archetype } from "../content.js";
  import { buildQueue } from "../session.js";
  import { tierClass } from "../ui.js";

  import DungeonFrame from "./DungeonFrame.svelte";
  import CastBar from "./CastBar.svelte";
  import OptionGrid from "./OptionGrid.svelte";
  import RevealPanel from "./RevealPanel.svelte";
  import NextButton from "./NextButton.svelte";
  import ModeNav from "./ModeNav.svelte";
  import FilterSheet from "./FilterSheet.svelte";

  // Shared cast-bar duration: the timer the player sees and the latency grader read
  // the same number so they can't drift.
  const DURATION = 7000;

  let queue = $state([]);
  let idx = $state(0);
  let total = $state(0); // session length when built (progress denominator)
  let reviewed = $state(0);
  let phase = $state("cue"); // "cue" | "reveal"
  let selected = $state(null);
  let wasCorrect = $state(false);
  let timedOut = $state(false);
  let castProgress = $state(0); // 0..1, bound from the cast bar's RAF clock
  let elapsedMs = $state(0); // stamped on pick/timeout so next() reads a stable value
  let showFilters = $state(false);

  let current = $derived(queue[idx] ?? null);
  let done = $derived(!current);

  // Rebuild the queue when the *filters* change (role / enabled dungeons).
  // Schedule reads inside buildQueue are untracked so grading doesn't reset us.
  $effect(() => {
    store.settings.role;
    store.settings.enabledDungeons;
    untrack(rebuild);
  });

  function rebuild() {
    queue = buildQueue({
      schedule: store.schedule,
      filters: {
        role: store.settings.role,
        enabledDungeons: store.settings.enabledDungeons,
      },
    });
    idx = 0;
    total = queue.length;
    reviewed = 0;
    resetCard();
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
    elapsedMs = DURATION; // ran out the clock; wrong anyway → grade is "again"
    selected = ""; // ran out of time — counts as a miss
    wasCorrect = false;
    timedOut = true;
    phase = "reveal";
  }

  // The cast bar is a solve timer: correctness + time-to-answer imply the grade,
  // so the reveal collapses to a single Next tap.
  function next() {
    const g = gradeFromLatency(wasCorrect, elapsedMs, DURATION);
    recordReview(current.id, g, wasCorrect);
    reviewed += 1;
    // "Again" → re-show this card later in the same session.
    if (g === "again") queue = [...queue, current];
    idx += 1;
    resetCard();
  }
</script>

<div
  class="phone {current ? tierClass(current.reveal.tier) : 'tier-job'}"
  style={current ? `--dgn: ${current.cue.dungeonHue}` : ""}
>
  <div class="screen">
    <!-- app bar -->
    <div class="appbar">
      <span class="font-mono text-xs uppercase tracking-[0.2em] text-ink-faint">Drill</span>
      <div class="flex items-center gap-3 text-xs text-ink-faint">
        {#if store.stats.streakDays > 0}<span>🔥 {store.stats.streakDays}-day</span>{/if}
        <span class="font-mono">{Math.min(reviewed + (done ? 0 : 1), total)} / {total}</span>
        <button class="text-base leading-none hover:text-ink-soft" onclick={() => (showFilters = true)}
          >⚙</button
        >
      </div>
    </div>
    <div class="mx-5 mb-1 h-1 rounded-full bg-surface-2">
      <div
        class="h-1 rounded-full bg-ink-faint transition-all"
        style="width: {total ? (reviewed / total) * 100 : 0}%"
      ></div>
    </div>

    {#if done}
      <!-- session complete / nothing due -->
      <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
        <p class="display text-2xl font-bold text-ink">
          {total === 0 ? "All caught up" : "Round complete"}
        </p>
        <p class="mt-2 text-sm leading-relaxed text-ink-soft">
          {#if total === 0}
            Nothing is due under your current filters. Widen the role or enable more dungeons.
          {:else}
            You reviewed {reviewed} card{reviewed === 1 ? "" : "s"} this round.
          {/if}
        </p>
        <button
          class="mt-6 rounded-xl border border-line bg-surface-2 px-5 py-2.5 text-sm text-ink"
          onclick={rebuild}
        >
          {total === 0 ? "Refresh" : "Another round"}
        </button>
      </div>
    {:else}
      <DungeonFrame
        cue={current.cue}
        height={phase === "reveal" ? 150 : 210}
        status={phase === "reveal" ? (wasCorrect ? "correct" : "wrong") : null}
      />

      {#key current.id}
        {#if phase === "cue"}
          <!-- retrieval: cue + timed multiple choice -->
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
          <!-- rich reveal + one-tap advance (grade inferred from latency) -->
          <div class="scroll {wasCorrect ? 'fx-correct' : 'fx-wrong'} flex-1 px-5 pt-4">
            <RevealPanel card={current} archetype={archetype(current.answer)} />
            <NextButton onnext={next} {wasCorrect} {timedOut} />
          </div>
        {/if}
      {/key}
    {/if}

    <ModeNav mode="drill" />
  </div>

  {#if showFilters}
    <FilterSheet onclose={() => (showFilters = false)} />
  {/if}
</div>
