"""The loom-to-jump figure: a disk looms, the brain's looming detectors and giant fibers fire, the jump motor neurons
follow, and NeuroMechFly jumps. From experiments/loom_jump.json and one short run of the body.

    python assets/loom_jump.py       # writes assets/loom_jump-light.svg and assets/loom_jump-dark.svg (~20 s)

The fly of experiments/loom_jump.py whose loom-evoked escape (a giant fiber on the loomed side, either side for a
head-on loom, first firing in the loom's last 60 ms, when its looming detectors are climbing) took off earliest
before contact, preferring one whose two TTMns fired within 2 ms of each other, so that both middle legs pushed. Left, what it sees: the dark
disk's angular size and side. Middle, its brain, from the saved run: LC4 and LPLC2 rates on each
side (10 ms bins, its own), and spikes of the giant fibers (GF) and TTMns, over the loom's last 300 ms. Right, the
body (brainfly.jump) driven by that fly's TTMn spikes, from its right side. The animation plays the brain up to the
first TTMn spike 20 times slower, then the jump from 0.4 ms before its force starts, 600 times slower.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assets"))
sys.path.insert(0, str(ROOT / "experiments"))
from jump import (FRONT_ORDER, PARTS, SIDE_ORDER, STYLE, THEMES, draw, geometry, shapes, text)  # noqa: E402,F401

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
W, H = 1120, 600
CONTACT, R_OVER_V, MAX_DEG = 1.8, 0.04, 45.0
BRAIN_FROM, BRAIN_FRAME, BRAIN_FRAME_S = 0.3, 0.01, 0.2       # s before contact shown, s per frame, s on screen
JUMP_FROM, JUMP_TO, JUMP_FRAME, JUMP_FRAME_S = -0.4e-3, 9e-3, 0.2e-3, 0.12   # around the first TTMn spike
HOLD = 1.6
S, GROUND, BODY_X = 60.0, 470.0, 920.0
TX0, TX1 = 400.0, 700.0                                        # brain timeline


def pick() -> tuple[dict, dict, int, str]:
    data = json.loads((ROOT / "experiments" / "loom_jump.json").read_text())
    best = None
    for name, sc in data["scenes"].items():
        loomed = {"left": "L", "right": "R"}.get(name)
        for f, j in enumerate(sc["jumps"]):
            gfs = sc["flies"][f]["gf"]
            first_gf = min((t[0] for x, t in gfs.items() if t and (loomed is None or x == loomed)), default=None)
            if not (j and j.get("took_off") and first_gf is not None and 0 < (CONTACT - first_gf) <= 0.06
                    and 0 < (CONTACT - j["first_ttmn_s"]) <= 0.06 and (j["takeoff_before_contact_ms"] or 0) > 0):
                continue
            firsts = [t[0] for t in sc["flies"][f]["ttmn"].values() if t]
            both = len(firsts) == 2 and abs(firsts[0] - firsts[1]) <= 0.002
            key = (both, j["takeoff_before_contact_ms"])
            if best is None or key > best[0]:
                best = (key, sc, j, f, name)
    if best is None:
        raise SystemExit("no loom-evoked escape took off before contact")
    return best[1], best[2], best[3], best[4]


def body_run(ttmn: dict, first: float):
    from brainfly.jump import Jump
    jump = Jump()
    spikes = {x: [t - first - JUMP_FROM for t in ttmn[x] if t - first < 0.02] for x in "LR"}
    rec = jump.run(spikes, seconds=JUMP_TO - JUMP_FROM + 1e-3)
    return jump, rec


def radius_deg(t: float) -> float:
    return min(np.degrees(np.arctan(R_OVER_V / max(CONTACT - t, 1e-9))), MAX_DEG)


def figure(theme: str, sc: dict, fly: int, jump, rec, first: float, scene: str, summary: dict) -> str:
    c = THEMES[theme]
    parts, tips = geometry(jump)
    flyd = sc["flies"][fly]
    t_start, t_stop = CONTACT - BRAIN_FROM, CONTACT
    t_end = first
    X = lambda t: TX0 + (TX1 - TX0) * (t - t_start) / (t_stop - t_start)
    where = {"left": "on its left", "right": "on its right", "head-on": "head-on"}[scene]
    out = [text(24, 34, f"A disk looms {where}; the fly's brain fires its escape and the body jumps", "lab"),
           text(24, 54, "flyvis's eyes, the whole MaleCNS brain, the giant fibers' electrical synapses onto the jump motor "
                "neurons, NeuroMechFly", "note")]
    # the brain panel, static
    rows = [("LC4 L", "LC4 R", "LC4"), ("LPLC2 L", "LPLC2 R", "LPLC2")]
    y = 110
    for a, b, label in rows:
        ra, rb = np.array(sc["rates"][a][fly]), np.array(sc["rates"][b][fly])
        tb = np.arange(len(ra)) * 0.01                                      # loom time of each 10 ms bin
        keep = (tb >= t_start) & (tb <= t_stop)
        top = max(float(max(ra[keep].max(initial=0), rb[keep].max(initial=0))), 1.0)
        for r, dash in ((ra, ""), (rb, ' stroke-dasharray="4 3"')):
            pts = " ".join(f"{X(t):.1f},{y + 60 - 55 * v / top:.1f}" for t, v in zip(tb[keep], r[keep]))
            out.append(f'<polyline points="{pts}" fill="none" stroke="{c["ink"]}" stroke-width="1.4"{dash}/>')
        out.append(text(TX0 - 8, y + 36, label, "val", "end"))
        out.append(text(TX0 - 8, y + 52, f"to {top:.0f} Hz", "tick", "end"))
        y += 80
    for key, label, colour in (("gf", "giant fiber", c["ink"]), ("ttmn", "jump motor neuron", c["red"])):
        for side in "LR":
            for t in flyd[key][side]:
                if t_start <= t <= t_stop:
                    out.append(f'<path d="M{X(t):.1f} {y}v16" stroke="{colour}" stroke-width="1.6"/>')
            out.append(text(TX0 - 8, y + 12, f"{label} {side}", "tick", "end"))
            y += 24
    out.append(text(TX1, 104, "solid: left side, dashed: right", "tick", "end"))
    legs = {"L": "its left middle leg alone", "R": "its right middle leg alone", "LR": "both middle legs"}
    out.append(text(30, 400, f"It left the ground {summary['takeoff_before_contact_ms']:.0f} ms before contact,", "val"))
    out.append(text(30, 420, f"pushing with {legs.get(summary['sides'], summary['sides'])}, at {summary['launch_speed_m_s']:.2f} m/s.", "val"))
    if summary["sides"] != "LR":
        out.append(text(30, 440, "A loom on one side fires only that side's giant fiber.", "note"))
    out.append(f'<path d="M{X(CONTACT):.1f} 104V{y}" stroke="{c["muted"]}" stroke-dasharray="3 3"/>')
    out.append(text(X(CONTACT), y + 18, "contact", "tick", "middle"))
    out.append(text(TX0, y + 18, f"{BRAIN_FROM * 1e3:.0f} ms before", "tick"))
    # frames
    frames = [("brain", t) for t in np.arange(t_start, t_end + 1e-9, BRAIN_FRAME)]
    frames = frames or [("brain", t_end)]
    frames += [("jump", first + dt) for dt in np.arange(JUMP_FROM, JUMP_TO + 1e-9, JUMP_FRAME)]
    x_rest = float(rec["thorax"][0, 0])
    side = lambda p: np.stack([BODY_X + S * (p[:, 0] - x_rest), GROUND - S * p[:, 2]], 1)
    dt_rec = rec["t"][1] - rec["t"][0]
    for f, (phase, t) in enumerate(frames):
        out.append(f'<g class="frame f{f}">')
        to_contact = (CONTACT - t) * 1e3
        out.append(text(24, 96, f"{to_contact:.1f} ms before contact" if phase == "jump" else f"{to_contact:.0f} ms before contact", "big"))
        r = radius_deg(t)
        out.append(f'<rect x="30" y="130" width="200" height="200" fill="{c["body"]}" stroke="{c["rule"]}"/>')
        cx = 130 - 85 * np.sin(np.radians(sc["azimuth_deg"]))                 # the disk's side, left positive
        out.append(f'<circle cx="{cx:.1f}" cy="230" r="{100 * r / MAX_DEG:.1f}" fill="{c["ink"]}"/>')
        out.append(text(130, 352, f"the disk spans {2 * r:.0f}°", "note", "middle"))
        out.append(f'<path d="M{X(min(t, t_end + 0.005)):.1f} 104V{y}" stroke="{c["red"]}" stroke-width="1.2"/>')
        i = int(np.clip(round((t - first - JUMP_FROM) / dt_rec), 0, len(rec["t"]) - 1)) if phase == "jump" else 0
        out += draw(shapes(rec, i, parts, tips), SIDE_ORDER, side, {"lf", "lm", "lh"})
        out.append("</g>")
    out.append(f'<path d="M700 {GROUND}H1100" stroke="{c["muted"]}" stroke-width="1.2"/>')
    out.append(text(BODY_X, GROUND + 22, "the body, from its right side", "note", "middle"))
    durations = [BRAIN_FRAME_S if p == "brain" else JUMP_FRAME_S for p, _ in frames]
    loop = sum(durations) + HOLD
    starts = np.concatenate([[0], np.cumsum(durations)])
    kf = []
    nf = len(frames)
    for f in range(nf):
        s0, s1 = 100 * starts[f] / loop, 100 * starts[f + 1] / loop
        last = f == nf - 1
        start = "0% { opacity: 1; }" if f == 0 else f"0% {{ opacity: 0; }} {s0:.3f}% {{ opacity: 1; }}"
        kf.append(f".f{f} {{ animation: fr{f} {loop:.2f}s steps(1) infinite; }} @keyframes fr{f} {{ {start} "
                  f"{(100 - 0.01) if last else s1:.3f}% {{ opacity: {1 if last else 0}; }} 100% {{ opacity: {1 if f == 0 else 0}; }} }}")
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .big {{ font-size: 20px; font-weight: 600; fill: {c["ink"]}; font-variant-numeric: tabular-nums; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .b {{ fill: {c["body"]}; stroke: {c["ink"]}; stroke-width: 1.1; stroke-linejoin: round; }}
    .e {{ fill: {c["eye"]}; stroke: {c["ink"]}; stroke-width: 1; }}
    .w {{ fill: {c["wing"]}; fill-opacity: 0.45; stroke: {c["muted"]}; stroke-width: 0.8; }}
    .m, .mf, .o, .of {{ fill: none; stroke-linecap: round; stroke-linejoin: round; }}
    .m {{ stroke: {c["red"]}; }} .mf {{ stroke: {c["red"]}; stroke-opacity: 0.45; }}
    .o {{ stroke: {c["muted"]}; }} .of {{ stroke: {c["muted"]}; stroke-opacity: 0.4; }}
    .s1 {{ stroke-width: 3.0; }} .s2 {{ stroke-width: 2.2; }} .s3 {{ stroke-width: 1.5; }}
    .frame {{ opacity: 0; }} .f{nf - 1} {{ opacity: 1; }}
    @media (prefers-reduced-motion: no-preference) {{
      .f{nf - 1} {{ opacity: 0; }}
      {" ".join(kf)}
    }}
    """
    title = ("A dark disk looms head-on at the simulated fly: its looming detectors and giant fibers fire, the jump motor "
             "neurons follow through their electrical synapses, and NeuroMechFly jumps")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    sc, j, fly, scene = pick()
    first = j["first_ttmn_s"]
    print("fly", fly, "of the", scene, "scene:", j)
    jump, rec = body_run(sc["flies"][fly]["ttmn"], first)
    for theme in THEMES:
        out = OUT / f"loom_jump-{theme}.svg"
        out.write_text(figure(theme, sc, fly, jump, rec, first, scene, j))
        print(f"{out} ({out.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
