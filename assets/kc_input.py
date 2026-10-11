"""The Kenyon cells' projection neuron input as the model ran it, against flies' and corrected, drawn from saved results
and the simulator's own step (nothing by hand).

    python assets/kc_input.py      # writes assets/kc_input-light.svg and assets/kc_input-dark.svg

Left: one projection neuron spike's EPSP in a Kenyon cell (the simulator's step, brainfly.hybrid's coefficients, from
experiments/kc_input_audit.json's mean synapse weight) as the model ran it (1.90 mV) and at mb_calibration6.py's 1.4 mV,
against flies' unitary EPSPs (Gruntman & Turner 2013: 1.24-1.48 mV; Turner et al. 2008: 1.4 mV). Middle: the steady
depolarization one connection gives at each projection neuron rate (the response's area times the rate), against
Gruntman & Turner's plateau (about 4.4 mV per connection at 115 spikes/s; research_notes/Rung 9 learning
data/kc_integration.md). Right: experiments/kc_epsp_check.json, three measures as a share of flies' value, as the model
ran and at the measured 1.4 mV (and 1.24 mV): the Kenyon cells answering 3-octanol (flies about 12%), those answering
4-methylcyclohexanol per one answering 3-octanol (flies 49 per 53, Hige et al. 2015), and the odor charge their synapses
would give MBON11 through the slow current (flies about 245-250 pC).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from brainfly.hybrid import _approach                     # noqa: E402
from brainfly.shiu import TAU                              # noqa: E402

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/looming.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 500
DT, TAU_M = 1e-4, 0.020
FLIES = {"density": 0.12, "mch_per_oct": 49 / 53, "charge_pc": 247.5}


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def axes(c, x0, y0, pw, ph, xs, ys, xlab, title, xfmt="{:g}", yfmt="{:g}"):
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
    return out, tx, ty


def poly(c, tx, ty, xs, ys, color, width, dash=None, title=""):
    pts = " ".join(f"{tx(x):.1f},{ty(y):.1f}" for x, y in zip(xs, ys))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts}" fill="none" stroke="{c[color]}" stroke-width="{width}"{d}><title>{title}</title></polyline>'


def epsp(w: float, steps: int = 800) -> np.ndarray:
    """The simulator's step from a jump of w in the synaptic current (u <- a_vv u + a_vx x, x <- a_xx x)."""
    a_vv, a_vx, a_xx = np.exp(-DT / TAU_M), _approach(TAU, TAU_M, DT), np.exp(-DT / TAU)
    u, x, out = 0.0, w, np.zeros(steps + 1)
    for t in range(steps):
        u, x = a_vv * u + a_vx * x, a_xx * x
        out[t + 1] = u
    return out


