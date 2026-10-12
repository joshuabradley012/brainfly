"""The flight motor neurons' splay state in the model, animated: five DLM motor neurons as dots running round a clock face,
each passing 12 o'clock as it fires, drawn from short reruns of the checks' calibrated units and from their saved
results (nothing by hand).

    python assets/dlm_splay.py      # writes assets/dlm_splay-light.svg and assets/dlm_splay-dark.svg

Top: three clocks, 2 s of each condition played at a quarter speed. Each dot's angle is its phase, (t - t_n) / (t_n+1 -
t_n), as Hürkey et al. 2023 compute it, so a splay state spreads the dots round the face and synchrony bunches them. The
conditions are leaky-integrator units at flies' irregularity (CV 0.22) and 6.6 Hz: uncoupled (dlm_splay_check2.py);
joined by conductances fitted to flies' coupling coefficients as flies measured them, 20 ms peak ratios, with each
unit's drive set so all five fire at one rate (dlm_splay_check6.py); and with the spikes' own spikelets as well
(dlm_splay_check6.py). Each is rerun here for 3 s (1 s discarded) with its check's own drives, kicks and junctions (seed
7). Under each clock, its 2 s as a raster. Bottom: the splayness of selected conditions (300 s x 8 runs, medians),
against flies' 0.73-0.79 and the 0.59 that independent phases give: the clocks' conditions, the AHP unit with spikelets
and 95% of its irregularity shared at flies' coupling with MN5 coupled like a weak pair (dlm_splay_check6.py) and
uncoupled (dlm_splay_check4.py), and the first runs' coupling at about half flies' (dlm_splay_check2.py).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))
import dlm_splay_check as c1                               # noqa: E402
import dlm_splay_check5 as c5                              # noqa: E402
import dlm_splay_check6 as c6                              # noqa: E402

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/looming.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 660
SHOW_S, SPEED, FPS = 2.0, 0.25, 20                         # model seconds shown, playback speed, keyframes per second
CLOCKS = [("uncoupled", "Uncoupled (as shakB knockdown)"), ("LIF, MN5 assumed", "At flies' measured coupling"),
          ("LIF + spikelets, MN5 assumed", "…and the spikes' spikelets")]
DOTS = ["ink", "red", "faint", "muted", "ink"]              # MN1-5; MN5 drawn hollow


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def rerun(d2: dict, d6: dict, name: str) -> list[np.ndarray]:
    """3 s of a condition (dlm_splay_check2.py's uncoupled, dlm_splay_check6.py's others), its own drives, kicks and
    junctions, one run (seed 7); the last 2 s of spikes."""
    hz = d2["calibration"]["chosen"]["kick_hz"]
    if name == "uncoupled":
        b = c1.brain(d2["conditions"]["uncoupled"]["bias_mv"], hz)
    else:
        coupling, gap = c6.junctions(d6["ratios"]["assumed_mn5"], c5.CC, spikelets="spikelets" in name)
        b = c5.unit("LIF", 0.0, hz, c1.KICK_MV, coupling, gap, c1.RUNS)
        b.set_bias(np.array(d6["conditions"][name]["unit_biases_mv"]))
    b.reset(7)
    b.advance(10000)
    _, sp = b.advance(int(round(SHOW_S / c1.DT)), record=np.arange(c1.N))
    return [np.flatnonzero(sp[0, :, i]) * c1.DT for i in range(c1.N)]


def angles(times: list[np.ndarray], ts: np.ndarray) -> np.ndarray:
    """Each unit's unwrapped phase in degrees at times ts (cycles counted, so it only ever increases)."""
    out = np.full((len(times), len(ts)), np.nan)
    for i, t in enumerate(times):
        if len(t) < 2:
            continue
        k = np.searchsorted(t, ts, side="right") - 1
        ok = (k >= 0) & (k < len(t) - 1)
        out[i, ok] = 360.0 * (k[ok] + (ts[ok] - t[k[ok]]) / (t[k[ok] + 1] - t[k[ok]]))
        first = ts < t[0]                                   # before the first spike: extrapolate with the first ISI
        isi0 = t[1] - t[0]
        out[i, first] = 360.0 * (ts[first] - t[0]) / isi0
        last = k >= len(t) - 1
        isi1 = t[-1] - t[-2]
        out[i, last] = 360.0 * (len(t) - 1 + (ts[last] - t[-1]) / isi1)
    return out


