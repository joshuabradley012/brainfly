"""The projection neurons' weak end (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/al_weak.py      # writes assets/al_weak-light.svg and assets/al_weak-dark.svg

Each glomerulus's projection neurons (the cholinergic ones; evoked spikes/s over the odor's first 0.5 s) against its
receptor input (receptor_fills.RECOMMENDED x 200 spikes/s) for 4-methylcyclohexanol and 3-octanol, from
experiments/odor_weak_glomeruli_check.py: the model with the whole odor (red), the model with the glomerulus driven alone
(rings; 4-methylcyclohexanol's glomeruli with at least 8 spikes/s), and Olsen et al. 2010's transform for flies (165 r^1.5
/ (12^1.5 + r^1.5), solid) and with their normalization by the odor's summed input (+ (0.05 x summed)^1.5, dashed).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/al_transform.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 480
Y0, Y1 = 120, 390
XLO, XHI, YMAX = 2.0, 200.0, 170.0


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def panel(c, x0, pw, odor: str, r: dict, olsen: dict) -> list[str]:
    sx = lambda v: x0 + pw * (np.log(min(max(v, XLO), XHI)) - np.log(XLO)) / (np.log(XHI) - np.log(XLO))
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), YMAX) / YMAX
    out = [text(x0, Y0 - 12, f"{odor}: projection neurons against receptor input", "val")]
    for v in (0, 50, 100, 150):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for v in (2, 5, 10, 20, 50, 100, 200):
        out.append(text(sx(v), Y1 + 16, f"{v}", "tick", "middle"))
    out.append(text(x0 + pw / 2, Y1 + 34, "receptor input (spikes/s)", "tick", "middle"))
    out.append(f'<text transform="translate({x0 - 36},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">projection neurons (spikes/s)</text>')
    rmax, sigma, m, n = olsen["rmax"], olsen["sigma"], olsen["m"], olsen["exponent"]
    grid = np.exp(np.linspace(np.log(XLO), np.log(XHI), 80))
    for norm, dash in ((0.0, ""), (m * r["summed_input_hz"], ' stroke-dasharray="5 4"')):
        pts = [(x, rmax * x ** n / (sigma ** n + x ** n + norm ** n)) for x in grid]
        d = " ".join(f"{'M' if i == 0 else 'L'}{sx(x):.1f} {sy(y):.1f}" for i, (x, y) in enumerate(pts))
        out.append(f'<path d="{d}" fill="none" stroke="{c["ink"]}" stroke-width="1.4" stroke-opacity="0.75"{dash}/>')
    rings, dots = [], []
    for g, t in r["table"].items():
        x = t["input_hz"]
        if t.get("model_alone") is not None:
            rings.append(f'<circle cx="{sx(x):.1f}" cy="{sy(t["model_alone"]):.1f}" r="4.5" fill="none" stroke="{c["ink"]}" stroke-width="1.6">'
                         f'<title>{g} alone: {t["model_alone"]:.0f} spikes/s at {x:g} (flies\' transform {t["olsen_alone"]:.0f})</title></circle>')
        dots.append(f'<circle cx="{sx(x):.1f}" cy="{sy(t["model_whole"]):.1f}" r="4.5" fill="{c["red"]}" stroke="{c["paper"]}" stroke-width="2">'
                    f'<title>{g} in the whole odor: {t["model_whole"]:.0f} spikes/s at {x:g} (flies\' transform, normalized: {t["olsen_whole"]:.0f})</title></circle>')
    return out + rings + dots


def bars(c, x0, pw, data: dict) -> list[str]:
    """Summed responses by receptor input, flies' transform (normalized) against the model, as horizontal bars."""
    out = [text(x0 - 60, Y0 - 12, "summed by receptor input", "val")]
    names = {"0-10 Hz": "under 10", "10-30 Hz": "10-30", "30-80 Hz": "30-80", "80-400 Hz": "80 or more"}
    rows = [(odor, b) for odor in data for b in names if b in data[odor]["bins"]]
    xmax = 700.0
    sx = lambda v: x0 + pw * min(max(v, 0.0), xmax) / xmax
    for v in (0, 200, 400, 600):
        out.append(f'<line x1="{sx(v):.1f}" y1="{Y0:.1f}" x2="{sx(v):.1f}" y2="{Y1:.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(sx(v), Y1 + 16, f"{v}", "tick", "middle"))
    out.append(text(x0 + pw / 2, Y1 + 34, "spikes/s, summed over glomeruli", "tick", "middle"))
    head = 18.0
    step = (Y1 - Y0 - head * len(data)) / len(rows)
    y, last = Y0, None
    for odor, b in rows:
        if odor != last:
            out.append(text(x0 - 60, y + 12, "4-methylcyclohexanol" if odor.startswith("4-") else "3-octanol", "val"))
            y += head
        v = data[odor]["bins"][b]
        out.append(text(x0 - 6, y + step / 2 + 4, names[b], "tick", "end"))
        for k, (key, fill) in enumerate((("olsen_whole", c["faint"]), ("model_whole", c["red"]))):
            by = y + step / 2 - 9 + k * 10
            out.append(f'<rect x="{x0:.1f}" y="{by:.1f}" width="{max(sx(v[key]) - x0, 0.5):.1f}" height="8" rx="2" fill="{fill}">'
                       f'<title>{odor}, {b}: {"flies\' transform" if k == 0 else "model"} {v[key]:.0f} spikes/s over {v["glomeruli"]} glomeruli</title></rect>')
        y += step
        last = odor
    out.append(text(x0 + pw / 2, Y1 + 50, "grey: flies' transform; red: model", "tick", "middle"))
    return out


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    odors = d["odors"]
    out = [text(24, 30, "The projection neurons' weak end is half of flies', and 4-methylcyclohexanol lives there", "lab"),
           text(24, 50, "Lines: Olsen et al.'s transform for flies (solid) and with the odor's normalization (dashed). Rings: the model's glomeruli "
                "driven alone, at about half the solid line;", "note"),
           text(24, 68, "red: in the whole odor, where the model divides about as flies do until weak glomeruli fall below threshold. "
                "Right: summed by input strength.", "note")]
    out += panel(c, 80, 330, "4-methylcyclohexanol", odors["4-methylcyclohexanol"], d["olsen"])
    out += panel(c, 490, 330, "3-octanol", odors["3-octanol"], d["olsen"])
    out += bars(c, 930, 170, odors)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = ("Projection neuron responses against receptor input for 4-methylcyclohexanol and 3-octanol: the model alone and in the "
             "whole odor against Olsen et al.'s transform, and the summed responses by input strength")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "odor_weak_glomeruli_check.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"al_weak-{theme}.svg"
        path_.write_text(figure(theme, d))
        print(path_)


if __name__ == "__main__":
    main()
