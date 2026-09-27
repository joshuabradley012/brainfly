"""The resting-brain-tastes figure in the README, from two short runs.

    python assets/tastes.py       # writes assets/tastes-light.svg and assets/tastes-dark.svg (~3 min)

taste_escape.py's model: the resting brain that escapes (escape_at_rest2.py), with rung 1's sugar route keeping
rung 1's settings (its cholinergic neurons undepressed, its descending neurons at 2 Hz), calibrated
(experiments/taste_escape/intact.npz). Left: one fly at rest; after 0.5 s its left sugar-taste neurons are
driven at 100 Hz (rung 1's drive). Every neuron firing in each 80 ms frame is lit, with the sugar route's
neurons marked by how fast they fire and MN9, the proboscis motor neuron, ringed when it spikes. Right: the
mean of 8 flies in 20 ms bins for the second-order taste neurons (G2N-1, Zorro, Clavicle, FMIn), the premotor
loop (Roundup, Roundtree, Rounddown) and MN9 L, under sugar, sugar with bitter, and no drive.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
sys.path.insert(0, str(ROOT / "assets"))
from rest import layer, text  # noqa: E402

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/sees.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", cloud=0.5, spark=0.8),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", cloud=0.4, spark=0.85),
}
W, H = 1120, 600
MAP_X, MAP_Y, MAP_W = 16, 64, 600
ONSET, T1, FRAME, BIN = 0.5, 1.5, 0.1, 0.02        # drive onset and end of the shown stretch (s), frame, trace bin
MAP_FROM = 0.2                                     # the map's frames start here (s)
HOLD = 2.0
TX0, TX1 = 790, 1090
GROUPS = {"second-order taste neurons": ["GNG232", "GNG215", "ANXXX462a", "GNG197"],
          "premotor loop": ["GNG108", "GNG120", "DNge080"], "MN9, left": ["MN9"]}


def setup(trials: int):
    import escape_at_rest2 as escape2
    import eyes_at_rest as eyes
    import rest_calibration as attempt1
    import taste_escape as te

    attempt1.network = escape2.network
    eyes.TRIALS = trials
    s, _ = te.build(None, seed=31)
    s.bias = np.load(ROOT / "experiments" / "taste_escape" / "intact.npz")["bias"]
    s.brain.set_bias(s.bias[s.gid])
    return s


def simulate() -> tuple[dict, dict]:
    from shiu_baseline import SETS

    s = setup(8)
    b = s.brain
    sugar, bitter = b.cells(SETS["sugar"], "L"), b.cells(SETS["bitter"], "L")
    cells = {name: b.cells(v, "L") for name, v in GROUPS.items()}
    traces = {}
    for cond, drive in (("sugar", [(sugar, 100.0)]), ("sugar + bitter", [(sugar, 100.0), (bitter, 100.0)]), ("no drive", [])):
        b.reset(40)
        b.set_release(s.ol.neurons, s.silent)
        b.advance(int(round(1.0 / b.dt)))
        rows = []
        for k in range(int(round(T1 / BIN))):
            c = b.advance(int(round(BIN / b.dt)), drive=drive if k * BIN >= ONSET - 1e-9 else ())
            rows.append({name: float(c[:, idx].mean()) / BIN for name, idx in cells.items()})
        traces[cond] = {name: [r[name] for r in rows] for name in cells}
    # one fly for the map
    import taste_escape as te
    one = setup(1)
    ob = one.brain
    route = np.flatnonzero(te.sugar_route(*te.network_for(None)[:3]))           # the whole route, 343 neurons
    ob.reset(8)
    ob.set_release(one.ol.neurons, one.silent)
    ob.advance(int(round(1.0 / ob.dt)))
    ob.advance(int(round(MAP_FROM / ob.dt)))
    frames = []
    for f in range(int(round((T1 - MAP_FROM) / FRAME))):
        drive = [(ob.cells(SETS["sugar"], "L"), 100.0)] if MAP_FROM + f * FRAME >= ONSET - 1e-9 else ()
        frames.append(ob.advance(int(round(FRAME / ob.dt)), drive=drive)[0])
    run = {"frames": np.stack(frames), "route": route, "mn9": ob.cells(["MN9"], "L")[0],
           "sugar": ob.cells(SETS["sugar"], "L")}
    return run, traces


def figure(theme: str, run: dict, pos: np.ndarray, traces: dict) -> str:
    c = THEMES[theme]
    known = ~np.isnan(pos).any(1)
    x0, x1 = np.nanmin(pos[known, 0]), np.nanmax(pos[known, 0])
    y0, y1 = np.nanmin(pos[known, 1]), np.nanmax(pos[known, 1])
    s = MAP_W / (x1 - x0)
    map_h = (y1 - y0) * s
    to_map = lambda i: ((pos[i, 0] - x0) * s, (pos[i, 1] - y0) * s)
    px, py = to_map(np.flatnonzero(known))
    nf = len(run["frames"])
    out = [text(MAP_X + 8, MAP_Y - 34, "The resting brain tastes sugar, and bitter vetoes it", "lab"),
           text(MAP_X + 8, MAP_Y - 14, "one fly: every neuron firing in each 100 ms lit; sugar's route through the brain marked", "note"),
           f'<g transform="translate({MAP_X} {MAP_Y})">', layer(px, py, MAP_W, map_h, np.ones(len(px)), c["ink"], c["cloud"], 0.7)]
    route = np.array([i for i in run["route"] if known[i]], int)
    rx, ry = to_map(route) if len(route) else (np.array([]), np.array([]))
    for f in range(nf):
        fired = run["frames"][f][known] > 0
        out.append(f'<g class="frame f{f}">' + layer(px[fired], py[fired], MAP_W, map_h, np.ones(fired.sum()), c["red"], c["spark"], 0.5))
        hz = run["frames"][f][route] / FRAME if len(route) else np.array([])
        for xx, yy, h in zip(rx, ry, hz):
            if h > 0:
                out.append(f'<circle class="rt" cx="{xx:.0f}" cy="{yy:.0f}" r="{2.6 + min(h, 80) / 30:.1f}"/>')
        if run["frames"][f][run["mn9"]] > 0:
            mx, my = to_map(run["mn9"])
            out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="10" fill="none" stroke="{c["red"]}" stroke-width="3"/>')
        if MAP_FROM + f * FRAME >= ONSET - 1e-9:
            out.append(text(MAP_X + MAP_W - 30, 20, "sugar on", "val", "end"))
        out.append("</g>")
    mx, my = to_map(run["mn9"])
    out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6"/>')
    out.append(f'<path d="M{mx + 7:.1f} {my:.1f}H{mx + 30:.1f}" stroke="{c["muted"]}" stroke-width="1"/>')
    out.append(text(mx + 34, my + 4, "MN9 (proboscis)", "note halo", "start"))
    out.append(text(0.14 * MAP_W, map_h - 30, "fly’s right", "note", "middle"))
    out.append(text(0.86 * MAP_W, map_h - 30, "fly’s left", "note", "middle"))
    out.append("</g>")

    # traces
    tb = (np.arange(len(traces["sugar"]["MN9, left"])) + 0.5) * BIN
    tx = lambda t: TX0 + (TX1 - TX0) * t / T1
    styles = {"sugar": (c["red"], "2.4", ""), "sugar + bitter": (c["ink"], "1.8", ""), "no drive": (c["muted"], "1.4", "3 3")}
    y = 76
    for name in GROUPS:
        top = max(max(v[name]) for v in traces.values())
        ymax = int(np.ceil(top / 10) * 10) or 10
        h = 96
        yv = lambda v: y + h - h * min(v, ymax) / ymax
        for v in (0, ymax):
            out.append(f'<path d="M{TX0} {yv(v):.1f}H{TX1}" stroke="{c["rule"]}"/>')
            out.append(text(TX0 - 6, yv(v) + 4, str(v), "tick", "end"))
        out.append(text(TX0, y - 8, name, "val"))
        for cond, (col, wdt, dash) in styles.items():
            sm = np.convolve(traces[cond][name], np.ones(3) / 3, mode="same")
            pts = " ".join(f"{tx(t):.1f},{yv(v):.1f}" for t, v in zip(tb, sm))
            out.append(f'<polyline clip-path="url(#sweep)" points="{pts}" fill="none" stroke="{col}" stroke-width="{wdt}" '
                       f'stroke-dasharray="{dash}" stroke-linejoin="round"/>')
        y += h + 46
    bottom = y - 46
    out.append(f'<path d="M{tx(ONSET):.1f} 70V{bottom}" stroke="{c["muted"]}" stroke-dasharray="2 3"/>')
    out.append(text(tx(ONSET), bottom + 18, "taste on", "note", "middle"))
    out.append(text(TX0, bottom + 18, "0 s", "note", "middle"))
    out.append(text(TX1, bottom + 18, f"{T1:g} s", "note", "middle"))
    lx = TX0 - 40
    for k, (cond, (col, wdt, dash)) in enumerate(styles.items()):
        xx = lx + k * 118
        out.append(f'<path d="M{xx} {bottom + 40}h22" stroke="{col}" stroke-width="{wdt}" stroke-dasharray="{dash}"/>')
        out.append(text(xx + 28, bottom + 44, cond, "note"))
    out.append(text(lx, bottom + 66, "spikes per second, mean of 8 flies", "note"))
    out.append(f'<clipPath id="sweep"><rect class="reveal" x="{TX0}" y="60" width="{TX1 - TX0 + 2}" height="{bottom - 50}"/></clipPath>')
    out.append(f'<path class="head" d="M{TX0} 70V{bottom}" stroke="{c["ink"]}" stroke-width="1.3"/>')

    play = T1 - MAP_FROM
    loop = play + HOLD
    pct = lambda t: 100 * t / loop
    kf = []
    for f in range(nf):
        a, b2 = pct(f * FRAME), pct((f + 1) * FRAME)
        last = f == nf - 1
        kf.append(f".f{f} {{ animation: fr{f} {loop}s steps(1) infinite; }} @keyframes fr{f} {{ 0% {{ opacity: 0; }} "
                  f"{a:.3f}% {{ opacity: 1; }} {(pct(loop) - 0.01) if last else b2:.3f}% {{ opacity: {1 if last else 0}; }} 100% {{ opacity: 0; }} }}")
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .rt {{ fill: {c["red"]}; stroke: {c["paper"]}; stroke-width: 0.6; }}
    .halo {{ paint-order: stroke; stroke: {c["paper"]}; stroke-width: 4px; stroke-linejoin: round; font-weight: 600; fill: {c["ink"]}; }}
    .frame {{ opacity: 0; }} .f{nf - 1} {{ opacity: 1; }}
    .head {{ opacity: 0; }}
    @media (prefers-reduced-motion: no-preference) {{
      .f{nf - 1} {{ opacity: 0; }}
      {" ".join(kf)}
      .reveal {{ transform-origin: {TX0}px 0; animation: reveal {loop}s linear infinite; }}
      .head {{ animation: head {loop}s linear infinite; }}
    }}
    @keyframes reveal {{ 0% {{ transform: scaleX({MAP_FROM / T1:.4f}); }} {pct(play):.2f}%, 100% {{ transform: scaleX(1); }} }}
    @keyframes head {{ 0% {{ opacity: 1; transform: translateX({tx(MAP_FROM) - TX0:.1f}px); }} {pct(play):.2f}% {{ opacity: 1; transform: translateX({TX1 - TX0}px); }}
                       {pct(play) + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
    """
    title = ("The simulated fly brain at rest: sugar reaches the left taste neurons, a route of neurons through the "
             "subesophageal zone lights up and the proboscis motor neuron MN9 fires; with bitter added it stays quiet")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    pos = np.load(Path.home() / "fly-data" / "brain.npz")["positions"]
    run, traces = simulate()
    for theme in THEMES:
        path = OUT / f"tastes-{theme}.svg"
        path.write_text(figure(theme, run, pos, traces))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
