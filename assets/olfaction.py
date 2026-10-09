"""The olfaction figure in the README, drawn from saved results (nothing by hand).

    python assets/olfaction.py      # writes assets/olfaction-light.svg and assets/olfaction-dark.svg

Rung 9's groundwork (experiments/odor_probe7.py): the olfactory pathway with its measured properties added in turn,
and one variant. For each model, across six DoOR odors (dot: mean; line: range): left, the share of Kenyon cells that
respond by Turner et al. 2008's criterion, against their 6 +- 5% (band); right, MBON11's odor-evoked spikes as Hige et
al. 2015 counted them (0 to 1.4 s from onset, spontaneous rate subtracted), against their 118 +- 8.3 to 3-octanol and
110 +- 11 to 4-methylcyclohexanol (band: the two means).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/rung3.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f", band=0.12),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681", band=0.25),
}
W, H = 960, 470
ROWS = [("rung 4 brain", "rung 4's brain"),
        ("measured receptor input", "measured receptor input"),
        ("+ Turner's Kenyon cells", "+ Turner's Kenyon cells"),
        ("+ undepressed outputs", "+ undepressed outputs (current)"),
        ("current, PN-KC depressed", "current, inputs depressed")]
CURRENT = "+ undepressed outputs"


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def load() -> list[dict]:
    d = json.loads((ROOT / "experiments" / "odor_probe7.json").read_text())
    rows = []
    for key, label in ROWS:
        c = d["conditions"][key]
        rows.append({"label": label, "current": key == CURRENT,
                     "share": np.array([100 * r["kc_share"] for r in c["odors"].values()]),
                     "spikes": np.array([r["evoked_spikes_0_1.4s"]["MBON11"] for r in c["odors"].values()])})
    return rows


def panel(c, rows, x0, x1, key, top, ticks, title, unit, band, note, labels=True):
    out = [text(x0, 96, title, "val")]
    y0, step = 150, 46
    sx = lambda v: x0 + (x1 - x0) * min(max(v, 0.0), top) / top
    out.append(f'<rect x="{sx(band[0]):.1f}" y="{y0 - 20}" width="{max(sx(band[1]) - sx(band[0]), 2):.1f}" '
               f'height="{step * len(rows)}" fill="{c["red"]}" fill-opacity="{c["band"]}"/>')
    out.append(text(sx(band[1]) + 4, y0 - 24, "flies", "tick"))
    for t in ticks:
        out.append(f'<line x1="{sx(t):.1f}" y1="{y0 - 20 + step * len(rows)}" x2="{sx(t):.1f}" y2="{y0 - 14 + step * len(rows)}" stroke="{c["rule"]}"/>')
        out.append(text(sx(t), y0 + 2 + step * len(rows), f"{t:g}", "tick", "middle"))
    out.append(text((x0 + x1) / 2, y0 + 20 + step * len(rows), unit, "tick", "middle"))
    fmt = (lambda v: f"{v + 0.0:.0f}") if key == "share" else (lambda v: f"{v + 0.0:.1f}".replace("-", "−"))
    for k, r in enumerate(rows):
        y = y0 + k * step
        v = r[key]
        colour = c["red"] if r["current"] else c["faint"]
        out.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(f'<line x1="{sx(v.min()):.1f}" y1="{y:.1f}" x2="{sx(v.max()):.1f}" y2="{y:.1f}" stroke="{colour}" stroke-width="2.5" stroke-linecap="round"/>')
        out.append(f'<circle cx="{sx(v.mean()):.1f}" cy="{y:.1f}" r="5" fill="{colour}" stroke="{c["paper"]}" stroke-width="2"/>')
        if labels:
            out.append(text(x0 - 12, y + 4, r["label"], "lab2" if r["current"] else "tick", "end"))
        out.append(text(sx(v.max()) + 8, y + 4, f"{fmt(v.min())}–{fmt(v.max())}", "tick"))
    out.append(text(x0, y0 + 44 + step * len(rows), note, "tick"))
    return out


def figure(theme: str, rows: list[dict]) -> str:
    c = THEMES[theme]
    cur = next(r for r in rows if r["current"])
    out = [text(24, 34, "Odors reach the mushroom body, but MBON11 hears them faintly", "lab"),
           text(24, 54, "Measured properties added in turn (rows 2-4), and one variant (row 5); six odors per row "
                "(dot: mean, line: range across odors)", "note")]
    out += panel(c, rows, 250, 520, "share", 60, (0, 20, 40, 60), "Kenyon cells responding (Turner's criterion)",
                 "% of 4,064 Kenyon cells", (1, 11), "flies: 6 ± 5% (Turner et al. 2008)")
    out += panel(c, rows, 620, 900, "spikes", 140, (0, 35, 70, 105, 140), "MBON11's odor-evoked spikes, 0–1.4 s",
                 "spikes above spontaneous", (110, 118), "flies: 118 ± 8 (OCT), 110 ± 11 (MCH); Hige et al. 2015",
                 labels=False)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .lab2 {{ font-size: 11px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = (f"Rung 9 groundwork: with the olfactory pathway's measured properties, {cur['share'].min():.0f}-"
             f"{cur['share'].max():.0f}% of Kenyon cells respond to an odor by Turner et al.'s criterion (flies 6 +- 5%), "
             f"and MBON11 gains {cur['spikes'].min():.0f}-{cur['spikes'].max():.0f} spikes in the 1.4 s after an odor's "
             f"onset (flies about 110-118)")
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
