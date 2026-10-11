"""The ladder figure in the README: the nine rungs and where each stands, read from the experiments'
saved verdicts wherever one exists (the rest of each line is the README's rung table, in short).

    python assets/ladder.py     # writes assets/ladder-light.svg and assets/ladder-dark.svg

A rung is "passed" only when its pre-registered test passed; "in progress" rungs list what is done
(filled marks) and what is still open (hollow marks).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {  # as in assets/loom.py
    "light": dict(ink="#1f2328", muted="#59636e", rule="#d1d9e0", red="#b8322a", paper="#ffffff", wash="#f6f8fa"),
    "dark": dict(ink="#e6edf3", muted="#9198a1", rule="#3d444d", red="#e5533f", paper="#0d1117", wash="#161b22"),
}
W, ROW, TOP = 1120, 58, 24
RAIL_X, RAIL_W = 36, 64


def verdict(name: str, *keys: str):
    """A saved result, or None if the experiment hasn't been run."""
    path = ROOT / "experiments" / f"{name}.json"
    if not path.exists():
        return None
    d = json.loads(path.read_text())
    for k in keys:
        d = d.get(k) if isinstance(d, dict) else None
    return d


def rungs() -> list[dict]:
    """Each rung: its name, status, and marks (done, text)."""
    lower = ("REST", "RELAY", "SIDE", "ESCAPE", "QUIET", "SUGAR", "RESPONSE", "BITTER", "IR94E", "STABLE")
    rung4 = [(bool(verdict("rung4_scaling", "RATE")), "rests at its 8 targeted rates, nothing runs away"),
             (all(verdict("rung4_scaling", k) for k in lower), "taste and escape still pass at rest"),
             (bool(verdict("rung4_scaling", "BUMP")), "a head-direction bump (fitted; still leaning)")]
    return [
        {"name": "Validated baseline", "status": "passed" if verdict("shiu_rewiring", "pass") else "in progress",
         "marks": [(True, "sugar drives the proboscis motor neuron; bitter suppresses it; rewiring abolishes it")]},
        {"name": "Signs and modulators", "status": "passed" if verdict("rung2_signs", "pass") else "in progress",
         "marks": [(True, "consensus transmitters; monoamines out of fast excitation"),
                   (bool(verdict("rung2_signs", "pass")), "signs audited by hemilineage; false positives 1 in 100")]},
        {"name": "Eye and optic lobe", "status": "passed" if verdict("rung3_001", "pass") else "in progress",
         "marks": [(bool(verdict("rung3_001", "DIRECTION")), "16/16 motion directions in the eye (fitted; weak)"),
                   (bool(verdict("rung3_001", "LOOMING")), "looming reaches LC4 and LPLC2 (as in model 001)"),
                   (bool(verdict("rung3_001", "POLARITY")), "31 of 32 polarities (fitted)")]},
        {"name": "Central brain at rest", "status": "passed" if verdict("rung4_scaling", "pass") else "in progress",
         "marks": rung4},
        {"name": "Nerve cord", "status": "passed" if verdict("rung5_vnc3", "pass") else "in progress",     # attempt 3
         "marks": [(bool(verdict("rung5_vnc3", "DNG100")), "DNg100 drives 7-15 Hz leg rhythms (attempt 3: one side a run short)"),
                   (bool(verdict("rung5_vnc3", "DNB08")), "DNb08 drives them"),
                   (bool(verdict("rung5_vnc3", "NULL")), "scrambled wiring doesn't, at any drive")]},
        {"name": "Gap junctions and proprioception", "status": "passed" if verdict("rung6_relay", "pass") else "started",
         "pill": "half passed" if verdict("rung6_relay", "pass") else None,     # its test has no proprioception
         "marks": [(True, "electrical synapses in the model"),
                   (bool(verdict("rung6_relay", "pass")), "giant fiber to jump muscle in 0.9 ms (built in); silent without them"),
                   (False, "leg sensors driven by the body")]},
        {"name": "Body and muscles", "status": "started",
         "marks": [(bool(verdict("closed_loop", "result", "pass")), "NeuroMechFly walks, steered by DNa02"),
                   (bool(verdict("jump_calibration", "bilateral", "took_off")), "jumps from jump motor neuron spikes"),
                   (False, "motor neurons drive muscles")]},
        {"name": "Flight, neck and song", "status": "not started", "marks": [(False, "saccades, head pose, song pulses")]},
        {"name": "State and learning", "status": "started" if verdict("rung9_learning", "verdicts") else "not started",     # attempt 1
         "marks": [(bool(verdict("rung9_learning", "verdicts", "PAIRED", "pass")), "pairing depresses MBON11's response to the odor"),
                   (bool(verdict("rung9_learning", "verdicts", "UNPAIRED", "pass")), "sparing the unpaired odor as flies' does"),
                   (bool(verdict("rung9_learning", "verdicts", "RECIPROCAL", "pass")), "both ways round (attempt 1: one way)"),
                   (False, "final hurdle: resting FC, once arousal sets the brain-wide state")]},
    ]


