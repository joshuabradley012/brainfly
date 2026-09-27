"""The compass figure in the README, from one short run.

    python assets/compass.py       # writes assets/compass-light.svg and assets/compass-dark.svg (~1 min)

ring_fit3.py's head-direction ring with ring_homeostasis.py's slow homeostasis: the 460-neuron sub-network
(the ring's six types, ER and ExR) with fitted class gains, as ring_drift.py runs it, alone, not yet in the
whole brain. One run (seed 21) at rest with no cue. Left: the ellipsoid body's 16 wedges, each lit by
its EPGs' spikes in each 100 ms, over 8 s of the run, in real time. Right: the same run's EPG activity by
wedge over 60 s (a kymograph), with the 8 s on the left bracketed, and the drift measured by ring_drift.py
against flies'.
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
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/sees.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117"),
}
W, H = 1120, 470
SECONDS, BIN, SHOW_FROM, SHOW = 60, 0.1, 20.0, 8.0          # run length, frame (s), the animated stretch
CX, CY, R0, R1 = 230, 270, 78, 160
KX0, KX1, KY0, KY1 = 520, 1090, 110, 350


def simulate() -> np.ndarray:
    """EPG spikes summed per wedge in each BIN: (bins, 16), mean per EPG."""
    import ring_fit

    p = json.loads((ROOT / "experiments" / "ring_fit3.json").read_text())["best"]["params"]
    extra_by_type = json.loads((ROOT / "experiments" / "ring_homeostasis_slow_ring_fit3.json").read_text())["extra_bias_mv"]
    r = ring_fit.Ring(p, 1, seed=21)
    b = r.brain
    types = np.asarray(b.mcns_type)
    extra = np.zeros(b.n)
    for t, vals in extra_by_type.items():
        extra[types == t] = vals
    b.set_bias(r.bias + extra)
    b.advance(int(round(2.0 / b.dt)))
    bins = []
    for _ in range(int(round(SECONDS / BIN))):
        c = b.advance(int(round(BIN / b.dt)))[0, r.epg]
        bins.append([c[r.wedge == k].mean() for k in range(16)])
    return np.array(bins) / BIN                                  # Hz per EPG


def sector(k: int) -> str:
    """Wedge k of the ellipsoid body as an annular sector (wedge 0 at the top, clockwise)."""
    a0, a1 = np.radians(k * 22.5 - 11.25 - 90 + 1.2), np.radians(k * 22.5 + 11.25 - 90 - 1.2)
    p = lambda r, a: f"{CX + r * np.cos(a):.1f} {CY + r * np.sin(a):.1f}"
    return f"M{p(R0, a0)}L{p(R1, a0)}A{R1} {R1} 0 0 1 {p(R1, a1)}L{p(R0, a1)}A{R0} {R0} 0 0 0 {p(R0, a0)}Z"


def figure(theme: str, act: np.ndarray, drift: dict) -> str:
    from scipy.ndimage import gaussian_filter1d
    c = THEMES[theme]
    ring = lambda x, sd: gaussian_filter1d(x, sd, axis=0, mode="nearest")
    frames_act, kymo = ring(act, 1.5), ring(act, 3.0)           # smoothed over ~0.15 and ~0.3 s for display
    a, z = int(SHOW_FROM / BIN), int((SHOW_FROM + SHOW) / BIN)
    cap = np.percentile(frames_act[a:z], 99)
    frames = np.clip(frames_act[a:z] / cap, 0, 1)
    nf = len(frames)
    out = [text(24, 36, "The connectome's compass holds a heading, with no cue", "lab"),
           text(24, 56, "the head-direction ring alone (460 neurons, fitted class gains); not yet inside the whole brain", "note")]
    out += [f'<path d="{sector(k)}" fill="none" stroke="{c["rule"]}" stroke-width="1"/>' for k in range(16)]
    for f in range(nf):
        out.append(f'<g class="frame f{f}">')
        for k in range(16):
            if frames[f, k] > 0.02:
                out.append(f'<path d="{sector(k)}" fill="{c["red"]}" fill-opacity="{0.12 + 0.88 * frames[f, k]:.2f}"/>')
        out.append("</g>")
    out.append(text(CX, CY + 4, "ellipsoid body", "note", "middle"))
    out.append(text(CX, CY + R1 + 30, "16 wedges, lit by their EPGs' spikes (100 ms frames, lightly smoothed)", "note", "middle"))

    # kymograph
    out.append(text(KX0, 90, "The same run over a minute: where the bump sits", "val"))
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
    for t in (0, 20, 40, 60):
        out.append(text(kx(t), KY1 + 18, f"{t} s", "tick", "middle"))
    out.append(f'<path d="M{kx(SHOW_FROM):.1f} {KY0 - 8}V{KY0 - 3}H{kx(SHOW_FROM + SHOW):.1f}V{KY0 - 8}" fill="none" stroke="{c["ink"]}" stroke-width="1.3"/>')
    out.append(f'<path class="head" d="M{kx(SHOW_FROM):.1f} {KY0}V{KY1}" stroke="{c["ink"]}" stroke-width="1.3"/>')
    d = drift["with ring_homeostasis.py --slow"]
    for k, line in enumerate((f"It drifts slowly, like a fly's in darkness: D = {d:.3f} rad²/s (flies: about 0.003–0.04),",
                              "and on unseen seeds of 300 s passes rung 4's bump test, visiting every wedge.")):
        out.append(text(KX0, KY1 + 50 + 20 * k, line, "note"))

    loop = SHOW + 1.0
    pct = lambda t: 100 * t / loop
    kf = []
    for f in range(nf):
        s0, s1 = pct(f * BIN), pct((f + 1) * BIN)
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
    @keyframes head {{ 0% {{ opacity: 1; transform: translateX(0); }} {pct(SHOW):.2f}% {{ opacity: 1; transform: translateX({kx(SHOW_FROM + SHOW) - kx(SHOW_FROM):.1f}px); }}
                       {pct(SHOW) + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
    """
    title = ("The fly connectome's head-direction ring, simulated alone with fitted gains: a bump of activity in the "
             "ellipsoid body holds a heading with no cue and drifts slowly, like a fly's in darkness")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    act = simulate()
    drift = {r["condition"]: r["D_rad2_per_s"] for r in json.loads((ROOT / "experiments" / "ring_drift_ring_fit3.json").read_text())["conditions"]}
    for theme in THEMES:
        path = OUT / f"compass-{theme}.svg"
        path.write_text(figure(theme, act, drift))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
