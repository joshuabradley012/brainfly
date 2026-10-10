"""The learning figure in the README (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/learning.py      # writes assets/learning-light.svg and assets/learning-dark.svg

Hige et al. 2015's protocol in the model (learning_pilot.py, learning_pilot2.py): dopamine-gated depression at the Kenyon
cell-to-MBON11 synapses, its rate set so that the paired odor's charge (the current its Kenyon cells deliver) falls 90%.
Left two panels: for each odor, how far its charge falls with the same rate (tau_e 0.5 s), on odor_probe7.py's model
(learning_pilot) and on odor_probe30.py's antennal lobe with MBON11's synapses from its own measurements
(learning_pilot2). Right: MBON11's evoked spikes after pairing, as a drop from before, for the paired and the unpaired
odor. Flies (Hige et al. 2015, one pairing direction): the paired odor's spikes fell 80% (118 to 24) and its charge 90%;
the unpaired odor's spikes fell about 25% (110 to 83) and its charge didn't change significantly (n = 5); the other four
odors weren't tested.
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
RUNS = [("learning_pilot", "odor_probe7's model (learning pilot 1)", "faint"),
        ("learning_pilot2", "probe 30's antennal lobe, MBON11 from its measurements (pilot 2)", "red")]
FLIES_SPIKES = {"paired": 0.80, "unpaired": 0.25}
X0, PW, GAP = 176, 250, 70                       # first panel's left edge, charge panels' width, gap
SX0, SPW = 884, 196                              # spike panel's left edge and width
Y0, ROW = 170, 34                                # first row's centre, row spacing


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def load() -> list[dict]:
    out = []
    for name, label, colour in RUNS:
        d = json.loads((ROOT / "experiments" / f"{name}.json").read_text())
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
            out.append(dot(c, sx(0), y, c["ink"], "flies: no significant change (Hige et al. 2015, n = 5)", ring=True))
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
        f = FLIES_SPIKES[role]
        out.append(dot(c, sx(f), y, c["ink"], f"flies: spikes {f:.0%} lower (Hige et al. 2015, one pairing direction)", ring=True))
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
    out = [text(24, 32, "Learning is now more specific to the paired odor, but not yet as specific as flies'", "lab"),
           text(24, 52, "Dopamine-gated depression at Kenyon cell-to-MBON11 synapses, its rate set to cut the paired odor's input by 90%. "
                "Left: how far each odor's input falls.", "note"),
           text(24, 70, "Right: MBON11's odor-evoked spikes afterwards. Rings: flies (Hige et al. 2015; at 0%: the unpaired odor's input "
                "didn't change significantly).", "note")]
    lx = 24
    items = [(label, c[colour], False) for _, label, colour in RUNS] + [("flies", c["ink"], True)]
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
    new, old = runs[-1]["pairings"], runs[0]["pairings"]
    title = ("Learning's specificity in the model: pairing 3-octanol cuts 4-methylcyclohexanol's Kenyon cell input to MBON11 by "
             f'{new["3-octanol"]["drop"]["4-methylcyclohexanol"]:.0%} (first pilot {old["3-octanol"]["drop"]["4-methylcyclohexanol"]:.0%}) '
             f'and its spikes by {new["3-octanol"]["spikes"]["4-methylcyclohexanol"]["drop"]:.0%}; flies: charge not significantly changed, '
             "spikes about 25% lower")
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
