"""brainfly: the fruit fly's whole nervous system, the MaleCNS v1.0 connectome (166,700 neurons),
as a network you can stimulate and record from, with a flyvis optic lobe and a walking body.

    from brainfly import FlyBrain
    brain = FlyBrain()                     # fetches the network files on first use
    fired = brain.step(inject=[(brain.cells(["LC4", "LPLC2"], side="L"), 0.4)])   # one 20 ms step
"""
from .brain import FlyBrain, cuda_available
from .data import DATA, download, ensure_data, has_data
from .eyes import Blob, Eyes, blob_for

__version__ = "0.1.0"
__all__ = ["FlyBrain", "cuda_available", "DATA", "download", "ensure_data", "has_data", "Blob", "Eyes", "blob_for"]
