"""The compass figure in the README, from one short run of the whole resting brain.

    python assets/compass.py       # writes assets/compass-light.svg and assets/compass-dark.svg

The brain that passed rung 4 (rung4_scaling.py's intact brain, attempt 5): taste_escape.py's resting brain with
ring_fit3.py's head-direction ring in it, each ring neuron's offset from ring_insitu.tune, and its synapses from outside
the ring scaled by its averaged factor (experiments/rung4_scaling/intact_state.npz). One batch of 8 fresh runs of 120 s
at grey, after 2 s to settle; the first run builds the brain (~5 min) and simulates (~10 min), and caches EPG activity
by wedge in experiments/rung4_scaling/compass.npz. The figure shows the run whose bump drifts at the median rate of
the 8. Left: the ellipsoid body's 16 wedges, each lit by its EPGs' spikes in 200-ms frames, over 40 s of that run at 5
times real time. Right: the same run's EPG activity by wedge over 120 s (a kymograph), with the 40 s on the left
bracketed; below it, where the bump sat over every window of rung 4's measurement (8 runs of 300 s) in its three
pre-registered attempts on fresh seeds: rung4_rest.py (offset homeostasis), rung4_anneal.py (annealed offsets) and
rung4_scaling.py (synaptic scaling, the brain shown).
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
from loom import png  # noqa: E402
from rest import text  # noqa: E402

OUT = Path(__file__).parent
CACHE = ROOT / "experiments" / "rung4_scaling" / "compass.npz"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/sees.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117"),
}
W, H = 1120, 580
SECONDS, BIN, SEED = 120, 0.2, 31                   # run length and frame (s), the batch's seed
SHOW_FROM, SHOW, SPEED = 40.0, 40.0, 5.0            # the animated stretch and its speed-up
CX, CY, R0, R1 = 230, 290, 78, 160
KX0, KX1, KY0, KY1 = 520, 1090, 110, 330
HX0, HY0, HY1 = 520, 420, 500                       # the position histograms


def wedges(side: np.ndarray, glom: np.ndarray) -> np.ndarray:
    """An EPG's ellipsoid-body wedge from its bridge glomerulus, as rest_calibration.bump_motion maps it."""
    return np.where(side == "R", (2 * glom) % 16, (19 - 2 * glom) % 16)


def simulate() -> np.ndarray:
    """EPG spikes per wedge in each BIN, per EPG: (runs, bins, 16) in Hz."""
    import rest_calibration as attempt1
    import rung4_scaling

    s = rung4_scaling.prepare("intact")[0]                # the saved state: biases, offsets, averaged factors
    b = s.brain
    epg, side, glom = attempt1.epgs(s.types)
    wedge = wedges(side, glom)
    b.reset(SEED)
    b.set_release(s.ol.neurons, s.silent)
    b.set_bias(s.bias[s.gid])
    b.advance(int(round(2.0 / b.dt)))
    bins = []
    for _ in range(int(round(SECONDS / BIN))):
        c = b.advance(int(round(BIN / b.dt)))[:, epg]
        bins.append(np.stack([c[:, wedge == k].mean(1) for k in range(16)], 1))
    return np.stack(bins, 1) / BIN


