"""Smart Glo rules: surface text <-> AST <-> wire string, in Python alone.

The AST is canonical; surface text and the wire string are two renderings of it
(projects/smart-glo/rule-language.md §7). The point of this module is that an agent can
author a rule, hand back a paste-able string, and read one back, without a running client
and — the constraint that shaped the format — without a Lua interpreter anywhere in the
decode path.

    uv run python -m wowkb.smartglo encode rules.sg      # surface text -> SG1: string
    uv run python -m wowkb.smartglo decode "SG1:..."     # -> surface text
    uv run python -m wowkb.smartglo decode "SG1:..." --json
    uv run python -m wowkb.smartglo check rules.sg       # parse and report refusals

The wire format is `SG1:` + base64(raw-deflate(json envelope)), the envelope carrying the
payload JSON as a string beside its adler32. The addon's three calls are
C_EncodingUtil.SerializeJSON / CompressString(Deflate) / EncodeBase64(Standard); Deflate
there is RAW deflate, which is zlib with wbits=-15 here.

**Two bowls.** `when` carries readable terms and takes as many as you like; `bind` carries
the one sealed leaf a glow may spend (§5). Which bowl a term belongs to is a fact about the
client build, not about the rule, so the tool owns the sorting and refuses a mis-sorted term
by naming the bowl it belongs to — in both directions.
"""

import argparse
import base64
import json
import re
import sys
import zlib
from pathlib import Path

from .gen_smartglo_symbols import load as load_symbols

PREFIX = "SG1:"

SECONDARY = {
    "soul_shards", "holy_power", "combo_points", "chi",
    "arcane_charges", "essence", "runes",
}

PRIMARY = {
    "mana", "rage", "focus", "energy", "runic_power",
    "fury", "pain", "insanity", "maelstrom", "astral_power",
}

# Which resources may carry `.after_cast`. Not every secondary can: the Tier-1 energize rows
# in `knowledge/classes/_abilities/power-gain.tsv` show Wake of Ashes returning 1, 3 or 5 Holy
# Power and Ambush 1, 2 or 3 Combo Points depending on talents and procs, so there is no single
# number to project with. Soul Shards are whole and invariant for every hard cast that
# generates them, which is what makes the projection honest here and a guess everywhere else.
PROJECTABLE = {"soul_shards"}

COMPARISONS = {">=", ">", "<=", "<", "=="}

# The hues Look.lua tints the one white master to. Names, not files: nothing but the master
# is ever named by filename (tool/gen_media.py).
COLORS = {"white", "yellow", "red", "green", "blue", "purple", "orange", "cyan", "black",
          "alarm"}  # `alarm` is a CYCLE — black crossing to yellow, dark to bright — not a solid

# Every readable term that is a call over one spell. One set, because this list appearing
# three times is how the Lua and Python grammars drift apart a term at a time.
SPELL_CALLS = {"ready", "aura", "talent", "at_max_charges", "no_charges", "active",
               "affordable", "refreshable"}

# The calls that name an AURA rather than something the spec learns. `refreshable()` is
# `aura()`'s sibling — same namespace, same tracked row, same three values.
AURA_CALLS = {"aura", "refreshable"}

# Which bowl each readable term goes in, and the sealed families the other bowl takes.
WHEN_TERMS = {"resource"} | SPELL_CALLS
BIND_FAMILIES = {"count", "duration", "health", "presence", "power", "remains"}

# A duration bind clamps to full alpha at zero remaining, and zero remaining means READY —
# so `<` and `outside` glow permanently while the spell is up unless something says
# otherwise. One of these two has to be present (§6, the duration analogue of §6.4).
UNBOUNDED_BELOW = {"<", "<=", "outside"}


class RuleError(Exception):
    """A rule that would author cleanly and then never fire, or will not parse."""


# --------------------------------------------------------------- the wire format

def encode(ast) -> str:
    payload = json.dumps(ast, separators=(",", ":"), sort_keys=True)
    envelope = json.dumps(
        {"c": zlib.adler32(payload.encode("utf-8")) & 0xFFFFFFFF, "j": payload},
        separators=(",", ":"), sort_keys=True)
    deflate = zlib.compressobj(9, zlib.DEFLATED, -15)
    packed = deflate.compress(envelope.encode("utf-8")) + deflate.flush()
    return PREFIX + base64.b64encode(packed).decode("ascii")


def decode(text: str):
    text = text.strip()
    if not text.startswith(PREFIX):
        raise RuleError(f"does not start with {PREFIX}")
    try:
        packed = base64.b64decode(text[len(PREFIX):], validate=True)
    except Exception as exc:
        raise RuleError(f"not valid base64: {exc}") from exc
    try:
        encoded = zlib.decompress(packed, -15)
    except zlib.error as exc:
        raise RuleError(f"not valid deflate: {exc}") from exc
    envelope = json.loads(encoded.decode("utf-8"))
    if not isinstance(envelope, dict) or "j" not in envelope or "c" not in envelope:
        raise RuleError("the payload is not a Smart Glo envelope")
    if zlib.adler32(envelope["j"].encode("utf-8")) & 0xFFFFFFFF != envelope["c"]:
        raise RuleError("checksum mismatch — the string was truncated or edited")
    return [modernize(g) for g in json.loads(envelope["j"])]


