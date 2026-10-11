# -*- coding: utf-8 -*-
"""Generates the SVG assets used by the profile README.

    python tools/make_assets.py

Writes assets/header-{dark,light}.svg and assets/architecture-{dark,light}.svg.

The motion is deliberately slow and low-contrast: a one-off reveal when the image
loads, then a single looping gesture per asset. Everything stops under
prefers-reduced-motion.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

THEMES = {
    "dark":  dict(text="#f0f6fc", muted="#8b949e", rule="#262c36",
                  dot="#3b424c", line="#3b424c", accent="#a78bfa"),
    "light": dict(text="#1f2328", muted="#59636e", rule="#d1d9e0",
                  dot="#c4ccd6", line="#c4ccd6", accent="#7c3aed"),
}

MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace"
W = 940
NAME = "JAHONGIR HAMIDOV"
SUBTITLE = "FULL-STACK ENGINEER · TASHKENT, UZBEKISTAN"


# -- header -------------------------------------------------------------------

HEADER_H = 172
PAD = 28
COLS, ROWS, GAP, TOP = 11, 4, 22, 52
RULE_LEN = W - 2 * PAD

HEADER_CSS = """
    .ch   {{ animation: rise .5s cubic-bezier(.2,.7,.3,1) backwards; }}
    .sub  {{ animation: rise .7s ease .62s backwards; }}
    .rule {{ stroke-dasharray: {rule_len}; animation: draw 1.4s cubic-bezier(.33,0,.2,1) .18s backwards; }}
    .d    {{ animation: wave 9s ease-in-out infinite; }}
    .lit  {{ animation: pulse 3.6s ease-in-out infinite; }}
    @keyframes rise  {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    @keyframes draw  {{ from {{ stroke-dashoffset: {rule_len} }} to {{ stroke-dashoffset: 0 }} }}
    @keyframes wave  {{ 0%, 100% {{ opacity: .7 }} 45% {{ opacity: 1 }} }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 1 }} 50% {{ opacity: .42 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .ch, .sub, .rule, .d, .lit {{ animation: none; stroke-dashoffset: 0 }}
    }}
"""


def header(c):
    # the name is drawn character by character so it can fade in as a sequence
    chars = []
    for i, ch in enumerate(NAME):
        if ch == " ":
            continue
        chars.append(
            '<tspan class="ch" x="%s" style="animation-delay:%.2fs">%s</tspan>'
            % (PAD + i * 20.0, 0.16 + i * 0.035, ch)
        )

    dots = []
    x0 = (W - PAD) - (COLS - 1) * GAP
    for r in range(ROWS):
        for i in range(COLS):
            cx, cy = x0 + i * GAP, TOP + r * GAP
            lit = (i == COLS - 1 and r == 1)
            dots.append(
                '<circle class="%s" cx="%d" cy="%d" r="%s" fill="%s" fill-opacity="%s" style="animation-delay:-%.2fs"/>'
                % ("lit" if lit else "d", cx, cy, 2.6 if lit else 2.2,
                   c["accent"] if lit else c["dot"],
                   1.0 if lit else round(0.42 + 0.58 * (i / (COLS - 1)), 3),
                   i * 0.42 + r * 0.2)
            )

    return """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Jahongir Hamidov - full-stack engineer, Tashkent, Uzbekistan">
  <style>{css}  </style>
  <g font-family="{mono}">
    <text y="82" font-size="30" font-weight="500" fill="{text}">{chars}</text>
    <text class="sub" x="{pad2}" y="112" font-size="11.5" letter-spacing="3" fill="{muted}">{subtitle}</text>
  </g>
  <g>
    {dots}
  </g>
  <line class="rule" x1="{pad}" y1="146" x2="{x2}" y2="146" stroke="{rule}" stroke-width="1"/>
