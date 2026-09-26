"""The optomotor figure in the README, drawn from the saved results (nothing is drawn by hand).

    python assets/optomotor.py     # writes assets/optomotor-light.svg and assets/optomotor-dark.svg

Left: experiments/optomotor.json's confirmation (8 flies, open loop): the HS cells' and DNa02's rates
on each side under a drum rotating counterclockwise or clockwise. Right: experiments/closed_loop.json:
each fly's heading while the brain steers the body inside the drum, against the drum's own rotation.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/loom.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117"),
}
W, H = 1120, 470


def bars(c, groups, x0, y0, w, h, top, title, unit):
    """Grouped bars: per group (label, ccw, cw)."""
    out = [f'<text x="{x0}" y="{y0 - 18}" fill="{c["ink"]}" font-size="15" font-weight="600">{title}</text>']
    for v in range(0, int(top) + 1, max(1, int(top) // 3)):
        y = y0 + h - h * v / top
        out.append(f'<line x1="{x0}" x2="{x0 + w}" y1="{y:.1f}" y2="{y:.1f}" stroke="{c["rule"]}" stroke-width="1"/>')
        out.append(f'<text x="{x0 - 8}" y="{y + 4:.1f}" fill="{c["muted"]}" font-size="12" text-anchor="end">{v}</text>')
    out.append(f'<text x="{x0 - 34}" y="{y0 + h / 2}" fill="{c["muted"]}" font-size="12" text-anchor="middle" '
               f'transform="rotate(-90 {x0 - 34} {y0 + h / 2})">{unit}</text>')
    slot = w / len(groups)
    for k, (label, ccw, cw) in enumerate(groups):
        cx = x0 + slot * (k + 0.5)
        for j, (val, col) in enumerate(((ccw, c["red"]), (cw, c["muted"]))):
            bh = h * min(val, top) / top
            out.append(f'<rect x="{cx - 26 + j * 28:.1f}" y="{y0 + h - bh:.1f}" width="24" height="{bh:.1f}" fill="{col}" rx="2"/>')
        out.append(f'<text x="{cx:.1f}" y="{y0 + h + 18}" fill="{c["ink"]}" font-size="13" text-anchor="middle">{label}</text>')
    return out


def draw(theme: str, open_loop: dict, closed: dict) -> str:
    c = THEMES[theme]
    g = open_loop["confirm"]["groups"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">',
             f'<rect width="{W}" height="{H}" fill="{c["paper"]}"/>']
    parts += bars(c, [("left", g["HS L"]["ccw"], g["HS L"]["cw"]), ("right", g["HS R"]["ccw"], g["HS R"]["cw"])],
                  90, 70, 190, 290, 30, "HS cells", "spikes/s")
    parts += bars(c, [("left", g["DNa02 L"]["ccw"], g["DNa02 L"]["cw"]), ("right", g["DNa02 R"]["ccw"], g["DNa02 R"]["cw"])],
                  360, 70, 190, 290, 4, "DNa02, steering", "spikes/s")
    # legend
    for j, (name, col) in enumerate((("drum turning left (ccw)", c["red"]), ("drum turning right (cw)", c["muted"]))):
        parts.append(f'<rect x="{90 + j * 230}" y="{425}" width="14" height="14" fill="{col}" rx="2"/>')
        parts.append(f'<text x="{112 + j * 230}" y="{437}" fill="{c["ink"]}" font-size="13">{name}</text>')
    parts.append(f'<text x="90" y="{405}" fill="{c["muted"]}" font-size="12">Open loop: 8 flies, mean rate 0.5-2 s</text>')
    # closed loop headings
    x0, y0, w, h, span = 680, 70, 400, 290, 130.0
    parts.append(f'<text x="{x0}" y="{y0 - 18}" fill="{c["ink"]}" font-size="15" font-weight="600">Closed loop: heading of the walking fly</text>')
    for v in (-120, -60, 0, 60, 120):
        y = y0 + h / 2 - h / 2 * v / span
        parts.append(f'<line x1="{x0}" x2="{x0 + w}" y1="{y:.1f}" y2="{y:.1f}" stroke="{c["rule"]}" stroke-width="1"/>')
        parts.append(f'<text x="{x0 - 8}" y="{y + 4:.1f}" fill="{c["muted"]}" font-size="12" text-anchor="end">{v:+d}°</text>')
    for t in (0, 1, 2, 3):
        x = x0 + w * t / 3
        parts.append(f'<text x="{x:.1f}" y="{y0 + h + 18}" fill="{c["muted"]}" font-size="12" text-anchor="middle">{t} s</text>')
    for sign in (+1, -1):   # the drum itself
        y1 = y0 + h / 2 - h / 2 * sign * 40 * 3 / span
        parts.append(f'<line x1="{x0}" y1="{y0 + h / 2}" x2="{x0 + w}" y2="{y1:.1f}" stroke="{c["muted"]}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    parts.append(f'<text x="{x0 + 8}" y="{y0 + h - 8}" fill="{c["muted"]}" font-size="12">dashed: the drum itself, ±40°/s</text>')
    for cond, col in (("static", c["rule"]), ("cw", c["muted"]), ("ccw", c["red"])):
        for fly in closed["flies"].values():
            hd = fly[cond]["heading_deg"]
            pts = " ".join(f"{x0 + w * i / (len(hd) - 1):.1f},{y0 + h / 2 - h / 2 * (v - hd[0]) / span:.1f}" for i, v in enumerate(hd))
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linejoin="round"/>')
    parts.append(f'<text x="{x0}" y="{405}" fill="{c["muted"]}" font-size="12">8 flies; the brain steers NeuroMechFly via DNa02</text>')
    parts.append(f'<text x="{x0}" y="{423}" fill="{c["muted"]}" font-size="12">light grey: drum not turning</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    open_loop = json.loads((ROOT / "experiments" / "optomotor.json").read_text())
    closed = json.loads((ROOT / "experiments" / "closed_loop.json").read_text())
    for theme in THEMES:
        (OUT / f"optomotor-{theme}.svg").write_text(draw(theme, open_loop, closed))


if __name__ == "__main__":
    main()