def modernize(glow: dict) -> dict:
    """Read a rule written before the two bowls. Wire strings already in the wild carry
    `show` and `count`; they mean exactly what `when` and a count `bind` mean now."""
    if not isinstance(glow, dict):
        return glow
    glow = dict(glow)
    if "show" in glow:
        glow.setdefault("when", glow.pop("show"))
    else:
        glow.pop("show", None)
    count = glow.pop("count", None)
    if count is not None and glow.get("bind") is None:
        glow["bind"] = {"family": "count", "aura": count.get("aura"),
                        "threshold": count.get("threshold")}
    return glow


# ------------------------------------------------------------------- spell names

def scope_key(word: str):
    """A spec scope: `demonology`, or `warlock.demonology` when the bare word names two."""
    symbols = load_symbols()
    word = word.strip().lower()
    if word in symbols["specs"]:
        return word
    if word in symbols["alias"]:
        return symbols["alias"][word]
    matches = sorted(k for k in symbols["specs"] if k.split(".", 1)[1] == word)
    if len(matches) > 1:
        raise RuleError(f"{word!r} names {len(matches)} specs; write one of "
                        + ", ".join(matches))
    raise RuleError(f"no spec {word!r}")


# Two namespaces, and the TERM picks which. `on` / `ready()` name something the spec learns;
# `aura()` names something the Cooldown Manager tracks. A word in both worlds — consecration,
# shield_of_the_righteous — is a DIFFERENT spell in each, so resolving an aura against the
# ability table is not a near miss, it is a wrong answer that parses clean.
# ⚠ `presence` shares the AURA tables but not the aura precondition, and that is the whole
# reason it is a kind of its own. Every other aura-naming family reads through a Cooldown
# Manager row; a presence bind reads `C_UnitAuras.GetUnitAuraInstanceIDs(unit, filter)` in
# untainted Blizzard code (`Presence.lua:8-11`), so a rowless debuff is squarely inside what
# it can watch and refusing one is the tool inventing a limit the addon does not have.
_NAMESPACE = {"ability": ("specs", "names"), "aura": ("auraSpecs", "auraNames"),
              "presence": ("auraSpecs", "auraNames")}
_AURA_KINDS = ("aura", "presence")


def _name_in(key: str, spell_id: int, kind: str = "ability"):
    """The name an id answers to inside ONE spec. Two ids of a spec sharing a slug is the
    norm, so the generator gives the bare slug to the one a rule can bind to and spells the
    rest `<slug>_<id>` for that spec alone — 24275 is `hammer_of_wrath` in Retribution and
    `hammer_of_wrath_24275` in Protection, where the row carries 1241413."""
    symbols = load_symbols()
    _, name_key = _NAMESPACE.get(kind, _NAMESPACE["ability"])
    if kind not in _AURA_KINDS:
        scoped = symbols.get("specNames", {}).get(key, {}).get(spell_id)
        if scoped is not None:
            return scoped
    return symbols[name_key].get(spell_id)


def _resolve_suffixed(key: str, text: str, kind: str):
    """`<slug>_<id>`, accepted for ANY id in the spec and not only the ones the generator had
    to mint it for. That generality is what makes the spelling stable: a rule written with a
    suffix keeps naming the same spell after a regeneration hands the bare slug to a different
    id. Both halves must agree, so a prefix naming a different spell than the id refuses.

    Reached only after the plain lookup missed, so a real name ending in digits still wins."""
    match = re.fullmatch(r"(.+)_(\d+)", text)
    if match is None:
        return None
    bare, spell_id = match.group(1), int(match.group(2))
    spec_key, _ = _NAMESPACE.get(kind, _NAMESPACE["ability"])
    if spell_id not in load_symbols()[spec_key].get(key, ()):
        if kind == "presence":
            return _presence_suffixed(key, text, bare, spell_id)
        raise RuleError(f"{key} carries no spell {spell_id}, so {text!r} names nothing here")
    full = _name_in(key, spell_id, kind)
    if full in (text, bare):
        return spell_id
    raise RuleError(f"{spell_id} is {full} in {key}, not {text!r}")


