"""The rung 3 figure in the README, drawn from saved results (nothing by hand).

    python assets/rung3.py      # writes assets/rung3-light.svg and assets/rung3-dark.svg

flyvis's model 001 against the same model fine-tuned with rung 3's direction test and the known polarities in its loss
(experiments/rung3_001.py, pre-registered; flyvis model flow/9014/000). Left: T5a's response in the right eye to dark
edges moving each way at 40 deg/s (flyvis_native.direction_selectivity; the mean over the eye's T5a cells of each
cell's peak), both models on one scale. Middle: the flash response index of flyvis's 32 known types,
signed so that the known polarity is positive, before (x) and after (y). Right: the fine-tuned eye's fast loom on the
left: the loomed side's LC4, LPLC2 and giant fiber (DNp01), mean of 8 flies in 20 ms bins, from the looming test's
confirmation (eyepath_native.py's protocol at gain 1); the other side's in grey.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/looming.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#c9cfd6"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#4a525c"),
}
W, H = 1120, 400
DIRS = ["front-to-back", "back-to-front", "upward", "downward"]
SHORT = {"front-to-back": "front to back", "back-to-front": "back to front", "upward": "up", "downward": "down"}
SECONDS, CONTACT, T0 = 2.0, 1.8, 1.0


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def load():
    e = ROOT / "experiments"
    before = json.loads((e / "rung3_verdict.json").read_text())
    after = json.loads((e / "rung3_001.json").read_text())
    loom = json.loads((e / "rung3_001" / "looming.json").read_text())["confirm"]
    return before, after, loom


def figure(theme: str, before: dict, after: dict, loom: dict) -> str:
    c = THEMES[theme]
    out = [text(24, 34, "Rung 3 passes on fitted criteria: an eye whose T2 answers darkening, with flies' polarities", "lab"),
           text(24, 54, "flyvis's model 001 (grey) and the same model fine-tuned with rung 3's direction test and the known "
                "polarities in its loss (red), on a fresh seed", "note")]

    # --- left: T5a in the eye
    x0, y0, y1, bw = 56, 120, 300, 16
    out.append(text(24, 96, "T5a in the eye, dark edges moving each way", "val"))
    top = max(max(res["R T5a"]["responses"].values()) for res in (before["direction_selectivity"], after["direction_selectivity"]))
    for m, (res, colour, dx) in enumerate(((before["direction_selectivity"], c["faint"], 0), (after["direction_selectivity"], c["red"], bw + 2))):
        r = res["R T5a"]["responses"]
        for k, d in enumerate(DIRS):
            h = (y1 - y0) * r[d] / top
            x = x0 + k * 80 + dx
            out.append(f'<rect x="{x:.1f}" y="{y1 - h:.1f}" width="{bw}" height="{h:.1f}" fill="{colour}"/>')
    out.append(f'<line x1="{x0}" y1="{y1}" x2="{x0 + 4 * 80 - 30}" y2="{y1}" stroke="{c["rule"]}"/>')
    for k, d in enumerate(DIRS):
        out.append(text(x0 + k * 80 + bw + 1, y1 + 16, SHORT[d], "tick", "middle"))
    out.append(text(24, y1 + 40, f"model 001 prefers up (DSI {before['direction_selectivity']['R T5a']['dsi']:.2f}): wrong", "tick"))
    ratio = after["direction_selectivity"]["R T5a"]["responses"]["front-to-back"] / before["direction_selectivity"]["R T5a"]["responses"]["front-to-back"]
    out.append(text(24, y1 + 56, f"fine-tuned prefers front to back (DSI {after['direction_selectivity']['R T5a']['dsi']:.2f}), as T5a does,", "tick"))
    out.append(text(24, y1 + 72, f"but at {ratio:.1f} of model 001's response; all 16 subtypes right", "tick"))

    # --- middle: polarity
    px0, px1, py0, py1 = 430, 690, 110, 330
    lo, hi = -0.35, 0.65
    sx = lambda v: px0 + (px1 - px0) * (v - lo) / (hi - lo)
    sy = lambda v: py1 - (py1 - py0) * (v - lo) / (hi - lo)
    out.append(text(px0 - 30, 96, "Polarity index, signed so that right is positive", "val"))
    out.append(f'<rect x="{sx(0):.1f}" y="{sy(hi):.1f}" width="{sx(hi) - sx(0):.1f}" height="{sy(0) - sy(hi):.1f}" fill="{c["red"]}" fill-opacity="0.06"/>')
    out.append(f'<line x1="{sx(0):.1f}" y1="{py0}" x2="{sx(0):.1f}" y2="{py1}" stroke="{c["rule"]}"/>')
    out.append(f'<line x1="{px0}" y1="{sy(0):.1f}" x2="{px1}" y2="{sy(0):.1f}" stroke="{c["rule"]}"/>')
    t_before = before["polarity"]["flow/0000/001"]["types"]
    t_after = after["polarity"]["types"]
    for name, row in t_after.items():
        s = row["known"]
        a, b = s * t_before[name]["fri"], s * row["fri"]
        a, b = float(np.clip(a, lo, hi)), float(np.clip(b, lo, hi))
        changed = (a > 0) != (b > 0)
        colour = c["red"] if b > 0 else c["muted"]
        out.append(f'<circle cx="{sx(a):.1f}" cy="{sy(b):.1f}" r="{4.5 if changed or name == "L2" else 3}" fill="{colour}"/>')
        if changed or name == "L2":
            dy = {"Tm2": -8, "R3": 14}.get(name, 4)
            out.append(text(sx(a) + 7, sy(b) + dy, name, "tick"))
    out.append(text((px0 + px1) / 2, py1 + 18, "model 001", "tick", "middle"))
    out.append(f'<text x="{px0 - 14}" y="{(py0 + py1) / 2:.1f}" class="tick" text-anchor="middle" transform="rotate(-90 {px0 - 14} {(py0 + py1) / 2:.1f})">fine-tuned</text>')
    out.append(text(px0 - 30, py1 + 40, f"{after['polarity']['correct']} of 32 right (model 001: 29): R3 and Tm2 crossed over;", "tick"))
    out.append(text(px0 - 30, py1 + 56, "L2, left out of the loss, is still wrong", "tick"))

    # --- right: looming
    tx0, tx1 = 770, 1040
    tr = loom["trace_hz"]["fastL"]
    bins = len(tr["LC4 L"])
    tb = (np.arange(bins) + 0.5) * SECONDS / bins
    keep = tb >= T0
    tx = lambda t: tx0 + (tx1 - tx0) * (t - T0) / (SECONDS - T0)
    out.append(text(tx0, 96, "A loom on the left, fine-tuned eye", "val"))
    rows = [("LC4", 30), ("LPLC2", 30), ("DNp01", 40)]
    labels = {"LC4": "LC4", "LPLC2": "LPLC2", "DNp01": "giant fiber"}
    for k, (cell, top) in enumerate(rows):
        yb = 160 + k * 70
        out.append(f'<line x1="{tx0}" y1="{yb}" x2="{tx1}" y2="{yb}" stroke="{c["rule"]}"/>')
        for side, colour, width in (("R", c["faint"], 1.2), ("L", c["red"], 1.8)):
            v = np.asarray(tr[f"{cell} {side}"])[keep]
            pts = " ".join(f"{tx(t):.1f},{yb - 50 * min(x, top) / top:.1f}" for t, x in zip(tb[keep], v))
            out.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="{width}"/>')
        peak = float(np.max(tr[f"{cell} L"]))
        out.append(text(tx0 - 6, yb - 30, labels[cell], "tick", "end"))
        out.append(text(tx1 + 4, yb - 40, f"{peak:.0f} Hz", "tick"))
    out.append(f'<line x1="{tx(CONTACT):.1f}" y1="{110}" x2="{tx(CONTACT):.1f}" y2="{300}" stroke="{c["muted"]}" stroke-dasharray="3 3"/>')
    out.append(text(tx(CONTACT), 316, "contact", "tick", "middle"))
    out.append(text(tx0, 340, "loomed side in red, the other in grey; peaks of", "tick"))
    out.append(text(tx0, 356, "at least 20 Hz asked of LC4 and LPLC2, a bar", "tick"))
    out.append(text(tx0, 372, "model 001 already met; looming wasn't in the loss", "tick"))

    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    peaks = {k: max(loom["trace_hz"]["fastL"][f"{k} L"]) for k in ("LC4", "LPLC2", "DNp01")}
    title = ("Rung 3: flyvis's model 001 fine-tuned with rung 3's direction test and polarities in its loss. T5a, which "
             "weakly preferred up, now prefers front to back in the eye, though with a smaller response; 31 of 32 "
             f"polarities are right; and a loom on the left still drives the loomed side's LC4 and LPLC2 to peaks of "
             f"{peaks['LC4']:.0f} and {peaks['LPLC2']:.0f} Hz and the giant fiber to {peaks['DNp01']:.0f} Hz")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    before, after, loom = load()
    for theme in THEMES:
        path = OUT / f"rung3-{theme}.svg"
        path.write_text(figure(theme, before, after, loom))
        print(path)


if __name__ == "__main__":
    main()
