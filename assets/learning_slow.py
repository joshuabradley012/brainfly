"""Rung 9's learning test with the slow Kenyon cell current, animated, drawn from a saved run (nothing by hand).

    python assets/learning_slow.py      # writes assets/learning_slow-light.svg and assets/learning_slow-dark.svg

experiments/learning_pilot12.py: learning_movie.py's protocol (learning pilot 11's, the receptor input the evidence
supports, MBON11 held near 6 Hz) with every Kenyon cell-to-MBON synapse in a slow current (mb_calibration5.py). In the
top left panel, also the response before pairing with the model's old 5 ms current (learning_movie.py). Each panel
is MBON11's rate (mean of 4 seeds of 8 flies, smoothed as Hige et al. smoothed theirs: a Gaussian with an SD of 50 ms; one
scale throughout) to one odor before (grey) and after (red) pairing one odor with dopamine: top, 3-octanol paired; bottom,
4-methylcyclohexanol paired; left, the response to 3-octanol; right, to 4-methylcyclohexanol. In the top row, the points
of flies' PSTH before pairing as research_notes/Rung 9 learning data/mbon11_input.md reads them off Hige et al. 2015's
Fig. 1E (the same group of flies, 3-octanol paired; the bottom row's flies, Fig. S3, have no PSTH read). Labelled with
the evoked spikes over 0-1.4 s before and after, flies' (Fig. 1F and S3) and the band rung 9's test set for the drop.
The recording plays at half speed, then holds.
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
W, H = 1120, 716
OCT, MCH = "3-octanol", "4-methylcyclohexanol"
COLS, CW = (80, 620), 430
ROWS, RH = (190, 460), 170
HOLD, SPEED, SD_S = 3.0, 0.5, 0.05
# by (paired odor, tested odor): flies' evoked spikes before pairing and drop (Hige et al. 2015, Fig. 1F and S3;
# research_notes/Rung 9 learning data/hige2015_specificity.md) and rung 9's band (rung9_learning.py)
FLIES = {(OCT, OCT): (118, 0.80, 0.65, None), (OCT, MCH): (110, 0.27, 0.10, 0.45), (MCH, OCT): (94.5, 0.38, 0.15, 0.50),
         (MCH, MCH): (103, 0.76, 0.65, None)}
# flies' PSTH before pairing, (s from the odor's onset, spikes/s), Fig. 1E as mbon11_input.md 2.3 reads it: rise begins,
# peak, the middle of the response (its two ends), 1.15 s (3-octanol) and back near baseline
PSTH = {OCT: [(0.15, 6), (0.30, 137.5), (0.70, 97.5), (1.05, 97.5), (1.15, 80), (1.45, 6)],
        MCH: [(0.15, 6), (0.26, 135), (0.60, 100), (0.90, 100), (1.45, 6)]}


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def series(calls: list) -> dict:
    """{(paired odor or None, tested odor): rate} from the recording's calls, in learning_pilot4.variant's order: the six
    odors before pairing (4 seeds each), then for each pairing 8 trials of the paired odor (for its eligibility) and the
    paired and unpaired odors after, with the seeds they had before."""
    before, seeds = {}, {}
    for k in range(6):
        group = calls[4 * k:4 * k + 4]
        odor = group[0]["odor"]
        assert all(c["odor"] == odor for c in group)
        before[odor], seeds[odor] = np.mean([c["mbon11_hz"] for c in group], 0), [c["seed"] for c in group]
    out = {(None, od): before[od] for od in (OCT, MCH)}
    for i, (paired, unpaired) in enumerate(((OCT, MCH), (MCH, OCT))):
        start = 24 + 16 * i + 8
        for k, od in enumerate((paired, unpaired)):
            group = calls[start + 4 * k:start + 4 * k + 4]
            assert [c["odor"] for c in group] == [od] * 4 and [c["seed"] for c in group] == seeds[od]
            out[(paired, od)] = np.mean([c["mbon11_hz"] for c in group], 0)
    assert len(calls) == 24 + 32
    return out


def smooth(v: np.ndarray, dt: float) -> np.ndarray:
    """A Gaussian with an SD of SD_S, as Hige et al. smoothed their PSTHs, cut at 3 SD; the ends padded with their values."""
    half = int(round(3 * SD_S / dt))
    k = np.exp(-0.5 * (np.arange(-half, half + 1) * dt / SD_S) ** 2)
    return np.convolve(np.pad(v, half, mode="edge"), k / k.sum(), mode="valid")


def shape(v: np.ndarray, ts: np.ndarray, dt: float) -> dict:
    """The raw and smoothed peaks, the share of the evoked spikes in the first 0.3 s and the rate from 0.5 to 1 s."""
    rest = v[ts < 0].mean()
    window = (ts > 0) & (ts < 1.4)
    evoked = v[window] - rest
    return {"peak_raw": v.max(), "peak": smooth(v, dt).max(), "t_peak": ts[np.argmax(smooth(v, dt))],
            "early": evoked[ts[window] < 0.3].sum() / evoked.sum(), "late": v[(ts > 0.5) & (ts < 1.0)].mean()}


def figure(theme: str, d: dict, old: dict) -> str:
    c = THEMES[theme]
    se = d["series"]
    s = {(None, OCT): np.asarray(se[f"pre {OCT}"]["hz"]), (None, MCH): np.asarray(se[f"pre {MCH}"]["hz"])}
    for paired in (OCT, MCH):
        for od in (OCT, MCH):
            s[(paired, od)] = np.asarray(se[f"{paired} paired, {od}"]["hz"])
    fast = series(old["calls"])[(None, OCT)]
    pairings = {p["paired"]: p["spikes"] for p in d["pairings"]}
    t0, dt = d["t0"], d["bin_s"]
    n = len(s[(None, OCT)])
    ts = t0 + (np.arange(n) + 0.5) * dt
    span = n * dt
    sweep = span / SPEED
    loop = sweep + HOLD
    top = 20.0 * np.ceil(1.2 * max(max(smooth(v, dt).max() for v in s.values()), 140.0) / 20.0)
    step = next(x for x in (10, 20, 25, 50, 100) if top / x <= 5)
    oo, om = pairings[OCT][OCT]["drop"], pairings[OCT][MCH]["drop"]
    mm, mo = pairings[MCH][MCH]["drop"], pairings[MCH][OCT]["drop"]
    sh, shf = shape(s[(None, OCT)], ts, dt), shape(fast, ts, dt)
    pre = {od: pairings[OCT][od]["pre"] for od in (OCT, MCH)}
    out = [text(24, 30, "Rung 9's learning test with the slow Kenyon cell current", "lab"),
           text(24, 50, f"With the Kenyon cell current as slow as flies' flash EPSC, MBON11's response to 3-octanol holds: "
                f"{sh['late']:.0f} spikes/s from 0.5 s to the odor's end (before {shf['late']:.0f}; flies 95-100),", "note"),
           text(24, 68, f"{pre[OCT]:.0f} evoked spikes (before 39; flies 118), {100 * sh['early']:.0f}% of them in the first 0.3 s (before "
                f"{100 * shf['early']:.0f}%). Pairing 3-octanol cuts its response {100 * oo:.0f}% (flies 80%) and 4-methylcyclohexanol's", "note"),
           text(24, 86, f"{100 * om:.0f}% (flies 27%); pairing 4-methylcyclohexanol cuts its own {100 * mm:.0f}% (flies 76%) but 3-octanol's "
                f"only {100 * mo:.0f}% (flies 38%): its Kenyon cells are still too few.", "note"),
           text(24, 104, f"To 4-methylcyclohexanol MBON11 gains only {pre[MCH]:.1f} spikes (flies 110).", "note")]
    for r, paired in enumerate((OCT, MCH)):
        y0 = ROWS[r]
        out.append(text(24, y0 - 36, f"{paired} paired with dopamine", "row"))
        for k, odor in enumerate((OCT, MCH)):
            x0 = COLS[k]
            tx = lambda t, x0=x0: x0 + CW * (t - t0) / span
            ty = lambda v, y0=y0: y0 + RH - RH * min(max(v, 0.0), top) / top
            out.append(f'<rect x="{tx(0):.1f}" y="{y0}" width="{tx(1.0) - tx(0):.1f}" height="{RH}" fill="{c["ink"]}" fill-opacity="0.05"/>')
            out.append(text(tx(0) + 4, y0 + 12, "odor", "tiny"))
            for v in np.arange(0, top + 1, step):
                out.append(f'<line x1="{x0}" y1="{ty(v):.1f}" x2="{x0 + CW}" y2="{ty(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.45}"/>')
                out.append(text(x0 - 6, ty(v) + 4, f"{v:.0f}", "tick", "end"))
            out.append(text(x0 + 4, y0 + 12, "spikes/s", "tiny"))
            for tt in (-0.5, 0, 0.5, 1.0, 1.5):
                out.append(text(tx(tt), y0 + RH + 16, f"{tt:g}".replace("-", "−"), "tick", "middle"))
            out.append(text(x0, y0 - 10, f"MBON11's response to {odor}", "val"))
            spikes = pairings[paired][odor]
            if r == 0 and k == 0:                       # the model's old 5 ms current, before pairing
                pts = " ".join(f"{tx(t):.1f},{ty(x):.1f}" for t, x in zip(ts, smooth(fast, dt)))
                out.append(f'<polyline points="{pts}" fill="none" stroke="{c["faint"]}" stroke-width="1.2" stroke-dasharray="4 3">'
                           f'<title>before pairing, with the old 5 ms current (learning_movie.py): peak {shf["peak"]:.0f} spikes/s</title></polyline>')
            if r == 0:                                  # flies' PSTH before pairing: the points read, joined
                pts = " ".join(f"{tx(t):.1f},{ty(v):.1f}" for t, v in PSTH[odor])
                out.append(f'<polyline points="{pts}" fill="none" stroke="{c["ink"]}" stroke-width="1" stroke-dasharray="2 3"/>')
                for t, v in PSTH[odor]:
                    out.append(f'<circle cx="{tx(t):.1f}" cy="{ty(v):.1f}" r="3.2" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.3">'
                               f'<title>flies before pairing (Hige et al. 2015, Fig. 1E, read off the figure): {v:g} spikes/s at {t:g} s</title></circle>')
            for key, color, width, label in (((None, odor), "faint", 1.6, f"before pairing: {spikes['pre']} evoked spikes"),
                                             ((paired, odor), "red", 2.2, f"after pairing: {spikes['post']} evoked spikes")):
                pts = " ".join(f"{tx(t):.1f},{ty(x):.1f}" for t, x in zip(ts, smooth(s[key], dt)))
                out.append(f'<polyline clip-path="url(#sweep{r}{k})" points="{pts}" fill="none" stroke="{c[color]}" stroke-width="{width}"><title>{label}</title></polyline>')
            fly_pre, fly, lo, hi = FLIES[(paired, odor)]
            drop = spikes["drop"]
            band = f"{100 * lo:.0f}% or more" if hi is None else f"{100 * lo:.0f}-{100 * hi:.0f}%"
            ok = drop >= lo if hi is None else lo <= drop <= hi
            out.append(text(x0 + CW - 8, y0 + 16, f"{spikes['pre']:.1f} → {spikes['post']:.1f} evoked spikes, {100 * drop:.0f}% fewer", "val", "end"))
            out.append(text(x0 + CW - 8, y0 + 32, f"flies: {fly_pre:g} before, {100 * fly:.0f}% fewer", "tick", "end"))
            out.append(text(x0 + CW - 8, y0 + 46, f"rung 9 asks for {band} ({'met' if ok else 'missed'})", "tick", "end"))
            out.append(f'<clipPath id="sweep{r}{k}"><rect class="reveal{r}{k}" x="{x0}" y="{y0 - 4}" width="{CW + 2}" height="{RH + 8}"/></clipPath>')
            out.append(f'<path class="head{r}{k}" d="M{x0} {y0}V{y0 + RH}" stroke="{c["ink"]}" stroke-width="1.2"/>')
    for x0 in COLS:
        out.append(text(x0 + CW / 2, ROWS[1] + RH + 34, "time from the odor's onset (s)", "tick", "middle"))
    lx, ly = COLS[0], H - 32
    out.append(f'<line x1="{lx}" y1="{ly - 4}" x2="{lx + 22}" y2="{ly - 4}" stroke="{c["faint"]}" stroke-width="1.6"/>')
    out.append(text(lx + 28, ly, "before pairing", "tick"))
    out.append(f'<line x1="{lx + 120}" y1="{ly - 4}" x2="{lx + 142}" y2="{ly - 4}" stroke="{c["red"]}" stroke-width="2.2"/>')
    out.append(text(lx + 148, ly, "after pairing", "tick"))
    out.append(f'<line x1="{lx + 236}" y1="{ly - 4}" x2="{lx + 266}" y2="{ly - 4}" stroke="{c["ink"]}" stroke-width="1" stroke-dasharray="2 3"/>')
    out.append(f'<circle cx="{lx + 251}" cy="{ly - 4}" r="3.2" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="1.3"/>')
    out.append(text(lx + 272, ly, "flies before pairing (Hige et al. 2015, read off Fig. 1E)", "tick"))
    out.append(f'<line x1="{lx + 590}" y1="{ly - 4}" x2="{lx + 612}" y2="{ly - 4}" stroke="{c["faint"]}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    out.append(text(lx + 618, ly, "before, with the old 5 ms current", "tick"))
    out.append(text(lx, H - 12, "The model: mean of 4 seeds of 8 flies, smoothed as Hige et al. smoothed theirs (a Gaussian, SD 50 ms, which "
                    "also spreads each rise earlier). Evoked spikes: 0-1.4 s, above the rest.", "tick"))
    end = 100 * sweep / loop
    reveals = " ".join(f".reveal{r}{k} {{ transform-origin: {COLS[k]}px 0; animation: reveal {loop}s linear infinite; }}"
                       for r in range(2) for k in range(2))
    heads = ", ".join(f".head{r}{k}" for r in range(2) for k in range(2))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .row {{ font-size: 14px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    {heads} {{ opacity: 0; }}
    @media (prefers-reduced-motion: no-preference) {{
      {reveals}
      {heads} {{ animation: head {loop}s linear infinite; }}
    }}
    @keyframes reveal {{ 0% {{ transform: scaleX(0.001); }} {end:.2f}%, 100% {{ transform: scaleX(1); }} }}
    @keyframes head {{ 0% {{ opacity: 1; transform: translateX(0); }} {end:.2f}% {{ opacity: 1; transform: translateX({CW}px); }}
                       {end + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
    """
    title = "Rung 9's learning test with the slow Kenyon cell current: MBON11's responses before and after pairing each odor"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "learning_pilot12.json").read_text())
    old = json.loads((ROOT / "experiments" / "learning_movie.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"learning_slow-{theme}.svg"
        path_.write_text(figure(theme, d, old))
        print(f"{path_} ({path_.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