def _presence_suffixed(key: str, text: str, bare: str, spell_id: int):
    """The second table a presence bind may name, and ONLY through the suffixed spelling.

    A rowless debuff — Essence Break, whose cast and debuff are both 258860 — is in the
    ability inventory and in no tracked-aura set, so `aura()`'s table cannot reach it and the
    container that would watch it needs no row. What makes this safe where a blind fallback
    would not be: the suffix states BOTH halves, so the id is checked against the name rather
    than trusted. A bare slug still refuses, because for most spells the cast and the aura are
    different ids (Moonfire 8921 against 164812) and guessing between them is the exact error
    `_resolve_aura` exists to prevent."""
    if spell_id not in load_symbols()["specs"].get(key, ()):
        raise RuleError(f"{key} carries no spell {spell_id}, so {text!r} names nothing here")
    full = _name_in(key, spell_id, "ability")
    if full in (text, bare):
        return spell_id
    raise RuleError(f"{spell_id} is {full} in {key}, not {text!r}")


def _spec_index(key: str, kind: str = "ability") -> dict:
    symbols = load_symbols()
    spec_key, name_key = _NAMESPACE.get(kind, _NAMESPACE["ability"])
    index = {_name_in(key, i, kind): i for i in symbols[spec_key].get(key, ())
             if _name_in(key, i, kind) is not None}
    # An id the sources name twice — a talent and the ability it grants, or the inventory and
    # the CDM disagreeing on wording — resolves under either name.
    if kind not in _AURA_KINDS:
        for i in symbols[spec_key].get(key, ()):
            also = symbols.get("also", {}).get(i)
            if also and also not in index:
                index[also] = i
    return index


def _refusal(key: str, bare: str) -> str:
    """Absent from the ABILITY table is two problems: a word the spec never had, or two ids
    that rank equally as a subject, where which one a build produces is a talent question no
    offline pass can answer. The second is the author's call, spelled `<slug>_<id>`."""
    ids = load_symbols().get("abilityAmbiguous", {}).get(key, {}).get(bare)
    if ids is None:
        return f"{key} has no {bare!r}"
    return (f"{bare!r} names {len(ids)} equally good spells in {key} and which one your "
            "talents produce cannot be known here; write one of "
            + ", ".join(f"{bare}_{i}" for i in ids))


def _presence_refusal(key: str, bare: str) -> str:
    """A presence bind needs no row, so "no tracked row" is the wrong thing to tell its
    author. When the ability inventory has the name, the refusal is only that a bare slug
    cannot be CHECKED against an id — and it names the spelling that can."""
    ids = load_symbols().get("auraAmbiguous", {}).get(key, {}).get(bare)
    if ids is not None:
        return (f"{bare!r} names {len(ids)} tracked rows in {key}; write one of "
                + ", ".join(f"{bare}_{i}" for i in ids))
    known = _spec_index(key, "ability").get(bare)
    if known is not None:
        return (f"{key} tracks no aura row called {bare!r}. A presence bind needs no row and "
                f"can still watch it, but only spelled with its id, which is what makes the "
                f"name checkable: write {bare}_{known}")
    return f"{key} has no {bare!r}"


def _aura_refusal(key: str, bare: str) -> str:
    """Absent from the aura table is two different problems, and the author needs to know
    which: a buff with no tracked row can never be named, while one naming two rows is a
    choice only the author can make."""
    ids = load_symbols().get("auraAmbiguous", {}).get(key, {}).get(bare)
    if ids is None:
        return (f"{key} tracks no aura called {bare!r} — an aura() term reads through a "
                "Cooldown Manager row, so a buff with no tracked row cannot be named here")
    return (f"{bare!r} names {len(ids)} tracked rows in {key}; write one of "
            + ", ".join(f"{bare}_{i}" for i in ids))


def resolve(text: str, scope, kind: str = "ability") -> int:
    """A spell reference: a raw id, `class.spec.name`, or a bare name inside `scope`."""
    text = text.strip().lower()
    if re.fullmatch(r"\d+", text):
        return int(text)
    if not text:
        raise RuleError("a spell name or id is required")
    parts = text.split(".")
    if len(parts) == 3:
        key = scope_key(f"{parts[0]}.{parts[1]}")
        found = _spec_index(key, kind).get(parts[2])
        if found is None:
            found = _resolve_suffixed(key, parts[2], kind)
        if found is None:
            raise RuleError(_refusal_for(kind)(key, parts[2]))
        return found
    if len(parts) != 1:
        raise RuleError(f"{text!r} is not a name; write <class>.<spec>.<name>, "
                        "a bare name, or an id")
    if scope is None:
        raise RuleError(f"{text!r} needs a scope — put `spec demonology` above the rules, "
                        f"or write warlock.demonology.{text}, or a raw spell id")
    found = _spec_index(scope, kind).get(text)
    if found is None:
        found = _resolve_suffixed(scope, text, kind)
    if found is None:
        raise RuleError(_refusal_for(kind)(scope, text))
    return found


def _refusal_for(kind: str):
    return {"aura": _aura_refusal, "presence": _presence_refusal}.get(kind, _refusal)


