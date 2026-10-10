"""The MBON11 figure in the README (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/mbon11.py      # writes assets/mbon11-light.svg and assets/mbon11-dark.svg

odor_probe32.py: MBON11 (MBON-gamma1pedc>a/b) in odor_probe30.py's model with its Kenyon cell synapses set from Yamada
et al. 2024's charge and Wang et al. 2026's gain (odor_probe31.py, 0.030 pC per synapse), 4 seeds of 8 flies, 50 ms
bins. Top: its rate, and the rate its own gain near rest (3.7 spikes/s per mV) predicts from its input above rest.
Bottom: its Kenyon cell input as a current per cell. Flies (Hige et al. 2015, Figs. 1E and 3C, read off the figures,
research_notes/Rung 9 learning data/mbon11_input.md): the PSTH and the EPSC's landmarks, their times moved 75 ms earlier
(odor_probe21.py's valve delay) so that 0 is the odor reaching the antenna, as in the model, and the PSTH's 6 Hz
baseline (the cells were held) raised to the model's resting rate.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/al_transform.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 690
VALVE = 0.075
ODORS = ("3-octanol", "4-methylcyclohexanol")
FLY_PSTH = {"3-octanol": [(0.0, 6), (0.15, 6), (0.30, 137), (0.70, 97), (1.05, 97), (1.15, 80), (1.45, 6)],
            "4-methylcyclohexanol": [(0.0, 6), (0.15, 6), (0.26, 135), (0.60, 100), (0.90, 100), (1.45, 6)]}
FLY_EPSC = [(0.0, 0), (0.18, 0), (0.24, 405), (0.35, 200), (0.60, 170), (1.00, 170), (1.50, 0)]   # both odors (n = 5)
T0, T1 = -0.5, 1.5
X0, PW, GAP = 92, 470, 70
RATE = (104, 340, 400)                           # top panel: top y, bottom y, max Hz
CURR = (420, 620, 1000)                          # bottom panel: top y, bottom y, max pA


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def axes(c, x0, box, unit, step, label: bool) -> list[str]:
    top, bottom, vmax = box
    sx = lambda t: x0 + PW * (t - T0) / (T1 - T0)
    sy = lambda v: bottom - (bottom - top) * min(max(v, 0), vmax) / vmax
    out = []
    for v in range(0, vmax + 1, step):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + PW}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        if label:
            out.append(text(x0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for t in (-0.5, 0, 0.5, 1.0, 1.5):
        out.append(text(sx(t), bottom + 16, f"{t:g}", "tick", "middle"))
    out.append(f'<rect x="{sx(0):.1f}" y="{top}" width="{sx(1.0) - sx(0):.1f}" height="{bottom - top}" fill="{c["ink"]}" fill-opacity="0.05"/>')
    if label:
        out.append(f'<text x="{x0 - 52}" y="{(top + bottom) / 2:.1f}" class="tick" text-anchor="middle" '
                   f'transform="rotate(-90 {x0 - 52} {(top + bottom) / 2:.1f})">{unit}</text>')
    return out


def line(c, x0, box, ts, vs, colour, dashed=False, width=2.0) -> str:
    top, bottom, vmax = box
    sx = lambda t: x0 + PW * (t - T0) / (T1 - T0)
    sy = lambda v: bottom - (bottom - top) * min(max(v, 0), vmax) / vmax
    d = " ".join(f"{'M' if i == 0 else 'L'}{sx(t):.1f} {sy(v):.1f}" for i, (t, v) in enumerate(zip(ts, vs)) if T0 <= t <= T1)
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linejoin="round"{dash}/>'


def rings(c, x0, box, points, title) -> list[str]:
    top, bottom, vmax = box
    sx = lambda t: x0 + PW * (t - T0) / (T1 - T0)
    sy = lambda v: bottom - (bottom - top) * min(max(v, 0), vmax) / vmax
    out = [line(c, x0, box, [t for t, _ in points], [v for _, v in points], c["ink"], dashed=True, width=1.2)]
    for t, v in points:
        out.append(f'<circle cx="{sx(t):.1f}" cy="{sy(v):.1f}" r="4.5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.8">'
                   f'<title>{title}: {v:g} at {t + VALVE:.2f} s after the valve opened</title></circle>')
    return out


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "MBON11 in the model: its input is too big for one odor and too small for the other, and half of it is lost in its timing", "lab"),
           text(24, 50, "Red: the model (odor_probe32.py, 0.030 pC per synapse). Dashed red: the rate MBON11's own gain near rest predicts from its "
                "input.", "note"),
           text(24, 68, "Rings: flies (Hige et al. 2015, read off the figures; the PSTH's held 6 Hz baseline raised to the model's resting rate).", "note")]
    for k, odor in enumerate(ODORS):
        x0 = X0 + k * (PW + GAP)
        r = d["odors"][odor]
        ts = [r["start_s"] + r["bin_s"] * (i + 0.5) for i in range(len(r["rate_hz"]))]
        rest_hz = r["rest"]["rate_hz"]
        out.append(text(x0, RATE[0] - 12, odor, "val"))
        out += axes(c, x0, RATE, "MBON11, spikes/s", 100, k == 0)
        out += rings(c, x0, RATE, [(t - VALVE, v - 6 + rest_hz) for t, v in FLY_PSTH[odor]], "flies' PSTH, baseline raised to the model's rest")
        out.append(line(c, x0, RATE, ts, r["predicted_rate_hz"], c["red"], dashed=True))
        out.append(line(c, x0, RATE, ts, r["rate_hz"], c["red"], width=2.4))
        out += axes(c, x0, CURR, "Kenyon cell input per cell, pA", 250, k == 0)
        out += rings(c, x0, CURR, [(t - VALVE, v) for t, v in FLY_EPSC], "flies' odor EPSC")
        out.append(line(c, x0, CURR, ts, [v - r["rest"]["kc_pa"] for v in r["kc_pa"]], c["red"], width=2.4))
        out.append(text(x0 + PW, RATE[0] - 12, f'{d["intact"][odor]:.0f} spikes evoked at rest, {d["held"][odor]:.0f} held at 6 Hz '
                        f'(flies {d["flies"]["spikes"][odor]}, held)', "tick", "end"))
        out.append(text(x0 + PW, CURR[0] - 12, f'{r["kc_charge_pc_per_cell"]:.0f} pC (flies {d["flies"]["charge_pc"][odor]})', "tick", "end"))
    out.append(text(X0 + PW + GAP / 2, CURR[1] + 40, "time from the odor reaching the antenna (s); shaded: the 1 s odor", "tick", "middle"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    o = d["odors"]["3-octanol"]
    title = (f"MBON11's odor response in the model against flies': to 3-octanol it gains {d['held']['3-octanol']:.0f} spikes held at 6 Hz from "
             f"{o['kc_charge_pc_per_cell']:.0f} pC of Kenyon cell input per cell (flies 118 from about 250); to 4-methylcyclohexanol "
             f"{d['held']['4-methylcyclohexanol']:.0f} from {d['odors']['4-methylcyclohexanol']['kc_charge_pc_per_cell']:.0f} pC (flies 110 from about 265)")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "odor_probe32.json").read_text())
    for theme in THEMES:
        path = OUT / f"mbon11-{theme}.svg"
        path.write_text(figure(theme, d))
        print(path)


if __name__ == "__main__":
    main()
