"""The looming figure in the README, drawn from saved results (nothing is drawn by hand).

    python assets/looming.py     # writes assets/looming-light.svg and assets/looming-dark.svg

A dark disk looms at the fly's left eye (eyepath_native.py's fast loom: r/v 0.04 s, contact at 1.8 s,
radius capped at 45 deg). flyvis's optic lobe (FlyvisNative) sees it and drives the brain. The traces
are the rates of LC4, LPLC2 and the giant fiber (DNp01), mean of 6 flies in 20 ms bins, from the two
experiments' sweeps at the same gain (1) and seed: flyvis's model 000, whose T2 responds only to light
increments (experiments/eyepath_native.json), against model 001, whose T2 also responds to decrements
(experiments/eyepath_native_t2.json). The bars are T2's flash responses in each model
(experiments/flyvis_screen.json). Shown from 1 s, when the disk is 3 deg across, to 2 s; the disk grows and the
traces draw in real time, then hold.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/loom.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", sky="#eef1f4", disk="#1f2328"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", sky="#c9d1d9", disk="#0d1117"),
}
W, H = 1120, 620
SECONDS, CONTACT, R_OVER_V, CAP = 2.0, 1.8, 0.04, 45.0
T0 = 1.0                        # the traces start here; nothing happens before (see the JSON)
LOOP = 4.0                      # 1 s of fly time in real time, then a 3 s hold
GAIN = 1.0

# layout
VX, VY, VS = 40, 70, 236        # the fly's view: a square of the visual field
TX0, TX1 = 420, 1070            # traces
STRIP_Y, STRIP_H = 56, 30       # the disk's size over time
PANEL_Y0, PANEL_H, PANEL_GAP = 140, 104, 50
PANELS = [("LC4", "LC4", 30), ("LPLC2", "LPLC2", 30), ("DNp01", "giant fiber (DNp01)", 40)]


def radius_deg(t):
    return np.degrees(np.minimum(np.arctan(R_OVER_V / np.maximum(CONTACT - t, 1e-9)), np.radians(CAP)))


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, t000: dict, t001: dict, t2: dict) -> str:
    c = THEMES[theme]
    tx = lambda t: TX0 + (TX1 - TX0) * (t - T0) / (SECONDS - T0)
    bins = len(t001["fastL"]["LC4 L"])
    tb = (np.arange(bins) + 0.5) * SECONDS / bins
    out = []

    # --- the fly's view, with the disk (animated by scale)
    cx, cy = VX + VS / 2, VY + VS / 2
    px_per_deg = (VS / 2 - 6) / CAP
    out.append(f'<rect x="{VX}" y="{VY}" width="{VS}" height="{VS}" rx="14" fill="{c["sky"]}" stroke="{c["rule"]}"/>')
    out.append(f'<clipPath id="view"><rect x="{VX}" y="{VY}" width="{VS}" height="{VS}" rx="14"/></clipPath>')
    out.append(f'<g clip-path="url(#view)"><circle class="disk" cx="{cx}" cy="{cy}" r="{CAP * px_per_deg:.1f}" fill="{c["disk"]}" opacity="0.92"/></g>')
    out.append(text(VX, VY - 16, "What the left eye sees", "lab"))
    out.append(text(VX, VY + VS + 26, "a dark disk approaching at constant speed", "note"))
    out.append(text(VX, VY + VS + 46, "contact at 1.8 s; flyvis's optic lobe sees it", "note"))

    # --- T2's flash responses: the reason
    bx, by, bh = VX + 8, VY + VS + 118, 84
    out.append(text(VX, by - 24, "Why: T2's response to a flash", "lab"))
    top = max(max(v) for v in t2.values()) * 1.1
    for k, (model, (on, off)) in enumerate(t2.items()):
        gx = bx + k * 130
        for j, (val, col, name) in enumerate(((on, c["muted"], "on"), (off, c["red"], "off"))):
            h = bh * max(val, 0) / top
            out.append(f'<rect x="{gx + j * 34:.1f}" y="{by + bh - h:.1f}" width="28" height="{max(h, 1):.1f}" fill="{col}" rx="2"/>')
            out.append(text(gx + j * 34 + 14, by + bh + 16, name, "note", "middle"))
        out.append(text(gx + 31, by + bh + 36, f"model {model}", "val", "middle"))
    out.append(f'<path d="M{bx - 4} {by + bh}H{bx + 250}" stroke="{c["rule"]}"/>')
    out.append(text(VX, by + bh + 60, "light on / off: only model 001's T2 answers darkening", "note"))

    # --- the disk's size over time
    tt = np.linspace(T0, SECONDS, 200)
    rr = radius_deg(tt)
    pts = " ".join(f"{tx(a):.1f},{STRIP_Y + STRIP_H - STRIP_H * r / CAP:.1f}" for a, r in zip(tt, rr))
    out.append(f'<polygon points="{tx(T0):.1f},{STRIP_Y + STRIP_H} {pts} {tx(SECONDS):.1f},{STRIP_Y + STRIP_H}" fill="{c["ink"]}" opacity="0.22"/>')
    out.append(text(TX0, STRIP_Y - 10, "size of the disk (radius, up to 45°)", "note"))

    # --- traces
    names = {"000": "model 000: T2 answers light only", "001": "model 001: T2 also answers darkening"}
    y = PANEL_Y0
    for key, label, ymax in PANELS:
        a, b = y, y + PANEL_H
        yv = lambda v: b - PANEL_H * min(v, ymax) / ymax
        for v in (0, ymax // 2, ymax):
            out.append(f'<path d="M{TX0} {yv(v):.1f}H{TX1}" stroke="{c["rule"]}" stroke-width="1"/>')
            out.append(text(TX0 - 8, yv(v) + 4, str(v), "tick", "end"))
        out.append(text(TX0, a - 10, label, "lab"))
        lines = [(t001["fastL"][f"{key} R"], c["rule"], "1.4", ""), (t000["fastL"][f"{key} L"], c["muted"], "1.8", ' stroke-dasharray="5 4"'),
                 (t001["fastL"][f"{key} L"], c["red"], "2.4", "")]
        keep = tb >= T0 - 0.02
        for series, col, width, dash in lines:
            p = " ".join(f"{tx(t):.1f},{yv(v):.1f}" for t, v in zip(tb[keep], np.asarray(series)[keep]))
            out.append(f'<polyline clip-path="url(#sweep)" points="{p}" fill="none" stroke="{col}" stroke-width="{width}"{dash} stroke-linejoin="round"/>')
        peak = max(t001["fastL"][f"{key} L"])
        out.append(text(TX1, a - 10, f"peak {peak:.0f} Hz", "val", "end"))
        y = b + PANEL_GAP
    bottom = y - PANEL_GAP
    out.append(f'<path d="M{tx(CONTACT):.1f} {STRIP_Y - 4}V{bottom + 4}" stroke="{c["muted"]}" stroke-width="1" stroke-dasharray="2 3"/>')
    out.append(text(tx(CONTACT), bottom + 22, "contact", "note", "middle"))
    for sec in (1.0, 1.25, 1.5, 1.75, 2.0):
        out.append(f'<path d="M{tx(sec):.1f} {bottom}v5" stroke="{c["muted"]}"/>')
        if abs(sec - CONTACT) > 0.08:
            out.append(text(tx(sec), bottom + 22, f"{sec:g} s", "note", "middle"))
    out.append(f'<text x="{TX0 - 38}" y="{(PANEL_Y0 + bottom) / 2:.1f}" class="note" text-anchor="middle" '
               f'transform="rotate(-90 {TX0 - 38} {(PANEL_Y0 + bottom) / 2:.1f})">spikes per second, loomed side</text>')
    # the reveal and the playhead
    out.append(f'<clipPath id="sweep"><rect class="reveal" x="{TX0}" y="{STRIP_Y - 10}" width="{TX1 - TX0 + 2}" height="{bottom - STRIP_Y + 20}"/></clipPath>')
    out.append(f'<path class="head" d="M{TX0} {STRIP_Y}V{bottom}" stroke="{c["ink"]}" stroke-width="1.4"/>')

    # legend
    ly = bottom + 58
    items = [(c["red"], "", names["001"]), (c["muted"], ' stroke-dasharray="5 4"', names["000"]), (c["rule"], "", "the other side (001)")]
    x = TX0 - 30
    for col, dash, name in items:
        out.append(f'<path d="M{x} {ly - 5}h24" stroke="{col}" stroke-width="2.4"{dash}/>')
        out.append(text(x + 31, ly, name, "note"))
        x += 31 + 6.6 * len(name) + 22

    # animation: the disk's scale and the reveal follow the loom in real time, then hold
    stops = np.linspace(T0, SECONDS, 81)
    scale = radius_deg(stops) / CAP
    frac = lambda t: 100 * (t - T0) / LOOP
    disk_kf = " ".join(f"{frac(t):.2f}% {{ transform: scale({max(s, 0.002):.4f}); }}" for t, s in zip(stops, scale))
    end = frac(SECONDS)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 14px; font-weight: 600; fill: {c["ink"]}; font-variant-numeric: tabular-nums; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 12px; fill: {c["muted"]}; font-variant-numeric: tabular-nums; }}
    .disk {{ transform-origin: {cx}px {cy}px; }}
    .head {{ opacity: 0; }}
    @media (prefers-reduced-motion: no-preference) {{
      .disk {{ animation: disk {LOOP}s linear infinite; }}
      .reveal {{ transform-origin: {TX0}px 0; animation: reveal {LOOP}s linear infinite; }}
      .head {{ animation: head {LOOP}s linear infinite; }}
    }}
    @keyframes disk {{ {disk_kf} 100% {{ transform: scale(1); }} }}
    @keyframes reveal {{ 0% {{ transform: scaleX(0.001); }} {end:.2f}%, 100% {{ transform: scaleX(1); }} }}
    @keyframes head {{ 0% {{ opacity: 1; transform: translateX(0); }} {end:.2f}% {{ opacity: 1; transform: translateX({TX1 - TX0}px); }}
                       {end + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
    """
    title = ("A dark disk looms at the fly's left eye. With flyvis's model 001, whose T2 answers darkening, "
             "LC4, LPLC2 and the giant fiber on that side respond; with model 000, LC4 stays flat.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    at_gain = lambda d: next(g for g in d["sweep"] if g["gain"] == GAIN)["trace_hz"]
    t000 = at_gain(json.loads((ROOT / "experiments" / "eyepath_native.json").read_text()))
    t001 = at_gain(json.loads((ROOT / "experiments" / "eyepath_native_t2.json").read_text()))
    screen = {m["model"]: m for m in json.loads((ROOT / "experiments" / "flyvis_screen.json").read_text())["models"]}
    t2 = {name: (screen[f"flow/0000/{name}"]["t2_on"], screen[f"flow/0000/{name}"]["t2_off"]) for name in ("000", "001")}
    for theme in THEMES:
        path = OUT / f"looming-{theme}.svg"
        path.write_text(figure(theme, t000, t001, t2))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
