"""The settled-start figure in the README (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/settle.py      # writes assets/settle-light.svg and assets/settle-dark.svg

experiments/settle_check.py: a minute of spontaneous activity in the base model (odor_probe44.py's, 8 flies), from a
reset (every synapse undepressed, as warm.py's settled starts began) and from the receptor synapses' resting depression
(warm.py's rested settling, odor_probe49.py on). Left: the receptor synapses' slow component, the share of full strength
the next spike would release (it recovers over 33 s); dashed, its resting value as the build computes it. Right: the
uniglomerular PNs' mean rate, 1 s running means of 0.5 s bins. Grey verticals: the end of the old 6 s settle and of the
new 3 s one.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/al_transform.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 470
T1 = 60.0
PANELS = ((86, "receptor synapses' slow component (share of full strength)", "strength_slow", 1.0, 0.2, "{:.1f}"),
          (636, "uniglomerular PNs (spikes/s)", "uPN", 4.0, 1.0, "{:.0f}"))
PW, Y0, Y1 = 440, 120, 380
CONDITIONS = (("from reset", "red", "from a reset (the old settled starts)"),
              ("resting depression", "ink", "from the resting depression (warm.py's rested settling)"))
REST_SLOW = 0.361                                  # odor_probe24.recalibrate_rest's resting strength (the build's log)


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def panel(c, data, x0, title, key, vmax, step, fmt) -> list[str]:
    sx = lambda t: x0 + PW * t / T1
    sy = lambda v: Y1 - (Y1 - Y0) * min(max(v, 0.0), vmax) / vmax
    out = [text(x0, Y0 - 14, title, "val")]
    for v in np.arange(0, vmax + 1e-9, step):
        out.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + PW}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
        out.append(text(x0 - 8, sy(v) + 4, fmt.format(v), "tick", "end"))
    for t in range(0, int(T1) + 1, 10):
        out.append(text(sx(t), Y1 + 16, f"{t}", "tick", "middle"))
    out.append(text(x0 + PW / 2, Y1 + 36, "time from the start (s)", "tick", "middle"))
    for t, label, dy in ((3.0, "3 s", 0), (6.0, "6 s", 14)):
        out.append(f'<line x1="{sx(t):.1f}" y1="{Y0}" x2="{sx(t):.1f}" y2="{Y1}" stroke="{c["faint"]}" stroke-width="1" stroke-dasharray="3 3"/>')
        out.append(text(sx(t) + 3, Y1 - 8 - dy, label, "tick"))
    if key == "strength_slow":
        out.append(f'<line x1="{x0}" y1="{sy(REST_SLOW):.1f}" x2="{x0 + PW}" y2="{sy(REST_SLOW):.1f}" stroke="{c["ink"]}" '
                   f'stroke-width="1.2" stroke-dasharray="6 4"/>')
        out.append(text(x0 + PW - 4, sy(REST_SLOW) + 16, f"resting value {REST_SLOW:.2f}", "tick", "end"))
    for name, colour, label in CONDITIONS:
        x = np.asarray(data["conditions"][name]["series"][key], float)
        if key == "uPN":
            x = np.convolve(x, np.ones(2) / 2, mode="valid")
            ts = 0.5 * (np.arange(len(x)) + 2)
        else:
            ts = 0.5 * (np.arange(len(x)) + 1)
        d = " ".join(f"{'M' if i == 0 else 'L'}{sx(t):.1f} {sy(v):.1f}" for i, (t, v) in enumerate(zip(ts, x)))
        at6 = float(x[int(round(6.0 / 0.5)) - (2 if key == "uPN" else 1)])
        out.append(f'<path d="{d}" fill="none" stroke="{c[colour]}" stroke-width="2.2" stroke-linejoin="round">'
                   f'<title>{label}: {at6:.2f} at 6 s, {float(np.mean(x[-20:])):.2f} over the last 10 s</title></path>')
    return out


def figure(theme: str, data: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "The settled starts hadn't settled: the receptor synapses' slow component takes a minute from a reset", "lab"),
           text(24, 50, "A minute of spontaneous activity in the base model (experiments/settle_check.py, 8 flies): from a reset (red), the slow "
                "component is still at 0.80 of its strength after 6 s and the PNs", "note"),
           text(24, 68, "fire 3.1 spikes/s, settling to 0.37 and 2.05 only after 30-45 s. Started at its resting depression, the "
                "antennal lobe is settled within about 2 s.", "note")]
    for x0, title, key, vmax, step, fmt in PANELS:
        out += panel(c, data, x0, title, key, vmax, step, fmt)
    lx, ly = 650, 425
    for i, (name, colour, label) in enumerate(CONDITIONS):
        y = ly + 18 * i
        out.append(f'<line x1="{lx}" y1="{y}" x2="{lx + 30}" y2="{y}" stroke="{c[colour]}" stroke-width="2.4"/>')
        out.append(text(lx + 38, y + 4, label, "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = ("The receptor synapses' slow component and the projection neurons' rate over a minute of spontaneous activity, from a "
             "reset and from the resting depression: from a reset neither has settled after the old 6 s settle")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    data = json.loads((ROOT / "experiments" / "settle_check.json").read_text())
    for theme in THEMES:
        path = OUT / f"settle-{theme}.svg"
        path.write_text(figure(theme, data))
        print(path)


if __name__ == "__main__":
    main()
