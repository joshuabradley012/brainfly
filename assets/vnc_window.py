"""Rung 5's nerve cord: where its walking rhythm lives (exploratory checks), drawn from saved results (nothing by hand).

    python assets/vnc_window.py      # writes assets/vnc_window-light.svg and assets/vnc_window-dark.svg

Left: experiments/vnc_drive_sweep.py, DNg100 alone at drives 300-700 in the front legs' network: replicates of 16 with a
rhythm (top; left and right DNg100) and the network's active neurons in the first second (bottom, log), each point labelled
with DNg100's own rate; shaded where DNg100 would fire at the rates walking descending neurons recorded in flies reach
(20 spikes/s and more; research_notes/Embodied fly connectome simulation/descending_neuron_rates.md). Right:
experiments/vnc_codrive_check.py, DNg97 added at drives 0-400: the rhythm's frequency against DNg100's alone (marker area:
replicates with a rhythm), against flies' stepping, which DNg97's co-activation speeds by about half (Sapkal et al. 2026).
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
W, H = 1120, 560
SIDES = {"R": ("red", "right DNg100"), "L": ("ink", "left DNg100")}


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, sweep: dict, co: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "Rung 5's nerve cord: a walking rhythm only in a narrow window", "lab"),
           text(24, 50, "DNg100 drives front-leg rhythms only while it fires about 10-20 spikes/s; faster, the network runs away "
                "and silences it. Walking descending neurons in flies fire about 20-60.", "note"),
           text(24, 68, "Adding DNg97, which speeds headless flies' stepping by about half, speeds the model's rhythm by at most "
                "16%, and the rhythm falls apart.", "note")]
    # left: the drive sweep
    x0, pw = 90, 520
    drives = [int(k.split()[-1]) for k in sweep["conditions"]["R"]]
    dx = lambda d: x0 + pw * (d - 275) / (725 - 275)
    T0, T1 = 118, 268                        # rhythmic replicates
    B0, B1 = 318, 468                        # active neurons, log
    ty = lambda v: T1 - (T1 - T0) * v / 16
    by = lambda v: B1 - (B1 - B0) * (np.log10(max(v, 10)) - 1) / (np.log10(5000) - 1)
    # where DNg100 would fire at walking DNs' rates: from the drive at which the model's DNg100 reaches 20 spikes/s
    r = [sweep["conditions"]["R"][f"DNg100 {d}"]["dng100_hz"] for d in drives]
    at20 = 450 + 50 * (20.0 - r[drives.index(450)]) / max(r[drives.index(500)] - r[drives.index(450)], 1e-9) if r[drives.index(450)] < 20 else 450
    at20 = min(max(at20, 450), 500)
    out.append(f'<rect x="{dx(at20):.1f}" y="{T0}" width="{dx(725) - dx(at20):.1f}" height="{B1 - T0}" fill="{c["ink"]}" fill-opacity="0.06">'
               f'<title>DNg100 at 20 spikes/s or more, where walking descending neurons recorded in flies fire</title></rect>')
    out.append(text(dx(725) - 6, T0 + 14, "flies' walking DN rates (20+ spikes/s)", "tick", "end"))
    out.append(text(x0, T0 - 26, "replicates with a front-leg rhythm, of 16", "val"))
    out.append(text(x0 + pw, T0 - 26, "numbers: the right DNg100's own rate (spikes/s)", "tiny", "end"))
    out.append(text(x0, B0 - 12, "neurons active (log)", "val"))
    for v in (0, 8, 16):
        out.append(f'<line x1="{x0}" y1="{ty(v):.1f}" x2="{x0 + pw}" y2="{ty(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, ty(v) + 4, f"{v}", "tick", "end"))
    for v in (10, 100, 1000):
        out.append(f'<line x1="{x0}" y1="{by(v):.1f}" x2="{x0 + pw}" y2="{by(v):.1f}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(text(x0 - 8, by(v) + 4, f"{v:,}", "tick", "end"))
    for d in drives:
        out.append(text(dx(d), B1 + 18, f"{d}", "tick", "middle"))
    out.append(text(x0 + pw / 2, B1 + 38, "DNg100's drive (rung 5's units; attempt 3 tested 400 and 800)", "tick", "middle"))
    for side, (color, label) in SIDES.items():
        rows = [sweep["conditions"][side][f"DNg100 {d}"] for d in drives]
        pts = " ".join(f"{dx(d):.1f},{ty(rw['rhythmic']):.1f}" for d, rw in zip(drives, rows))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c[color]}" stroke-width="2"/>')
        pts = " ".join(f"{dx(d):.1f},{by(rw['active_median']):.1f}" for d, rw in zip(drives, rows))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c[color]}" stroke-width="2"/>')
        for d, rw in zip(drives, rows):
            title = f"{label}, drive {d}: {rw['rhythmic']} of 16 rhythmic; {rw['active_median']} neurons active; DNg100 {rw['dng100_hz']} spikes/s"
            out.append(f'<circle cx="{dx(d):.1f}" cy="{ty(rw["rhythmic"]):.1f}" r="4" fill="{c[color]}" stroke="{c["paper"]}" stroke-width="1.5"><title>{title}</title></circle>')
            out.append(f'<circle cx="{dx(d):.1f}" cy="{by(rw["active_median"]):.1f}" r="4" fill="{c[color]}" stroke="{c["paper"]}" stroke-width="1.5"><title>{title}</title></circle>')
            if side == "R":
                out.append(text(dx(d), ty(rw["rhythmic"]) - 10, f"{rw['dng100_hz']:.0f}", "tiny", "middle"))
    lx = x0 + 10
    for k, (side, (color, label)) in enumerate(SIDES.items()):
        out.append(f'<line x1="{lx + 150 * k}" y1="{B1 + 58}" x2="{lx + 150 * k + 20}" y2="{B1 + 58}" stroke="{c[color]}" stroke-width="2"/>')
        out.append(text(lx + 150 * k + 26, B1 + 62, label, "tick"))
    # right: the co-drive
    x1, pw1 = 720, 360
    Y0, Y1 = 118, 468
    d97 = [0, 100, 200, 400]
    cx = lambda d: x1 + pw1 * (d + 40) / 480
    fy = lambda f: Y1 - (Y1 - Y0) * (f - 0.9) / (1.7 - 0.9)
    out.append(text(x1, Y0 - 12, "with DNg97 added: rhythm frequency, against DNg100 alone", "val"))
    for f in (1.0, 1.25, 1.5):
        out.append(f'<line x1="{x1}" y1="{fy(f):.1f}" x2="{x1 + pw1}" y2="{fy(f):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if f == 1.0 else 0.5}"/>')
        out.append(text(x1 - 8, fy(f) + 4, f"{f:g}x", "tick", "end"))
    out.append(f'<rect x="{x1}" y="{fy(1.6):.1f}" width="{pw1}" height="{fy(1.4) - fy(1.6):.1f}" fill="{c["ink"]}" fill-opacity="0.07">'
               f'<title>flies: co-activating DNg97 raises ball stepping from about 8 to 12 Hz (Sapkal et al. 2026)</title></rect>')
    out.append(text(x1 + pw1 - 6, fy(1.6) - 6, "flies: about 1.5x (Sapkal et al. 2026)", "tick", "end"))
    for d in d97:
        out.append(text(cx(d), Y1 + 18, f"{d}", "tick", "middle"))
    out.append(text(x1 + pw1 / 2, Y1 + 38, "DNg97's drive (DNg100 at 400)", "tick", "middle"))
    names = ["DNg100 400", "DNg100 400 + DNg97 100", "DNg100 400 + DNg97 200", "DNg100 400 + DNg97 400"]
    for side, (color, label) in SIDES.items():
        rows = [co["conditions"][side][n] for n in names]
        base = rows[0]["freq_hz_median"]
        pts = []
        for d, rw in zip(d97, rows):
            if rw["freq_hz_median"] is None:
                continue
            f = rw["freq_hz_median"] / base
            pts.append(f"{cx(d):.1f},{fy(f):.1f}")
            rad = 2 + 5 * np.sqrt(rw["rhythmic"] / 16)
            out.append(f'<circle cx="{cx(d):.1f}" cy="{fy(f):.1f}" r="{rad:.1f}" fill="{c[color]}" stroke="{c["paper"]}" stroke-width="1.5">'
                       f'<title>{label}, DNg97 {d}: {rw["freq_hz_median"]} Hz, {rw["rhythmic"]} of 16 rhythmic</title></circle>')
            if d > 0:
                out.append(text(cx(d) + (9 if side == "R" else -9), fy(f) + (-9 if side == "R" else 15), f"{rw['rhythmic']}/16",
                                "tiny", "start" if side == "R" else "end"))
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c[color]}" stroke-width="1.6"/>')
    out.append(text(cx(0) + 10, fy(1.0) + 16, "16/16 each", "tiny"))
    out.append(text(x1, Y1 + 62, "marker area and labels: replicates still rhythmic, of 16 (red: the right DNg100)", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = "Rung 5's nerve cord model holds a walking rhythm only while DNg100 fires 10-20 spikes/s, and DNg97 barely speeds it"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    sweep = json.loads((ROOT / "experiments" / "vnc_drive_sweep.json").read_text())
    co = json.loads((ROOT / "experiments" / "vnc_codrive_check.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"vnc_window-{theme}.svg"
        path_.write_text(figure(theme, sweep, co))
        print(path_)


if __name__ == "__main__":
    main()
