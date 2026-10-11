"""Rung 7's twitch with two activation models, drawn from saved results (nothing by hand).

    python assets/leg_activation.py      # writes assets/leg_activation-light.svg and assets/leg_activation-dark.svg

experiments/leg_activation_check.py: FlyMimic's tibia flexor pushing a fly's force probe, timed from the motor neuron's
spike at the soma (the muscle 2.5 ms later). Red: a calcium-like active state with a steep link (the Ding/Wilson
two-state model, research_notes/Embodied fly connectome simulation/muscle_activation.md, as given, nothing fitted). Ink:
MuJoCo's first-order activation with 10 ms deactivation; dashed: with the stated 40 ms. Shaded: flies (Azevedo et al.
2020): the twitch's peak at 17-23 ms and half gone 12-16 ms after it, two spikes giving 1.4-1.6 times one, and the
fast motor unit's plateau at 28-30 uN (the rate of flies' bursts wasn't reported; 120 Hz is shown).
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
W, H = 1120, 492
Y0, Y1 = 140, 394
PANELS = (  # (trace, x max ms, y max uN, title, x ticks)
    ("one spike", 60, 12, "One spike", (0, 20, 40, 60)),
    ("two spikes 12 ms apart", 80, 18, "Two spikes, 12 ms apart", (0, 20, 40, 60, 80)),
    ("17 spikes at 120 Hz", 300, 32, "17 spikes at 120 Hz", (0, 100, 200, 300)),
)
MODELS = (("two_state", "note's set", "red", None, "two-state"), ("first_order", "deactivation 10 ms", "ink", None, "first-order, 10 ms"),
          ("first_order", "deactivation 40 ms", "muted", "6 4", "first-order, 40 ms"))


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    fly = d["fly"]
    twitch_uN = fly["spike_uN"]
    out = [text(24, 30, "Rung 7's twitch: a calcium-like active state against MuJoCo's first-order activation", "lab"),
           text(24, 50, "FlyMimic's tibia flexor against a fly's force probe, from the motor neuron's spike. Shaded: flies "
                "(Azevedo et al. 2020); 120 Hz stands in for flies' unreported burst rate.", "note"),
           text(24, 68, "The two-state model relaxes and plateaus like a fly's muscle but sums two spikes too strongly; "
                "the first-order one fits the twitch and the doublet but not the plateau.", "note")]
    pw, gap, x0 = 300, 66, 70
    for i, (key, xmax, ymax, title, xticks) in enumerate(PANELS):
        px = x0 + i * (pw + gap)
        sx = lambda t, px=px, xmax=xmax: px + pw * t / xmax
        sy = lambda v, ymax=ymax: Y1 - (Y1 - Y0) * min(v, ymax) / ymax
        out.append(text(px, Y0 - 16, title, "val"))
        step = 4 if ymax <= 12 else 6 if ymax <= 18 else 10
        for v in range(0, ymax + 1, step):
            out.append(f'<line x1="{px}" y1="{sy(v):.1f}" x2="{px + pw}" y2="{sy(v):.1f}" stroke="{c["rule"]}" stroke-opacity="{1 if v == 0 else 0.5}"/>')
            out.append(text(px - 6, sy(v) + 4, f"{v}", "tick", "end"))
        for t in xticks:
            out.append(text(sx(t), Y1 + 16, f"{t}", "tick", "middle"))
        out.append(text(px + pw / 2, Y1 + 34, "ms from the spike", "tick", "middle"))
        if i == 0:
            out.append(f'<text transform="translate({px - 40},{(Y0 + Y1) / 2}) rotate(-90)" class="tick" text-anchor="middle">probe force (uN)</text>')
            lo, hi = fly["peak_ms"]
            out.append(f'<rect x="{sx(lo):.1f}" y="{Y0}" width="{sx(hi) - sx(lo):.1f}" height="{Y1 - Y0}" fill="{c["ink"]}" fill-opacity="0.08"><title>flies: peak at 17-23 ms</title></rect>')
            out.append(text((sx(lo) + sx(hi)) / 2, Y0 + 12, "flies' peak", "tick", "middle"))
            a, b = lo + fly["half_decay_ms"][0], hi + fly["half_decay_ms"][1]
            out.append(f'<rect x="{sx(a):.1f}" y="{sy(twitch_uN * 0.5) - 3:.1f}" width="{sx(b) - sx(a):.1f}" height="6" rx="3" fill="{c["ink"]}" fill-opacity="0.18"><title>flies: half gone 12-16 ms after the peak</title></rect>')
            out.append(text((sx(a) + sx(b)) / 2, sy(twitch_uN * 0.5) - 8, "half gone", "tick", "middle"))
            out.append(f'<line x1="{px}" y1="{sy(twitch_uN):.1f}" x2="{px + pw}" y2="{sy(twitch_uN):.1f}" stroke="{c["ink"]}" stroke-dasharray="2 3"><title>flies: 9 uN per spike</title></line>')
            out.append(text(px + pw, sy(twitch_uN) - 5, "flies' 9 uN", "tick", "end"))
        elif i == 1:
            lo, hi = fly["two_spike_ratio"]
            out.append(f'<rect x="{px}" y="{sy(hi * twitch_uN):.1f}" width="{pw}" height="{sy(lo * twitch_uN) - sy(hi * twitch_uN):.1f}" fill="{c["ink"]}" fill-opacity="0.08"><title>flies: 1.4-1.6 times one spike</title></rect>')
            out.append(text(px + pw - 4, sy(hi * twitch_uN) - 5, "flies: 1.4-1.6 x one spike", "tick", "end"))
        else:
            lo, hi = fly["plateau_uN"]
            out.append(f'<rect x="{px}" y="{sy(hi):.1f}" width="{pw}" height="{sy(lo) - sy(hi):.1f}" fill="{c["ink"]}" fill-opacity="0.08"><title>flies: 28-30 uN plateau</title></rect>')
            out.append(text(px + pw - 4, sy(hi) - 5, "flies' plateau", "tick", "end"))
        for group, name, color, dash, label in MODELS:
            tr = d[group][name]["traces"]
            ys = tr[key]
            pts = " ".join(f"{sx(k * tr['dt_ms']):.1f},{sy(max(v, 0.0)):.1f}" for k, v in enumerate(ys) if k * tr["dt_ms"] <= xmax)
            dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
            out.append(f'<polyline points="{pts}" fill="none" stroke="{c[color]}" stroke-width="2"{dash_attr} stroke-linejoin="round"><title>{label}</title></polyline>')
    lx, ly = x0, 96                                                  # legend: one row above the panels
    for k, (group, name, color, dash, label) in enumerate(MODELS):
        x = lx + 170 * k
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{x}" y1="{ly}" x2="{x + 24}" y2="{ly}" stroke="{c[color]}" stroke-width="2"{dash_attr}/>')
        out.append(text(x + 30, ly + 4, label, "tick"))
    v = {name: d[g][name] for g, name, *_ in MODELS}
    s = v["note's set"]
    out.append(text(x0, H - 30, f"Two-state: twitch {s['single_spike']['peak_uN']} uN, peak {s['single_spike']['peak_ms']} ms, half gone "
                    f"{s['single_spike']['half_decay_ms']} ms after it, two spikes {s['two_spike_ratio']['12 ms']} x one. First-order, 10 ms: "
                    f"{v['deactivation 10 ms']['single_spike']['peak_uN']} uN, {v['deactivation 10 ms']['single_spike']['peak_ms']} ms, "
                    f"{v['deactivation 10 ms']['single_spike']['half_decay_ms']} ms, {v['deactivation 10 ms']['two_spike_ratio']['12 ms']} x.", "tick"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    title = "Rung 7's twitch: FlyMimic's tibia flexor with a two-state and a first-order activation, against flies"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "leg_activation_check.json").read_text())
    for theme in THEMES:
        path_ = OUT / f"leg_activation-{theme}.svg"
        path_.write_text(figure(theme, d))
        print(path_)


if __name__ == "__main__":
    main()
