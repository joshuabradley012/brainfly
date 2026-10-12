"""Pair by pair against flies: how closely each pair of the five flight motor neurons fires, in brainfly's units and in
Hürkey et al.'s own conductance model, from the saved results (nothing by hand).

    python assets/dlm_pairs.py      # writes assets/dlm_pairs-light.svg and assets/dlm_pairs-dark.svg

Columns: the strongly coupled pairs (MN1-2, MN3-4), the weakly coupled MN1-4 pairs, and MN5's four pairs. Rows: each
pair's spikes within 10 ms of the partner's, as a multiple of chance, and dip10, the share of the partner's spikes in the
first or last tenth of the cycle (dlm_splay_check6.pairs); dashed, chance. Grey bands: flies' ranges (Hürkey et al. 2023's five-unit
flies; dlm_splay_check6.FLIES_PAIRS). Each line spans that kind's pairs (each a median over 8 runs of 300 s) and its dot
marks their mean. Conditions: leaky-integrator units at flies' coupling, all five at one rate (dlm_splay_check6.py),
and with MN5 at 1.26 times the others' rate with each unit's kicks set for its own rate (dlm_splay_check10.py); Hürkey et
al.'s conductance model as published (dlm_splay_check8.py's A), and leaky integrators at its coupling, irregularity and
rates (dlm_splay_check11.py's "as A"); Hürkey et al.'s model with its published coupling at flies' irregularity
(dlm_splay_check8.py's D), and leaky integrators the same (dlm_splay_check11.py's "as D"). At flies' coupling their model
fires at no fly-like rate, so it isn't shown.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/dlm_splay.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 570
KINDS = [("strong", "Strongly coupled pairs (MN1–2, MN3–4)"), ("weak", "Weakly coupled MN1–4 pairs"), ("mn5", "MN5's pairs")]
MEASURES = [("within_10ms_over_chance", "within 10 ms, × chance", (0.0, 1.1), (0.0, 0.5, 1.0)),
            ("dip10", "dip10", (0.0, 0.22), (0.0, 0.1, 0.2))]
CONDITIONS = [  # (label, JSON, path to the condition, color, filled)
    ("Leaky integrators, flies' coupling, one rate", "dlm_splay_check6.json", ("conditions", "LIF, MN5 assumed"), "ink", True),
    ("…MN5 at 1.26 × the others' rate, as irregular", "dlm_splay_check10.json", ("conditions", "LIF, MN5 at 1.26 x MN1-4, own kicks"), "ink", False),
    ("Hürkey et al.'s model, as published", "dlm_splay_check8.json", ("conditions", "A, as published"), "red", True),
    ("Leaky integrators at that coupling, CV and rates", "dlm_splay_check11.json", ("part2", "as A"), "ink", True),
    ("Hürkey et al.'s model, flies' irregularity", "dlm_splay_check8.json", ("conditions", "D, published coupling, flies' irregularity"), "red", False),
    ("Leaky integrators at that coupling, CV and rates", "dlm_splay_check11.json", ("part2", "as D"), "ink", False),
]


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, flies: dict, data: list) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "Pair by pair against flies: the weakly coupled pairs fall short in every model shown", "lab"),
           text(24, 50, "Flies' five DLM motor neurons avoid firing together pair by pair (grey: flies' ranges). The weakly coupled MN1–4 pairs come within 10 ms", "note"),
           text(24, 68, "of each other more often than flies' in brainfly's units and in Hürkey et al.'s own model, which holds them apart less well at the same coupling and noise.", "note")]
    lx, x0, cw, gap = 24, 330, 236, 28
    rowh, top = 24, 120
    cellh = rowh * len(data) + 44
    for m, (key, mlabel, (vmin, vmax), ticks) in enumerate(MEASURES):
        y0 = top + m * (cellh + 30)
        out.append(text(lx, y0 - 8, mlabel[0].upper() + mlabel[1:], "val"))
        for k, (kind, klabel) in enumerate(KINDS):
            cx = x0 + k * (cw + gap)
            tx = lambda v: cx + cw * (v - vmin) / (vmax - vmin)
            if m == 0:
                out.append(text(cx + cw / 2, top - 28, klabel, "val", "middle"))
            lo, hi = flies[kind][key]
            out.append(f'<rect x="{tx(lo):.1f}" y="{y0:.1f}" width="{tx(hi) - tx(lo):.1f}" height="{rowh * len(data):.1f}" '
                       f'fill="{c["ink"]}" fill-opacity="0.10"><title>flies {lo:g}–{hi:g}</title></rect>')
            if k == 0:
                out.append(text((tx(lo) + tx(hi)) / 2, y0 - 4, "flies", "tiny", "middle"))
            if key == "within_10ms_over_chance":
                out.append(f'<line x1="{tx(1.0):.1f}" y1="{y0:.1f}" x2="{tx(1.0):.1f}" y2="{y0 + rowh * len(data):.1f}" '
                           f'stroke="{c["muted"]}" stroke-dasharray="4 3"/>')
                if k == 0:
                    out.append(text(tx(1.0), y0 - 4, "chance", "tiny", "middle"))
            for sep in (2, 4):                                     # groups: flies' coupling; as published; flies' irregularity
                out.append(f'<line x1="{cx}" y1="{y0 + rowh * sep:.1f}" x2="{cx + cw}" y2="{y0 + rowh * sep:.1f}" stroke="{c["rule"]}" stroke-dasharray="2 3"/>')
            base = y0 + rowh * len(data) + 6
            out.append(f'<line x1="{cx}" y1="{base}" x2="{cx + cw}" y2="{base}" stroke="{c["rule"]}"/>')
            for t in ticks:
                out.append(f'<line x1="{tx(t):.1f}" y1="{base}" x2="{tx(t):.1f}" y2="{base + 4}" stroke="{c["rule"]}"/>')
                out.append(text(tx(t), base + 16, f"{t:g}", "tiny", "middle"))
            for r, (label, color, filled, pairs) in enumerate(data):
                y = y0 + rowh * r + rowh / 2
                vals = np.array([p[key] for p in pairs.values() if p["kind"] == kind])
                a, b, mean = float(vals.min()), float(vals.max()), float(vals.mean())
                col = c[color]
                out.append(f'<line x1="{tx(a):.1f}" y1="{y:.1f}" x2="{tx(b):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2" stroke-linecap="round"/>')
                fill = col if filled else c["paper"]
                out.append(f'<circle cx="{tx(mean):.1f}" cy="{y:.1f}" r="5" fill="{fill}" stroke="{col}" stroke-width="2">'
                           f'<title>{label}: {a:.3f}–{b:.3f} (mean {mean:.3f})</title></circle>')
                if k == 0:
                    out.append(text(lx, y + 4, label, "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = ("Pairwise measures of the five flight motor neurons against flies' ranges: the weakly coupled pairs come "
             "within 10 ms of each other more often than flies' in leaky-integrator units and in Hürkey et al.'s own model")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    loaded = {}
    data = []
    for label, file, (part, name), color, filled in CONDITIONS:
        d = loaded.setdefault(file, json.loads((ROOT / "experiments" / file).read_text()))
        data.append((label, color, filled, d[part][name]["pairs"]))
    flies = loaded["dlm_splay_check8.json"]["flies_pairs"]
    for theme in THEMES:
        path_ = OUT / f"dlm_pairs-{theme}.svg"
        path_.write_text(figure(theme, flies, data))
        print(path_)


if __name__ == "__main__":
    main()
