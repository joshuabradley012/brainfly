"""The resting fly brain as whole-brain imaging sees it, and the same measurement taken of the model.

Turner, Mann & Clandinin (2021, Curr Biol 31:2386; data: figshare 10.6084/m9.figshare.13349282, MIT
licence) imaged 20 immobilized female flies at rest, in darkness and with no stimulus. They used
pan-neuronal GCaMP6s at 1.2 Hz for about 28 minutes each, and averaged each neuropil of the Ito et
al. (2014) atlas. Their functional connectivity (FC) between two regions is the Fisher z of the
correlation of the two signals, after a first-order high-pass at 0.01 Hz (applied forward only) and
dropping the first 100 frames, with three flies' artefacts cut as well.

This module:
- fetches their region signals (turner),
- computes FC exactly their way (connectivity; tests/test_imaging.py reproduces their published
  matrix),
- maps their regions onto MaleCNS's ROIs (region_weights: each neuron's synapses in each region),
- and turns a simulation's spikes into the same measurement (record, then image).

REGIONS are the 66 regions used here: the 67 non-optic regions that every fly has, with left and
right IB merged, because MaleCNS draws IB as one region.
"""
from __future__ import annotations

import io
import sys
import tarfile
from pathlib import Path

import numpy as np
from scipy import signal, sparse

from .data import DATA, _fetch

TURNER_URL = "https://ndownloader.figshare.com/files/26356327"         # data_TurnerMannClandinin.tar.gz, v3
TURNER_SHA256 = "b6b0ea42da2d728e76ff3c646b56e7d32ecf0fcabb63eba585725cf1f0835f77"
ROI_URL = "https://storage.googleapis.com/flyem-male-cns/v1.0/database/neuprint-inputs/roi_elements.feather"
ROI_SHA256 = "9a14d45b433686118c05ca0784e89792f66931ba321fbb2d36dfdaa80b56d99a"
FS, CUTOFF, DROP = 1.2, 0.01, 100
# SC-FC's frame ranges for three flies with artefacts (github.com/mhturner/SC-FC, trimRegionResponse)
TRIMS = {"2018-10-19_1": np.r_[100:900, 1100:2000], "2017-11-08_1": np.r_[100:1900, 2000:4000],
         "2018-10-20_1": np.r_[100:1000]}
OPTIC = ("ME", "AME", "LO", "LOP", "LA")
# Ito atlas names whose MaleCNS ROIs aren't a plain rename (base name, before the side)
SPECIAL = {"MB_CA": ["CA"], "MB_PED": ["PED"], "MB_VL": ["a'L", "aL"], "MB_ML": ["b'L", "bL", "gL"],
           "LAL": ["LAL(-GA)"], "GA": ["GA"], "SAD": ["SAD(-AMMC)"], "AMMC": ["AMMC"]}
RENAMED = {"IVLP_L": "WED_L"}                  # the atlas's label file still uses the old name


def mcns_rois(region: str) -> list[str]:
    """MaleCNS ROIs making up one of REGIONS, e.g. "MB_ML_R" -> ["b'L(R)", "bL(R)", "gL(R)"]."""
    if region == "IB":
        return ["IB"]
    base, side = (region[:-2], region[-1]) if region[-2:] in ("_L", "_R") else (region, None)
    names = SPECIAL.get(base, [base])
    return [f"{n}({side})" if side else n for n in names]


def _turner_folder(data: Path | str | None = None) -> Path:
    """Turner et al.'s region signals, label names and published FC, extracted into <data>/turner2021
    (fetching their 246 MB archive into <data>/raw first if it isn't there)."""
    data = Path(DATA if data is None else data)
    folder = data / "turner2021"
    if (folder / "labels.csv").exists():
        return folder
    archive = data / "raw" / "data_TurnerMannClandinin.tar.gz"
    if not archive.exists():
        archive.parent.mkdir(parents=True, exist_ok=True)
        print("fetching Turner, Mann & Clandinin 2021's data (246 MB, once)", file=sys.stderr)
        _fetch(TURNER_URL, archive, TURNER_SHA256)
    folder.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            name = member.name.split("data/", 1)[-1]
            keep = (name.startswith("ito_responses/ito_") and name.endswith(".pkl")) or name in (
                "ito_68_atlas/Original_Index_panda_full.csv", "subsample/subsample_CorrelationMatrix_Full.pkl")
            if keep:
                target = folder / {"ito_68_atlas/Original_Index_panda_full.csv": "labels.csv",
                                   "subsample/subsample_CorrelationMatrix_Full.pkl": "published_fc.pkl"}.get(name, Path(name).name)
                target.write_bytes(tar.extractfile(member).read())
    return folder


