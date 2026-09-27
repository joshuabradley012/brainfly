"""brainfly.vistrain runs flyvis's network on Apple's GPU with the CPU's numbers, measures T2's flash responses as
flyvis_screen.py reports them, and saves models flyvis loads unchanged. Needs flyvis and its pretrained models;
skipped without."""
from __future__ import annotations

import shutil

import pytest

torch = pytest.importorskip("torch")
from brainfly import vistrain as vt  # noqa: E402  (sets flyvis's data folder before flyvis is imported)

pytest.importorskip("flyvis")


def _have(model: str) -> bool:
    import flyvis
    return (flyvis.results_dir / model / "chkpts").exists()


pytestmark = pytest.mark.skipif(not _have("flow/0000/000"), reason="needs flyvis's pretrained models")
CPU = torch.device("cpu")


def test_t2_flash_peaks_match_the_screen():
    _, net, _ = vt.load("flow/0000/000", CPU)
    with torch.no_grad():
        on, off = vt.flash_peaks(net, "T2", dt=0.005, t_pre=1.0, t_flash=1.0, dev=CPU).tolist()
    assert on == pytest.approx(2.896, abs=0.01)             # flyvis_screen.py: 2.893 and 0.001
    assert abs(off) < 0.01


@pytest.mark.skipif(not torch.backends.mps.is_available(), reason="no Apple GPU")
def test_the_gpu_gives_the_cpus_responses():
    mps = torch.device("mps")
    peaks = []
    for dev in (CPU, mps):
        _, net, _ = vt.load("flow/0000/000", dev)
        with torch.no_grad():
            peaks.append(vt.flash_responses(net, "T2", dev=dev).cpu())
    assert torch.allclose(peaks[0], peaks[1], atol=1e-4)


def test_a_saved_model_loads_back_unchanged():
    import flyvis
    from flyvis import NetworkView
    name = "flow/test_vistrain/000"
    _, net, dec = vt.load("flow/0000/000", CPU)
    try:
        vt.save(net, dec, name, note={"test": True})
        back = NetworkView(flyvis.results_dir / name).init_network()
        for k, v in net.state_dict().items():
            assert torch.equal(v.cpu(), back.state_dict()[k].cpu()), k
    finally:
        shutil.rmtree(flyvis.results_dir / "flow" / "test_vistrain", ignore_errors=True)
