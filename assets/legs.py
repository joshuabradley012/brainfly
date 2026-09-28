"""The front-leg figure: NeuroMechFly's front legs moved by the nerve cord's DNg100 rhythm, from one replicate.

    python assets/legs.py       # writes assets/legs-light.svg and assets/legs-dark.svg (~30 s)

The replicate is experiments/vnc_legs.py's reference, the one in the README's rhythm figure: the right DNg100 driven
at 400 in brainfly's copy of Pugliese et al.'s front-leg network. brainfly.legs turns its leg motor neurons' rates
into joint torques, with the gain vnc_legs.json calibrated. The fly is tethered in the air by the thorax. Left, it is
seen from its left side; middle, from the front. Both views are drawn from the simulated body, as in assets/jump.py.
The front legs, which the motor neurons move, are red, and the other legs are held still. The thin red line is the
left foot's path over the whole window. The dashed line is a fly's recorded step (FlyGym's PreprogrammedSteps) around
the same thorax. Frames are 2 ms apart, over three cycles from 1.18 s after the drive starts, played 25 times
slower in a loop. Below: the left leg's active motor neurons, summed by module and scaled to their peaks, and its two moving
joints. Right: vnc_legs.json's numbers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.spatial import ConvexHull

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
sys.path.insert(0, str(ROOT / "assets"))
import rung5_vnc as r5  # noqa: E402
import vnc_rhythm as v  # noqa: E402
from jump import FONT, PARTS, STYLE, geometry, path, shapes  # noqa: E402
from rest import text  # noqa: E402

from brainfly import legs as L  # noqa: E402
from vnc_own import own_network  # noqa: E402

OUT = Path(__file__).parent
THEMES = {  # as in assets/jump.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff",
                  body="#eaeef2", eye="#8c959f", wing="#d1d9e0"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117",
                 body="#262c34", eye="#6e7681", wing="#3d444d"),
}
W, H = 1120, 660
START, CYCLES, FRAME_MS, SLOW = 1.2, 3, 2.0, 25.0    # s into the run (drive from 0.02 s), cycles, ms per frame, slowdown
S = 95.0                                             # px per mm
SIDE_X, FRONT_X, MID_Y = 150.0, 598.0, 245.0         # screen position of the thorax in each view
TX0, TX1, TY = 250.0, 1040.0, 474.0                  # timeline
# back to front, seen from the left side (camera at +y) and from the front (camera at +x)
SIDE_ORDER = ["rf", "rm", "rh", "r_eye", "r_wing", "abdomen", "thorax", "proboscis", "head", "l_eye", "l_wing", "lh", "lm", "lf"]
FRONT_ORDER = ["lh", "rh", "abdomen", "l_wing", "r_wing", "thorax", "lm", "rm", "proboscis", "head", "l_eye", "r_eye", "lf", "rf"]
FRONT = ("lf", "rf")
ROWS = [("coxa swing", "coxa swing: promotors"), ("coxa stance", "coxa stance: remotor"),
        ("femur/tr flex", "femur/tr flex: Tr flexors"), ("femur/tr extend", "femur/tr extend"),
        ("femur reductor", "femur reductor"), ("tibia flex", "tibia flex"), ("tibia extend", "tibia extend")]


def simulate() -> dict:
    """The reference replicate's rates and the tethered body under them, every body kept each ms."""
    res = json.loads((ROOT / "experiments" / "vnc_legs.json").read_text())
    table, _ = v.network()
    Wn, _ = own_network(table)
    j = int(np.flatnonzero(table["instance"].astype(str).to_numpy() == "DNg100_R")[0])
    mn = np.flatnonzero(table["class"].to_numpy() == "motor neuron")
    p = v.params(table, np.random.default_rng(r5.SEED + 1), 1)
    stim = np.zeros((len(table), 1))
    stim[j] = v.STIM
    rates = r5.simulate(Wn, p, stim, v.T)[:, mn, 0]
    cols = [table[k].to_numpy()[mn] for k in ("motor module", "type", "somaSide")]
    legs = L.Legs()
    rec = legs.run(L.torques(rates, v.SAVE, *cols, gain=res["calibration"]["gain"]), v.SAVE, bodies=True)
    return {"legs": legs, "rec": rec, "rates": rates, "cols": cols, "res": res}


