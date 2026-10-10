"""The antennal lobe local neuron figure in the README (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/al_lns.py      # writes assets/al_lns-light.svg and assets/al_lns-dark.svg

Top: the GABAergic local neurons' (LNs') mean rate per cell to 2-heptanone in 50 ms bins, against Nagel et al. 2015's
mean of 45 LNs (Fig. 5b, read off the figure; 22, 13, 8 and 6 spikes/s over 0-50, 50-100, 100-200 and 200-500 ms after
their fast valve), drawn 50 ms later for the model's receptor latency as odor_probe39.py's fit compares them. Left: every
synapse onto the LNs scaled by s in the model as built, the LNs' rest re-set (odor_probe39.py). Right: the antennal lobe
rebuilt around the scaled LNs, their rest at flies' 4 spikes/s and the presynaptic inhibition fitted again
(odor_probe40.py). Bottom: 3-octanol's strongly driven projection neurons (PNs of glomeruli driven above 0.2) in the same
runs, each line divided by its own peak, against the mean of 843 PN responses in flies (Bhandawat et al. 2007, Fig. 1b,
read off the figure: the peak about 145 ms after the valve, 0.48 of it at 500 ms), moved 75 ms earlier for the valve's
delay (odor_probe21.py) so that 0 is the odor reaching the antenna, as in the model.
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
W, H = 1120, 776
VALVE = 0.075
NAGEL = ((0.0, 0.05, 22.0), (0.05, 0.1, 13.0), (0.1, 0.2, 8.0), (0.2, 0.5, 6.0))   # flies' bins after the valve, spikes/s
LATENCY = 0.05                                     # odor_probe39.py: the model's bins taken 50 ms later
BHANDAWAT = ((0.145 - VALVE, 1.0), (0.5 - VALVE, 0.48))
T0, T1 = 0.0, 0.55
X0, PW, GAP = 92, 470, 70
LN = (128, 348, 70)                                # top panel: top y, bottom y, max spikes/s
PN = (436, 656, 1.2)                               # bottom panel: top y, bottom y, max (fraction of the peak)
SWEEP_OPACITY = {"1": 0.32, "0.6": 0.44, "0.45": 0.58, "0.35": 0.76, "0.25": 1.0}


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def scales(x0, box):
    top, bottom, vmax = box
    return (lambda t: x0 + PW * (t - T0) / (T1 - T0)), (lambda v: bottom - (bottom - top) * min(max(v, 0), vmax) / vmax)


def axes(c, x0, box, unit, ticks, fmt, label: bool) -> list[str]:
    top, bottom, _ = box
    sx, sy = scales(x0, box)
    out = []
    for v in ticks:
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + PW}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        if label:
            out.append(text(x0 - 8, sy(v) + 4, fmt(v), "tick", "end"))
    for t in (0, 0.1, 0.2, 0.3, 0.4, 0.5):
        out.append(text(sx(t), bottom + 16, f"{t:g}", "tick", "middle"))
    if label:
        out.append(f'<text x="{x0 - 52}" y="{(top + bottom) / 2:.1f}" class="tick" text-anchor="middle" '
                   f'transform="rotate(-90 {x0 - 52} {(top + bottom) / 2:.1f})">{unit}</text>')
    return out


def line(x0, box, vs, colour, opacity=1.0, dashed=False, width=2.2, title="") -> str:
    sx, sy = scales(x0, box)
    d = " ".join(f"{'M' if i == 0 else 'L'}{sx(0.025 + 0.05 * i):.1f} {sy(v):.1f}" for i, v in enumerate(vs))
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    tip = f"<title>{title}</title>" if title else ""
    return (f'<path d="{d}" fill="none" stroke="{colour}" stroke-opacity="{opacity}" stroke-width="{width}" '
            f'stroke-linejoin="round"{dash}>{tip}</path>')


def legend(c, x, y, items) -> list[str]:
    out = []
    for i, (label, colour, opacity, dashed) in enumerate(items):
        yy = y + 17 * i
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        out.append(f'<line x1="{x}" y1="{yy:.1f}" x2="{x + 26}" y2="{yy:.1f}" stroke="{colour}" stroke-opacity="{opacity}" '
                   f'stroke-width="2.4"{dash}/>')
        out.append(text(x + 34, yy + 4, label, "tick"))
    return out


def nagel(c, x0) -> list[str]:
    sx, sy = scales(x0, LN)
    out = []
    for a, z, v in NAGEL:
        a, z = a + LATENCY, z + LATENCY
        out.append(f'<line x1="{sx(a):.1f}" y1="{sy(v):.1f}" x2="{sx(z):.1f}" y2="{sy(v):.1f}" stroke="{c["ink"]}" '
                   f'stroke-width="1.4" stroke-dasharray="4 3"/>')
        out.append(f'<circle cx="{sx((a + z) / 2):.1f}" cy="{sy(v):.1f}" r="4.5" fill="{c["paper"]}" stroke="{c["ink"]}" '
                   f'stroke-width="1.8"><title>flies (Nagel et al. 2015): {v:g} spikes/s per LN over {1000 * (a - LATENCY):.0f}-'
                   f'{1000 * (z - LATENCY):.0f} ms after the valve, drawn {1000 * LATENCY:.0f} ms later</title></circle>')
    out.append(f'<line x1="{sx(0):.1f}" y1="{sy(4):.1f}" x2="{sx(T1):.1f}" y2="{sy(4):.1f}" stroke="{c["ink"]}" '
               f'stroke-width="1" stroke-dasharray="1 3"/>')
    out.append(text(sx(T1) - 4, sy(4) + 14, "flies' rest, 4 spikes/s", "tick", "end"))
    return out


def bhandawat(c, x0) -> list[str]:
    sx, sy = scales(x0, PN)
    (t0, v0), (t1, v1) = BHANDAWAT
    out = [f'<line x1="{sx(t0):.1f}" y1="{sy(v0):.1f}" x2="{sx(t1):.1f}" y2="{sy(v1):.1f}" stroke="{c["ink"]}" '
           f'stroke-width="1.2" stroke-dasharray="4 3"/>']
    for t, v in BHANDAWAT:
        out.append(f'<circle cx="{sx(t):.1f}" cy="{sy(v):.1f}" r="4.5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.8">'
                   f'<title>flies (Bhandawat et al. 2007, 843 PN responses): {v:g} of the peak at {t + VALVE:.3f} s after the valve'
                   f'</title></circle>')
    return out


def normalised(vs) -> tuple[list, float]:
    peak = max(vs)
    return [v / peak for v in vs], peak


def figure(theme: str, sweep: dict, rebuilt: dict | None) -> str:
    c = THEMES[theme]
    best = rebuilt["best"] if rebuilt else None
    out = [text(24, 30, "Scaled to flies' onset, the local neurons leave the projection neurons' time course as it was", "lab"),
           text(24, 50, "Red: the model. Top: the GABAergic LNs' mean rate per cell to 2-heptanone. Bottom: 3-octanol's strongly driven PNs, "
                "each line over its own peak.", "note"),
           text(24, 68, "Left: the model as built with every synapse onto the LNs times s (odor_probe39.py). Right: the antennal lobe rebuilt "
                "around the scaled LNs (odor_probe40.py).", "note"),
           text(24, 86, "Rings: flies (Nagel et al. 2015's LNs, drawn 50 ms later for the model's receptor latency; Bhandawat et al. 2007's "
                "mean of 843 PN responses).", "note")]
    panels = [(X0, "the model as built, every LN input times s (odor_probe39.py)"),
              (X0 + PW + GAP, "rebuilt around the scaled LNs (odor_probe40.py)")]
    for k, (x0, title) in enumerate(panels):
        out.append(text(x0, LN[0] - 12, title, "val"))
        out += axes(c, x0, LN, "spikes/s per GABAergic LN, 2-heptanone", range(0, 71, 10), lambda v: f"{v}", k == 0)
        out += nagel(c, x0)
        out += axes(c, x0, PN, "3-octanol's driven PNs, of their peak", (0, 0.25, 0.5, 0.75, 1.0), lambda v: f"{v:g}", k == 0)
        out += bhandawat(c, x0)
    x0 = panels[0][0]
    for s, row in sweep["scales"].items():
        ln = row["odors"]["2-heptanone"]["ln_hz_50ms"]
        pn, peak = normalised(row["odors"]["3-octanol"]["oct_pn_hz_50ms"])
        op = SWEEP_OPACITY.get(s, 0.5)
        out.append(line(x0, LN, ln, c["red"], op, title=f"s = {s}: {', '.join(f'{v:g}' for v in ln)} spikes/s per LN"))
        out.append(line(x0, PN, pn, c["red"], op, title=f"s = {s}: peak {peak:.0f} spikes/s"))
    out += legend(c, x0 + PW - 150, LN[0] + 10, [(f"s = {s}", c["red"], SWEEP_OPACITY.get(s, 0.5), False) for s in sweep["scales"]])
    out.append(text(x0 + PW, PN[1] + 34, "PNs' peaks: " + ", ".join(f"{max(r['odors']['3-octanol']['oct_pn_hz_50ms']):.0f}"
                                                                    for r in sweep["scales"].values()) + " spikes/s (s = 1 to 0.25)", "tick", "end"))
    if rebuilt:
        x0 = panels[1][0]
        ref = sweep["scales"]["1"]
        out.append(line(x0, LN, ref["odors"]["2-heptanone"]["ln_hz_50ms"], c["faint"], 1.0, title="as built, s = 1"))

        pn, _ = normalised(ref["odors"]["3-octanol"]["oct_pn_hz_50ms"])
        out.append(line(x0, PN, pn, c["faint"], 1.0, title="as built, s = 1"))
        notes = []
        for s, entry in rebuilt["conditions"].items():
            r = entry["ln_response"]
            ln = r["odors"]["2-heptanone"]["ln_hz_50ms"]
            pn, peak = normalised(r["odors"]["3-octanol"]["oct_pn_hz_50ms"])
            dashed = s != best
            out.append(line(x0, LN, ln, c["red"], 1.0, dashed, title=f"rebuilt, s = {s}: {', '.join(f'{v:g}' for v in ln)} spikes/s per LN"))
            out.append(line(x0, PN, pn, c["red"], 1.0, dashed, title=f"rebuilt, s = {s}: peak {peak:.0f} spikes/s"))
            notes.append(f"s = {s}{' (dashed)' if dashed else ''}: peak {peak:.0f}")
        out += legend(c, x0 + PW - 150, LN[0] + 10, [("as built, s = 1", c["faint"], 1.0, False)] +
                      [(f"rebuilt, s = {s}", c["red"], 1.0, s != best) for s in rebuilt["conditions"]])
        out.append(text(x0 + PW, PN[1] + 34, "PNs' peaks: " + "; ".join(notes) + " spikes/s", "tick", "end"))
    out.append(text(X0 + PW + GAP / 2, PN[1] + 60, "time from the odor reaching the antenna (s)", "tick", "middle"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = "The antennal lobe's GABAergic local neurons' odor response in the model against flies', and its projection neurons' time course"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    sweep = json.loads((ROOT / "experiments" / "odor_probe39.json").read_text())
    path = ROOT / "experiments" / "odor_probe40.json"
    rebuilt = json.loads(path.read_text()) if path.exists() else None
    if rebuilt:
        rebuilt["best"] = min(rebuilt["conditions"], key=lambda s: rebuilt["conditions"][s]["ln_response"]["rms_log_error"])
    for theme in THEMES:
        p = OUT / f"al_lns-{theme}.svg"
        p.write_text(figure(theme, sweep, rebuilt))
        print(p)


if __name__ == "__main__":
    main()
