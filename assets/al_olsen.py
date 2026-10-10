"""The antennal lobe measured as Olsen et al. measured flies (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/al_olsen.py      # writes assets/al_olsen-light.svg and assets/al_olsen-dark.svg

Top: each glomerulus's cholinergic projection neurons' rise over the 500 ms from the valve's opening against its receptor
neurons' (Olsen et al. 2010's protocol: experiments/odor_olsen_protocol_check.py on odor_probe49.py's model, one-pool
receptor synapses, grey; odor_probe51.py's measures, two pools, red), against flies' points (rings, Olsen et al.'s Fig.
1B as digitized in research_notes/Rung 9 learning data/weak_input_gain.md) and their fitted curves (thin). Bottom left:
VM7d's projection neurons over time for weak and intermediate receptor input (two pools; 50 ms running means less rest),
against flies' VM7 PSTHs (Olsen et al. Fig. 8, samples every 25 ms; 2-butanone 10^-6 and 10^-5, receptor input about 12
and 48 spikes/s). Bottom right: the share of VM7d's response alone that survives pentyl acetate's lateral input
(experiments/odor_normalization_check.py), for responses at 0.47 and 0.81 of the model's Rmax, against flies' VM7 at 0.47
and 0.83 of theirs (Olsen et al. Fig. 2C; lateral input as summed receptor rates derived from their field potentials).
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
W, H = 1120, 720
GLOMERULI = ("DM4", "DL5", "VM7d", "DM1")
OLSEN_FIT = {"DM4": (170, 16.3), "DL5": (167, 11.8), "VM7d": (163, 12.4), "DM1": (144, 44.8)}
FLY_POINTS = {"DM4": [(5.0, 27.9), (6.1, 31.5), (13.4, 63.9), (25.8, 115.9), (29.6, 129.5), (62.2, 143.8), (71.1, 153.4), (125.0, 164.1)],
              "DL5": [(5.1, 44.2), (13.4, 84.9), (41.5, 148.6), (98.7, 158.4)],
              "VM7d": [(11.6, 78.0), (47.9, 138.3), (107.1, 161.4)],
              "DM1": [(9.2, 20.9), (21.8, 40.1), (24.3, 44.0), (25.7, 51.5), (28.7, 40.1), (36.0, 61.9), (51.3, 73.6), (55.8, 72.0),
                      (73.5, 105.2), (111.2, 122.6)]}
FLY_PSTH = {"weak": (11.6, [2, 2, 2, 2, 2, 58, 160, 176, 161, 143, 122, 110, 99, 109, 82, 84, 81, 74, 74, 80, 74]),
            "intermediate": (48.0, [-1, -1, -1, -1, -1, 219, 296, 263, 236, 221, 193, 170, 159, 141, 136, 142, 136, 135, 135, 131, 129])}
MODEL_PSTH = {"weak": "10", "intermediate": "40"}
FLY_KEPT = {"0.47": [1.0, 0.66, 0.47, 0.22, 0.10], "0.83": [1.0, 0.90, 0.84, 0.67, 0.55]}
MODEL_KEPT = {"0.47": "20", "0.83": "80"}
XS = (5.0, 10.0, 20.0, 40.0, 80.0, 160.0)
# panels
TX0, TPW, TGAP, TY0, TY1 = 70, 220, 40, 120, 300
BY0, BY1 = 450, 640


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def path(points, sx, sy) -> str:
    return " ".join(f"{'M' if i == 0 else 'L'}{sx(x):.1f} {sy(y):.1f}" for i, (x, y) in enumerate(points))


def transform_panel(c, x0, g, models) -> list[str]:
    lo, hi, vmax = np.log(3.0), np.log(200.0), 200.0
    sx = lambda x: x0 + TPW * (np.log(x) - lo) / (hi - lo)
    sy = lambda v: TY1 - (TY1 - TY0) * min(max(v, 0.0), vmax) / vmax
    out = [text(x0, TY0 - 12, g, "val")]
    for v in (0, 50, 100, 150, 200):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + TPW}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        if x0 == TX0:
            out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for x in (5, 10, 20, 50, 100, 200):
        out.append(text(sx(x), TY1 + 15, f"{x}", "tick", "middle"))
    rmax, sigma = OLSEN_FIT[g]
    grid = np.exp(np.linspace(lo, hi, 60))
    fit = [(x, rmax * x ** 1.5 / (x ** 1.5 + sigma ** 1.5)) for x in grid]
    out.append(f'<path d="{path(fit, sx, sy)}" fill="none" stroke="{c["ink"]}" stroke-width="1" stroke-opacity="0.7"/>')
    for x, v in FLY_POINTS[g]:
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6">'
                   f'<title>flies, {g}: {v:g} spikes/s at {x:g} spikes/s of receptor input</title></circle>')
    for label, colour, pts in models:
        series = [(x, pts[f"{x:g}"]["window_mean"]) for x in XS]
        out.append(f'<path d="{path(series, sx, sy)}" fill="none" stroke="{c[colour]}" stroke-width="2"/>')
        for x, v in series:
            out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="3" fill="{c[colour]}"><title>{label}, {g}: {v:.0f} spikes/s at {x:g}</title></circle>')
    return out


def psth_panel(c, x0, pw, key, model_pts) -> list[str]:
    t1, vmax = 0.6, 320.0
    sx = lambda t: x0 + pw * t / t1
    sy = lambda v: BY1 - (BY1 - BY0) * min(max(v, 0.0), vmax) / vmax
    x_in, fly = FLY_PSTH[key]
    out = [text(x0, BY0 - 12, f"VM7d, {key} input", "val")]
    for v in (0, 100, 200, 300):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for t in (0, 0.2, 0.4, 0.6):
        out.append(text(sx(t), BY1 + 15, f"{t:g}", "tick", "middle"))
    out.append(text(x0 + pw / 2, BY1 + 32, "s from the valve's opening", "tick", "middle"))
    pts = [(0.025 * i, v) for i, v in enumerate(fly)]
    out.append(f'<path d="{path(pts, sx, sy)}" fill="none" stroke="{c["ink"]}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    for t, v in pts:
        out.append(f'<circle cx="{sx(t):.1f}" cy="{sy(v):.1f}" r="2.6" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.2"/>')
    psth = np.asarray(model_pts["psth"], float)
    n_pre = 50
    rest = psth[:n_pre].mean()
    smooth = np.convolve(psth[n_pre:] - rest, np.ones(5) / 5, mode="valid")      # smooth[k]: 10k + 25 ms
    series = [(0.01 * k + 0.025, v) for k, v in enumerate(smooth) if 0.01 * k + 0.025 <= t1]
    out.append(f'<path d="{path(series, sx, sy)}" fill="none" stroke="{c["red"]}" stroke-width="2"/>')
    out.append(text(x0 + pw - 4, BY0 + 10, f"flies ≈{x_in:g}, model {MODEL_PSTH[key]} spikes/s of input", "tick", "end"))
    return out


def kept_panel(c, x0, pw, data) -> list[str]:
    levels = data["levels_hz"]
    xmax = 1000.0
    sx = lambda v: x0 + pw * v / xmax
    sy = lambda v: BY1 - (BY1 - BY0) * min(max(v, 0.0), 1.05) / 1.05
    out = [text(x0, BY0 - 12, "VM7d's response kept under pentyl acetate", "val")]
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v:g}", "tick", "end"))
    for v in (0, 250, 500, 750, 1000):
        out.append(text(sx(v), BY1 + 15, f"{v}", "tick", "middle"))
    out.append(text(x0 + pw / 2, BY1 + 32, "lateral receptor input, summed spikes/s", "tick", "middle"))
    for share, dash in (("0.47", ""), ("0.83", ' stroke-dasharray="6 4"')):
        fly = list(zip(levels, FLY_KEPT[share]))
        out.append(f'<path d="{path(fly, sx, sy)}" fill="none" stroke="{c["ink"]}" stroke-width="1.3"{dash}/>')
        for v, k in fly:
            out.append(f'<circle cx="{sx(v):.1f}" cy="{sy(k):.1f}" r="3.6" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.5">'
                       f'<title>flies, VM7 at {share} of Rmax: {k:g} kept at {v:g} spikes/s</title></circle>')
        kept = data["glomeruli"]["VM7d"]["rates"][MODEL_KEPT[share]]["kept"]
        model = [(v, k) for v, k in zip(levels, kept)]
        out.append(f'<path d="{path(model, sx, sy)}" fill="none" stroke="{c["red"]}" stroke-width="2"{dash}/>')
        for v, k in model:
            out.append(f'<circle cx="{sx(v):.1f}" cy="{sy(k):.1f}" r="3" fill="{c["red"]}"><title>model, VM7d at {share} of Rmax: {k:.2f} kept</title></circle>')
    out.append(text(x0 + pw - 4, BY0 + 10, "solid: 0.47 of Rmax; dashed: about 0.8", "tick", "end"))
    return out


def figure(theme: str, p49: dict, p51: dict, norm: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "Measured as flies were, the projection neurons answer at half to two thirds of flies' strength, and a broad odor divides them as it divides flies'", "lab"),
           text(24, 50, "Cholinergic projection neurons, Olsen et al. 2010's protocol: receptor synapses as one pool (grey, odor_probe49.py) or two "
                "(red, odor_probe51.py, the base model); rings: flies.", "note"),
           text(24, 68, "Flies' responses rise steeply and saturate by about 50 spikes/s of input; the model's keep rising. Below: VM7d's time "
                "course, and how much of its response a broad odor leaves.", "note")]
    for i, g in enumerate(GLOMERULI):
        x0 = TX0 + i * (TPW + TGAP)
        models = [("one pool", "faint", p49["protocols"]["olsen"][g]["cholinergic"]["points"]),
                  ("two pools", "red", p51["condition"]["olsen_protocol"]["olsen"][g]["cholinergic"]["points"])]
        out += transform_panel(c, x0, g, models)
    out.append(text(TX0 + 2 * (TPW + TGAP) - TGAP / 2, TY1 + 34, "receptor neurons' rise over 500 ms (spikes/s, log scale)", "tick", "middle"))
    out.append(f'<text x="{TX0 - 46}" y="{(TY0 + TY1) / 2:.1f}" class="tick" text-anchor="middle" '
               f'transform="rotate(-90 {TX0 - 46} {(TY0 + TY1) / 2:.1f})">PN rise (spikes/s)</text>')
    vm7 = p51["condition"]["olsen_protocol"]["olsen"]["VM7d"]["cholinergic"]["points"]
    out += psth_panel(c, 70, 300, "weak", vm7[MODEL_PSTH["weak"]])
    out += psth_panel(c, 430, 300, "intermediate", vm7[MODEL_PSTH["intermediate"]])
    out += kept_panel(c, 800, 290, norm)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = ("Projection neuron responses measured with Olsen et al.'s protocol against flies': the transform in four glomeruli, VM7d's time "
             "course for weak and intermediate input, and the share of its response a broad odor leaves")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    e = ROOT / "experiments"
    p49 = json.loads((e / "odor_olsen_protocol_check.json").read_text())
    p51 = json.loads((e / "odor_probe51.json").read_text())
    norm = json.loads((e / "odor_normalization_check_probe51.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"al_olsen-{theme}.svg"
        path_.write_text(figure(theme, p49, p51, norm))
        print(path_)


if __name__ == "__main__":
    main()