def window(rec: dict, freq: float) -> tuple[int, int]:
    """Record indices of CYCLES cycles from START, the end nudged (±10 ms) to where the left leg best repeats the
    start, so the loop is seamless."""
    a = int(round(START / 1e-3))
    guess = a + int(round(CYCLES / freq / 1e-3))
    ends = np.arange(guess - 10, guess + 11)
    diff = [np.abs(rec["joints"][e, 0] - rec["joints"][a, 0]).sum() for e in ends]
    return a, int(ends[int(np.argmin(diff))])


def legs_svg(world: dict, order: list, project, names: set, cls: str) -> list[str]:
    out = []
    for name in order:
        if name not in names:
            continue
        pts = project(world[name])
        out.append(f'<path class="{cls} s1" d="{path(pts[:3], False)}"/><path class="{cls} s2" d="{path(pts[2:4], False)}"/>'
                   f'<path class="{cls} s3" d="{path(pts[3:], False)}"/>')
    return out


def static(world: dict, order: list, project, far: set) -> list[str]:
    """The body and the legs that don't move, in drawing order (the front legs are animated)."""
    out = []
    for name in order:
        if name in FRONT:
            continue
        pts = project(world[name])
        if name in PARTS:
            out.append(f'<path class="{STYLE[name]}" d="{path(pts[ConvexHull(pts).vertices], True)}"/>')
        else:
            tone = "of" if name in far else "o"
            out.append(f'<path class="{tone} s1" d="{path(pts[:3], False)}"/><path class="{tone} s2" d="{path(pts[2:4], False)}"/>'
                       f'<path class="{tone} s3" d="{path(pts[3:], False)}"/>')
    return out


def polyline(xs, ys, cls: str) -> str:
    return f'<polyline class="{cls}" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))}"/>'


def timeline(data: dict, a: int, b: int) -> tuple[list[str], tuple]:
    rec, rates = data["rec"], data["rates"]
    modules, _, sides = data["cols"]
    t = rec["t"][a:b + 1]
    X = lambda tt: TX0 + (TX1 - TX0) * (tt - t[0]) / (t[-1] - t[0])
    out = [text(24, TY - 26, "The left leg's motor neurons and joints", "val")]
    rows = []
    for module, label in ROWS:
        idx = [i for i in range(len(modules)) if modules[i] == module and sides[i] == "L" and rates[v.CLIP:, i].max() > 0.01]
        if idx:
            rows.append((f"{label} ({len(idx)})" if len(idx) > 1 else label, rates[a:b + 1, idx].sum(1), module))
    ctr, thc = L.JOINTS.index("CTr pitch"), L.JOINTS.index("ThC pitch")
    rows.append(("ThC pitch, forward up", -rec["joints"][a:b + 1, 0, thc], "angle"))
    rows.append(("CTr pitch, flexed up", -rec["joints"][a:b + 1, 0, ctr], "angle"))
    step = 30.0
    for k, (label, y, kind) in enumerate(rows):
        base = TY + k * step + 20
        out.append(text(TX0 - 12, base - 6, label, "note", "end"))
        lo, hi = float(y.min()), float(y.max())
        ys = base - 22 * (y - lo) / max(hi - lo, 1e-9)
        cls = "tr" if kind in ("coxa swing", "femur/tr flex", "tibia flex") else ("tm" if kind == "angle" else "ti")
        out.append(polyline(X(t)[::2], ys[::2], cls))
        scale = f"{hi - lo:.0f}°" if kind == "angle" else f"peak {hi:.0f} Hz"
        out.append(text(TX1 + 8, base - 6, scale, "tick"))
    bottom = TY + len(rows) * step + 4
    for ms in range(0, int(round((t[-1] - t[0]) * 1e3)) + 1, 50):
        out.append(text(X(t[0] + ms / 1e3), bottom + 14, f"{(t[0] - v.PULSE[0]) * 1e3 + ms:.0f} ms", "tick", "middle"))
    return out, (X, TY - 4, bottom)