def name_of(spell_id: int, scope, kind: str = "ability") -> str:
    """How a rule should spell an id back. Bare inside its own scope, qualified when the
    id belongs to another spec, and the number itself when nothing names it — an override
    id such as Ruination is a real subject and is in no spec inventory."""
    symbols = load_symbols()
    spec_key, _ = _NAMESPACE.get(kind, _NAMESPACE["ability"])
    if scope is not None and spell_id in symbols[spec_key].get(scope, ()):
        here = _name_in(scope, spell_id, kind)
        if here is not None:
            return here
    for key, ids in symbols[spec_key].items():
        if spell_id in ids:
            name = _name_in(key, spell_id, kind)
            if name is not None:
                return f"{key}.{name}"
    if kind == "presence":
        # No tracked row names it, so the ability inventory might — and the SUFFIXED form is
        # the only spelling that parses back, since a bare slug is refused on that path.
        ability = name_of(spell_id, scope, "ability")
        if ability != str(spell_id):
            return f"{ability}_{spell_id}"
    return str(spell_id)


# -------------------------------------------------------------- the surface text

TOKEN = re.compile(r"""
    (?P<ws>\s+)
  | (?P<comment>--[^\n]*)
  | (?P<number>\d+)
  | (?P<name>[A-Za-z_][A-Za-z_0-9.]*)
  | (?P<cmp>>=|<=|==|>|<)
  | (?P<punct>[()])
  | (?P<string>"[^"]*")
""", re.VERBOSE)


def _lex(text):
    out, pos = [], 0
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if m is None:
            raise RuleError(f"cannot read {text[pos:pos + 20]!r}")
        pos = m.end()
        kind = m.lastgroup
        if kind in ("ws", "comment"):
            continue
        out.append((kind, m.group()))
    out.append(("end", ""))
    return out


class _Parser:
    def __init__(self, tokens, scope):
        self.tokens = tokens
        self.i = 0
        self.scope = scope

    def peek(self):
        return self.tokens[self.i]

    def take(self):
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def expect(self, value):
        kind, text = self.take()
        if text != value:
            raise RuleError(f"expected {value!r}, found {text!r}")
        return text

    def expression(self):
        node = self.conjunction()
        while self.peek()[1] == "or":
            self.take()
            node = {"t": "or", "terms": [node, self.conjunction()]}
        return node

    def conjunction(self):
        node = self.unary()
        while self.peek()[1] == "and":
            self.take()
            node = {"t": "and", "terms": [node, self.unary()]}
        return node

    def unary(self):
        if self.peek()[1] == "not":
            self.take()
            return {"t": "not", "term": self.unary()}
        return self.primary()

    def primary(self):
        kind, text = self.take()
        if text == "(":
            node = self.expression()
            self.expect(")")
            return node
        if kind != "name":
            raise RuleError(f"expected a term, found {text!r}")
        if text in SPELL_CALLS:
            self.expect("(")
            ref = self.take()
            if ref[0] not in ("name", "number"):
                raise RuleError(f"{text}() takes a spell name or id, found {ref[1]!r}")
            self.expect(")")
            kind = "aura" if text in AURA_CALLS else "ability"
            return {"t": text, "spell": resolve(ref[1], self.scope, kind)}
        if text in ("health", "health%"):
            raise RuleError("health is never readable — UnitHealth is unconditionally "
                            "secret. It belongs in `bind` as `health% < <n>`, not in `when`")
        # `soul_shards.after_cast` is one lexer token, so the suffix comes off before the
        # name is looked up — which is also what lets `mana.after_cast` earn the primary
        # refusal rather than the useless "unknown term".
        power, projected = text, False
        if text.endswith(".after_cast"):
            power, projected = text[: -len(".after_cast")], True
        if power in PRIMARY:
            raise RuleError(f"{power} is a primary resource, which is never readable — it "
                            f"belongs in `bind` as a percent, not in `when`")
        sealed = re.search(r"\.(stacks|cooldown)$", power)
        if sealed:
            raise RuleError(f"{power} is a sealed term and belongs in `bind`, not in `when`")
        if power not in SECONDARY:
            raise RuleError(f"unknown term {text!r}")
        cmp_kind, cmp_text = self.take()
        if cmp_kind != "cmp" or cmp_text not in COMPARISONS:
            raise RuleError(f"expected a comparison after {text}, found {cmp_text!r}")
        value = self.take()
        if value[0] != "number":
            raise RuleError(f"expected a number after {cmp_text}, found {value[1]!r}")
        node = {"t": "resource", "power": power, "cmp": cmp_text, "value": int(value[1])}
        if projected:
            node["projected"] = True
        return node


# A bind is at most one leaf, so it is matched rather than parsed. `absent show` is the
# author saying what a `<`/`outside` duration should do while the spell is ready.
_STACKS = re.compile(r"^(?P<spell>[\w.]+)\.stacks\s*>=\s*(?P<n>\d+)$")
_COUNT = re.compile(r"^count\(\s*(?P<spell>[\w.]+)\s*\)\s*>=\s*(?P<n>\d+)$")
_OUTSIDE = re.compile(r"^(?P<spell>[\w.]+)\.cooldown\s+outside\s+"
                      r"(?P<lo>[\d.]+)s\s*\.\.\s*(?P<hi>[\d.]+)s(?P<rest>.*)$")
