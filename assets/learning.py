"""The learning figure in the README (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/learning.py      # writes assets/learning-light.svg and assets/learning-dark.svg

Hige et al. 2015's protocol in the model (learning_pilot.py): dopamine-gated depression at the Kenyon cell-to-MBON11
synapses, its rate set so that the paired odor's charge (the current its Kenyon cells deliver) falls 90%. Left two
panels: for each odor, how far its charge falls with the same rate (tau_e 0.5 s), on odor_probe30.py's model
(learning_pilot3) and on the rebuilt model (odor_probe44.py's antennal lobe with mb_calibration.py's mushroom body;
learning_pilot5), its Kenyon cell-to-MBON synapses undepressed or depressing as Yamada et al. 2024 measured, MBON11's spikes
counted held near 6 Hz as Hige et al. counted them. Right: MBON11's evoked spikes after pairing, as a drop from before, for the paired and the unpaired
odor. Flies (Hige et al. 2015, read off the figures in research_notes/Rung 9 learning data/hige2015_specificity.md): with
3-octanol paired, its spikes fell 80% and 4-methylcyclohexanol's 27% (Fig. 1F, n = 7), and 4-methylcyclohexanol's charge
fell 20% (Fig. 3, n = 5, not significant) and 35% (Fig. 4, n = 6, every cell); with 4-methylcyclohexanol paired, its
spikes fell 76% and 3-octanol's 38% (Fig. S3D, n = 6; no charge measured); the other four odors weren't tested.
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
W, H = 1120, 412
ODORS = ("3-octanol", "4-methylcyclohexanol", "ethyl acetate", "isopentyl acetate", "benzaldehyde", "2-heptanone")
RUNS = [("learning_pilot3", None, "old model (pilot 3)", "faint"),
        ("learning_pilot5", "undepressed", "rebuilt model, Kenyon cell-to-MBON synapses undepressed (pilot 5)", "red"),
        ("learning_pilot5", "depressing", "rebuilt model, the synapses depressing as measured (pilot 5)", "muted")]
FLIES_SPIKES = {("3-octanol", "paired"): 0.80, ("3-octanol", "unpaired"): 0.27,               # Fig. 1F
                ("4-methylcyclohexanol", "paired"): 0.76, ("4-methylcyclohexanol", "unpaired"): 0.38}  # Fig. S3D
FLIES_CHARGE = {"3-octanol": [(0.20, "Fig. 3, n = 5, not significant"), (0.35, "Fig. 4, n = 6")]}   # the unpaired odor's
X0, PW, GAP = 176, 250, 70                       # first panel's left edge, charge panels' width, gap
SX0, SPW = 884, 196                              # spike panel's left edge and width
Y0, ROW = 170, 34                                # first row's centre, row spacing


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def load() -> list[dict]:
    out = []
    for name, variant, label, colour in RUNS:
        d = json.loads((ROOT / "experiments" / f"{name}.json").read_text())
        if variant:
            d = d["variants"][variant]
        out.append({"label": label, "colour": colour,
                    "pairings": {p["paired"]: {"unpaired": p["unpaired"], "drop": p["by_tau"]["0.5"]["charge_drop"],
                                               "spikes": p["spikes"]} for p in d["pairings"]}})
    return out


def grid(c, x0, width, bottom) -> list[str]:
    out = []
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        x = x0 + width * t
        out.append(f'<line x1="{x:.1f}" y1="{Y0 - 18}" x2="{x:.1f}" y2="{bottom}" stroke="{c["rule"]}" '
                   f'stroke-opacity="{1 if t == 0 else 0.5}"/>')
        out.append(text(x, bottom + 16, f"{t:.0%}", "tick", "middle"))
    return out


def dot(c, x, y, colour, title, ring=False) -> str:
    fill = "none" if ring else colour
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{fill}" stroke="{colour if ring else c["paper"]}" stroke-width="2">'
            f'<title>{title}</title></circle>')


def charge_panel(c, runs, paired, x0) -> list[str]:
    sx = lambda v: x0 + PW * min(max(v, 0.0), 1.0)
    bottom = Y0 + ROW * (len(ODORS) - 1) + 22
    unpaired = runs[0]["pairings"][paired]["unpaired"]
    out = [text(x0, Y0 - 34, f"{paired} paired", "val")] + grid(c, x0, PW, bottom)
    for i, odor in enumerate(ODORS):
        y = Y0 + ROW * i
        if x0 == X0:
            out.append(text(X0 - 14, y + 4, odor, "tick", "end"))
        role = " (paired)" if odor == paired else " (unpaired)" if odor == unpaired else ""
        drops = [r["pairings"][paired]["drop"][odor] for r in runs]
        out.append(f'<line x1="{sx(min(drops)):.1f}" y1="{y}" x2="{sx(max(drops)):.1f}" y2="{y}" stroke="{c["rule"]}" stroke-width="2"/>')
        if odor == unpaired:
            for v, src in FLIES_CHARGE.get(paired, []):
                out.append(dot(c, sx(v), y, c["ink"], f"flies: {odor}'s charge {v:.0%} lower (Hige et al. 2015, {src})", ring=True))
        for r, v in zip(runs, drops):
            out.append(dot(c, sx(v), y, c[r["colour"]], f'{r["label"]}: {odor}{role}, charge {v:.0%} lower'))
    return out


def spike_panel(c, runs) -> list[str]:
    sx = lambda v: SX0 + SPW * min(max(v, 0.0), 1.0)
    rows = [(p, role) for p in runs[0]["pairings"] for role in ("paired", "unpaired")]
    bottom = Y0 + ROW * (len(rows) - 1) + 22
    out = [text(SX0, Y0 - 34, "MBON11's spikes after pairing", "val")] + grid(c, SX0, SPW, bottom)
    for i, (paired, role) in enumerate(rows):
        y = Y0 + ROW * i
        odor = paired if role == "paired" else runs[0]["pairings"][paired]["unpaired"]
        short = {"3-octanol": "OCT", "4-methylcyclohexanol": "MCH"}
        out.append(text(SX0 - 10, y + 4, f"{short[odor]}, {role}", "tick", "end"))
        f = FLIES_SPIKES[(paired, role)]
        out.append(dot(c, sx(f), y, c["ink"], f"flies: spikes {f:.0%} lower (Hige et al. 2015)", ring=True))
        for r in runs:
            s = r["pairings"][paired]["spikes"][odor]
            v = s["drop"]
            label = f'{r["label"]}: {odor} ({role}), {s["pre"]:.1f} to {s["post"]:.1f} spikes, {v:.0%} lower'
            out.append(dot(c, sx(v), y, c[r["colour"]], label))
            if v > 1.0:
                out.append(text(sx(1.0) + 9, y + 4, f"{v:.0%}", "tick"))
    return out


def figure(theme: str, runs: list[dict]) -> str:
    c = THEMES[theme]
    out = [text(24, 32, "On the rebuilt model learning is about as specific as flies' both ways; with 4-methylcyclohexanol paired, still too narrow", "lab"),
           text(24, 52, "Dopamine-gated depression at Kenyon cell-to-MBON11 synapses, its rate set to cut the paired odor's input by 90%. "
                "Left: how far each odor's input falls.", "note"),
           text(24, 70, "Right: MBON11's odor-evoked spikes afterwards. Rings: flies (Hige et al. 2015; no charge was measured with "
                "4-methylcyclohexanol paired).", "note")]
    lx = 24
    items = [(label, c[colour], False) for _, _, label, colour in RUNS] + [("flies", c["ink"], True)]
    for label, col, ring in items:                 # legend, one row above the panels
        out.append(f'<circle cx="{lx + 6}" cy="100" r="6" fill="{"none" if ring else col}" stroke="{col}" stroke-width="2"/>')
        out.append(text(lx + 18, 104, label, "tick"))
        lx += 18 + 6.1 * len(label) + 30
    pairs = list(runs[0]["pairings"])
    for k, paired in enumerate(pairs):
        out += charge_panel(c, runs, paired, X0 + k * (PW + GAP))
    out += spike_panel(c, runs)
    bottom = Y0 + ROW * (len(ODORS) - 1) + 22
    out.append(text(X0 + (2 * PW + GAP) / 2, bottom + 40, "drop in the odor's Kenyon cell input (charge) to MBON11", "tick", "middle"))
    out.append(text(SX0 + SPW / 2, Y0 + ROW * 3 + 22 + 40, "drop in evoked spikes", "tick", "middle"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    new = runs[1]["pairings"]
    title = ("Learning's specificity in the rebuilt model (Kenyon cell-to-MBON synapses undepressed): pairing 3-octanol cuts "
             f'4-methylcyclohexanol\'s spikes by {new["3-octanol"]["spikes"]["4-methylcyclohexanol"]["drop"]:.0%} (flies 27%), and pairing '
             f'4-methylcyclohexanol cuts 3-octanol\'s by {new["4-methylcyclohexanol"]["spikes"]["3-octanol"]["drop"]:.0%} (flies 38%)')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    runs = load()
    for theme in THEMES:
        path = OUT / f"learning-{theme}.svg"
        path.write_text(figure(theme, runs))
        print(path)


if __name__ == "__main__":
    main()
