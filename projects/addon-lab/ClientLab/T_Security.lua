-- T_Security.lua — what is still OPEN in the §4.2 secret-value operation table,
-- anchored in knowledge/addon-dev/security-taint-and-restricted-data.md.
--
-- The table itself is a KB claim now: thirteen of its fourteen rows are measured and
-- written up, and their tests were deleted with the claims that carry them.  What is
-- left is row 8, which no obtainable secret can exercise, and the aspect-less sinks,
-- which no instrument can read.
--
-- Everything here declares needs="secret".  The runner gates it: OUT OF COMBAT a
-- genuine Secret Value can't be obtained, so it records `skipped` with the reason and
-- NEVER a value.  In combat, ns.GetSecret() hands back a real secret (a GCD cooldown
-- field) and each op runs inside its own pcall — a raise is often the claim being
-- tested, so it is recorded as the answer rather than allowed to break the run.
local ADDON, ns = ...

-- op(fn) — run one operation on the secret and normalise the outcome.  On success
-- the result is stashed (a secret result degrades to "<secret>") and its secrecy
-- recorded — the OUTPUT's secrecy is the half the KB does not state for the
-- "allowed" rows.  On failure the error string is the answer.
local function op(fn)
  local ok, res = pcall(fn)
  if ok then
    return { errored = false, result = ns.stash(res), resultSecret = ns.IsSecret(res) }
  end
  return { errored = true, err = tostring(res) }
end

local function row(id, line, question, run, blocked)
  ns.Test{ id = id, anchor = "security-taint-and-restricted-data.md:" .. line,
           bucket = "secret", needs = "secret", question = question, run = run,
           blocked = blocked }
end

row("secret-op-bool-test-boolean", 729, "§4.2 row 8 — boolean test on a BOOLEAN secret.",
  function()
    local v = ns.GetSecret()
    -- type() on a secret is allowed and returns the real type (row 14).  If our
    -- secret is not boolean we CANNOT measure this row honestly — record that,
    -- never a fabricated verdict.
    local ok, ty = pcall(type, v)
    if not ok then return { measured = false, why = "type() on the secret errored" } end
    if ty ~= "boolean" then
      return { measured = false, why = "no boolean secret available (cooldown source is " .. tostring(ty) .. ")" }
    end
    return op(function() if v then return "truthy" else return "falsy" end end)
  end,
  "a boolean-valued secret source — every secret this client hands an addon is a "
  .. "cooldown number, so the row cannot be exercised at all")

--------------------------------------------------------------------------------
-- The aspect-less secret sinks — the eyeball channel
--------------------------------------------------------------------------------
-- `Texture:SetAtlas` accepts a Secret Value, declares no SecretArgumentsAddAspect,
-- exposes no getter and leaves the anchor chain clean.  So no instrument can say
-- whether a pixel moved, and INERT is the dangerous verdict rather than the boring one.
--
-- ⚠ THE CONTROL IS THE WHOLE DESIGN.  An atlas NAME is a string, and the only secret
-- string obtainable here is a concatenation (§4.2 row 4, measured secret), which is not
-- a valid atlas name.  So "the secret cell is blank" is ambiguous on its own — an
-- invalid plain name is blank too.  The middle cell is fed exactly that, so the person
-- is comparing the secret against BOTH outcomes rather than guessing which one it is.
-- If secret and invalid look alike, this channel is NOT demonstrated, and that is the
-- honest reading, not a disappointment.
--
-- SetVertexColor is deliberately ABSENT: it declares aspect {VertexColor, Alpha}, so it
-- has a readback and was settled by instrument. Putting it in front of a human asked
-- them to squint at something already measured.
local ATLAS_VALID = "UI-HUD-ActionBar-IconFrame-Mouseover"
local ATLAS_INVALID = "ClientLab-NoSuchAtlas-zzzz"

-- A framed, labelled cell, so "rendered empty" and "not there" are distinguishable.
-- Without the border an absent region and a blank one look identical, which is what
-- made the first version of this stimulus unreadable.
local function cell(canvas, x, label)
  local f = CreateFrame("Frame", nil, canvas)
  f:SetSize(120, 92)
  f:SetPoint("TOPLEFT", canvas, "TOPLEFT", x, -30)
  local bg = f:CreateTexture(nil, "BACKGROUND")
  bg:SetAllPoints(f)
  bg:SetColorTexture(0.10, 0.10, 0.12, 1)
  ns.UI.edge(f, 0.5, 0.5, 0.6, 1)
  local cap = f:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
  cap:SetPoint("BOTTOM", f, "BOTTOM", 0, 4)
  cap:SetText(label)
  local tex = f:CreateTexture(nil, "ARTWORK")
  tex:SetSize(104, 60)
  tex:SetPoint("TOP", f, "TOP", 0, -6)
  return f, tex
end

ns.Ask.Register{
  id = "secret-aspectless-pixel-moved",
  anchor = "security-taint-and-restricted-data.md:1282", bucket = "secret",
  needs = "secret",
  question = "Cell 3 (SECRET) — does it look like cell 1 (VALID), like cell 2 (INVALID), or like neither?",
  note = "All three boxes exist; judge what is DRAWN INSIDE each. SetAtlas has no getter "
      .. "and no aspect, so this is the only oracle. If 3 matches 2, the secret was "
      .. "dropped exactly as a bad name is and this channel is NOT demonstrated — that is "
      .. "a real answer. If 3 matches 1, or shows anything else, the channel is live.",
  options = { "3 matches 2 (INVALID)", "3 matches 1 (VALID)", "3 is different from both", "can't tell" },
  setup = function(canvas)
    local secret = ns.GetSecret()
    -- Concatenation yields a SECRET STRING (§4.2 row 4, measured 2026-08-05). It is the
    -- only secret string reachable from a cooldown source, and it is necessarily not a
    -- real atlas name — which is exactly why cell 2 exists.
    local secretName = "ClientLab-" .. secret

    local head = canvas:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    head:SetPoint("TOP", canvas, "TOP", 0, -8)
    head:SetText("Texture:SetAtlas — same call, three arguments")

    local f1, t1 = cell(canvas, 24, "1 · VALID name")
    local f2, t2 = cell(canvas, 156, "2 · INVALID name")
    local f3, t3 = cell(canvas, 288, "3 · SECRET string")

    local ok1 = pcall(function() t1:SetAtlas(ATLAS_VALID) end)
    local ok2 = pcall(function() t2:SetAtlas(ATLAS_INVALID) end)
    local ok3, err3 = pcall(function() t3:SetAtlas(secretName) end)

    -- Whether the CALL was refused is instrument-readable and worth showing beside the
    -- pixels: a refusal is a different finding from an accepted-but-inert call.
    local foot = canvas:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
    foot:SetPoint("BOTTOM", canvas, "BOTTOM", 0, 8)
    foot:SetText(string.format("call accepted:  1 %s   2 %s   3 %s%s",
      tostring(ok1), tostring(ok2), tostring(ok3),
      ok3 and "" or ("  |cffff8844(" .. tostring(err3) .. ")|r")))

    canvas.kids = { f1, f2, f3 }
    canvas.regions = { head, foot }
  end,
}
