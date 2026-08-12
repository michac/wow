# Combat Assist Plus — open questions

**What this file is for:** product questions that still require an author decision. It holds
the smallest live options and what would decide between them. Approved behavior belongs in
`spec.md`; agreed work in `backlog.md`; completed reasoning in `notes.md`.

The corrected simplification keeps discrete ASAP / SOON / FALLBACK tiers while retaining the
small pilot, readable-first markers, enhanced-abilities-only catalogs, no automatic
current/next sequences, static baseline treatments and one Tyrant-bar experiment.

## D18 — What static tier treatments survive real icon art?

The baseline needs three treatments that are categorically distinguishable across several
icons without requiring comparison of small brightness differences. They must also remain
distinct from Blizzard's stock proc glow.

Smallest candidates:

- distinct static border colors with one shared geometry;
- distinct border thickness or silhouette as a color-independent second channel;
- a compact tier glyph paired with a restrained border.

The first flight should test categorical recognition, brightness, contrast, size and
stock-proc interaction on the actual CDM surface. No alpha, blend mode or geometry is approved
before that look.

**Baseline under test:** static gold / blue / slate borders for ASAP / SOON / FALLBACK, with
decreasing thickness. Their exact paint is disposable until the checkpoint flight.

## D19 — How should stock proc glow coexist with Demonbolt emphasis?

The first suppression attempt did not visibly dim Blizzard's proc glow. The product need is
only that Demonbolt's readable shard context not be drowned out.

Smallest options:

- reliably soften the stock glow while cap has a Demonbolt opinion;
- leave it intact and make cap's static treatment distinguishable by shape and position;
- stop adding icon emphasis and put shard context in a nearby marker instead.

First instrument whether the alert field resolves and whether the setter runs. Then choose by
looking; a successful setter call cannot decide the visual result.

**Baseline under test:** leave the stock glow intact and distinguish cap by the static outer
border. The draw capture says `stock:coexist`; it does not claim the two are visually distinct.

## D20 — What should the two Tyrant setup markers look like?

The facts are approved: separate readable markers for Dreadstalkers and Grimoire setup state,
with no combined press/don't-press verdict. The remaining choice is how the player tells the
facts apart without learning a miniature legend.

Smallest options:

- two fixed-position dots with distinct colors;
- simple glyphs tied to the source abilities;
- one compact two-cell marker whose positions are stable.

Choose the simplest form the player can identify during a real Tyrant setup.

**Baseline under test:** a blue left dot for Dreadstalkers committed and a purple right dot for
the transformed Grimoire row. These are commitment facts, not pet-active indicators.

## D21 — Does the Tyrant bar earn its surface?

The bar is deliberately independent of icon emphasis and markers. It succeeds only if the
next burst window becomes easier to read than it is from the CDM icon alone.

After one flight, keep it if the countdown is legible and useful without pulling attention
away from the icon. Otherwise remove the bar rather than generalizing it to more cooldowns.