def turner(data: Path | str | None = None) -> dict[str, dict[str, np.ndarray]]:
    """Each fly's region signals: {fly: {atlas region: raw mean fluorescence per frame}}."""
    import pandas as pd

    folder = _turner_folder(data)
    labels = pd.read_csv(folder / "labels.csv")
    names = {int(k): v for k, v in zip(labels["num"], labels["name"]) if isinstance(v, str)}
    out = {}
    for path in sorted(folder.glob("ito_*.pkl")):
        frame = pd.read_pickle(path)
        out[path.stem[len("ito_"):]] = {names[int(i)]: frame.loc[i].to_numpy(float) for i in frame.index if int(i) in names}
    return out


def published_fc(data: Path | str | None = None):
    """Turner et al.'s own 37 x 37 mean FC (Fisher z), as a pandas DataFrame."""
    import pandas as pd

    return pd.read_pickle(_turner_folder(data) / "published_fc.pkl")


def rest_signals(flies: dict[str, dict[str, np.ndarray]]) -> dict[str, np.ndarray]:
    """Each fly's signals for REGIONS, as a (66, frames) array: left and right IB averaged, and the
    atlas's old IVLP_L label read as WED_L."""
    out = {}
    for fly, series in flies.items():
        series = {RENAMED.get(k, k): v for k, v in series.items()}
        series["IB"] = (series.pop("IB_L") + series.pop("IB_R")) / 2
        out[fly] = np.array([series[r] for r in REGIONS])
    return out


def connectivity(signals: dict[str, np.ndarray], trims: dict = TRIMS, fs: float = FS, cutoff: float = CUTOFF,
                 drop: int = DROP) -> tuple[np.ndarray, np.ndarray]:
    """FC as Turner et al. computed it: for each fly's (regions, frames) signals, a first-order
    Butterworth high-pass at `cutoff`, applied forward only, then the frames in `trims` for that
    fly or else all but the first `drop`, then the Fisher z of every pair's Pearson correlation.
    Returns the mean over flies and each fly's matrix (diagonals NaN)."""
    sos = signal.butter(1, cutoff, "hp", fs=fs, output="sos")
    each = []
    for fly, x in signals.items():
        y = signal.sosfilt(sos, np.asarray(x, float))
        y = y[:, trims[fly]] if fly in trims else y[:, drop:]
        c = np.corrcoef(y)
        np.fill_diagonal(c, np.nan)
        each.append(np.arctanh(c))
    with np.errstate(invalid="ignore"), __import__("warnings").catch_warnings():
        __import__("warnings").simplefilter("ignore", RuntimeWarning)          # the all-NaN diagonal
        mean = np.nanmean(np.stack(each, axis=2), axis=2)
    np.fill_diagonal(mean, np.nan)
    return mean, np.array(each)


def region_weights(data: Path | str | None = None) -> sparse.csr_matrix:
    """Each neuron of brain.npz's synapses (pre + post) in each of REGIONS, (neurons, 66), from
    MaleCNS's neuprint table roi_elements.feather (3.7 GB, fetched into <data>/raw once). Cached as
    <data>/region_weights.npz."""
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.ipc as ipc

    data = Path(DATA if data is None else data)
    cache = data / "region_weights.npz"
    if cache.exists():
        return sparse.load_npz(cache).tocsr()
    source = data / "raw" / "roi_elements.feather"
    if not source.exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        print("fetching MaleCNS's roi_elements.feather (3.7 GB, once)", file=sys.stderr)
        _fetch(ROI_URL, source, ROI_SHA256)
    ids = np.load(data / "brain.npz")["ids"]
    rois = [roi for region in REGIONS for roi in mcns_rois(region)]
    region_of = np.array([r for r, region in enumerate(REGIONS) for _ in mcns_rois(region)])
    wanted, known = pa.array(rois), pa.array(ids)
    rows, cols, vals = [], [], []
    with pa.memory_map(str(source)) as stream:
        reader = ipc.open_file(stream)
        for k in range(reader.num_record_batches):
            batch = reader.get_batch(k)
            keep = pc.and_(pc.is_in(batch.column("roi"), value_set=wanted), pc.is_in(batch.column("body"), value_set=known))
            if not pc.any(keep).as_py():
                continue
            part = batch.filter(keep)
            rows.append(pc.index_in(part.column("body"), value_set=known).to_numpy())
            cols.append(region_of[pc.index_in(part.column("roi"), value_set=wanted).to_numpy()])
            vals.append((part.column("pre").to_numpy() + part.column("post").to_numpy()).astype(np.float32))
    W = sparse.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(len(ids), len(REGIONS)))
    sparse.save_npz(cache, W, compressed=True)
    return W


