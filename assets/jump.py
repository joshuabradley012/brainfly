"""The escape-jump figure: NeuroMechFly jumping from one spike in each jump motor neuron, from one short run.

    python assets/jump.py       # writes assets/jump-light.svg and assets/jump-dark.svg (~15 s)

brainfly.jump with the jump muscle's strength calibrated by experiments/jump_calibration.py (tau_max from its
JSON, whose checks the right column lists). One spike in each TTMn, 0.4 ms after a giant fiber spike, time 0
here. Left, the fly seen from its right side; middle, from the front. Both are drawn from the simulated
body: convex outlines of the head, thorax, abdomen, eyes and wings, and the legs as lines through their
joints. The middle legs, which the jump muscles (TTM) extend, are red. One frame every 0.2 ms, played 600
times slower. Below, the timeline: the giant fiber and TTMn spikes, the TTM's activation and the scripted
tibia extension, the legs' contact with the ground, and takeoff.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import ConvexHull

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assets"))
from rest import text  # noqa: E402

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/compass.py, with the body's greys
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff",
                  body="#eaeef2", eye="#8c959f", wing="#d1d9e0"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117",
                 body="#262c34", eye="#6e7681", wing="#3d444d"),
}
W, H = 1120, 676
FRAME_MS, FRAME_S, HOLD = 0.2, 0.12, 1.8          # fly time per frame, seconds per frame, pause at the end
T_FROM, T_TO = -0.4, 10.0                          # ms after the giant fiber spike
S = 72.0                                           # px per mm
GROUND = 468.0
SIDE_X, FRONT_X = 290.0, 590.0                     # screen x of the thorax at rest in each view
TX0, TX1, TY = 170.0, 1090.0, 552.0                # timeline
LEGS = ["lf", "lm", "lh", "rf", "rm", "rh"]
PARTS = {  # outline: geoms (named by body) drawn as one convex shape
    "abdomen": ["c_abdomen12", "c_abdomen3", "c_abdomen4", "c_abdomen5", "c_abdomen6"],
    "thorax": ["c_thorax"], "head": ["c_head"], "proboscis": ["c_rostrum", "c_haustellum"],
    "l_eye": ["l_eye"], "r_eye": ["r_eye"], "l_wing": ["l_wing"], "r_wing": ["r_wing"],
}
STYLE = {"abdomen": "b", "thorax": "b", "head": "b", "proboscis": "b", "l_eye": "e", "r_eye": "e", "l_wing": "w", "r_wing": "w"}
# back to front, seen from the right side (camera at -y) and from the front (camera at +x)
SIDE_ORDER = ["lf", "lm", "lh", "l_eye", "l_wing", "abdomen", "thorax", "proboscis", "head", "r_eye", "r_wing", "rh", "rm", "rf"]
FRONT_ORDER = ["lh", "rh", "abdomen", "l_wing", "r_wing", "thorax", "lm", "rm", "proboscis", "head", "l_eye", "r_eye", "lf", "rf"]


def simulate() -> tuple:
    from brainfly.jump import GF_TO_TTMN, Jump

    cal = json.loads((ROOT / "experiments" / "jump_calibration.json").read_text())
    jump = Jump()
    rec = jump.run({"L": [0.0], "R": [0.0]}, seconds=(T_TO + 0.2) * 1e-3 - GF_TO_TTMN, tau_max=cal["calibration"]["tau_max"])
    return jump, rec, cal, GF_TO_TTMN * 1e3


def geometry(jump) -> tuple[dict, dict]:
    """Each part's mesh vertices in its bodies' frames, and each leg's tarsus tip in its tarsus5's frame."""
    import mujoco as mj
    m = jump.model
    body_of = {int(b): i for i, b in enumerate(jump._bodies)}

    def verts(g):
        mesh = m.geom_dataid[g]
        v = m.mesh_vert[m.mesh_vertadr[mesh]:m.mesh_vertadr[mesh] + m.mesh_vertnum[mesh]]
        R = np.zeros(9)
        mj.mju_quat2Mat(R, m.geom_quat[g])
        return v[::2] @ R.reshape(3, 3).T + m.geom_pos[g]

    geoms = {mj.mj_id2name(m, mj.mjtObj.mjOBJ_GEOM, g).split("/")[-1]: g for g in range(m.ngeom)
             if m.geom_type[g] == mj.mjtGeom.mjGEOM_MESH}
    parts = {p: [(body_of[int(m.geom_bodyid[geoms[n]])], verts(geoms[n])) for n in names] for p, names in PARTS.items()}
    tips = {}
    for leg in LEGS:
        v = verts(geoms[f"{leg}_tarsus5"])
        tips[leg] = v[np.argmax(np.linalg.norm(v, axis=1))]
    return parts, tips


def shapes(rec: dict, i: int, parts: dict, tips: dict) -> dict:
    """World coordinates at record index i: outline points per part, and the joint chain of each leg."""
    P, R, segs = rec["positions"][i], rec["rotations"][i], rec["segments"]
    out = {p: np.concatenate([P[b] + v @ R[b].T for b, v in pieces]) for p, pieces in parts.items()}
    for leg in LEGS:
        chain = [P[segs.index(f"{leg}_{s}")] for s in ("coxa", "trochanterfemur", "tibia", "tarsus1", "tarsus5")]
        t5 = segs.index(f"{leg}_tarsus5")
        out[leg] = np.array(chain + [P[t5] + R[t5] @ tips[leg]])
    return out


def path(points: np.ndarray, closed: bool) -> str:
    keep = [points[0]]
    for p in points[1:]:
        if np.hypot(*(p - keep[-1])) > 1.2:
            keep.append(p)
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in keep) + ("Z" if closed else "")


def draw(world: dict, order: list, project, far: set) -> list[str]:
    out = []
    for name in order:
        pts = project(world[name])
        if name in PARTS:
            out.append(f'<path class="{STYLE[name]}" d="{path(pts[ConvexHull(pts).vertices], True)}"/>')
            continue
        tone = ("m" if name[1] == "m" else "o") + ("f" if name in far else "")
        out.append(f'<path class="{tone} s1" d="{path(pts[:3], False)}"/><path class="{tone} s2" d="{path(pts[2:4], False)}"/>'
                   f'<path class="{tone} s3" d="{path(pts[3:], False)}"/>')
    return out


def tx(t_ms: float) -> float:
    return TX0 + (TX1 - TX0) * (t_ms - T_FROM) / (T_TO - T_FROM)


def ms(t: float) -> str:
    return f"{t:.1f}".replace("-", "−") + " ms"


def timeline(rec: dict, c: dict, shift: float) -> list[str]:
    """The static rows; `shift` (ms) turns the record's time into time after the giant fiber spike."""
    s = rec["summary"]
    t = rec["t"] * 1e3 + shift
    out = [text(24, TY - 30, "Timeline", "val")]
    rows = {"giant fiber spike": TY - 6, "TTMn spikes (L, R)": TY + 16, "TTM activation": TY + 42, "on the ground": TY + 78}
    for label, y in rows.items():
        out.append(text(24, y + 4, label, "note"))
    out.append(f'<path d="M{tx(0):.1f} {rows["giant fiber spike"] - 8}v16" stroke="{c["ink"]}" stroke-width="2"/>')
    t_ttmn = min(v[0] for v in rec["spikes"].values() if v) * 1e3 + shift
    out.append(f'<path d="M{tx(t_ttmn):.1f} {rows["TTMn spikes (L, R)"] - 8}v16" stroke="{c["red"]}" stroke-width="2"/>')
    base, height = rows["TTM activation"] + 10, 24
    keep = (t >= T_FROM) & (t <= T_TO)
    curve = lambda v: " ".join(f"{tx(a):.1f},{base - height * b:.1f}" for a, b in zip(t[keep][::2], v[keep][::2]))
    ttm, tibia = curve(rec["activation"][:, 0]), curve(-rec["torque"][:, 2] / rec["params"]["tau_max"])
    out.append(f'<polygon points="{tx(t[keep][0]):.1f},{base} {ttm} {tx(t[keep][::2][-1]):.1f},{base}" fill="{c["red"]}" fill-opacity="0.16"/>')
    out.append(f'<polyline points="{ttm}" fill="none" stroke="{c["red"]}" stroke-width="1.6"/>')
    out.append(f'<polyline points="{tibia}" fill="none" stroke="{c["muted"]}" stroke-width="1.3" stroke-dasharray="4 3"/>')
    out.append(text(24, rows["TTM activation"] + 18, "dashed: tibia, scripted", "tick"))
    y0 = rows["on the ground"] - 8
    off = lambda k: s["legs_off_ms"][k] + shift
    groups = (("middle legs", [1, 4], c["red"], 3.0, y0), ("front and hind legs", [0, 2, 3, 5], c["muted"], 1.8, y0 + 11))
    for label, legs, color, width, y in groups:
        for n, k in enumerate(legs):
            out.append(f'<path d="M{tx(T_FROM):.1f} {y + 3.5 * n:.1f}H{tx(off(k)):.1f}" stroke="{color}" stroke-width="{width}"/>')
        out.append(text(tx(max(off(k) for k in legs)) + 6, y + 4 + 1.75 * (len(legs) - 1), label, "tick"))
    to = s["takeoff_after_gf_ms"]
    out.append(f'<path d="M{tx(to):.1f} {TY - 18}V{y0 + 34}" stroke="{c["ink"]}" stroke-width="1" stroke-dasharray="3 3"/>')
    out.append(text(tx(to) + 5, TY - 8, f"takeoff, {ms(to)}", "tick"))
    for v in range(0, int(T_TO) + 1, 2):
        out.append(text(tx(v), TY + 112, f"{v} ms", "tick", "middle"))
    return out


