"""A built olfaction model saved once and restored into a freshly constructed one, so that experiments on the same model
needn't rebuild it (odor_probe30.py's antennal lobe takes about 9 minutes to build).

The cache keeps every attribute of the brain, its Olfaction wrapper, the wrapper's setup and the receptor drive, except
functions and the per-trial state that HybridBrain.reset renews; restoring puts back each attribute whose value differs
from the fresh model's and leaves the rest as constructed. It records the hash of every file of this repository loaded
when it was saved and is used only while none of them has changed. Whenever a cache is saved it is first restored into a
fresh model, and both models are run from the same seed through rest and an odor: their spikes must match exactly, or
nothing is saved (the run goes on with the model it built).

    o, rec, built = brain_cache.load("odor_probe30", p31.build, prepare)     (or brain_cache.probe30())

`prepare` sets the module globals the build relies on (seeds, patched functions); it runs before either path.
"""
from __future__ import annotations

import ast
import hashlib
import pickle
import sys
from pathlib import Path

import numpy as np

import odor_probe10 as p10
import odor_probe24 as p24
import odor_probe7 as p7

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "fly-data" / "cache"
TRANSIENT = {"u", "x", "s", "until", "ad", "pending", "fpending", "pending_slow", "touched", "n_touched", "graded_input",
             "slow_graded_input", "external_input", "release", "rng", "driven", "left", "last", "left_s", "last_s",
             "presynaptic_state", "t"}                    # renewed by HybridBrain.reset
CHECK_SEED, CHECK_ODOR = 999001, "3-octanol"


def _digest(path: Path) -> str:
    """sha256 of a module's code: its syntax tree without docstrings."""
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                node.body = node.body[1:] or [ast.Pass()]
    return hashlib.sha256(ast.dump(tree).encode()).hexdigest()


def _sources(build) -> dict:
    """The repository's modules loaded now, but this one and the running script unless it holds the build: path ->
    digest."""
    out = {}
    for name, mod in list(sys.modules.items()):
        f = getattr(mod, "__file__", None)
        if not f or not Path(f).is_absolute() or (name in ("__main__", __name__) and name != getattr(build, "__module__", None)):
            continue                                      # (some compiled modules give a relative, made-up path)
        p = Path(f).resolve()
        if p.suffix == ".py" and p.is_relative_to(ROOT) and ".venv" not in p.parts and p.exists():
            out[str(p.relative_to(ROOT))] = _digest(p)
    return out


def _fresh(sources: dict) -> bool:
    return all((ROOT / name).exists() and _digest(ROOT / name) == digest for name, digest in sources.items())


def _state(obj, skip=()) -> dict:
    return {k: v for k, v in vars(obj).items() if k not in skip and not callable(v)}


def _parts(o: p7.Olfaction, rec: p10.Receptors) -> dict:
    return {"brain": (o.brain, TRANSIENT), "olfaction": (o, {"brain", "s"}), "setup": (o.s, {"brain", "ol"}),
            "receptors": (rec, ())}                       # ol: the optic lobe, which olfaction leaves silent


def _same(a, b) -> bool:
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return (isinstance(a, np.ndarray) and isinstance(b, np.ndarray) and a.dtype == b.dtype and a.shape == b.shape
                and np.array_equal(a, b, equal_nan=a.dtype.kind == "f"))
    try:
        return bool(a == b) if type(a) is type(b) else False
    except (ValueError, TypeError):
        return False


def _restore(state: dict) -> tuple:
    o = p7.Olfaction()
    rec = p10.Receptors(o)
    replaced = 0
    for part, (obj, skip) in _parts(o, rec).items():
        current = vars(obj)
        for k, v in state[part].items():
            if k not in current or not _same(current[k], v):
                setattr(obj, k, v)
                replaced += 1
    o.brain.reset(0)
    return o, rec, replaced


def _spikes(o: p7.Olfaction, rec: p10.Receptors) -> np.ndarray:
    """0.5 s of rest and 0.3 s of an odor from CHECK_SEED: spike counts per 10 ms piece."""
    b = o.brain
    b.reset(CHECK_SEED)
    b.set_release(o.s.ol.neurons, o.s.silent)
    out = [b.advance(int(round(0.5 / b.dt)), drive=p24.spontaneous(rec))]
    plan = rec.plan(CHECK_ODOR, 1.0, p10.PEAK_HZ)
    for k in range(30):
        out.append(b.advance(int(round(p10.PIECE / b.dt)), drive=rec.at(plan, k * p10.PIECE)))
    return np.stack(out)


def save(name: str, o: p7.Olfaction, rec: p10.Receptors, built: dict, build=None) -> Path:
    state = {part: _state(obj, skip) for part, (obj, skip) in _parts(o, rec).items()}
    state["built"], state["sources"] = built, _sources(build)
    blob = pickle.dumps(state, protocol=5)
    o2, rec2, replaced = _restore(pickle.loads(blob))
    a, c = _spikes(o, rec), _spikes(o2, rec2)
    if not np.array_equal(a, c):
        raise RuntimeError(f"cache {name}: the restored model's spikes differ ({int(np.abs(a - c).sum())} spikes); not saved")
    DIR.mkdir(parents=True, exist_ok=True)
    path = DIR / f"{name}.pkl"
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(blob)
    tmp.replace(path)
    print(f"cache {name}: saved ({len(blob) / 1e6:.0f} MB, {replaced} attributes differ from a fresh model; "
          f"{int(a.sum())} spikes matched)", flush=True)
    return path


def load(name: str, build, prepare=None) -> tuple:
    """(o, rec, built): restored from the cache if it exists and its sources haven't changed, else built and saved."""
    if prepare is not None:
        prepare()
    path = DIR / f"{name}.pkl"
    if path.exists():
        state = pickle.loads(path.read_bytes())
        if _fresh(state["sources"]):
            o, rec, replaced = _restore(state)
            print(f"cache {name}: restored ({replaced} attributes)", flush=True)
            return o, rec, state["built"]
        print(f"cache {name}: sources changed; rebuilding", flush=True)
    o, rec, built = build()
    try:
        save(name, o, rec, built, build)
    except Exception as e:                                # a cache that can't be saved mustn't cost the run
        print(f"cache {name}: not saved ({type(e).__name__}: {e})", flush=True)
    return o, rec, built


def probe30() -> tuple:
    """odor_probe30.py's brain: odor_probe31.build, which rebuilds it on odor_probe30.py's seeds, or the cache."""
    import odor_probe21 as p21
    import odor_probe22 as p22
    import odor_probe27 as p27
    import odor_probe28 as p28
    import odor_probe29 as p29
    import odor_probe30 as p30
    import odor_probe31 as p31

    def prepare() -> None:
        p21.SEED = p22.SEED = p24.SEED = p27.SEED = p28.SEED = p30.SEED
        p21.masks = p29.pn_only_masks
    return load("odor_probe30", p31.build, prepare)
