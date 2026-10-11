"""The receptor synapse's slow component and the projection neurons' saturation (rung 9's groundwork), drawn from saved
results (nothing by hand).

    python assets/al_saturation.py      # writes assets/al_saturation-light.svg and assets/al_saturation-dark.svg

Left: DL5's cholinergic projection neurons' fast and slow synaptic currents over the last 300 ms of the odor against the
receptor neurons' rate (experiments/odor_drive_check.py, odor_probe52.py's model, Olsen et al.'s protocol). Middle: DL5's
transform measured as Olsen et al. measured flies, with the slow component depressing as Nagel et al. fitted it
(odor_probe52.py, grey) or as they measured it (odor_probe54.py, red), against flies' points and fit. Right:
4-methylcyclohexanol's summed response as a share of 3-octanol's at the receptor neurons, the projection neurons and the
Kenyon cells: flies (Barth et al. 2014, Badel et al. 2016, Hige et al. 2015; ranges as bars) and odor_probe54.py's model
with DoOR's input and with the receptor and PN-inferred fills (odor_probe53.py's Kenyon cells for the filled input).
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
W, H = 1120, 470
Y0, Y1 = 120, 370
FLY_DL5 = [(5.1, 44.2), (13.4, 84.9), (41.5, 148.6), (98.7, 158.4)]
OLSEN_DL5 = (167, 11.8)
XS = (5.0, 10.0, 20.0, 40.0, 80.0, 160.0)
STAGES = ("receptor neurons", "PNs", "Kenyon cells")
FLIES = ((0.41, 0.51), (0.85, 0.98), (0.73, 0.92))


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def path(points, sx, sy) -> str:
    return " ".join(f"{'M' if i == 0 else 'L'}{sx(x):.1f} {sy(y):.1f}" for i, (x, y) in enumerate(points))


def log_axis(c, x0, pw, label) -> tuple:
    lo, hi = np.log(4.0), np.log(200.0)
    sx = lambda x: x0 + pw * (np.log(x) - lo) / (hi - lo)
    out = [text(sx(x), Y1 + 15, f"{x}", "tick", "middle") for x in (5, 10, 20, 50, 100, 200)]
    out.append(text(x0 + pw / 2, Y1 + 32, label, "tick", "middle"))
    return sx, out


def currents_panel(c, x0, pw, drive) -> list[str]:
    vmax = 60.0
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), vmax) / vmax
    sx, out = log_axis(c, x0, pw, "receptor neurons' rise (spikes/s)")
    out.insert(0, text(x0, Y0 - 12, "DL5's synaptic currents, last 300 ms", "val"))
    for v in (0, 20, 40, 60):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    rates = [float(x) for x in drive["rates"]]
    for key, colour, label in (("pn_fast_current", "ink", "fast"), ("pn_slow_current", "red", "slow")):
        pts = [(x, drive["rates_hz"][f"{x:g}"]["last_300ms"][key]) for x in rates]
        out.append(f'<path d="{path(pts, sx, sy)}" fill="none" stroke="{c[colour]}" stroke-width="2.2"/>')
        for x, v in pts:
            out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="3.2" fill="{c[colour]}"><title>{label} current at {x:g} spikes/s: {v:.1f}</title></circle>')
        out.append(text(sx(pts[-1][0]) + 6, sy(pts[-1][1]) + 4, label, "tick"))
    return out


def transform_panel(c, x0, pw, p52, p54) -> list[str]:
    vmax = 180.0
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), vmax) / vmax
    sx, out = log_axis(c, x0, pw, "receptor neurons' rise (spikes/s)")
    out.insert(0, text(x0, Y0 - 12, "DL5's projection neurons, Olsen et al.'s protocol", "val"))
    for v in (0, 50, 100, 150):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    rmax, sigma = OLSEN_DL5
    grid = np.exp(np.linspace(np.log(4.0), np.log(200.0), 60))
    out.append(f'<path d="{path([(x, rmax * x ** 1.5 / (x ** 1.5 + sigma ** 1.5)) for x in grid], sx, sy)}" fill="none" '
               f'stroke="{c["ink"]}" stroke-width="1" stroke-opacity="0.7"/>')
    for x, v in FLY_DL5:
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6"/>')
    for label, colour, pts in (("slow component as fitted", "faint", p52), ("as measured", "red", p54)):
        series = [(x, pts[f"{x:g}"]["window_mean"]) for x in XS]
        out.append(f'<path d="{path(series, sx, sy)}" fill="none" stroke="{c[colour]}" stroke-width="2.2"/>')
        for x, v in series:
            out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="3.2" fill="{c[colour]}"><title>{label}: {v:.0f} spikes/s at {x:g}</title></circle>')
    out.append(text(x0 + pw - 4, Y1 - 52, "grey: slow component as fitted", "tick", "end"))
    out.append(text(x0 + pw - 4, Y1 - 38, "red: as measured; rings: flies", "tick", "end"))
    return out


def ratio_panel(c, x0, pw, model) -> list[str]:
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), 1.05) / 1.05
    out = [text(x0, Y0 - 12, "4-methylcyclohexanol as a share of 3-octanol", "val")]
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v:g}", "tick", "end"))
    step = pw / len(STAGES)
    for i, stage in enumerate(STAGES):
        cx = x0 + step * (i + 0.5)
        lo, hi = FLIES[i]
        out.append(f'<rect x="{cx - 9:.1f}" y="{sy(hi):.1f}" width="18" height="{sy(lo) - sy(hi):.1f}" fill="{c["ink"]}" fill-opacity="0.18">'
                   f'<title>flies, {stage}: {lo:g}-{hi:g}</title></rect>')
        out.append(text(cx, Y1 + 15, stage, "tick", "middle"))
    for key, colour, dx, label in (("DoOR", "faint", -20, "DoOR"), ("filled", "red", 20, "with fills")):
        pts = [(x0 + step * (i + 0.5) + dx, v) for i, v in enumerate(model[key])]
        out.append(" ".join(f'<circle cx="{x:.1f}" cy="{sy(v):.1f}" r="4.5" fill="{c[colour]}"><title>model ({label}): {v:.2f}</title></circle>'
                            for x, v in pts))
        out.append(f'<path d="{" ".join(f"{chr(77) if i == 0 else chr(76)}{x:.1f} {sy(v):.1f}" for i, (x, v) in enumerate(pts))}" '
                   f'fill="none" stroke="{c[colour]}" stroke-width="1.6"/>')
    out.append(text(x0 + pw - 4, Y0 + 6, "bars: flies; grey: DoOR; red: with fills", "tick", "end"))
    return out


def figure(theme: str, drive: dict, p52: dict, p54: dict, model: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "The slow receptor component kept the projection neurons from saturating; measured, it doesn't, and 4-methylcyclohexanol still trails", "lab"),
           text(24, 50, "Left: DL5's fast current is flat above 20 spikes/s of input; its slow current grows with the input (experiments/odor_drive_check.py). "
                "Middle: with the slow component", "note"),
           text(24, 68, "depressing as Nagel et al. measured it, the transform saturates as flies' does, at three quarters of their size. Right: "
                "the model barely raises 4-methylcyclohexanol.", "note")]
    out += currents_panel(c, 70, 300, drive)
    out += transform_panel(c, 440, 300, p52, p54)
    out += ratio_panel(c, 810, 290, model)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = ("DL5's synaptic currents against receptor input, its transform with the slow component as fitted and as measured, and "
             "4-methylcyclohexanol's share of 3-octanol at three stages in flies and the model")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    e = ROOT / "experiments"
    drive = json.loads((e / "odor_drive_check.json").read_text())
    p52 = json.loads((e / "odor_probe52.json").read_text())["condition"]
    p54 = json.loads((e / "odor_probe54.json").read_text())["condition"]
    p53 = json.loads((e / "odor_probe53.json").read_text())["conditions"]["receptor and PN-inferred fills"]
    kc = lambda od: od["4-methylcyclohexanol"]["kc_share"] / od["3-octanol"]["kc_share"]
    model = {"DoOR": [p54["equalization"]["mch_over_oct"]["orn_first"], p54["equalization"]["mch_over_oct"]["upn_first"], kc(p54["odors"])],
             "filled": [p54["equalization_filled"]["mch_over_oct"]["orn_first"], p54["equalization_filled"]["mch_over_oct"]["upn_first"],
                        kc(p53["odors"])]}
    t52 = p52["olsen_protocol"]["olsen"]["DL5"]["cholinergic"]["points"]
    t54 = p54["olsen_protocol"]["olsen"]["DL5"]["cholinergic"]["points"]
    for theme in THEMES:
        path_ = OUT / f"al_saturation-{theme}.svg"
        path_.write_text(figure(theme, drive, t52, t54, model))
        print(path_)


if __name__ == "__main__":
    main()
