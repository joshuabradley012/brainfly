"""Where 4-methylcyclohexanol falls behind (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/al_inputs.py      # writes assets/al_inputs-light.svg and assets/al_inputs-dark.svg

Left and middle: each glomerulus's projection neurons for 3-octanol and for 4-methylcyclohexanol, flies' (Badel et al.
2016, mean dF/F over the 37 glomeruli their NP225 imaging covers; research_notes/Rung 9 learning data/oct_mch_input.md
section 8) against the model's (experiments/odor_probe55.py: evoked spikes/s over the odor's first 0.5 s, with the
receptor input the receptor-level evidence supports at Hige et al.'s concentration, receptor_fills.RECOMMENDED). Filled:
glomeruli that input drives at 0.05 or more (10 spikes/s); rings: less or none. Right: the APL sweep
(experiments/odor_apl_range_check.py): for each APL gain and Kenyon cell synapse scale, how much silencing APL raises
the Kenyon cells' spikes (the block effect, mean of the two odors) against how much APL raises 4-methylcyclohexanol's
share of answering Kenyon cells (the ratio with APL working over silenced); flies: block effect 2-3 and 0.95 over 0.76
(Prisco et al. 2021).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import receptor_fills  # noqa: E402

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/al_transform.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 500
Y0, Y1 = 120, 400
BADEL = {  # Badel et al. 2016 Table S2, mean dF/F (%), as oct_mch_input.md section 8 tabulates it
    "glomeruli": ("DM6", "DM3", "VM2", "DL3", "D", "DA2", "VM3", "DA1", "DA3", "VM7v", "DM2", "DC3", "DC2", "DM5", "VM4",
                  "DL5", "VM1", "VC1", "VA2", "DL1", "DL4", "VM7d", "VA6", "VA7m", "VA4", "VA5", "VA3", "DA4l", "DM4",
                  "VC2", "VA7l", "DP1m", "DM1", "VA1d", "VL2a", "VL2p", "VA1v"),
    "3-octanol": (278, 219, 171, 166, 146, 140, 122, 118, 113, 106, 97, 86, 74, 53, 48, 38, 36, 36, 32, 27, 26, 26, 25,
                  25, 21, 19, 18, 15, 12, 12, 12, 10, 9, 7, -1, -10, -33),
    "4-methylcyclohexanol": (88, 87, 34, 91, 172, 236, 72, 78, 116, 121, 42, 101, 20, 43, 10, 77, 24, 51, 19, 37, 97, 84,
                             69, 16, 21, 110, 108, 96, 23, 40, 26, 15, 14, 50, -1, -3, 17),
}
DRIVEN = 0.05
LABEL_HZ, LABEL_FLY, GAP, LABEL_AT_HZ = 35.0, 85.0, 30.0, 50.0
FLY_BLOCK, FLY_EQUAL = (2.0, 3.0), 0.95 / 0.76


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def scatter_panel(c, x0, pw, odor: str, model: dict) -> list[str]:
    xmax, ymax = 300.0, 160.0
    sx = lambda v: x0 + pw * min(max(v, 0.0), xmax) / xmax
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), ymax) / ymax
    out = [text(x0, Y0 - 12, f"{odor}: projection neurons by glomerulus", "val")]
    for v in (0, 40, 80, 120, 160):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for v in (0, 100, 200, 300):
        out.append(text(sx(v), Y1 + 16, f"{v}", "tick", "middle"))
    out.append(text(x0 + pw / 2, Y1 + 34, "flies' response (dF/F, %; Badel et al.)", "tick", "middle"))
    out.append(f'<text transform="translate({x0 - 34},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">model (spikes/s)</text>')
    drive = receptor_fills.RECOMMENDED[odor]
    rings, dots, quiet = [], [], []
    for g, fly in zip(BADEL["glomeruli"], BADEL[odor]):
        m = model.get(g)
        if m is None:
            continue
        driven = drive.get(g, 0.0) >= DRIVEN
        tip = f"<title>{g}: flies {fly}%, model {m:.0f} spikes/s; receptor input {drive.get(g, 0.0):.2f}</title>"
        if driven:
            dots.append(f'<circle cx="{sx(fly):.1f}" cy="{sy(m):.1f}" r="5" fill="{c["red"]}" stroke="{c["paper"]}" stroke-width="2">{tip}</circle>')
            if m >= LABEL_HZ:
                out.append(text(sx(fly), sy(m) - 9, g, "tick", "middle"))
        else:
            rings.append(f'<circle cx="{sx(fly):.1f}" cy="{sy(m):.1f}" r="4.5" fill="none" stroke="{c["ink"]}" stroke-width="1.6">{tip}</circle>')
            if fly >= LABEL_FLY and m < LABEL_HZ:
                quiet.append((fly, g))
    quiet.sort()
    groups = []
    for fly, g in quiet:                     # the strong flies' responses the model leaves at rest, bracketed in runs
        if groups and fly - groups[-1][-1][0] <= GAP:
            groups[-1].append((fly, g))
        else:
            groups.append([(fly, g)])
    for grp in groups:
        lo, hi = sx(grp[0][0]), sx(grp[-1][0])
        mid, y = (lo + hi) / 2, sy(0) - 10
        if hi - lo > 1:
            out.append(f'<path d="M{lo:.1f} {y + 5:.1f} L{lo:.1f} {y:.1f} L{hi:.1f} {y:.1f} L{hi:.1f} {y + 5:.1f}" fill="none" stroke="{c["muted"]}" stroke-width="1"/>')
        out.append(f'<line x1="{mid:.1f}" y1="{y:.1f}" x2="{mid:.1f}" y2="{sy(LABEL_AT_HZ):.1f}" stroke="{c["muted"]}" stroke-width="1"/>')
        names = [g for _, g in grp]
        lines = [", ".join(names[i:i + 4]) for i in range(0, len(names), 4)]
        for j, line in enumerate(reversed(lines)):
            out.append(text(mid, sy(LABEL_AT_HZ) - 5 - 13 * j, line, "tick", "middle"))
    return out + rings + dots


def apl_panel(c, x0, pw, apl: dict) -> list[str]:
    xlo, xhi, ylo, yhi = 1.0, 3.2, 0.6, 1.4
    sx = lambda v: x0 + pw * (min(max(v, xlo), xhi) - xlo) / (xhi - xlo)
    sy = lambda v: Y1 - (Y1 - Y0) * (min(max(v, ylo), yhi) - ylo) / (yhi - ylo)
    out = [text(x0, Y0 - 12, "APL: blocking like flies' leaves no equalizing", "val")]
    for v in (0.6, 0.8, 1.0, 1.2, 1.4):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 1.0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v:g}", "tick", "end"))
    for v in (1.0, 1.5, 2.0, 2.5, 3.0):
        out.append(text(sx(v), Y1 + 16, f"{v:g}", "tick", "middle"))
    out.append(text(x0 + pw / 2, Y1 + 34, "block effect: KC spikes, APL silenced / working", "tick", "middle"))
    out.append(f'<text transform="translate({x0 - 34},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">MCH share of KCs, APL on / off</text>')
    out.append(f'<rect x="{sx(FLY_BLOCK[0]):.1f}" y="{sy(FLY_EQUAL + 0.05):.1f}" width="{sx(FLY_BLOCK[1]) - sx(FLY_BLOCK[0]):.1f}" '
               f'height="{sy(FLY_EQUAL - 0.05) - sy(FLY_EQUAL + 0.05):.1f}" fill="{c["ink"]}" fill-opacity="0.15">'
               f'<title>flies: block effect 2-3, claws answering 0.76 to 0.95 with APL (Prisco et al. 2021)</title></rect>')
    out.append(text(sx(FLY_BLOCK[1]) - 4, sy(FLY_EQUAL + 0.05) - 6, "flies", "tick", "end"))
    for name, r in apl["conditions"].items():
        block = sum(r["block_ratio"].values()) / len(r["block_ratio"])
        eq = r["kc_answering_ratio_on"] / r["kc_answering_ratio_off"]
        chosen = name == apl.get("chosen")
        out.append(f'<circle cx="{sx(block):.1f}" cy="{sy(eq):.1f}" r="{6 if chosen else 4.5}" fill="{c["red"]}" '
                   f'stroke="{c["paper"]}" stroke-width="2"><title>{name}: block {block:.2f}, on/off {eq:.2f}'
                   f'{" (chosen by block effect and APL ratio)" if chosen else ""}</title></circle>')
        if chosen:
            out.append(text(sx(block) + 10, sy(eq) + 4, "chosen", "tick"))
    out.append(text(sx(1.05), sy(1.35), "weak APL: graded", "tick"))
    out.append(text(sx(3.15), sy(0.64), "strong APL: saturates", "tick", "end"))
    return out


def figure(theme: str, models: dict, apl: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "Flies' projection neurons answer where no receptor input reaches; the model's don't, and its APL can't make up for it", "lab"),
           text(24, 50, "Left, middle: with the receptor input the evidence supports, the model answers in the glomeruli that input drives (red) "
                "and nowhere else (rings), where flies'", "note"),
           text(24, 68, "answer strongly in many more. Right: an APL strong enough for flies' block effect saturates and stops favouring "
                "4-methylcyclohexanol; a weak one favours it as flies' does.", "note")]
    out += scatter_panel(c, 80, 290, "3-octanol", models["3-octanol"])
    out += scatter_panel(c, 450, 290, "4-methylcyclohexanol", models["4-methylcyclohexanol"])
    out += apl_panel(c, 840, 250, apl)
    out.append(text(80, Y1 + 56, "red: receptor input of at least 10 spikes/s at Hige et al.'s concentration; rings: less or none", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = ("Projection neuron responses by glomerulus for 3-octanol and 4-methylcyclohexanol, flies against the model, and the "
             "APL sweep's block effect against its equalization")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    e = ROOT / "experiments"
    p55 = json.loads((e / "odor_probe55.json").read_text())["equalization"]["odors"]
    models = {od: p55[od]["pn_evoked_hz_by_glomerulus_first_0.5s"] for od in ("3-octanol", "4-methylcyclohexanol")}
    apl = json.loads((e / "odor_apl_range_check.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"al_inputs-{theme}.svg"
        path_.write_text(figure(theme, models, apl))
        print(path_)


if __name__ == "__main__":
    main()
