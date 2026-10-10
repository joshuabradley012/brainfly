"""The MBON11 depression figure in the README (rung 9's groundwork), drawn from saved results (nothing by hand).

    python assets/mbon11_depression.py      # writes assets/mbon11_depression-light.svg and -dark.svg

odor_probe34.py: MBON11 in odor_probe30.py's model with Inada et al.'s Kenyon cell class offsets and its Kenyon cell
synapses set from Yamada et al. 2024's charge and Wang et al. 2026's gain (0.030 pC per synapse), the Kenyon cell-to-MBON
synapses undepressed (the current model) or depressing as Yamada et al. measured (each spike leaving 0.5 of the strength,
recovering over 1.5 s), 4 seeds of 8 flies, 50 ms bins. Top: MBON11's rate. Bottom: its Kenyon cell input as a current
per cell, each spike counted with the strength its depression has left. Flies as in assets/mbon11.py (Hige et al. 2015,
read off the figures, 75 ms of valve delay taken off, the PSTH's held 6 Hz baseline raised to the model's resting rate).
"""
from __future__ import annotations

import json

import mbon11 as base

OUT, ROOT, THEMES, FONT = base.OUT, base.ROOT, base.THEMES, base.FONT
W, H = 1120, 690
FLY_SPIKES = {"3-octanol": 118, "4-methylcyclohexanol": 110}
FLY_CHARGE = {"3-octanol": "245-250", "4-methylcyclohexanol": 265}
SERIES = (("undepressed", "red", False, "undepressed (the current model)"),
          ("depressing", "red", True, "depressing as Yamada et al. measured"))


def figure(theme: str, d: dict) -> str:
    c = THEMES[theme]
    out = [base.text(24, 30, "With the measured depression MBON11's input gets flies' early peak, but not their plateau", "lab"),
           base.text(24, 50, "Kenyon cell-to-MBON11 synapses undepressed (solid) or depressing as Yamada et al. 2024 measured (dashed), odor_probe34.py; "
                     "numbers: undepressed / depressing.", "note"),
           base.text(24, 68, "Rings: flies (Hige et al. 2015, read off the figures; the PSTH's held 6 Hz baseline raised to the model's "
                     "resting rate).", "note")]
    for k, odor in enumerate(base.ODORS):
        x0 = base.X0 + k * (base.PW + base.GAP)
        out.append(base.text(x0, base.RATE[0] - 12, odor, "val"))
        out += base.axes(c, x0, base.RATE, "MBON11, spikes/s", 100, k == 0)
        out += base.axes(c, x0, base.CURR, "Kenyon cell input per cell, pA", 250, k == 0)
        rest_hz = d["conditions"]["undepressed"]["course"][odor]["rest_hz"]
        out += base.rings(c, x0, base.RATE, [(t - base.VALVE, v - 6 + rest_hz) for t, v in base.FLY_PSTH[odor]],
                          "flies' PSTH, baseline raised to the model's rest")
        out += base.rings(c, x0, base.CURR, [(t - base.VALVE, v) for t, v in base.FLY_EPSC], "flies' odor EPSC")
        for name, colour, dashed, label in SERIES:
            r = d["conditions"][name]["course"][odor]
            ts = [-0.5, -0.025] + [r["start_s"] + r["bin_s"] * (i + 0.5) for i in range(len(r["mbon11_hz"]))]
            out.append(base.line(c, x0, base.RATE, ts, [r["rest_hz"]] * 2 + r["mbon11_hz"], c[colour], dashed=dashed, width=2.4))
            out.append(base.line(c, x0, base.CURR, ts, [0.0, 0.0] + [v - r["rest_pa"] for v in r["kc_current_pa"]], c[colour],
                                 dashed=dashed, width=2.4))
        u, dp = (d["conditions"][n]["odors"][odor] for n in ("undepressed", "depressing"))
        out.append(base.text(x0 + base.PW, base.RATE[0] - 12, f'{u["MBON11"]:.0f} / {dp["MBON11"]:.0f} spikes evoked '
                             f'(flies {FLY_SPIKES[odor]})', "tick", "end"))
        out.append(base.text(x0 + base.PW, base.CURR[0] - 12, f'{u["kc_charge_pc_per_cell"]:.0f} / {dp["kc_charge_pc_per_cell"]:.0f} pC '
                             f'per cell (flies {FLY_CHARGE[odor]})', "tick", "end"))
    out.append(base.text(base.X0 + base.PW + base.GAP / 2, base.CURR[1] + 40,
                         "time from the odor reaching the antenna (s); shaded: the 1 s odor", "tick", "middle"))
    style = f"""
    text {{ font-family: {FONT}; }}
    .lab {{ font-size: 16px; font-weight: 600; fill: {c["ink"]}; }}
    .val {{ font-size: 13px; font-weight: 600; fill: {c["ink"]}; }}
    .note {{ font-size: 13px; fill: {c["muted"]}; }}
    .tick {{ font-size: 11px; fill: {c["muted"]}; }}
    """
    dep = d["conditions"]["depressing"]["course"]["3-octanol"]
    title = ("MBON11 with and without the measured depression at its Kenyon cell synapses: depressing, its input to 3-octanol "
             f"peaks at {max(dep['kc_current_pa']):.0f} pA and falls to about {dep['kc_current_pa'][19]:.0f} pA by 1 s, where flies' EPSC holds about 170 pA")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title><style>{style}</style><rect width="{W}" height="{H}" fill="{c["paper"]}"/>'
            + "".join(out) + "</svg>")


def main() -> None:
    d = json.loads((ROOT / "experiments" / "odor_probe34.json").read_text())
    for theme in THEMES:
        path = OUT / f"mbon11_depression-{theme}.svg"
        path.write_text(figure(theme, d))
        print(path)


if __name__ == "__main__":
    main()