def figure(theme: str, d2: dict, runs: dict, splay: list) -> str:
    c = THEMES[theme]
    loop = SHOW_S / SPEED
    ts = np.linspace(0.0, SHOW_S, int(loop * FPS) + 1)
    out = [text(24, 30, "The flight motor neurons' splay state at flies' measured coupling", "lab"),
           text(24, 50, "Flies' five DLM motor neurons fire at one rate but avoid firing together (Hürkey et al. 2023). Joined by conductances fitted to flies'", "note"),
           text(24, 68, "coupling, five of the model's units spread round the cycle; the spikes' spikelets bunch them, unless the units carry flies' long AHP.", "note")]
    keyframes, rules = [], []
    for col, (name, label) in enumerate(CLOCKS):
        cx, cy, r = 190 + col * 370, 222, 80
        out.append(text(cx, 104, label, "val", "middle"))
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["rule"]}" stroke-width="1.5"/>')
        out.append(f'<line x1="{cx}" y1="{cy - r - 6}" x2="{cx}" y2="{cy - r + 6}" stroke="{c["ink"]}" stroke-width="2"/>')
        out.append(text(cx + 9, cy - r - 9, "fires", "tiny"))
        ang = angles(runs[name], ts)
        for i in range(c1.N):
            a = ang[i]
            if np.all(np.isnan(a)):
                continue
            a = np.nan_to_num(a, nan=float(np.nanmin(a)))
            cls = f"d{col}{i}"
            frames = " ".join(f"{100 * k / (len(a) - 1):.2f}% {{ transform: rotate({v:.1f}deg); }}" for k, v in enumerate(a))
            keyframes.append(f"@keyframes k{cls} {{ {frames} }}")
            rules.append(f".{cls} {{ transform-origin: {cx}px {cy}px; animation: k{cls} {loop:g}s linear infinite; }}")
            fill = "none" if i == 4 else c[DOTS[i]]
            stroke = c["ink"] if i == 4 else c["paper"]
            out.append(f'<g class="{cls}" style="transform: rotate({a[0]:.1f}deg); transform-origin: {cx}px {cy}px">'
                       f'<circle cx="{cx}" cy="{cy - r}" r="8" fill="{fill}" stroke="{stroke}" stroke-width="2">'
                       f'<title>MN{i + 1}</title></circle></g>')
        # raster under the clock
        rx, ry, rw = cx - 150, 334, 300
        for i, t in enumerate(runs[name]):
            y = ry + i * 14
            out.append(text(rx - 6, y + 4, f"MN{i + 1}", "tiny", "end"))
            for s in t:
                x = rx + rw * s / SHOW_S
                out.append(f'<line x1="{x:.1f}" y1="{y - 5}" x2="{x:.1f}" y2="{y + 5}" stroke="{c[DOTS[i]] if i < 4 else c["ink"]}" stroke-width="1.6"/>')
        out.append(f'<line x1="{rx}" y1="{ry + 72}" x2="{rx + rw}" y2="{ry + 72}" stroke="{c["rule"]}"/>')
        out.append(text(rx, ry + 86, "0", "tiny", "middle"))
        out.append(text(rx + rw, ry + 86, f"{SHOW_S:g} s", "tiny", "middle"))
    # splayness bars
    bx, by, bw, bh = 280, 478, 740, 130
    vmin, vmax = 0.2, 0.85
    tx = lambda v: bx + bw * (v - vmin) / (vmax - vmin)
    out.append(text(24, by - 14, "Splayness, selected conditions (300 s × 8 runs, medians)", "val"))
    out.append(f'<rect x="{tx(0.73):.1f}" y="{by}" width="{tx(0.79) - tx(0.73):.1f}" height="{bh}" fill="{c["ink"]}" fill-opacity="0.10"/>')
    out.append(text(tx(0.76), by + bh + 14, "flies 0.73–0.79", "tiny", "middle"))
    out.append(f'<line x1="{tx(0.59):.1f}" y1="{by}" x2="{tx(0.59):.1f}" y2="{by + bh}" stroke="{c["muted"]}" stroke-dasharray="4 3"/>')
    out.append(text(tx(0.59), by + bh + 14, "independent 0.59", "tiny", "middle"))
    for v in (0.2, 0.4, 0.6, 0.8):
        out.append(text(tx(v), by + bh + 28, f"{v:.1f}", "tiny", "middle"))
    rowh = bh / len(splay)
    for k, (label, v, hot) in enumerate(splay):
        y = by + k * rowh + rowh / 2
        out.append(text(bx - 8, y + 4, label, "tick", "end"))
        out.append(f'<line x1="{tx(vmin):.1f}" y1="{y:.1f}" x2="{tx(v):.1f}" y2="{y:.1f}" stroke="{c["rule"]}" stroke-width="1"/>')
        out.append(f'<circle cx="{tx(v):.1f}" cy="{y:.1f}" r="5" fill="{c["red"] if hot else c["ink"]}"><title>{label}: {v:.3f}</title></circle>')
        out.append(text(tx(v) + 9, y + 4, f"{v:.2f}", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    @media (prefers-reduced-motion: no-preference) {{
      {" ".join(rules)}
    }}
    {" ".join(keyframes)}
    """
    title = "Five flight motor neurons as dots on clock faces: uncoupled they drift independently, with flies' measured coupling they spread round the cycle, with spikelets they bunch; and the splayness of selected conditions"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d2 = json.loads((ROOT / "experiments" / "dlm_splay_check2.json").read_text())
    d4 = json.loads((ROOT / "experiments" / "dlm_splay_check4.json").read_text())
    d6 = json.loads((ROOT / "experiments" / "dlm_splay_check6.json").read_text())
    runs = {name: rerun(d2, d6, name) for name, _ in CLOCKS}
    s2, s6 = d2["conditions"], d6["conditions"]
    splay = [("uncoupled", s2["uncoupled"]["summary"]["splayness"][0], False),
             ("flies' coupling, one rate", s6["LIF, MN5 assumed"]["summary"]["splayness"][0], True),
             ("flies' coupling + spikelets", s6["LIF + spikelets, MN5 assumed"]["summary"]["splayness"][0], False),
             ("flies' AHP, 95% shared, uncoupled", d4["shares"]["0.95"]["conditions"]["uncoupled"]["summary"]["splayness"][0], False),
             ("flies' AHP, 95% shared, coupled + spikelets", s6["AHP 95% shared + spikelets, MN5 as weak pairs"]["summary"]["splayness"][0], True),
             ("first runs: half flies' coupling", s2["measured"]["summary"]["splayness"][0], False)]
    for theme in THEMES:
        path_ = OUT / f"dlm_splay-{theme}.svg"
        path_.write_text(figure(theme, d2, runs, splay))
        print(path_)


if __name__ == "__main__":
    main()
