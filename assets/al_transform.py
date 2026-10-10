"""The antennal lobe figure in the README (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/al_transform.py      # writes assets/al_transform-light.svg and assets/al_transform-dark.svg

Olsen, Bhandawat & Wilson 2010 drove one glomerulus's receptor neurons (ORNs) alone with a private odor and fitted its
projection neurons' (PNs') rise over the 500 ms stimulus as PN = Rmax ORN^1.5 / (ORN^1.5 + sigma^1.5). The model's
PNs, driven the same way (odor_probe16.py's protocol: each glomerulus's ORNs at 5-160 Hz for 0.5 s, the PNs' mean rise
over it): with the fast synapse alone (odor_probe16.py), and with Nagel et al.'s two-component synapse and presynaptic
inhibition fitted to Olsen & Wilson 2008, Kazama & Wilson's 6.19 mV unitary EPSP read as the synapse's strength at rest
under tonic inhibition (odor_probe21.py) or as its uninhibited strength (odor_probe25.py). One panel per glomerulus Olsen
et al. fitted.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/olfaction.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 486
GLOMERULI = ("DM4", "DL5", "VM7d", "DM1")
OLSEN = {"DM4": (170, 16.3), "DL5": (167, 11.8), "VM7d": (163, 12.4), "DM1": (144, 44.8)}   # Rmax, sigma (spikes/s)
RATES = (5, 10, 20, 40, 80, 160)
# (experiment, path to its transform, label, colour key, dashed)
SERIES = [("odor_probe16", ("conditions", "no cholinergic LN->PN"), "fast synapse only (probe 16)", "faint", False),
          ("odor_probe21", ("conditions", "presynaptic", "transform"), "6.19 mV at rest, under inhibition (probe 21)", "red", False),
          ("odor_probe25", ("condition", "transform"), "6.19 mV uninhibited (probe 25)", "muted", True)]
X0, X1, PW, GAP = 64, 1096, 232, 34                    # panels' left edge, right edge, width, gap
Y0, Y1, TOP = 136, 376, 400                            # plot top, bottom (px), y range (spikes/s)


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def load() -> list[dict]:
    out = []
    for name, path, label, colour, dashed in SERIES:
        d = json.loads((ROOT / "experiments" / f"{name}.json").read_text())
        for k in path:
            d = d[k]
        out.append({"label": label, "colour": colour, "dashed": dashed,
                    "points": {g: [d[g]["alone"][f"{r:g}"]["whole"] for r in RATES] for g in GLOMERULI},
                    "fit": {g: d[g]["fit"] for g in GLOMERULI}})
    return out


def olsen(x, rmax, sigma):
    return rmax * x ** 1.5 / (x ** 1.5 + sigma ** 1.5)


def panel(c, series, g, x0) -> list[str]:
    sx = lambda v: x0 + PW * (np.log2(v) - np.log2(RATES[0])) / (np.log2(RATES[-1]) - np.log2(RATES[0]))
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), TOP) / TOP
    out = [text(x0, Y0 - 16, g, "val")]
    for t in range(0, TOP + 1, 100):
        out.append(f'<line x1="{x0}" y1="{sy(t):.1f}" x2="{x0 + PW}" y2="{sy(t):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if t == 0 else 0.5}"/>')
        if x0 == X0:
            out.append(text(x0 - 8, sy(t) + 4, f"{t}", "tick", "end"))
    for r in RATES:
        out.append(text(sx(r), Y1 + 18, f"{r}", "tick", "middle"))
    rmax, sigma = OLSEN[g]
    xs = np.geomspace(RATES[0], RATES[-1], 60)
    path = " ".join(f"{'M' if i == 0 else 'L'}{sx(x):.1f} {sy(olsen(x, rmax, sigma)):.1f}" for i, x in enumerate(xs))
    out.append(f'<path d="{path}" fill="none" stroke="{c["ink"]}" stroke-width="2.5" stroke-linecap="round"/>')
    for s in series:
        col = c[s["colour"]]
        ys = s["points"][g]
        path = " ".join(f"{'M' if i == 0 else 'L'}{sx(r):.1f} {sy(y):.1f}" for i, (r, y) in enumerate(zip(RATES, ys)))
        dash = ' stroke-dasharray="5 4"' if s["dashed"] else ""
        out.append(f'<path d="{path}" fill="none" stroke="{col}" stroke-width="2"{dash}/>')
        for r, y in zip(RATES, ys):
            out.append(f'<circle cx="{sx(r):.1f}" cy="{sy(y):.1f}" r="4" fill="{col}" stroke="{c["paper"]}" stroke-width="1.5">'
                       f'<title>{s["label"].replace("&", "&amp;")}, {g}: {y:.0f} spikes/s at {r} Hz</title></circle>')
    out.append(text(x0, Y1 + 40, f"flies: Rmax {rmax}, σ {sigma:g}", "tick"))
    for i, s in enumerate(series[1:]):
        name = s["label"].split("(")[-1].rstrip(")")
        out.append(text(x0, Y1 + 56 + 16 * i, f"{name}: Rmax {s['fit'][g]['rmax']:.0f}, σ {s['fit'][g]['sigma']:.0f}", "tick"))
    return out


def figure(theme: str, series: list[dict]) -> str:
    c = THEMES[theme]
    out = [text(24, 32, "With measured inhibition, two readings of one measurement bracket flies' transform", "lab"),
           text(24, 52, "One glomerulus's receptor neurons driven alone for 0.5 s; its projection neurons' mean rise over it.", "note"),
           text(24, 70, "Probes 21 and 25 differ only in whether Kazama & Wilson's 6.19 mV unitary EPSP is the synapse's strength at rest, "
                "under tonic inhibition, or uninhibited.", "note")]
    lx = 24
    items = [("flies (Olsen et al. 2010's fit)", c["ink"], False, 2.5)] + [(s["label"], c[s["colour"]], s["dashed"], 2) for s in series]
    for label, col, dashed, wid in items:            # legend, one row above the panels
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        out.append(f'<line x1="{lx}" y1="96" x2="{lx + 26}" y2="96" stroke="{col}" stroke-width="{wid}"{dash}/>')
        out.append(text(lx + 32, 100, label, "tick"))
        lx += 32 + 6.1 * len(label) + 26
    for k, g in enumerate(GLOMERULI):
        out += panel(c, series, g, X0 + k * (PW + GAP))
    out.append(text(X0 - 48, (Y0 + Y1) / 2, "", "tick"))
    out.append(f'<text x="18" y="{(Y0 + Y1) / 2:.1f}" class="tick" text-anchor="middle" transform="rotate(-90 18 {(Y0 + Y1) / 2:.1f})">'
               f'projection neurons, spikes/s above rest</text>')
    out.append(text((X0 + X1) / 2, Y1 + 104, "receptor neurons' rate, spikes/s (log scale)", "tick", "middle"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    last = series[-1]
    title = ("The antennal lobe's receptor-to-projection-neuron transform in four glomeruli, against Olsen et al. 2010's fits to "
             "flies: with " + last["label"] + ", fitted Rmax " + ", ".join(f'{last["fit"][g]["rmax"]:.0f}' for g in GLOMERULI)
             + " spikes/s against flies' 144-170")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    series = load()
    for theme in THEMES:
        path = OUT / f"al_transform-{theme}.svg"
        path.write_text(figure(theme, series))
        print(path)


if __name__ == "__main__":
    main()