def numbers(res: dict) -> list[str]:
    ref = res["runs"]["reference"]["body"]
    left, right = ref["L"], ref["R"]
    fly = res["recorded_step"]
    dn, rw = res["summary"]["DNg100"], res["summary"]["rewired"]
    freqs = [r["mn_freq_hz"] for r in dn if r["mn_freq_hz"]]
    loops = [r["loop_index"] for r in dn if r["loop_index"] is not None]
    thc, ctr = left["joints"]["ThC pitch"], left["joints"]["CTr pitch"]
    held = [r["active_mn"] for r in rw]
    feet = res["runs"]["standing"]["front_feet_on_ground"][0]
    flex = res["runs"]["reference"]["module_phase_deg"]["L"]["femur/tr flex"]
    items = [
        (f"The left leg swings at its motor neurons' {left['freq_hz']:.1f} Hz",
         f"so do 8 more replicates, at {min(freqs):.1f}–{max(freqs):.1f} Hz"),
        (f"ThC pitch {thc['pp']:.0f}°, CTr pitch {ctr['pp']:.0f}° peak to peak",
         f"one gain, fitted to a fly step's {fly['joints']['ThC pitch']['pp']:.0f}° and {fly['joints']['CTr pitch']['pp']:.0f}°"),
        (f"Held {abs(thc['mean'] - thc['rest']):.0f}° forward and {abs(ctr['mean'] - ctr['rest']):.0f}° flexed",
         "the motor neurons' rates have a large steady part"),
        (f"The foot runs along a line: loop index {left['foot']['loop_index']:.2f}",
         f"a fly's step {fly['foot']['loop_index']:.2f}; the 8 replicates at most {max(loops):.2f}"),
        ("Swing and stance muscles fire together",
         f"promotors, Tr flexors {abs(flex):.0f}° apart: both lift the foot"),
        ("No tibia or tarsus motor neuron is active", "those joints stay at rest"),
        (f"The right leg moves under {max(right['joints'][n]['pp'] for n in L.JOINTS):.0f}°",
         "each DNg100 drives the opposite leg alone"),
    ]
    x, y = 770, 100
    out = [text(x, y - 14, "Stepping or twitching?", "val")]
    for k, (head, sub) in enumerate(items):
        yy = y + 14 + 37 * k
        out += [text(x, yy, head, "val2"), text(x, yy + 17, sub, "note")]
    yy = y + 14 + 37 * len(items) + 6
    out += [text(x, yy, "Controls", "val"),
            text(x, yy + 18, "No drive: no motor neuron fires; legs still", "note"),
            text(x, yy + 35, f"Rewired: {min(held)}–{max(held)} motor neurons on, no rhythm;", "note"),
            text(x, yy + 52, "motors at their cap, legs held at extremes", "note"),
            text(x, yy + 69, f"Standing: the foot is off the ground {100 * (1 - feet):.0f}% of the time", "note")]
    return out


