/* Combat Assist Plus — the primitives gallery (primitives.html only).
 *
 * Split out of stepper.js 2026-08-24 for the page budget: this code draws only into the
 * `#gallery` / `#frames` hosts, which exist on primitives.html alone, so its bytes were dead
 * weight on every spec page. capart embeds it back into stepper.js's __GALLERY_JS__ seam
 * at build time — SAME SCOPE, so everything here still reads stepper.js's helpers (el, host,
 * rgb, itemNode, D, T) directly. The no-colors rule of stepper.js applies unchanged.
 */
  function swatch(name, why, build) {
    var s = el("div", "swatch");
    var host = el("div", "swatch-stage");
    host.style.height = "calc(" + T.surfaces.icon_px + "px * 1.6)";
    host.appendChild(build());
    s.appendChild(host);
    var n = el("div", "name"); n.textContent = name; s.appendChild(n);
    var w = el("div", "why"); w.innerHTML = why; s.appendChild(w);
    return s;
  }

  var gallery = host("gallery");

  var SCAN_SAMPLES = D.scan_samples || [];

  // V13 · in the scan. One swatch, because there is one treatment: an icon either participates
  // in the read or it does not. What used to be four hue-coded lanes is now carried by row
  // order plus elimination, which is what the reading rule already used.
  //
  // ⚠ The blend mode is READ OFF THE TOKEN, never restated here. It was `ADD` until 2026-08-23
  // and this caption still said "additive" after the shelf had stopped saying it — a caption
  // that names a value the token owns is a second copy that drifts.
  gallery.appendChild(swatch(
    "in the scan · V13",
    "a <b>" + T.ready.line_px + "px</b> edge at alpha " + T.ready.alpha + ", blended <b>" +
      T.ready.blend + "</b>, drawn ON the icon rect. The restrained <em>area</em> is what lets " +
      "full brightness sit at alpha " + T.ready.alpha + " without the row shouting. Every " +
      "non-swiped row wears it <em>identically</em> — the press is the leftmost thing not " +
      "ruled out, not a thing cap draws. It has no falloff, so it cannot reach a neighbour.",
    function () { return bareItem(D.scan_sample, "press"); }
  ));


  gallery.appendChild(swatch("swipe", "Blizzard's own dial — cap draws nothing here, and does " +
    "not restyle it. The cheapest possible “ruled out”.",
    function () { return bareItem(D.scan_sample, "cd"); }));

  // V5 · one swatch per cue, then the full three slots, so "do three badges crowd the face?"
  // is answerable rather than asserted.
  var cueKeys = Object.keys(T.cues);
  cueKeys.forEach(function (key) {
    var cue = T.cues[key];
    gallery.appendChild(swatch(
      "cue · " + key + (cue.open ? " ⚠" : ""),
      (cue.open ? "<b>declared, unverified in client — produces no hint yet.</b> " : "") +
        cue.means + " <em>(rank " + cue.rank + ", " + cue.frames.length + " frames @ " +
        cue.duration_s + "s " + cue.loop + ")</em>",
      function () { return bareItem(D.scan_sample, "below", { cues: [key] }); }
    ));
  });

  // The stack is a Z-STACK, so "how far down the icon does it reach?" has stopped being a
  // question and this swatch answers the one that replaced it: WHICH badge survives. It hands
  // the row every cue in the vocabulary at once — the worst case by construction rather than by
  // a number someone has to keep up to date — and one disc comes back.
  var stack = cueKeys.slice().sort(function (a, b) {
    return (T.cues[a].rank || 99) - (T.cues[b].rank || 99);
  });
  gallery.appendChild(swatch("badges · the whole vocabulary at once",
    "Every cue in the vocabulary on one row, and <b>one badge draws</b>: they share a corner " +
    "and only the top of the order is visible. The order is <em>negatives occlude positives, " +
    "rank decides inside a polarity</em> — not rank alone — because the two mistakes are not " +
    "the same size: a skip hidden under a promotion makes a held row look pressable and costs " +
    "the press, where a promotion hidden under a skip costs a beat. Worn: " + stack.join(" · ") +
    ".",
    function () { return bareItem(D.scan_sample, "below", { cues: stack }); }));

  // A badge overhanging the corner can collide with the next icon. That is arithmetic, and
  // arithmetic in a caption is an assertion; drawn in a real row it is a finding.
  var over = T.badges.overhang_px, gap = T.surfaces.row_gap_px;
  gallery.appendChild(swatch("badges · in a real row",
    "overhangs <b>" + over + "px</b> past the edge; the row gap is <b>" + gap + "px</b>" +
      (over > gap ? " — <b>they collide.</b>" : " — <b>they clear.</b>"),
    function () {
      var strip = el("div", "swatch-stage");
      SCAN_SAMPLES.slice(0, 3).forEach(function (name, i) {
        strip.appendChild(bareItem(name, "below",
          { cues: [cueKeys[i % cueKeys.length]] }));
      });
      return strip;
    }));

  /* V16-V19 · the sealed displays.
   *
   * ⚠ Each caption leads with WHAT THE ROW IS SAYING, then how it is drawn. The pixels are
   * already on screen; what a reader cannot see is the statement, and a caption that only
   * describes the drawing spends its whole length on the half you can check yourself.
   *
   * "Sealed" is not about auras. It means the VALUE cap hands the client is one Lua may never
   * read or branch on: cap authors the rule, the client evaluates it against the secret and
   * draws the result, and cap never learns which way it went. Everything above this point on
   * the page is driven by a fact cap can read.
   *
   * All of them draw through the same `sealedNode` a scenario row uses, so a swatch and a live
   * row cannot diverge.
   */
  gallery.appendChild(swatch("sealed · count bands · V16",
    "<b>&ldquo;there are enough of these for the thing you are about to press.&rdquo;</b> " +
    "A stack cap is not allowed to count reached a number the catalog cares about, and the " +
    "client said so on cap's behalf. The band picks the mark <em>or</em> the numeral: the " +
    "numeral while <em>how many more</em> is still the live question, the mark once the answer " +
    "has stopped being a number. Since 2026-08-24 the positive direction wears <b>no hatch</b> " +
    "— a hatch means <em>ruled out</em>, so it belongs to the eliminating direction alone — and " +
    "the numeral sits on the badge plate like every other corner mark (its own slot, same " +
    "thresholds). ⚠ <b>No scenario in any catalog draws this direction</b> — " +
    "every shipped band eliminates — which is exactly why it is drawn here.",
    function () {
      return bareItem(D.scan_sample, "press", { sealed: ["count-bands"], count: 4 });
    }));

  gallery.appendChild(swatch("sealed · count bands · V17 (complement)",
    "<b>&ldquo;not yet — there are not enough of these, so this row is out.&rdquo;</b> The same " +
    "sink authored the other way round: the marks draw BELOW the threshold and clear at it, so " +
    "the row rules <em>itself</em> out and becomes a candidate the moment the count arrives. " +
    "This is the only eliminating signal that is neither Blizzard's swipe nor a badge cap " +
    "decided to show. Since 2026-08-24 the corner states the <b>count itself</b>, in the " +
    "negative red on the plate — <em>how many there are</em> is the live question the whole " +
    "time the row is out, and a glyph could only say <em>some</em>. ⚠ Honest only where " +
    "<em>low is bad</em>; on a rising resource it would call progress a fault.",
    function () {
      return bareItem(D.scan_sample, "ruled-sealed", { sealed: ["count-bands"], count: 2 });
    }));

  gallery.appendChild(swatch("sealed · count bar · V18 — segmented, red at full",
    "<b>&ldquo;this many banked — and at full, STOP BANKING.&rdquo;</b> Left: the sealed count " +
    "as a left-to-right bar on the row's bottom edge, over a segment grid (cap's own track " +
    "art) that makes it read as <em>2 of 4</em> rather than <em>some</em>. Right: at max the " +
    "<b>whole bar flips to the negative red</b> — a warning that stacks are capped and procs " +
    "are about to be wasted. The flip is not the fill recolouring (the value is sealed): it is " +
    "a second slot's count band drawing a full-width pre-tinted red crop at threshold = max, " +
    "client-decided like every band. ⚠ It can never be silent: <code>SetValue</code> clamps " +
    "into [0, max], so the track is on the row at every value including zero — the straight " +
    "trade against V16, which can say nothing at all.",
    function () {
      var strip = el("div", "swatch-stage");
      strip.appendChild(bareItem(D.scan_sample, "press", { sealed: ["count-bar"] }));
      strip.appendChild(bareItem(D.scan_sample, "press", { sealed: ["count-bar"], full: true }));
      return strip;
    }));

  gallery.appendChild(swatch("sealed · pandemic window · V19 — the DoT pair",
    "<b>Two states for a running DoT, left to right.</b> Aura up but <b>outside</b> its " +
    "refresh window: the gold hatch — <em>do not refresh yet</em>, drawn by " +
    "<code>SetDurationText</code> band tables on the aura's remaining seconds. Aura up and " +
    "<b>inside</b> the window: the badge — plate, the positive cues' halo behind it, and at " +
    "its centre the <b>dial</b>: a radial the <em>client</em> drains off the DoT's own " +
    "remaining lifetime (<code>SetDurationBar</code>, RemainingTime — cap reads nothing). No " +
    "numeral. <em>&ldquo;refreshing this now clips nothing — and this much time to do it.&rdquo;</em> " +
    "⚠ The two edges are not the same fact: the badge appears on Blizzard's real window " +
    "(<code>GetRefreshExtendedDuration &minus; GetAuraBaseDuration</code>, per spell — cap " +
    "authors <b>no threshold</b> there), while the hatch clears at a threshold the " +
    "<b>catalog</b> authors in seconds, because the pandemic sink cannot be inverted. They can " +
    "disagree near the boundary, and the seam between them is a flight question.",
    function () {
      var strip = el("div", "swatch-stage");
      strip.appendChild(bareItem(D.scan_sample, "press", { sealed: ["pandemic"], outside: true }));
      strip.appendChild(bareItem(D.scan_sample, "press", { sealed: ["pandemic"] }));
      return strip;
    }));

  gallery.appendChild(swatch("sealed · proc bar · V20 — the client drains the proc's clock",
    "<b>The proc's remaining lifetime as a thin bar above the charge bar.</b> The slot " +
    "filters to the proc aura; while it is up the client shows the button and " +
    "<code>SetDurationBar</code> (RemainingTime) drains the fill off the aura's own duration " +
    "— when the proc drops, the whole button vanishes with it. cap authors no threshold, " +
    "reads nothing, and never learns where the fill is. It lives on the <em>edge</em>, not in " +
    "the badge column, because hue carries polarity there and gold time beside a red hold " +
    "read as two verdicts arguing (the corner-dial form lasted one day; V19's badge dial " +
    "stays, inside the promotion where gold is the right language). Left: alone on the " +
    "bottom edge. Right: lifted above V18's charge bar — <em>&ldquo;this many banked, this " +
    "long to use one&rdquo;</em> — beside a held row's badge, which stays red-only. " +
    "Consumers: Demonic Core on Demonbolt; the armed Demonic Art on the Infernal Bolt row.",
    function () {
      var strip = el("div", "swatch-stage");
      strip.appendChild(bareItem(D.scan_sample, "press", { sealed: ["proc-bar"] }));
      strip.appendChild(bareItem(D.scan_sample, "hold-readable", { sealed: ["count-bar", "proc-bar"] }));
      return strip;
    }));

  gallery.appendChild(swatch("sealed · base cooldown · V21 — the held row's cooldown, live",
    "<b>The <code>blocked</code> badge, drawing the cooldown it is blocked on.</b> A row held " +
    "because something is on cooldown used to wear <code>timer_CW_50</code> — a picture of a " +
    "clock face frozen at 50&nbsp;%, on a row where the real remaining time exists and is " +
    "reachable. It draws the real one instead: a red radial on the remaining, with a white " +
    "countdown in it. Same cue, same polarity, same rank, same red hatch beside it. Two catalog " +
    "displays reach this picture. <b>Its own base spell</b> " +
    "(<code>sealed-base-cooldown</code>): while a Grimoire is talented its row spends the whole " +
    "120&nbsp;s wearing the dispel it becomes, and <code>GetSpellCooldownInfo</code> resolves " +
    "the <em>display</em> identity before reading — so the swipe on that row is the dispel's " +
    "15&nbsp;s and the two-minute one runs invisibly underneath. <b>Another ability's</b> " +
    "(<code>sealed-cooldown-range</code>): the dependency a band is waiting on, named by " +
    "catalog key. Either way the arc drains a real remaining " +
    "(<code>GetSpellCooldownDuration</code> → <code>SetTimerDuration</code>, RemainingTime) and " +
    "the numeral is the same object's <code>FormatRemainingDuration</code> — a secret string " +
    "the client renders and cap never reads back. Left: the dial with no cue on the row, which " +
    "is what a swiped row draws — the countdown is a quantity there and nothing is being ruled " +
    "out that Blizzard has not already ruled out. Right: the same widget carrying the " +
    "<code>blocked</code> verdict, which is the whole change — one statement, not a still " +
    "clock drawn over a running one.",
    function () {
      var strip = el("div", "swatch-stage");
      strip.appendChild(bareItem(D.scan_sample, "cd", { sealed: ["base-cooldown"] }));
      strip.appendChild(bareItem(D.scan_sample, "open",
        { sealed: ["base-cooldown"], cues: ["blocked"], cue_dials: ["blocked"] }));
      return strip;
    }));

  gallery.appendChild(swatch("sealed · aura remaining · V21 — an aura's clock, in the badge's place",
    "<b>The third supplier of V21's picture, and the only one that resolves no cooldown at " +
    "all.</b> (<code>sealed-aura-remaining</code>): the slot filters to an <em>aura</em>, and the " +
    "client drains the arc off that aura's own duration object — so the badge exists exactly " +
    "while the aura does and its visibility <em>is</em> the gate. The subject is the ability the " +
    "MARKER names rather than the bound row's, which is what lets it reach across rows: " +
    "Demonbolt held because row&nbsp;9 is showing Infernal Bolt draws the armed Art's clock, " +
    "which is how long that hold lasts. <b>No numeral, and that is a limit rather than a " +
    "choice:</b> V21's number comes from <code>FormatRemainingDuration</code> on a cooldown " +
    "object cap holds, while the only aura-side text sink " +
    "(<code>SetDurationText</code>) emits fixed strings — <code>\"\"</code> or a texture " +
    "escape — never a value over the remaining seconds. The arc alone is still strictly more " +
    "than a clock face frozen at 50&nbsp;%.",
    function () {
      var strip = el("div", "swatch-stage");
      strip.appendChild(bareItem(D.scan_sample, "open",
        { sealed: ["aura-remaining"], cues: ["blocked"], cue_dials: ["blocked"] }));
      return strip;
    }));

  gallery.appendChild(swatch("badge · numeral · V22 — the count cap holds",
    "<b>The badge, with a number cap authored where the glyph would be.</b> The same defect as " +
    "V21's, one row over: <code>implosion_no_imps</code> wore <code>timer_CW_50</code> — a clock " +
    "frozen at 50&nbsp;% — on a row where nothing is on cooldown and nothing is being waited " +
    "out, while the three states beside it on that row drew a <em>number</em>: red at 1–5 imps, " +
    "gold at 6 or more. The zero was the one value in the sequence drawn as a symbol, and the " +
    "one value cap holds outright. <b>The licence is the marker's own <code>when</code>:</b> " +
    "everywhere else a count is the client's, out of an AuraContainer FontString cap never " +
    "reads back — this one is a constant a readable term already established, because " +
    "<code>!aura(wild_imp)</code> <em>means</em> zero. A numeral whose value its own marker does " +
    "not fix would be cap asserting a count it does not hold, and <code>Catalog.Check</code> " +
    "refuses it. Left: the numeral, in <code>count.low_rgb</code> — byte-identical to the shared " +
    "badge red, because a <code>0</code> and a <code>1</code> are the same statement about the " +
    "same row. Right: the client's own numeral at three, for comparison — the sequence the zero " +
    "now joins.",
    function () {
      var strip = el("div", "swatch-stage");
      strip.appendChild(bareItem(D.scan_sample, "open",
        { cues: ["blocked"], cue_numerals: { blocked: 0 } }));
      strip.appendChild(bareItem(D.scan_sample, "ruled-sealed",
        { sealed: ["count-bands"], count: 3 }));
      return strip;
    }));

  // The frame strips, so the art itself is inspectable rather than only seen in motion.
  var framesHost = host("frames");
  cueKeys.forEach(function (key) {
    var cue = T.cues[key];
    var s = el("div", "swatch");
    var strip = el("div", "frames");
    cue.frames.forEach(function (fn) {
      var f = D.frames[fn];
      var d = el("div", "f");
      var g = el("i");
      if (f) {
        g.style.backgroundColor = rgb(T.badges.rgb);
        g.style.webkitMaskImage = g.style.maskImage = "url(" + f.uri + ")";
        g.style.webkitMaskSize = g.style.maskSize = "contain";
        g.style.webkitMaskRepeat = g.style.maskRepeat = "no-repeat";
        g.style.webkitMaskPosition = g.style.maskPosition = "center";
      }
      d.appendChild(g);
      strip.appendChild(d);
    });
    s.appendChild(strip);
    var n = el("div", "name"); n.textContent = key; s.appendChild(n);
    var w = el("div", "why");
    w.innerHTML = cue.frames.join(" → ") + " · " + cue.loop.toLowerCase();
    s.appendChild(w);
    framesHost.appendChild(s);
  });

  /* ------------------------------------------------------------------ tables */

  var vt = host("verdicts");
  var head = "<tr><th>verdict</th><th>in the scan</th><th>swipe</th><th>hatch</th>" +
    "<th>eliminates</th><th>cues</th></tr>";
  vt.innerHTML = head + Object.keys(T.verdicts).map(function (k) {
    var r = T.verdicts[k];
    return "<tr><td>" + k + "</td><td>" + (r.scan ? "yes" : "—") + "</td><td>" +
           (r.swipe ? "yes" : "—") + "</td><td>" + (r.hatch ? "yes" : "—") + "</td><td>" +
           (r.eliminates ? "yes" : "—") + "</td><td>" +
           ((r.cues && r.cues.length) ? r.cues.join(", ") : "—") + "</td></tr>";
  }).join("");