_REMAINS = re.compile(r"^(?P<spell>[\w.]+)\.cooldown\s*(?P<cmp>>=|<=|>|<)\s*"
                      r"(?P<n>[\d.]+)s(?P<rest>.*)$")

# An AURA's remaining time, in seconds, not a cooldown's — the distinct suffix is what keeps
# it off `.cooldown`. ⚠ `_REMAINS` above is the COOLDOWN one; these read different clocks.
_AURA_REMAINS = re.compile(r"^(?P<aura>[\w.]+)\.remains\s*(?P<cmp>>=|<=|>|<)\s*"
                           r"(?P<n>[\d.]+)s$")

_HEALTH = re.compile(r"^health%\s*(?P<cmp>>=|<=|>|<)\s*(?P<n>[\d.]+)$")

# A primary resource, as a percent. The subject is a bar rather than a unit, so it is its own
# family and not health's -- but it is the same mechanism: `UnitPowerPercent(unit, type,
# usePredicted, curve)` is `UnitHealthPercent`'s documented sibling and evaluates the curve in C
# (`security-taint-and-restricted-data.md` §4.8.0, whose worked example is a mana bar).
_POWER = re.compile(r"^(?P<power>[a-z_]+)%\s*(?P<cmp>>=|<=|>|<)\s*(?P<n>[\d.]+)$")

BIND_FORMS = ("<spell>.stacks >= <n>", "<spell>.up [on <unit>] [mine]",
              "<spell>.cooldown > <n>s", "<spell>.cooldown outside <a>s..<b>s",
              "<aura>.remains < <n>s", "health% < <n>", "<primary>% >= <n>")


def _absent(rest: str) -> dict:
    rest = rest.strip()
    if not rest:
        return {}
    word = rest.split()
    if len(word) != 2 or word[0] != "absent" or word[1] not in ("dark", "show"):
        raise RuleError(f"trailing {rest!r}; the only tail a bind takes is "
                        "`absent dark` or `absent show`")
    return {"absent": word[1]}


# `<spell>.up [on <unit>] [mine]` — the unit picks the default filter, because the useful pair
# is a buff on you and a debuff on your target. `mine` adds PLAYER, which NARROWS to auras you
# applied; it is not what a container is limited to.
_UP = re.compile(r"^(?P<spell>.+?)\.up\s*(?:on\s+(?P<unit>\S+)\s*)?(?P<mine>mine\s*)?$")
_PRESENCE_UNITS = {"player": "HELPFUL", "target": "HARMFUL"}


def _resolve_aura(text: str, scope) -> int:
    """Every container-backed bind names an aura rather than an ability.

    ⚠ NO fallback to the ability table, and the addon's `Parse.ResolveAura` says why in the
    same words: the two namespaces differ on purpose — the aura table is the CDM's tracked
    categories, which is the whole set a sealed aura bind can ever latch — so an ability id
    armed here matches no aura and lights nothing, with no refusal to say why. A name that is
    not an aura is an error, not a guess. This function used to fall back, which let the tool
    emit a rule the addon refuses."""
    return resolve(text, scope, "aura")