def regional(counts: np.ndarray, weights: sparse.spmatrix) -> np.ndarray:
    """Each region's activity: the synapse-weighted mean of its neurons' spike counts. counts:
    (..., neurons); returns (..., regions)."""
    W = sparse.csr_matrix(weights)
    flat = np.asarray(counts, np.float32).reshape(-1, W.shape[0])
    out = (sparse.csr_matrix(flat) @ W).toarray() / np.maximum(W.sum(0).A1, 1)
    return out.reshape(*np.shape(counts)[:-1], W.shape[1])


def record(brain, seconds: float, weights: sparse.spmatrix, bin: float = 0.01, **advance) -> np.ndarray:
    """Run a HybridBrain for `seconds` and keep only each region's activity in bins of `bin`
    seconds: (trials, regions, bins). Extra keywords go to brain.advance (drive, silence)."""
    steps = int(round(bin / brain.dt))
    bins = int(round(seconds / bin))
    out = np.empty((brain.trials, weights.shape[1], bins), np.float32)
    for k in range(bins):
        out[:, :, k] = regional(brain.advance(steps, **advance), weights)
    return out


def image(activity: np.ndarray, dt: float, rise: float = 0.2, decay: float = 1.0, fs: float = FS) -> np.ndarray:
    """What the imaging would record: activity (regions, bins of dt seconds) convolved with a
    GCaMP6s-like kernel (1 - exp(-t/rise)) exp(-t/decay), then averaged over each frame at fs.
    The kernel's time constants are approximate; at 1.2 Hz, FC hardly depends on them. Returns
    (regions, frames)."""
    t = np.arange(0, 8 * decay, dt)
    kernel = (1 - np.exp(-t / rise)) * np.exp(-t / decay)
    kernel /= kernel.sum()
    calcium = signal.fftconvolve(activity, kernel[None, :], axes=1)[:, :activity.shape[1]]
    frames = int(calcium.shape[1] * dt * fs)
    edges = np.round(np.arange(frames + 1) / (fs * dt)).astype(int)       # frame k: bins edges[k] to edges[k + 1]
    return np.add.reduceat(calcium[:, :edges[-1]], edges[:-1], axis=1) / np.diff(edges)


def _regions() -> list[str]:
    """The 67 non-optic regions every Turner fly has, with IVLP_L read as WED_L and the two IBs
    merged."""
    names = ["AL_L", "AL_R", "AMMC_L", "AMMC_R", "AOTU_L", "AOTU_R", "ATL_L", "ATL_R", "AVLP_L", "AVLP_R",
             "BU_L", "BU_R", "CAN_L", "CAN_R", "CRE_L", "CRE_R", "EB", "EPA_L", "EPA_R", "FB", "FLA_L", "FLA_R",
             "GA_L", "GA_R", "GNG", "GOR_L", "GOR_R", "ICL_L", "ICL_R", "IPS_L", "IPS_R", "WED_L", "LAL_L",
             "LAL_R", "LH_L", "LH_R", "MB_CA_L", "MB_CA_R", "MB_ML_L", "MB_ML_R", "MB_PED_L", "MB_PED_R",
             "MB_VL_L", "MB_VL_R", "NO", "PB", "PLP_L", "PLP_R", "PRW", "PVLP_L", "PVLP_R", "SAD", "SCL_L",
             "SCL_R", "SIP_L", "SIP_R", "SLP_L", "SLP_R", "SMP_L", "SMP_R", "SPS_L", "SPS_R", "VES_L", "VES_R",
             "WED_R", "IB"]
    return names


REGIONS = _regions()