def figure(theme: str, rows: list[dict]) -> str:
    c = THEMES[theme]
    H = TOP * 2 + ROW * len(rows)
    out = [f'<rect width="{W}" height="{H}" fill="{c["paper"]}"/>']
    # rails
    out.append(f'<path d="M{RAIL_X} {TOP - 10}V{H - TOP + 10}M{RAIL_X + RAIL_W} {TOP - 10}V{H - TOP + 10}" '
               f'stroke="{c["muted"]}" stroke-width="3" stroke-linecap="round"/>')
    for k, r in enumerate(rows):                 # rung 1 at the bottom
        y = H - TOP - ROW * (k + 0.5)
        state = r["status"]
        done = state == "passed"
        partial = state in ("in progress", "started")
        col = c["red"] if (done or partial) else c["rule"]
        out.append("<g>")
        if k % 2 == 0:
            out.append(f'<rect x="{RAIL_X + RAIL_W + 16}" y="{y - ROW / 2 + 3:.1f}" width="{W - RAIL_X - RAIL_W - 30}" height="{ROW - 6}" rx="8" fill="{c["wash"]}"/>')
        out.append(f'<path d="M{RAIL_X} {y:.1f}H{RAIL_X + RAIL_W}" stroke="{col}" stroke-width="{7 if done else 5}" stroke-linecap="round"'
                   + ('' if (done or partial) else ' stroke-dasharray="2 7"') + "/>")
        tx = RAIL_X + RAIL_W + 36
        out.append(f'<text x="{tx}" y="{y - 4:.1f}" class="num" fill="{col if (done or partial) else c["muted"]}">{k + 1}</text>')
        out.append(f'<text x="{tx + 30}" y="{y - 4:.1f}" class="name">{r["name"]}</text>')
        pill = r.get("pill") or {"passed": "passed", "in progress": "in progress", "started": "started", "not started": "not started"}[state]
        pw = 12 + 7.6 * len(pill)
        px = W - 32 - pw
        if done:
            out.append(f'<rect x="{px:.1f}" y="{y - 21:.1f}" width="{pw:.1f}" height="24" rx="12" fill="{c["red"]}"/>')
            out.append(f'<text x="{px + pw / 2:.1f}" y="{y - 4:.1f}" class="pill" fill="{c["paper"]}" text-anchor="middle">{pill}</text>')
        else:
            out.append(f'<rect x="{px:.1f}" y="{y - 21:.1f}" width="{pw:.1f}" height="24" rx="12" fill="none" '
                       f'stroke="{col if partial else c["rule"]}" stroke-width="1.5"/>')
            out.append(f'<text x="{px + pw / 2:.1f}" y="{y - 4:.1f}" class="pill" fill="{col if partial else c["muted"]}" text-anchor="middle">{pill}</text>')
        mx = tx + 30
        for ok, label in r["marks"]:
            dot = (f'<circle cx="{mx + 5:.1f}" cy="{y + 14:.1f}" r="4.5" fill="{c["red"] if ok else "none"}" '
                   f'stroke="{c["red"] if ok else c["muted"]}" stroke-width="1.4"/>')
            out.append(dot + f'<text x="{mx + 15:.1f}" y="{y + 19:.1f}" class="mark">{label}</text>')
            mx += 15 + 6.45 * len(label) + 24
        out.append("</g>")
    style = f"""
    text {{ font-family: {FONT}; }}
    .num {{ font-size: 18px; font-weight: 700; font-variant-numeric: tabular-nums; }}
    .name {{ font-size: 17px; font-weight: 600; fill: {c["ink"]}; }}
    .mark {{ font-size: 13.5px; fill: {c["muted"]}; }}
    .pill {{ font-size: 12.5px; font-weight: 600; }}
    """
    title = "brainfly's ladder of nine rungs, from a validated baseline to state and learning, and where each stands"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style>' + "".join(out) + "</svg>")


def main() -> None:
    rows = rungs()
    for theme in THEMES:
        path = OUT / f"ladder-{theme}.svg"
        path.write_text(figure(theme, rows))
        print(f"{path} ({path.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
