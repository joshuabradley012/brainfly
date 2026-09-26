"""The figure at the top of the README, made from one run of the model (nothing is drawn by hand).

    python assets/loom.py        # writes assets/loom-light.svg and assets/loom-dark.svg (~10 s)

8 flies (FlyBrain(batch=8), default settings) settle for 2 s, then 3 s are recorded. From 1 s to 2 s
the looming detectors of the fly's left eye (LC4 and LPLC2) get +DRIVE per step. The map is every
neuron with a known cell body position, seen from the front, so the fly's left is on the right.
Highlighted: the driven neurons, and every other neuron whose rate (mean over the 8 flies) rose by
at least RISE Hz during the drive. The raster is the giant fiber (DNp01) on each side, every fly.
"""
from __future__ import annotations

import base64
import struct
import zlib
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter

from brainfly import FlyBrain

OUT = Path(__file__).parent
FLIES, SETTLE, STEPS, ON, OFF, DRIVE, RISE, SEED = 8, 100, 150, 50, 100, 0.4, 5.0, 7
LOOP = 6.0  # seconds per animation loop: 3 s of brain time played in real time, then a 3 s hold
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # GitHub's own ink and surfaces, plus the brand red (the fly's eye pigment)
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", cloud=0.72, band=0.08),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", cloud=0.55, band=0.14),
}

# layout, in SVG user units
W, H = 1120, 600
MAP_X, MAP_Y, MAP_W = 8, 60, 640                # the brain
RAS_X0, RAS_X1, RAS_Y = 742, 1104, 132           # the raster
ROW, TICK, GAP = 11, 8, 64                       # raster row pitch, tick height, gap between the two fibers


def simulate() -> dict:
    brain = FlyBrain(batch=FLIES, seed=SEED)
    loom = brain.cells(["LC4", "LPLC2"], side="L")
    fiber = {s: brain.cells(["DNp01"], side=s) for s in "LR"}
    for _ in range(SETTLE):
        brain.step()
    spikes = np.zeros((2, brain.n))                    # before / during the drive, summed over flies
    raster = {s: np.zeros((FLIES, STEPS), bool) for s in "LR"}
    for t in range(STEPS):
        fired = brain.step(inject=[(loom, DRIVE)] if ON <= t < OFF else ())
        for f, idx in enumerate(fired):
            if t < OFF:
                spikes[int(t >= ON), idx] += 1         # idx has no repeats within one fly
            for s in "LR":
                raster[s][f, t] = np.isin(fiber[s], idx).any()
    rise = (spikes[1] - spikes[0]) / ((OFF - ON) * brain.dt * FLIES)
    followers = np.setdiff1d(np.flatnonzero(rise >= RISE), loom)
    hz = {s: {k: raster[s][:, a:b].mean() / brain.dt for k, (a, b) in (("before", (0, ON)), ("during", (ON, OFF)))}
          for s in "LR"}
    return dict(pos=brain.positions, loom=loom, followers=followers, fiber=fiber, raster=raster, hz=hz, dt=brain.dt)


def png(level: np.ndarray, color: str, levels: int) -> bytes:
    """8-bit palette PNG: pixel value i is `color` at opacity i / (levels - 1)."""
    h, w = level.shape
    rgb = bytes(int(color[i:i + 2], 16) for i in (1, 3, 5))
    raw = b"".join(b"\x00" + level[y].astype(np.uint8).tobytes() for y in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 3, 0, 0, 0))
            + chunk(b"PLTE", rgb * levels) + chunk(b"tRNS", bytes(round(255 * i / (levels - 1)) for i in range(levels)))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def cloud(px: np.ndarray, py: np.ndarray, w: int, h: int, color: str, alpha: float, scale: float = 1.6, levels: int = 24) -> str:
    """Every neuron as a soft speck, rendered at `scale`x and embedded as a PNG."""
    iw, ih = int(w * scale), int(h * scale)
    img = np.zeros((ih, iw), np.float32)
    xi = np.clip((px * scale).astype(int), 0, iw - 1)
    yi = np.clip((py * scale).astype(int), 0, ih - 1)
    np.add.at(img, (yi, xi), 1.0)
    img = gaussian_filter(img, 0.7)
    k = np.percentile(img[img > 0.05], 70)
    a = alpha * (1 - np.exp(-img / k))
    data = base64.b64encode(png(np.round(a * (levels - 1)), color, levels)).decode()
    return f'<image x="0" y="0" width="{w}" height="{h}" href="data:image/png;base64,{data}"/>'


