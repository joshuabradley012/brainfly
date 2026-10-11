"""MBON11's Kenyon cell input budget in the corrected model against flies', drawn from saved results (nothing by hand).

    python assets/mbon11_budget.py      # writes assets/mbon11_budget-light.svg and assets/mbon11_budget-dark.svg

Left: experiments/mbon11_budget_check.json, the synapse-spikes the Kenyon cells give MBON11_R in 0-1.4 s, by class, for
3-octanol and 4-methylcyclohexanol (every above-rest spike, Hige et al.'s window), against flies' budget on the same
synapse counts (research_notes/Rung 9 learning data/mbon11_kc_activity.md section 3.7: gamma-main and gamma-s 3.5% x 3.5
spikes, alpha/beta s, m, c 6% x 2.5, alpha'/beta' 20% x 5; total range 1,300-7,500; estimated at Hige's stimulus, where
flies answer the two odors about equally). Right: what that activity carries onto MBON11_R at the model's 0.054 pC per
synapse, before and after the synapses' depression (0.5 per spike, recovering over 1.5 s; the same spikes at 10 ms),
against flies' odor charge (Hige et al. 2015: about 245-250 pC for 3-octanol, 230-273 for 4-methylcyclohexanol).
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
CLASSES = ("gamma-main and gamma-s", "alpha/beta s, m, c", "alpha'/beta'")
LABELS = {"gamma-main and gamma-s": "γ", "alpha/beta s, m, c": "α/β", "alpha'/beta'": "α′/β′"}
SHADES = {"gamma-main and gamma-s": ("ink", 0.85), "alpha/beta s, m, c": ("red", 1.0), "alpha'/beta'": ("faint", 1.0)}
FLIES_CHARGE = {"3-octanol": (245, 250), "4-methylcyclohexanol": (230, 273)}
Q_PC = 0.054


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    oct_ = d["odors"]["3-octanol"]
    out = [text(24, 30, "MBON11's input: flies' Kenyon cell activity, half flies' charge", "lab"),
           text(24, 50, f"With the corrected input the Kenyon cells give MBON11 about flies' budget of synapse-spikes to 3-octanol "
                f"({oct_['synapse_spikes_all']:,.0f}; flies about 3,200), worth flies' charge undepressed.", "note"),
           text(24, 68, "The synapses' depression leaves half of it. To 4-methylcyclohexanol the activity itself is a seventh of "
                "flies'.", "note")]
    # left: synapse-spikes by class
    x0, y0, pw, ph = 80, 120, 470, 260
    vmax = 8000.0
    ty = lambda v: y0 + ph - ph * min(v, vmax) / vmax
    out.append(text(x0, y0 - 14, "Synapse-spikes onto MBON11_R, 0-1.4 s", "val"))
    for v in (0, 2000, 4000, 6000, 8000):
        out.append(f'<line x1="{x0}" y1="{ty(v):.1f}" x2="{x0 + pw}" y2="{ty(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.45}"/>')
        out.append(text(x0 - 6, ty(v) + 4, f"{v:,}", "tick", "end"))
    flies = {cl: d["classes"][cl]["synapses_onto_mbon11_r"] * a * s for cl, (a, s) in d["flies"].items() if cl in CLASSES}
    cols = [("3-octanol", "model", {cl: d["odors"]["3-octanol"]["classes"][cl]["synapse_spikes_all"] for cl in CLASSES}),
            ("3-octanol", "flies", flies),
            ("4-methylcyclohexanol", "model", {cl: d["odors"]["4-methylcyclohexanol"]["classes"][cl]["synapse_spikes_all"] for cl in CLASSES}),
            ("4-methylcyclohexanol", "flies", flies)]
    bw = 62
    for i, (odor, who, vals) in enumerate(cols):
        bx = x0 + 40 + i * 105 + (20 if i >= 2 else 0)
        base = 0.0
        for cl in CLASSES:
            v = vals[cl]
            color, op = SHADES[cl]
            out.append(f'<rect x="{bx}" y="{ty(base + v):.1f}" width="{bw}" height="{ty(base) - ty(base + v):.1f}" fill="{c[color]}" fill-opacity="{op}">'
                       f'<title>{odor}, {who}, {LABELS[cl]}: {v:,.0f}</title></rect>')
            base += v
        if who == "flies":
            lo, hi = 1300, 7500
            rx = bx + bw + 9
            out.append(f'<line x1="{rx:.1f}" y1="{ty(lo):.1f}" x2="{rx:.1f}" y2="{ty(hi):.1f}" stroke="{c["ink"]}" stroke-width="1.5">'
                       f'<title>the range for flies, 1,300-7,500</title></line>')
            for y in (lo, hi):
                out.append(f'<line x1="{rx - 5:.1f}" y1="{ty(y):.1f}" x2="{rx + 5:.1f}" y2="{ty(y):.1f}" stroke="{c["ink"]}" stroke-width="1.5"/>')
        out.append(text(bx + bw / 2, ty(base) - 6, f"{base:,.0f}", "tick", "middle"))
        out.append(text(bx + bw / 2, y0 + ph + 16, who, "tick", "middle"))
    out.append(text(x0 + 40 + 105 - 20 + bw / 2, y0 + ph + 32, "3-octanol", "tiny", "middle"))
    out.append(text(x0 + 40 + 3 * 105 + bw / 2 - 30, y0 + ph + 32, "4-methylcyclohexanol (flies: as for 3-octanol)", "tiny", "middle"))
    ly = y0 + ph + 56
    for k, cl in enumerate(CLASSES):
        color, op = SHADES[cl]
        x = x0 + 90 * k
        out.append(f'<rect x="{x}" y="{ly - 10}" width="14" height="12" fill="{c[color]}" fill-opacity="{op}"/>')
        out.append(text(x + 20, ly, LABELS[cl], "tick"))
    out.append(text(x0 + 270, ly, "bar: flies' range", "tick"))
    # right: the charge
    x1, pw2 = 700, 380
    cmax = 300.0
    ty2 = lambda v: y0 + ph - ph * min(v, cmax) / cmax
    out.append(text(x1, y0 - 14, "What it carries onto MBON11_R (pC)", "val"))
    for v in (0, 100, 200, 300):
        out.append(f'<line x1="{x1}" y1="{ty2(v):.1f}" x2="{x1 + pw2}" y2="{ty2(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.45}"/>')
        out.append(text(x1 - 6, ty2(v) + 4, f"{v}", "tick", "end"))
    for g, odor in enumerate(("3-octanol", "4-methylcyclohexanol")):
        r = d["odors"][odor]
        und, dep = r["charge_pc_at_q_undepressed"], r["timed"]["charge_pc_depressed"]
        gx = x1 + 30 + g * 180
        lo, hi = FLIES_CHARGE[odor]
        out.append(f'<rect x="{gx - 10}" y="{ty2(hi):.1f}" width="150" height="{max(ty2(lo) - ty2(hi), 2):.1f}" fill="{c["ink"]}" fill-opacity="0.12">'
                   f'<title>flies {lo}-{hi} pC</title></rect>')
        for k, (v, label, color, op) in enumerate(((und, "undepressed", "ink", 0.85), (dep, "after depression", "red", 1.0))):
            bx = gx + 8 + k * 64
            out.append(f'<rect x="{bx}" y="{ty2(v):.1f}" width="50" height="{ty2(0) - ty2(v):.1f}" fill="{c[color]}" fill-opacity="{op}">'
                       f'<title>{odor}, {label}: {v:.0f} pC</title></rect>')
            if v > 60:                                  # inside a tall bar, clear of flies' band above it
                out.append(f'<text x="{bx + 25:.1f}" y="{ty2(v) + 16:.1f}" class="tick" text-anchor="middle" style="fill: {c["paper"]}">{v:.0f}</text>')
            else:
                out.append(text(bx + 25, ty2(v) - 6, f"{v:.0f}", "tick", "middle"))
        out.append(text(gx + 65, y0 + ph + 16, odor, "tiny", "middle"))
    ly2 = y0 + ph + 56
    out.append(f'<rect x="{x1}" y="{ly2 - 10}" width="14" height="12" fill="{c["ink"]}" fill-opacity="0.85"/>')
    out.append(text(x1 + 20, ly2, "undepressed", "tick"))
    out.append(f'<rect x="{x1 + 115}" y="{ly2 - 10}" width="14" height="12" fill="{c["red"]}"/>')
    out.append(text(x1 + 135, ly2, "after depression", "tick"))
    out.append(f'<rect x="{x1 + 255}" y="{ly2 - 10}" width="14" height="12" fill="{c["ink"]}" fill-opacity="0.12"/>')
    out.append(text(x1 + 275, ly2, "flies", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = "MBON11 gets flies' budget of Kenyon cell synapse-spikes to 3-octanol but half flies' charge after the synapses' depression; to 4-methylcyclohexanol a seventh of the activity"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "mbon11_budget_check.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"mbon11_budget-{theme}.svg"
        path_.write_text(figure(theme, d))
        print(path_)


if __name__ == "__main__":
    main()