def figure(theme: str, data: dict) -> str:
    c = THEMES[theme]
    legs, rec, res = data["legs"], data["rec"], data["res"]
    parts, tips = geometry(SimpleNamespace(model=legs.model, _bodies=legs.bodies))
    freq = res["runs"]["reference"]["body"]["L"]["freq_hz"]
    a, b = window(rec, freq)
    th = rec["positions"][a, 0]
    side = lambda p: np.stack([SIDE_X - S * (p[:, 0] - th[0]), MID_Y - S * (p[:, 2] - th[2])], 1)
    front = lambda p: np.stack([FRONT_X + S * (p[:, 1] - th[1]), MID_Y - S * (p[:, 2] - th[2])], 1)
    world0 = shapes(rec, a, parts, tips)
    frames = list(range(a, b, int(round(FRAME_MS))))
    nf = len(frames)

    out = [text(24, 36, "The nerve cord's rhythm moves the front legs", "lab"),
           text(24, 56, "NeuroMechFly tethered in the air, its front legs pulled by the leg motor neurons of brainfly's nerve "
                f"cord with the right DNg100 driven; played {SLOW:.0f}× slower", "note"),
           text(40, 116, "after the drive starts", "note"),
           text(SIDE_X + 90, 404, "seen from its left side", "note", "middle"),
           text(FRONT_X, 404, "from the front", "note", "middle"),
           text(24, 428, "Thin red line: the left foot's path over these three cycles. Dashed: the foot in a fly's recorded step, "
                "around the same thorax.", "tick"),
           f'<path d="M40 384h{S:.0f}" stroke="{c["muted"]}" stroke-width="2"/>',
           text(40 + S / 2, 378, "1 mm", "tick", "middle")]
    for project in (side, front):
        top = project(np.array([[th[0], th[1], th[2] + 0.3]]))[0]
        out.append(f'<path d="M{top[0]:.1f} 132V{top[1]:.1f}" stroke="{c["muted"]}" stroke-width="3" stroke-linecap="round"/>')
    out.append(text(SIDE_X + 8, 142, "tether", "tick"))
    foot = legs.segments.index("lf_tarsus5")
    trail = rec["positions"][a:b + 1, foot]
    fly = np.array(res["recorded_step"]["foot_path"]) + th                 # tarsus5's origin, as the trail
    tl, (X, y0, y1) = timeline(data, a, b)
    out += numbers(res) + tl
    # the right front leg is behind the body in the side view; everything else animated is in front
    for f, i in enumerate(frames):
        out.append(f'<g class="frame f{f}">' + "".join(legs_svg(shapes(rec, i, parts, tips), SIDE_ORDER, side, {"rf"}, "df")) + "</g>")
    out += static(world0, SIDE_ORDER, side, {"rf", "rm", "rh"}) + static(world0, FRONT_ORDER, front, set())
    for project in (side, front):
        out.append(f'<path class="fly" d="{path(project(np.concatenate([fly, fly[:1]])), False)}"/>')
        out.append(f'<path class="trail" d="{path(project(trail), False)}"/>')
    for f, i in enumerate(frames):
        world = shapes(rec, i, parts, tips)
        out.append(f'<g class="frame f{f}">')
        out.append(text(40, 96, f"{(rec['t'][i] - v.PULSE[0]) * 1e3:.0f} ms", "big"))
        out += legs_svg(world, SIDE_ORDER, side, {"lf"}, "d") + legs_svg(world, FRONT_ORDER, front, set(FRONT), "d")
        out.append(f'<path d="M{X(rec["t"][i]):.1f} {y0}V{y1}" stroke="{c["ink"]}" stroke-width="1.3"/>')
        out.append("</g>")

    frame_s = FRAME_MS / 1e3 * SLOW
    loop = nf * frame_s
    pct = lambda s_: 100 * s_ / loop
    kf = []
    for f in range(nf):
        s0, s1 = pct(f * frame_s), pct((f + 1) * frame_s)
        start = "0% { opacity: 1; }" if f == 0 else f"0% {{ opacity: 0; }} {s0:.3f}% {{ opacity: 1; }}"
        end = "" if f == nf - 1 else f" {s1:.3f}% {{ opacity: 0; }}"
        kf.append(f".f{f} {{ animation: fr{f} {loop:.2f}s steps(1) infinite; }} @keyframes fr{f} {{ {start}{end} "
                  f"100% {{ opacity: {1 if f == nf - 1 else 0}; }} }}")
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .big {{ font-size: 22px; font-weight: 600; fill: {c["ink"]}; font-variant-numeric: tabular-nums; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .val2 {{ font-size: 13px; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .b {{ fill: {c["body"]}; stroke: {c["ink"]}; stroke-width: 1.1; stroke-linejoin: round; }}
    .e {{ fill: {c["eye"]}; stroke: {c["ink"]}; stroke-width: 1; }}
    .w {{ fill: {c["wing"]}; fill-opacity: 0.45; stroke: {c["muted"]}; stroke-width: 0.8; }}
    .d, .df, .o, .of {{ fill: none; stroke-linecap: round; stroke-linejoin: round; }}
    .d {{ stroke: {c["red"]}; }} .df {{ stroke: {c["red"]}; stroke-opacity: 0.45; }}
    .o {{ stroke: {c["muted"]}; }} .of {{ stroke: {c["muted"]}; stroke-opacity: 0.4; }}
    .s1 {{ stroke-width: 4; }} .s2 {{ stroke-width: 3; }} .s3 {{ stroke-width: 2; }}
    .trail {{ fill: none; stroke: {c["red"]}; stroke-width: 1; stroke-opacity: 0.7; }}
    .fly {{ fill: none; stroke: {c["muted"]}; stroke-width: 1.2; stroke-dasharray: 4 3; }}
    .tr, .ti, .tm {{ fill: none; stroke-width: 1.5; stroke-linejoin: round; }}
    .tr {{ stroke: {c["red"]}; }} .ti {{ stroke: {c["ink"]}; }} .tm {{ stroke: {c["muted"]}; }}
    .frame {{ opacity: 0; }} .f{nf - 1} {{ opacity: 1; }}
    @media (prefers-reduced-motion: no-preference) {{
      .f{nf - 1} {{ opacity: 0; }}
      {" ".join(kf)}
    }}
    """
    title = ("NeuroMechFly tethered in the air, its front legs moved by the leg motor neurons of brainfly's nerve cord "
             f"with DNg100 driven: the left front leg swings at the rhythm's {freq:.0f} Hz, but its foot runs up and down "
             "a line instead of stepping")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    data = simulate()
    for theme in THEMES:
        out = OUT / f"legs-{theme}.svg"
        out.write_text(figure(theme, data))
        print(f"{out} ({out.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
