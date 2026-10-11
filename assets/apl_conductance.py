"""APL as a conductance (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/apl_conductance.py      # writes assets/apl_conductance-light.svg and assets/apl_conductance-dark.svg

experiments/odor_apl_conductance_check.py, DoOR's input. Left: how far APL holds the Kenyon cells down during 3-octanol,
their mean free membrane potential with APL working less silenced (50 ms means, from the odor's onset): the calibrated APL
(grey; mb_calibration.py, a current, saturating), the graded APL as a current (dashed; mb_calibration2.py) and as a
conductance reversing 20 mV below rest (red; mb_calibration3.py), against the 10-12 mV at which flies' APL saturates
however hard it is driven (shaded; Inada et al. 2017) and the 15 mV that is the most Kenyon cells have been seen inhibited
through it (line; Vrontou et al. 2021). Right: every condition tried, APL's 4-methylcyclohexanol/3-octanol peak ratio
against the rise silencing APL gives the Kenyon cells' spikes, each a segment from one odor's rise to the other's; flies'
2-3-fold rise (shaded) and APL's 0.49 (Prisco et al. 2021; line).
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
W, H = 1120, 540
Y0, Y1 = 128, 430
CHOSEN = "reversal -20, effect 2.22, drive 1.5"
CALIBRATED = "mb_calibration.py (fast current), drive 10, effect 1"
GRADED = "mb_calibration2.py (fast current), drive 1.5, effect 2.5"
ODORS = ("3-octanol", "4-methylcyclohexanol")


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    rows = d["conditions"]
    ch, gr, ca = rows[CHOSEN], rows[GRADED], rows[CALIBRATED]
    out = [text(24, 30, "APL as a conductance: graded like flies', and never holding the Kenyon cells past flies' limit", "lab"),
           text(24, 50, "As a current, APL graded like flies' takes the Kenyon cells 21 mV down as an odor begins; as a conductance reversing "
                "20 mV below rest it divides a responding cell's input", "note"),
           text(24, 68, f"more than it pulls a quiet one down: {abs(ch['3-octanol']['largest_inhibition_mv_50ms']):.1f} mV at most, "
                f"with flies' graded response ({ch['apl_peak_mch_over_oct']:.2f}; flies 0.49) and silencing effect "
                f"({ch['3-octanol']['block_ratio']:.2f} and {ch['4-methylcyclohexanol']['block_ratio']:.2f}-fold; flies 2-3).", "note")]
    # left: the inhibition's time course during 3-octanol
    x0, pw = 90, 440
    t_max, v_min = 0.6, -24.0
    sx = lambda t: x0 + pw * t / t_max
    sy = lambda v: Y0 + (Y1 - Y0) * min(max(v, v_min), 0.0) / v_min
    out.append(text(x0, Y0 - 22, "The Kenyon cells' inhibition as 3-octanol begins", "val"))
    for v in range(0, -25, -5):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for t in (0.0, 0.2, 0.4, 0.6):
        out.append(text(sx(t), Y1 + 18, f"{t:g}", "tick", "middle"))
    out.append(text(x0 + pw / 2, Y1 + 38, "time from the odor's onset (s)", "tick", "middle"))
    out.append(f'<text transform="translate({x0 - 48},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">mV from where they sit with APL silenced</text>')
    out.append(f'<rect x="{x0}" y="{sy(-10):.1f}" width="{pw}" height="{sy(-12) - sy(-10):.1f}" fill="{c["ink"]}" fill-opacity="0.08">'
               f'<title>Inada et al. 2017: driving APL directly saturates Kenyon cells 10-12 mV below rest</title></rect>')
    out.append(text(x0 + pw - 4, sy(-10) - 5, "flies' APL saturates here (Inada et al.)", "tick", "end"))
    out.append(f'<line x1="{x0}" y1="{sy(-15):.1f}" x2="{x0 + pw}" y2="{sy(-15):.1f}" stroke="{c["ink"]}" stroke-dasharray="2 3"/>')
    out.append(text(x0 + pw - 4, sy(-15) + 14, "the most seen in flies (Vrontou et al.)", "tick", "end"))
    legend = []
    for row, color, dash, width, label in ((ca, "faint", "", 1.6, "calibrated APL (a current)"),
                                           (gr, "ink", "6 4", 1.6, "graded APL as a current"),
                                           (ch, "red", "", 2.4, "graded APL as a conductance")):
        course = row["3-octanol"]["inhibition_course_mv_50ms"]
        ts = (np.arange(len(course)) + 2.5) * 0.01
        pts = " ".join(f"{sx(t):.1f},{sy(v):.1f}" for t, v in zip(ts, course) if t <= t_max)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c[color]}" stroke-width="{width}"'
                   + (f' stroke-dasharray="{dash}"' if dash else "") + f'><title>{label}: at most {min(course):.1f} mV</title></polyline>')
        legend.append((color, dash, width, f"{label}: at most {-min(course):.1f} mV"))
    for j, (color, dash, width, label) in enumerate(reversed(legend)):     # in the empty lower right
        lx, ly = sx(0.21), sy(-18.0) + 20 * j
        out.append(f'<line x1="{lx:.1f}" y1="{ly - 4:.1f}" x2="{lx + 22:.1f}" y2="{ly - 4:.1f}" stroke="{c[color]}" stroke-width="{width}"'
                   + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
        out.append(text(lx + 30, ly, label, "valred" if color == "red" else "tick"))
    # right: the grid
    x1, pw2 = 640, 420
    bmin, bmax, rmin, rmax = 1.5, 12.0, 0.3, 1.05
    bx = lambda v: x1 + pw2 * (np.log(v) - np.log(bmin)) / (np.log(bmax) - np.log(bmin))
    ry = lambda v: Y1 - (Y1 - Y0) * (v - rmin) / (rmax - rmin)
    out.append(text(x1, Y0 - 22, "Every APL tried: graded response against silencing effect", "val"))
    for v in (2, 3, 4, 6, 8, 12):
        out.append(f'<line x1="{bx(v):.1f}" y1="{Y0}" x2="{bx(v):.1f}" y2="{Y1}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(text(bx(v), Y1 + 18, f"{v:g}", "tick", "middle"))
    for v in (0.4, 0.6, 0.8, 1.0):
        out.append(f'<line x1="{x1}" y1="{ry(v):.1f}" x2="{x1 + pw2}" y2="{ry(v):.1f}" stroke="{c["rule"]}" stroke-opacity="0.5"/>')
        out.append(text(x1 - 8, ry(v) + 4, f"{v:g}", "tick", "end"))
    out.append(text(x1 + pw2 / 2, Y1 + 38, "how much silencing APL raises the Kenyon cells' spikes (fold; log)", "tick", "middle"))
    out.append(f'<text transform="translate({x1 - 44},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">APL\'s peak, 4-methylcyclohexanol over 3-octanol</text>')
    out.append(f'<rect x="{bx(2):.1f}" y="{Y0}" width="{bx(3) - bx(2):.1f}" height="{Y1 - Y0}" fill="{c["ink"]}" fill-opacity="0.07">'
               f'<title>flies: silencing APL raises Kenyon cell activity 2-3-fold (Lin et al. 2014, Bergmann et al. 2026)</title></rect>')
    out.append(f'<line x1="{x1}" y1="{ry(0.49):.1f}" x2="{x1 + pw2}" y2="{ry(0.49):.1f}" stroke="{c["ink"]}" stroke-dasharray="2 3"/>')
    out.append(text(x1 + pw2 - 4, ry(0.49) + 14, "flies' APL: 0.49 (Prisco et al.)", "tick", "end"))
    out.append(text(bx(2.5), Y1 - 8, "flies", "tick", "middle"))
    shades = {-15.0: ("faint", 1.0), -20.0: ("muted", 1.0), -30.0: ("ink", 0.55)}
    for e, (shade, alpha) in shades.items():                # each reversal's drives, 1 to 10, as a path
        mine = sorted((row["drive"], name) for name, row in rows.items() if row.get("reversal_mv") == e)
        centres = []
        for drive, name in mine:
            row = rows[name]
            lo, hi = sorted(row[od]["block_ratio"] for od in ODORS)
            y = row["apl_peak_mch_over_oct"]
            centres.append((float(np.sqrt(lo * hi)), y))
            title = (f"reversal {e:g} mV, drive {drive:g}: APL ratio {y:.2f}; silencing {row['3-octanol']['block_ratio']:.2f} "
                     f"(3-octanol), {row['4-methylcyclohexanol']['block_ratio']:.2f} (4-methylcyclohexanol); at most "
                     f"{abs(row['3-octanol']['largest_inhibition_mv_50ms']):.1f} mV down")
            color, width = ("red", 3.2) if name == CHOSEN else (shade, 1.6)
            op = 1.0 if name == CHOSEN else alpha
            out.append(f'<line x1="{bx(lo):.1f}" y1="{ry(y):.1f}" x2="{bx(hi):.1f}" y2="{ry(y):.1f}" stroke="{c[color]}" stroke-width="{width}"'
                       f' stroke-opacity="{op}" stroke-linecap="round"><title>{title}</title></line>')
            for v in (lo, hi):
                out.append(f'<circle cx="{bx(v):.1f}" cy="{ry(y):.1f}" r="{4 if name == CHOSEN else 3}" fill="{c[color]}" fill-opacity="{op}"><title>{title}</title></circle>')
        pts = " ".join(f"{bx(x):.1f},{ry(y):.1f}" for x, y in centres)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c[shade]}" stroke-opacity="{alpha * 0.6}" stroke-width="1" stroke-dasharray="1 3"/>')
        x, y = centres[-1]
        label_x = min(bx(x) + 10, x1 + pw2 - 4)
        out.append(text(label_x, ry(y) - 8, f"{e:g} mV", "tick", "end" if label_x >= x1 + pw2 - 4 else "start"))
    for row, label, dy in ((gr, "graded current", None), (ca, "calibrated (saturates)", 4)):
        lo, hi = sorted(row[od]["block_ratio"] for od in ODORS)
        y = row["apl_peak_mch_over_oct"]
        out.append(f'<line x1="{bx(lo):.1f}" y1="{ry(y):.1f}" x2="{bx(hi):.1f}" y2="{ry(y):.1f}" stroke="{c["ink"]}" stroke-width="1.6"/>')
        for v in (lo, hi):
            out.append(f'<circle cx="{bx(v):.1f}" cy="{ry(y):.1f}" r="3.5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.5">'
                       f'<title>{label}: APL ratio {y:.2f}; silencing {lo:.2f}-{hi:.2f}</title></circle>')
        if dy is None:                                       # up and left, with a leader, clear of the crowded segments
            out.append(f'<line x1="{bx(1.72):.1f}" y1="{ry(0.573):.1f}" x2="{bx(lo) - 4:.1f}" y2="{ry(y) - 3:.1f}" stroke="{c["muted"]}" stroke-width="0.8"/>')
            out.append(text(bx(1.55), ry(0.58), label, "tick"))
        else:
            out.append(text(bx(hi) + 8, ry(y) + dy, label, "tick"))
    out.append(text(bx(ch["3-octanol"]["block_ratio"]) + 10, ry(ch["apl_peak_mch_over_oct"]) + 18, "chosen: -20 mV, drive 1.5", "valred"))
    out.append(text(x1, H - 24, "Filled: conductances, by reversal (dotted: drive rising 1 to 10); rings: currents.", "tick"))
    out.append(text(x1, H - 10, "Each segment spans the two odors' silencing effects.", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .valred {{ font-size: 12px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = "APL's inhibition of the Kenyon cells as a current and as a conductance, against flies' limits"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "odor_apl_conductance_check.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"apl_conductance-{theme}.svg"
        path_.write_text(figure(theme, d))
        print(path_)


if __name__ == "__main__":
    main()
