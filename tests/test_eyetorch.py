"""brainfly.eyetorch: flyvis's network on the male eye in PyTorch, against FlyvisNative's numpy version."""
import os

import numpy as np
import pytest

pytest.importorskip("brainfly.vistrain")         # before flyvis: it points flyvis at brainfly's data


@pytest.mark.skipif(not os.environ.get("FLY_DATA") and not os.path.exists(os.path.expanduser("~/fly-data/brain.npz")),
                    reason="needs brainfly's data")
def test_the_torch_eye_answers_edges_as_flyvis_native_does():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
    import torch
    from brainfly import FlyBrain, vistrain as vt              # first: it points flyvis at brainfly's data
    from brainfly.eyetorch import EyeTorch
    from flyvis_native import direction_selectivity
    from brainfly.optic import GRADED, FlyvisNative
    model = "flow/0000/001"
    _, net, _ = vt.load(model)
    eye = EyeTorch(net, "R", dt=0.02)
    with torch.no_grad():
        rest = eye.settle(net)
        off = eye.edge_sweeps(-1.0)
        peak = eye.peaks(net, off, rest)
    ref = direction_selectivity(FlyvisNative(FlyBrain(batch=1, graded=GRADED, dt=0.002, refractory=0.004), model=model, dt=0.02))
    for sub in "abcd":
        mine = eye.type_means(peak, f"T5{sub}").cpu().numpy()
        theirs = np.array([ref[f"R T5{sub}"]["responses"][n] for n in off[2]])
        assert np.abs(mine - theirs).max() < 2e-3


def test_tile_entries_rebuild_tiles_weights():
    from brainfly.eye2d import column_directions
    from brainfly.optic import flyvis_filters, plane, tile, tile_entries
    from scipy import sparse
    f = flyvis_filters("flow/0000/001")
    dirs = column_directions()
    ks = sorted(k for k in dirs if k[0] == "R")[:120]
    C = np.array([(h1, h2) for _, h1, h2 in ks])
    xy = plane(*C.T)
    o = C[np.argmin(((xy - xy.mean(0)) ** 2).sum(1))]
    ct, cc, W = tile(C, o, f)
    ct2, cc2, rows, cols, element, keys = tile_entries(C, o, f)
    w = np.array([f["sign"][(s, t)] * f["strength"][(s, t)] * f["count"][(s, t, du, dv)] for s, t, du, dv in keys])
    W2 = sparse.csr_matrix((w[element], (rows, cols)), shape=W.shape)
    assert (ct == ct2).all() and (cc == cc2).all() and abs(W - W2).max() == 0
