"""brainfly.legs: every motor module in Pugliese et al.'s table pulls a joint, the muscle's low-pass, and torque that
flexes a joint flexes it in the body."""
from __future__ import annotations

import numpy as np
import pytest

from brainfly import legs as L
from brainfly.data import DATA

TABLE = DATA / "pugliese" / "wTable_20260210_vncRoisOnly.csv"


def test_every_motor_module_pulls_a_joint():
    assert set(L.MODULES) == {"coxa swing", "coxa stance", "femur/tr flex", "femur/tr extend", "tibia flex",
                              "tibia extend", "femur reductor", "substrate grip", "tarsus control"}
    assert L.pull("tarsus control", "Ta depressor MN") == (L.JOINTS.index("TiTa pitch"), 1)
    assert L.pull("tarsus control", "Ta levator MN") == (L.JOINTS.index("TiTa pitch"), -1)
    assert L.pull(float("nan"), None) is None and L.pull("wing", None) is None
    assert {L.JOINTS[L.pull(m, "Ta levator MN")[0]] for m in L.MODULES} == set(L.DRIVEN)
    if not TABLE.exists():
        pytest.skip("Pugliese et al.'s table isn't in the data directory")
    pd = pytest.importorskip("pandas")
    t = pd.read_csv(TABLE, index_col=0)
    mn = t[t["class"] == "motor neuron"]
    annotated = mn[mn["motor module"].notna()]
    assert set(annotated["motor module"]) <= set(L.MODULES)
    assert all(L.pull(m, c) is not None for m, c in zip(annotated["motor module"], annotated["type"]))
    M = L.matrix(annotated["motor module"], annotated["type"], annotated["somaSide"].astype(str))
    assert (np.abs(M).sum((0, 1)) == 1).all()                      # each one pulls exactly one joint of one leg


def test_activation_is_a_first_order_low_pass():
    dt = 1e-4
    a = L.activation(np.ones((int(0.1 / dt), 1)), dt)[:, 0]
    assert a[0] == pytest.approx(0.5 * (1 - np.exp(-dt / L.TAU)))
    assert a[int(round(L.TAU / dt))] == pytest.approx(1 - np.exp(-1), abs=0.01)
    assert a[-1] == pytest.approx(1.0, abs=1e-2) and np.all(np.diff(a) >= 0)


@pytest.fixture(scope="module")
def legs():
    pytest.importorskip("flygym")
    return L.Legs()


def angle_at(P, segs, a, b, c):
    u, w = P[segs.index(a)] - P[segs.index(b)], P[segs.index(c)] - P[segs.index(b)]
    return np.degrees(np.arccos(np.dot(u, w) / np.linalg.norm(u) / np.linalg.norm(w)))


@pytest.mark.parametrize("module, joint, sign, chain", [
    ("femur/tr flex", "CTr pitch", -1, ("lf_coxa", "lf_trochanterfemur", "lf_tibia")),
    ("tibia flex", "FTi pitch", 1, ("lf_trochanterfemur", "lf_tibia", "lf_tarsus1")),
])
def test_flexor_torque_flexes_the_joint(legs, module, joint, sign, chain):
    rates = np.full((101, 1), 2.0)                                  # one left motor neuron at 2 Hz for 0.1 s
    rec = legs.run(L.torques(rates, 1e-3, [module], ["x"], ["L"]), 1e-3, bodies=True)
    j = L.JOINTS.index(joint)
    moved = rec["joints"][-1, 0] - rec["joints"][0, 0]
    assert sign * moved[j] > 5.0                                    # degrees, in the joint's flexion direction
    assert np.abs(np.delete(moved, j)).max() < 0.5                  # the leg's other joints stay put
    assert np.abs(rec["joints"][-1, 1] - rec["joints"][0, 1]).max() < 0.5    # and so does the right leg
    segs = rec["segments"]
    before, after = (angle_at(rec["positions"][i], segs, *chain) for i in (0, -1))
    assert after < before - 5.0                                     # the joint's angle closes


def test_coxa_swing_moves_the_foot_forward(legs):
    rates = np.full((101, 1), 2.0)
    swing = legs.run(L.torques(rates, 1e-3, ["coxa swing"], ["x"], ["R"]), 1e-3)
    stance = legs.run(L.torques(rates, 1e-3, ["coxa stance"], ["x"], ["R"]), 1e-3)
    assert swing["foot"][-1, 1, 0] - swing["foot"][0, 1, 0] > 0.1                   # mm forward
    assert stance["foot"][-1, 1, 0] - stance["foot"][0, 1, 0] < -0.1                # mm back
