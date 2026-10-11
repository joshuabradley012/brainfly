"""Rung 9's learning test, attempt 1 (pre-registered), drawn from its saved result (nothing by hand).

    python assets/rung9.py      # writes assets/rung9-light.svg and assets/rung9-dark.svg

experiments/rung9_learning.py: Hige et al. 2015's pairing on the model, odor_probe56.py's with the receptor input the
evidence supports. Each column is one pre-registered quantity: how far MBON11's evoked spikes (or its Kenyon cell
charge) fall after pairing, for the paired and the unpaired odor, both ways round, and after backward pairing (the
charge's change). Shaded: the band the test required (research_notes/Rung 9 learning data/hige2015_specificity.md);
rings: flies (Hige et al. 2015; for the unpaired odor's charge their two experiments); red: the model.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/al_transform.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 460
Y0, Y1 = 110, 350
YLO, YHI = -30.0, 120.0
OCT, MCH = "3-octanol", "4-methylcyclohexanol"


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def columns(d: dict) -> list:
    by = {(p["paired"], p["unpaired"]): p for p in d["result"]["pairings"]}
    o, m = by[(OCT, MCH)], by[(MCH, OCT)]
    v = d["verdicts"]
    sp = lambda p, od: 100 * p["spikes"][od]["drop"]
    ch = lambda p, od: 100 * p["by_tau"]["0.5"]["charge_drop"][od]
    bw = lambda p: 100 * p["by_tau"]["0.5"]["backward_charge_drop"]
    return [  # (group, label, model, band, flies, test name)
        ("3-octanol paired", "3-octanol's spikes", sp(o, OCT), (65, 120), (80,), "PAIRED"),
        ("3-octanol paired", "4-methylcyclohexanol's spikes", sp(o, MCH), (10, 45), (27,), "UNPAIRED"),
        ("3-octanol paired", "4-methylcyclohexanol's charge", ch(o, MCH), (10, 45), (20, 35), "UNPAIRED"),
        ("4-methylcyclohexanol paired", "its own spikes", sp(m, MCH), (65, 120), (76,), "RECIPROCAL"),
        ("4-methylcyclohexanol paired", "3-octanol's spikes", sp(m, OCT), (15, 50), (38,), "RECIPROCAL"),
        ("dopamine first", "3-octanol's charge", bw(o), (-15, 15), (7,), "BACKWARD"),
        ("dopamine first", "4-methylcyclohexanol's charge", bw(m), (-15, 15), (-4,), "BACKWARD"),
    ], v


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    cols, v = columns(d)
    x0, pw = 90, 980
    sy = lambda val: Y1 - (Y1 - Y0) * (min(max(val, YLO), YHI) - YLO) / (YHI - YLO)
    verdict = "passed" if v["pass"] else "failed"
    out = [text(24, 30, f"Rung 9's learning test, attempt 1 (pre-registered): {verdict}", "lab"),
           text(24, 50, "Each column: how far MBON11's response falls after an odor is paired with dopamine. Shaded: the band "
                "fixed in advance; rings: flies (Hige et al. 2015); red: the model.", "note"),
           text(24, 68, "3-octanol paired, the model is as specific as flies; 4-methylcyclohexanol paired, it barely touches "
                "3-octanol, whose input its few Kenyon cells hardly carry.", "note")]
    for val in (-25, 0, 25, 50, 75, 100):
        out.append(f'<line x1="{x0}" y1="{sy(val):.1f}" x2="{x0 + pw}" y2="{sy(val):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if val == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(val) + 4, f"{val}%", "tick", "end"))
    out.append(f'<text transform="translate({x0 - 50},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">fall after pairing</text>')
    step = pw / len(cols)
    groups = {}
    for i, (group, label, model, band, flies, test) in enumerate(cols):
        cx = x0 + step * (i + 0.5)
        groups.setdefault(group, []).append(cx)
        lo, hi = band
        out.append(f'<rect x="{cx - 26:.1f}" y="{sy(hi):.1f}" width="52" height="{sy(lo) - sy(hi):.1f}" rx="3" fill="{c["ink"]}" fill-opacity="0.12">'
                   f'<title>band: {lo}-{hi if hi < 120 else 100}%</title></rect>')
        for k, f in enumerate(flies):
            fx = cx - 10 + 20 * k if len(flies) > 1 else cx - 10
            out.append(f'<circle cx="{fx:.1f}" cy="{sy(f):.1f}" r="5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6"><title>flies: {f}%</title></circle>')
        out.append(f'<circle cx="{cx + 10:.1f}" cy="{sy(model):.1f}" r="6" fill="{c["red"]}" stroke="{c["paper"]}" stroke-width="2"><title>model: {model:.1f}%</title></circle>')
        ok = lo <= model <= hi
        head, _, tail = label.rpartition(" ")                    # two lines: "4-methylcyclohexanol's" / "spikes"
        out.append(text(cx, Y1 + 16, head, "tick", "middle"))
        out.append(text(cx, Y1 + 29, tail, "tick", "middle"))
        out.append(text(cx, sy(min(max(model, YLO), YHI)) - 14 if model > hi else sy(hi) - 8, "in band" if ok else "outside", "tick" if ok else "miss", "middle"))
    for group, xs in groups.items():
        out.append(text(sum(xs) / len(xs), Y1 + 50, group, "val", "middle"))
    tests = ", ".join(f"{k} {'pass' if v[k]['pass'] else 'fail'}" for k in ("PAIRED", "UNPAIRED", "RECIPROCAL", "BACKWARD"))
    out.append(text(x0 + pw, Y1 + 74, f"tests: {tests} (PAIRED and RECIPROCAL also need the paired odor 30 points beyond the unpaired)", "tick", "end"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .miss {{ font-size: 11px; font-weight: 600; fill: {c["red"]}; }}
    """
    title = "Rung 9's pre-registered learning test: MBON11's response drops after pairing, the model against flies and the bands"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "rung9_learning.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"rung9-{theme}.svg"
        path_.write_text(figure(theme, d))
        print(path_)


if __name__ == "__main__":
    main()