def checks(cal: dict) -> list[str]:
    ch, b, one = cal["checks"], cal["bilateral"], cal["unilateral"]["L"]
    mark = lambda k: "✓" if ch[k]["pass"] else "✗"
    pitch = b["pitch_at_takeoff_deg"]
    items = [
        ("", f"Launch speed {b['launch_speed_m_s']:.2f} m/s", "fitted to flies' 0.48 m/s: TTM torque "
         f"{cal['calibration']['tau_max']:.0f} µN·mm"),
        (mark("extension_ms"), f"Leg extension {b['extension_ms']:.1f} ms", "flies 3.3 ms (accept 2–5)"),
        (mark("takeoff_after_gf_ms"), f"Takeoff {b['takeoff_after_gf_ms']:.1f} ms after the GF spike", "flies about 7 ms (accept 5–10)"),
        (mark("launch_angle_deg"), f"Launch angle {b['launch_angle_deg']:.0f}°, backward", "flies about 45° (accept 30–60°)"),
        (mark("pitch_at_takeoff_deg"), f"Pitch at takeoff {abs(pitch):.0f}° head-{'down' if pitch < 0 else 'up'}",
         "flies pitch head-up (39 of 43)"),
        (mark("peak_vertical_acceleration_m_s2"), f"Peak acceleration {b['peak_vertical_acceleration_m_s2']:.0f} m/s² up, "
         f"{b['peak_horizontal_acceleration_m_s2']:.0f} across", "flies about 110 m/s² each (accept 60–160)"),
    ]
    x, y = 770, 104
    out = [text(x, y - 14, "Calibrated once, then checked", "val")]
    for k, (m, head, sub) in enumerate(items):
        yy = y + 16 + 42 * k
        out += [text(x, yy, m, "mark"), text(x + 20, yy, head, "val2"), text(x + 20, yy + 17, sub, "note")]
    yy = y + 16 + 42 * len(items) + 10
    out += [text(x, yy, "One TTMn alone (a loom on one side):", "val2"),
            text(x, yy + 17, f"takes off at {one['launch_speed_m_s']:.1f} m/s, {one['takeoff_after_gf_ms']:.1f} ms after", "note"),
            text(x, yy + 34, f"the GF spike, rolling over sideways ({one['roll_rate_at_takeoff_deg_s'] / 1e3:.0f}°/ms)", "note")]
    return out


