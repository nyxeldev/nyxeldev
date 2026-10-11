# -*- coding: utf-8 -*-
"""Generates the SVG assets used by the profile README.

    python tools/make_assets.py

Writes assets/header-{dark,light}.svg and assets/architecture-{dark,light}.svg.
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


# ── header ───────────────────────────────────────────────────────────────────

HEADER_H = 172
PAD = 28
COLS, ROWS, GAP, TOP = 11, 4, 22, 52


def header(c):
    dots = []
    x0 = (W - PAD) - (COLS - 1) * GAP
    for r in range(ROWS):
        for i in range(COLS):
            cx, cy = x0 + i * GAP, TOP + r * GAP
            lit = (i == COLS - 1 and r == 1)
            dots.append(
                '<circle cx="%d" cy="%d" r="%s" fill="%s" fill-opacity="%s"/>'
                % (cx, cy, 2.6 if lit else 2.2,
                   c["accent"] if lit else c["dot"],
                   1.0 if lit else round(0.42 + 0.58 * (i / (COLS - 1)), 3))
            )
    return """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Jahongir Hamidov - full-stack engineer, Tashkent, Uzbekistan">
  <g font-family="{mono}">
    <text x="{pad}" y="82" font-size="30" font-weight="500" letter-spacing="6" fill="{text}">JAHONGIR HAMIDOV</text>
    <text x="{pad2}" y="112" font-size="11.5" letter-spacing="3" fill="{muted}">FULL-STACK ENGINEER &#183; TASHKENT, UZBEKISTAN</text>
  </g>
  <g>
    {dots}
  </g>
  <line x1="{pad}" y1="146" x2="{x2}" y2="146" stroke="{rule}" stroke-width="1"/>
</svg>
""".format(w=W, h=HEADER_H, mono=MONO, pad=PAD, pad2=PAD + 2, x2=W - PAD,
           dots="\n    ".join(dots), **c)


# ── architecture ─────────────────────────────────────────────────────────────

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

PATHS = [
    "M160 125 H205 V58 H250",
    "M160 125 H250",
    "M375 147 V170",
    "M500 125 H560 V102 H620",
    "M500 125 H560 V170 H620",
]


def architecture(c):
    parts = []
    for d in PATHS:
        parts.append('<path d="%s" fill="none" stroke="%s" stroke-width="1"/>' % (d, c["line"]))
    for x, y, w, h, title, sub in BOXES:
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="none" stroke="%s" stroke-width="1"/>'
                     % (x, y, w, h, c["rule"]))
        if sub is None:
            parts.append('<text x="%d" y="%d" font-size="12" letter-spacing="0.4" fill="%s">%s</text>'
                         % (x + 14, y + h / 2 + 4, c["text"], title))
        else:
            parts.append('<text x="%d" y="%d" font-size="12" letter-spacing="0.4" fill="%s">%s</text>'
                         % (x + 14, y + 19, c["text"], title))
            parts.append('<text x="%d" y="%d" font-size="10.5" letter-spacing="0.3" fill="%s">%s</text>'
                         % (x + 14, y + 34, c["muted"], sub))
    return """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="seasmp architecture: nginx in front of a Next.js web client, a Fastify TypeScript API and a Python FastAPI analytics service, backed by PostgreSQL and Redis">
  <g font-family="{mono}" transform="translate(0,-16)">
    {body}
  </g>
</svg>
""".format(w=W, h=ARCH_H, mono=MONO, body="\n    ".join(parts))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, c in THEMES.items():
        for kind, svg in (("header", header(c)), ("architecture", architecture(c))):
            path = os.path.join(OUT, "%s-%s.svg" % (kind, name))
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)
            print("wrote", os.path.relpath(path, ROOT))