def figure(theme: str, audit: dict, check: dict) -> str:
    c = THEMES[theme]
    w_run = audit["classes"]["alpha/beta"]["mean_weight_mv"]
    run = epsp(w_run)
    fixed = run * (1.4 / run.max())
    t_ms = np.arange(len(run)) * DT * 1000
    area_run = float(epsp(w_run, 20000).sum() * DT)         # mV s per spike, over 2 s (100 time constants)
    area_fixed = area_run * 1.4 / run.max()
    cond = check["conditions"]
    out = [text(24, 30, "The Kenyon cells' input was a third stronger than flies'", "lab"),
           text(24, 50, f"One projection neuron spike gave a Kenyon cell {run.max():.2f} mV: the calibration aimed at 1.4 mV after the "
                "synapse's resting depression, but these synapses don't depress.", "note"),
           text(24, 68, "At the measured size the cells answer at the low end of flies' density, 4-methylcyclohexanol reaches a seventh "
                "as many cells as 3-octanol, and MBON11 gets under a third of flies' charge.", "note")]
    y0, ph = 130, 260
    # left: the EPSP
    o, tx, ty = axes(c, 70, y0, 290, ph, (0, 80, (0, 20, 40, 60, 80)), (0, 2.0, (0, 0.5, 1.0, 1.5, 2.0)),
                     "time after the spike (ms)", "One spike's EPSP in a Kenyon cell (mV)")
    out += o
    out.append(f'<rect x="{tx(0):.1f}" y="{ty(1.48):.1f}" width="{tx(80) - tx(0):.1f}" height="{ty(1.24) - ty(1.48):.1f}" fill="{c["ink"]}" fill-opacity="0.08">'
               f'<title>flies: unitary EPSPs 1.24-1.48 mV (Gruntman &amp; Turner 2013)</title></rect>')
    out.append(text(tx(78), ty(1.48) - 5, "flies 1.24–1.48", "tiny", "end"))
    out.append(poly(c, tx, ty, t_ms, run, "ink", 2.2, title=f"as the model ran: {run.max():.2f} mV"))
    out.append(poly(c, tx, ty, t_ms, fixed, "red", 2.2, title="corrected (mb_calibration6.py): 1.40 mV"))
    j = int(np.argmax(run))
    out.append(text(tx(t_ms[j]) + 6, ty(run.max()) - 6, f"as run, {run.max():.2f} mV", "tick"))
    out.append(text(tx(26), ty(1.36) + 4, "corrected, 1.40 mV", "tick"))
    # middle: the steady drive
    o, tx, ty = axes(c, 450, y0, 260, ph, (0, 150, (0, 50, 100, 150)), (0, 10, (0, 2, 4, 6, 8, 10)),
                     "projection neuron rate (spikes/s)", "Steady drive per connection (mV)")
    out += o
    r = np.array([0.0, 150.0])
    out.append(poly(c, tx, ty, r, r * area_run, "ink", 2.2, title=f"as run: {115 * area_run:.2f} mV at 115 spikes/s"))
    out.append(poly(c, tx, ty, r, r * area_fixed, "red", 2.2, title=f"corrected: {115 * area_fixed:.2f} mV at 115 spikes/s"))
    out.append(f'<circle cx="{tx(115):.1f}" cy="{ty(4.4):.1f}" r="5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="2">'
               f'<title>flies: about 4.4 mV per connection at 115 spikes/s (Gruntman &amp; Turner 2013)</title></circle>')
    out.append(text(tx(115) + 9, ty(4.4) + 15, "flies", "tick"))
    out.append(text(tx(150) - 4, ty(150 * area_run) - 6, f"as run, {115 * area_run:.1f} at 115", "tick", "end"))
    out.append(text(tx(52), ty(52 * area_fixed) + 26, f"corrected, {115 * area_fixed:.1f} at 115", "tick"))
    # right: the consequences, as a share of flies'
    o, tx, ty = axes(c, 800, y0, 290, ph, (0, 3, ()), (0, 1.4, (0, 0.25, 0.5, 0.75, 1.0, 1.25)),
                     "", "As a share of flies' value", yfmt="{:.2f}")
    out += o
    out.append(f'<line x1="{tx(0):.1f}" y1="{ty(1):.1f}" x2="{tx(3):.1f}" y2="{ty(1):.1f}" stroke="{c["ink"]}" stroke-dasharray="4 3"><title>flies</title></line>')
    out.append(text(tx(3) - 2, ty(1) - 5, "flies", "tick", "end"))
    measures = [("Kenyon cells", "answering 3-octanol", lambda d: d["share_answering_3_octanol"] / FLIES["density"],
                 lambda d: f'{100 * d["share_answering_3_octanol"]:.1f}% of cells (flies about 12%)'),
                ("4-methylcyclohexanol's", "cells per 3-octanol's", lambda d: d["answering_mch_over_oct"]["APL working"] / FLIES["mch_per_oct"],
                 lambda d: f'{d["answering_mch_over_oct"]["APL working"]:.2f} (flies 0.92)'),
                ("MBON11's", "odor charge", lambda d: d["by_odor"]["3-octanol"]["mbon11_slow_current"]["charge_pc_0_to_1.4s"] / FLIES["charge_pc"],
                 lambda d: f'{d["by_odor"]["3-octanol"]["mbon11_slow_current"]["charge_pc_0_to_1.4s"]:.0f} pC (flies 245-250)')]
    shades = (("as now", "ink", 0.85, "as run"), ("1.4 mV", "red", 1.0, "1.4 mV"), ("1.24 mV", "faint", 1.0, "1.24 mV"))
    for i, (l1, l2, f, desc) in enumerate(measures):
        for k, (key, color, opacity, label) in enumerate(shades):
            v = f(cond[key])
            bx = tx(i + 0.5) - 33 + 22 * k
            out.append(f'<rect x="{bx:.1f}" y="{ty(v):.1f}" width="20" height="{ty(0) - ty(v):.1f}" fill="{c[color]}" fill-opacity="{opacity}">'
                       f'<title>{l1} {l2}, {label}: {desc(cond[key])}</title></rect>')
        out.append(text(tx(i + 0.5), y0 + ph + 16, l1, "tiny", "middle"))
        out.append(text(tx(i + 0.5), y0 + ph + 29, l2, "tiny", "middle"))
    ly = y0 + ph + 56
    for k, (key, color, opacity, label) in enumerate(shades):
        x = 800 + (0, 80, 205)[k]
        out.append(f'<rect x="{x}" y="{ly - 10}" width="14" height="12" fill="{c[color]}" fill-opacity="{opacity}"/>')
        out.append(text(x + 20, ly, label + (", adopted" if key == "1.4 mV" else ""), "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = "The model's Kenyon cell input was a third stronger than flies'; at the measured size the cells answer less and MBON11 gets a third of flies' charge"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    load = lambda name: json.loads((ROOT / "experiments" / f"{name}.json").read_text())
    audit, check = load("kc_input_audit"), load("kc_epsp_check")
    for theme in THEMES:
        path_ = OUT / f"kc_input-{theme}.svg"
        path_.write_text(figure(theme, audit, check))
        print(path_)


if __name__ == "__main__":
    main()
