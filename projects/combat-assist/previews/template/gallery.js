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

  // The stack FLOWS, so there are no slots to show one-per. What this has to answer instead is
  // "how far down the icon does a full stack reach, and does it still read?" — so it draws every
  // cue in the vocabulary at once, which is the worst case by construction rather than by a
  // number someone has to keep up to date.
  var stack = cueKeys.slice().sort(function (a, b) {
    return (T.cues[a].rank || 99) - (T.cues[b].rank || 99);
  });
  gallery.appendChild(swatch("badges · the full stack",
    "Every cue at once, in rank order — the deepest stack the vocabulary can produce, which is " +
    "the crowding question worth answering now that there is no ceiling. Positives rank first " +
    "and sit on the corner, so a promotion is the badge the eye reaches before any skip. " +
    "Shown: " + stack.join(" · ") + ".",
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