def parse_bind(text: str, scope) -> dict:
    m = _UP.match(text)
    if m:
        unit = m.group("unit") or "player"
        base = _PRESENCE_UNITS.get(unit)
        if base is None:
            raise RuleError(f"unknown unit {unit!r}; a presence bind reads `player` or `target`")
        filt = base + "|PLAYER" if m.group("mine") else base
        return {"family": "presence",
                "aura": resolve(m.group("spell").strip(), scope, "presence"),
                "unit": unit, "filter": filt}
    m = _STACKS.match(text) or _COUNT.match(text)
    if m:
        # A count bind does NOT read through a CDM row: it pins an AuraContainer slot by
        # spell id on the player, so its reach is wider than aura()'s and neither table is
        # exactly its universe. Tracked names first, then the ability inventory — two sources
        # for one question, so the fallback widens what resolves and changes no existing rule.
        return {"family": "count", "aura": _resolve_aura(m.group("spell"), scope),
                "threshold": int(m.group("n"))}
    m = _OUTSIDE.match(text)
    if m:
        lo, hi = float(m.group("lo")), float(m.group("hi"))
        if hi <= lo:
            raise RuleError(f"outside {lo}s..{hi}s is empty; the second bound must be larger")
        return {"family": "duration", "spell": resolve(m.group("spell"), scope),
                "cmp": "outside", "lo": lo, "hi": hi, **_absent(m.group("rest"))}
    m = _REMAINS.match(text)
    if m:
        return {"family": "duration", "spell": resolve(m.group("spell"), scope),
                "cmp": m.group("cmp"), "seconds": float(m.group("n")),
                **_absent(m.group("rest"))}
    m = _AURA_REMAINS.match(text)
    if m:
        return {"family": "remains", "aura": _resolve_aura(m.group("aura"), scope),
                "cmp": m.group("cmp"), "seconds": float(m.group("n"))}
    m = _HEALTH.match(text)
    if m:
        pct = float(m.group("n"))
        if not 0 < pct < 100:
            raise RuleError(f"health% {m.group('cmp')} {pct:g} never changes; the threshold "
                            f"has to sit strictly between 0 and 100")
        return {"family": "health", "cmp": m.group("cmp"), "percent": pct}
    m = _POWER.match(text)
    if m:
        power, pct = m.group("power"), float(m.group("n"))
        if power in SECONDARY:
            raise RuleError(f"{power} is a secondary resource and reads plain — write it in "
                            f"`when` as a count, not in `bind` as a percent")
        if power not in PRIMARY:
            raise RuleError(f"unknown resource {power!r}; a percent bind reads `health%` or "
                            "one of " + ", ".join(sorted(PRIMARY)))
        if not 0 < pct < 100:
            raise RuleError(f"{power}% {m.group('cmp')} {pct:g} never changes; the threshold "
                            f"has to sit strictly between 0 and 100")
        return {"family": "power", "power": power, "cmp": m.group("cmp"), "percent": pct}
    head = text.split()[0] if text.split() else text
    bare = head.split(".")[0]
    # §6.6: the only sink is a percent curve, so a primary written as a bare number has no
    # form. Naming the missing `%` is the whole fix, so say that rather than "cannot read".
    if bare in PRIMARY:
        raise RuleError(f"{bare} is a primary resource and its only sink is a percent curve — "
                        f"write `{bare}% >= <n>`, not a bare count")
    if bare in SECONDARY:
        raise RuleError(f"{bare} is a secondary resource and reads plain — it belongs in "
                        f"`when`, not `bind`")
    raise RuleError(f"cannot read the bind {text!r}; the forms are "
                    + " | ".join(BIND_FORMS))


def parse(text: str):
    """Surface text -> the glow list the addon stores."""
    glows, current, scope = [], None, None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("--", 1)[0].strip()
        if not line:
            continue
        head, _, rest = line.partition(" ")
        head, rest = head.strip(), rest.strip()
        try:
            if head == "spec":
                scope = scope_key(rest)
            elif head == "glow":
                current = {"name": rest.strip('"')}
                glows.append(current)
            elif current is None:
                raise RuleError(f"{head!r} outside any glow")
            elif head == "on":
                current["subject"] = resolve(rest.split()[0], scope)
            elif head in ("when", "show"):
                parser = _Parser(_lex(rest), scope)
                current["when"] = parser.expression()
                if parser.peek()[0] != "end":
                    raise RuleError(f"trailing {parser.peek()[1]!r}")
            elif head in ("bind", "count"):
                current["bind"] = parse_bind(rest, scope)
            elif head == "color":
                current["color"] = rest.split()[0]
            elif head == "urgent":
                # A flag, not a value: `urgent` says a rung outranks the ordinary reading,
                # and the only levels are present and absent.
                if rest.strip():
                    raise RuleError(f"`urgent` takes nothing, found {rest.strip()!r}")
                current["urgent"] = True
            else:
                raise RuleError(f"unknown keyword {head!r}")
        except RuleError as exc:
            raise RuleError(f"line {lineno}: {exc}") from exc
    return glows


def render_expr(node, scope=None) -> str:
    if not isinstance(node, dict):
        return "?"
    kind = node.get("t")
    if kind in ("and", "or"):
        joined = f" {kind} ".join(render_expr(t, scope) for t in node["terms"])
        return f"({joined})"
    if kind == "not":
        return "not " + render_expr(node["term"], scope)
    if kind == "resource":
        suffix = ".after_cast" if node.get("projected") else ""
        return f"{node['power']}{suffix} {node['cmp']} {node['value']}"
    if kind in SPELL_CALLS:
        space = "aura" if kind in AURA_CALLS else "ability"
        return f"{kind}({name_of(node['spell'], scope, space)})"
    return str(kind)


