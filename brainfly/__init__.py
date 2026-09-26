"""brainfly: the complete fruit fly nervous system (MaleCNS v1.0 connectome, 166,700 neurons)
as a spiking network you can stimulate and read out.

    from brainfly import FlyBrain
    brain = FlyBrain(device="auto")      # downloads the brain files on first use
    brain.stimulate(brain.cells(["LC4", "LPLC2"], side="L"), 0.8)
    fired = brain.step()                 # indices of the neurons that spiked this 20 ms step
"""
from .brain import FlyBrain, cuda_available
from .data import DATA, download, ensure_data, has_data
from .eyes import Blob, Eyes, blob_for

__version__ = "0.1.0"

__all__ = ["FlyBrain", "cuda_available", "DATA", "download", "ensure_data", "has_data",
           "Blob", "Eyes", "blob_for"]
