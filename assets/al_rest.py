"""The projection neurons resting at flies' rate (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/al_rest.py      # writes assets/al_rest-light.svg and assets/al_rest-dark.svg

Left and middle: DL5's and VM7d's cholinergic projection neurons measured as Olsen et al. 2010 measured flies' (their
protocol; experiments/odor_olsen_protocol_check.py), with the PNs resting at 2.7 spikes/s (odor_probe54.py, grey) and at
about flies' rate (odor_probe56.py, red), against flies' points and fit. Right: the model's value as a share of flies' for
the measures these two models differ on, odor_probe54.py (grey; odor_probe55.py for the weighed input) and odor_probe56.py
(red): DL5's response at 5 and 10 spikes/s of input (flies' fit), Rmax and sigma (the mean over DL5, VM7d and DM4), the
share of the peak strong responses keep at 500 ms (DL5 at 80 spikes/s; flies 0.44), MBON11's spikes to 3-octanol (DoOR's
input; flies 118), and 4-methylcyclohexanol as a share of 3-octanol at the Kenyon cells (DoOR's input; flies 0.73-0.92,
taken at 0.82) and at the PNs over the glomeruli whose imaging whole-cell recordings support (the weighed input; flies
1.11; research_notes/Rung 9 learning data/lateral_pn_responses.md).
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
Y0, Y1 = 120, 380
XS = (5.0, 10.0, 20.0, 40.0, 80.0, 160.0)
OLSEN_FIT = {"DM4": (170, 16.3), "DL5": (167, 11.8), "VM7d": (163, 12.4)}       # as in assets/al_olsen.py
FLY_POINTS = {"DL5": [(5.1, 44.2), (13.4, 84.9), (41.5, 148.6), (98.7, 158.4)], "VM7d": [(11.6, 78.0), (47.9, 138.3), (107.1, 161.4)]}
BADEL = ("DM6", "DM3", "VM2", "DL3", "D", "DA2", "VM3", "DA1", "DA3", "VM7v", "DM2", "DC3", "DC2", "DM5", "VM4", "DL5",
         "VM1", "VC1", "VA2", "DL1", "DL4", "VM7d", "VA6", "VA7m", "VA4", "VA5", "VA3", "DA4l", "DM4", "VC2", "VA7l", "DP1m",
         "DM1", "VA1d", "VL2a", "VL2p", "VA1v")
UNRELIABLE = {"DA1", "DL3", "DA2", "DA3", "DM3", "VM7v", "VM3"}


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def olsen(x: float, g: str) -> float:
    rmax, sigma = OLSEN_FIT[g]
    return rmax * x ** 1.5 / (x ** 1.5 + sigma ** 1.5)


def transform_panel(c, x0, pw, g: str, before: dict, after: dict) -> list[str]:
    lo, hi, vmax = np.log(4.0), np.log(200.0), 180.0
    sx = lambda x: x0 + pw * (np.log(x) - lo) / (hi - lo)
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), vmax) / vmax
    out = [text(x0, Y0 - 12, f"{g}'s projection neurons, Olsen et al.'s protocol", "val")]
    for v in (0, 50, 100, 150):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for x in (5, 10, 20, 50, 100, 200):
        out.append(text(sx(x), Y1 + 15, f"{x}", "tick", "middle"))
    out.append(text(x0 + pw / 2, Y1 + 32, "receptor neurons' rise (spikes/s)", "tick", "middle"))
    grid = np.exp(np.linspace(lo, hi, 60))
    d = " ".join(f"{'M' if i == 0 else 'L'}{sx(x):.1f} {sy(olsen(x, g)):.1f}" for i, x in enumerate(grid))
    out.append(f'<path d="{d}" fill="none" stroke="{c["ink"]}" stroke-width="1" stroke-opacity="0.7"/>')
    for x, v in FLY_POINTS[g]:
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6"><title>flies: {v:.0f} at {x:g}</title></circle>')
    for label, colour, pts in (("resting at 2.7 spikes/s", "faint", before), ("at about flies' rate", "red", after)):
        series = [(x, pts[f"{x:g}"]["window_mean"]) for x in XS]
        d = " ".join(f"{'M' if i == 0 else 'L'}{sx(x):.1f} {sy(v):.1f}" for i, (x, v) in enumerate(series))
        out.append(f'<path d="{d}" fill="none" stroke="{c[colour]}" stroke-width="2.2"/>')
        for x, v in series:
            out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="3.2" fill="{c[colour]}"><title>{label}: {v:.0f} spikes/s at {x:g}</title></circle>')
    out.append(text(x0 + pw - 4, Y1 - 38, "grey: PNs resting at 2.7 spikes/s", "tick", "end"))
    out.append(text(x0 + pw - 4, Y1 - 24, "red: at about flies' rate; rings: flies", "tick", "end"))
    return out


def summary_panel(c, x0, pw, rows: list) -> list[str]:
    lo, hi = np.log(0.2), np.log(2.0)
    sx = lambda v: x0 + pw * (np.log(min(max(v, 0.2), 2.0)) - lo) / (hi - lo)
    out = [text(x0 - 150, Y0 - 12, "the model as a share of flies' value", "val")]
    for v in (0.25, 0.5, 1.0, 2.0):
        out.append(f'<line x1="{sx(v):.1f}" y1="{Y0:.1f}" x2="{sx(v):.1f}" y2="{Y1:.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 1.0 else 0.5}"/>')
        out.append(text(sx(v), Y1 + 15, f"{v:g}", "tick", "middle"))
    out.append(text(sx(1.0), Y1 + 32, "1 = flies", "tick", "middle"))
    step = (Y1 - Y0) / len(rows)
    for i, (label, before, after, tip) in enumerate(rows):
        y = Y0 + step * (i + 0.5)
        out.append(text(x0 - 8, y + 4, label, "tick", "end"))
        out.append(f'<line x1="{sx(before):.1f}" y1="{y:.1f}" x2="{sx(after):.1f}" y2="{y:.1f}" stroke="{c["faint"]}" stroke-width="1.6"/>')
        out.append(f'<circle cx="{sx(before):.1f}" cy="{y:.1f}" r="4.5" fill="{c["faint"]}"><title>{tip}: {before:.2f} of flies\' before</title></circle>')
        out.append(f'<circle cx="{sx(after):.1f}" cy="{y:.1f}" r="5" fill="{c["red"]}" stroke="{c["paper"]}" stroke-width="2"><title>{tip}: {after:.2f} of flies\' now</title></circle>')
    return out


def reliable_ratio(eq: dict) -> float:
    s = {od: sum(max(eq["odors"][od]["pn_evoked_hz_by_glomerulus_first_0.5s"].get(g, 0.0), 0.0) for g in BADEL if g not in UNRELIABLE)
         for od in ("3-octanol", "4-methylcyclohexanol")}
    return s["4-methylcyclohexanol"] / s["3-octanol"]


def figure(theme: str, p54: dict, p55: dict, p56: dict) -> str:
    c = THEMES[theme]
    t54, t56 = p54["olsen_protocol"]["olsen"], p56["condition"]["olsen_protocol"]["olsen"]
    pts = lambda t, g: t[g]["cholinergic"]["points"]
    fit = lambda t, k: float(np.mean([t[g]["cholinergic"]["fit"][k] for g in ("DL5", "VM7d", "DM4")]))
    flies_fit = lambda k: float(np.mean([OLSEN_FIT[g][0 if k == "rmax" else 1] for g in ("DL5", "VM7d", "DM4")]))
    kc = lambda od: od["4-methylcyclohexanol"]["kc_share"] / od["3-octanol"]["kc_share"]
    rows = [("DL5 at 5 spikes/s", pts(t54, "DL5")["5"]["window_mean"] / olsen(5, "DL5"), pts(t56, "DL5")["5"]["window_mean"] / olsen(5, "DL5"), "DL5 at 5"),
            ("DL5 at 10 spikes/s", pts(t54, "DL5")["10"]["window_mean"] / olsen(10, "DL5"), pts(t56, "DL5")["10"]["window_mean"] / olsen(10, "DL5"), "DL5 at 10"),
            ("Rmax", fit(t54, "rmax") / flies_fit("rmax"), fit(t56, "rmax") / flies_fit("rmax"), "Rmax"),
            ("sigma (below 1: steeper)", fit(t54, "sigma") / flies_fit("sigma"), fit(t56, "sigma") / flies_fit("sigma"), "sigma"),
            ("kept at 500 ms", pts(t54, "DL5")["80"]["at_500ms_over_peak"] / 0.44, pts(t56, "DL5")["80"]["at_500ms_over_peak"] / 0.44, "late/peak"),
            ("MBON11, 3-octanol", p54["mbon11_input"]["3-octanol"]["MBON11"] / 118, p56["condition"]["mbon11_input"]["3-octanol"]["MBON11"] / 118, "MBON11"),
            ("MCH/OCT, Kenyon cells", kc(p54["odors"]) / 0.82, kc(p56["condition"]["odors"]) / 0.82, "KC ratio"),
            ("MCH/OCT, PNs (weighed)", reliable_ratio(p55["equalization"]) / 1.11, reliable_ratio(p56["weighed_input"]["equalization"]) / 1.11, "PN ratio")]
    out = [text(24, 30, "Resting at flies' rate, the projection neurons answer weak input more as flies' do", "lab"),
           text(24, 50, "Left, middle: polished to flies' resting rate (about 5 spikes/s instead of 2.7), the PNs answer 1.2-1.4 times as "
                "strongly to weak input and keep more of strong", "note"),
           text(24, 68, "responses, closer to flies' points. Right: most measures move toward flies' (1); 4-methylcyclohexanol's share "
                "barely moves.", "note")]
    out += transform_panel(c, 70, 290, "DL5", pts(t54, "DL5"), pts(t56, "DL5"))
    out += transform_panel(c, 430, 290, "VM7d", pts(t54, "VM7d"), pts(t56, "VM7d"))
    out += summary_panel(c, 940, 160, rows)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = ("DL5's and VM7d's transforms with the projection neurons resting at 2.7 spikes/s and at about flies' rate, against "
             "flies', and eight measures as a share of flies' values before and after")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    e = ROOT / "experiments"
    p54 = json.loads((e / "odor_probe54.json").read_text())["condition"]
    p55 = json.loads((e / "odor_probe55.json").read_text())
    p56 = json.loads((e / "odor_probe56.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"al_rest-{theme}.svg"
        path_.write_text(figure(theme, p54, p55, p56))
        print(path_)


if __name__ == "__main__":
    main()