def render_bind(bind, scope=None) -> str:
    if not isinstance(bind, dict):
        return "?"
    if bind.get("family") == "count":
        return f'{name_of(bind["aura"], scope, "aura")}.stacks >= {bind["threshold"]}'
    if bind.get("family") == "presence":
        # ⚠ The `presence` namespace, not `aura`: it prints a tracked row's bare name where
        # there is one, and `<slug>_<id>` for a rowless debuff the ability inventory carries.
        # Never a bare ability slug, which would re-parse to a different spell.
        body = f'{name_of(bind["aura"], scope, "presence")}.up'
        if bind.get("unit") != "player":
            body += f" on {bind['unit']}"
        if "PLAYER" in bind.get("filter", ""):
            body += " mine"
        return body
    if bind.get("family") == "duration":
        spell = name_of(bind["spell"], scope)
        if bind.get("cmp") == "outside":
            body = f"{spell}.cooldown outside {_secs(bind['lo'])}s..{_secs(bind['hi'])}s"
        else:
            body = f"{spell}.cooldown {bind['cmp']} {_secs(bind['seconds'])}s"
        return body + (f" absent {bind['absent']}" if bind.get("absent") else "")
    if bind.get("family") == "remains":
        return (f'{name_of(bind["aura"], scope, "aura")}.remains '
                f'{bind["cmp"]} {_secs(bind["seconds"])}s')
    if bind.get("family") == "health":
        return f"health% {bind['cmp']} {bind['percent']:g}"
    if bind.get("family") == "power":
        return f"{bind['power']}% {bind['cmp']} {bind['percent']:g}"
    return str(bind.get("family"))


def _secs(v) -> str:
    return f"{v:g}"


def render(glows, scope=None) -> str:
    lines = []
    if scope:
        lines += [f"spec {scope}", ""]
    for glow in glows:
        lines.append(f'glow "{glow.get("name", "")}"')
        lines.append(f"  on     {name_of(glow.get('subject'), scope)}")
        if glow.get("when") is not None:
            lines.append(f"  when   {render_expr(glow['when'], scope)}")
        if glow.get("bind") is not None:
            lines.append(f"  bind   {render_bind(glow['bind'], scope)}")
        if glow.get("color") is not None:
            lines.append(f"  color  {glow['color']}")
        if glow.get("urgent"):
            lines.append("  urgent")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ------------------------------------------------------------------- the refusals

def check(glows):
    """The checker's refusal list (rule-language.md §6). Returns a list of strings."""
    errs = []
    for i, glow in enumerate(glows, start=1):
        if not isinstance(glow.get("subject"), int):
            errs.append(f"glow {i}: needs `on <spell>`")
        if glow.get("when") is None and glow.get("bind") is None:
            errs.append(f"glow {i}: needs a `when` expression, a `bind`, or both")
        if glow.get("urgent") not in (None, True):
            errs.append(f"glow {i}: `urgent` is a flag; it is present or it is not")
        color = glow.get("color")
        if color is not None and color not in COLORS:
            errs.append(f"glow {i}: unknown colour {color!r}; known: {', '.join(sorted(COLORS))}")
        errs.extend(f"glow {i}: {e}" for e in _check_expr(glow.get("when")))
        errs.extend(f"glow {i}: {e}" for e in _check_bind(glow.get("bind"), glow.get("when")))
    return errs


def _check_expr(node):
    if node is None:
        return []
    if not isinstance(node, dict):
        return ["a term must be an object"]
    kind = node.get("t")
    if kind in ("and", "or"):
        out = []
        for sub in node.get("terms", []):
            out.extend(_check_expr(sub))
        return out
    if kind == "not":
        return _check_expr(node.get("term"))
    if kind == "resource":
        power = node.get("power")
        if power in PRIMARY:
            return [f"{power} is a primary resource, which is never readable — it belongs "
                    f"in `bind` as a percent, not in `when`"]
        if power not in SECONDARY:
            return [f"unknown resource {power!r}"]
        if node.get("cmp") not in COMPARISONS:
            return [f"unknown comparison {node.get('cmp')!r}"]
        if node.get("projected") and power not in PROJECTABLE:
            return [f"{power} cannot be read past the current cast — what a cast returns "
                    f"depends on talents and procs for every resource but soul_shards, so "
                    f"there is no one number to project with"]
        return []
    if kind in WHEN_TERMS:
        if not isinstance(node.get("spell"), int):
            return [f"{kind}() needs a spell"]
        return []
    if kind == "charges":
        return ["a charge COUNT is neither readable nor sealed; use ready() instead"]
    if kind in BIND_FAMILIES:
        return [f"{kind} is a sealed term and belongs in `bind`, not in `when`"]
    return [f"unknown term {kind!r}"]


