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
    // ⚠ THE THIRD ELIMINATING SIGNAL (render-shelf.md V17). `ruled-sealed` is a band the CLIENT
    // evaluated against a secret cap never saw. It draws the same stripe sheet, out of the same
    // FontString that draws the mark, so it reads exactly as ruled out — and it carries no cue,
    // because a cue is a badge cap shows and this is not one.
    if (rule.eliminates) ruledOut = true;
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

    // V12 · the virtual-row tick. PREVIEW ONLY, and it exists because this page compresses a
    // geometry the client does not have: in game a virtual row sits in cap's own panel, and that
    // physical separation is what says "cap owns this frame, the Cooldown Manager has no row for
    // it". One flat row loses the separation, so the tick carries the bit instead. It is CHROME
    // in the strictest sense -- it asserts nothing about the press, wears no polarity and takes
    // no part in either reading pass -- and it holds the bottom-left corner, which no badge
    // (top-right, flowing down) and no hotkey (top-left) can claim.
    if (entry.virtual) {
      var vm = el("div", "virtual-mark");
      vm.title = "cap-owned icon — this ability has no Cooldown Manager frame";
      item.appendChild(vm);
    }

    // The SEALED DISPLAYS (render-shelf.md V16-V19). Every one of them is art the client draws
    // from a rule cap authored and never reads back, so the preview draws the SHAPE and states
    // the value nowhere: a scenario names the sink, and what value the client found is exactly
    // the thing cap cannot know.
    (entry.sealed || []).forEach(function (kind) {
      item.appendChild(sealedNode(kind, entry));
    });

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
    if (entry.virtual) col.setAttribute("data-virtual", "1");
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
      (col.getAttribute("data-virtual")
        ? "<span class=\"tip-cues\">virtual row — cap-owned icon, no CDM frame</span>" : "") +
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

  /* ------------------------------------------------------------------ page sections
   *
   * ONE script serves TWO pages: a spec's scenario stepper and the lab. Each section renders only
   * where its host exists, so a spec page carries no lab markup and the lab page carries no
   * scenario stepper — which is the whole point of splitting them, since the lab was the larger
   * half of every spec page and was duplicated into all of them.
   *
   * A section this page does not have gets a DETACHED node instead of a null, so the code that
   * fills it neither branches nor throws. A missing host is a page boundary, never an error.
   * ⚠ `document.createElement`, not `el()` — a class name here would be a class the stylesheet
   * has no rule for, which is exactly what `smoke_dom` fails on.
   */
  var DETACHED = document.createElement("div");
  function host(id) { return document.getElementById(id) || DETACHED; }

  /* ------------------------------------------------------------------ the stepper */

  var pick = host("pick");
  var rowEl = host("row");
  var walkEl = host("walk");
  var stateEl = host("state");
  var extrasEl = host("extras");

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
      // An `⚠ UNSURE` bullet is a claim the authoring docs themselves doubt, and the whole point
      // of this page is that the author can SEE those without reading the markdown. So it draws
      // as a block, not as a grey footnote. The label carries it -- no separate field -- because
      // the doc grammar already has exactly one place to put a label and inventing a second
      // would put the loudness somewhere the doc cannot state it.
      if (x.label.indexOf("⚠ UNSURE") === 0) n.setAttribute("data-unsure", "1");
      n.innerHTML = "<b>" + x.label + ".</b> " + x.html;
      extrasEl.appendChild(n);
    });
  }

  pick.addEventListener("change", function () { current = +pick.value; step = 0; render(); });
  host("next").addEventListener("click", function () {
    var sc = D.scenarios[current];
    step = Math.min(step + 1, sc.steps.length);
    render();
  });
  host("prev").addEventListener("click", function () {
    step = Math.max(step - 1, 0); render();
  });
  host("all").addEventListener("click", function () { step = 0; render(); });
  host("zoom").addEventListener("click", function () {
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

  // One bare row item, shared by the gallery's swatches AND the lab's cell builders — so a
  // swatch, a lab cell and a live row can never diverge. It lives HERE, not in gallery.js,
  // because the lab page ships without the gallery.
  function bareItem(name, verdict, opts) {
    opts = opts || {};
    return itemNode({ name: name, verdict: verdict, cues: opts.cues,
                      sealed: opts.sealed, count: opts.count,
                      outside: opts.outside, full: opts.full }, 0).firstChild;
  }

  /*__GALLERY_JS__*/

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

  /* One sealed display, drawn as the shape it is rather than at a value it cannot have.
   *
   *   count-bands    — V16/V17. The plate and the mark the fired band names, in the corner. When
   *                    the row is `ruled-sealed` the hatch above is the same band's other escape,
   *                    which is why nothing extra is drawn for it here.
   *   count-bar      — V18. The radial, inside the badge plate. Drawn at a nominal fraction: a
   *                    bar has no blank state, so "there is an arc here" is the whole claim.
   *   pandemic — V19. The badge the client shows and hides on Blizzard's own window.
   */
  function sealedNode(kind, entry) {
    var negative = entry.verdict === "ruled-sealed";
    if (kind === "count-bar") {
      /* V18: the segmented bar on the row's bottom edge. A scenario states "there is a bar
       * here", never a value, so the fill is a nominal 2-of-4 — full (and the whole-bar red
       * flip, a second slot's count band at threshold = max) only where a swatch passes
       * `full` to demonstrate it. */
      var sbMax = 4;
      var sb = el("div", "sealed-bar");
      var sbFill = el("div", "sealed-bar-fill");
      sbFill.style.width = (entry.full ? 100 : 50) + "%";
      sb.appendChild(sbFill);
      for (var sbi = 1; sbi < sbMax; sbi++) {
        var tick = el("div", "sealed-bar-seg");
        tick.style.left = (100 * sbi / sbMax).toFixed(1) + "%";
        sb.appendChild(tick);
      }
      if (entry.full) sb.appendChild(el("div", "sealed-bar-full"));
      return sb;
    }
    if (kind === "pandemic") {
      /* The pair's OTHER state: aura up, OUTSIDE the window — the gold do-not-refresh hatch,
       * off SetDurationText bands on remaining seconds. Catalog threshold, client badge (V19). */
      if (entry.outside) {
        var orun = el("div", "sealed sealed-run");
        var oh = el("div", "sealed-band-hatch");
        oh.style.setProperty("--sx-ink", "var(--pd-rgb)");
        var ost = D.lab_stripes;
        if (ost) {
          oh.style.webkitMaskImage = oh.style.maskImage = "url(" + ost.uri + ")";
        }
        orun.appendChild(oh);
        return orun;
      }
      var w = el("div", "sealed sealed-pandemic");
      /* The FULL positive-cue treatment — V14's promotion ring AND the halo — because this
       * badge is a client-decided promotion and must read as bright as one. Both are armed
       * BEFORE the handover in the client (§3.5.3). */
      w.appendChild(promoRing());
      w.appendChild(el("div", "sealed-pd-glow"));
      w.appendChild(el("div", "sealed-plate"));
      var wm = el("div", "sealed-mark");
      var wa = (D.frames || {})[T.pandemic.frame];
      if (wa && wa.uri) wm.style.webkitMaskImage = wm.style.maskImage = "url(" + wa.uri + ")";
      wm.style.setProperty("--sx-ink", "var(--pd-rgb)");
      w.appendChild(wm);
      return w;
    }

    /* count-bands. ONE SLOT PER ELEMENT — the hatch across the face, and ON THE CORNER either
     * the mark or the numeral, never both. Each is its own AuraContainer slot with its own
     * button, FontString and band table (`Channel.CountElements`), so nothing here shares an
     * advance width with anything.
     *
     * ⚠ `count` and `mark` are exclusive in the band vocabulary, and this is where you can see
     * why: they are anchored on the same badge corner in the same polarity hue, so a band asking
     * for both draws a digit on top of a glyph. `entry.count` picks which one this row states.
     */
    var run = el("div", "sealed sealed-run");
    /* The hatch draws for the ELIMINATING direction only (V16, 2026-08-24): a hatch means
     * "ruled out" — a gold hatch on the positive direction was a contradiction wearing pixels. */
    if (negative) {
      var hatch = el("div", "sealed-band-hatch");
      hatch.style.setProperty("--sx-ink", "var(--count-low)");
      // Same sheet, same call-time resolution, same reason as `maskedStripe`: `D.lab_stripes` is
      // a build-time data: URI and a module-scope hoist of it is still undefined when the gallery
      // runs. Without it this layer is a flat field of the escape's colour over the whole icon.
      var stripes = D.lab_stripes;
      if (stripes) {
        hatch.style.webkitMaskImage = hatch.style.maskImage = "url(" + stripes.uri + ")";
      }
      run.appendChild(hatch);
    }

    if (entry.count != null) {
      // The plate is its OWN element/slot (V16, 2026-08-24): a plate escape cannot sit under
      // text within one string. Same thresholds; the client blanks both together.
      var pbadge = el("div", "sealed-band-badge");
      pbadge.appendChild(el("div", "sealed-plate"));
      run.appendChild(pbadge);
      // The numeral, which is the client's `%d` — the one element that can never be a baked crop,
      // and the one the shelf lets a colour escape reach, because it is text.
      var n = el("div", "sealed-band-count");
      n.textContent = String(entry.count);
      n.style.setProperty("--sx-ink", negative ? "var(--count-low)" : "var(--count-rgb)");
      run.appendChild(n);
    } else {
      var badge = el("div", "sealed-band-badge");
      badge.appendChild(el("div", "sealed-plate"));
      var mark = el("div", "sealed-mark");
      var art = (D.frames || {})[T.count.mark];
      if (art && art.uri) mark.style.webkitMaskImage = mark.style.maskImage = "url(" + art.uri + ")";
      mark.style.setProperty("--sx-ink", negative ? "var(--count-low)" : "var(--count-rgb)");
      badge.appendChild(mark);
      run.appendChild(badge);
    }
    return run;
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

  /* Part 7 · a secret aura APPLICATION COUNT reaching a pixel.
   *
   * Two renderers, because the client offers two genuinely different sinks for the same fact.
   *
   * `countItem` is the NumericRuleFormatter route: cap authors a breakpoint table, the client
   * evaluates it against the sealed count and calls SetText with the result. This function does
   * exactly what `ApplyApplicationCount` does — pick the highest breakpoint whose threshold the
   * value reaches, clamp, format — because that is the only way the cell can be an argument
   * about the client rather than about this file.
   *
   * ⚠ The value is drawn from the cell, never read back from anything. In the client the number
   * is SECRET: cap hands over a rule and never learns which band fired. A cell says "at 4
   * stacks" so a reader can judge the look; it is not a claim cap can know that.
   */
  function bandFor(bands, value) {
    var hit = null;
    (bands || []).forEach(function (b) {
      if (value >= b.threshold && (!hit || b.threshold >= hit.threshold)) hit = b;
    });
    return hit;
  }

  function bandText(bands, value) {
    var b = bandFor(bands, value);
    if (!b) return { text: "", rgb: null };
    var v = value;
    if (b.step) v = Math.round(v / b.step) * b.step;
    if (b.min != null && v < b.min) v = b.min;
    if (b.max != null && v > b.max) v = b.max;
    // The client's own colour escape, resolved the way the client resolves it. The hue lives in
    // the band's format string because that is where cap has to put it -- the count sink adds
    // Text and Shown and never VertexColor, so per-band hue has nowhere else to go.
    var rgb = null;
    var fmt = b.format || "";
    var esc = fmt.match(/^\|c[fF]{2}([0-9a-fA-F]{6})(.*)\|r$/);
    if (esc) {
      rgb = "#" + esc[1];
      fmt = esc[2];
    }
    return { text: fmt.replace("%d", String(v)), rgb: rgb };
  }

  /* `countMarkItem` is the same formatter, with a TEXTURE ESCAPE in the band instead of a
   * numeral. Measured 2026-08-21: `|T…|t` and `|A:…|a` inside a band's `format` RENDER as art.
   *
   * ⚠ The interesting cells are the COMPOSITED ones. A plate cap draws is an ordinary texture
   * with no sink on it, so it draws at every value including the ones the band blanks (see the
   * `place: "badge"` cells in L1). But the escape may name art that ALREADY CONTAINS the plate —
   * one crop, disc and glyph together — and then the plate's visibility rides the band for free.
   * That is the difference between a badge that appears and a badge that is always there and
   * sometimes has a glyph in it.
   */
  // ⚠ ALL escapes, not the first. One format string may carry several -- the long form takes
  // `:xoff:yoff` after the size, which is how a real UI places more than one mark in one
  // FontString instead of letting them flow side by side. So "hatch the whole icon AND put a
  // badge in the corner" is ONE band, not two sinks: there is only one count FontString per
  // button and it has to carry everything the count says.
  var ESCAPE = /\|[AT]:?([A-Za-z0-9_\\/.-]+):(\d+):(\d+)(?::(-?\d+):(-?\d+))?[^|]*\|[at]/g;

  function marksFromFormat(fmt) {
    var out = [], rest = fmt, m;
    ESCAPE.lastIndex = 0;
    while ((m = ESCAPE.exec(fmt)) !== null) {
      out.push({ frame: m[1].split(/[\\/]/).pop(), h: +m[2], w: +m[3] });
      rest = rest.replace(m[0], "");
    }
    return { marks: out, rest: rest };
  }

  function countMarkItem(key, spec, cell) {
    var item = bareItem(cell.ability, cell.verdict || "below", { cues: cell.cues || [] });
    // The BAND INPUT is whatever the sink is driven by. The count sinks band on
    // `auraData.applications`; `SetDurationText` bands on a DurationTextBindingProperty --
    // RemainingPercent here -- through the same NumericFormatter object. One renderer, because
    // it is one formatter: what changes is which sealed number the client feeds it.
    var value = (cell.remaining_pct != null) ? cell.remaining_pct : cell.stacks;
    var b = bandFor(cell.bands, value);
    var fmt = (b && b.format) || "";
    var parsed = marksFromFormat(fmt);
    var corner = [];
    parsed.marks.forEach(function (mk) {
      // The hatch sheet is a mark like any other -- it is just 56x56 and centred, so it covers
      // the icon instead of sitting on a corner. Nothing about the sink changes; only the size
      // in the escape does. This is why "hatch the row" needs no extra layer and no second
      // frame: it is one more texture a band can name.
      if (mk.frame === "stripes") item.appendChild(skipLayer());
      else corner.push(mk);
    });

    var host = el("div", cell.place === "badge" ? "mark-slot" : "mark-centre");
    if (cell.composited) host.classList.add("composited");
    if (cell.motion === "pulse") {
      host.classList.add("pulsing");
      host.style.setProperty("--mk-dur", "var(--lab-" + key + "-cg-pulse-dur)");
      host.style.setProperty("--mk-a0", "var(--lab-" + key + "-cg-pulse-a0)");
      host.style.setProperty("--mk-a1", "var(--lab-" + key + "-cg-pulse-a1)");
      host.style.setProperty("--mk-scale", "var(--lab-" + key + "-cg-pulse-scale)");
    }
    host.style.setProperty("--mk-size", "var(--lab-" + key + "-cg-size)");
    host.style.setProperty("--mk-rgb", cell.alt_hue
      ? "var(--lab-" + key + "-cg-alt)" : "var(--lab-" + key + "-cg-rgb)");

    corner.forEach(function (mk) {
      var art = (D.frames || {})[mk.frame];
      var sprite = el("div", "mark-sprite");
      if (art && art.uri) {
        sprite.style.webkitMaskImage = sprite.style.maskImage = "url(" + art.uri + ")";
      }
      host.appendChild(sprite);
    });
    // A band may carry BOTH — `"%d|T…|t"` was accepted and drawn. The numeral sits beside the
    // mark rather than under it, because a band that says "5, and here is the mark" is one
    // statement.
    var textPart = parsed.rest;
    if (textPart) {
      var n = el("div", "mark-text");
      n.textContent = textPart.replace("%d", String(value));
      n.style.setProperty("--cn-size", "var(--lab-" + key + "-cg-size)");
      n.style.setProperty("--cn-outline", "1px");
      n.style.setProperty("--cn-rgb", "var(--lab-" + key + "-cg-rgb)");
      host.appendChild(n);
    }
    // ⚠ EMPTY IS A RESULT. A band drawing nothing appends the host anyway, so a composited cell
    // at a resting value shows an EMPTY CORNER rather than an empty disc -- which is the whole
    // finding and would be invisible if the host were skipped.
    if (!corner.length && !textPart) host.classList.add("blank");
    item.appendChild(host);
    return item;
  }

  /* `pandemicItem` is the odd one out and the only sink where the CLIENT owns visibility.
   * `AddPandemicRegion(region)` takes any Region -- a Frame with children included -- seals its
   * `Shown`, and calls SetShown(inPandemicWindow) every frame off Blizzard's own
   * GetRefreshExtendedDuration - GetAuraBaseDuration. So cap authors NO threshold, and every
   * treatment below is cap-owned art whose only sealed property is whether it is on screen.
   */
  function pandemicItem(key, spec, cell) {
    var item = bareItem(cell.ability, cell.verdict || "below", { cues: cell.cues || [] });
    if (!cell.in_window) {
      // The out-of-window cell draws the row with nothing added, which is the correct picture:
      // the client has hidden the region, and a hidden region is not a faint one.
      var off = el("div", "pd-off");
      item.appendChild(off);
      return item;
    }
    var shape = cell.shape || "wash";
    var n = el("div", "pd-" + shape);
    n.style.setProperty("--pd-rgb", "var(--lab-" + key + "-pd-rgb)");
    n.style.setProperty("--pd-wash", "var(--lab-" + key + "-pd-wash)");
    n.style.setProperty("--pd-edge", "var(--lab-" + key + "-pd-edge)");
    n.style.setProperty("--pd-foot", "var(--lab-" + key + "-pd-foot)");
    n.style.setProperty("--pd-size", "var(--lab-" + key + "-pd-size)");
    if (cell.motion === "pulse") {
      n.classList.add("pulsing");
      n.style.setProperty("--mk-dur", "var(--lab-" + key + "-pd-pulse-dur)");
      n.style.setProperty("--mk-a0", "var(--lab-" + key + "-pd-pulse-a0)");
      n.style.setProperty("--mk-a1", "var(--lab-" + key + "-pd-pulse-a1)");
    }
    if (shape === "badge") {
      var art = (D.frames || {})[cell.frame];
      var sp = el("div", "mark-sprite");
      sp.style.setProperty("--mk-rgb", "var(--lab-" + key + "-pd-rgb)");
      if (art && art.uri) sp.style.webkitMaskImage = sp.style.maskImage = "url(" + art.uri + ")";
      n.appendChild(sp);
    }
    item.appendChild(n);
    return item;
  }

  /* `compositeItem` draws a row wearing SEVERAL sinks at once, which is the only way to judge
   * whether a design survives contact with a real row. Each layer names the sink that would
   * draw it in the client, because the point of the cell is the combination and not the parts:
   *
   *   hatch  -> a 56x56 texture escape in the count FontString's band
   *   arc    -> SetApplicationBar (or SetDurationBar) in Radial render mode
   *   ring   -> a full static crop from the count band, covering the arc when the threshold IS
   *             the maximum -- which is why no texture ever has to crop angularly
   *   mark   -> a composited plate+glyph crop from the same band
   *   count  -> `%d` in the same band, beside the mark
   *   absent -> the aura is not up, so the CLIENT has hidden the button and no sink draws
   */
  function compositeItem(key, spec, cell) {
    var item = bareItem(cell.ability, cell.verdict || "below", { cues: cell.cues || [] });
    var v = function (h) { return "var(--lab-" + key + "-cx-" + h + ")"; };

    if (cell.absent) {
      item.classList.add("cx-absent");
      // The hatch for an absent aura is cap's OWN frame on the readable `aura` latch, not a
      // sink -- so it is drawn here even though everything else on the row is not.
      if (cell.hatch) item.appendChild(maskedStripe("stripes skip-hatch", v(cell.hatch),
                                                    "var(--hatch-skip-phase)"));
      return item;
    }
    if (cell.hatch) {
      item.appendChild(maskedStripe("stripes skip-hatch", v(cell.hatch),
                                    "var(--hatch-skip-phase)"));
    }

    var slot = el("div", "cx-slot");
    var any = false;
    // The PLATE goes down first whenever anything occupies the corner. Every badge on a cap row
    // wears one -- light art over busy icon work washes out, and contrast is the cheap fix --
    // so an arc badge that skipped it was the odd one out and looked like a floating ring.
    if (cell.arc || cell.ring || cell.mark || cell.count != null || cell.plate) {
      slot.appendChild(el("div", "cx-plate"));
      any = true;
    }
    if (cell.arc) {
      var arc = el("div", "cx-arc");
      arc.style.setProperty("--cx-inset", v("arc-inset"));
      arc.style.setProperty("--cx-hue", v(cell.arc.hue));
      arc.style.setProperty("--cx-track", v("arc-track"));
      arc.style.setProperty("--cx-frac", cell.arc.pct + "%");
      slot.appendChild(arc); any = true;
    }
    if (cell.ring) {
      var ring = el("div", "cx-ring");
      ring.style.setProperty("--cx-hue", v(cell.ring));
      ring.style.setProperty("--cx-inset", v("arc-inset"));
      slot.appendChild(ring); any = true;
    }
    if (cell.mark) {
      var host = el("div", "cx-mark");
      var art = (D.frames || {})[cell.mark.frame];
      var sp = el("div", "mark-sprite");
      sp.style.setProperty("--mk-rgb", v(cell.mark.hue));
      sp.style.setProperty("--cx-size", v("size"));
      if (art && art.uri) sp.style.webkitMaskImage = sp.style.maskImage = "url(" + art.uri + ")";
      host.appendChild(sp);
      slot.appendChild(host); any = true;
    }
    if (cell.count != null) {
      var n = el("div", "cx-count");
      n.textContent = String(cell.count);
      n.style.setProperty("--cx-size", v("size"));
      n.style.setProperty("--cx-ink", v(cell.count_hue || "ink"));
      slot.appendChild(n); any = true;
    }
    // The pulse rides the SLOT, so everything gated by the band breathes together on one clock.
    // Two loops at different rates on one row read as malfunction.
    if (cell.pulse) {
      slot.classList.add("pulsing");
      slot.style.setProperty("--mk-dur", v("pulse-dur"));
      slot.style.setProperty("--mk-a0", v("pulse-a0"));
      slot.style.setProperty("--mk-a1", v("pulse-a1"));
      slot.style.setProperty("--mk-scale", v("pulse-scale"));
    }
    if (any) item.appendChild(slot);
    return item;
  }

  function countItem(key, spec, cell) {
    var item = bareItem(cell.ability, cell.verdict || "below", { cues: cell.cues || [] });
    var n = el("div", "count-band");
    var out = bandText(cell.bands, cell.stacks);
    n.textContent = out.text;
    n.style.setProperty("--cn-size", "var(--lab-" + key + "-cn-size)");
    n.style.setProperty("--cn-outline", "var(--lab-" + key + "-cn-outline)");
    // Three hue sources, in the order the client resolves them: a band's own escape wins, then a
    // cell's static SetTextColor, then the entry's default. A cell drawing nothing keeps whatever
    // it would have had -- an empty string has no colour to argue about.
    n.style.setProperty("--cn-rgb", out.rgb ? out.rgb
      : cell.static_rgb ? rgbCss(cell.static_rgb)
      : "var(--lab-" + key + "-cn-rgb)");
    if (cell.size_px) n.style.setProperty("--cn-size", cell.size_px + "px");
    // `place: "badge"` puts the string inside the badge stack's own disc, at the badge stack's
    // own corner. The plate is a plain cap texture with no sink on it -- so unlike the numeral
    // it cannot be driven by the sealed count, and it draws at every value including the ones
    // the band blanks. A cell at a blanked value is drawn for exactly that reason.
    if (cell.place === "badge") {
      var disc = el("div", "count-plate");
      disc.appendChild(n);
      item.appendChild(disc);
      return item;
    }
    item.appendChild(n);
    return item;
  }

  /* `countBarItem` is SetApplicationBar: the client sets min/max from cap's authored
   * `maxApplications` and SetValue's the sealed count into it. The fill is a texture cap chose,
   * which is why this is the only count route that reaches a SHAPE rather than a numeral.
   *
   * ⚠ It has no blank state and the cells are written to show that. SetValue clamps into
   * [0, max], so at zero the track is still drawn -- there is no band, no complement, and no
   * "nothing until N". That is the trade against the formatter, and it is the whole question.
   */
  function countBarItem(key, spec, cell) {
    var item = bareItem(cell.ability, cell.verdict || "below", { cues: cell.cues || [] });
    var max = Math.max(cell.max || 1, 1);
    var frac = Math.min(Math.max((cell.stacks || 0) / max, 0), 1);
    // Three shapes, and the third is a different RENDER MODE rather than a different look:
    // Radial drives the texture's radial progress percent instead of moving its anchors. Same
    // SetValue, same sealed BarValue, an arc instead of a waterline.
    if (cell.shape === "radial") {
      var arc = el("div", "count-radial");
      arc.style.setProperty("--cb-rgb", "var(--lab-" + key + "-cb-rgb)");
      arc.style.setProperty("--cb-track", "var(--lab-" + key + "-cb-track)");
      arc.style.setProperty("--cb-frac", (frac * 100).toFixed(1) + "%");
      item.appendChild(arc);
      return item;
    }
    if (cell.shape === "ring") {
      // The arc drawn as a RING around the whole icon rather than as a corner disc: the same
      // radial render mode, hung on the perimeter, where it competes with the badge stack for
      // nothing. ⚠ It competes with V13's scan edge for the border instead.
      var ring = el("div", "count-ring");
      ring.style.setProperty("--cb-rgb", "var(--lab-" + key + "-cb-rgb)");
      ring.style.setProperty("--cb-track", "var(--lab-" + key + "-cb-track)");
      ring.style.setProperty("--cb-ring", "var(--lab-" + key + "-cb-ring)");
      ring.style.setProperty("--cb-frac", (frac * 100).toFixed(1) + "%");
      item.appendChild(ring);
      return item;
    }
    var track = el("div", cell.shape === "disc" ? "count-disc" : "count-bar-track");
    track.style.setProperty("--cb-h", "var(--lab-" + key + "-cb-h)");
    track.style.setProperty("--cb-track", "var(--lab-" + key + "-cb-track)");
    var fill = el("div", "count-fill");
    fill.style.setProperty("--cb-rgb", "var(--lab-" + key + "-cb-rgb)");
    fill.style.setProperty("--cb-frac", (frac * 100).toFixed(1) + "%");
    if (cell.banded) {
      /* The full-state hue baked into the fill art's last cell: the bar CROPS its texture
       * [client 2026-08-21], so the tip is revealed only at max. */
      fill.classList.add("banded");
      var sheet = el("div", "count-fill-sheet");
      sheet.style.setProperty("--cb-full", "var(--lab-" + key + "-cb-full)");
      sheet.style.setProperty("--cb-tip", (100 * (max - 1) / max).toFixed(1) + "%");
      if (frac > 0) sheet.style.width = (10000 / (frac * 100)).toFixed(1) + "%";
      fill.appendChild(sheet);
    }
    track.appendChild(fill);
    if (cell.segments) {
      // cap's own track art: one tick per application boundary. Nothing sealed touches it.
      for (var si = 1; si < max; si++) {
        var seg = el("div", "count-seg");
        seg.style.left = (100 * si / max).toFixed(1) + "%";
        track.appendChild(seg);
      }
    }
    item.appendChild(track);
    if (cell.overlay && frac >= 1) {
      /* The WHOLE-BAR flip at full: a second slot's count band drawing a full-width crop at
       * threshold = max — V16's machinery, the client deciding. */
      var over2 = el("div", "count-full-overlay");
      over2.style.setProperty("--cb-h", "var(--lab-" + key + "-cb-h)");
      over2.style.setProperty("--cb-full", "var(--lab-" + key + "-cb-full)");
      item.appendChild(over2);
    }
    return item;
  }

  function rgbCss(t) {
    return "rgba(" + Math.round(t[0] * 255) + "," + Math.round(t[1] * 255) + "," +
           Math.round(t[2] * 255) + ",1)";
  }

  var LAB_FONTS = D.lab_fonts || {};

  var LAB = T.lab || {};
  var labHost = host("lab");
  var labKeys = Object.keys(LAB).filter(function (k) { return k.charAt(0) !== "_"; });

  if (!labKeys.length) {
    // An empty lab is a lab, not a defect — and the page should say so rather than render a
    // silent gap that reads as a missing section.
    var empty = el("div", "lab-empty");
    empty.innerHTML = "<b>The lab is empty, and that is its correct resting state.</b> " +
      "Everything it held has either been promoted into the declared style — the only way a " +
      "treatment leaves (Part 7, rule 4) — or deleted because the question it asked got an " +
      "answer. <code>V2</code>, <code>V5</code>, <code>V11</code>, <code>V13</code>, " +
      "<code>V14</code> and <code>V15</code> were all chosen here and are drawn above, as the " +
      "style. Part 7 keeps the ledger of what left and where it went; <code>git log</code> " +
      "keeps the entries themselves with their <code>asks</code> intact, which is where a " +
      "revived idea should be read from. The next idea gets a <code>lab</code> key, an " +
      "<code>asks</code>, and a section here.";
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
        if (spec.draws === "count") {
          var headC = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "below") +
                      "</code> · at <b>" + cell.stacks + "</b> stacks<br>";
          e.row.appendChild(labCell(countItem(key, spec, cell), headC + cap));
          return;
        }
        if (spec.draws === "count-glyph") {
          var headCG = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "below") +
                       "</code> · at <b>" + cell.stacks + "</b> stacks<br>";
          e.row.appendChild(labCell(countMarkItem(key, spec, cell), headCG + cap));
          return;
        }
        if (spec.draws === "composite") {
          var headX = "<b>" + cell.ability + "</b> · <code>" + (cell.state || "") + "</code><br>";
          e.row.appendChild(labCell(compositeItem(key, spec, cell), headX + cap));
          return;
        }
        if (spec.draws === "duration") {
          var headD = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "below") +
                      "</code> · <b>" + cell.remaining_pct + "%</b> of its duration left<br>";
          e.row.appendChild(labCell(countMarkItem(key, spec, cell), headD + cap));
          return;
        }
        if (spec.draws === "pandemic") {
          var headPD = "<b>" + cell.ability + "</b> · <code>" +
                       (cell.in_window ? "IN the pandemic window" : "outside it") + "</code><br>";
          e.row.appendChild(labCell(pandemicItem(key, spec, cell), headPD + cap));
          return;
        }
        if (spec.draws === "count-bar") {
          var headCB = "<b>" + cell.ability + "</b> · <code>" + (cell.verdict || "below") +
                       "</code> · <b>" + cell.stacks + "</b> of <b>" + cell.max +
                       "</b><br>";
          e.row.appendChild(labCell(countBarItem(key, spec, cell), headCB + cap));
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

  host("prov").innerHTML = D.provenance_html;

  // A build-time honesty flag: art drawn through a path we have not verified in client, or a
  // declared lane no ability in this catalog can actually draw.
  (D.notes || []).forEach(function (msg) {
    var n = el("div", "note");
    n.innerHTML = "⚠ " + msg;
    var anchor = document.getElementById("state");
    if (anchor) anchor.parentNode.insertBefore(n, anchor);
  });

  // The honest condition, rather than a test on which page this is: with no scenarios there is
  // nothing to walk, and the lab page ships none.
  if (D.scenarios.length) render();
})();
