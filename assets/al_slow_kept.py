"""The projection neuron figure in the README (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/al_slow_kept.py      # writes assets/al_slow_kept-light.svg and assets/al_slow_kept-dark.svg

The antennal lobe with its local neurons calibrated to flies' odor response and its inhibition fitted after the resting
polishes (odor_probe42.py at s = 0.17), crossed with the receptor synapse's slow component at Nagel et al. 2015's odor
fit (0.774 of the fast charge) or Kazama & Wilson 2008's unitary size (0.086), and the projection neurons (PNs) either
losing their synaptic current at each spike (Shiu et al.'s rule) or keeping it (odor_probe41.py). Left: 3-octanol's
PNs (every PN of its glomeruli) in 50 ms bins, against the mean of 843 PN responses in flies (Bhandawat et al. 2007,
Fig. 1b, read off the figure: about 4.5 spikes/s at rest, 88 at the peak about 145 ms after the valve, 42 at 500 ms),
moved 75 ms earlier for the valve's delay so that 0 is the odor reaching the antenna, as in the model. Right: the share
of Kenyon cells responding to each of six odors and the responding alpha/beta cells' spikes per response (odor_probe7's
measures), against flies' 6 +- 5% and 2.2 +- 1.2 (Turner et al. 2008).
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
W, H = 1120, 540
VALVE = 0.075
FLIES = ((0.145 - VALVE, 88.0), (0.5 - VALVE, 42.0))     # Bhandawat et al. 2007's grand mean
FLY_REST = 4.5
# (label, source, condition key, colour key, dashed)
SERIES = (("slow 0.774, Shiu's rule", "odor_probe42", "0.17", "faint", True),
          ("slow 0.774, current kept", "odor_probe41", "nagel_kept", "faint", False),
          ("slow 0.086, Shiu's rule", "odor_probe41", "kw08", "red", True),
          ("slow 0.086, current kept", "odor_probe41", "kw08_kept", "red", False))
ODORS = ("3-octanol", "4-methylcyclohexanol", "ethyl acetate", "isopentyl acetate", "benzaldehyde", "2-heptanone")
X0, PW = 86, 560                                   # the time-course panel
T0, T1, VMAX = 0.0, 1.0, 140.0
Y0, Y1 = 120, 440
DX0, DPW = 800, 290                                # the two dot panels
ROWS = (128, 320)                                  # their tops; each 150 px high


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def sx(t):
    return X0 + PW * (t - T0) / (T1 - T0)


def sy(v):
    return Y1 - (Y1 - Y0) * min(max(v, 0), VMAX) / VMAX


def course_panel(c, rows) -> list[str]:
    out = [text(X0, Y0 - 14, "3-octanol's projection neurons", "val")]
    for v in range(0, int(VMAX) + 1, 20):
        out.append(f'<line x1="{X0}" y1="{sy(v):.1f}" x2="{X0 + PW}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(X0 - 8, sy(v) + 4, f"{v}", "tick", "end"))
    for t in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        out.append(text(sx(t), Y1 + 16, f"{t:g}", "tick", "middle"))
    out.append(text(X0 + PW / 2, Y1 + 36, "time from the odor reaching the antenna (s)", "tick", "middle"))
    out.append(f'<text x="{X0 - 50}" y="{(Y0 + Y1) / 2:.1f}" class="tick" text-anchor="middle" '
               f'transform="rotate(-90 {X0 - 50} {(Y0 + Y1) / 2:.1f})">spikes/s per PN</text>')
    (t0, v0), (t1, v1) = FLIES
    out.append(f'<line x1="{sx(0):.1f}" y1="{sy(FLY_REST):.1f}" x2="{sx(t0):.1f}" y2="{sy(v0):.1f}" stroke="{c["ink"]}" '
               f'stroke-width="1.2" stroke-dasharray="4 3"/>')
    out.append(f'<line x1="{sx(t0):.1f}" y1="{sy(v0):.1f}" x2="{sx(t1):.1f}" y2="{sy(v1):.1f}" stroke="{c["ink"]}" '
               f'stroke-width="1.2" stroke-dasharray="4 3"/>')
    for t, v in FLIES:
        out.append(f'<circle cx="{sx(t):.1f}" cy="{sy(v):.1f}" r="4.5" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.8">'
                   f'<title>flies (Bhandawat et al. 2007, 843 PN responses): {v:g} spikes/s at {t + VALVE:.3f} s after the valve</title></circle>')
    for label, colour, dashed, pn in rows:
        d = " ".join(f"{'M' if i == 0 else 'L'}{sx(0.025 + 0.05 * i):.1f} {sy(v):.1f}" for i, v in enumerate(pn))
        dash = ' stroke-dasharray="7 4"' if dashed else ""
        width = 2.6 if (colour == "red" and not dashed) else 2.0
        out.append(f'<path d="{d}" fill="none" stroke="{c[colour]}" stroke-width="{width}" stroke-linejoin="round"{dash}>'
                   f'<title>{label}: peak {max(pn):.0f} spikes/s</title></path>')
    lx, ly = sx(0.58), sy(78)                       # below the grey curves, above the red ones
    for i, (label, colour, dashed, pn) in enumerate(rows):
        y = ly + 18 * i
        dash = ' stroke-dasharray="7 4"' if dashed else ""
        out.append(f'<line x1="{lx:.1f}" y1="{y:.1f}" x2="{lx + 30:.1f}" y2="{y:.1f}" stroke="{c[colour]}" stroke-width="2.4"{dash}/>')
        out.append(text(lx + 38, y + 4, f"{label} (peak {max(pn):.0f})", "tick"))
    y = ly + 18 * len(rows)
    out.append(f'<line x1="{lx:.1f}" y1="{y:.1f}" x2="{lx + 30:.1f}" y2="{y:.1f}" stroke="{c["ink"]}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    out.append(text(lx + 38, y + 4, "flies (Bhandawat et al. 2007)", "tick"))
    return out


def dot_panel(c, top, title, values, band, vmax, fmt) -> list[str]:
    """One row per condition: a dot per odor, flies' band shaded."""
    height = 150
    gx = lambda v: DX0 + DPW * min(max(v, 0), vmax) / vmax
    out = [text(DX0, top - 10, title, "val")]
    lo, hi = band
    out.append(f'<rect x="{gx(lo):.1f}" y="{top}" width="{gx(hi) - gx(lo):.1f}" height="{height}" fill="{c["ink"]}" fill-opacity="0.07"/>')
    for v in (0, vmax / 2, vmax):
        out.append(f'<line x1="{gx(v):.1f}" y1="{top}" x2="{gx(v):.1f}" y2="{top + height}" stroke="{c["rule"]}" stroke-opacity="0.6"/>')
        out.append(text(gx(v), top + height + 15, fmt(v), "tick", "middle"))
    step = height / (len(values) + 1)
    for i, (label, colour, dashed, vals) in enumerate(values):
        y = top + step * (i + 1)
        out.append(text(DX0 - 8, y + 4, label, "tick", "end"))
        for odor, v in vals:
            if v is None:
                continue
            fill = c[colour] if not dashed else c["paper"]
            out.append(f'<circle cx="{gx(v):.1f}" cy="{y:.1f}" r="4.2" fill="{fill}" stroke="{c[colour]}" stroke-width="1.6">'
                       f'<title>{label}, {odor}: {fmt(v)}</title></circle>')
    return out


