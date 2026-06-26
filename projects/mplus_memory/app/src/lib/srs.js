/**
 * srs.js — SM-2 spaced-repetition scheduler.
 *
 * A card's schedule state is a plain object so the whole map serialises into one
 * localStorage blob. Grades map onto SM-2 quality scores:
 *   Again → 1 (lapse) · Hard → 3 · Good → 4 · Easy → 5
 *
 * @typedef {"again"|"hard"|"good"|"easy"} Grade
 * @typedef {Object} CardState
 * @property {number} ease       SM-2 easiness factor (>= 1.3)
 * @property {number} interval   days until next review
 * @property {number} reps       consecutive successful reviews
 * @property {number} lapses     count of Again grades
 * @property {number} due        epoch ms when the card is next due
 * @property {number} [last]     epoch ms of the last review
 */

export const GRADE_QUALITY = { again: 1, hard: 3, good: 4, easy: 5 };

const DAY = 86_400_000;
const MIN_EASE = 1.3;

/** A brand-new card: due immediately, never seen. */
export function freshState(now = Date.now()) {
  return { ease: 2.5, interval: 0, reps: 0, lapses: 0, due: now, last: 0 };
}

/**
 * Apply a grade to a card state and return the next state (pure).
 * @param {CardState} state
 * @param {Grade} grade
 * @param {number} now epoch ms
 * @returns {CardState}
 */
export function review(state, grade, now = Date.now()) {
  const s = state ?? freshState(now);
  const q = GRADE_QUALITY[grade] ?? 4;

  // Easiness update (classic SM-2), clamped.
  let ease = s.ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02));
  if (ease < MIN_EASE) ease = MIN_EASE;

  let { reps, lapses, interval } = s;

  if (q < 3) {
    // Lapse: reset reps, short relearn step, nudge ease down.
    reps = 0;
    lapses += 1;
    interval = 0; // due again this session (≈10 min handled by due offset below)
    return {
      ease,
      interval,
      reps,
      lapses,
      due: now + 10 * 60_000, // 10-minute relearn step
      last: now,
    };
  }

  reps += 1;
  if (reps === 1) interval = 1;
  else if (reps === 2) interval = 3;
  else interval = Math.round(interval * ease);

  // Hard tightens, Easy stretches the computed interval a touch.
  if (grade === "hard") interval = Math.max(1, Math.round(interval * 0.8));
  if (grade === "easy") interval = Math.round(interval * 1.3);

  return { ease, interval, reps, lapses, due: now + interval * DAY, last: now };
}

/**
 * Infer an SM-2 grade from correctness + how long the player took, replacing the
 * manual Again/Hard/Good/Easy self-grade. The cast bar is already a solve timer:
 * a fast correct answer means the card was easy, a last-second one means it was hard.
 * Any wrong answer (or timeout) is a lapse → "again". Thresholds are fractions of
 * the cast-bar `duration` and tunable by feel.
 * @param {boolean} wasCorrect did the player pick the right archetype (and in time)?
 * @param {number} elapsedMs   ms taken to answer
 * @param {number} durationMs  full cast-bar duration
 * @returns {Grade}
 */
export function gradeFromLatency(wasCorrect, elapsedMs, durationMs) {
  if (!wasCorrect) return "again"; // wrong pick or timeout
  const frac = durationMs > 0 ? elapsedMs / durationMs : 1;
  if (frac < 0.33) return "easy"; // snap-fast
  if (frac < 0.66) return "good"; // comfortable
  return "hard"; // slow / last-second
}

/** Is this card due for review at `now`? Unseen cards (no state) are due. */
export function isDue(state, now = Date.now()) {
  return !state || state.due <= now;
}
