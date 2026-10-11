"""APL as a conductance with flies' time course (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/apl_conductance.py      # writes assets/apl_conductance-light.svg and assets/apl_conductance-dark.svg

Left: how far APL holds the Kenyon cells down during 3-octanol (DoOR's input), their mean free membrane potential with APL
working less silenced, 50 ms means from the odor's onset: the calibrated APL (grey; mb_calibration.py, a current,
saturating) and the graded APL as a current (dashed; mb_calibration2.py), from experiments/odor_apl_conductance_check.py,
and the graded APL as a conductance reversing 20 mV below each Kenyon cell's rest and decaying over 0.3 s (red;
mb_calibration4.py), from experiments/odor_apl_conductance2_check.py; against the 10-12 mV at which flies' APL saturates
(shaded; Inada et al. 2017) and the 15 mV that is the most Kenyon cells have been seen inhibited through it (line;
Vrontou et al. 2021). Middle: Inada et al.'s Fig. 5B on the model, APL driven to its ceiling for 1 s at rest, the quiet
Kenyon cells' inhibition as a share of its plateau (red), against flies' landmarks (rings; research_notes/Rung 9 learning
data/apl_kinetics.md): 10, 50 and 90% of the plateau at 0.14, 0.27 and 0.56 s, half gone 0.32 s after the drive, about
0.22 left after 1 s. Right: every conductance tried in odor_apl_conductance2_check.py, APL's 4-methylcyclohexanol/
3-octanol peak ratio against the rise silencing APL gives the Kenyon cells' spikes, each a segment spanning the two odors;
flies' 2-3-fold rise (shaded) and APL's 0.49 (Prisco et al. 2021; line); the two currents for comparison (rings).
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
W, H = 1120, 570
Y0, Y1 = 140, 440
CALIBRATED = "mb_calibration.py (fast current), drive 10, effect 1"
GRADED = "mb_calibration2.py (fast current), drive 1.5, effect 2.5"
ODORS = ("3-octanol", "4-methylcyclohexanol")
FLY_RISE = ((0.14, 0.1), (0.27, 0.5), (0.56, 0.9))
FLY_FALL = ((1.32, 0.5), (2.0, 0.22))


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, first: dict, second: dict) -> str:
    c = THEMES[theme]
    ch_name = second["chosen"]["condition"]
    ch = second["conditions"][ch_name]
    ca, gr = first["conditions"][CALIBRATED], first["conditions"][GRADED]
    inada = second["inada_5b"][f"{ch_name} | reversal -20 mV"]
    out = [text(24, 30, "APL as a conductance: graded like flies', within flies' limits, and as slow as flies'", "lab"),
           text(24, 50, "APL's synapses onto the Kenyon cells reverse 20 mV below each cell's rest and fade over 0.3 s: APL answers "
                f"4-methylcyclohexanol with {ch['apl_peak_mch_over_oct']:.2f} of its 3-octanol peak (flies 0.49),", "note"),
           text(24, 68, f"silencing it raises the Kenyon cells' spikes {ch['3-octanol']['block_ratio']:.1f}- and "
                f"{ch['4-methylcyclohexanol']['block_ratio']:.1f}-fold (flies 2-3), and it never holds them past "
                f"{abs(ch['3-octanol']['largest_inhibition_mv_50ms']):.1f} mV during an odor (as a current: 21).", "note")]
    # left: inhibition during 3-octanol
    x0, pw = 78, 290
    t_max, v_min = 0.6, -24.0
    sx = lambda t: x0 + pw * t / t_max
    sy = lambda v: Y0 + (Y1 - Y0) * min(max(v, v_min), 0.0) / v_min
    out.append(text(x0 - 40, Y0 - 24, "The Kenyon cells' inhibition as 3-octanol begins", "val"))
    for v in range(0, -25, -5):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for t in (0.0, 0.2, 0.4, 0.6):
        out.append(text(sx(t), Y1 + 18, f"{t:g}", "tick", "middle"))
    out.append(text(x0 + pw / 2, Y1 + 36, "s from the odor's onset", "tick", "middle"))
    out.append(f'<text transform="translate({x0 - 42},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">mV, APL working less silenced</text>')
    out.append(f'<rect x="{x0}" y="{sy(-10):.1f}" width="{pw}" height="{sy(-12) - sy(-10):.1f}" fill="{c["ink"]}" fill-opacity="0.08">'
               f'<title>Inada et al. 2017: driving APL directly saturates Kenyon cells 10-12 mV below rest</title></rect>')
    out.append(text(x0 + pw - 4, sy(-10) - 5, "flies' APL saturates (Inada)", "tick", "end"))
    out.append(f'<line x1="{x0}" y1="{sy(-15):.1f}" x2="{x0 + pw}" y2="{sy(-15):.1f}" stroke="{c["ink"]}" stroke-dasharray="2 3"/>')
    out.append(text(x0 + pw - 4, sy(-15) + 14, "the most seen in flies (Vrontou)", "tick", "end"))
    legend = []
    for row, color, dash, width, label in ((ca, "faint", "", 1.6, "calibrated APL, a current"),
                                           (gr, "ink", "6 4", 1.6, "graded APL, a current"),
                                           (ch, "red", "", 2.4, "graded APL, a slow conductance")):
        course = row["3-octanol"]["inhibition_course_mv_50ms"]
        ts = (np.arange(len(course)) + 2.5) * 0.01
        pts = " ".join(f"{sx(t):.1f},{sy(v):.1f}" for t, v in zip(ts, course) if t <= t_max)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c[color]}" stroke-width="{width}"'
                   + (f' stroke-dasharray="{dash}"' if dash else "") + f'><title>{label}: at most {-min(course):.1f} mV</title></polyline>')
        legend.append((color, dash, width, f"{label}: {-min(course):.1f} mV at most"))
    for j, (color, dash, width, label) in enumerate(reversed(legend)):
        lx, ly = x0 + 70, sy(-17.6) + 18 * j
        out.append(f'<line x1="{lx:.1f}" y1="{ly - 4:.1f}" x2="{lx + 20:.1f}" y2="{ly - 4:.1f}" stroke="{c[color]}" stroke-width="{width}"'
                   + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
        out.append(text(lx + 26, ly, label, "valred" if color == "red" else "tick"))
    # middle: Inada et al.'s Fig. 5B on the model
    x1, pw1 = 450, 250
    u_max = 2.5
    mx = lambda t: x1 + pw1 * (t + 0.2) / (u_max + 0.2)
    my = lambda f: Y1 - (Y1 - Y0) * max(min(f, 1.15), -0.1) / 1.15
    out.append(text(x1 - 30, Y0 - 24, "APL driven to its ceiling for 1 s (Inada Fig. 5B)", "val"))
    out.append(f'<rect x="{mx(0):.1f}" y="{Y0}" width="{mx(1.0) - mx(0):.1f}" height="{Y1 - Y0}" fill="{c["ink"]}" fill-opacity="0.05"/>')
    out.append(text((mx(0) + mx(1.0)) / 2, Y0 + 14, "APL driven", "tick", "middle"))
    for f in (0.0, 0.5, 1.0):
        out.append(f'<line x1="{x1}" y1="{my(f):.1f}" x2="{x1 + pw1}" y2="{my(f):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if f == 0 else 0.5}"/>')
        out.append(text(x1 - 8, my(f) + 4, f"{f:g}", "tick", "end"))
    for t in (0, 1, 2):
        out.append(text(mx(t), Y1 + 18, f"{t}", "tick", "middle"))
    out.append(text(x1 + pw1 / 2, Y1 + 36, "s from the drive's start", "tick", "middle"))
    out.append(f'<text transform="translate({x1 - 32},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">share of its plateau</text>')
    d = np.convolve(np.array(inada["course_mv"]) / inada["plateau_mv"], np.ones(5) / 5, mode="same")     # 50 ms means
    ts = (np.arange(len(d)) + 1) * 0.01 - 0.5
    keep = (ts >= -0.2) & (ts <= u_max)
    pts = " ".join(f"{mx(t):.1f},{my(v):.1f}" for t, v in zip(ts[keep], d[keep]))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{c["red"]}" stroke-width="2"><title>the model: plateau '
               f'{abs(inada["plateau_mv"]):.1f} mV below rest</title></polyline>')
    for t, f in FLY_RISE + FLY_FALL:
        out.append(f'<circle cx="{mx(t):.1f}" cy="{my(f):.1f}" r="4.5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6">'
                   f'<title>flies: {f:g} of the plateau at {t:g} s</title></circle>')
    out.append(f'<circle cx="{x1 + 18}" cy="{Y1 + 56}" r="4.5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6"/>')
    out.append(text(x1 + 28, Y1 + 60, "flies (Inada et al. 2017)", "tick"))
    out.append(f'<line x1="{x1 + 150}" y1="{Y1 + 56}" x2="{x1 + 170}" y2="{Y1 + 56}" stroke="{c["red"]}" stroke-width="2"/>')
    out.append(text(x1 + 176, Y1 + 60, "the model", "tick"))
    # right: every conductance tried
    x2, pw2 = 810, 280
    bmin, bmax, rmin, rmax = 1.2, 7.0, 0.3, 1.05
    bx = lambda v: x2 + pw2 * (np.log(v) - np.log(bmin)) / (np.log(bmax) - np.log(bmin))
    ry = lambda v: Y1 - (Y1 - Y0) * (v - rmin) / (rmax - rmin)
    out.append(text(x2 - 40, Y0 - 24, "Every conductance tried", "val"))
    for v in (1.5, 2, 3, 5, 7):
        out.append(f'<line x1="{bx(v):.1f}" y1="{Y0}" x2="{bx(v):.1f}" y2="{Y1}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(text(bx(v), Y1 + 18, f"{v:g}", "tick", "middle"))
    for v in (0.4, 0.6, 0.8, 1.0):
        out.append(f'<line x1="{x2}" y1="{ry(v):.1f}" x2="{x2 + pw2}" y2="{ry(v):.1f}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(text(x2 - 8, ry(v) + 4, f"{v:g}", "tick", "end"))
    out.append(text(x2 + pw2 / 2, Y1 + 36, "silencing APL raises spikes (fold; log)", "tick", "middle"))
    out.append(f'<text transform="translate({x2 - 36},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">APL\'s peak, 4-methylcyclohexanol over 3-octanol</text>')
    out.append(f'<rect x="{bx(2):.1f}" y="{Y0}" width="{bx(3) - bx(2):.1f}" height="{Y1 - Y0}" fill="{c["ink"]}" fill-opacity="0.07">'
               f'<title>flies: silencing APL raises Kenyon cell activity 2-3-fold</title></rect>')
    out.append(text(bx(2.5), Y1 - 8, "flies", "tick", "middle"))
    out.append(f'<line x1="{x2}" y1="{ry(0.49):.1f}" x2="{x2 + pw2}" y2="{ry(0.49):.1f}" stroke="{c["ink"]}" stroke-dasharray="2 3"/>')
    groups = {("1", -20.0): ("ink", 0.85, "11 mV ceiling, -20 mV", (3.6, 0.88)),
              ("1", -15.0): ("faint", 1.0, "11 mV ceiling, -15 mV", (3.9, 0.36)),
              ("2", -20.0): ("muted", 0.8, "pipette reading", (1.25, 0.87))}
    for (strength, rev), (shade, alpha, label, (lbx, lby)) in groups.items():
        rows = sorted((r["drive"], name) for name, r in second["conditions"].items()
                      if r["strength"] == strength and r["reversal_mv"] == rev)
        for drive, name in rows:
            r = second["conditions"][name]
            lo, hi = sorted(r[od]["block_ratio"] for od in ODORS)
            y = r["apl_peak_mch_over_oct"]
            color, width, op = ("red", 3.0, 1.0) if name == ch_name else (shade, 1.6, alpha)
            title = f"{label}, drive {drive:g}: APL ratio {y:.2f}; silencing {lo:.2f}-{hi:.2f}"
            out.append(f'<line x1="{bx(lo):.1f}" y1="{ry(y):.1f}" x2="{bx(hi):.1f}" y2="{ry(y):.1f}" stroke="{c[color]}" stroke-width="{width}"'
                       f' stroke-opacity="{op}" stroke-linecap="round"><title>{title}</title></line>')
            for v in (lo, hi):
                out.append(f'<circle cx="{bx(v):.1f}" cy="{ry(y):.1f}" r="{4 if name == ch_name else 3}" fill="{c[color]}" fill-opacity="{op}"><title>{title}</title></circle>')
        out.append(text(bx(lbx), ry(lby), label, "tick"))
    for row, label in ((gr, "graded current"), (ca, "calibrated current")):
        lo, hi = sorted(row[od]["block_ratio"] for od in ODORS)
        y = row["apl_peak_mch_over_oct"]
        out.append(f'<line x1="{bx(lo):.1f}" y1="{ry(y):.1f}" x2="{bx(hi):.1f}" y2="{ry(y):.1f}" stroke="{c["ink"]}" stroke-width="1.2"/>')
        for v in (lo, hi):
            out.append(f'<circle cx="{bx(v):.1f}" cy="{ry(y):.1f}" r="3.5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.4"><title>{label}</title></circle>')
    lo, hi = sorted(ch[od]["block_ratio"] for od in ODORS)
    out.append(text(bx(hi) + 8, ry(ch["apl_peak_mch_over_oct"]) - 6, "chosen", "valred"))
    out.append(text(x2, H - 22, "Rings: the two currents, for comparison.", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .valred {{ font-size: 11px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = "APL's inhibition of the Kenyon cells as a slow conductance, against flies' limits and time course"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    first = json.loads((ROOT / "experiments" / "odor_apl_conductance_check.json").read_text())
    second = json.loads((ROOT / "experiments" / "odor_apl_conductance2_check.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"apl_conductance-{theme}.svg"
        path_.write_text(figure(theme, first, second))
        print(path_)


if __name__ == "__main__":
    main()
