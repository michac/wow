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
    "fury", "pain", "insanity", "maelstrom",
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
COLORS = {"white", "yellow", "red", "green", "blue", "purple", "orange", "cyan"}

# Which bowl each readable term goes in, and the sealed families the other bowl takes.
WHEN_TERMS = {"resource", "ready", "aura", "talent"}
BIND_FAMILIES = {"count", "duration", "health"}

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


def _spec_index(key: str) -> dict:
    symbols = load_symbols()
    return {symbols["names"][i]: i for i in symbols["specs"][key]
            if i in symbols["names"]}


def resolve(text: str, scope) -> int:
    """A spell reference: a raw id, `class.spec.name`, or a bare name inside `scope`."""
    text = text.strip().lower()
    if re.fullmatch(r"\d+", text):
        return int(text)
    if not text:
        raise RuleError("a spell name or id is required")
    parts = text.split(".")
    if len(parts) == 3:
        key = scope_key(f"{parts[0]}.{parts[1]}")
        found = _spec_index(key).get(parts[2])
        if found is None:
            raise RuleError(f"{key} has no {parts[2]!r}")
        return found
    if len(parts) != 1:
        raise RuleError(f"{text!r} is not a name; write <class>.<spec>.<name>, "
                        "a bare name, or an id")
    if scope is None:
        raise RuleError(f"{text!r} needs a scope — put `spec demonology` above the rules, "
                        f"or write warlock.demonology.{text}, or a raw spell id")
    found = _spec_index(scope).get(text)
    if found is None:
        raise RuleError(f"{scope} has no {text!r}")
    return found


def name_of(spell_id: int, scope) -> str:
    """How a rule should spell an id back. Bare inside its own scope, qualified when the
    id belongs to another spec, and the number itself when nothing names it — an override
    id such as Ruination is a real subject and is in no spec inventory."""
    symbols = load_symbols()
    name = symbols["names"].get(spell_id)
    if name is None:
        return str(spell_id)
    if scope is not None and spell_id in symbols["specs"].get(scope, ()):
        return name
    for key, ids in symbols["specs"].items():
        if spell_id in ids:
            return f"{key}.{name}"
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
        if text in ("ready", "aura", "talent"):
            self.expect("(")
            ref = self.take()
            if ref[0] not in ("name", "number"):
                raise RuleError(f"{text}() takes a spell name or id, found {ref[1]!r}")
            self.expect(")")
            return {"t": text, "spell": resolve(ref[1], self.scope)}
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

_HEALTH = re.compile(r"^health%\s*(?P<cmp>>=|<=|>|<)\s*(?P<n>[\d.]+)$")

BIND_FORMS = ("<spell>.stacks >= <n>", "<spell>.cooldown > <n>s",
              "<spell>.cooldown outside <a>s..<b>s", "health% < <n>")


def _absent(rest: str) -> dict:
    rest = rest.strip()
    if not rest:
        return {}
    word = rest.split()
    if len(word) != 2 or word[0] != "absent" or word[1] not in ("dark", "show"):
        raise RuleError(f"trailing {rest!r}; the only tail a bind takes is "
                        "`absent dark` or `absent show`")
    return {"absent": word[1]}


def parse_bind(text: str, scope) -> dict:
    m = _STACKS.match(text) or _COUNT.match(text)
    if m:
        return {"family": "count", "aura": resolve(m.group("spell"), scope),
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
    m = _HEALTH.match(text)
    if m:
        pct = float(m.group("n"))
        if not 0 < pct < 100:
            raise RuleError(f"health% {m.group('cmp')} {pct:g} never changes; the threshold "
                            f"has to sit strictly between 0 and 100")
        return {"family": "health", "cmp": m.group("cmp"), "percent": pct}
    head = text.split()[0] if text.split() else text
    bare = head.split(".")[0]
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
    if kind in ("ready", "aura", "talent"):
        return f"{kind}({name_of(node['spell'], scope)})"
    return str(kind)


def render_bind(bind, scope=None) -> str:
    if not isinstance(bind, dict):
        return "?"
    if bind.get("family") == "count":
        return f"{name_of(bind['aura'], scope)}.stacks >= {bind['threshold']}"
    if bind.get("family") == "duration":
        spell = name_of(bind["spell"], scope)
        if bind.get("cmp") == "outside":
            body = f"{spell}.cooldown outside {_secs(bind['lo'])}s..{_secs(bind['hi'])}s"
        else:
            body = f"{spell}.cooldown {bind['cmp']} {_secs(bind['seconds'])}s"
        return body + (f" absent {bind['absent']}" if bind.get("absent") else "")
    if bind.get("family") == "health":
        return f"health% {bind['cmp']} {bind['percent']:g}"
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
    if family == "health":
        if bind.get("cmp") not in COMPARISONS - {"=="}:
            return [f"unknown health comparison {bind.get('cmp')!r}"]
        pct = bind.get("percent")
        if not isinstance(pct, (int, float)) or not 0 < pct < 100:
            return ["a health bind needs a percent strictly between 0 and 100"]
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