def figure(theme: str, rec: dict, cal: dict, parts: dict, tips: dict, shift: float) -> str:
    c = THEMES[theme]
    x_rest = float(rec["thorax"][0, 0])
    side = lambda p: np.stack([SIDE_X + S * (p[:, 0] - x_rest), GROUND - S * p[:, 2]], 1)
    front = lambda p: np.stack([FRONT_X + S * p[:, 1], GROUND - S * p[:, 2]], 1)
    times = np.arange(T_FROM, T_TO + 1e-9, FRAME_MS)
    nf, dt_ms = len(times), (rec["t"][1] - rec["t"][0]) * 1e3
    out = [text(24, 36, "The escape jump, from one spike in each jump motor neuron", "lab"),
           text(24, 56, "NeuroMechFly in FlyGym: the TTM twitch extends the middle legs (red); the tibia extension "
                "is scripted; the wings don't move", "note"),
           text(40, 100, "after the giant fiber spike", "note"),
           text(SIDE_X - 70, GROUND + 22, "seen from its right side", "note", "middle"),
           text(FRONT_X, GROUND + 22, "from the front", "note", "middle"),
           f'<path d="M24 {GROUND}H740" stroke="{c["muted"]}" stroke-width="1.2"/>',
           f'<path d="M{SIDE_X + 88} {GROUND - 14}h{S:.0f}" stroke="{c["muted"]}" stroke-width="2"/>',
           text(SIDE_X + 88 + S / 2, GROUND - 20, "1 mm", "tick", "middle")]
    out += checks(cal) + timeline(rec, c, shift)
    for f, tm in enumerate(times):
        world = shapes(rec, int(np.clip(round((tm - shift) / dt_ms), 0, len(rec["t"]) - 1)), parts, tips)
        out.append(f'<g class="frame f{f}">')
        out.append(text(40, 80, ms(tm), "big"))
        out += draw(world, SIDE_ORDER, side, {"lf", "lm", "lh"}) + draw(world, FRONT_ORDER, front, set())
        out.append(f'<path d="M{tx(tm):.1f} {TY - 18}V{TY + 98}" stroke="{c["ink"]}" stroke-width="1.3"/>')
        out.append("</g>")

    loop = nf * FRAME_S + HOLD
    pct = lambda s_: 100 * s_ / loop
    kf = []
    for f in range(nf):
        s0, s1 = pct(f * FRAME_S), pct((f + 1) * FRAME_S)
        last = f == nf - 1
        start = "0% { opacity: 1; }" if f == 0 else f"0% {{ opacity: 0; }} {s0:.3f}% {{ opacity: 1; }}"
        kf.append(f".f{f} {{ animation: fr{f} {loop:.2f}s steps(1) infinite; }} @keyframes fr{f} {{ {start} "
                  f"{(100 - 0.01) if last else s1:.3f}% {{ opacity: {1 if last else 0}; }} 100% {{ opacity: {1 if f == 0 else 0}; }} }}")
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .big {{ font-size: 22px; font-weight: 600; fill: {c["ink"]}; font-variant-numeric: tabular-nums; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .val2 {{ font-size: 13px; fill: {c["ink"]}; }}
    .mark {{ font-size: 14px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .b {{ fill: {c["body"]}; stroke: {c["ink"]}; stroke-width: 1.1; stroke-linejoin: round; }}
    .e {{ fill: {c["eye"]}; stroke: {c["ink"]}; stroke-width: 1; }}
    .w {{ fill: {c["wing"]}; fill-opacity: 0.45; stroke: {c["muted"]}; stroke-width: 0.8; }}
    .m, .mf, .o, .of {{ fill: none; stroke-linecap: round; stroke-linejoin: round; }}
    .m {{ stroke: {c["red"]}; }} .mf {{ stroke: {c["red"]}; stroke-opacity: 0.45; }}
    .o {{ stroke: {c["muted"]}; }} .of {{ stroke: {c["muted"]}; stroke-opacity: 0.4; }}
    .s1 {{ stroke-width: 3.2; }} .s2 {{ stroke-width: 2.4; }} .s3 {{ stroke-width: 1.6; }}
    .frame {{ opacity: 0; }} .f{nf - 1} {{ opacity: 1; }}
    @media (prefers-reduced-motion: no-preference) {{
      .f{nf - 1} {{ opacity: 0; }}
      {" ".join(kf)}
    }}
    """
    title = ("NeuroMechFly's escape jump from one spike in each jump motor neuron: the jump muscles' twitch extends the "
             "middle legs and the fly leaves the ground about 6 ms after the giant fiber spike")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    jump, rec, cal, shift = simulate()
    parts, tips = geometry(jump)
    for theme in THEMES:
        out = OUT / f"jump-{theme}.svg"
        out.write_text(figure(theme, rec, cal, parts, tips, shift))
        print(f"{out} ({out.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