def figure(theme: str, data: dict) -> str:
    c = THEMES[theme]
    rows, density, spikes = [], [], []
    for label, src, key, colour, dashed in SERIES:
        e = data[src]["conditions"][key]
        rows.append((label, colour, dashed, e["course"]["3-octanol"]["pn_hz"]))
        density.append((label, colour, dashed, [(o, 100 * e["odors"][o]["kc_share"]) for o in ODORS]))
        spikes.append((label, colour, dashed, [(o, e["odors"][o]["spikes_per_response"]["alpha/beta"]) for o in ODORS]))
    out = [text(24, 30, "The measured slow component makes the projection neurons accommodate; keeping their current makes them open hard", "lab"),
           text(24, 50, "The antennal lobe with its local neurons calibrated (odor_probe42.py), the receptor synapse's slow component at Nagel et al.'s "
                "0.774 (grey) or Kazama & Wilson's 0.086 (red),", "note"),
           text(24, 68, "and the projection neurons losing their synaptic current at each spike (dashed) or keeping it (solid; odor_probe41.py). "
                "Right: one dot per odor; shaded: flies (Turner et al. 2008).", "note")]
    out += course_panel(c, rows)
    out += dot_panel(c, ROWS[0], "Kenyon cells responding, % (flies 6 ± 5)", density, (1.0, 11.0), 20.0, lambda v: f"{v:.0f}")
    out += dot_panel(c, ROWS[1], "α/β cells' spikes per response (flies 2.2 ± 1.2)", spikes, (1.0, 3.4), 9.0, lambda v: f"{v:.1f}")
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = ("3-octanol's projection neurons over 1 s and the Kenyon cells' responses in four antennal lobe models: the slow receptor "
             "component's size decides whether the projection neurons accommodate, and keeping their synaptic current decides how hard "
             "they open")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    data = {name: json.loads((ROOT / "experiments" / f"{name}.json").read_text()) for name in ("odor_probe41", "odor_probe42")}
    for theme in THEMES:
        path = OUT / f"al_slow_kept-{theme}.svg"
        path.write_text(figure(theme, data))
        print(path)


if __name__ == "__main__":
    main()
