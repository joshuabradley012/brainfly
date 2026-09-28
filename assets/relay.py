"""The giant fiber relay figure in the README (rung 6), from experiments/rung6_relay.json.

    python assets/relay.py     # writes assets/relay-light.svg and assets/relay-dark.svg

Left: the predicted muscle latencies after a giant fiber spike (the model's motor neuron spike times plus the
literature's conduction and neuromuscular delays) against flies' measured ranges. Middle: how many spikes of 10-spike
giant fiber trains the jump (TTMn) and flight (DLMn) motor neurons follow at 100 and 250 Hz, intact and with the
electrical synapses removed (shakB-like), against flies. Right: the second of two giant fiber spikes answered, against
their interval, with flies' refractory periods.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/loom.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", band="#f3e1df"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", band="#3a2422"),
}
W, H = 1120, 350
FLY_LATENCY = {"jump muscle (TTM)": (0.8, 1.1), "flight muscle (DLM)": (1.3, 1.6)}          # ms, escape_circuit.md 2.1
FLY_FOLLOW = {("TTMn", 100): (1.0, 1.0), ("TTMn", 250): (0.88, 1.0), ("DLMn", 100): (0.84, 0.84), ("DLMn", 250): (0.28, 0.57)}
FLY_REFRACTORY = {"TTMn": 3.3, "DLMn": 5.2}                                                  # ms, Engel & Wu 1996


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, r: dict) -> str:
    c = THEMES[theme]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">',
           '<title id="t">The giant fiber relay in brainfly: muscle latencies, following at 100 and 250 Hz, and twin-pulse '
           'refractoriness, intact and without electrical synapses, against flies</title>',
           f'<style>text {{ font-family: {FONT}; }} .h {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }} '
           f'.lab {{ font-size: 12px; fill: {c["muted"]}; }} .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}</style>',
           f'<rect width="{W}" height="{H}" fill="{c["paper"]}"/>']
    # latencies
    x0, x1, y0 = 40, 330, 70
    out.append(text(x0, 36, "Latency after a giant fiber spike", "h"))
    X = lambda ms: x0 + 150 + (ms - 0.5) / (2.0 - 0.5) * (x1 - x0 - 150)
    single = r["intact"]["part_a"]["single"]
    model = {"jump muscle (TTM)": single["ttm_latency_ms_median"], "flight muscle (DLM)": single["dlm_latency_ms_median"]}
    for k, (name, (lo, hi)) in enumerate(FLY_LATENCY.items()):
        y = y0 + 40 + 60 * k
        out.append(f'<rect x="{X(lo):.1f}" y="{y - 10}" width="{X(hi) - X(lo):.1f}" height="20" fill="{c["band"]}"/>')
        out.append(f'<circle cx="{X(model[name]):.1f}" cy="{y}" r="5" fill="{c["red"]}"/>')
        out.append(text(x0 + 140, y + 4, name, "lab", "end"))
    for ms in (0.5, 1.0, 1.5, 2.0):
        out.append(text(X(ms), y0 + 170, f"{ms:g}", "lab", "middle"))
    out.append(text((X(0.5) + X(2.0)) / 2, y0 + 188, "ms (band: flies; dot: brainfly)", "lab", "middle"))
    shak = r["shakB"]["part_a"]["single"]
    out.append(text(x0, y0 + 230, f"Without electrical synapses: TTMn answer {shak['ttmn_answered']:.0%}, DLMn {shak['dlmn_answered']:.0%}", "val"))
    out.append(text(x0, y0 + 250, "of single giant fiber spikes (shakB² flies: 0-57% and none)", "lab"))
    # following
    fx, fw = 420, 330
    out.append(text(fx, 36, "Following 10-spike trains", "h"))
    groups = [("TTMn", 100), ("TTMn", 250), ("DLMn", 100), ("DLMn", 250)]
    bw, gap = 22, 18
    base, top = y0 + 200, y0 + 20
    Y = lambda f: base - (base - top) * f
    for k, (mn, hz) in enumerate(groups):
        gx = fx + 20 + k * (3 * bw + gap)
        lo, hi = FLY_FOLLOW[(mn, hz)]
        out.append(f'<rect x="{gx}" y="{Y(hi):.1f}" width="{bw}" height="{max(Y(lo) - Y(hi), 2):.1f}" fill="{c["band"]}" stroke="{c["red"]}" stroke-width="0.8"/>')
        for j, cond in enumerate(("intact", "shakB")):
            f = r[cond]["part_a"][f"train_{hz}hz"][f"{mn.lower()}_following"]
            out.append(f'<rect x="{gx + (j + 1) * bw:.1f}" y="{Y(f):.1f}" width="{bw - 3}" height="{max(base - Y(f), 1):.1f}" '
                       f'fill="{c["ink"] if cond == "intact" else c["muted"]}"/>')
        out.append(text(gx + 1.5 * bw, base + 16, f"{mn}", "lab", "middle"))
        out.append(text(gx + 1.5 * bw, base + 30, f"{hz} Hz", "lab", "middle"))
    out.append(f'<line x1="{fx}" y1="{base}" x2="{fx + fw}" y2="{base}" stroke="{c["rule"]}"/>')
    out.append(text(fx, base + 56, "each group: flies (band), brainfly intact (dark), without electrical synapses (grey)", "lab"))
    # twin pulses
    tx, tw = 800, 280
    out.append(text(tx, 36, "Second of two spikes answered", "h"))
    twin = r["intact"]["part_a"]["twin"]
    gaps = sorted(int(k[:-2]) for k in twin)
    T = lambda ms: tx + 20 + (ms - 1) / (11 - 1) * (tw - 30)
    for mn, dash, key in (("TTMn", "", "ttmn_second"), ("DLMn", ' stroke-dasharray="5 3"', "dlmn_second")):
        pts = " ".join(f"{T(g):.1f},{Y(twin[f'{g}ms'][key]):.1f}" for g in gaps)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c["ink"]}" stroke-width="1.8"{dash}/>')
        rf = FLY_REFRACTORY[mn]
        out.append(f'<line x1="{T(rf):.1f}" y1="{top}" x2="{T(rf):.1f}" y2="{base}" stroke="{c["red"]}" stroke-width="1.2"{dash}/>')
        out.append(text(T(rf) + 3, top + (12 if mn == "TTMn" else 28), f"flies' {mn[:-1]} {rf} ms", "lab"))
    for g in (2, 4, 6, 8, 10):
        out.append(text(T(g), base + 16, f"{g}", "lab", "middle"))
    out.append(f'<line x1="{tx}" y1="{base}" x2="{tx + tw}" y2="{base}" stroke="{c["rule"]}"/>')
    out.append(text(T(6), base + 32, "ms between spikes; solid TTMn, dashed DLMn", "lab", "middle"))
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    r = json.loads((ROOT / "experiments" / "rung6_relay.json").read_text())
    for theme in THEMES:
        (OUT / f"relay-{theme}.svg").write_text(figure(theme, r))
    print("wrote", [f"relay-{t}.svg" for t in THEMES])


if __name__ == "__main__":
    main()
