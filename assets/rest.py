"""The resting-brain figure in the README (rung 4), made from saved results and one short run.

    python assets/rest.py       # writes assets/rest-light.svg and assets/rest-dark.svg (~1 min)

Left: the brain at rest, attempt 2's model (experiments/rest_calibration2.py) with its calibrated
biases (experiments/rest_calibration2/intact.npz). One fly settles for 2 s, then 1 s is recorded in
FRAME bins; each frame lights the neurons that fired in it, over every neuron with a known position,
seen from the front. Right, from the attempts' saved results: the measured types' resting rates
against their targets in attempts 1 and 2, and the flies' functional connectivity against the model's.
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
sys.path.insert(0, str(ROOT / "assets"))
from loom import png  # noqa: E402

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/loom.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", cloud=0.55, spark=0.95),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", cloud=0.42, spark=1.0),
}
W, H = 1120, 640
MAP_X, MAP_Y, MAP_W = 16, 70, 600
FRAME, FRAMES, SETTLE = 0.1, 10, 2.0           # 1 s of brain time, played in real time
SCALE = 0.95                                    # raster resolution of the map layers
MEASURED = ["MBON11", "MBON12", "MBON13", "MBON14", "MBON17", "MBON18", "PPL101", "PEN_a(PEN1)"]


def simulate() -> dict:
    import rest_calibration as attempt1
    import rest_calibration2 as attempt2
    from brainfly.hybrid import HybridBrain
    from shiu_rewiring import W_SYN

    M, scale, labels, types, superclass = attempt1.network()
    key = np.where(types != "", types, np.char.add("superclass:", superclass))
    names, gid = np.unique(key, return_inverse=True)
    saved = np.load(ROOT / "experiments" / "rest_calibration2" / "intact.npz")
    assert np.array_equal(saved["groups"], names)
    spec, sets = attempt2.model(types, superclass)
    brain = HybridBrain(trials=1, w_syn=W_SYN, matrix=M, scale=scale, labels=labels, seed=2026, types=spec, sets=sets,
                        bias=saved["bias"][gid])
    brain.advance(int(round(SETTLE / brain.dt)))
    frames = np.stack([brain.advance(int(round(FRAME / brain.dt)))[0] for _ in range(FRAMES)])
    return {"frames": frames, "mean_hz": float(frames.sum() / (brain.n * FRAMES * FRAME))}


def layer(px, py, w, h, weight, color, alpha, blur=0.6, levels=24) -> str:
    """Neurons as soft specks with the given weights, as an embedded palette PNG."""
    iw, ih = int(w * SCALE), int(h * SCALE)
    img = np.zeros((ih, iw), np.float32)
    np.add.at(img, (np.clip((py * SCALE).astype(int), 0, ih - 1), np.clip((px * SCALE).astype(int), 0, iw - 1)), weight)
    img = gaussian_filter(img, blur)
    k = np.percentile(img[img > 0.02], 75) if (img > 0.02).any() else 1.0
    a = alpha * (1 - np.exp(-img / k))
    data = base64.b64encode(png(np.round(a * (levels - 1)), color, levels)).decode()
    return f'<image x="0" y="0" width="{w}" height="{h}" href="data:image/png;base64,{data}"/>'


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def brain_map(c: dict, run: dict, pos: np.ndarray) -> tuple[list[str], float]:
    known = ~np.isnan(pos).any(1)
    x0, x1 = np.nanmin(pos[known, 0]), np.nanmax(pos[known, 0])
    y0, y1 = np.nanmin(pos[known, 1]), np.nanmax(pos[known, 1])
    s = MAP_W / (x1 - x0)
    map_h = (y1 - y0) * s
    px, py = (pos[known, 0] - x0) * s, (pos[known, 1] - y0) * s
    out = [f'<g transform="translate({MAP_X} {MAP_Y})">', layer(px, py, MAP_W, map_h, np.ones(len(px)), c["ink"], c["cloud"], 0.7)]
    for f in range(FRAMES):
        fired = run["frames"][f][known] > 0
        out.append(f'<g class="frame f{f}">' + layer(px[fired], py[fired], MAP_W, map_h, np.ones(fired.sum()), c["red"], c["spark"], 0.5)
                   + "</g>")
    out.append("</g>")
    return out, map_h


def figure(theme: str, run: dict, pos: np.ndarray, results: dict) -> str:
    c = THEMES[theme]
    out, map_h = brain_map(c, run, pos)
    out.insert(0, text(MAP_X + 8, MAP_Y - 30, "The brain at rest", "lab"))
    out.insert(1, text(MAP_X + 8, MAP_Y - 10, f"each red speck a neuron firing in that {FRAME * 1000:.0f} ms; "
                       f"mean {run['mean_hz']:.1f} Hz, 1 s of brain time per loop", "note"))
    # the frames cycle: each shows for one FRAME of the loop
    loop = FRAMES * FRAME
    kf = []
    for f in range(FRAMES):
        a, b = 100 * f / FRAMES, 100 * (f + 1) / FRAMES
        kf.append(f".f{f} {{ animation: fr{f} {loop}s steps(1) infinite; }} "
                  f"@keyframes fr{f} {{ 0% {{ opacity: {1 if f == 0 else 0}; }} {a:.3f}% {{ opacity: 1; }} {b:.3f}% {{ opacity: 0; }} 100% {{ opacity: {1 if f == 0 else 0}; }} }}")
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; font-variant-numeric: tabular-nums; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 12px; fill: {c["muted"]}; font-variant-numeric: tabular-nums; }}
    .frame {{ opacity: 0; }} .f0 {{ opacity: 1; }}
    @media (prefers-reduced-motion: no-preference) {{ {" ".join(kf)} }}
    """
    out += right_panels(c, results)
    title = "The simulated fly brain at rest, every neuron firing at its calibrated rate, and its resting activity against real flies'"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def right_panels(c: dict, results: dict) -> list[str]:
    out = []
    # --- measured types: target, attempt 1, attempt 2, on a log axis
    x0, x1, y0, row = 760, 1090, 84, 22
    lo, hi = 0.1, 100.0
    lx = lambda v: x0 + (x1 - x0) * (np.log10(max(v, lo)) - np.log10(lo)) / (np.log10(hi) - np.log10(lo))
    out.append(text(650, 40, "Resting rates of the types measured in real flies", "lab"))
    for v in (0.1, 1, 10, 100):
        out.append(f'<path d="M{lx(v):.1f} {y0 - 12}V{y0 + row * len(MEASURED) - 10}" stroke="{c["rule"]}"/>')
        out.append(text(lx(v), y0 + row * len(MEASURED) + 6, f"{v:g} Hz" if v >= 1 else "≤0.1", "tick", "middle"))
    a1, a2 = results.get("attempt1", {}), results.get("attempt2", {})
    for k, t in enumerate(MEASURED):
        y = y0 + k * row
        target = a1[t]["target_hz"]
        out.append(text(650, y + 4, t.replace("(PEN1)", ""), "note"))
        pts = [lx(target)] + [lx(a[t]["hz"]) for a in (a1, a2) if t in a]
        out.append(f'<path d="M{min(pts):.1f} {y}H{max(pts):.1f}" stroke="{c["rule"]}" stroke-width="2"/>')
        if t in a1:
            out.append(f'<circle cx="{lx(a1[t]["hz"]):.1f}" cy="{y}" r="5" fill="{c["muted"]}"/>')
        if t in a2:
            out.append(f'<circle cx="{lx(a2[t]["hz"]):.1f}" cy="{y}" r="5.5" fill="{c["red"]}"/>')
        out.append(f'<circle cx="{lx(target):.1f}" cy="{y}" r="8" fill="none" stroke="{c["ink"]}" stroke-width="1.6"/>')
    ly = y0 + row * len(MEASURED) + 30
    for k, (kind, name) in enumerate((("ring", "measured in flies"), ("a1", "attempt 1"), ("a2", "attempt 2"))):
        x = 650 + k * 150
        if kind == "ring":
            out.append(f'<circle cx="{x + 6}" cy="{ly - 4}" r="6" fill="none" stroke="{c["ink"]}" stroke-width="1.6"/>')
        else:
            out.append(f'<circle cx="{x + 6}" cy="{ly - 4}" r="5" fill="{c["muted"] if kind == "a1" else c["red"]}"/>')
        out.append(text(x + 18, ly, name, "note"))

    # --- functional connectivity: flies against the model
    if "data_fc" in results and "model_fc" in results:
        order = results["order"]
        cell, fy = 2.9, 392
        for j, (name, m, sub_) in enumerate((("Real flies (Turner et al.)", results["data_fc"], "20 flies"),
                                             ("Model, attempt 2", results["model_fc"], results["model_note"]))):
            fx = 650 + j * 228
            out.append(text(fx, fy - 26, name, "val"))
            out.append(text(fx, fy - 10, sub_, "note"))
            z = np.asarray(m, float)[np.ix_(order, order)]
            level = np.round(np.clip(np.nan_to_num(z, nan=0.0) / 1.2, 0, 1) * 23)
            data = base64.b64encode(png(level, c["red"], 24)).decode()
            side_px = cell * len(order)
            out.append(f'<image x="{fx}" y="{fy}" width="{side_px:.1f}" height="{side_px:.1f}" style="image-rendering: pixelated" '
                       f'preserveAspectRatio="none" href="data:image/png;base64,{data}"/>')
            out.append(f'<rect x="{fx}" y="{fy}" width="{side_px:.1f}" height="{side_px:.1f}" fill="none" stroke="{c["rule"]}"/>')
            for cut in results["cuts"]:                          # left | middle | right
                q = cut * cell
                out.append(f'<path d="M{fx + q:.1f} {fy}v{side_px:.1f}M{fx} {fy + q:.1f}h{side_px:.1f}" stroke="{c["muted"]}" '
                           f'stroke-width="0.8" opacity="0.6"/>')
        for k, line in enumerate(results["fc_lines"]):
            out.append(text(650, fy + cell * len(order) + 22 + 18 * k, line, "note"))
        out.append(text(650, 330, "Resting functional connectivity, 66 regions", "lab"))
    return out


