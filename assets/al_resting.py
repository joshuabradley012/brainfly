"""The antennal lobe at rest: tonic presynaptic inhibition (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/al_resting.py      # writes assets/al_resting-light.svg and assets/al_resting-dark.svg

Left: how far the cholinergic projection neurons' free membrane potential (where the membrane would sit without its own
spikes) falls when every receptor neuron is silenced, by glomerulus, in odor_probe56.py's model (grey;
experiments/odor_gaba_block_check.py) and odor_probe57.py's, which adds tonic presynaptic inhibition (red), against flies'
estimates (rings; research_notes/Rung 9 learning data/orn_pn_resting_state.md, section
1.6: Kazama & Wilson 2009's depression with measured rates and counts, no tonic inhibition; derived, not measured) and
Gouwens & Wilson 2009's 5-10 mV over unstated glomeruli (shaded). Right: how far it rises when the antennal lobe's GABA
receptors are blocked, in DM6, VM2 and VM7, the glomeruli Nagel, Hong & Wilson 2015 recorded, against their 5-8 mV
(shaded).
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
W, H = 1120, 470
Y0, Y1 = 128, 374
DROP = ("DM4", "DM6", "VM2", "VM7d", "DL5", "DM1", "DL1", "DA1")
FLY_DROP = {"DM4": (5.6,), "DM6": (7.6,), "VM2": (7.4,), "VM7d": (6.6, 6.8), "DL5": (7.5, 7.7), "DM1": (13.4, 14.2),
            "DL1": (14.6,), "DA1": (14.6,)}          # orn_pn_resting_state.md, section 1.6 (KW09 pool)
RISE = ("DM6", "VM2", "VM7d", "VM7v")
SILENCED, BLOCKED = "receptor neurons silenced", "GABA receptors blocked"


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, before: dict, after: dict, divisor: float) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "The antennal lobe at rest: the model's postsynaptic GABA already disinhibits like flies'", "lab"),
           text(24, 50, "Grey: blocking GABA raises the PNs 5 mV (flies 5-8) with no tonic presynaptic inhibition. Red: dividing "
                f"the receptor synapses by {divisor:g} at rest (Nagel et al.'s form)", "note"),
           text(24, 68, "shrinks the resting drive, still twice flies', but makes the disinhibition overshoot. Membrane "
                "potentials as they would sit without the PNs' own spikes.", "note")]
    # left: the drop by glomerulus
    x0, pw = 80, 560
    ymax = 40.0
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), ymax) / ymax
    out.append(text(x0, Y0 - 18, "Every receptor neuron silenced: the fall, by glomerulus", "val"))
    for v in range(0, 41, 10):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    out.append(f'<text transform="translate({x0 - 44},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">mV</text>')
    out.append(f'<rect x="{x0}" y="{sy(10):.1f}" width="{pw}" height="{sy(5) - sy(10):.1f}" fill="{c["ink"]}" fill-opacity="0.08">'
               f'<title>Gouwens &amp; Wilson 2009: 5-10 mV over unstated glomeruli</title></rect>')
    out.append(text(x0 + pw - 4, sy(10) - 5, "Gouwens & Wilson: 5-10 mV", "tick", "end"))
    step = pw / len(DROP)
    for i, g in enumerate(DROP):
        cx = x0 + step * (i + 0.5)
        b = -before["conditions"][SILENCED]["free_change_mv"][g]
        a = -after["conditions"][SILENCED]["free_change_mv"][g]
        fly = FLY_DROP[g]
        if len(fly) > 1:
            out.append(f'<line x1="{cx - 14:.1f}" y1="{sy(fly[0]):.1f}" x2="{cx - 14:.1f}" y2="{sy(fly[1]):.1f}" stroke="{c["ink"]}" stroke-width="2"/>')
        out.append(f'<circle cx="{cx - 14:.1f}" cy="{sy(sum(fly) / len(fly)):.1f}" r="5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6">'
                   f'<title>flies, estimated: {"-".join(f"{x:g}" for x in fly)} mV</title></circle>')
        out.append(f'<line x1="{cx + 2:.1f}" y1="{sy(b):.1f}" x2="{cx + 12:.1f}" y2="{sy(a):.1f}" stroke="{c["faint"]}" stroke-width="1.2"/>')
        out.append(f'<circle cx="{cx + 2:.1f}" cy="{sy(b):.1f}" r="5" fill="{c["faint"]}" stroke="{c["paper"]}" stroke-width="1.5"><title>without: {b:.1f} mV</title></circle>')
        out.append(f'<circle cx="{cx + 12:.1f}" cy="{sy(a):.1f}" r="6" fill="{c["red"]}" stroke="{c["paper"]}" stroke-width="2"><title>with: {a:.1f} mV</title></circle>')
        out.append(text(cx, Y1 + 18, g, "tick", "middle"))
    # right: the rise with GABA blocked
    x1, pw2 = 760, 320
    ymax2 = 16.0
    sy2 = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), ymax2) / ymax2
    out.append(text(x1, Y0 - 18, "GABA receptors blocked: the rise (flies 5-8 mV, shaded)", "val"))
    for v in range(0, 17, 4):
        out.append(f'<line x1="{x1}" y1="{sy2(v):.1f}" x2="{x1 + pw2}" y2="{sy2(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x1 - 8, sy2(v) + 4, f"{v}", "tick", "end"))
    out.append(f'<rect x="{x1}" y="{sy2(8):.1f}" width="{pw2}" height="{sy2(5) - sy2(8):.1f}" fill="{c["ink"]}" fill-opacity="0.12">'
               f'<title>Nagel, Hong &amp; Wilson 2015: 5-8 mV (DM6, VM2, VM7)</title></rect>')
    step2 = pw2 / len(RISE)
    for i, g in enumerate(RISE):
        cx = x1 + step2 * (i + 0.5)
        b = before["conditions"][BLOCKED]["free_change_mv"][g]
        a = after["conditions"][BLOCKED]["free_change_mv"][g]
        out.append(f'<rect x="{cx - 20:.1f}" y="{sy2(b):.1f}" width="16" height="{sy2(0) - sy2(b):.1f}" rx="3" fill="{c["faint"]}"><title>without: {b:.1f} mV</title></rect>')
        out.append(f'<rect x="{cx + 2:.1f}" y="{sy2(a):.1f}" width="16" height="{sy2(0) - sy2(a):.1f}" rx="3" fill="{c["red"]}"><title>with: {a:.1f} mV</title></rect>')
        out.append(text(cx, Y1 + 18, g, "tick", "middle"))
    nb = before["conditions"][BLOCKED]["free_change_mv"]["nagel_glomeruli"]
    na = after["conditions"][BLOCKED]["free_change_mv"]["nagel_glomeruli"]
    db = -before["conditions"][SILENCED]["free_change_mv"]["all"]
    da = -after["conditions"][SILENCED]["free_change_mv"]["all"]
    out.append(text(x0, H - 30, f"Over all cholinergic uniglomerular PNs the fall goes from {db:.1f} to {da:.1f} mV; in Nagel et al.'s "
                    f"glomeruli the rise from {nb:.1f} to {na:.1f} mV. Fly fall estimates are derived (rings), not measured.", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = "The antennal lobe at rest: projection neurons' free membrane potential with receptor neurons silenced and with GABA blocked, two models against flies"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    before = json.loads((ROOT / "experiments" / "odor_gaba_block_check.json").read_text())
    p57 = json.loads((ROOT / "experiments" / "odor_probe57.json").read_text())
    after = p57["condition"]["resting_state"]
    for theme in THEMES:
        path_ = OUT / f"al_resting-{theme}.svg"
        path_.write_text(figure(theme, before, after, p57["resting_divisor"]))
        print(path_)


if __name__ == "__main__":
    main()
