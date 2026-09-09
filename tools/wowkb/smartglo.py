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
"""

import argparse
import base64
import json
import re
import sys
import zlib
from pathlib import Path

PREFIX = "SG1:"

SECONDARY = {
    "soul_shards", "holy_power", "combo_points", "chi",
    "arcane_charges", "essence", "runes",
}

PRIMARY = {
    "mana", "rage", "focus", "energy", "runic_power",
    "fury", "pain", "insanity", "maelstrom",
}

COMPARISONS = {">=", ">", "<=", "<", "=="}

# The palette tool/gen_media.py bakes. A gate tints the white master at runtime; a count
# names one of these files, because a band's inline texture escape cannot be tinted.
COLORS = {"white", "yellow", "red", "green", "blue", "purple", "orange", "cyan"}


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
    return json.loads(envelope["j"])


# -------------------------------------------------------------- the surface text

TOKEN = re.compile(r"""
    (?P<ws>\s+)
  | (?P<comment>--[^\n]*)
  | (?P<number>\d+)
  | (?P<name>[A-Za-z_][A-Za-z_0-9]*)
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
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

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
        if text in ("ready", "aura"):
            self.expect("(")
            spell = self.take()
            if spell[0] != "number":
                raise RuleError(f"{text}() takes a spell id, found {spell[1]!r}")
            self.expect(")")
            return {"t": text, "spell": int(spell[1])}
        if text in PRIMARY:
            raise RuleError(f"{text} is a primary resource and can never be a gate")
        if text not in SECONDARY:
            raise RuleError(f"unknown term {text!r}")
        cmp_kind, cmp_text = self.take()
        if cmp_kind != "cmp" or cmp_text not in COMPARISONS:
            raise RuleError(f"expected a comparison after {text}, found {cmp_text!r}")
        value = self.take()
        if value[0] != "number":
            raise RuleError(f"expected a number after {cmp_text}, found {value[1]!r}")
        return {"t": "resource", "power": text, "cmp": cmp_text, "value": int(value[1])}


def parse(text: str):
    """Surface text -> the glow list the addon stores."""
    glows, current = [], None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("--", 1)[0].strip()
        if not line:
            continue
        head, _, rest = line.partition(" ")
        head, rest = head.strip(), rest.strip()
        try:
            if head == "glow":
                current = {"name": rest.strip('"')}
                glows.append(current)
            elif current is None:
                raise RuleError(f"{head!r} outside any glow")
            elif head == "on":
                current["subject"] = int(rest.split()[0])
            elif head == "show":
                parser = _Parser(_lex(rest))
                current["show"] = parser.expression()
                if parser.peek()[0] != "end":
                    raise RuleError(f"trailing {parser.peek()[1]!r}")
            elif head == "color":
                current["color"] = rest.split()[0]
            elif head == "count":
                m = re.match(r"(?:count\()?(\d+)\)?\s*>=\s*(\d+)$", rest)
                if m is None:
                    raise RuleError("count takes the form `count count(<aura>) >= <n>`")
                current["count"] = {"aura": int(m.group(1)), "threshold": int(m.group(2))}
            else:
                raise RuleError(f"unknown keyword {head!r}")
        except RuleError as exc:
            raise RuleError(f"line {lineno}: {exc}") from exc
    return glows


def render_expr(node) -> str:
    if not isinstance(node, dict):
        return "?"
    kind = node.get("t")
    if kind in ("and", "or"):
        joined = f" {kind} ".join(render_expr(t) for t in node["terms"])
        return f"({joined})"
    if kind == "not":
        return "not " + render_expr(node["term"])
    if kind == "resource":
        return f"{node['power']} {node['cmp']} {node['value']}"
    if kind in ("ready", "aura"):
        return f"{kind}({node['spell']})"
    return str(kind)


def render(glows) -> str:
    lines = []
    for glow in glows:
        lines.append(f'glow "{glow.get("name", "")}"')
        lines.append(f"  on     {glow.get('subject')}")
        if glow.get("show") is not None:
            lines.append(f"  show   {render_expr(glow['show'])}")
        if glow.get("count") is not None:
            lines.append(f"  count  count({glow['count']['aura']}) >= {glow['count']['threshold']}")
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
            errs.append(f"glow {i}: needs `on <spell id>`")
        if glow.get("show") is None and glow.get("count") is None:
            errs.append(f"glow {i}: needs a `show` expression, a `count` element, or both")
        color = glow.get("color")
        if color is not None and color not in COLORS:
            errs.append(f"glow {i}: unknown colour {color!r}; known: {', '.join(sorted(COLORS))}")
        count = glow.get("count")
        if count is not None:
            if not isinstance(count.get("aura"), int) or not isinstance(count.get("threshold"), int):
                errs.append(f"glow {i}: a count element needs a numeric aura and threshold")
        errs.extend(f"glow {i}: {e}" for e in _check_expr(glow.get("show")))
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
            return [f"{power} is a primary resource and can never be a gate"]
        if power not in SECONDARY:
            return [f"unknown resource {power!r}"]
        if node.get("cmp") not in COMPARISONS:
            return [f"unknown comparison {node.get('cmp')!r}"]
        return []
    if kind in ("ready", "aura"):
        if not isinstance(node.get("spell"), int):
            return [f"{kind}() needs a spell id"]
        return []
    if kind == "charges":
        return ["a charge COUNT is neither a gate nor a binding"]
    if kind == "count":
        return ["a count is a sealed binding and cannot appear inside an expression"]
    return [f"unknown term {kind!r}"]


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
    if args.json:
        print(json.dumps(glows, indent=2))
    else:
        print(render(glows), end="")
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
