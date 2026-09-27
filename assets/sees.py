"""The resting-brain-escapes figure in the README, from saved results and one short run.

    python assets/sees.py       # writes assets/sees-light.svg and assets/sees-dark.svg (~2 min)

escape_at_rest2.py's model: rung 4's resting brain with short-term depression set by synapse class and
no synapses between visual projection neurons of the same type, given flyvis's eyes (model 001) and
recalibrated with the eyes open (experiments/escape_at_rest2/intact.npz). One fly settles for 1 s on a
grey screen, then a dark disk looms at its left eye (eyepath_native.py's fast loom, contact at 1.8 s),
at gain 1. Left: the brain seen from the front, every neuron that fires in a FRAME lit, with the left
eye's looming detectors (LC4, LPLC2) marked by how fast they fire and the left giant fiber flashing
when it spikes. Right: the disk, and LC4, LPLC2 and the giant fiber on the loomed side, mean of the 8
flies of escape_at_rest2.py's confirmation run (gain 1, seed 2; experiments/escape_at_rest2.json).
"""
from __future__ import annotations

import base64
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
THEMES = {  # as in assets/loom.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", cloud=0.5, spark=0.8,
                  sky="#eef1f4", disk="#1f2328"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", cloud=0.4, spark=0.85,
                 sky="#c9d1d9", disk="#0d1117"),
}
W, H = 1120, 600
MAP_X, MAP_Y, MAP_W = 16, 64, 600
T0, T1, FRAME = 1.2, 2.0, 0.08            # scene time shown, and frame length (10 frames, played in real time)
HOLD = 2.2                                 # seconds held after the loop's last frame
CONTACT, R_OVER_V, CAP = 1.8, 0.04, 45.0
TX0, TX1 = 790, 1090


