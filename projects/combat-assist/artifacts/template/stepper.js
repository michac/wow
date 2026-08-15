/* Combat Assist Plus — artifact behavior.
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

  function badgeNode(key) {
    var cue = T.cues[key] || {};
    var slot = el("div", "slot");
    slot.setAttribute("data-slot", String(cue.slot || 1));
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

  /* ------------------------------------------------------------------ one CDM item */

  function itemNode(entry, index) {
    var ab = D.abilities[entry.name] || {};
    // `border` is the lane that actually DRAWS — the CHARGES substitution has already been
    // applied by capart off the catalog's charge column. `lane` is still the authored role
    // lane; the artifact shows both so the substitution is visible rather than silent.
    var lane = ab.border || ab.lane || "FALLBACK";
    var rule = T.verdicts[entry.verdict] || {};
    var laneTok = T.lanes[lane] || T.lanes.FALLBACK;

    var item = el("div", "item");
    item.style.setProperty("--lane-color", rgb(laneTok.rgb));
    item.style.setProperty("--lane-px", laneTok.thickness_px + "px");

    var art = el("div", "art");
    if (ab.icon) art.style.backgroundImage = "url(" + ab.icon + ")";
    item.appendChild(art);

    if (rule.swipe) item.appendChild(el("div", "swipe"));
    if (rule.veil) item.appendChild(el("div", "veil"));

    // Every non-`cd` row wears its lane border. `press`, `press-promoted` and `below` render
    // IDENTICALLY, and that is the point: the press is "the leftmost thing not ruled out", not
    // a thing cap draws (render-shelf.md Part 0.5).
    if (rule.border) item.appendChild(el("div", "edge"));

    var open = false;
    var cues = (rule.cues || []).concat(entry.cues || []);
    cues.slice(0, T.badges.slots.length).forEach(function (k) {
      if ((T.cues[k] || {}).open) open = true;
      item.appendChild(badgeNode(k));
    });
    if (open) item.setAttribute("data-open", "1");

    var col = el("div", "lane");
    col.appendChild(item);
    var cap = el("div", "caption"); cap.textContent = entry.name; col.appendChild(cap);
    var v = el("div", "verdict"); v.textContent = entry.verdict; col.appendChild(v);
    return col;
  }

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

  // V2 · the four lane borders. `lane_sample` names an ability whose ART to borrow; the border
  // is forced here because this swatch is ABOUT the lane. Where the sample ability would draw a
  // different border in a real row (the CHARGES substitution), the caption says so.
  Object.keys(T.lanes).forEach(function (lane) {
    var tok = T.lanes[lane];
    var name = D.lane_sample[lane];
    var ab = D.abilities[name] || {};
    var note = "solid " + tok.thickness_px + "px, static — no pulse, no ring";
    if (ab.border && ab.border !== lane) {
      note += ". <b>⚠ " + name + " draws " + ab.border + " in a real row</b> (it has " +
              ab.charges + " charges); the art is borrowed, the lane is forced.";
    } else if (lane === "CHARGES") {
      note += ". " + name + " is authored <b>" + ab.lane + "</b> and renders CHARGES because the " +
              "client reports " + ab.charges + " charges — the substitution, not a re-authoring.";
    }
    gallery.appendChild(swatch("lane · " + lane, note, function () {
      var node = bareItem(name, "press");
      node.style.setProperty("--lane-color", rgb(tok.rgb));
      node.style.setProperty("--lane-px", tok.thickness_px + "px");
      return node;
    }));
  });

  // V2 · the arrival snap. Artifact chrome: the addon fires this ON THE EVENT and stops. Here a
  // timer stands in for the event so it can be watched — which is why the interval lives under
  // `tokens.artifact` and not in the style.
  var ARRIVING = [];
  gallery.appendChild(swatch(
    "arrival snap",
    "the ONE piece of motion in the style: " + T.arrival.from_scale + "× → 1× over " +
      T.arrival.duration_s + "s (" + T.arrival.smoothing + "), fired when something " +
      "<b>arrives</b> — a cooldown finishes, a charge returns, a spender becomes affordable. " +
      "Replayed every " + T.artifact.arrival_replay_s + "s here <em>only</em> so it can be seen.",
    function () {
      var strip = el("div", "swatch-stage");
      Object.keys(T.lanes).forEach(function (lane) {
        var node = bareItem(D.lane_sample[lane], "press");
        var tok = T.lanes[lane];
        node.style.setProperty("--lane-color", rgb(tok.rgb));
        node.style.setProperty("--lane-px", tok.thickness_px + "px");
        var e = node.querySelector(".edge");
        if (e) ARRIVING.push(e);
        strip.appendChild(node);
      });
      return strip;
    }
  ));
  (function () {
    function fire() {
      ARRIVING.forEach(function (e, i) {
        e.removeAttribute("data-anim");
        void e.offsetWidth;                                  // restart the animation
        setTimeout(function () { e.setAttribute("data-anim", "1"); }, i * 120);
      });
    }
    fire();
    setInterval(fire, T.artifact.arrival_replay_s * 1000);
  })();

  gallery.appendChild(swatch("veil", "de-emphasis at alpha " + T.veil.alpha +
    " — the veil says <b>skip</b>; a badge says <b>why</b>",
    function () { return bareItem(D.lane_sample.ROTATION, "withheld"); }));
  gallery.appendChild(swatch("swipe", "Blizzard's own dial — cap draws nothing here, and does " +
    "not restyle it. The cheapest possible “ruled out”.",
    function () { return bareItem(D.lane_sample.COOLDOWN, "cd"); }));

  // V5 · one swatch per cue, then the full three slots, so "do three badges crowd the face?"
  // is answerable rather than asserted.
  var cueKeys = Object.keys(T.cues);
  cueKeys.forEach(function (key) {
    var cue = T.cues[key];
    gallery.appendChild(swatch(
      "cue · " + key + (cue.open ? " ⚠" : ""),
      (cue.open ? "<b>declared, unverified in client — produces no hint yet.</b> " : "") +
        cue.means + " <em>(slot " + cue.slot + ", " + cue.frames.length + " frames @ " +
        cue.duration_s + "s " + cue.loop + ")</em>",
      function () { return bareItem(D.lane_sample.ROTATION, "below", { cues: [key] }); }
    ));
  });

  // One cue per DISTINCT slot, not the first N cues: `starved` and `overcap` deliberately share
  // slot 2 (they are the same question about the same resource, and never co-occur), so taking
  // the first three would stack two badges in one place and draw only two. This swatch exists to
  // answer "do three badges crowd the face?", which it cannot do while showing two.
  var perSlot = [];
  T.badges.slots.forEach(function (s) {
    var k = cueKeys.filter(function (c) { return T.cues[c].slot === s.id; })[0];
    if (k) perSlot.push(k);
  });
  gallery.appendChild(swatch("badges · all three slots",
    T.badges.slots.length + " is the ceiling the shelf sets. If a fourth slot wants in, one of " +
    "the three is not earning its place. Shown: " + perSlot.join(" · ") + " — one per slot, so " +
    "the crowding question is answerable. Slot 3 is the positive cue's, and reads gold.",
    function () { return bareItem(D.lane_sample.ROTATION, "below", { cues: perSlot }); }));

  // A badge overhanging the corner can collide with the next icon. That is arithmetic, and
  // arithmetic in a caption is an assertion; drawn in a real row it is a finding.
  var over = T.badges.overhang_px, gap = T.surfaces.row_gap_px;
  gallery.appendChild(swatch("badges · in a real row",
    "overhangs <b>" + over + "px</b> past the edge; the row gap is <b>" + gap + "px</b>" +
      (over > gap ? " — <b>they collide.</b>" : " — <b>they clear.</b>"),
    function () {
      var strip = el("div", "swatch-stage");
      ["COOLDOWN", "ROTATION", "FALLBACK"].forEach(function (lane, i) {
        strip.appendChild(bareItem(D.lane_sample[lane], "below",
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
  var head = "<tr><th>verdict</th><th>border</th><th>veil</th><th>swipe</th><th>cues</th></tr>";
  vt.innerHTML = head + Object.keys(T.verdicts).map(function (k) {
    var r = T.verdicts[k];
    return "<tr><td>" + k + "</td><td>" + (r.border ? "lane" : "—") + "</td><td>" +
           (r.veil ? "yes" : "—") + "</td><td>" + (r.swipe ? "yes" : "—") + "</td><td>" +
           ((r.cues && r.cues.length) ? r.cues.join(", ") : "—") + "</td></tr>";
  }).join("");

  /* ------------------------------------------------------------------ Part 7 · the lab
   *
   * Experiments, drawn so they can be looked at. Nothing here is the style, and nothing a
   * scenario can reach may reference it — `capart build` enforces that, this just draws it.
   */

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
      var box = el("div", "lab-entry");
      var h = el("h3");
      h.innerHTML = (spec.title || key) + ' <span class="key">lab.' + key + "</span>";
      box.appendChild(h);
      var asks = el("p", "asks");
      asks.innerHTML = "<b>Asks:</b> " + (spec.asks || "<em>nothing — Part 7 says an entry that " +
        "cannot say what it is asking is decoration</em>");
      box.appendChild(asks);
      labHost.appendChild(box);
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