def load_results() -> dict:
    from brainfly import imaging

    exp = ROOT / "experiments"
    out = {"attempt1": json.loads((exp / "rest_calibration" / "intact.json").read_text())["measured_types"]}
    a2 = exp / "rest_calibration2" / "intact.json"
    if a2.exists():
        d = json.loads(a2.read_text())
        out["attempt2"] = d["measured_types"]
        data_fc, _ = imaging.connectivity(imaging.rest_signals(imaging.turner()))
        regions = imaging.REGIONS
        side = lambda r: 0 if r.endswith("_L") else (2 if r.endswith("_R") else 1)
        out["order"] = sorted(range(len(regions)), key=lambda i: (side(regions[i]), regions[i].rsplit("_", 1)[0]))
        sides = [side(regions[i]) for i in out["order"]]
        out["cuts"] = [sides.index(1), sides.index(2)]
        out["data_fc"], out["model_fc"] = data_fc, d["fc"]
        out["model_note"] = f"r = {d['r']} with the flies"
        report = exp / "rest_calibration2.json"
        rivals = json.loads(report.read_text())["rivals"] if report.exists() else {"independent": d["r_independent"]}
        rew = [v for k, v in rivals.items() if k.startswith("rewired")]
        out["fc_lines"] = [f"left, middle, right regions in each; r with the flies: model {d['r']:.2f},",
                           f"its neurons firing independently {rivals['independent']:.2f}, rewired networks "
                           + " and ".join(f"{v:.2f}" for v in rew)]
    return out


def main() -> None:
    pos = np.load(Path.home() / "fly-data" / "brain.npz")["positions"]
    run = simulate()
    results = load_results()
    for theme in THEMES:
        path = OUT / f"rest-{theme}.svg"
        path.write_text(figure(theme, run, pos, results))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB); mean {run['mean_hz']:.2f} Hz")


if __name__ == "__main__":
    main()
