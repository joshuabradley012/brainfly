"""Yamada et al.'s flash in the model, and the odor EPSC a slow Kenyon cell current predicts, drawn from saved results
(nothing by hand).

    python assets/kc_flash.py      # writes assets/kc_flash-light.svg and assets/kc_flash-dark.svg

Left: experiments/kc_flash_check.py, the gamma Kenyon cells at the model's 20 ms membrane time constant, one spike per
flashed cell per flash: the current into MBON11 through the model's 5 ms synapses and through the slow current (rising
with 40 ms, decaying with 280 ms), each as a share of its first peak, against Yamada et al. 2024's flash EPSC as
research_notes/Rung 9 learning data/mbon11_kc_activity.md 2.1 measures it (peak 102-118 ms after the flash, 0.32-0.39 of
it left at 400 ms, the second flash 0.38-0.68 of the first). Middle: when the flashed cells fire, the share of the first
flash's spikes by each time after it, at four membrane time constants (three spikes per cell). Right:
experiments/mbon11_slow_epsc.py, 3-octanol as in the learning test: the current the Kenyon cells deliver to MBON11 through
each, against flies' odor EPSC (Hige et al. 2015, Fig. 3; mbon11_input.md 2.5: about 380-430 pA at its peak, about 170 pA
from 0.6 to 1.0 s, starting about 0.18 s after the odor valve opens).
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
W, H = 1120, 590
TAU_STYLE = {"0.02": ("red", None, "20 ms (the model)"), "0.05": ("ink", None, "50 ms"), "0.1": ("ink", "5 3", "100 ms"),
             "0.15": ("faint", None, "150 ms")}


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def axes(c, x0, y0, pw, ph, xs, ys, xlab, ylab, title, xfmt="{:g}", yfmt="{:g}"):
    """Gridlines and ticks; returns the drawing and the two scales."""
    (xa, xb, xticks), (ya, yb, yticks) = xs, ys
    tx = lambda v: x0 + pw * (v - xa) / (xb - xa)
    ty = lambda v: y0 + ph - ph * (min(max(v, ya), yb) - ya) / (yb - ya)
    out = [text(x0, y0 - 14, title, "val")]
    for v in yticks:
        out.append(f'<line x1="{x0}" y1="{ty(v):.1f}" x2="{x0 + pw}" y2="{ty(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == ya else 0.45}"/>')
        out.append(text(x0 - 6, ty(v) + 4, yfmt.format(v), "tick", "end"))
    for v in xticks:
        out.append(text(tx(v), y0 + ph + 16, xfmt.format(v), "tick", "middle"))
    out.append(text(x0 + pw / 2, y0 + ph + 34, xlab, "tick", "middle"))
    out.append(text(x0 + 4, y0 + 10, ylab, "tiny"))
    return out, tx, ty


def poly(c, tx, ty, xs, ys, color, width, dash=None, title=""):
    pts = " ".join(f"{tx(x):.1f},{ty(y):.1f}" for x, y in zip(xs, ys))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts}" fill="none" stroke="{c[color]}" stroke-width="{width}"{d}><title>{title}</title></polyline>'


def bar(c, x, y_lo, y_hi, tx, ty, title, w=7):
    """A measured range, as a short vertical bar with caps."""
    out = [f'<line x1="{tx(x):.1f}" y1="{ty(y_lo):.1f}" x2="{tx(x):.1f}" y2="{ty(y_hi):.1f}" stroke="{c["ink"]}" stroke-width="2"><title>{title}</title></line>']
    for y in (y_lo, y_hi):
        out.append(f'<line x1="{tx(x) - w / 2:.1f}" y1="{ty(y):.1f}" x2="{tx(x) + w / 2:.1f}" y2="{ty(y):.1f}" stroke="{c["ink"]}" stroke-width="2"/>')
    return out


def figure(theme: str, flash: dict, epsc: dict) -> str:
    c = THEMES[theme]
    one = flash["conditions"]["0.02"]["targets"]["1"]
    dt = flash["bin_s"]
    t = flash["t0"] + (np.arange(len(one["series"]["current_fast_pa"])) + 0.5) * dt
    oct_ = epsc["conditions"]["as tested"]["3-octanol"]
    out = [text(24, 30, "Yamada et al.'s flash, in the model: the Kenyon cell current into MBON11 is too fast", "lab"),
           text(24, 50, "Flashed, the model's Kenyon cells fire within about 50 ms whatever their membrane time constant, so its 5 ms "
                "synapses deliver a flash's charge in about 10 ms,", "note"),
           text(24, 68, f"peaking at {one['current_fast']['peak']:,.0f} pA where flies' EPSC reaches 80-117 pA over about 250 ms. Through "
                "a slow current the same input gives flies' flash EPSC, and from the model's", "note"),
           text(24, 86, f"Kenyon cells and depression as they are, their odor EPSC's peak ({oct_['slow']['peak_pa']:.0f} pA; flies about "
                f"400) and about half its plateau ({oct_['slow']['pa_0.6_to_1s']:.0f} pA; flies about 170).", "note")]
    y0, ph = 150, 280
    # left: the flash
    o, tx, ty = axes(c, 80, y0, 300, ph, (0.0, 0.8, (0, 0.2, 0.4, 0.6, 0.8)), (0.0, 1.0, (0, 0.25, 0.5, 0.75, 1.0)),
                     "time from the first flash (s)", "", "Flashes at 0 and 0.4 s: share of the first peak")
    out += o
    for x in (0.0, 0.4):
        out.append(f'<line x1="{tx(x):.1f}" y1="{y0}" x2="{tx(x):.1f}" y2="{y0 + ph}" stroke="{c["faint"]}" stroke-dasharray="1 3"/>')
    keep = t <= 0.8
    for key, color, width, label in (("current_fast_pa", "red", 1.8, "the model's 5 ms current"), ("current_slow_pa", "ink", 2.2, "a slow current")):
        v = np.asarray(one["series"][key])
        v = (v - v[t < 0].mean())
        v = v / v[(t > 0) & (t < 0.4)].max()
        out.append(poly(c, tx, ty, t[keep], v[keep], color, width, title=label))
    s = one["current_slow"]
    out += bar(c, 0.11, 0.97, 1.0, tx, ty, "flies: peak 102-118 ms after the flash")
    out.append(f'<line x1="{tx(0.102):.1f}" y1="{ty(1.0):.1f}" x2="{tx(0.118):.1f}" y2="{ty(1.0):.1f}" stroke="{c["ink"]}" stroke-width="3"/>')
    out += bar(c, 0.395, 0.32, 0.39, tx, ty, "flies: 0.32-0.39 of the peak left at 400 ms")
    tail = s["left_at_400ms"]
    out += bar(c, 0.51, tail + 0.38, tail + 0.68, tx, ty, "flies: the second flash 0.38-0.68 of the first (above the current left)")
    out.append(text(80, y0 + ph + 52, "One spike per flashed cell, 20 ms membranes. Bars: flies'", "tiny"))
    out.append(text(80, y0 + ph + 66, "peak (102-118 ms), share left at 400 ms (0.32-0.39), second flash", "tiny"))
    out.append(text(80, y0 + ph + 80, f"(0.38-0.68). First peaks: {one['current_fast']['peak']:,.0f} pA (the model), {s['peak']:.0f} pA (slow; flies 80-117).", "tiny"))
    # middle: when the flashed cells fire
    o, tx, ty = axes(c, 470, y0, 260, ph, (0.0, 0.15, (0, 0.05, 0.1, 0.15)), (0.0, 1.0, (0, 0.5, 1.0)),
                     "time from the flash (s)", "", "When the flashed cells fire: share of their spikes")
    out += o
    out += bar(c, 0.11, 0.0, 0.08, tx, ty, "flies' EPSC peaks 102-118 ms after the flash")
    out.append(text(470, y0 + ph + 52, "Three spikes per flashed cell. Bar: when flies' flash EPSC peaks.", "tiny"))
    for tau, (color, dash, label) in TAU_STYLE.items():
        r = flash["conditions"][tau]["targets"].get("3")
        if not r:
            continue
        spk = np.asarray(r["series"]["spikes_per_cell"])
        w = (t > 0) & (t < 0.4)
        cum = np.cumsum(spk[w]) / spk[w].sum()
        sel = t[w] <= 0.15
        out.append(poly(c, tx, ty, t[w][sel], cum[sel], color, 1.8, dash, f"tau_m {label}: 90% of the spikes by {r['spikes_per_cell']['ninety_percent_by_s'] * 1000:.0f} ms"))
    ly = y0 + 150
    for k, (tau, (color, dash, label)) in enumerate(TAU_STYLE.items()):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{tx(0.075):.1f}" y1="{ly + 18 * k:.1f}" x2="{tx(0.09):.1f}" y2="{ly + 18 * k:.1f}" stroke="{c[color]}" stroke-width="1.8"{d}/>')
        out.append(text(tx(0.093), ly + 18 * k + 4, label, "tick"))
    out.append(text(tx(0.075), ly - 14, "membrane time constant", "tick"))
    # right: the odor EPSC
    te = -0.5 + (np.arange(200) + 0.5) * 0.01
    o, tx, ty = axes(c, 820, y0, 260, ph, (-0.5, 1.5, (-0.5, 0, 0.5, 1.0, 1.5)), (0.0, 800.0, (0, 200, 400, 600, 800)),
                     "time from the odor's onset (s)", "", "3-octanol: the EPSC each gives (pA per cell)")
    out += o
    out.append(f'<rect x="{tx(0):.1f}" y="{y0}" width="{tx(1.0) - tx(0):.1f}" height="{ph}" fill="{c["ink"]}" fill-opacity="0.05"/>')
    out.append(f'<rect x="{tx(0.18):.1f}" y="{ty(430):.1f}" width="{tx(0.32) - tx(0.18):.1f}" height="{ty(380) - ty(430):.1f}" fill="{c["ink"]}" fill-opacity="0.25">'
               f'<title>flies: peak about 380-430 pA</title></rect>')
    out.append(f'<rect x="{tx(0.6):.1f}" y="{ty(185):.1f}" width="{tx(1.0) - tx(0.6):.1f}" height="{ty(155) - ty(185):.1f}" fill="{c["ink"]}" fill-opacity="0.25">'
               f'<title>flies: about 170 pA from 0.6 to 1.0 s</title></rect>')
    out.append(text(tx(0.33) + 4, ty(405) + 4, "flies' peak", "tiny"))
    out.append(text(tx(1.0) + 4, ty(170) + 4, "flies", "tiny"))
    for key, color, width, label in (("fast", "red", 1.8, "the model's 5 ms current"), ("slow", "ink", 2.2, "the slow current")):
        v = np.asarray(oct_[key]["series_pa"])
        r = oct_[key]
        out.append(poly(c, tx, ty, te, v, color, width, title=f"{label}: peak {r['peak_pa']:.0f} pA at {r['t_peak_s']} s, {r['pa_0.6_to_1s']:.0f} pA from 0.6 to 1.0 s, "
                                                             f"{r['charge_pc_0_to_1.4s']:.0f} pC over 0-1.4 s"))
    out.append(text(tx(0.12), ty(800) + 12, f"← {oct_['fast']['peak_pa']:,.0f} pA at {oct_['fast']['t_peak_s'] * 1000:.0f} ms", "tiny"))
    out.append(text(820, y0 + ph + 52, "As in the learning test. Shaded: flies' peak and plateau", "tiny"))
    out.append(text(820, y0 + ph + 66, "(Hige et al. 2015); flies' EPSC starts 0.18 s after their valve.", "tiny"))
    # legend
    lx, ly = 80, H - 22
    for k, (color, width, label) in enumerate((("red", 1.8, "through the model's 5 ms current"), ("ink", 2.2, "through a slow current (rising 40 ms, decaying 280 ms)"))):
        x = lx + 260 * k
        out.append(f'<line x1="{x}" y1="{ly - 4}" x2="{x + 22}" y2="{ly - 4}" stroke="{c[color]}" stroke-width="{width}"/>')
        out.append(text(x + 28, ly, label, "tick"))
    out.append(text(lx + 640, ly, "bars: flies (Yamada et al. 2024; Hige et al. 2015)", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = "In the model a flash of Kenyon cells gives MBON11 a current 30 times faster than flies'; a slow current gives flies' flash and odor EPSCs"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    flash = json.loads((ROOT / "experiments" / "kc_flash_check.json").read_text())
    epsc = json.loads((ROOT / "experiments" / "mbon11_slow_epsc.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"kc_flash-{theme}.svg"
        path_.write_text(figure(theme, flash, epsc))
        print(path_)


if __name__ == "__main__":
    main()
