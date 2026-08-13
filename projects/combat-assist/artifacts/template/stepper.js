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

  /* ------------------------------------------------------------------ cue glyphs
   * Placeholder shapes standing in for the white-alpha textures the shelf's Part 4 says
   * we author ourselves. They are drawn as flat tinted paths — the SHAPE is provisional,
   * the tint and the placement are the shelf's.
   */
  var GLYPH = {
    cross:   "M22 22 L78 78 M78 22 L22 78",
    bar:     "M14 42 H86 V58 H14 Z",
    check:   "M18 52 L40 74 L84 26",
    chevron: "M30 22 L64 50 L30 78"
  };
  function cueNode(key) {
    var spec = T.cues[key] || {};
    var wrap = el("div", "cue");
    wrap.title = key + (spec.open ? " (open — unverified in client)" : "");
    if (spec.open) wrap.setAttribute("data-open", "1");
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 100 100");
    var p = document.createElementNS("http://www.w3.org/2000/svg", "path");
    p.setAttribute("d", GLYPH[spec.glyph] || GLYPH.bar);
    var filled = spec.glyph === "bar";
    p.setAttribute("fill", filled ? rgb(spec.rgb || [1, 1, 1]) : "none");
    p.setAttribute("stroke", filled ? "none" : rgb(spec.rgb || [1, 1, 1]));
    p.setAttribute("stroke-width", "14");
    p.setAttribute("stroke-linecap", "round");
    p.setAttribute("stroke-linejoin", "round");
    svg.appendChild(p);
    wrap.appendChild(svg);
    return wrap;
  }

  /* ------------------------------------------------------------------ one CDM item */

  function itemNode(entry, index) {
    var ab = D.abilities[entry.name] || {};
    var lane = ab.lane || "FALLBACK";
    var rule = T.verdicts[entry.verdict] || {};
    var laneTok = T.lanes[lane] || T.lanes.FALLBACK;

    var item = el("div", "item");
    item.style.setProperty("--lane-color", rgb(laneTok.rgb));
    item.style.setProperty("--phase", (index * T.pulse.phase_offset_s).toFixed(3) + "s");
    item.style.setProperty("--pulse-dur", (0.5 / laneTok.pulse_hz).toFixed(3) + "s");

    if (rule.emphasis === "promoted") {
      item.style.setProperty("--lane-alpha", String(T.promotion.alpha));
      item.style.setProperty("--item-scale", String(T.promotion.scale));
    } else {
      item.style.setProperty("--lane-alpha", String(laneTok.alpha));
    }
    if (rule.desaturate) item.style.setProperty("--desat", String(rule.desaturate));

    var art = el("div", "art");
    if (ab.icon) art.style.backgroundImage = "url(" + ab.icon + ")";
    item.appendChild(art);

    if (rule.swipe) item.appendChild(el("div", "swipe"));
    if (rule.veil) item.appendChild(el("div", "veil"));
    if (rule.emphasis === "lane" || rule.emphasis === "promoted") item.appendChild(el("div", "ring"));

    var open = false;
    var cues = (rule.cues || []).concat(entry.cues || []);
    if (cues.length) {
      var bar = el("div", "cues");
      cues.slice(0, T.surfaces.center_row.max).forEach(function (k) {
        if ((T.cues[k] || {}).open) open = true;
        bar.appendChild(cueNode(k));
      });
      item.appendChild(bar);
    }
    if (open) item.setAttribute("data-open", "1");

    (entry.dots || []).slice(0, 2).forEach(function (dot, i) {
      var d = el("div", "dot");
      d.setAttribute("data-corner", i === 0 ? "left" : "right");
      d.setAttribute("data-state", dot.state);
      d.title = dot.label + " — " + (dot.state === "go" ? "on cooldown (the dependency is satisfied)"
                                                        : "ready (the press would waste it)");
      item.appendChild(d);
    });

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

  function render() {
    var sc = D.scenarios[current];
    var reach = reachedThrough(sc, step - 1);

    stateEl.innerHTML = "<b>State.</b> " + sc.state;

    rowEl.innerHTML = "";
    sc.row.forEach(function (entry, i) {
      var col = itemNode(entry, i);
      if (i >= reach && step > 0) col.setAttribute("data-dimmed", "1");
      if (step > 0 && i === reach - 1) col.setAttribute("data-active", "1");
      rowEl.appendChild(col);
    });

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
    if (sc.open_note) {
      var w = el("div", "note");
      w.innerHTML = "⚠ " + sc.open_note;
      extrasEl.appendChild(w);
    }
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
    var host = el("div"); host.style.height = "calc(" + T.surfaces.icon_px + "px * 1.6)";
    host.style.display = "flex"; host.style.alignItems = "center"; host.style.justifyContent = "center";
    host.appendChild(build());
    s.appendChild(host);
    var n = el("div", "name"); n.textContent = name; s.appendChild(n);
    var w = el("div", "why"); w.textContent = why; s.appendChild(w);
    return s;
  }

  var gallery = document.getElementById("gallery");

  // The swatch's lane comes from whichever ability it borrows art from, exactly as it does
  // in a scenario row — so a gallery swatch and a live row can never diverge.
  function bareItem(name, verdict, opts) {
    opts = opts || {};
    var col = itemNode({ name: name, verdict: verdict, dots: opts.dots, cues: opts.cues }, opts.index || 0);
    return col.firstChild;
  }

  Object.keys(T.lanes).forEach(function (lane) {
    var tok = T.lanes[lane];
    var name = D.lane_sample[lane];
    gallery.appendChild(swatch(
      "lane · " + lane,
      "ring tinted " + rgb(tok.rgb) + ", pulsing at " + tok.pulse_hz + " Hz",
      function () { return bareItem(name, "press"); }
    ));
  });

  gallery.appendChild(swatch("promotion", "the press, scaled " + T.promotion.scale + "× at full alpha",
    function () { return bareItem(D.lane_sample.ROTATION, "press-promoted"); }));
  gallery.appendChild(swatch("veil", "de-emphasis at alpha " + T.veil.alpha,
    function () { return bareItem(D.lane_sample.ROTATION, "withheld"); }));
  gallery.appendChild(swatch("starved", "veil plus full desaturation",
    function () { return bareItem(D.lane_sample.ROTATION, "starved"); }));
  gallery.appendChild(swatch("swipe", "Blizzard's own dial — cap draws nothing here",
    function () { return bareItem(D.lane_sample.COOLDOWN, "cd"); }));
  gallery.appendChild(swatch("dots · go / wait", "top corners; go = dependency satisfied",
    function () {
      return bareItem(D.lane_sample.COOLDOWN, "press", {
        dots: [{ label: "Eye Beam", state: "go" }, { label: "Death Sweep", state: "wait" }]
      });
    }));

  var cueKeys = Object.keys(T.cues).filter(function (k) { return k !== "dot"; });
  cueKeys.forEach(function (key) {
    var tok = T.cues[key];
    gallery.appendChild(swatch(
      "cue · " + key + (tok.open ? " ⚠" : ""),
      tok.open ? "declared, unverified in client — produces no hint yet"
               : "center-row cue, " + tok.glyph + " glyph",
      function () { return bareItem(D.lane_sample.ROTATION, "press", { cues: [key] }); }
    ));
  });

  gallery.appendChild(swatch("center row · full",
    T.surfaces.center_row.max + " cues is the ceiling the shelf sets",
    function () {
      return bareItem(D.lane_sample.ROTATION, "press", { cues: cueKeys.slice(0, T.surfaces.center_row.max) });
    }));

  /* ------------------------------------------------------------------ tables */

  var vt = document.getElementById("verdicts");
  var head = "<tr><th>verdict</th><th>emphasis</th><th>veil</th><th>swipe</th><th>cues</th></tr>";
  vt.innerHTML = head + Object.keys(T.verdicts).map(function (k) {
    var r = T.verdicts[k];
    return "<tr><td>" + k + "</td><td>" + r.emphasis + "</td><td>" + (r.veil ? "yes" : "—") +
           "</td><td>" + (r.swipe ? "yes" : "—") + "</td><td>" +
           ((r.cues && r.cues.length) ? r.cues.join(", ") : (k === "hold-readable" ? "dots" : "—")) + "</td></tr>";
  }).join("");

  /* ------------------------------------------------------------------ Part 7 · the lab
   *
   * Experiments, drawn so they can be looked at. Nothing here is the style, and nothing a
   * scenario can reach may reference it — `capart build` enforces that, this just draws it.
   */

  function labEntry(key, spec) {
    var box = el("div", "lab-entry");
    var h = el("h3");
    h.innerHTML = spec.title + ' <span class="key">lab.' + key + "</span>";
    box.appendChild(h);
    var asks = el("p", "asks");
    asks.innerHTML = "<b>Asks:</b> " + spec.asks;
    box.appendChild(asks);
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
    cap.innerHTML = caption;
    c.appendChild(cap);
    return c;
  }

  var LAB = T.lab || {};
  var labHost = document.getElementById("lab");

  /* --- L1 · solid border, animated only on arrival ---------------------------------- */
  var L1 = LAB["border-arrival"];
  if (L1 && labHost) {
    var e1 = labEntry("border-arrival", L1);
    var edges = [];
    L1.triggers.forEach(function (t) {
      var ab = D.abilities[t.ability];
      var node = el("div", "lab-bord");
      node.setAttribute("data-lane", t.lane);
      var art = el("div", "art");
      if (ab) art.style.backgroundImage = "url(" + ab.icon + ")";
      node.appendChild(art);
      var edge = el("div", "edge");
      node.appendChild(edge);
      edges.push(edge);
      e1.row.appendChild(labCell(node,
        "<b>" + t.lane + "</b><br>" + t.ability + "<br>" + t.label));
    });

    // The addon fires this on the event and stops. Here the timer stands in for the event,
    // so the entry can be watched — it is a viewing aid, not part of the proposal.
    var fire = function () {
      edges.forEach(function (e, i) {
        e.removeAttribute("data-anim");
        void e.offsetWidth;                     // restart the animation
        setTimeout(function () { e.setAttribute("data-anim", "1"); }, i * 120);
      });
    };
    fire();
    setInterval(fire, L1.arrival.replay_every_s * 1000);

    var note1 = el("div", "cap");
    note1.style.width = "100%";
    note1.innerHTML = "The three triggers fire the <b>same</b> animation from three different " +
      "causes. Replayed every " + L1.arrival.replay_every_s + "s so it can be watched; in the " +
      "addon it fires once, on the event, and stops.";
    e1.box.appendChild(note1);
    labHost.appendChild(e1.box);
  }

  /* --- L2 · OS-style corner badges --------------------------------------------------- */
  var L2 = LAB["badge-slots"];
  if (L2 && labHost && D.lab_frames) {
    var e2 = labEntry("badge-slots", L2);
    var badgeKeys = Object.keys(L2.badges);

    // One cell per badge alone, then one with both, then all three slots filled — so the
    // question "do three slots crowd the face?" is answerable rather than asserted.
    var combos = badgeKeys.map(function (k) { return { slots: [k], cap: "<b>" + k + "</b> alone" }; });
    if (badgeKeys.length > 1) {
      combos.push({ slots: badgeKeys.slice(0, 2), cap: "<b>two</b> slots" });
      combos.push({ slots: [badgeKeys[0], badgeKeys[1], badgeKeys[0]], cap: "<b>three</b> — the ceiling" });
    }

    var timers = [];
    combos.forEach(function (combo, ci) {
      var node = el("div", "lab-badges");
      var art = el("div", "art");
      var ab = D.abilities[D.lane_sample.ROTATION];
      if (ab) art.style.backgroundImage = "url(" + ab.icon + ")";
      node.appendChild(art);

      combo.slots.forEach(function (bk, si) {
        var b = L2.badges[bk];
        var slot = el("div", "slot");
        slot.setAttribute("data-slot", String(si + 1));
        var sprite = el("div", "sprite");
        sprite.style.setProperty("--lab-badge-tint", rgb(b.rgb));
        slot.appendChild(sprite);
        node.appendChild(slot);

        // Hand-stepped frames: the client walks a FlipBook, we walk the same frame list at
        // the same rate, so what you see is the sheet's real cadence and not a CSS easing.
        var n = b.frames.length;
        var per = (b.duration_s / n) * 1000;
        var i = 0, dir = 1;
        var step = function () {
          var f = D.lab_frames[b.frames[i]];
          if (f) sprite.style.setProperty("--lab-frame", "url(" + f.uri + ")");
          if (b.loop === "BOUNCE") {
            if (i + dir < 0 || i + dir >= n) dir = -dir;
            i += dir;
          } else {
            i = (i + 1) % n;
          }
        };
        step();
        timers.push(setInterval(step, per));
      });
      e2.row.appendChild(labCell(node, combo.cap));
    });

    // A badge whose CENTER is on the corner overhangs by half its diameter, and the CDM row
    // gap is only tokens.surfaces.row_gap_px — so neighbours can collide. That is arithmetic,
    // and arithmetic in a caption is an assertion; drawn in a real row it is a finding.
    var rowCell = el("div", "lab-cell");
    rowCell.style.width = "auto";
    var stage = el("div", "lab-stage");
    var strip = el("div");
    strip.style.display = "flex";
    strip.style.gap = "var(--row-gap)";
    ["COOLDOWN", "ROTATION", "FALLBACK"].forEach(function (lane, li) {
      var node = el("div", "lab-badges");
      var art = el("div", "art");
      var ab = D.abilities[D.lane_sample[lane]];
      if (ab) art.style.backgroundImage = "url(" + ab.icon + ")";
      node.appendChild(art);
      [badgeKeys[li % badgeKeys.length]].forEach(function (bk) {
        var b = L2.badges[bk];
        var slot = el("div", "slot");
        slot.setAttribute("data-slot", "1");
        var sprite = el("div", "sprite");
        sprite.style.setProperty("--lab-badge-tint", rgb(b.rgb));
        sprite.style.setProperty("--lab-frame", "url(" + D.lab_frames[b.frames[b.frames.length - 1]].uri + ")");
        slot.appendChild(sprite);
        node.appendChild(slot);
      });
      strip.appendChild(node);
    });
    stage.appendChild(strip);
    rowCell.appendChild(stage);
    var rc = el("div", "cap");
    var overhang = (L2.diameter_pct / 100 * T.surfaces.icon_px) / 2;
    rc.innerHTML = "<b>in a real row</b> — badge overhangs " + overhang.toFixed(1) +
      "px past the edge; the row gap is " + T.surfaces.row_gap_px + "px" +
      (overhang > T.surfaces.row_gap_px
        ? ". <b>They collide.</b>" : ". They clear.");
    rowCell.appendChild(rc);
    e2.row.appendChild(rowCell);

    // The frame strips, so the art itself is inspectable rather than only seen in motion.
    var legend = el("div", "lab-legend");
    badgeKeys.forEach(function (bk) {
      var b = L2.badges[bk];
      var li = el("div", "li");
      var strip = el("div", "lab-frames");
      b.frames.forEach(function (fn) {
        var f = D.lab_frames[fn];
        var d = el("div", "f");
        if (f) {
          d.style.backgroundColor = rgb(b.rgb);
          d.style.webkitMaskImage = d.style.maskImage = "url(" + f.uri + ")";
          d.style.webkitMaskSize = d.style.maskSize = "contain";
          d.style.webkitMaskRepeat = d.style.maskRepeat = "no-repeat";
        }
        strip.appendChild(d);
      });
      li.appendChild(strip);
      var t = el("span");
      t.innerHTML = "<b>" + bk + "</b> — " + b.means + " (" + b.duration_s + "s, " + b.loop + ")";
      li.appendChild(t);
      legend.appendChild(li);
    });
    e2.box.appendChild(legend);
    labHost.appendChild(e2.box);
  }

  document.getElementById("prov").innerHTML = D.provenance_html;

  // A build-time honesty flag: art drawn through a path we have not verified in client.
  (D.notes || []).forEach(function (msg) {
    var n = el("div", "note");
    n.innerHTML = "⚠ " + msg;
    document.getElementById("state").parentNode.insertBefore(n, document.getElementById("state"));
  });

  render();
})();
