"""Rung 9's crux: the two odors' Kenyon cell sets, and the learning marks they give, drawn from saved results (nothing by
hand).

    python assets/kc_sets.py      # writes assets/kc_sets-light.svg and assets/kc_sets-dark.svg

Left: experiments/kc_setc_check.py, the Kenyon cells answering 3-octanol only, both odors and 4-methylcyclohexanol only, per
100 answering 3-octanol, with the model's Kenyon cells as they are (set A) and integrating longer with depressing synapses
(set C), against flies (Hige et al. 2015: 49 and 53 cells answering, sharing 30-33% of their responders; research_notes/
Rung 9 learning data/hige2015_specificity.md). Right: rung 9's four marks (rung9_learning.py) in learning_pilot12.py (set
A) and learning_pilot13.py (set C), each odor's spikes' drop against the band the test asks for and flies' value: PAIRED,
3-octanol paired, its own drop (and the gap to 4-methylcyclohexanol's, 30 points required); UNPAIRED, 3-octanol paired,
4-methylcyclohexanol's; RECIPROCAL, 4-methylcyclohexanol paired, 3-octanol's; BACKWARD, the larger change in the paired
odor's charge with dopamine first.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/looming.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 470
OCT, MCH = "3-octanol", "4-methylcyclohexanol"
FLIES_SETS = (49, 53, 15.5)                     # answering 3-octanol and 4-methylcyclohexanol (Hige et al. 2015), both at 30-33%


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def sets(row: dict) -> tuple:
    n_oct, n_mch = row[OCT]["kcs_answering"], row[MCH]["kcs_answering"]
    both = row["share_answering_both"][OCT] * n_oct
    return n_oct, n_mch, both


def figure(theme: str, check: dict, lp12: dict, lp13: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "Rung 9's crux: 4-methylcyclohexanol's Kenyon cells sit inside 3-octanol's", "lab"),
           text(24, 50, "Flies' two odors reach separate sets of about the same size, sharing about a third each way. The model's "
                "4-methylcyclohexanol reaches a small set, mostly inside", "note"),
           text(24, 68, "3-octanol's. Kenyon cells that integrate longer (set C) widen it toward 3-octanol's, and the reciprocal mark "
                "passes, but pairing 3-octanol then cuts 4-methylcyclohexanol too.", "note")]
    # left: the sets, per 100 cells answering 3-octanol
    x0, y0, bw, gap = 80, 130, 380, 78
    rows = [("flies (Hige et al. 2015)", FLIES_SETS), ("model, Kenyon cells as now (set A)", sets(check["conditions"]["A"])),
            ("model, integrating longer (set C)", sets(check["conditions"]["C"]))]
    out.append(text(x0, y0 - 18, "Kenyon cells answering, per 100 answering 3-octanol", "val"))
    scale = bw / 200.0
    for k, (label, (n_oct, n_mch, both)) in enumerate(rows):
        y = y0 + 22 + k * gap
        f = 100.0 / n_oct
        o_only, b_, m_only = (n_oct - both) * f, both * f, (n_mch - both) * f
        out.append(text(x0, y - 8, label, "tick"))
        xa = x0
        for width, fill, opacity, title in ((o_only, c["ink"], 0.85, f"3-octanol only: {o_only:.0f}"),
                                            (b_, c["red"], 1.0, f"both: {b_:.0f} ({100 * both / n_mch:.0f}% of 4-methylcyclohexanol's)"),
                                            (m_only, c["faint"], 1.0, f"4-methylcyclohexanol only: {m_only:.0f}")):
            out.append(f'<rect x="{xa:.1f}" y="{y}" width="{max(width * scale, 0.5):.1f}" height="22" fill="{fill}" fill-opacity="{opacity}"><title>{title}</title></rect>')
            xa += width * scale + 2
        share = ("30-33% of each odor's cells answer the other" if k == 0 else
                 f"{100 * both / n_mch:.0f}% of 4-methylcyclohexanol's cells answer 3-octanol, {100 * both / n_oct:.0f}% of 3-octanol's the other")
        out.append(text(x0, y + 36, share, "tiny"))
    ly = y0 + 22 + 3 * gap - 6
    for k, (fill, opacity, label) in enumerate(((c["ink"], 0.85, "3-octanol only"), (c["red"], 1.0, "both"), (c["faint"], 1.0, "4-methylcyclohexanol only"))):
        x = x0 + 150 * k
        out.append(f'<rect x="{x}" y="{ly - 10}" width="14" height="12" fill="{fill}" fill-opacity="{opacity}"/>')
        out.append(text(x + 20, ly, label, "tick"))
    # right: the marks
    x1, pw, y1, ph = 640, 440, 130, 250
    marks = [("PAIRED", "3-octanol's own", (0.65, 1.0), 0.80), ("UNPAIRED", "4-methylcyclohexanol's", (0.10, 0.45), 0.27),
             ("RECIPROCAL", "3-octanol's", (0.15, 0.50), 0.38), ("BACKWARD", "change, dopamine first", (0.0, 0.15), None)]
    ty = lambda v: y1 + ph - ph * v
    out.append(text(x1, y1 - 18, "rung 9's marks: the spikes' drop", "val"))
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        out.append(f'<line x1="{x1}" y1="{ty(v):.1f}" x2="{x1 + pw}" y2="{ty(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.45}"/>')
        out.append(text(x1 - 6, ty(v) + 4, f"{100 * v:.0f}%", "tick", "end"))
    col = pw / len(marks)
    values = {}
    for name, d in (("A", lp12), ("C", lp13)):
        m = d["marks"]
        values[name] = [m["PAIRED"]["oct_spikes_drop"], m["UNPAIRED"]["mch_spikes_drop"], m["RECIPROCAL"]["oct_spikes_drop"],
                        max(abs(m["BACKWARD"]["oct_paired_charge_change"]), abs(m["BACKWARD"]["mch_paired_charge_change"]))]
        values[name + " pass"] = [m[k]["pass"] for k in ("PAIRED", "UNPAIRED", "RECIPROCAL", "BACKWARD")]
    for i, (name, what, (lo, hi), fly) in enumerate(marks):
        cx = x1 + col * (i + 0.5)
        out.append(f'<rect x="{cx - col * 0.36:.1f}" y="{ty(hi):.1f}" width="{col * 0.72:.1f}" height="{ty(lo) - ty(hi):.1f}" fill="{c["ink"]}" fill-opacity="0.07">'
                   f'<title>{name}: the band rung 9 asks for, {100 * lo:.0f}-{100 * hi:.0f}%</title></rect>')
        if fly is not None:
            out.append(f'<line x1="{cx - col * 0.36:.1f}" y1="{ty(fly):.1f}" x2="{cx + col * 0.36:.1f}" y2="{ty(fly):.1f}" stroke="{c["ink"]}" stroke-dasharray="3 3"><title>flies {100 * fly:.0f}%</title></line>')
        for k, (set_name, color) in enumerate((("A", "faint"), ("C", "red"))):
            v = values[set_name][i]
            bx = cx - col * 0.22 + k * col * 0.24
            out.append(f'<rect x="{bx:.1f}" y="{ty(v):.1f}" width="{col * 0.2:.1f}" height="{ty(0) - ty(v):.1f}" fill="{c[color]}">'
                       f'<title>set {set_name}: {100 * v:.1f}% ({"passes" if values[set_name + " pass"][i] else "fails"})</title></rect>')
            out.append(text(bx + col * 0.1, ty(v) - 5, "✓" if values[set_name + " pass"][i] else "✗", "tiny", "middle"))
        out.append(text(cx, y1 + ph + 16, name, "tick", "middle"))
        out.append(text(cx, y1 + ph + 30, what, "tiny", "middle"))
    lx, ly2 = x1, y1 + ph + 54
    out.append(f'<rect x="{lx}" y="{ly2 - 10}" width="14" height="12" fill="{c["faint"]}"/>')
    out.append(text(lx + 20, ly2, "set A (learning pilot 12)", "tick"))
    out.append(f'<rect x="{lx + 170}" y="{ly2 - 10}" width="14" height="12" fill="{c["red"]}"/>')
    out.append(text(lx + 190, ly2, "set C (learning pilot 13)", "tick"))
    out.append(f'<line x1="{lx + 340}" y1="{ly2 - 4}" x2="{lx + 360}" y2="{ly2 - 4}" stroke="{c["ink"]}" stroke-dasharray="3 3"/>')
    out.append(text(lx + 366, ly2, "flies", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = "4-methylcyclohexanol's Kenyon cells sit mostly inside 3-octanol's in the model, unlike flies', and rung 9's marks follow"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    load = lambda name: json.loads((ROOT / "experiments" / f"{name}.json").read_text())
    check, lp12, lp13 = load("kc_setc_check"), load("learning_pilot12"), load("learning_pilot13")
    for theme in THEMES:
        path_ = OUT / f"kc_sets-{theme}.svg"
        path_.write_text(figure(theme, check, lp12, lp13))
        print(path_)


if __name__ == "__main__":
    main()
