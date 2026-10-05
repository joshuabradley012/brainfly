"""Exploratory, not pre-registered: does flyvis_t2_scratch.py's T2 penalty still measure T2's flash responses in the
network it trains?

The penalty (flyvis_t2_pilot5.penalty) reads T2's response to a light and a dark flash as the change from 0.1 s of grey,
starting from the network's steady state (vistrain.flash_responses' defaults). flyvis_t2_scratch.py logs T2's peaks
after 1.0 s of grey instead. In the main run the logged flag went False in most checkpoints from iteration 80,000 on,
while the penalty stayed near zero. Measured here, on the central T2 cell of flyvis's model 000 and of the main run's
last checkpoint: the flash responses (peaks and means over the penalty's 0.25 s window) after 0.1 s and after 1.0 s of
grey, and T2's activity at grey with no flash at all, from 0.05 to 3 s after the steady state (dt 0.01 s, the
penalty's).
Ran: the penalty is fooled. In model 000, T2 rests steadily at 3.5 and answers light by 3.0 and dark by nothing, the
same after either wait. In the main run at 120,000 iterations T2 rests at about 48 and wanders on its own (44.9 to
50.1 within the first second). After 0.1 s of grey that wander reads as equal answers to light and dark (peaks 3.2 and
3.5, means 2.9 and 2.9), which satisfies the penalty; after 1.0 s T2 barely answers either (0.20 and -0.05). So the
main run's T2 lost its responses while the penalty saw none of it. A penalty that subtracts a grey run from the same
starting state would cancel the wander.

    python experiments/t2_penalty_check.py      (writes experiments/t2_penalty_check.json; on the CPU)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

os.environ["BRAINFLY_DEVICE"] = "cpu"
sys.argv = [sys.argv[0]]                             # flyvis_t2_scratch's main run

import torch  # noqa: E402

import flyvis_t2_scratch as fs  # noqa: E402
from brainfly import vistrain as vt  # noqa: E402
from flyvis_t2_pilot5 import DT, WINDOW  # noqa: E402

OUT = Path(__file__).with_suffix(".json")
DEV = torch.device("cpu")


def main() -> None:
    import flyvis
    view, net, dec, task, opt, pen, sched = fs.build()
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(flyvis.results_dir / fs.NAME / "chkpts" / "scratch_last.pt", Path(tmp) / "ck.pt")
        ck = torch.load(Path(tmp) / "ck.pt", map_location="cpu", weights_only=False)
    _, net000, _ = vt.load("flow/0000/000", DEV)
    out = {"question": __doc__, "dt": DT, "window_s": WINDOW, "networks": {}}
    w = int(round(WINDOW / DT))
    for name, state in (("model 000", net000.state_dict()), (f"main at {ck['iteration']:,}", ck["network"])):
        net.load_state_dict(state)
        net.eval()
        row = {}
        with torch.no_grad():
            for t_pre in (0.1, 1.0):
                r = vt.flash_responses(net, "T2", dt=DT, t_pre=t_pre, t_flash=0.5, dev=DEV)
                row[f"after {t_pre} s of grey"] = {"peak_on": round(float(r[0].max()), 3), "peak_off": round(float(r[1].max()), 3),
                                                  "mean_on": round(float(r[0, :w].mean()), 3), "mean_off": round(float(r[1, :w].mean()), 3)}
            j, steps = vt.central(net, "T2"), int(round(3.0 / DT))
            with vt.on(DEV):
                state0 = net.steady_state(t_pre=0.5, dt=DT, batch_size=1, value=0.5)
                net.stimulus.zero(1, steps)
                net.stimulus.add_input(torch.full((1, steps, 1, vt.N_OMMATIDIA), 0.5))
                a = net(net.stimulus(), DT, state=state0)[0, :, j]
            row["grey_only"] = {f"{s} s": round(float(a[int(round(s / DT)) - 1]), 3) for s in (0.05, 0.1, 0.6, 1.0, 3.0)}
            row["grey_only"]["range_first_second"] = [round(float(a[:int(round(1.0 / DT))].min()), 3), round(float(a[:int(round(1.0 / DT))].max()), 3)]
        out["networks"][name] = row
        print(name, json.dumps(row), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
