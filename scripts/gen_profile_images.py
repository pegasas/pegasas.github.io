#!/usr/bin/env python3
"""Generate profile / site infographics (SVG) from pegasas-notes-v2.

Outputs to assets/images/profile/ and is meant to be re-run together with
sync_notes.py, so the GitHub profile README (which embeds these URLs) and the
site stay in step with the notes repo.

  python3 scripts/gen_profile_images.py --source ~/pegasas-notes-v2
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from xml.sax.saxutils import escape

SITE_ROOT = Path(__file__).resolve().parent.parent
OUT = SITE_ROOT / "assets/images/profile"

GREEN, ORANGE, BLUE, VIOLET = "#7bd43c", "#ff7a1f", "#3d9bff", "#9a6bff"
BG, TEXT, MUTED, LINE = "#07080b", "#e9edf4", "#98a2b3", "#1b2230"
FONT = '-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Inter,Helvetica,Arial,sans-serif'

# (path under knowledge/, English label, group)
DOMAINS = [
    ("algorithm", "Algorithms & Math", "Foundations"),
    ("language/cpp", "C/C++", "Foundations"),
    ("language/java", "Java / JVM", "Foundations"),
    ("language/go", "Go", "Foundations"),
    ("language/python", "Python", "Foundations"),
    ("language/rust", "Rust", "Foundations"),
    ("os/linux", "Linux", "Systems"),
    ("web", "Web & Browser", "Systems"),
    ("distributed", "Distributed Systems", "Systems"),
    ("data-systems", "Data Systems", "Systems"),
    ("cloud-native", "Cloud Native", "Systems"),
    ("ai-models", "AI/ML & Models", "AI"),
    ("physical-ai", "Physical AI", "AI"),
    ("accelerators", "Accelerators & GPU", "AI"),
    ("ai-infra", "AI Infra", "AI"),
    ("agent", "Agents", "AI"),
]
GROUP_COLOR = {"Foundations": GREEN, "Systems": BLUE, "AI": ORANGE}

PATHS = [
    ("Systems", GREEN, ["C/C++", "Linux", "Networking", "Distributed", "Data Systems"]),
    ("Backend", BLUE, ["Java · Go · Python · Rust", "Data Systems", "Cloud Native"]),
    ("Data Eng", VIOLET, ["Distributed", "Kafka · Spark · Flink", "Data Systems"]),
    ("AI Infra", ORANGE, ["Python / C++", "Model Mechanics", "Accelerators", "Training & Inference", "Clusters"]),
    ("Agents", GREEN, ["Model Basics", "State & Tools", "RAG · Memory", "Evaluation"]),
    ("Physical AI", BLUE, ["AI / ML", "Perception & Action", "Simulation", "Control"]),
]


def count(source: Path, rel: str) -> int:
    return sum(1 for p in (source / "knowledge" / rel).rglob("*.md")
               if not any(part.startswith((".", "_")) for part in p.parts))


def frame(w: int, h: int, title: str, subtitle: str, body: str, accent_line: bool = True) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<defs>
<radialGradient id="ga" cx="0%" cy="0%" r="60%"><stop offset="0" stop-color="{GREEN}" stop-opacity=".22"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>
<radialGradient id="gb" cx="100%" cy="100%" r="60%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".22"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".3" stop-color="{GREEN}"/><stop offset=".65" stop-color="{BLUE}"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient>
<clipPath id="r"><rect width="{w}" height="{h}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#r)" font-family="{FONT}">
<rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#ga)"/><rect width="{w}" height="{h}" fill="url(#gb)"/>
{f'<rect y="{h-2}" width="{w}" height="2" fill="url(#ln)"/>' if accent_line else ''}
<text x="40" y="58" font-size="13" font-weight="800" letter-spacing="2.5" fill="{GREEN}">{escape(subtitle.upper())}</text>
<text x="40" y="92" font-size="28" font-weight="900" fill="#fff">{escape(title)}</text>
{body}
</g>
</svg>
'''


def squarify(items, x, y, w, h):
    """Squarified treemap. items: list of (value, payload) sorted desc."""
    tot = sum(v for v, _ in items)
    out, items = [], [(v * w * h / tot, p) for v, p in items]  # values -> pixel areas
    while items:
        short = min(w, h)
        row, rest = [items[0]], items[1:]

        def worst(r):
            s = sum(v for v, _ in r)
            return max(max(short * short * v / (s * s), (s * s) / (short * short * v)) for v, _ in r)
        while rest and worst(row + [rest[0]]) <= worst(row):
            row.append(rest.pop(0))
        s = sum(v for v, _ in row)
        total = s + sum(v for v, _ in rest)
        if w >= h:
            rw = w * s / total
            cy = y
            for v, p in row:
                rh = h * v / s
                out.append((x, cy, rw, rh, p)); cy += rh
            x, w = x + rw, w - rw
        else:
            rh = h * s / total
            cx = x
            for v, p in row:
                rw = w * v / s
                out.append((cx, y, rw, rh, p)); cx += rw
            y, h = y + rh, h - rh
        items = rest
    return out


def knowledge_map(data, total) -> str:
    W, H = 1200, 600
    items = sorted(((c ** 0.62, (label, group, c)) for _, label, group, c in data), reverse=True)
    tiles = []
    for x, y, w, h, (label, group, c) in squarify(items, 40, 130, W - 80, H - 170):
        col, g = GROUP_COLOR[group], 4
        x, y, w, h = x + g / 2, y + g / 2, w - g, h - g
        fs = max(12, min(22, int(min((w - 24) / (len(label) * .62), h / 3.2))))
        nfs = max(14, min(40, int(min(w / 3.6, h / 2.4))))
        tiles.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-opacity=".55"/>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="3" rx="1.5" fill="{col}"/>'
            f'<text x="{x + 14:.1f}" y="{y + 14 + nfs:.1f}" font-size="{nfs}" font-weight="900" fill="#fff">{c}</text>'
            f'<text x="{x + 14:.1f}" y="{y + 26 + nfs + fs:.1f}" font-size="{fs}" font-weight="600" fill="{TEXT}" fill-opacity=".85">{escape(label)}</text>')
    legend, lx = [], W - 40
    for group in ("AI", "Systems", "Foundations"):
        n = sum(c for _, _, g, c in data if g == group)
        txt = f"{group} · {n}"
        lx -= len(txt) * 8.2 + 34
        legend.append(f'<rect x="{lx:.0f}" y="80" width="12" height="12" rx="3" fill="{GROUP_COLOR[group]}"/>'
                      f'<text x="{lx + 20:.0f}" y="91" font-size="14" fill="{MUTED}">{escape(txt)}</text>')
    return frame(W, H, f"{total:,} notes across {len(data)} domains", "Knowledge Map", "".join(tiles + legend))


def coverage(data) -> str:
    rows = sorted(data, key=lambda d: -d[3])
    W, top, rh = 1200, 130, 30
    H = top + rh * len(rows) + 30
    mx = rows[0][3]
    lw, bx, bw = 230, 290, W - 290 - 110
    body = []
    for i, (_, label, group, c) in enumerate(rows):
        y = top + i * rh
        col = GROUP_COLOR[group]
        w = max(6, bw * c / mx)
        body.append(
            f'<text x="{40 + lw:.0f}" y="{y + 19}" text-anchor="end" font-size="15" font-weight="600" fill="{TEXT}">{escape(label)}</text>'
            f'<rect x="{bx}" y="{y + 6}" width="{bw}" height="16" rx="8" fill="#fff" fill-opacity=".04"/>'
            f'<rect x="{bx}" y="{y + 6}" width="{w:.1f}" height="16" rx="8" fill="{col}"/>'
            f'<text x="{bx + w + 12:.1f}" y="{y + 19}" font-size="14" font-weight="800" fill="#fff">{c}</text>')
    return frame(W, H, "Where the notes go deepest", "Coverage", "".join(body))


def learning_paths() -> str:
    W, top, rh = 1200, 132, 62
    H = top + rh * len(PATHS) + 24
    body = []
    for i, (name, col, steps) in enumerate(PATHS):
        y = top + i * rh
        body.append(f'<text x="40" y="{y + 27}" font-size="15" font-weight="900" fill="{col}" letter-spacing="1">{escape(name.upper())}</text>')
        x = 190
        for j, step in enumerate(steps):
            w = len(step) * 8.6 + 34
            body.append(f'<rect x="{x:.0f}" y="{y + 6}" width="{w:.0f}" height="32" rx="16" fill="{col}" fill-opacity="{.10 + .05 * j:.2f}" stroke="{col}" stroke-opacity=".6"/>'
                        f'<text x="{x + w / 2:.0f}" y="{y + 27}" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">{escape(step)}</text>')
            x += w
            if j < len(steps) - 1:
                body.append(f'<path d="M{x + 8:.0f} {y + 22} h18 m-6 -5 l6 5 l-6 5" fill="none" stroke="{MUTED}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
                x += 34
    return frame(W, H, "Learning paths by goal", "Roadmaps", "".join(body))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=os.environ.get("NOTES_SOURCE", str(Path.home() / "pegasas-notes-v2")))
    src = Path(ap.parse_args().source).expanduser()
    data = [(p, label, g, count(src, p)) for p, label, g in DOMAINS]
    total = sum(d[3] for d in data)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in (("knowledge-map.svg", knowledge_map(data, total)),
                      ("coverage.svg", coverage(data)),
                      ("learning-paths.svg", learning_paths())):
        (OUT / name).write_text(svg)
        print("wrote", (OUT / name).relative_to(SITE_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
