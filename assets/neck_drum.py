"""Rung 8's neck groundwork: a rotating drum seen by rung 6's whole brain, and what its neck motor neurons do, from
experiments/neck_drive_probe.json (nothing by hand).

    python assets/neck_drum.py      # writes assets/neck_drum-light.svg and assets/neck_drum-dark.svg

Each row is a cell type, with its left-side cells (filled) and right-side cells (open) joined by a line, under the drum
rotating counterclockwise (seen from above; front-to-back across the left eye) and clockwise. Rates are means over 8
flies, 0.5-2 s into a 2 s drum after 1 s of grey (30 deg grating at 40 deg/s). Grey ticks: the same cells at grey. Rows:
the lobula plate's HS and H2 cells; DNp15, the descending neuron that carries HS signals to the nerve cord; the brain's
yaw neck motor neurons (GNG283, GNG276, GNG647 = VCvN1/2, GNG653 = CvN1/2, GNG314 = VCvN3); and its pitch ones (CvN4-7).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/dlm_splay.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 600
ROWS = [("Motion cells", [("HS", "HS (HSN, HSE, HSS)"), ("H2", "H2")]),
        ("Descending", [("DNp15", "DNp15 (DNHS1)")]),
        ("Yaw neck MNs", [("GNG283", "GNG283"), ("GNG276", "GNG276"), ("GNG647", "GNG647 (VCvN1/2)"), ("GNG653", "GNG653 (CvN1/2)"),
                          ("GNG314", "GNG314 (VCvN3)")]),
        ("Pitch neck MNs", [("CvN4", "CvN4"), ("CvN5", "CvN5"), ("CvN6", "CvN6"), ("CvN7", "CvN7")])]
VMAX = 160.0


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    sc = d["scenes"]
    out = [text(24, 30, "A rotating drum drives the brain's yaw neck motor neurons on the side whose HS cells it excites", "lab"),
           text(24, 50, "Rung 6's whole brain with its eyes, open loop (8 flies). Counterclockwise drives the left HS cells, DNp15 and yaw motor neurons; clockwise", "note"),
           text(24, 68, "the right ones. The pitch motor neuron CvN7 stays near rest; CvN6 follows the opposite side's HSS input. Filled: left cells; open: right.", "note")]
    lx, x0, cw, gap = 24, 300, 370, 40
    rowh, top = 22, 122
    cols = [("ccw", "Counterclockwise (front-to-back on the left eye)"), ("cw", "Clockwise (front-to-back on the right eye)")]
    nrows = sum(len(r) for _, r in ROWS) + len(ROWS)
    bottom = top + nrows * rowh
    for k, (scene, label) in enumerate(cols):
        cx = x0 + k * (cw + gap)
        tx = lambda v: cx + cw * min(v, VMAX) / VMAX
        out.append(text(cx + cw / 2, top - 22, label, "val", "middle"))
        for v in (0, 50, 100, 150):
            out.append(f'<line x1="{tx(v):.1f}" y1="{top - 6}" x2="{tx(v):.1f}" y2="{bottom}" stroke="{c["rule"]}" stroke-width="1"/>')
            out.append(text(tx(v), bottom + 16, f"{v}", "tiny", "middle"))
        out.append(text(cx + cw / 2, bottom + 32, "spikes/s", "tiny", "middle"))
        y = top
        for group, rows in ROWS:
            if k == 0:
                out.append(text(lx, y + 15, group, "val"))
            y += rowh
            for key, name in rows:
                yy = y + rowh / 2
                if k == 0:
                    out.append(text(lx + 12, yy + 4, name, "tick"))
                lft, rgt = sc[scene]["rates_hz"][key]["L"], sc[scene]["rates_hz"][key]["R"]
                gl, gr = sc["grey"]["rates_hz"][key]["L"], sc["grey"]["rates_hz"][key]["R"]
                for g in (gl, gr):
                    out.append(f'<line x1="{tx(g):.1f}" y1="{yy - 5:.1f}" x2="{tx(g):.1f}" y2="{yy + 5:.1f}" stroke="{c["faint"]}" stroke-width="2"/>')
                out.append(f'<line x1="{tx(lft):.1f}" y1="{yy:.1f}" x2="{tx(rgt):.1f}" y2="{yy:.1f}" stroke="{c["muted"]}" stroke-width="1.5"/>')
                out.append(f'<circle cx="{tx(lft):.1f}" cy="{yy:.1f}" r="5.5" fill="{c["ink"]}"><title>{name} left: {lft:.1f} Hz</title></circle>')
                out.append(f'<circle cx="{tx(rgt):.1f}" cy="{yy:.1f}" r="5.5" fill="{c["paper"]}" stroke="{c["red"]}" stroke-width="2.2">'
                           f'<title>{name} right: {rgt:.1f} Hz</title></circle>')
                y += rowh
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = ("Left and right rates of motion cells, DNp15 and the brain's neck motor neurons under a counterclockwise and a "
             "clockwise drum: the yaw neck motor neurons follow the side whose HS cells the drum excites")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "neck_drive_probe.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"neck_drum-{theme}.svg"
        path_.write_text(figure(theme, d))
        print(path_)


if __name__ == "__main__":
    main()