def drift(act: np.ndarray, window: float = 1.0) -> np.ndarray:
    """Each run's diffusion coefficient (rad^2/s) from 1-s windows, as rest_calibration.bump_motion measures it."""
    per = int(round(window / BIN))
    prof = act[:, : act.shape[1] // per * per].reshape(len(act), -1, per, 16).sum(2)
    theta = np.unwrap(np.angle(prof @ np.exp(2j * np.pi * np.arange(16) / 16)), axis=1)
    lags = np.arange(1, 21)
    return np.array([np.polyfit(lags * window, [np.mean((th[k:] - th[:-k]) ** 2) for k in lags], 1)[0] / 2 for th in theta])


def sector(k: int) -> str:
    """Wedge k of the ellipsoid body as an annular sector (wedge 0 at the top, clockwise)."""
    a0, a1 = np.radians(k * 22.5 - 11.25 - 90 + 1.2), np.radians(k * 22.5 + 11.25 - 90 - 1.2)
    p = lambda r, a: f"{CX + r * np.cos(a):.1f} {CY + r * np.sin(a):.1f}"
    return f"M{p(R0, a0)}L{p(R1, a0)}A{R1} {R1} 0 0 1 {p(R1, a1)}L{p(R0, a1)}A{R0} {R0} 0 0 0 {p(R0, a0)}Z"


def figure(theme: str, act: np.ndarray, d: float, panels: list) -> str:
    from scipy.ndimage import gaussian_filter1d
    c = THEMES[theme]
    frames_act, kymo = gaussian_filter1d(act, 1.0, axis=0, mode="nearest"), gaussian_filter1d(act, 1.5, axis=0, mode="nearest")
    a, z = int(SHOW_FROM / BIN), int((SHOW_FROM + SHOW) / BIN)
    frames = np.clip(frames_act[a:z] / np.percentile(frames_act[a:z], 99), 0, 1)
    nf = len(frames)
    out = [text(24, 36, "The connectome's compass, inside the whole resting brain", "lab"),
           text(24, 56, "its EPGs' bump holds a heading with no cue and wanders slowly, like a fly's in darkness", "note")]
    out += [f'<path d="{sector(k)}" fill="none" stroke="{c["rule"]}" stroke-width="1"/>' for k in range(16)]
    for f in range(nf):
        out.append(f'<g class="frame f{f}">')
        for k in range(16):
            if frames[f, k] > 0.02:
                out.append(f'<path d="{sector(k)}" fill="{c["red"]}" fill-opacity="{0.12 + 0.88 * frames[f, k]:.2f}"/>')
        out.append("</g>")
    out.append(text(CX, CY + 4, "ellipsoid body", "note", "middle"))
    out.append(text(CX, CY + R1 + 30, f"16 wedges, lit by their EPGs' spikes; {SHOW:.0f} s at {SPEED:g}× real time", "note", "middle"))

    # kymograph
    out.append(text(KX0, 90, f"The same run over {SECONDS} s: where the bump sits", "val"))
    centre = np.angle((kymo @ np.exp(2j * np.pi * np.arange(16) / 16)).sum()) / (2 * np.pi / 16)
    shift = int(round(8 - centre)) % 16                           # the run's mean wedge in the middle row
    kymo = np.roll(kymo, shift, axis=1)
    img = np.round(np.clip(kymo / np.percentile(kymo, 99), 0, 1).T * 23)   # 16 rows x bins
    data = base64.b64encode(png(img, c["red"], 24)).decode()
    out.append(f'<image x="{KX0}" y="{KY0}" width="{KX1 - KX0}" height="{KY1 - KY0}" style="image-rendering: pixelated" '
               f'preserveAspectRatio="none" href="data:image/png;base64,{data}"/>')
    out.append(f'<rect x="{KX0}" y="{KY0}" width="{KX1 - KX0}" height="{KY1 - KY0}" fill="none" stroke="{c["rule"]}"/>')
    ky = lambda wedge: KY0 + (KY1 - KY0) * (wedge + 0.5) / 16
    for row in (0, 4, 8, 12):
        out.append(text(KX0 - 8, ky(row) + 4, f"{((row - shift) % 16) * 22.5:g}°", "tick", "end"))
    kx = lambda t: KX0 + (KX1 - KX0) * t / SECONDS
    for t in range(0, SECONDS + 1, 30):
        out.append(text(kx(t), KY1 + 18, f"{t} s", "tick", "middle"))
    out.append(f'<path d="M{kx(SHOW_FROM):.1f} {KY0 - 8}V{KY0 - 3}H{kx(SHOW_FROM + SHOW):.1f}V{KY0 - 8}" fill="none" stroke="{c["ink"]}" stroke-width="1.3"/>')
    out.append(f'<path class="head" d="M{kx(SHOW_FROM):.1f} {KY0}V{KY1}" stroke="{c["ink"]}" stroke-width="1.3"/>')
    out.append(text(KX0, KY1 + 40, f"This run drifts at D = {d:.3f} rad²/s; flies' bumps in darkness, about 0.003–0.04.", "note"))

    # where the bump sat in rung 4's three pre-registered attempts
    gap = 30
    hw = (KX1 - HX0 - gap * (len(panels) - 1)) / len(panels)
    top = max(max(h["hist"]) for h in panels)
    for j, h in enumerate(panels):
        x0 = HX0 + j * (hw + gap)
        out.append(text(x0, HY0 - 30, h["title"], "val"))
        out.append(text(x0, HY0 - 14, h["subtitle"], "tick"))
        bw = hw / 16
        for k, v in enumerate(h["hist"]):
            y = HY1 - (HY1 - HY0) * v / top
            out.append(f'<rect x="{x0 + k * bw + 0.8:.1f}" y="{y:.1f}" width="{bw - 1.6:.1f}" height="{HY1 - y:.1f}" '
                       f'fill="{c["red"] if h["even"] else c["muted"]}"/>')
        out.append(f'<line x1="{x0}" y1="{HY1}" x2="{x0 + hw}" y2="{HY1}" stroke="{c["rule"]}"/>')
        out.append(text(x0, HY1 + 18, h["note"], "tick"))
        out.append(text(x0, HY1 + 32, h["verdict"], "tick"))
    out.append(text(HX0, HY1 + 54, "Each: the share of time at each of the 16 wedges over 8 runs of 300 s on fresh seeds;", "tick"))
    out.append(text(HX0, HY1 + 68, "rung 4 asks an entropy of at least 0.9 and resultants under 0.6.", "tick"))

    loop = SHOW / SPEED + 1.0
    pct = lambda t: 100 * t / loop
    kf = []
    for f in range(nf):
        s0, s1 = pct(f * BIN / SPEED), pct((f + 1) * BIN / SPEED)
        last = f == nf - 1
        kf.append(f".f{f} {{ animation: fr{f} {loop}s steps(1) infinite; }} @keyframes fr{f} {{ 0% {{ opacity: 0; }} "
                  f"{s0:.3f}% {{ opacity: 1; }} {(100 - 0.01) if last else s1:.3f}% {{ opacity: {1 if last else 0}; }} 100% {{ opacity: 0; }} }}")
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .frame {{ opacity: 0; }} .f{nf - 1} {{ opacity: 1; }}
    .head {{ opacity: 0; }}
    @media (prefers-reduced-motion: no-preference) {{
      .f{nf - 1} {{ opacity: 0; }}
      {" ".join(kf)}
      .head {{ animation: head {loop}s linear infinite; }}
    }}
    @keyframes head {{ 0% {{ opacity: 1; transform: translateX(0); }} {pct(SHOW / SPEED):.2f}% {{ opacity: 1; transform: translateX({kx(SHOW_FROM + SHOW) - kx(SHOW_FROM):.1f}px); }}
                       {pct(SHOW / SPEED) + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
    """
    title = ("The fly connectome's head-direction ring inside the whole simulated resting brain: a bump of activity in the "
             "ellipsoid body holds a heading with no cue and wanders slowly, visiting every heading once each ring neuron "
             "has scaled its synapses from outside the ring")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    if CACHE.exists():
        act = np.load(CACHE)["act"]
    else:
        act = simulate()
        np.savez_compressed(CACHE, act=act, seed=SEED, bin=BIN)
    d = drift(act)
    run = int(np.argsort(d)[len(d) // 2])                         # the run with the median drift
    load = lambda name: json.loads((ROOT / "experiments" / name / "intact.json").read_text())
    panels = []
    for name, title, subtitle, verdict in (("rung4_rest", "Attempt 3", "offsets in place", "favors one side: fails"),
                                           ("rung4_anneal", "Attempt 4", "annealed offsets", "leans: fails"),
                                           ("rung4_scaling", "Attempt 5", "scaled synapses (above)", "even: passes")):
        m = load(name)
        res = max(m["bump"][x]["resultant"] for x in "LR")
        panels.append({"title": title, "subtitle": subtitle, "hist": m["bump_motion"]["position_histogram"], "even": bool(m["BUMP"]),
                       "note": f"entropy {m['bump_motion']['position_entropy']:.2f}, resultant {res:.2f}", "verdict": verdict})
    print("drift per run", np.round(d, 4), "showing run", run)
    for theme in THEMES:
        path = OUT / f"compass-{theme}.svg"
        path.write_text(figure(theme, act[run], float(d[run]), panels))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
