"""Rung 8's neck: which synapses carry the neck motor neurons' visual signals in rung 6's whole brain with its eyes, from
experiments/neck_lesion_check.json, neck_route_check.json and neck_ocg_check.json (nothing by hand).

    python assets/neck_lesion.py      # writes assets/neck_lesion-light.svg and assets/neck_lesion-dark.svg

Left: each yaw neck motor neuron type's drum direction signal ((left - right, counterclockwise) - (left - right,
clockwise); soma side is nerve side) intact (filled) and with every HS and H2 synapse onto the five yaw types cut (open).
The grey tick is where the cut would leave it if the rate followed the drive linearly: the intact signal times the
share of the drive's direction change that doesn't come from HS and H2. Middle: CvN6's drum drive change (preferred
drum minus the other, by nerve side, both cells summed, mV) by input. Right: CvN7's vertical drive change (down - up,
both cells summed, mV) by input. Drive is weight x spikes per s (each weighted by its depression) x 5 ms. Means over 8
flies on one seed; whiskers are standard errors over flies.
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
W, H = 1120, 400
YAW = [("GNG283", "GNG283"), ("GNG276", "GNG276"), ("GNG647", "GNG647 (VCvN1/2)"), ("GNG653", "GNG653 (CvN1/2)"),
       ("GNG314", "GNG314 (VCvN3)")]
VS_TYPE = "VS1,VS2,VS3,VS4,VS5,VS6,VS7,VS8"


def text(x, y, s, cls, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def axis(c, tx, lo, hi, step, top, bottom, unit, mid) -> list[str]:
    out, k = [], lo
    while k <= hi + 1e-9:
        out.append(f'<line x1="{tx(k):.1f}" y1="{top - 8}" x2="{tx(k):.1f}" y2="{bottom}" stroke="{c["rule"]}" stroke-width="1"/>')
        out.append(text(tx(k), bottom + 16, f"{k:g}", "tiny", "middle"))
        k += step
    if lo < 0 < hi:
        out.append(f'<line x1="{tx(0):.1f}" y1="{top - 8}" x2="{tx(0):.1f}" y2="{bottom}" stroke="{c["muted"]}" stroke-width="1.5"/>')
    out.append(text(mid, bottom + 32, unit, "tiny", "middle"))
    return out


def yaw_panel(c, lesion: dict, route: dict, x0: float, x1: float, top: float) -> list[str]:
    out = [text(x0, top - 30, "Yaw neck MNs' drum signal", "val")]
    ax = x0 + 132
    lo, hi, step = 0, 80, 20
    tx = lambda v: ax + (x1 - ax) * (v - lo) / (hi - lo)
    rowh = 40
    bottom = top + rowh * len(YAW)
    out += axis(c, tx, lo, hi, step, top, bottom, "spikes/s", (ax + x1) / 2)
    for i, (key, name) in enumerate(YAW):
        y = top + rowh * i + rowh / 2
        out.append(text(x0, y + 4, name, "tick"))
        a = lesion["conditions"]["intact"]["yaw"][key]
        b = lesion["conditions"]["HS/H2 cut"]["yaw"][key]
        share = route["targets"][key]["cut_share_of_yaw_change"]
        linear = a["signal_hz"] * (1 - share)
        out.append(f'<line x1="{tx(linear):.1f}" y1="{y - 9:.1f}" x2="{tx(linear):.1f}" y2="{y + 9:.1f}" stroke="{c["faint"]}" stroke-width="3">'
                   f'<title>{name}: linear expectation {linear:.1f} spikes/s (HS and H2 give {100 * share:.0f}% of the drive change)</title></line>')
        out.append(f'<line x1="{tx(a["signal_hz"]):.1f}" y1="{y:.1f}" x2="{tx(b["signal_hz"]):.1f}" y2="{y:.1f}" stroke="{c["faint"]}" stroke-width="1.5"/>')
        for v, fill, stroke in ((a, c["ink"], c["ink"]), (b, c["paper"], c["red"])):
            se = abs(v["signal_hz"] / v["t"]) if v["t"] else 0.0
            out.append(f'<line x1="{tx(v["signal_hz"] - se):.1f}" y1="{y:.1f}" x2="{tx(v["signal_hz"] + se):.1f}" y2="{y:.1f}" '
                       f'stroke="{c["muted"]}" stroke-width="1.5"/>')
        out.append(f'<circle cx="{tx(a["signal_hz"]):.1f}" cy="{y:.1f}" r="5.5" fill="{c["ink"]}"><title>{name} intact: '
                   f'{a["signal_hz"]:.1f} spikes/s (t {a["t"]})</title></circle>')
        out.append(f'<circle cx="{tx(b["signal_hz"]):.1f}" cy="{y:.1f}" r="5.5" fill="{c["paper"]}" stroke="{c["red"]}" stroke-width="2">'
                   f'<title>{name}, HS and H2 cut: {b["signal_hz"]:.1f} spikes/s (t {b["t"]})</title></circle>')
    ly = bottom + 50
    out.append(f'<circle cx="{x0 + 6}" cy="{ly - 4}" r="5" fill="{c["ink"]}"/>')
    out.append(text(x0 + 16, ly, "intact", "tiny"))
    out.append(f'<circle cx="{x0 + 66}" cy="{ly - 4}" r="5" fill="{c["paper"]}" stroke="{c["red"]}" stroke-width="2"/>')
    out.append(text(x0 + 76, ly, "HS and H2 synapses cut", "tiny"))
    out.append(f'<line x1="{x0 + 214}" y1="{ly - 11}" x2="{x0 + 214}" y2="{ly + 3}" stroke="{c["faint"]}" stroke-width="3"/>')
    out.append(text(x0 + 222, ly, "if rate followed drive linearly", "tiny"))
    return out


def drive_panel(c, rows: list[tuple[str, float]], total: float, x0: float, x1: float, top: float, title: str, unit: str,
                lo: float, hi: float, step: float, note: str | None = None) -> list[str]:
    out = [text(x0, top - 30, title, "val")]
    ax = x0 + 92
    tx = lambda v: ax + (x1 - ax) * (v - lo) / (hi - lo)
    rowh = 30
    allrows = rows + [("all inputs", total)]
    bottom = top + rowh * len(allrows)
    out += axis(c, tx, lo, hi, step, top, bottom, unit, (ax + x1) / 2)
    for i, (name, v) in enumerate(allrows):
        y = top + rowh * i + rowh / 2
        last = i == len(allrows) - 1
        out.append(text(x0, y + 4, name, "val" if last else "tick"))
        a, b = sorted((tx(0), tx(v)))
        if last:
            out.append(f'<rect x="{a:.1f}" y="{y - 8:.1f}" width="{max(b - a, 1):.1f}" height="16" rx="3" fill="none" stroke="{c["ink"]}" stroke-width="2">'
                       f'<title>{name}: {v:+.1f} mV</title></rect>')
        else:
            colour = c["ink"] if v >= 0 else c["red"]
            out.append(f'<rect x="{a:.1f}" y="{y - 8:.1f}" width="{max(b - a, 1):.1f}" height="16" rx="3" fill="{colour}">'
                       f'<title>{name}: {v:+.1f} mV</title></rect>')
        out.append(text(tx(v) + (6 if v >= 0 else -6), y + 4, f"{v:+.1f}", "tiny", "start" if v >= 0 else "end"))
    if note:
        out.append(text(x0, bottom + 50, note, "tiny"))
    return out


def figure(theme: str, lesion: dict, route: dict, ocg: dict | None) -> str:
    c = THEMES[theme]
    cv6, cv7 = route["targets"]["CvN6"], route["targets"]["CvN7"]
    pick = lambda e, key, ty: next((r[key] for r in e["top_yaw" if key == "yaw_change" else "top_vertical"] if r["type"] == ty), 0.0)
    six = [("VS", cv6["named"]["VS"]["yaw_change"]["mv"]), ("HSS", cv6["named"]["HSS"]["yaw_change"]["mv"]),
           ("H2", cv6["named"]["H2"]["yaw_change"]["mv"]), ("CB3714", pick(cv6, "yaw_change", "CB3714")),
           ("OCG01f", pick(cv6, "yaw_change", "OCG01f"))]
    total6 = cv6["all_inputs"]["yaw_change"]["mv"]
    six.append(("others", total6 - sum(v for _, v in six)))
    seven = [("VS", cv7["named"]["VS"]["vertical_change"]["mv"]), ("OCG01f", pick(cv7, "vertical_change", "OCG01f")),
             ("PS237", pick(cv7, "vertical_change", "PS237")), ("CB0213", pick(cv7, "vertical_change", "CB0213"))]
    total7 = cv7["all_inputs"]["vertical_change"]["mv"]
    seven.append(("others", total7 - sum(v for _, v in seven)))
    note7 = None
    if ocg is not None:
        a, b = ocg["conditions"]["intact"]["pitch"]["CvN7"], ocg["conditions"]["OCG01f cut"]["pitch"]["CvN7"]
        note7 = f"Cutting OCG01f's synapses: CvN7 {a['vertical_hz']:+.1f} to {b['vertical_hz']:+.1f} spikes/s, down - up"
    out = [text(24, 30, HEADLINE, "lab")] + [text(24, 50 + 18 * i, s, "note") for i, s in enumerate(SUB)]
    top = 132
    out += yaw_panel(c, lesion, route, 24, 400, top)
    out += drive_panel(c, six, total6, 440, 760, top, "CvN6's drum drive, by input", "mV, preferred drum minus other", -6, 12, 3)
    out += drive_panel(c, seven, total7, 790, 1096, top, "CvN7's vertical drive, by input", "mV, down minus up", -15, 18, 5, note7)
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    .tiny {{ font-size: 10px; fill: {c["muted"]}; }}
    """
    title = ("Which synapses carry the neck motor neurons' visual signals in rung 6's brain: the yaw neurons' drum signal "
             "with HS and H2 cut, and CvN6's and CvN7's drive by input")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


HEADLINE = "Cutting HS and H2 removes most of the yaw neck neurons' drum signal; in CvN7, OCG01f cancels most of VS's drive"
SUB = ["Rung 6's whole brain with its eyes, open loop, 8 flies on one seed. Cutting only HS's and H2's synapses removes more of each yaw",
       "neuron's signal than their share of its drive (grey ticks): they also hold the cells near threshold. CvN6 follows the drum mostly via VS."]


def main() -> None:
    exp = ROOT / "experiments"
    lesion = json.loads((exp / "neck_lesion_check.json").read_text())
    route = json.loads((exp / "neck_route_check.json").read_text())
    ocg = json.loads((exp / "neck_ocg_check.json").read_text()) if (exp / "neck_ocg_check.json").exists() else None
    for theme in THEMES:
        path_ = OUT / f"neck_lesion-{theme}.svg"
        path_.write_text(figure(theme, lesion, route, ocg))
        print(path_)


if __name__ == "__main__":
    main()
