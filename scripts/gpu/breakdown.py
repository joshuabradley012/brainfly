"""Where a flyvis_t2_scratch.py training iteration spends its time on this machine (nothing saved).

    python scripts/gpu/breakdown.py [main|control|noaug|decoder000|fast] [iterations]
"""
from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
run = sys.argv[1] if len(sys.argv) > 1 else "main"
iters = int(sys.argv[2]) if len(sys.argv) > 2 else 12
sys.path.insert(0, str(ROOT / "experiments"))
sys.argv = [sys.argv[0]] + ([] if run == "main" else [run])

import torch  # noqa: E402

import flyvis_t2_scratch as s  # noqa: E402
from brainfly import vistrain as vt  # noqa: E402


def sync():
    if vt.DEVICE.type == "cuda":
        torch.cuda.synchronize()
    elif vt.DEVICE.type == "mps":
        torch.mps.synchronize()


def main() -> None:
    view, net, dec, task, opt, pen, sched = s.build()
    sched(0)
    dt, warm = task.dataset.dt, 3
    spent = defaultdict(float)
    net.train()
    k = 0
    with task.dataset.augmentation(s.AUGMENT):
        while k < iters + warm:
            sync(); t = time.perf_counter()
            with vt.on(vt.DEVICE), torch.no_grad():
                state = net.steady_state(t_pre=0.5, dt=dt, batch_size=task.batch_size, value=0.5)
            sync(); spent["steady state (per epoch)"] += (time.perf_counter() - t) * (k >= warm)
            loader = iter(task.train_data)
            while k < iters + warm:
                t = time.perf_counter()
                try:
                    data = next(loader)
                except StopIteration:
                    break
                marks = [("data", time.perf_counter())]
                with vt.on(vt.DEVICE):
                    opt.zero_grad()
                    net.stimulus.zero(*data["lum"].shape[:2])
                    net.stimulus.add_input(data["lum"].to(vt.DEVICE))
                    act = net(net.stimulus(), dt, state=state)
                    loss = task.loss(dec["flow"](act), data["flow"].to(vt.DEVICE), "flow")
                    sync(); marks.append(("forward", time.perf_counter()))
                    extra = s.capped_t2_penalty(net) * (s.T2_EVERY * s.T2_WEIGHT / 1000.0) if k % s.T2_EVERY == 0 and s.T2_WEIGHT else 0.0
                    sync(); marks.append(("T2 penalty forward", time.perf_counter()))
                    (loss + extra).backward(retain_graph=True)
                    sync(); marks.append(("backward", time.perf_counter()))
                    opt.step()
                    sync(); marks.append(("optimizer", time.perf_counter()))
                    pen(activity=act, iteration=k)
                    sync(); marks.append(("activity penalty", time.perf_counter()))
                if k >= warm:
                    prev = t
                    for name, m in marks:
                        spent[name] += m - prev
                        prev = m
                k += 1
    total = sum(spent.values())
    print(f"{run} on {vt.DEVICE}, batch {task.batch_size}: {total / iters:.3f} s per iteration over {iters}")
    for name, v in sorted(spent.items(), key=lambda x: -x[1]):
        print(f"  {name:28s} {v / iters:.3f} s  ({100 * v / total:.0f}%)")


if __name__ == "__main__":
    main()
