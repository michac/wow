/* Combat Assist Plus — preview behavior.
 *
 * This file holds NO colors, rates or sizes. Everything it draws with comes from the
 * embedded token block, which `wowkb.capart` lifted verbatim out of
 * `specs/render-shelf.md` Part 6. If a swatch looks wrong, the fix is a shelf edit and a
 * rebuild — never an edit here, and never an edit to the generated HTML.
 */
(function () {
  "use strict";

  var T = JSON.parse(document.getElementById("cap-tokens").textContent);
  var D = JSON.parse(document.getElementById("cap-data").textContent);

  function rgb(c, a) {
    var f = function (v) { return Math.round(v * 255); };
    return "rgba(" + f(c[0]) + "," + f(c[1]) + "," + f(c[2]) + "," + (a === undefined ? 1 : a) + ")";
  }
  function el(tag, cls) { var n = document.createElement(tag); if (cls) n.className = cls; return n; }

  /* ------------------------------------------------------------------ badge sprites
   * A cue is a filled disc with one sprite frame showing at a time. The client walks a
   * FlipBook; we walk the same frame list at the same rate, so what you see is the art's real
   * cadence and not a CSS easing. BOUNCE plays forward then back, exactly as the animation
   * system does.
   */
  // Row badges are rebuilt on every step, so their timers must be reaped or they pile up one
  // set per keypress. Gallery badges are built once and must NOT be reaped with them — hence
  // the collector rather than a single global list.
  var ROW_TIMERS = [];
  var COLLECT = null;

  function animateSprite(sprite, cue) {
    var n = cue.frames.length;
    var i = 0, dir = 1;
    // A single-frame cue (loop HOLD) is a still image. Setting an interval on it would burn a
    // timer to re-assign the same url forever, so bind the one frame and stop.
    if (n < 2) {
      var only = D.frames[cue.frames[0]];
      if (only) sprite.style.setProperty("--frame", "url(" + only.uri + ")");
      return;
    }
    function tick() {
      var f = D.frames[cue.frames[i]];
      if (f) sprite.style.setProperty("--frame", "url(" + f.uri + ")");
      if (cue.loop === "BOUNCE") {
        if (i + dir < 0 || i + dir >= n) dir = -dir;
        i += dir;
      } else {
        i = (i + 1) % n;
      }
    }
    tick();
    var id = setInterval(tick, (cue.duration_s / n) * 1000);
    if (COLLECT) COLLECT.push(id);
  }

  function badgeNode(key, index) {
    var cue = T.cues[key] || {};
    var slot = el("div", "slot");
    slot.setAttribute("data-index", String(index || 0));
    slot.title = key + " — " + (cue.means || "") + (cue.open ? " (open — unverified in client)" : "");
    if (cue.open) slot.setAttribute("data-open", "1");
    slot.setAttribute("data-polarity", cue.polarity || "negative");
    // Per-cue hue, falling back to the shared badge red. The negatives all take the fallback on
    // purpose: one red for every "skip this" is what makes the row readable without decoding.
    if (cue.rgb) slot.style.setProperty("--slot-tint", "var(--cue-" + key + "-tint)");
    // The GLOW pulses BEHIND the glyph, and the glyph itself never changes alpha. A cue that
    // faded would make its own information blink, which is the thing the text limits exist to
    // forbid; a halo can breathe without the fact it carries ever going away.
    if (cue.glow) {
      var glow = el("div", "glow");
      glow.style.setProperty("--g-dur", "var(--cue-" + key + "-glow-dur)");
      glow.style.setProperty("--g-a0", "var(--cue-" + key + "-glow-a0)");
      glow.style.setProperty("--g-a1", "var(--cue-" + key + "-glow-a1)");
      glow.style.setProperty("--g-scale", "var(--cue-" + key + "-glow-scale)");
      slot.appendChild(glow);
    }
    var sprite = el("div", "sprite");
    slot.appendChild(sprite);
    if (cue.frames) animateSprite(sprite, cue);
    return slot;
  }

  /* ------------------------------------------------------------------ V13 · the scan edge
   *
   * One hue, no roles, no motion. Its numbers come from `tokens.ready`, emitted as --ready-* by
   * capart, so no value appears in this file. There is no art and nothing to walk: the ring
   * flipbook the retired V2 border stepped through is Part 7's now, and only the in-game
   * `/cap style` gallery can draw it (CSS has no four-strip ring).
   */

  function scanMark() {
    var n = el("div", "ready-line");
    n.style.setProperty("--rl-rgb", "var(--ready-rgb)");
    n.style.setProperty("--rl-rest", "var(--ready-alpha)");
    n.style.setProperty("--rl-line", "var(--ready-line)");
    return n;
  }

  /* ------------------------------------------------------------------ one CDM item */

  function itemNode(entry, index) {
    var ab = D.abilities[entry.name] || {};
    var rule = T.verdicts[entry.verdict] || {};

    var item = el("div", "item");

    var art = el("div", "art");
    if (ab.icon) art.style.backgroundImage = "url(" + ab.icon + ")";
    clientPaint(art, entry, rule);
    item.appendChild(art);

    if (rule.swipe) item.appendChild(el("div", "swipe"));

    // V11 · the cooldown hatch. Over the icon and the swipe, under the badges — it states a
    // condition about the whole button, and the marks that say *why* must stay legible on top.
    // DEDUPED. A cue named twice is ONE badge -- that is how the band grammar expresses an OR,
    // and it holds just as much when the second mention comes from the verdict rather than from
    // a second marker. Without this, an entry whose verdict already implies `blocked` and which
    // also declares it draws two identical discs, which reads as two different reasons.
    var cueList = (rule.cues || []).concat(entry.cues || []).filter(function (k, i, all) {
      return all.indexOf(k) === i;
    });
    if (rule.hatch) item.appendChild(hatchLayer());
    // V11's second cause: cap's own verdict. A row wearing ANY negative cue is ruled out, and
    // the hatch is Part 0.5's pass 2 drawn -- until this shipped, a swiped row was unmistakably
    // out while a badged one relied on the reader noticing a 22px disc.
    var ruledOut = cueList.some(function (k) {
      return (T.cues[k] || {}).polarity !== "positive";
    });
    if (ruledOut) item.appendChild(skipLayer());

    // Every non-`cd` row is IN THE SCAN and wears the edge. `press`, `press-promoted` and
    // `below` render IDENTICALLY, and that is the point: the press is "the leftmost thing not
    // ruled out", not a thing cap draws (render-shelf.md Part 0.5). The edge goes OVER the art
    // — it is a rim on the button, not a layer across it.
    if (rule.scan) item.appendChild(scanMark());

    // V15 · the keybind hint. CHROME, not a cue (spec.md §3.8): it names the row and takes no
    // part in the scan, so it holds the top-left corner the badges never flow into and no
    // verdict can add or remove it. ⚠ The key is SIMULATED — `tokens.preview.hotkeys` by roster
    // position — because the point of drawing it here is judging how the text sits in the corner
    // before any of it reaches the game, and an empty corner cannot be judged.
    if (ab.hotkey) {
      var hk = el("div", "hotkey");
      hk.textContent = ab.hotkey;
      item.appendChild(hk);
    }

    var open = false;
    // Sorted by the cue's RANK, not by the order the catalog happened to name them, so two rows
    // wearing the same pair always stack them the same way round. Positives rank above
    // negatives, so a promotion lands on the corner (render-shelf.md Part 1).
    var cues = cueList.slice().sort(function (a, b) {
      return ((T.cues[a] || {}).rank || 99) - ((T.cues[b] || {}).rank || 99);
    });
    cues.forEach(function (k, i) {
      if ((T.cues[k] || {}).open) open = true;
      var node = badgeNode(k, i);
      // V14 rides the badge it belongs to, so it moves with the stack rather than being
      // anchored to the corner independently.
      if ((T.cues[k] || {}).polarity === "positive") node.insertBefore(promoRing(), node.firstChild);
      item.appendChild(node);
    });
    if (open) item.setAttribute("data-open", "1");

    var col = el("div", "lane");
    col.appendChild(item);
    // The name and the verdict are the ANSWER, and the row exists to ask whether the
    // decorations carry it unaided — so they hover rather than print. They also used to size
    // the lane (a caption wider than the icon set the lane width), which made the icon pitch
    // uneven and misreported the client's fixed-pitch row.
    col.setAttribute("data-name", entry.name);
    col.setAttribute("data-verdict", entry.verdict);
    if ((entry.cues || []).length) col.setAttribute("data-cues", entry.cues.join(" "));
    return col;
  }

  /* The one tooltip, fixed-position on <body> so no ancestor's overflow can clip it. */

  var tipEl = el("div", "tip");
  tipEl.id = "tip";
  document.body.appendChild(tipEl);

  function tipShow(col) {
    var cues = col.getAttribute("data-cues");
    tipEl.innerHTML = "<b>" + col.getAttribute("data-name") + "</b>" +
      "<span class=\"tip-verdict\">" + col.getAttribute("data-verdict") + "</span>" +
      (cues ? "<span class=\"tip-cues\">" + cues + "</span>" : "");
    tipEl.setAttribute("data-on", "1");
    var r = col.getBoundingClientRect(), t = tipEl.getBoundingClientRect();
    var x = r.left + r.width / 2 - t.width / 2;
    tipEl.style.left = Math.max(4, Math.min(x, window.innerWidth - t.width - 4)) + "px";
    tipEl.style.top = (r.bottom + 8) + "px";
  }
  function tipHide() { tipEl.removeAttribute("data-on"); }

  document.addEventListener("mouseover", function (e) {
    var col = e.target.closest && e.target.closest(".lane[data-name]");
    if (col) tipShow(col); else tipHide();
  });
  // NOT capture-phase: mouseleave does not bubble, but a capture listener on `document`
  // still sees every descendant's, so moving between an icon and its own badge would
  // flicker the tip away. Un-captured, this fires only when the pointer leaves the page.
  document.addEventListener("mouseleave", tipHide);
  window.addEventListener("scroll", tipHide, true);

  /* ------------------------------------------------------------------ the stepper */

  var pick = document.getElementById("pick");
  var rowEl = document.getElementById("row");
  var walkEl = document.getElementById("walk");
  var stateEl = document.getElementById("state");
  var extrasEl = document.getElementById("extras");

  var current = 0, step = 0;

  D.scenarios.forEach(function (s, i) {
    var o = el("option");
    o.value = String(i);
    o.textContent = s.id + " · " + s.title;
    pick.appendChild(o);
  });

  function reachedThrough(sc, upto) {
    // How far along the row the walk has got: the furthest row entry named by any step
    // shown so far. `upto < 0` means "the whole row", the resting view.
    if (upto < 0) return sc.row.length;
    var furthest = 0;
    for (var i = 0; i <= upto && i < sc.steps.length; i++) {
      sc.steps[i].names.forEach(function (n) {
        for (var j = 0; j < sc.row.length; j++) if (sc.row[j].name === n && j + 1 > furthest) furthest = j + 1;
      });
    }
    return furthest;
  }

  function clearRowTimers() { ROW_TIMERS.forEach(clearInterval); ROW_TIMERS = []; }

  function render() {
    var sc = D.scenarios[current];
    var reach = reachedThrough(sc, step - 1);

    stateEl.innerHTML = "<b>State.</b> " + sc.state;

    clearRowTimers();
    COLLECT = ROW_TIMERS;
    rowEl.innerHTML = "";
    sc.row.forEach(function (entry, i) {
      var col = itemNode(entry, i);
      if (i >= reach && step > 0) col.setAttribute("data-dimmed", "1");
      if (step > 0 && i === reach - 1) col.setAttribute("data-active", "1");
      rowEl.appendChild(col);
    });
    COLLECT = null;

    walkEl.innerHTML = "";
    sc.steps.forEach(function (s, i) {
      var n = el("div", "step");
      if (step > 0 && i === step - 1) n.setAttribute("data-active", "1");
      if (step > 0 && i > step - 1) n.setAttribute("data-future", "1");
      var num = el("div", "n"); num.textContent = String(i + 1);
      var body = el("div"); body.innerHTML = s.html;
      n.appendChild(num); n.appendChild(body);
      walkEl.appendChild(n);
    });

    extrasEl.innerHTML = "";
    (sc.extras || []).forEach(function (x) {
      var n = el("div", "aside");
      n.innerHTML = "<b>" + x.label + ".</b> " + x.html;
      extrasEl.appendChild(n);
    });
  }

  pick.addEventListener("change", function () { current = +pick.value; step = 0; render(); });
  document.getElementById("next").addEventListener("click", function () {
    var sc = D.scenarios[current];
    step = Math.min(step + 1, sc.steps.length);
    render();
  });
  document.getElementById("prev").addEventListener("click", function () {
    step = Math.max(step - 1, 0); render();
  });
  document.getElementById("all").addEventListener("click", function () { step = 0; render(); });
  document.getElementById("zoom").addEventListener("click", function () {
    var on = rowEl.getAttribute("data-zoom") === "2";
    rowEl.setAttribute("data-zoom", on ? "1" : "2");
    this.setAttribute("aria-pressed", on ? "false" : "true");
  });

  /* ------------------------------------------------------------------ gallery */

  // ------------------------------------------------------------------ Blizzard's baseline
  // What the client already paints on this icon, before cap draws anything. It goes on `.art`
  // itself rather than into a layer of its own, because that is where the client puts it — a
  // SetVertexColor on the icon texture — and because everything cap adds (swipe, hatch, border,
  // badges) is a sibling drawn OVER `.art`, so the stacking falls out for free.
  //
  // ⚠ Read from `D.client_paint`, never from `T`. These numbers are Blizzard's, transcribed from
  // its source; they are not shelf tokens and nothing here may treat them as tunable.
  function clientPaint(art, entry, rule) {
    var paint = D.client_paint || {};
    // Desaturation means ON COOLDOWN and nothing else, so it follows the `cd` verdict rather
    // than a declaration. `--desat` is the grayscale filter `.art` already carries.
    if (rule.swipe && paint.cooldown_desaturates) art.style.setProperty("--desat", "1");

    var state = entry.client;
    if (!state) return;                      // no declaration = ITEM_USABLE_COLOR = untouched
    var tint = (paint.tints || {})[state];
    if (!tint) return;
    // SetVertexColor MULTIPLIES. So does this. A filter/hue-rotate would look similar and would
    // be able to produce colours the client cannot, which is the one lie a reproduction may not
    // tell (see this tool's header).
    art.style.backgroundColor = rgb(tint.rgb);   // 0..1 floats, same scale as the shelf's
    art.style.backgroundBlendMode = "multiply";
    art.title = "client: " + tint.constant + " — " + tint.means;
  }

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

  var gallery = document.getElementById("gallery");

  // The swatch's border comes from whichever ability it borrows art from, exactly as it does in
  // a scenario row — so a gallery swatch and a live row can never diverge.
  function bareItem(name, verdict, opts) {
    opts = opts || {};
    return itemNode({ name: name, verdict: verdict, cues: opts.cues }, 0).firstChild;
  }

  var SCAN_SAMPLES = D.scan_samples || [];

  // V2 · in the scan. One swatch, because there is one treatment: an icon either participates
  // in the read or it does not. What used to be four hue-coded lanes is now carried by row
  // order plus elimination, which is what the reading rule already used.
  gallery.appendChild(swatch(
    "in the scan · V2",
    "a <b>" + T.ready.line_px + "px</b> additive edge at alpha " + T.ready.alpha + ", drawn ON " +
      "the icon rect. Additive is why full brightness reads as a <b>hot line</b> rather than a " +
      "painted one, and the restrained area is why full brightness is not loud. Every " +
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

  // The frame strips, so the art itself is inspectable rather than only seen in motion.
  var framesHost = document.getElementById("frames");
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

  var vt = document.getElementById("verdicts");
  var head = "<tr><th>verdict</th><th>in the scan</th><th>swipe</th><th>hatch</th>" +
    "<th>cues</th></tr>";
  vt.innerHTML = head + Object.keys(T.verdicts).map(function (k) {
    var r = T.verdicts[k];
    return "<tr><td>" + k + "</td><td>" + (r.scan ? "yes" : "—") + "</td><td>" +
           (r.swipe ? "yes" : "—") + "</td><td>" + (r.hatch ? "yes" : "—") + "</td><td>" +
           ((r.cues && r.cues.length) ? r.cues.join(", ") : "—") + "</td></tr>";
  }).join("");

  /* ------------------------------------------------------------------ Part 7 · the lab
   *
   * Experiments, drawn so they can be looked at. Nothing here is the style, and nothing a
   * scenario can reach may reference it — `capart build` enforces that, this just draws it.
   */

  function labEntry(key, spec) {
    var box = el("div", "lab-entry");
    var h = el("h3");
    h.innerHTML = (spec.title || key) + ' <span class="key">lab.' + key + "</span>";
    box.appendChild(h);
    var asks = el("p", "asks");
    asks.innerHTML = "<b>Asks:</b> " + (spec.asks || "<em>nothing — Part 7 says an entry that " +
      "cannot say what it is asking is decoration</em>");
    box.appendChild(asks);
    // A font entry says where its face came from and what it costs, because "could we ship our
    // own font" is a licence question before it is a taste question.
    var f = LAB_FONTS[key];
    if (f) {
      var prov = el("p", "asks");
      prov.innerHTML = "<b>" + f.family + "</b> · " + f.origin + " · " + f.license +
        " · <b>" + (f.shippable ? "ours to ship" : "preview only") + "</b> · " +
        (f.source_bytes / 1024).toFixed(0) + " KB, subset to " +
        (f.subset_bytes / 1024).toFixed(1) + " KB";
      box.appendChild(prov);
    }
    var row = el("div", "lab-row");
    box.appendChild(row);
    return { box: box, row: row };
  }

  function labCell(node, caption) {
    var c = el("div", "lab-cell");
    var stage = el("div", "lab-stage");
    stage.appendChild(node);
    c.appendChild(stage);
    var cap = el("div", "cap");
    cap.innerHTML = caption || "";
    c.appendChild(cap);
    return c;
  }

  /* Diagonal stripes — V11's cooldown hatch, and Part 7's remaining entries.
   *
   * ONE tileable white-alpha sheet, generated at build time from `tokens.hatch`; every render
   * asks it for something DIFFERENT. `background-color` + `mask-image` is the faithful CSS
   * analogue of SetVertexColor multiplying white art, and `mask-position` is the SetTexCoord
   * offset that makes a complementary phase possible.
   *
   * There is deliberately no shared "is this striped" flag: a layer is built from ONE render's
   * own colour and phase, and a cell that needs two conditions shown gets two layers.
   */
  function maskedStripe(cls, rgbVar, phaseVar) {
    var n = el("div", cls);
    n.style.setProperty("--stripe-rgb", rgbVar);
    n.style.setProperty("--stripe-phase", phaseVar);
    // ⚠ Resolved AT CALL TIME, never hoisted into a module-scope `var`. The gallery is built
    // before the Part 7 section of this file executes, so a `var SHEET = D.lab_stripes` above
    // was still `undefined` when a cue swatch asked for it — and an unmasked stripe layer is
    // not a missing treatment, it is a FLAT RED FIELD that looks like a deliberate different
    // one. Measured 2026-08-19: gallery `mask-image: none`, scenario rows masked correctly.
    var sheet = D.lab_stripes;
    if (sheet) {
      n.style.webkitMaskImage = n.style.maskImage = "url(" + sheet.uri + ")";
    }
    return n;
  }

  function hatchLayer() {
    return maskedStripe("stripes", "var(--hatch-rgb)", "var(--hatch-phase)");
  }

  // The same sheet, cap's own colour and phase. One geometry, two verdicts (V11).
  function skipLayer() {
    // Its own class as well as the shared one: cap's half of V11 overhangs the icon rect and
    // carries a border, so that a ruled-out row's red REPLACES V13's yellow scan edge instead of
    // sitting inside it. Two treatments making opposite statements about one row, with the
    // yellow reading louder because it is a hard line, is the thing this prevents.
    var n = maskedStripe("stripes skip-hatch", "var(--hatch-skip-rgb)",
                         "var(--hatch-skip-phase)");
    return n;
  }

  /* V14 · the promotion ring — a glowing ring around the badge of a row wearing a positive cue.
   * A measured replica of Blizzard's proc glow: it does NOT pulse, it never covers the icon, and
   * its falloff is asymmetric. See render-shelf.md V14 for what was measured and why. */
  function promoRing() {
    var art = D.promotion || {};
    var n = el("div", "promo-ring");
    if (!art.uri) return n;
    var sc = art.w / 64, sr = art.h / 64;
    n.style.webkitMaskImage = n.style.maskImage = "url(" + art.uri + ")";
    n.style.webkitMaskSize = n.style.maskSize = (sc * 100) + "% " + (sr * 100) + "%";
    var i = 0;
    var stepX = sc > 1 ? 100 / (sc - 1) : 0, stepY = sr > 1 ? 100 / (sr - 1) : 0;
    var cols = T.promotion.cols, frames = T.promotion.frames;
    function tick() {
      var c = i % cols, r = Math.floor(i / cols);
      n.style.webkitMaskPosition = n.style.maskPosition = (c * stepX) + "% " + (r * stepY) + "%";
      i = (i + 1) % frames;
    }
    tick();
    var id = setInterval(tick, 1000 / T.promotion.fps);
    if (COLLECT) COLLECT.push(id);
    return n;
  }

  function stripeLayer(key) {
    return maskedStripe("stripes", "var(--lab-" + key + "-rgb)",
                        "var(--lab-" + key + "-phase)");
  }

  // The bare sheet, so pitch and angle are directly visible rather than only inferable from an
  // icon that is also doing five other things.
  function sheetSwatch(key) {
    return maskedStripe("lab-sheet", "var(--lab-" + key + "-rgb)",
                        "var(--lab-" + key + "-phase)");
  }

  function stripedItem(key, cell) {
    var item = bareItem(cell.ability, cell.verdict || "below", { cues: cell.cues || [] });
    var layers = cell.stripes || [];
    // Inserted BEFORE the first badge slot, so the stripes lie over the icon and the swipe but
    // under the corner badges — the badges are the thing that says *why* and must stay legible.
    var anchor = item.querySelector(".slot");
    layers.forEach(function (which) {
      var layer = stripeLayer(which === "self" ? key : which);
      if (anchor) item.insertBefore(layer, anchor); else item.appendChild(layer);
    });
    return item;
  }

  /* Part 7 · the flipbook entries — icon-scale VFX, the proc-glow family.
   *
   * These sit on the ICON RECT, not on a badge: Blizzard's proc glow surrounds the whole
   * button, and half of why it reads is that it is big. `scale` is a multiple of the icon.
   *
   * A sheet is stepped with `background-position` on a `steps()` animation, which is the CSS
   * analogue of SetTexCoord walking a grid. Baked-hue sheets draw as-is; a neutral one is
   * masked and tinted so it takes the lane's own colour.
   */
  var VFX = D.lab_vfx || {};

  function flipbookLayer(key, spec) {
    var art = VFX[spec.sheet] || {};
    var n = el("div", "vfx");
    n.setAttribute("data-fit", spec.frames > 1 ? "sheet" : "single");
    n.style.setProperty("--vfx-scale", "var(--lab-" + key + "-scale)");
    n.style.setProperty("--vfx-dur", "var(--lab-" + key + "-dur)");
    n.style.setProperty("--vfx-cols", "var(--lab-" + key + "-cols)");
    n.style.setProperty("--vfx-rows", "var(--lab-" + key + "-rows)");
    if (spec.period_s) n.style.setProperty("--vfx-period", "var(--lab-" + key + "-period)");
    if (!art.uri) return n;

    // ⚠ The CELL SIZE IS DECLARED, never assumed. The sheet is padded to a power of two, so
    // neither `art.w / cols` nor a fixed 64 is right: `corona` is one 128px frame in a 128x128
    // sheet, and `energy` is an 8x3 grid of 64px cells in a 512x256 one with a quarter of the
    // height unused. Assuming 64 drew the corona as a 2x2 grid and showed one corner of it.
    var cell = spec.cell;
    var sheetCols = art.w / cell, sheetRows = art.h / cell;
    // Scale the sheet so ONE cell covers the layer, then walk it by whole cells.
    var bgW = sheetCols * 100, bgH = sheetRows * 100;

    if (spec.tint === "lane") {
      n.setAttribute("data-tint", "lane");
      n.style.setProperty("--vfx-rgb", "var(--lab-" + key + "-rgb)");
      n.style.webkitMaskImage = n.style.maskImage = "url(" + art.uri + ")";
      n.style.webkitMaskSize = n.style.maskSize = bgW + "% " + bgH + "%";
    } else {
      n.style.backgroundImage = "url(" + art.uri + ")";
      n.style.backgroundSize = bgW + "% " + bgH + "%";
    }

    if (spec.frames > 1) walkSheet(n, spec, sheetCols, sheetRows);
    return n;
  }

  // Step a flipbook by setting background-position per frame, the same way `animateSprite`
  // steps the badge frames. CSS `steps()` cannot walk a 2-D grid without generated keyframes,
  // and generating keyframes per entry puts layout arithmetic into a stylesheet that is not
  // allowed to hold numbers.
  function walkSheet(node, spec, sheetCols, sheetRows) {
    var i = 0;
    // `background-position` in % is a RATIO, not an offset: 100% means "align the image's right
    // edge with the box's right edge". So one cell of travel is 100/(cells-1), over the sheet's
    // OWN cell count -- including the padding cells, which is why the frame count is what bounds
    // the walk and the grid is only what shapes it.
    var stepX = sheetCols > 1 ? 100 / (sheetCols - 1) : 0;
    var stepY = sheetRows > 1 ? 100 / (sheetRows - 1) : 0;
    function tick() {
      var c = i % spec.cols, r = Math.floor(i / spec.cols);
      var pos = (c * stepX) + "% " + (r * stepY) + "%";
      if (spec.tint === "lane") {
        node.style.webkitMaskPosition = node.style.maskPosition = pos;
      } else {
        node.style.backgroundPosition = pos;
      }
      i = (i + 1) % spec.frames;
    }
    tick();
    var id = setInterval(tick, 1000 / (spec.fps || 30));
    if (COLLECT) COLLECT.push(id);
  }

  function flipbookItem(key, spec, cell) {
    var item = bareItem(cell.ability, cell.verdict || "below", { cues: [] });
    if (cell.treat === false) return item;
    // BEFORE the badge slots, so a corner badge stays legible over the effect — the badge is
    // the thing that says *why*, and an effect that buries it has taken information away.
    var anchor = item.querySelector(".slot");
    var layer = flipbookLayer(key, spec);
    if (anchor) item.insertBefore(layer, anchor); else item.appendChild(layer);
    return item;
  }

  /* Part 7 · the blaze. A promotion that SHOUTS instead of pointing.
   *
   * Two entries differ in one thing: what shape the light has. `behind: "glyph"` masks the
   * bright field to the sprite's own silhouette, so the flame appears to be the source.
   * `behind: "plate"` puts it behind the badge's dark disc, so the light has a hard circular
   * edge and the plate keeps doing its contrast job.
   *
   * No number is in this file — `spread`, the two alphas and the period all arrive as CSS
   * variables from the shelf, same discipline as the stripe and readiness renders.
   */
  var LAB_SPRITES = D.lab_sprites || {};

  function blazeItem(key, spec, cell) {
    var item = bareItem(cell.ability, cell.verdict || "below", { cues: [] });
    // A CONTROL cell draws the icon and nothing else. Without this every cell wore the
    // treatment, including the one captioned "the same icon untreated" -- which makes the
    // comparison the entry exists for impossible to actually make.
    if (cell.treat === false) return item;
    var art = LAB_SPRITES[spec.sprite] || {};
    var badge = el("div", "blaze-badge");
    badge.setAttribute("data-behind", spec.behind || "glyph");
    badge.style.setProperty("--bl-rgb", "var(--lab-" + key + "-rgb)");
    badge.style.setProperty("--bl-rest", "var(--lab-" + key + "-rest)");
    badge.style.setProperty("--bl-flare", "var(--lab-" + key + "-flare)");
    badge.style.setProperty("--bl-spread", "var(--lab-" + key + "-spread)");
    badge.style.setProperty("--bl-glyph", "var(--lab-" + key + "-glyph)");
    if (spec.period_s) badge.style.setProperty("--bl-period", "var(--lab-" + key + "-period)");

    // The bright field, in one of THREE shapes -- which is the only thing separating these
    // entries. Masked to the GLYPH, a plain DISC behind the plate, or a RING from real art.
    // All three sit behind the sprite, and none ever touches the sprite's own alpha: a
    // promotion whose glyph blinks is a promotion that hides its own information.
    var behind = spec.behind || "glyph";
    var blaze = el("div", "blaze");
    if (behind === "glyph" && art.uri) {
      blaze.style.webkitMaskImage = blaze.style.maskImage = "url(" + art.uri + ")";
    } else if (behind === "corona" || behind === "sheet") {
      // Real art as the field. A ring or a flipbook, drawn rather than tinted, because both
      // carry their own falloff and a flat colour through a mask would lose the part that reads
      // as heat. `sheet` walks its frames; `corona` is a single frame and simply sits there.
      var art2 = VFX[spec.sheet] || {};
      if (art2.uri) {
        var sc = art2.w / spec.cell, sr = art2.h / spec.cell;
        if (spec.tint === "lane") {
          // The one neutral field: masked and tinted, so it takes the lane's colour.
          blaze.style.webkitMaskImage = blaze.style.maskImage = "url(" + art2.uri + ")";
          blaze.style.webkitMaskSize = blaze.style.maskSize = (sc * 100) + "% " + (sr * 100) + "%";
          blaze.setAttribute("data-tint", "lane");
        } else {
          blaze.style.backgroundImage = "url(" + art2.uri + ")";
          blaze.style.backgroundSize = (sc * 100) + "% " + (sr * 100) + "%";
        }
        if (spec.frames > 1) walkSheet(blaze, spec, sc, sr);
      }
    }
    badge.appendChild(blaze);

    var sprite = el("div", "blaze-sprite");
    if (art.uri) {
      sprite.style.webkitMaskImage = sprite.style.maskImage = "url(" + art.uri + ")";
    }
    badge.appendChild(sprite);

    item.appendChild(badge);
    return item;
  }

  /* The readiness treatments. Each entry supplies its own numbers and nothing is shared
   * between them — same discipline as the stripe renders above. `draws` picks the layer;
   * the CSS variables carry the values, so no number appears in this file. */

  function readyGlow(key, spec, index) {
    var n = el("div", "ready-glow");
    n.style.setProperty("--rg-rgb", "var(--lab-" + key + "-rgb)");
    n.style.setProperty("--rg-rest", "var(--lab-" + key + "-rest)");
    n.style.setProperty("--rg-flare", "var(--lab-" + key + "-flare)");
    n.style.setProperty("--rg-spread", "var(--lab-" + key + "-glow)");
    if (spec.flare_mult) {
      n.style.setProperty("--rg-flare-spread", "var(--lab-" + key + "-flare-glow)");
      n.style.setProperty("--rg-decay", "var(--lab-" + key + "-decay)");
      n.setAttribute("data-flare", "1");
    }
    if (spec.period_s) {
      n.style.setProperty("--rg-period", "var(--lab-" + key + "-period)");
      // The cycle's top. An entry that declares no `peak_alpha` breathes up to its flare value,
      // which is what a breathe-only entry means by it.
      n.style.setProperty("--rg-peak", spec.peak_alpha
        ? "var(--lab-" + key + "-peak)" : "var(--lab-" + key + "-flare)");
      // Out of phase on purpose: four breathing in lockstep read as one region blinking.
      n.style.setProperty("--rg-phase", (-(index || 0) * 0.37) + "s");
      n.setAttribute("data-breathe", "1");
    }
    return n;
  }

  // A cell may override the width, so one entry can show the ladder side by side rather than
  // needing an entry per value. The number is still the shelf's; this only chooses which.
  function readyLine(key, cell) {
    var n = el("div", "ready-line");
    n.style.setProperty("--rl-rgb", "var(--lab-" + key + "-rgb)");
    n.style.setProperty("--rl-rest", "var(--lab-" + key + "-rest)");
    n.style.setProperty("--rl-line", (cell && cell.line_px)
      ? cell.line_px + "px" : "var(--lab-" + key + "-line)");
    return n;
  }

  // The glow goes UNDER the icon art — it is light spilling out from behind the button, not a
  // wash over its face. The hairline goes over, because it is an edge.
  function readyItem(key, spec, cell, ability, index) {
    var item = bareItem(ability, cell.verdict || "below", { cues: cell.cues || [] });
    // These entries ask what the GLOW or the HAIRLINE says. The declared scan edge is a second
    // answer in the same frame and at icon size it is the louder one, so an entry may drop it and
    // be judged alone. ⚠ It strips `.ready-line`, the class `itemNode` appends for `rule.scan` —
    // this used to strip `.edge`, a class the DOM has not carried since the collapse, so every
    // readiness cell was silently judged with a 2px gold line composited over it.
    if (spec.inner_border === false) {
      var mark = item.querySelector(":scope > .ready-line");
      if (mark) mark.remove();
    }
    if (spec.draws === "ready-line") {
      item.appendChild(readyLine(key, cell));
    } else {
      item.insertBefore(readyGlow(key, spec, index), item.firstChild);
    }
    return item;
  }

  function readyRow(key, spec, cell) {
    var row = el("div", "ready-row");
    (cell.abilities || []).forEach(function (ability, i) {
      row.appendChild(readyItem(key, spec, cell, ability, i));
    });
    return row;
  }

  /* Part 7 · the font candidates for V15's hotkey text.
   *
   * The cell is a REAL row — same icon, same verdict, same badges — with the label overridden to
   * this entry's family and dials. Judging a font on its own line proves nothing: the question is
   * whether four characters survive the art under them and the badge beside them, and only a row
   * asks that. ⚠ Every family here is SUBSET to the keybind alphabet at build time, so the
   * advance widths are the real ones and the page still weighs what it weighed.
   */
  function hotkeyItem(key, spec, cell) {
    var item = bareItem(cell.ability, cell.verdict || "press", { cues: cell.cues || [] });
    var hk = item.querySelector(":scope > .hotkey");
    if (!hk) {
      hk = el("div", "hotkey");
      item.appendChild(hk);
    }
    hk.textContent = cell.key || "3";
    hk.style.setProperty("--hotkey-font", "var(--lab-" + key + "-hk-font)");
    hk.style.setProperty("--hotkey-size", "var(--lab-" + key + "-hk-size)");
    hk.style.setProperty("--hotkey-outline-px", "var(--lab-" + key + "-hk-outline)");
    if (spec.bar) {
      // A bar is a different object from a corner label, so it takes its own rule rather than
      // overloading `.hotkey`'s. Everything positional in that rule is overridden.
      hk.className = "hotkey hotkey-bar";
      hk.style.setProperty("--hotkey-bar", "var(--lab-" + key + "-hk-bar)");
      hk.style.setProperty("--hotkey-bar-h", "var(--lab-" + key + "-hk-bar-h)");
      hk.style.setProperty("--hotkey-bar-align", "var(--lab-" + key + "-hk-bar-align)");
      hk.style.setProperty("--hotkey-bar-rule", "var(--lab-" + key + "-hk-bar-rule)");
    }
    if (spec.plate) {
      hk.style.setProperty("--hotkey-plate", "var(--lab-" + key + "-hk-plate)");
      hk.style.setProperty("--hotkey-plate-x", "var(--lab-" + key + "-hk-plate-x)");
      hk.style.setProperty("--hotkey-plate-y", "var(--lab-" + key + "-hk-plate-y)");
    }
    return item;
  }

  var LAB_FONTS = D.lab_fonts || {};

  var LAB = T.lab || {};
  var labHost = document.getElementById("lab");
  var labKeys = Object.keys(LAB).filter(function (k) { return k.charAt(0) !== "_"; });

  if (!labKeys.length) {
    // An empty lab is a lab, not a defect — and the page should say so rather than render a
    // silent gap that reads as a missing section.
    var empty = el("div", "lab-empty");
    empty.innerHTML = "<b>The lab is currently empty.</b> Its two entries were promoted into " +
      "the declared style on 2026-08-13 and deleted from here, which is the only way a " +
      "treatment leaves the lab (Part 7, rule 4): <code>border-arrival</code> became the lane " +
      "border and its arrival snap, and <code>badge-slots</code> became the corner badges with " +
      "a negative-only cue vocabulary (which gained one positive cue on 2026-08-14 — see Part " +
      "0.5). Both are drawn above, as the style. The next idea gets a " +
      "<code>lab</code> key, an <code>asks</code>, and a section here.";
    labHost.appendChild(empty);
  } else {
    labKeys.forEach(function (key) {
      var spec = LAB[key];
      var e = labEntry(key, spec);
      // An entry with no cells is not half-authored: some treatments have no CSS analogue at
      // all — a four-strip ring being scaled is one — and those are drawn by the in-game
      // gallery instead. Say so, rather than leaving a gap that reads as a broken build.
      if (!(spec.cells || []).length) {
        var only = el("p", "asks");
        only.innerHTML = "<b>Drawn in the client only</b> — <code>/cap style</code>, under " +
          "<em>lab</em>. This treatment has no faithful CSS analogue, so the preview would be " +
          "an argument about the client rather than the client. See Part 7.";
        e.box.appendChild(only);
      }
      (spec.cells || []).forEach(function (cell) {
        var cap = cell.caption || "";
        if (cell.kind === "sheet") {
          e.row.appendChild(labCell(sheetSwatch(key), cap));
          return;
        }
        if (cell.kind === "row") {
          e.row.appendChild(labCell(readyRow(key, spec, cell), cap));
          return;
        }
        if (spec.draws === "hotkey") {
          var headK = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "press") +
                      "</code><br>";
          e.row.appendChild(labCell(hotkeyItem(key, spec, cell), headK + cap));
          return;
        }
        if (spec.draws === "flipbook") {
          var headF = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "below") +
                      "</code><br>";
          e.row.appendChild(labCell(flipbookItem(key, spec, cell), headF + cap));
          return;
        }
        if (spec.draws === "blaze") {
          var headB = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "below") +
                      "</code><br>";
          e.row.appendChild(labCell(blazeItem(key, spec, cell), headB + cap));
          return;
        }
        if (spec.draws === "ready-glow" || spec.draws === "ready-line") {
          var head1 = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "below") +
                      "</code><br>";
          e.row.appendChild(labCell(readyItem(key, spec, cell, cell.ability, 0),
                                    head1 + cap));
          return;
        }
        var head = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "below") +
                   "</code><br>";
        e.row.appendChild(labCell(stripedItem(key, cell), head + cap));
      });
      labHost.appendChild(e.box);
    });
  }

  document.getElementById("prov").innerHTML = D.provenance_html;

  // A build-time honesty flag: art drawn through a path we have not verified in client, or a
  // declared lane no ability in this catalog can actually draw.
  (D.notes || []).forEach(function (msg) {
    var n = el("div", "note");
    n.innerHTML = "⚠ " + msg;
    document.getElementById("state").parentNode.insertBefore(n, document.getElementById("state"));
  });

  render();
})();
