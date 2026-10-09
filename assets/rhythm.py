"""The nerve cord figure in the README (rung 5), from rung5_vnc.py's results and two short runs.

    python assets/rhythm.py     # writes assets/rhythm-light.svg and assets/rhythm-dark.svg (~1 min)

rung5_vnc.py's model: Pugliese et al.'s rate model on brainfly's copy of the front legs' neuromere network. Left:
one replicate with the right DNg100 driven, the active leg motor neurons' rates over 0.3 s, each scaled to its own
peak and labelled by the muscle it drives. Middle: the same replicate's parameters in a degree-preserving rewiring of
the network. Right: every DNg100 replicate's frequency (rung5_vnc.json) against flies' stepping range.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import rung5_vnc as r5  # noqa: E402
import vnc_rhythm as v  # noqa: E402
from brainfly import nulls  # noqa: E402
from vnc_own import own_network  # noqa: E402

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/loom.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", band="#f3e1df"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", band="#3a2422"),
}
W, H = 1120, 560
WINDOW = (1.2, 1.5)                  # s of the 2-s drive shown
SEED_REPLICATE = 0


def runs() -> dict:
    table, _ = v.network()
    Wn, _ = own_network(table)
    types, inst = table["type"].astype(str).to_numpy(), table["instance"].astype(str).to_numpy()
    j = int(np.flatnonzero(inst == "DNg100_R")[0])
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    out = {}
    for name, net in (("real", Wn), ("rewired", nulls.degree_preserving(Wn, np.random.default_rng(r5.SEED + 1001)))):
        p = v.params(table, np.random.default_rng(r5.SEED + 1), 1)
        stim = np.zeros((len(table), 1))
        stim[j] = v.STIM
        rates = r5.simulate(net, p, stim, v.T)[:, :, 0]
        active = mn[rates[v.CLIP:, mn].max(0) > 0.01]
        out[name] = {"rates": rates[:, active], "modules": [str(m) if isinstance(m, str) else "" for m in table["motor module"].to_numpy()[active]],
                     "side": table["somaSide"].astype(str).to_numpy()[active].tolist()}
    return out


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def traces(r: dict, x0: float, y0: float, w: float, h: float, c: dict, limit: int = 12) -> list[str]:
    out = []
    rates, mods, sides = r["rates"], r["modules"], r["side"]
    a, b = (int(round(t / v.SAVE)) for t in WINDOW)
    order = np.argsort([m for m in mods], kind="stable")[:limit]
    n = max(len(order), 1)
    row = h / n
    for k, i in enumerate(order):
        x = rates[a:b, i]
        peak = max(float(rates[v.CLIP:, i].max()), 1e-9)
        ys = y0 + (k + 0.85) * row - 0.75 * row * x / peak
        xs = x0 + np.linspace(0, w, len(x))
        pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in zip(xs, ys))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{c["red"] if "swing" in mods[i] or "flex" in mods[i] else c["ink"]}" stroke-width="1.4"/>')
        out.append(text(x0 - 8, y0 + (k + 0.7) * row, f"{mods[i] or 'other'} ({sides[i]})", "lab", "end"))
    out.append(f'<line x1="{x0}" y1="{y0 + h + 6}" x2="{x0 + w * 0.1 / (WINDOW[1] - WINDOW[0])}" y2="{y0 + h + 6}" stroke="{c["ink"]}" stroke-width="2"/>')
    out.append(text(x0, y0 + h + 22, "100 ms", "lab"))
    return out


def figure(theme: str, data: dict, res: dict) -> str:
    c = THEMES[theme]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">',
           '<title id="t">Driving the descending neuron DNg100 makes the front legs\' motor neurons oscillate at walking frequency in '
           'brainfly\'s nerve cord; rewiring the network, at the same drive, abolishes the rhythm</title>',
           f'<style>text {{ font-family: {FONT}; }} .h {{ font-size: 17px; font-weight: 600; fill: {c["ink"]}; }} '
           f'.lab {{ font-size: 12px; fill: {c["muted"]}; }} .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}</style>',
           f'<rect width="{W}" height="{H}" fill="{c["paper"]}"/>']
    out.append(text(24, 34, "DNg100 driven: the front legs' motor neurons oscillate", "h"))
    out += traces(data["real"], 190, 60, 250, 400, c)
    out.append(text(640, 34, "rewired network", "h"))
    out += traces(data["rewired"], 640, 60, 170, 400, c, limit=12)
    # frequencies of every DNg100 replicate
    fx, fy, fw, fh = 880, 80, 210, 300
    freqs = [f for r in res["dng100"].values() for f in r["freq_hz"]]
    lo, hi = 5.0, 20.0
    X = lambda f: fx + (f - lo) / (hi - lo) * fw
    out.append(f'<rect x="{X(7):.1f}" y="{fy}" width="{X(15) - X(7):.1f}" height="{fh}" fill="{c["band"]}"/>')
    out.append(text(X(11), fy - 8, "flies step at 7-15 Hz", "lab", "middle"))
    hist, edges = np.histogram(freqs, bins=np.arange(lo, hi + 0.5, 0.5))
    top = max(int(hist.max()), 1)
    for n_, e in zip(hist, edges[:-1]):
        if n_:
            bh = fh * n_ / top
            out.append(f'<rect x="{X(e) + 0.5:.1f}" y="{fy + fh - bh:.1f}" width="{X(e + 0.5) - X(e) - 1:.1f}" height="{bh:.1f}" fill="{c["red"]}"/>')
    out.append(f'<line x1="{fx}" y1="{fy + fh}" x2="{fx + fw}" y2="{fy + fh}" stroke="{c["rule"]}"/>')
    for f in (5, 10, 15, 20):
        out.append(text(X(f), fy + fh + 16, f"{f}", "lab", "middle"))
    out.append(text(fx + fw / 2, fy + fh + 34, "rhythm frequency (Hz)", "lab", "middle"))
    n_rhythmic = sum(r["rhythmic"] for r in res["dng100"].values())
    n_all = sum(r["of"] for r in res["dng100"].values())
    nulls_rh = sum(e[k]["rhythmic"] for e in res.get("nulls", []) for k in res["dng100"])
    nulls_all = sum(e[k]["of"] for e in res.get("nulls", []) for k in res["dng100"])
    out.append(text(fx, fy + fh + 64, f"rhythmic: {n_rhythmic} of {n_all} replicates", "val"))
    if nulls_all:
        out.append(text(fx, fy + fh + 84, f"rewired: {nulls_rh} of {nulls_all}", "val"))
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    res = json.loads((ROOT / "experiments" / "rung5_vnc.json").read_text())
    data = runs()
    for theme in THEMES:
        (OUT / f"rhythm-{theme}.svg").write_text(figure(theme, data, res))
    print("wrote", [f"rhythm-{t}.svg" for t in THEMES])


if __name__ == "__main__":
    main()
