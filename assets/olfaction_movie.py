"""The olfactory pathway answering two odors, animated (rung 9), drawn from a saved recording (nothing by hand).

    python assets/olfaction_movie.py      # writes assets/olfaction_movie-light.svg and assets/olfaction_movie-dark.svg

experiments/olfaction_movie.py: the current model (odor_probe60.py's antennal lobe, mb_calibration4.py's mushroom body) with
the receptor input the evidence supports, 3-octanol (left) and 4-methylcyclohexanol (right) for 1 s from t = 0. Top: each
glomerulus's uniglomerular PNs (rows, the glomeruli either odor drives to 20 spikes/s or more, ordered by 3-octanol's
response), their mean rate over 8 flies in 40 ms bins, darker for more. Middle: one fly's Kenyon cells that spike to
either odor (rows: those answering both first, then 3-octanol's alone, then 4-methylcyclohexanol's alone), each spike a
tick at 10 ms resolution. Bottom: APL's release and MBON11's rate (50 ms means over 8 flies). The recording plays in real
time, then holds.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/looming.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", faint="#8c959f"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", faint="#6e7681"),
}
W, H = 1120, 760
ODORS = ("3-octanol", "4-methylcyclohexanol")
COLS = (70, 600)                  # each odor's column, x of its time axis's start
CW = 450                          # width of a column's time axis
PN_Y, PN_H = 132, 170
KC_Y, KC_H = 352, 210
APL_Y, APL_H = 600, 50
MB_Y, MB_H = 680, 50
BIN = 0.04
HOLD = 3.0
PN_MAX = 150.0


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    t0, t1, piece = d["t0"], d["t1"], d["piece_s"]
    span = t1 - t0
    loop = span + HOLD
    rows = {od: d["odors"][od] for od in ODORS}
    names = rows[ODORS[0]]["glomeruli"]
    pn = {od: np.array(rows[od]["pn_hz"]) for od in ODORS}                    # (pieces, glomeruli)
    n_bin = int(round(BIN / piece))
    binned = {od: pn[od][: (len(pn[od]) // n_bin) * n_bin].reshape(-1, n_bin, len(names)).mean(1) for od in ODORS}
    peak = np.maximum(binned[ODORS[0]].max(0), binned[ODORS[1]].max(0))
    order = [i for i in np.argsort(-binned[ODORS[0]].max(0)) if peak[i] >= 20.0]
    spikes = {od: {int(k): v for k, v in rows[od]["kc_spikes"].items()} for od in ODORS}
    a, b = set(spikes[ODORS[0]]), set(spikes[ODORS[1]])
    first = lambda cell, od: min(spikes[od][cell]) if cell in spikes[od] else 9.0
    kc_order = (sorted(a & b, key=lambda k: first(k, ODORS[0])) + sorted(a - b, key=lambda k: first(k, ODORS[0]))
                + sorted(b - a, key=lambda k: first(k, ODORS[1])))
    n_kc = len(kc_order)
    out = [text(24, 30, "The olfactory pathway answering two odors", "lab"),
           text(24, 50, f"3-octanol drives many glomeruli and {len(a)} of one fly's {d['kenyon_cells']} Kenyon cells; 4-methylcyclohexanol, "
                f"with the receptor input the evidence supports, drives two strongly and {len(b)} Kenyon cells,", "note"),
           text(24, 68, f"{len(a & b)} of them shared. That gap is what keeps rung 9's learning test failing: pairing "
                "4-methylcyclohexanol can barely touch 3-octanol's Kenyon cells.", "note")]
    for k, od in enumerate(ODORS):
        x0 = COLS[k]
        tx = lambda t, x0=x0: x0 + CW * (t - t0) / span
        out.append(text(x0, 108, od, "lab"))
        # projection neurons
        gh = PN_H / max(len(order), 1)
        bw = CW * BIN / span
        out.append(f'<g clip-path="url(#sweep{k})">')
        for r, gi in enumerate(order):
            y = PN_Y + r * gh
            for j, v in enumerate(binned[od][:, gi]):
                if v >= 2.0:
                    op = min(v / PN_MAX, 1.0)
                    out.append(f'<rect x="{tx(t0 + j * BIN):.1f}" y="{y:.1f}" width="{bw + 0.3:.1f}" height="{gh + 0.3:.1f}" '
                               f'fill="{c["red"]}" fill-opacity="{op:.2f}"/>')
        out.append("</g>")
        for r, gi in enumerate(order):
            if k == 0 or True:
                if r % 3 == 0 or len(order) <= 24:
                    out.append(text(x0 - 6, PN_Y + (r + 0.75) * gh, names[gi], "tiny", "end"))
        out.append(f'<rect x="{x0}" y="{PN_Y}" width="{CW}" height="{PN_H}" fill="none" stroke="{c["rule"]}"/>')
        # Kenyon cells
        kh = KC_H / max(n_kc, 1)
        out.append(f'<g clip-path="url(#sweep{k})">')
        for r, cell in enumerate(kc_order):
            for s in spikes[od].get(cell, []):
                out.append(f'<rect x="{tx(s) - 0.8:.1f}" y="{KC_Y + r * kh:.1f}" width="1.6" height="{max(kh, 0.6):.2f}" fill="{c["ink"]}"/>')
        out.append("</g>")
        out.append(f'<rect x="{x0}" y="{KC_Y}" width="{CW}" height="{KC_H}" fill="none" stroke="{c["rule"]}"/>')
        for lo, hi, label in ((0, len(a & b), "both"), (len(a & b), len(a & b) + len(a - b), "3-octanol only"),
                              (len(a & b) + len(a - b), n_kc, "4-methylcyclohexanol only")):
            if hi > lo and k == 0:                     # inside, at the right edge: the left margin is narrow
                out.append(text(x0 + CW - 4, KC_Y + (lo + hi) / 2 * kh + 4, label, "tiny", "end"))
            if hi > lo:
                out.append(f'<line x1="{x0}" y1="{KC_Y + hi * kh:.1f}" x2="{x0 + CW}" y2="{KC_Y + hi * kh:.1f}" stroke="{c["rule"]}" stroke-dasharray="2 3"/>')
        # APL and MBON11
        ts = t0 + (np.arange(len(rows[od]["apl_release_hz"])) + 0.5) * piece
        for y0, hh, series, top, label in ((APL_Y, APL_H, rows[od]["apl_release_hz"], 40.0, "APL release (Hz)"),
                                           (MB_Y, MB_H, np.convolve(rows[od]["mbon11_hz"], np.ones(5) / 5, mode="same"), 100.0, "MBON11 (spikes/s)")):
            sy = lambda v, y0=y0, hh=hh, top=top: y0 + hh - hh * min(max(v, 0.0), top) / top
            out.append(f'<line x1="{x0}" y1="{y0 + hh}" x2="{x0 + CW}" y2="{y0 + hh}" stroke="{c["rule"]}"/>')
            out.append(text(x0 - 6, y0 + 8, f"{top:g}", "tiny", "end"))
            out.append(text(x0 - 6, y0 + hh, "0", "tiny", "end"))
            pts = " ".join(f"{tx(t):.1f},{sy(v):.1f}" for t, v in zip(ts, series))
            out.append(f'<polyline clip-path="url(#sweep{k})" points="{pts}" fill="none" stroke="{c["red"] if "APL" in label else c["ink"]}" stroke-width="1.6"/>')
            out.append(text(x0 + 4, y0 - 4, label, "tick"))
        # odor bar, time axis
        out.append(f'<rect x="{tx(0):.1f}" y="{PN_Y - 10}" width="{tx(1.0) - tx(0):.1f}" height="5" fill="{c["faint"]}"/>')
        out.append(text(tx(0.5), PN_Y - 14, "odor", "tiny", "middle"))
        for s in (0.0, 0.5, 1.0, 1.5):
            out.append(f'<line x1="{tx(s):.1f}" y1="{MB_Y + MB_H}" x2="{tx(s):.1f}" y2="{MB_Y + MB_H + 4}" stroke="{c["muted"]}"/>')
            out.append(text(tx(s), MB_Y + MB_H + 16, f"{s:g} s", "tick", "middle"))
        out.append(f'<clipPath id="sweep{k}"><rect class="reveal{k}" x="{x0}" y="{PN_Y - 20}" width="{CW + 2}" height="{MB_Y + MB_H - PN_Y + 24}"/></clipPath>')
        out.append(f'<path class="head{k}" d="M{x0} {PN_Y}V{MB_Y + MB_H}" stroke="{c["ink"]}" stroke-width="1.2"/>')
    out.append(text(COLS[0] + 150, 108, "projection neurons, by glomerulus (40 ms bins)", "tick", "start"))
    out.append(text(COLS[0], KC_Y - 8, "Kenyon cells (one fly), each spike a tick", "tick", "start"))
    end = 100 * span / loop
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 9px; fill: {c["muted"]}; }}
    .head0, .head1 {{ opacity: 0; }}
    @media (prefers-reduced-motion: no-preference) {{
      .reveal0 {{ transform-origin: {COLS[0]}px 0; animation: reveal {loop}s linear infinite; }}
      .reveal1 {{ transform-origin: {COLS[1]}px 0; animation: reveal {loop}s linear infinite; }}
      .head0, .head1 {{ animation: head {loop}s linear infinite; }}
    }}
    @keyframes reveal {{ 0% {{ transform: scaleX(0.001); }} {end:.2f}%, 100% {{ transform: scaleX(1); }} }}
    @keyframes head {{ 0% {{ opacity: 1; transform: translateX(0); }} {end:.2f}% {{ opacity: 1; transform: translateX({CW}px); }}
                       {end + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
    """
    title = ("The olfactory pathway answering 3-octanol and 4-methylcyclohexanol: projection neurons by glomerulus, one fly's "
             "Kenyon cells, APL and MBON11")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "olfaction_movie.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"olfaction_movie-{theme}.svg"
        path_.write_text(figure(theme, d))
        print(f"{path_} ({path_.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
