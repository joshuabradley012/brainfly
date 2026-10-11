"""The antennal lobe's inhibition against an odor's strength (rung 9's groundwork), drawn from saved results (nothing by
hand).

    python assets/al_normalization.py      # writes assets/al_normalization-light.svg and assets/al_normalization-dark.svg

experiments/odor_normalization_check.py: for sixteen odors (DoOR's input), the presynaptic divisor over the first 0.5 s
against the odor's summed evoked receptor input, log-log, its excess D - 1: odor_probe56.py's model (grey; the inhibition
linear in the LNs' rate above rest) and odor_probe60.py's (red; that rate squared, with a small resting division).
The line: Olsen et al. 2010's normalization written as a divisor, (1 + (m s / sigma)^1.5)^(2/3) - 1, with m chosen so it
passes through the strong odors' divisor (Olsen & Wilson 2008's EPSCs, to which both models are fitted); its slope, not
its height, is the comparison.
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
W, H = 1120, 520
X0, X1, Y0, Y1 = 110, 700, 110, 440
SX = (300.0, 1400.0)
SY = (0.25, 2.5)
LABELLED = ("3-octanol", "4-methylcyclohexanol")
FLIES_BADEL = 0.98   # 4-methylcyclohexanol's PN response summed over Badel et al. 2016's 37 glomeruli, against 3-octanol's


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, before: dict, after: dict, badel: tuple[float, float]) -> str:
    c = THEMES[theme]
    sx = lambda v: X0 + (X1 - X0) * (np.log(v) - np.log(SX[0])) / (np.log(SX[1]) - np.log(SX[0]))
    sy = lambda v: Y1 - (Y1 - Y0) * (np.log(max(v, SY[0])) - np.log(SY[0])) / (np.log(SY[1]) - np.log(SY[0]))
    strong = [r for r in before["odors"].values() if r["summed_evoked_hz"] > 1000]
    s_ref = float(np.mean([r["summed_evoked_hz"] for r in strong]))
    d_ref = float(np.mean([r["divisor"] for r in strong]))
    x_ref = ((d_ref ** 1.5 - 1) ** (2 / 3))                      # m s / sigma at the strong odors
    curve = lambda s: (1 + (x_ref * s / s_ref) ** 1.5) ** (2 / 3) - 1
    out = [text(24, 30, "The antennal lobe's inhibition against an odor's strength", "lab"),
           text(24, 50, "Each dot an odor: its presynaptic divisor's excess over 1 against its summed receptor input. Flies' "
                "normalization grows as the line (Olsen et al. 2010);", "note"),
           text(24, 68, f"the model's linear inhibition grew about half as steeply (grey, slope {before['slope_model']:.2f}), "
                f"so weak odors lost too much; squared, it comes close (red, slope {after['slope_model']:.2f}; the line's 1.20).", "note")]
    for v in (300, 500, 700, 1000, 1400):
        out.append(f'<line x1="{sx(v):.1f}" y1="{Y0}" x2="{sx(v):.1f}" y2="{Y1}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(text(sx(v), Y1 + 18, f"{v:g}", "tick", "middle"))
    for v in (0.25, 0.5, 1.0, 2.0):
        out.append(f'<line x1="{X0}" y1="{sy(v):.1f}" x2="{X1}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(text(X0 - 8, sy(v) + 4, f"{v:g}", "tick", "end"))
    out.append(text((X0 + X1) / 2, Y1 + 40, "summed evoked receptor input (spikes/s, over glomeruli; log)", "tick", "middle"))
    out.append(f'<text transform="translate({X0 - 56},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">divisor - 1 (log)</text>')
    xs = np.exp(np.linspace(np.log(SX[0]), np.log(SX[1]), 60))
    pts = " ".join(f"{sx(s):.1f},{sy(curve(s)):.1f}" for s in xs)
    out.append(f'<polyline points="{pts}" fill="none" stroke="{c["ink"]}" stroke-width="1.6" stroke-dasharray="5 4"><title>Olsen et al. 2010, scaled to the strong odors</title></polyline>')
    out.append(text(sx(420), sy(curve(420)) + 24, "flies' normalization", "tick"))
    for data, color, r, label in ((before, "faint", 5, "linear (odor_probe56.py)"), (after, "red", 6, "squared + resting division (odor_probe60.py)")):
        for odor, row in data["odors"].items():
            x, y = sx(row["summed_evoked_hz"]), sy(row["divisor"] - 1)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c[color]}" stroke="{c["paper"]}" stroke-width="1.5">'
                       f'<title>{odor}: {row["summed_evoked_hz"]:.0f} spikes/s, divisor {row["divisor"]:.2f} ({label})</title></circle>')
    for odor in LABELLED:
        b, a = before["odors"][odor], after["odors"][odor]
        x = sx(a["summed_evoked_hz"])
        out.append(f'<line x1="{x:.1f}" y1="{sy(b["divisor"] - 1):.1f}" x2="{x:.1f}" y2="{sy(a["divisor"] - 1):.1f}" stroke="{c["muted"]}" stroke-width="1"/>')
    a = after["odors"]["3-octanol"]                              # the strong odors crowd: a leader to the empty lower right
    x, y, lx_, ly_ = sx(a["summed_evoked_hz"]), sy(a["divisor"] - 1), sx(1120), sy(0.95)
    out.append(f'<line x1="{x:.1f}" y1="{y + 7:.1f}" x2="{lx_ - 2:.1f}" y2="{ly_ - 12:.1f}" stroke="{c["muted"]}" stroke-width="1"/>')
    out.append(text(lx_, ly_, "3-octanol", "val"))
    b = before["odors"]["4-methylcyclohexanol"]
    out.append(text(sx(b["summed_evoked_hz"]), sy(b["divisor"] - 1) - 12, "4-methylcyclohexanol", "val", "middle"))
    lx, ly = X1 + 40, Y0 + 20                                    # legend and the two odors' numbers
    for k, (color, r, label) in enumerate((("faint", 5, "linear in the LNs' rate (before)"), ("red", 6, "squared, with a resting division (now)"))):
        out.append(f'<circle cx="{lx + 6}" cy="{ly + 22 * k}" r="{r}" fill="{c[color]}"/>')
        out.append(text(lx + 18, ly + 22 * k + 4, label, "tick"))
    out.append(f'<line x1="{lx}" y1="{ly + 44}" x2="{lx + 14}" y2="{ly + 44}" stroke="{c["ink"]}" stroke-dasharray="5 4" stroke-width="1.6"/>')
    out.append(text(lx + 18, ly + 48, "flies' normalization (Olsen et al. 2010)", "tick"))
    y = ly + 96
    for odor in LABELLED:
        b, a = before["odors"][odor], after["odors"][odor]
        out.append(text(lx, y, f"{odor}: divided by {b['divisor']:.2f} before, {a['divisor']:.2f} now", "tick"))
        y += 20
    out.append(text(lx, y + 14, "4-methylcyclohexanol at the PNs (Badel set, DoOR input):", "tick"))
    out.append(text(lx, y + 32, f"{badel[0]:.2f} of 3-octanol before, {badel[1]:.2f} now; flies {FLIES_BADEL:.2f}", "val"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = "The antennal lobe's presynaptic divisor against odor strength, two models against flies' normalization"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    before = json.loads((ROOT / "experiments" / "odor_normalization_check.json").read_text())
    p60 = json.loads((ROOT / "experiments" / "odor_probe60.json").read_text())
    p56 = json.loads((ROOT / "experiments" / "odor_probe56.json").read_text())
    badel = tuple(p["condition"]["equalization"]["mch_over_oct"]["badel_glomeruli_first"] for p in (p56, p60))
    for theme in THEMES:
        path_ = OUT / f"al_normalization-{theme}.svg"
        path_.write_text(figure(theme, before, p60["normalization"], badel))
        print(path_)


if __name__ == "__main__":
    main()