def text(x, y, s, cls="", anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(run: dict, theme: str) -> str:
    c = THEMES[theme]
    pos = run["pos"]
    known = ~np.isnan(pos).any(1)
    x0, x1 = np.nanmin(pos[known, 0]), np.nanmax(pos[known, 0])
    y0, y1 = np.nanmin(pos[known, 1]), np.nanmax(pos[known, 1])
    s = MAP_W / (x1 - x0)
    map_h = int(np.ceil((y1 - y0) * s))
    to_map = lambda i: ((pos[i, 0] - x0) * s, (pos[i, 1] - y0) * s)
    px, py = to_map(np.flatnonzero(known))

    def dots(idx, r, fill):
        idx = idx[known[idx]]
        xs, ys = to_map(idx)
        return "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c["paper"]}" stroke-width="1.2"/>'
                       for x, y in zip(xs, ys))

    (glx, gly), (grx, gry) = (to_map(run["fiber"][k][0]) for k in "LR")
    n_known = int(known.sum())
    ras_w = RAS_X1 - RAS_X0
    step_w = ras_w / STEPS
    t_on, t_off = RAS_X0 + ON * step_w, RAS_X0 + OFF * step_w
    block_y = {"L": RAS_Y + 24, "R": RAS_Y + 24 + FLIES * ROW + GAP}
    ras_bottom = block_y["R"] + FLIES * ROW

    # --- the map
    g = [f'<g transform="translate({MAP_X} {MAP_Y})">', cloud(px, py, MAP_W, map_h, c["ink"], c["cloud"])]
    g.append(f'<g class="lit">{dots(run["followers"], 2.3, c["ink"])}{dots(run["loom"], 2.8, c["red"])}</g>')
    g.append(f'<circle cx="{grx:.1f}" cy="{gry:.1f}" r="6" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6"/>')
    g.append(f'<circle cx="{glx:.1f}" cy="{gly:.1f}" r="6" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.6"/>')
    g.append(f'<circle class="lit" cx="{glx:.1f}" cy="{gly:.1f}" r="4.4" fill="{c["ink"]}"/>')
    # leader lines up to the fiber labels
    top = -18
    g.append(f'<path d="M{grx:.1f} {gry - 7:.1f}V{top + 6}M{glx:.1f} {gly - 7:.1f}V{top + 6}" stroke="{c["muted"]}" stroke-width="1" fill="none"/>')
    g.append(text(grx - 8, top, "right giant fiber", "lab", "end"))
    g.append(text(glx + 8, top, "left giant fiber", "lab"))
    lx, ly = to_map(run["loom"][known[run["loom"]]])
    cx, cy = float(np.median(lx)), float(np.max(ly))
    g.append(f'<path d="M{cx:.1f} {cy + 6:.1f}V{map_h + 12}" stroke="{c["muted"]}" stroke-width="1" fill="none"/>')
    g.append(text(cx, map_h + 30, "looming detectors, left side", "lab", "middle"))
    g.append(text(0.14 * MAP_W, map_h - 40, "fly’s right", "note", "middle"))   # under each optic lobe
    g.append(text(0.86 * MAP_W, map_h - 40, "fly’s left", "note", "middle"))
    g.append("</g>")

    # --- the raster
    r = [f'<rect x="{t_on:.1f}" y="{RAS_Y - 8}" width="{t_off - t_on:.1f}" height="{ras_bottom - RAS_Y + 16}" fill="{c["red"]}" opacity="{c["band"]}"/>',
         text((t_on + t_off) / 2, RAS_Y - 18, "left looming detectors driven", "lab", "middle")]
    names = {"L": "Left giant fiber (DNp01)", "R": "Right giant fiber (DNp01)"}
    ticks = []
    for side in "LR":
        by = block_y[side]
        hz = run["hz"][side]["during"]
        r.append(text(RAS_X0, by - 10, names[side], "lab"))
        r.append(text(RAS_X1, by - 10, f"{hz:.0f} Hz" if hz >= 1 else f"{hz:.1f} Hz", "val", "end"))
        for f in range(FLIES):
            for t in np.flatnonzero(run["raster"][side][f]):
                ticks.append(f'M{RAS_X0 + (t + 0.5) * step_w:.1f} {by + f * ROW:.0f}v{TICK}')
    r.append(f'<clipPath id="sweep"><rect class="reveal" x="{RAS_X0 - 2}" y="{RAS_Y - 10}" width="{ras_w + 4}" height="{ras_bottom - RAS_Y + 20}"/></clipPath>')
    r.append(f'<path clip-path="url(#sweep)" d="{"".join(ticks)}" stroke="{c["ink"]}" stroke-width="{min(1.8, step_w * 0.7):.2f}"/>')
    for f in range(FLIES):  # faint row guides, so a silent fly still shows as a row
        for side in "LR":
            yy = block_y[side] + f * ROW + TICK / 2
            r.append(f'<path d="M{RAS_X0} {yy:.1f}H{RAS_X1}" stroke="{c["rule"]}" stroke-width="0.6" opacity="0.7"/>')
    ay = ras_bottom + 18
    r.append(f'<path d="M{RAS_X0} {ay}H{RAS_X1}" stroke="{c["muted"]}" stroke-width="1"/>')
    for sec in range(4):
        xx = RAS_X0 + sec / (STEPS * run["dt"]) * ras_w
        r.append(f'<path d="M{xx:.1f} {ay}v5" stroke="{c["muted"]}" stroke-width="1"/>')
        r.append(text(xx, ay + 22, f"{sec} s", "note", "middle"))
    r.append(text(RAS_X0, ay + 50, f"each row is one of {FLIES} simulated flies, each tick a spike", "note"))
    head = "".join(f"M{RAS_X0} {block_y[k] - 4}v{FLIES * ROW + 4}" for k in "LR")   # over the rows only, clear of the labels
    r.append(f'<path class="head" d="{head}" stroke="{c["ink"]}" stroke-width="1.5"/>')

    # --- legend under the map
    ly = MAP_Y + map_h + 68
    legend = [f'<circle cx="{MAP_X + 16}" cy="{ly - 5}" r="4.2" fill="{c["red"]}"/>',
              text(MAP_X + 28, ly, f"{len(run['loom'])} driven", "note"),
              f'<circle cx="{MAP_X + 136}" cy="{ly - 5}" r="3.6" fill="{c["ink"]}"/>',
              text(MAP_X + 148, ly, f"{len(run['followers'])} others speed up by {RISE:.0f} Hz or more", "note"),
              f'<circle cx="{MAP_X + 452}" cy="{ly - 5}" r="4.2" fill="{c["ink"]}" opacity="{c["cloud"] * 0.45:.2f}"/>',
              text(MAP_X + 464, ly, f"all {n_known:,} with a known position", "note")]

    loop = LOOP
    on_pct, off_pct = 100 * ON * run["dt"] / loop, 100 * STEPS * run["dt"] / loop
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 17px; fill: {c["ink"]}; }}
    .val {{ font-size: 17px; font-weight: 600; fill: {c["ink"]}; font-variant-numeric: tabular-nums; }}
    .note {{ font-size: 15px; fill: {c["muted"]}; }}
    .head {{ opacity: 0; }}
    @media (prefers-reduced-motion: no-preference) {{
      .reveal {{ transform-origin: {RAS_X0 - 2}px 0; animation: reveal {loop}s linear infinite; }}
      .head {{ animation: head {loop}s linear infinite; }}
      .lit {{ animation: lit {loop}s linear infinite; }}
    }}
    @keyframes reveal {{ 0% {{ transform: scaleX(0.001); }} {off_pct:.2f}%, 100% {{ transform: scaleX(1); }} }}
    @keyframes head {{ 0% {{ opacity: 1; transform: translateX(0); }} {off_pct:.2f}% {{ opacity: 1; transform: translateX({ras_w + 2}px); }}
                       {off_pct + 0.01:.2f}%, 100% {{ opacity: 0; transform: translateX({ras_w + 2}px); }} }}
    @keyframes lit {{ 0%, {on_pct:.2f}% {{ opacity: 0; }} {on_pct + 2:.2f}%, 96% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
    """
    title = ("Drive the looming detectors of the fly's left eye and the left giant fiber fires, "
             "in every one of 8 simulated flies, while the right one stays silent.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style>'
            + "".join(g) + "".join(r) + "".join(legend) + "</svg>")


if __name__ == "__main__":
    run = simulate()
    print(f"left giant fiber {run['hz']['L']['before']:.1f} -> {run['hz']['L']['during']:.1f} Hz, "
          f"right {run['hz']['R']['before']:.1f} -> {run['hz']['R']['during']:.1f} Hz, "
          f"{len(run['followers'])} neurons rose >= {RISE} Hz")
    for theme in THEMES:
        path = OUT / f"loom-{theme}.svg"
        path.write_text(figure(run, theme))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB)")
