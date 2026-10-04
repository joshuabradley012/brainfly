"""Time flyvis training iterations on this machine without touching any run's checkpoint.

Builds the same network, task and optimizer as experiments/flyvis_t2_scratch.py (for the given run), trains a fresh
copy in memory for a few hundred iterations, and reports seconds per iteration after a warm-up. Nothing is saved.

    python scripts/gpu/bench.py [main|control|noaug|decoder000|fast] [iterations]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
run = sys.argv[1] if len(sys.argv) > 1 else "main"
iters = int(sys.argv[2]) if len(sys.argv) > 2 else 300
sys.path.insert(0, str(ROOT / "experiments"))
sys.argv = [sys.argv[0]] + ([] if run == "main" else [run])   # flyvis_t2_scratch reads its run from argv on import

import torch  # noqa: E402

import flyvis_t2_scratch as s  # noqa: E402
from brainfly import vistrain as vt  # noqa: E402


def sync():
    if vt.DEVICE.type == "cuda":
        torch.cuda.synchronize()
    elif vt.DEVICE.type == "mps":
        torch.mps.synchronize()


def launch_us(n: int = 5000) -> float:
    """Microseconds per tiny GPU operation after a warm-up. Training is thousands of these per iteration, so a box
    that launches them slowly trains slowly whatever its GPU (healthy NVIDIA boxes: 5-10 us; the RunPod 4090 of
    October 2026: 60-200)."""
    z = torch.zeros(1000, device=vt.DEVICE)
    for _ in range(n):
        z.add_(1)
    sync()
    t = time.perf_counter()
    for _ in range(n):
        z.add_(1)
    sync()
    return (time.perf_counter() - t) / n * 1e6


def main() -> None:
    print(f"device {vt.DEVICE}" + (f" ({torch.cuda.get_device_name()})" if vt.DEVICE.type == "cuda" else ""), flush=True)
    print(f"{launch_us():.0f} us per tiny GPU operation (healthy NVIDIA boxes: 5-10)", flush=True)
    view, net, dec, task, opt, pen, sched = s.build()
    sched(0)
    dt, k, warm, t0 = task.dataset.dt, 0, min(20, iters // 5), None
    net.train()
    with task.dataset.augmentation(s.AUGMENT):
        while k < iters:
            with vt.on(vt.DEVICE), torch.no_grad():
                state = net.steady_state(t_pre=0.5, dt=dt, batch_size=task.batch_size, value=0.5)
            for data in task.train_data:
                if k >= iters:
                    break
                if k == warm:
                    sync()
                    t0 = time.perf_counter()
                with vt.on(vt.DEVICE):
                    opt.zero_grad()
                    net.stimulus.zero(*data["lum"].shape[:2])
                    net.stimulus.add_input(data["lum"].to(vt.DEVICE))
                    act = net(net.stimulus(), dt, state=state)
                    loss = task.loss(dec["flow"](act), data["flow"].to(vt.DEVICE), "flow")
                    extra = s.capped_t2_penalty(net) * (s.T2_EVERY * s.T2_WEIGHT / 1000.0) if k % s.T2_EVERY == 0 and s.T2_WEIGHT else 0.0
                    (loss + extra).backward(retain_graph=True)
                    opt.step()
                    pen(activity=act, iteration=k)
                k += 1
    sync()
    per = (time.perf_counter() - t0) / (iters - warm)
    import flyvis
    chkpt = flyvis.results_dir / s.NAME / "chkpts" / "scratch_last.pt"
    done = torch.load(chkpt, map_location="cpu", weights_only=False)["iteration"] if chkpt.exists() else 0
    print(f"{per:.3f} s per iteration over {iters - warm} iterations (Apple M4 Pro GPU: 0.46)")
    print(f"a full {s.ITERS:,}-iteration run: {s.ITERS * per / 3600:.1f} h; this run's checkpoint is at {done:,}, "
          f"so about {(s.ITERS - done) * per / 3600:.1f} h to go, plus validation passes")


if __name__ == "__main__":
    main()
