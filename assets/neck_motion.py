"""Rung 8's neck groundwork: what rung 6's whole brain with its eyes does with wide-field motion, from
experiments/neck_drive_probe.json and experiments/neck_pitch_probe.json (nothing by hand).

    python assets/neck_motion.py      # writes assets/neck_motion-light.svg and assets/neck_motion-dark.svg

Each row is a cell type, with its left-soma cells (filled) and right-soma cells (open) joined by a line, under a drum
rotating counterclockwise (seen from above; front-to-back across the left eye) and clockwise (30 deg vertical grating at
40 deg/s), and under horizontal stripes moving down and up on both eyes (30 deg, 40 deg/s). Rates are means over 8
flies, 0.5-2 s into a 2 s scene after 1 s of grey. Grey ticks: the same cells at grey. A blank row means the probe
didn't read that cell type. Sides are soma sides: CvN6's and CvN7's axons cross, so their nerves are on the other side.
Rows: the lobula plate's HS, H2 and VS cells; DNp15 and DNp20, descending neurons that carry their signals; the brain's
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
W, H = 1120, 660
ROWS = [("Motion cells", [("HS", "HS (HSN, HSE, HSS)"), ("H2", "H2"), ("VS", "VS")]),
        ("Descending", [("DNp15", "DNp15 (DNHS1)"), ("DNp20", "DNp20 (DNOVS1)")]),
        ("Yaw neck MNs", [("GNG283", "GNG283"), ("GNG276", "GNG276"), ("GNG647", "GNG647 (VCvN1/2)"), ("GNG653", "GNG653 (CvN1/2)"),
                          ("GNG314", "GNG314 (VCvN3)")]),
        ("Pitch neck MNs", [("CvN4", "CvN4"), ("CvN5", "CvN5"), ("CvN6", "CvN6"), ("CvN7", "CvN7")])]
COLS = [("yaw", "ccw", "Drum counterclockwise"), ("yaw", "cw", "Drum clockwise"), ("pitch", "down", "Stripes moving down"),
        ("pitch", "up", "Stripes moving up")]
VMAX = 160.0


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, probes: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 30, "Wide-field motion reaches the brain's neck motor neurons: yaw ones strongly, the pitch ones weakly", "lab"),
           text(24, 50, "Rung 6's whole brain with its eyes, open loop (8 flies). A drum drives the yaw neck motor neurons on the side whose HS cells it excites;", "note"),
           text(24, 68, "stripes moving down drive the VS cells and DNp20 hard and CvN7 a little. Filled: left-soma cells; open: right-soma.", "note")]
    lx, x0, cw, gap = 24, 268, 196, 16
    rowh, top = 21, 122
    nrows = sum(len(r) for _, r in ROWS) + len(ROWS)
    bottom = top + nrows * rowh
    for k, (probe, scene, label) in enumerate(COLS):
        d = probes[probe]["scenes"]
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
                rates = d[scene]["rates_hz"].get(key, {})
                if "L" in rates and "R" in rates:
                    lft, rgt = rates["L"], rates["R"]
                    gl, gr = d["grey"]["rates_hz"][key]["L"], d["grey"]["rates_hz"][key]["R"]
                    for g in (gl, gr):
                        out.append(f'<line x1="{tx(g):.1f}" y1="{yy - 5:.1f}" x2="{tx(g):.1f}" y2="{yy + 5:.1f}" stroke="{c["faint"]}" stroke-width="2"/>')
                    out.append(f'<line x1="{tx(lft):.1f}" y1="{yy:.1f}" x2="{tx(rgt):.1f}" y2="{yy:.1f}" stroke="{c["muted"]}" stroke-width="1.5"/>')
                    out.append(f'<circle cx="{tx(lft):.1f}" cy="{yy:.1f}" r="5" fill="{c["ink"]}"><title>{name} left: {lft:.1f} Hz</title></circle>')
                    out.append(f'<circle cx="{tx(rgt):.1f}" cy="{yy:.1f}" r="5" fill="{c["paper"]}" stroke="{c["red"]}" stroke-width="2">'
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
    title = ("Left and right rates of motion cells, descending neurons and the brain's neck motor neurons under a drum rotating "
             "each way and stripes moving down and up")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    probes = {"yaw": json.loads((ROOT / "experiments" / "neck_drive_probe.json").read_text()),
              "pitch": json.loads((ROOT / "experiments" / "neck_pitch_probe.json").read_text())}
    for theme in THEMES:
        path_ = OUT / f"neck_motion-{theme}.svg"
        path_.write_text(figure(theme, probes))
        print(path_)


if __name__ == "__main__":
    main()
