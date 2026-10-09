"""The olfaction figure in the README, drawn from saved results (nothing by hand).

    python assets/olfaction.py      # writes assets/olfaction-light.svg and assets/olfaction-dark.svg

Rung 9's groundwork: the olfactory pathway set from measurements one property at a time (experiments/odor_probe3.py
to odor_probe6.py). For each step, across six DoOR odors (dot: mean; line: range): left, the share of Kenyon cells
firing at least one extra spike in the odor's second, in at least half of 8 flies, against Turner et al. 2008's
6 +- 5% (band); right, MBON11's rise over its rest, against about 20 Hz in flies (Hige et al. 2015; dashed).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/rung3.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f", band="#b8322a"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681", band="#e5533f"),
}
W, H = 960, 450
STEPS = [("odor_probe3", "rung 4 brain", "rung 4's brain"),
         ("odor_probe3", "ORN + KC", "receptor synapses, Kenyon cell rest"),
         ("odor_probe4", "+ tau", "+ 150 ms Kenyon cell membrane"),
         ("odor_probe5", "Turner", "Kenyon cells from Turner 2008"),
         ("odor_probe6", None, "+ undepressed Kenyon cell outputs")]


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def load() -> list[dict]:
    rows = []
    for probe, cond, label in STEPS:
        d = json.loads((ROOT / "experiments" / f"{probe}.json").read_text())
        c = d["condition"] if cond is None else d["conditions"][cond]
        share = np.array([100 * r["kc_share_1spike"] for r in c["odors"].values()])
        rise = np.array([r["read"]["MBON11"][1] - r["read"]["MBON11"][0] for r in c["odors"].values()])
        rows.append({"label": label, "share": share, "rise": rise})
    return rows


def panel(c, rows, x0, x1, key, top, ticks, title, unit, band=None, line=None, note="", labels=True):
    out = [text(x0, 96, title, "val")]
    y0, step = 150, 46
    sx = lambda v: x0 + (x1 - x0) * v / top
    if band:
        out.append(f'<rect x="{sx(band[0]):.1f}" y="{y0 - 20}" width="{sx(band[1]) - sx(band[0]):.1f}" height="{step * len(rows)}" '
                   f'fill="{c["band"]}" fill-opacity="0.10"/>')
        out.append(text(sx(band[1]) + 4, y0 - 24, "flies", "tick"))
    if line is not None:
        out.append(f'<line x1="{sx(line):.1f}" y1="{y0 - 20}" x2="{sx(line):.1f}" y2="{y0 - 20 + step * len(rows)}" '
                   f'stroke="{c["red"]}" stroke-dasharray="4 3"/>')
        out.append(text(sx(line) + 4, y0 - 24, "flies", "tick"))
    for t in ticks:
        out.append(f'<line x1="{sx(t):.1f}" y1="{y0 - 20 + step * len(rows)}" x2="{sx(t):.1f}" y2="{y0 - 14 + step * len(rows)}" stroke="{c["rule"]}"/>')
        out.append(text(sx(t), y0 + 2 + step * len(rows), f"{t:g}", "tick", "middle"))
    out.append(text((x0 + x1) / 2, y0 + 20 + step * len(rows), unit, "tick", "middle"))
    for k, r in enumerate(rows):
        y = y0 + k * step
        v = r[key]
        last = k == len(rows) - 1
        colour = c["red"] if last else c["faint"]
        out.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(f'<line x1="{sx(min(v.min(), top)):.1f}" y1="{y:.1f}" x2="{sx(min(v.max(), top)):.1f}" y2="{y:.1f}" stroke="{colour}" stroke-width="2.5" stroke-linecap="round"/>')
        out.append(f'<circle cx="{sx(min(v.mean(), top)):.1f}" cy="{y:.1f}" r="5" fill="{colour}" stroke="{c["paper"]}" stroke-width="2"/>')
        if labels:
            out.append(text(x0 - 12, y + 4, r["label"], "lab2" if last else "tick", "end"))
        fmt = (lambda x: f"{x + 0.0:.0f}") if key == "share" else (lambda x: f"{max(x, 0.0):.1f}")
        out.append(text(sx(min(v.max(), top)) + 8, y + 4, f"{fmt(v.min())}–{fmt(v.max())}", "tick"))
    if note:
        out.append(text(x0, y0 + 44 + step * len(rows), note, "tick"))
    return out


def figure(theme: str, rows: list[dict]) -> str:
    c = THEMES[theme]
    out = [text(24, 34, "Odors reach the mushroom body once its synapses are set from measurements", "lab"),
           text(24, 54, "Each step adds measured properties; six odors per step (dot: mean, line: range across odors)", "note")]
    out += panel(c, rows, 250, 520, "share", 100, (0, 25, 50, 75, 100), "Kenyon cells responding", "% of 4,064 Kenyon cells",
                 band=(1, 11), note="flies: 6 ± 5% (Turner 2008)")
    out += panel(c, rows, 620, 900, "rise", 25, (0, 5, 10, 15, 20, 25), "MBON11's rise over rest", "Hz",
                 line=20, note="flies: about 37 to 57 Hz (Hige 2015)", labels=False)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .lab2 {{ font-size: 11px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    last = rows[-1]
    title = (f"Rung 9 groundwork: as the olfactory pathway's properties are set from measurements, the share of Kenyon "
             f"cells responding to an odor goes from about half to {last['share'].min():.0f}-{last['share'].max():.0f}% "
             f"(flies 6 +- 5%), and MBON11's rise to {last['rise'].min():.0f}-{last['rise'].max():.0f} Hz (flies about 20)")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    rows = load()
    for theme in THEMES:
        path = OUT / f"olfaction-{theme}.svg"
        path.write_text(figure(theme, rows))
        print(path)


if __name__ == "__main__":
    main()