def simulate() -> dict:
    import escape_at_rest as escape
    import escape_at_rest2 as escape2
    import eyes_at_rest as eyes
    import rest_calibration as attempt1
    import rest_calibration2 as attempt2
    from eyepath_fast import scenes

    attempt2.model, attempt1.network = escape.model, escape2.network
    eyes.TRIALS = 1
    s = eyes.Setup(None, seed=31)
    s.bias = np.load(ROOT / "experiments" / "escape_at_rest2" / "intact.npz")["bias"]
    b, ol = s.brain, s.ol
    b.set_bias(s.bias[s.gid])
    b.reset(8)
    ol.reset()
    ol.gain = 1.0
    per = int(round(eyes.OPTIC_DT / b.dt))
    for _ in range(int(round(1.0 / eyes.OPTIC_DT))):
        b.set_release(ol.neurons, 50.0 * ol.step(None))
        b.advance(per)
    scene = scenes()["fastL"]
    steps_frame = int(round(FRAME / eyes.OPTIC_DT))
    frames = []
    for k in range(int(round(T1 / eyes.OPTIC_DT))):
        t = k * eyes.OPTIC_DT
        b.set_release(ol.neurons, 50.0 * ol.step(ol.contrast(scene(t))))
        c = b.advance(per)[0]
        if t >= T0 - 1e-9:
            j = int((t - T0 + 1e-9) // FRAME)
            if j >= len(frames):
                frames.append(np.zeros(b.n))
            frames[j] += c
    cells = {name: s.cells[name] for name in ("LC4 L", "LPLC2 L", "DNp01 L")}
    return {"frames": np.stack(frames[:int(round((T1 - T0) / FRAME))]), "cells": cells, "external": b.external.copy()}


def radius_deg(t):
    return np.degrees(np.minimum(np.arctan(R_OVER_V / np.maximum(CONTACT - t, 1e-9)), np.radians(CAP)))


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
    out = [text(MAP_X + 8, MAP_Y - 34, "The resting brain sees a looming disk, and its escape neuron fires", "lab"),
           text(MAP_X + 8, MAP_Y - 14, "one fly: every neuron firing in each 80 ms lit; the left eye's looming detectors ringed", "note"),
           f'<g transform="translate({MAP_X} {MAP_Y})">', layer(px, py, MAP_W, map_h, np.ones(len(px)), c["ink"], c["cloud"], 0.7)]
    for f in range(nf):
        fired = run["frames"][f][known] > 0
        out.append(f'<g class="frame f{f}">' + layer(px[fired], py[fired], MAP_W, map_h, np.ones(fired.sum()), c["red"], c["spark"], 0.5))
        for name, r0 in (("LC4 L", 3.4), ("LPLC2 L", 3.4)):
            idx = run["cells"][name]
            idx = idx[known[idx]]
            xs, ys = to_map(idx)
            hz = run["frames"][f][idx] / FRAME
            for xx, yy, h in zip(xs, ys, hz):
                if h > 0:
                    out.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{r0 + min(h, 60) / 20:.1f}" fill="{c["red"]}" '
                               f'stroke="{c["paper"]}" stroke-width="0.8"/>')
        gf = run["cells"]["DNp01 L"][0]
        gx, gy = to_map(gf)
        if run["frames"][f][gf] > 0:
            out.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="9" fill="none" stroke="{c["red"]}" stroke-width="3"/>')
        out.append("</g>")
    gx, gy = to_map(run["cells"]["DNp01 L"][0])
    out.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6"/>')
    out.append(f'<path d="M{gx - 7:.1f} {gy:.1f}H{gx - 26:.1f}" stroke="{c["muted"]}" stroke-width="1"/>')
    out.append(text(gx - 30, gy + 4, "left giant fiber", "note", "end"))
    lx, ly = to_map(np.concatenate([run["cells"]["LC4 L"], run["cells"]["LPLC2 L"]]))
    out.append(f'<path d="M{np.max(lx) + 8:.1f} {np.min(ly) + 4:.1f}L{np.max(lx) + 30:.1f} {np.min(ly) - 22:.1f}" stroke="{c["muted"]}" stroke-width="1"/>')
    out.append(text(np.max(lx) + 34, np.min(ly) - 26, "left LC4 and LPLC2", "note", "start"))
    out.append(text(0.14 * MAP_W, map_h - 30, "fly’s right", "note", "middle"))
    out.append(text(0.86 * MAP_W, map_h - 30, "fly’s left", "note", "middle"))
    out.append("</g>")

    # --- the disk
    vx, vy, vs = 660, 64, 104
    cx, cy = vx + vs / 2, vy + vs / 2
    out.append(f'<rect x="{vx}" y="{vy}" width="{vs}" height="{vs}" rx="10" fill="{c["sky"]}" stroke="{c["rule"]}"/>')
    out.append(f'<clipPath id="v"><rect x="{vx}" y="{vy}" width="{vs}" height="{vs}" rx="10"/></clipPath>')
    out.append(f'<g clip-path="url(#v)"><circle class="disk" cx="{cx}" cy="{cy}" r="{vs / 2 - 3}" fill="{c["disk"]}" opacity="0.92"/></g>')
    out.append(text(vx, vy + vs + 20, "the left eye's view", "note"))

    # --- traces (8 flies, gain 1)
    tx = lambda t: TX0 + (TX1 - TX0) * (t - T0) / (T1 - T0)
    tb = (np.arange(len(traces["LC4 L"])) + 0.5) * 0.02
    keep = tb >= T0
    y = 76
    for name, label in (("LC4 L", "LC4, left"), ("LPLC2 L", "LPLC2, left"), ("DNp01 L", "giant fiber, left")):
        ymax = int(np.ceil(max(np.asarray(traces[name])[keep]) / 10) * 10)
        h = 96
        yv = lambda v: y + h - h * min(v, ymax) / ymax
        for v in (0, ymax):
            out.append(f'<path d="M{TX0} {yv(v):.1f}H{TX1}" stroke="{c["rule"]}"/>')
            out.append(text(TX0 - 6, yv(v) + 4, str(v), "tick", "end"))
        out.append(text(TX0, y - 8, label, "val"))
        pts = " ".join(f"{tx(t):.1f},{yv(v):.1f}" for t, v in zip(tb[keep], np.asarray(traces[name])[keep]))
        out.append(f'<polyline clip-path="url(#sweep)" points="{pts}" fill="none" stroke="{c["red"]}" stroke-width="2.2" stroke-linejoin="round"/>')
        y += h + 46
    bottom = y - 46
    out.append(f'<path d="M{tx(CONTACT):.1f} 70V{bottom}" stroke="{c["muted"]}" stroke-dasharray="2 3"/>')
    out.append(text(tx(CONTACT), bottom + 18, "contact", "note", "middle"))
    out.append(text(TX0, bottom + 18, f"{T0:g} s", "note", "middle"))
    out.append(text(TX1, bottom + 18, f"{T1:g} s", "note", "middle"))
    out.append(text(TX0 - 40, bottom + 40, "spikes per second, mean of 8 flies", "note"))
    out.append(f'<clipPath id="sweep"><rect class="reveal" x="{TX0}" y="60" width="{TX1 - TX0 + 2}" height="{bottom - 50}"/></clipPath>')
    out.append(f'<path class="head" d="M{TX0} 70V{bottom}" stroke="{c["ink"]}" stroke-width="1.3"/>')

    # animation: frames step in real time over T0..T1, then hold on the last
    play = T1 - T0
    loop = play + HOLD
    pct = lambda t: 100 * t / loop
    kf = []
    for f in range(nf):
        a, b = pct(f * FRAME), pct((f + 1) * FRAME)
        last = f == nf - 1
        kf.append(f".f{f} {{ animation: fr{f} {loop}s steps(1) infinite; }} @keyframes fr{f} {{ 0% {{ opacity: 0; }} "
                  f"{a:.3f}% {{ opacity: 1; }} {(pct(loop) - 0.01) if last else b:.3f}% {{ opacity: {1 if last else 0}; }} 100% {{ opacity: 0; }} }}")
    stops = np.linspace(T0, T1, 41)
    disk_kf = " ".join(f"{pct(t - T0):.2f}% {{ transform: scale({max(radius_deg(t) / CAP, 0.003):.4f}); }}" for t in stops)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .frame {{ opacity: 0; }} .f{nf - 1} {{ opacity: 1; }}
    .disk {{ transform-origin: {cx}px {cy}px; }}
    .head {{ opacity: 0; }}
    @media (prefers-reduced-motion: no-preference) {{
      .f{nf - 1} {{ opacity: 0; }}
      {" ".join(kf)}
      .disk {{ animation: disk {loop}s linear infinite; }}
      .reveal {{ transform-origin: {TX0}px 0; animation: reveal {loop}s linear infinite; }}
      .head {{ animation: head {loop}s linear infinite; }}
    }}
    @keyframes disk {{ {disk_kf} 100% {{ transform: scale(1); }} }}
    @keyframes reveal {{ 0% {{ transform: scaleX(0.001); }} {pct(play):.2f}%, 100% {{ transform: scaleX(1); }} }}
    @keyframes head {{ 0% {{ opacity: 1; transform: translateX(0); }} {pct(play):.2f}% {{ opacity: 1; transform: translateX({TX1 - TX0}px); }}
                       {pct(play) + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
    """
    title = ("The simulated fly brain at rest, with flyvis's eyes: a dark disk looms at the left eye, the left looming "
             "detectors LC4 and LPLC2 light up over the resting activity, and the left giant fiber fires")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    pos = np.load(Path.home() / "fly-data" / "brain.npz")["positions"]
    run = simulate()
    d = json.loads((ROOT / "experiments" / "escape_at_rest2.json").read_text())
    traces = d["confirm"]["trace_hz"]["fastL"]
    for theme in THEMES:
        path = OUT / f"sees-{theme}.svg"
        path.write_text(figure(theme, run, pos, traces))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