</svg>
""".format(w=W, h=HEADER_H, mono=MONO, pad=PAD, pad2=PAD + 2, x2=W - PAD,
           css=HEADER_CSS.format(rule_len=RULE_LEN), chars="".join(chars),
           subtitle=SUBTITLE, dots="\n    ".join(dots), **c)


# -- architecture --------------------------------------------------------------

ARCH_H = 210

BOXES = [
    # x, y, w, h, title, subtitle
    (40,  103, 120, 44, "nginx",     "reverse proxy"),
    (250,  36, 250, 44, "web",       "Next.js 16 · shadcn/ui"),
    (250, 103, 250, 44, "api",       "Fastify · TypeScript · Prisma"),
    (250, 170, 250, 44, "analytics", "FastAPI · scikit-learn"),
    (620,  82, 170, 40, "PostgreSQL 17", None),
    (620, 150, 170, 40, "Redis 7.4",     None),
]

# path, delay of the travelling highlight
PATHS = [
    ("M160 125 H205 V58 H250",  0.0),
    ("M160 125 H250",           0.9),
    ("M375 147 V170",           2.4),
    ("M500 125 H560 V102 H620", 1.5),
    ("M500 125 H560 V170 H620", 3.0),
]

ARCH_CSS = """
    .b {{ animation: appear .55s ease backwards; }}
    .w {{ animation: draw 1s cubic-bezier(.4,0,.2,1) backwards; }}
    .f {{ stroke: {accent}; stroke-width: 1.4; opacity: .5;
          animation: flow linear infinite; }}
    @keyframes appear {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    @keyframes draw   {{ from {{ stroke-dashoffset: var(--len) }} to {{ stroke-dashoffset: 0 }} }}
    @keyframes flow   {{ from {{ stroke-dashoffset: var(--travel) }} to {{ stroke-dashoffset: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{
      .b, .w {{ animation: none }}
      .f {{ display: none }}
    }}
"""


def path_len(d):
    """Length of an H/V-only path."""
    toks = d.replace("M", "").split()
    x, y = float(toks[0]), float(toks[1])
    total, i = 0.0, 2
    while i < len(toks):
        cmd = toks[i][0]
        inline = toks[i][1:]
        val = float(inline) if inline else float(toks[i + 1])
        i += 1 if inline else 2
        if cmd == "H":
            total += abs(val - x)
            x = val
        else:
            total += abs(val - y)
            y = val
    return total


def architecture(c):
    parts = []
    for n, (d, flow_delay) in enumerate(PATHS):
        ln = path_len(d)
        parts.append(
            '<path class="w" d="%s" fill="none" stroke="%s" stroke-width="1" '
            'style="--len:%d;stroke-dasharray:%d;animation-delay:%.2fs"/>'
            % (d, c["line"], ln, ln, 0.25 + n * 0.12))
        # one highlight glides along the line, then the line rests: the dash
        # travels further than the path is long, at a constant 55 px/s
        travel = ln + 170
        parts.append(
            '<path class="f" d="%s" fill="none" '
            'style="--travel:%d;stroke-dasharray:5 %d;'
            'animation-duration:%.1fs;animation-delay:%.1fs"/>'
            % (d, travel, travel, travel / 55.0, flow_delay))

    for n, (x, y, w, h, title, sub) in enumerate(BOXES):
        parts.append('<g class="b" style="animation-delay:%.2fs">' % (0.1 + n * 0.09))
        parts.append(
            '<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="none" stroke="%s" stroke-width="1"/>'
            % (x, y, w, h, c["rule"]))
        if sub is None:
            parts.append('<text x="%d" y="%d" font-size="12" letter-spacing="0.4" fill="%s">%s</text>'
                         % (x + 14, y + h / 2 + 4, c["text"], title))
        else:
            parts.append('<text x="%d" y="%d" font-size="12" letter-spacing="0.4" fill="%s">%s</text>'
                         % (x + 14, y + 19, c["text"], title))
            parts.append('<text x="%d" y="%d" font-size="10.5" letter-spacing="0.3" fill="%s">%s</text>'
                         % (x + 14, y + 34, c["muted"], sub))
        parts.append("</g>")

    return """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="seasmp architecture: nginx in front of a Next.js web client, a Fastify TypeScript API and a Python FastAPI analytics service, backed by PostgreSQL and Redis">
  <style>{css}  </style>
  <g font-family="{mono}" transform="translate(0,-16)">
    {body}
  </g>
</svg>
""".format(w=W, h=ARCH_H, mono=MONO, css=ARCH_CSS.format(accent=c["accent"]),
           body="\n    ".join(parts))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, c in THEMES.items():
        for kind, svg in (("header", header(c)), ("architecture", architecture(c))):
            path = os.path.join(OUT, "%s-%s.svg" % (kind, name))
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)
            print("wrote", os.path.relpath(path, ROOT))
