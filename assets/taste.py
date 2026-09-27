"""The rung 1 figure in the README, drawn from experiments/shiu_rewiring.json (nothing is drawn by hand).

    python assets/taste.py     # writes assets/taste-light.svg and assets/taste-dark.svg

Left: the proboscis motor neuron MN9 (left and right) under sugar, water, and sugar with bitter or Ir94e
taste neurons, 30 trials each; below it, MN9 at 10 and 100 Hz of sugar. Right: MN9 under sugar in the
real network and in 20 rewirings of each kind (every dot a network); the degree-preserving and
class-preserving rewirings gate the pass, the within-neuron weight shuffles are reported only.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/loom.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117"),
}
W, H = 1120, 430


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    t = d["tests"]
    out = [f'<rect width="{W}" height="{H}" fill="{c["paper"]}"/>']
    # --- left: what drives MN9
    x0, x1, y0, row, top = 210, 560, 70, 42, 50.0
    bx = lambda v: x0 + (x1 - x0) * min(v, top) / top
    out.append(text(24, 36, "What drives MN9, the neuron that extends the proboscis", "lab"))
    for v in (0, 25, 50):
        out.append(f'<path d="M{bx(v):.1f} {y0 - 14}V{y0 + row * 4 - 12}" stroke="{c["rule"]}"/>')
        out.append(text(bx(v), y0 + row * 4 + 6, f"{v} Hz", "tick", "middle"))
    rows = [("sugar", "sugar"), ("water", "water"), ("sugar + bitter", "sugar+bitter"), ("sugar + Ir94e", "sugar+ir94e")]
    for k, (label, key) in enumerate(rows):
        y = y0 + k * row
        out.append(text(x0 - 14, y + 5, label, "name", "end"))
        for j, (side, col) in enumerate((("L", c["red"]), ("R", c["muted"]))):
            v = t[f"mn9_{side}_hz"][key]
            yy = y - 10 + j * 12
            out.append(f'<rect class="bar" x="{x0}" y="{yy:.1f}" width="{max(bx(v) - x0, 1.5):.1f}" height="10" rx="2" fill="{col}"/>')
            out.append(text(bx(v) + 8, yy + 9, f"{v:.0f}", "val"))
    out.append(f'<rect x="24" y="{y0 + row * 4 + 22}" width="12" height="10" rx="2" fill="{c["red"]}"/>')
    out.append(text(42, y0 + row * 4 + 32, "left MN9", "note"))
    out.append(f'<rect x="118" y="{y0 + row * 4 + 22}" width="12" height="10" rx="2" fill="{c["muted"]}"/>')
    out.append(text(136, y0 + row * 4 + 32, "right MN9 (30 trials each; taste neurons driven at 100 Hz)", "note"))
    # dose
    dy = y0 + row * 4 + 72
    out.append(text(24, dy, "Dose: MN9 follows the sugar rate", "lab"))
    for k, (label, v) in enumerate((("10 Hz of sugar", d["mn9_L_hz_10"]), ("100 Hz of sugar", d["mn9_L_hz_100"]))):
        y = dy + 30 + k * 28
        out.append(text(x0 - 14, y + 5, label, "name", "end"))
        out.append(f'<rect class="bar" x="{x0}" y="{y - 6:.1f}" width="{max(bx(v) - x0, 1.5):.1f}" height="12" rx="2" fill="{c["red"]}"/>')
        out.append(text(bx(v) + 8, y + 5, f"{v:.0f} Hz", "val"))

    # --- right: scrambled wiring
    rx0, rx1 = 700, 1090
    out.append(text(640, 36, "Scramble the wiring and sugar no longer reaches MN9", "lab"))
    groups = [("real network", [d["mn9_L_hz_100"]], c["red"]),
              ("degree-preserving", d["nulls"]["degree_preserving"]["mn9_L_hz"], c["ink"]),
              ("class-preserving", d["nulls"]["class_preserving"]["mn9_L_hz"], c["ink"]),
              ("weight shuffle*", d["nulls"]["within_neuron_shuffle"]["mn9_L_hz"], c["muted"])]
    sx = lambda v: rx0 + (rx1 - rx0) * min(v, top) / top
    for v in (0, 25, 50):
        out.append(f'<path d="M{sx(v):.1f} 58V{58 + 62 * len(groups)}" stroke="{c["rule"]}"/>')
        out.append(text(sx(v), 76 + 62 * len(groups), f"{v} Hz", "tick", "middle"))
    rng = np.random.default_rng(3)
    for k, (label, vals, col) in enumerate(groups):
        y = 90 + k * 62
        out.append(text(rx0 - 14, y + 5, label, "name", "end"))
        n_zero = sum(v == 0 for v in vals)
        for v in vals:
            jitter = rng.uniform(-11, 11) if len(vals) > 1 else 0
            out.append(f'<circle class="dot" cx="{sx(v):.1f}" cy="{y + jitter:.1f}" r="{7 if len(vals) == 1 else 4.2}" fill="{col}" opacity="{1 if len(vals) == 1 else 0.75}"/>')
        note = "MN9 at 41 Hz" if len(vals) == 1 else f"MN9 silent in {n_zero} of {len(vals)}"
        out.append(text(rx0, y + 30, note, "note"))
    out.append(text(640, H - 20, "* reported only: it keeps each neuron's partners, so it tests weights, not routing", "note"))

    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .name {{ font-size: 14px; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; font-variant-numeric: tabular-nums; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 12px; fill: {c["muted"]}; font-variant-numeric: tabular-nums; }}
    @media (prefers-reduced-motion: no-preference) {{
      .bar {{ transform-box: fill-box; transform-origin: left center; animation: grow 1.2s ease-out both; }}
      .dot {{ animation: fade 1.6s ease-out both; }}
    }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
    @keyframes fade {{ from {{ opacity: 0; }} }}
    """
    title = "Rung 1: sugar drives the proboscis motor neuron MN9, bitter and Ir94e suppress it, and scrambled wiring abolishes it"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style>' + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "shiu_rewiring.json").read_text())
    for theme in THEMES:
        path = OUT / f"taste-{theme}.svg"
        path.write_text(figure(theme, d))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
