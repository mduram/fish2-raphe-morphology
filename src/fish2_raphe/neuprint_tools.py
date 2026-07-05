from __future__ import annotations

import os
from typing import Iterable

import pandas as pd


def make_client(server: str = "neuprint-fish2.janelia.org", dataset: str = "fish2"):
    from neuprint import Client
    # neuprint-python will use the configured token/environment; never hard-code it here.
    return Client(server, dataset)


def exact_raphe_superior_rois(client, requested=("Raphe_Superior", "Raphe_Superior1")) -> list[str]:
    available = set(client.meta["roiInfo"].keys())
    valid = [r for r in requested if r in available]
    if not valid:
        raise RuntimeError(f"None of requested ROIs exist: {list(requested)}")
    return valid


def fetch_touching_neurons(client, rois: Iterable[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    from neuprint import fetch_neurons, NeuronCriteria as NC
    return fetch_neurons(NC(rois=list(rois), roi_req="any"), client=client)
