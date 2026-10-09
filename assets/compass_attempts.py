"""Where the compass's bump sits, attempt by attempt: the README's static summary of rung 4's head-direction runs.

    python assets/compass_attempts.py       # writes assets/compass_attempts-light.svg and -dark.svg

Each panel: the share of rung 4's measurement windows (8 runs of 300 s) that the bump spent at each of the ellipsoid
body's 16 wedges, with the position entropy and the two bridge sides' resultants. Rung 4 asks an entropy of at least
0.9 and resultants under 0.6 (with a strong bump that drifts at a fly's rate). From the saved results of
ring_insitu.py, rung4_rest.py, ring_anneal.py (averaged offsets), rung4_anneal.py, ring_longruns.py, ring_scaling.py
(averaged factors) and rung4_scaling.py.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/compass.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117"),
}
W, H = 1120, 300
X0, PW, GAP, Y0, Y1 = 24, 132, 20, 126, 210


def load(path: str, *keys: str) -> dict:
    d = json.loads((ROOT / "experiments" / path).read_text())
    for k in keys:
        d = d[k]
    return d


def panels() -> list[dict]:
    rows = [("Exploratory run", ("80 rounds of offset", "homeostasis in place"), load("ring_insitu.json")),
            ("Attempt 3", ("the same, fresh seeds", "pre-registered"), load("rung4_rest/intact.json")),
            ("Annealed", ("attempt 3's brain,", "40 more rounds"), load("ring_anneal.json", "measured", "averaged")),
            ("Attempt 4", ("annealed, fresh seeds", "pre-registered"), load("rung4_anneal/intact.json")),
            ("Long runs", ("attempt 4's brain,", "10 rounds of 300 s"), load("ring_longruns.json", "measured")),
            ("Synaptic scaling", ("outside synapses scaled,", "40 rounds"), load("ring_scaling.json", "measured", "averaged")),
            ("Attempt 5", ("scaling, fresh seeds", "pre-registered"), load("rung4_scaling/intact.json"))]
    out = []
    for title, sub, m in rows:
        motion, bump = m["bump_motion"], m["bump"]
        out.append({"title": title, "sub": sub, "hist": motion["position_histogram"], "entropy": motion["position_entropy"],
                    "resultants": (bump["L"]["resultant"], bump["R"]["resultant"]), "pass": bool(m["BUMP"])})
    return out


def text(x, y, s, cls, anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def figure(theme: str, ps: list[dict]) -> str:
    c = THEMES[theme]
    out = [text(X0, 34, "Where the compass's bump sits, run by run", "lab"),
           text(X0, 54, "share of time at each of the 16 wedges over 8 runs of 300 s; rung 4 asks a position entropy of at "
                "least 0.9 and resultants under 0.6", "note")]
    top = max(max(p["hist"]) for p in ps)
    for j, p in enumerate(ps):
        x0 = X0 + j * (PW + GAP)
        out.append(text(x0, Y0 - 44, p["title"], "val"))
        out.append(text(x0, Y0 - 28, p["sub"][0], "tick"))
        out.append(text(x0, Y0 - 14, p["sub"][1], "tick"))
        bw = PW / 16
        for k, v in enumerate(p["hist"]):
            y = Y1 - (Y1 - Y0) * v / top
            out.append(f'<rect x="{x0 + k * bw + 0.8:.1f}" y="{y:.1f}" width="{bw - 1.6:.1f}" height="{Y1 - y:.1f}" '
                       f'fill="{c["red"] if p["pass"] else c["muted"]}"/>')
        out.append(f'<line x1="{x0}" y1="{Y1}" x2="{x0 + PW}" y2="{Y1}" stroke="{c["rule"]}"/>')
        ok = lambda good: "" if good else " ✗"
        out.append(text(x0, Y1 + 20, f"entropy {p['entropy']:.2f}{ok(p['entropy'] >= 0.9)}", "tick"))
        out.append(text(x0, Y1 + 36, f"resultants {p['resultants'][0]:.2f}, {p['resultants'][1]:.2f}"
                        f"{ok(max(p['resultants']) < 0.6)}", "tick"))
        out.append(text(x0, Y1 + 56, "BUMP passes" if p["pass"] else "BUMP fails", "pass" if p["pass"] else "fail"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .pass {{ font-size: 12px; font-weight: 600; fill: {c["red"]}; }}
    .fail {{ font-size: 12px; font-weight: 600; fill: {c["muted"]}; }}
    """
    title = ("Where the simulated fly's head-direction bump sat over rung 4's measurement in seven runs: even in the exploratory "
             "run, lopsided on fresh seeds, even again after annealed homeostasis, leaning toward three wedges in the fourth "
             "attempt, pinned in one place by homeostasis on long runs, and even with synaptic scaling in the exploratory run, "
             "nearly even in the fifth attempt (still leaning toward the fourth's wedges), which passes")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    ps = panels()
    for theme in THEMES:
        path = OUT / f"compass_attempts-{theme}.svg"
        path.write_text(figure(theme, ps))
        print(path)


if __name__ == "__main__":
    main()