def _check_bind(bind, when):
    if bind is None:
        return []
    if not isinstance(bind, dict):
        return ["a bind must be an object"]
    family = bind.get("family")
    if family in WHEN_TERMS:
        return [f"{family} is readable and belongs in `when`, not in `bind`"]
    if family == "count":
        if not isinstance(bind.get("aura"), int) or not isinstance(bind.get("threshold"), int):
            return ["a count bind needs an aura and a numeric threshold"]
        return []
    if family == "presence":
        if not isinstance(bind.get("aura"), int):
            return ["a presence bind needs a numeric aura id"]
        if bind.get("unit") not in _PRESENCE_UNITS:
            return [f"unknown unit {bind.get('unit')!r}; a presence bind reads "
                    "`player` or `target`"]
        # AuraUtil.IsValidFilterString ASSERTS, so an unknown component is a hard error inside
        # AddAuraSlot rather than an empty result. Refuse it here instead.
        bad = [c for c in str(bind.get("filter", "")).split("|")
               if c not in {"HELPFUL", "HARMFUL", "PLAYER"}]
        if bad:
            return [f"unknown aura filter {bad[0]!r}"]
        return []
    if family == "duration":
        if not isinstance(bind.get("spell"), int):
            return ["a duration bind needs a spell"]
        cmp_ = bind.get("cmp")
        if cmp_ == "outside":
            if not isinstance(bind.get("lo"), (int, float)) or not isinstance(bind.get("hi"), (int, float)):
                return ["`outside` needs two bounds"]
        elif cmp_ not in COMPARISONS - {"=="}:
            return [f"unknown duration comparison {cmp_!r}"]
        elif not isinstance(bind.get("seconds"), (int, float)):
            return ["a duration bind needs a number of seconds"]
        if cmp_ in UNBOUNDED_BELOW and not bind.get("absent") and not _guards_ready(when, bind["spell"]):
            return [f"`{cmp_}` on a cooldown is also true when the spell is READY, so this "
                    f"would glow permanently while it is up. Add `not ready(...)` to `when`, "
                    f"or say `absent dark` / `absent show` on the bind"]
        return []
    if family == "remains":
        if not isinstance(bind.get("aura"), int):
            return ["a remains bind needs a numeric aura id"]
        if bind.get("cmp") not in COMPARISONS - {"=="}:
            return [f"unknown remains comparison {bind.get('cmp')!r}"]
        secs = bind.get("seconds")
        if not isinstance(secs, (int, float)) or secs <= 0:
            return ["a remains bind needs a positive number of seconds"]
        return []
    if family == "health":
        if bind.get("cmp") not in COMPARISONS - {"=="}:
            return [f"unknown health comparison {bind.get('cmp')!r}"]
        pct = bind.get("percent")
        if not isinstance(pct, (int, float)) or not 0 < pct < 100:
            return ["a health bind needs a percent strictly between 0 and 100"]
        return []
    if family == "power":
        if bind.get("power") not in PRIMARY:
            return [f"{bind.get('power')!r} is not a primary resource; a power bind reads "
                    "one of " + ", ".join(sorted(PRIMARY))]
        if bind.get("cmp") not in COMPARISONS - {"=="}:
            return [f"unknown power comparison {bind.get('cmp')!r}"]
        pct = bind.get("percent")
        if not isinstance(pct, (int, float)) or not 0 < pct < 100:
            return ["a power bind needs a percent strictly between 0 and 100"]
        return []
    return [f"unknown bind family {family!r}"]


def _guards_ready(node, spell) -> bool:
    """Is `not ready(<spell>)` somewhere in the readable half? Only a conjunction counts —
    a disjunct leaves a path where the guard is false and the bind still drives."""
    if not isinstance(node, dict):
        return False
    if node.get("t") == "and":
        return any(_guards_ready(t, spell) for t in node.get("terms", []))
    if node.get("t") == "not":
        inner = node.get("term")
        return isinstance(inner, dict) and inner.get("t") == "ready" and inner.get("spell") == spell
    return False


# ------------------------------------------------------------------- the commands

def _read(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def cmd_encode(args) -> int:
    glows = parse(_read(args.source))
    errs = check(glows)
    if errs:
        for err in errs:
            print(f"refused: {err}", file=sys.stderr)
        return 1
    print(encode(glows))
    return 0


def cmd_decode(args) -> int:
    glows = decode(args.string)
    scope = scope_key(args.spec) if args.spec else None
    if args.json:
        print(json.dumps(glows, indent=2))
    else:
        print(render(glows, scope), end="")
    errs = check(glows)
    for err in errs:
        print(f"refused: {err}", file=sys.stderr)
    return 1 if errs else 0


def cmd_check(args) -> int:
    glows = parse(_read(args.source))
    errs = check(glows)
    for err in errs:
        print(f"refused: {err}")
    if errs:
        return 1
    print(f"ok — {len(glows)} glows")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m wowkb.smartglo",
        description="Smart Glo rules: surface text, AST and wire string.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("encode", help="surface text -> a paste-able SG1: string")
    p.add_argument("source", help="a .sg file, or - for stdin")
    p.set_defaults(fn=cmd_encode)

    p = sub.add_parser("decode", help="an SG1: string -> surface text")
    p.add_argument("string")
    p.add_argument("--json", action="store_true", help="print the AST instead")
    p.add_argument("--spec", help="render bare spell names in this spec's scope")
    p.set_defaults(fn=cmd_decode)

    p = sub.add_parser("check", help="parse and report the checker's refusals")
    p.add_argument("source", help="a .sg file, or - for stdin")
    p.set_defaults(fn=cmd_check)

    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except RuleError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
