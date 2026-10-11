"""What ends MBON11's odor response in the model, drawn from a saved check (nothing by hand).

    python assets/mbon11_burst.py      # writes assets/mbon11_burst-light.svg and assets/mbon11_burst-dark.svg

experiments/mbon11_burst_check.py, 3-octanol, mean of 4 seeds of 8 flies, smoothed as Hige et al. smoothed their PSTHs (a
Gaussian, SD 50 ms). Left: MBON11's rate in the four conditions (as in the learning test; the Kenyon cell-to-MBON11
synapses not depressing; APL silenced; both), against the points of flies' PSTH as research_notes/Rung 9 learning
data/mbon11_input.md reads them off Hige et al. 2015's Fig. 1E. Middle: the drive the Kenyon cells deliver onto MBON11
(each synapse's weight x its Kenyon cell's spikes x the strength its depression has left), as a share of its peak,
against flies' odor EPSC from 0.6 to 1.0 s (about 170 pA of a peak of about 400; Fig. 3C). Right: the Kenyon cells'
firing by class as tested, spikes/s per cell.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/looming.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 500
OCT = "3-octanol"
SD_S = 0.05
STYLES = {"as tested": ("red", 2.4, None), "not depressing": ("ink", 1.8, None), "APL silenced": ("faint", 1.8, None),
          "both": ("ink", 1.3, "5 4")}
LABELS = {"as tested": "as in the learning test", "not depressing": "synapses not depressing", "APL silenced": "APL silenced",
          "both": "both"}
PSTH = [(0.15, 6), (0.30, 137.5), (0.70, 97.5), (1.05, 97.5), (1.15, 80), (1.45, 6)]   # learning_movie.py's
CLASSES = {"alpha'/beta'": ("ink", None, "α′/β′"), "alpha/beta": ("ink", "5 3", "α/β"),
           "gamma": ("faint", None, "γ")}


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def smooth(v, dt: float) -> np.ndarray:
    v = np.asarray(v, float)
    half = int(round(3 * SD_S / dt))
    k = np.exp(-0.5 * (np.arange(-half, half + 1) * dt / SD_S) ** 2)
    return np.convolve(np.pad(v, half, mode="edge"), k / k.sum(), mode="valid")


def panel(c, x0, y0, pw, ph, top, step, unit, title, fmt="{:.0f}"):
    out = [text(x0, y0 - 14, title, "val")]
    ty = lambda v: y0 + ph - ph * min(max(v, 0.0), top) / top
    for v in np.arange(0, top + 1e-9, step):
        out.append(f'<line x1="{x0}" y1="{ty(v):.1f}" x2="{x0 + pw}" y2="{ty(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.45}"/>')
        out.append(text(x0 - 6, ty(v) + 4, fmt.format(v), "tick", "end"))
    out.append(text(x0 + 4, y0 + 10, unit, "tiny"))
    tx = lambda t: x0 + pw * (t + 0.5) / 2.0
    out.append(f'<rect x="{tx(0):.1f}" y="{y0}" width="{tx(1.0) - tx(0):.1f}" height="{ph}" fill="{c["ink"]}" fill-opacity="0.05"/>')
    out.append(text(tx(1.0) - 4, y0 + 10, "odor", "tiny", "end"))
    for t in (-0.5, 0, 0.5, 1.0, 1.5):
        out.append(text(tx(t), y0 + ph + 16, f"{t:g}".replace("-", "−"), "tick", "middle"))
    out.append(text(x0 + pw / 2, y0 + ph + 34, "time from the odor's onset (s)", "tick", "middle"))
    return out, tx, ty


def line(c, tx, ty, ts, v, color, width, dash, title):
    pts = " ".join(f"{tx(t):.1f},{ty(x):.1f}" for t, x in zip(ts, v))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts}" fill="none" stroke="{c[color]}" stroke-width="{width}"{d}><title>{title}</title></polyline>'


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    dt = d["bin_s"]
    ts = d["t0"] + (np.arange(200) + 0.5) * dt
    cond = {name: rows[OCT] for name, rows in d["conditions"].items()}
    tested, free = cond["as tested"], cond["not depressing"]
    out = [text(24, 30, "What ends MBON11's burst: the depression of its Kenyon cell synapses", "lab"),
           text(24, 50, f"Without it, MBON11's response to 3-octanol holds as flies' does ({free['mbon11']['hz_0.5_to_1s']:.0f} spikes/s "
                f"from 0.5 to 1 s, flies 95-100; {free['mbon11']['evoked_spikes']:.0f} evoked spikes, flies 118), though it peaks too "
                f"high ({free['mbon11']['peak_hz']:.0f}, flies 135-140).", "note"),
           text(24, 68, "Silencing APL doubles the Kenyon cells' firing but leaves the response brief. As tested the Kenyon cells keep "
                f"firing, but the synapses their first spikes", "note"),
           text(24, 86, f"depressed deliver {100 * tested['drive']['late_over_peak']:.1f}% of the peak drive from 0.6 s on, where flies' "
                f"EPSC keeps 43%.", "note")]
    y0, ph, pw = 150, 250, 290
    # left: MBON11
    o, tx, ty = panel(c, 80, y0, pw, ph, 350, 100, "spikes/s", "MBON11's response to 3-octanol")
    out += o
    pts = " ".join(f"{tx(t):.1f},{ty(v):.1f}" for t, v in PSTH)
    out.append(f'<polyline points="{pts}" fill="none" stroke="{c["ink"]}" stroke-width="1" stroke-dasharray="2 3"/>')
    for t, v in PSTH:
        out.append(f'<circle cx="{tx(t):.1f}" cy="{ty(v):.1f}" r="3.2" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.3">'
                   f'<title>flies (Hige et al. 2015, Fig. 1E, read off the figure): {v:g} spikes/s at {t:g} s</title></circle>')
    for name, (color, width, dash) in STYLES.items():
        m = cond[name]["mbon11"]
        out.append(line(c, tx, ty, ts, smooth(cond[name]["series"]["mbon_hz"], dt), color, width, dash,
                        f"{LABELS[name]}: peak {m['peak_hz']} spikes/s, {m['evoked_spikes']} evoked spikes, {m['hz_0.5_to_1s']} spikes/s from 0.5 to 1 s"))
    # middle: the delivered drive, as a share of its peak
    o, tx, ty = panel(c, 450, y0, pw, ph, 1.0, 0.25, "share of the peak", "The drive the Kenyon cells deliver", "{:g}")
    out += o
    out.append(f'<rect x="{tx(0.6):.1f}" y="{ty(0.47):.1f}" width="{tx(1.0) - tx(0.6):.1f}" height="{ty(0.39) - ty(0.47):.1f}" '
               f'fill="{c["ink"]}" fill-opacity="0.18"><title>flies: odor EPSC about 170 pA from 0.6 to 1.0 s, of a peak of about 400 '
               f'(Hige et al. 2015, Fig. 3C)</title></rect>')
    out.append(text(tx(1.0) + 4, ty(0.43) + 4, "flies' EPSC", "tiny"))
    for name, (color, width, dash) in STYLES.items():
        drive = np.sum([cond[name]["series"]["drive"][k] for k in cond[name]["series"]["drive"]], 0)
        rest = drive[ts < 0].mean()
        sm = smooth(drive - rest, dt)
        out.append(line(c, tx, ty, ts, sm / sm.max(), color, width, dash,
                        f"{LABELS[name]}: from 0.6 to 1.0 s, {cond[name]['drive']['late_over_peak']} of the peak"))
    # right: the Kenyon cells by class, as tested
    o, tx, ty = panel(c, 820, y0, pw - 10, ph, 3.5, 1.0, "spikes/s per cell", "Kenyon cells as tested, by class", "{:g}")
    out += o
    for name, (color, dash, label) in CLASSES.items():
        v = smooth(tested["series"]["kc_hz"][name], dt)
        k = tested["kcs"][name]
        out.append(line(c, tx, ty, ts, v, color, 1.8, dash, f"{label}: {k['hz_per_cell_0_to_0.3s']} spikes/s per cell in the first 0.3 s, "
                                                           f"{k['hz_per_cell_0.5_to_1s']} from 0.5 to 1 s"))
        k_ = list(CLASSES).index(name)                  # a legend in the panel's empty upper right
        d_ = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{tx(1.05):.1f}" y1="{ty(3.25 - 0.35 * k_):.1f}" x2="{tx(1.25):.1f}" y2="{ty(3.25 - 0.35 * k_):.1f}" '
                   f'stroke="{c[color]}" stroke-width="1.8"{d_}/>')
        out.append(text(tx(1.29), ty(3.25 - 0.35 * k_) + 4, label, "tick"))
    # legend
    lx, ly = 80, H - 22
    for k, (name, (color, width, dash)) in enumerate(STYLES.items()):
        x = lx + 190 * k
        d_ = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{x}" y1="{ly - 4}" x2="{x + 22}" y2="{ly - 4}" stroke="{c[color]}" stroke-width="{width}"{d_}/>')
        out.append(text(x + 28, ly, LABELS[name], "tick"))
    x = lx + 190 * 4
    out.append(f'<line x1="{x}" y1="{ly - 4}" x2="{x + 30}" y2="{ly - 4}" stroke="{c["ink"]}" stroke-width="1" stroke-dasharray="2 3"/>')
    out.append(f'<circle cx="{x + 15}" cy="{ly - 4}" r="3.2" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.3"/>')
    out.append(text(x + 36, ly, "flies (Hige et al. 2015)", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = "MBON11's response to 3-octanol holds like flies' only when its Kenyon cell synapses don't depress"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "mbon11_burst_check.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"mbon11_burst-{theme}.svg"
        path_.write_text(figure(theme, d))
        print(path_)


if __name__ == "__main__":
    main()
