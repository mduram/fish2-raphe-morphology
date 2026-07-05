from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import cut_tree, linkage
from scipy.spatial.distance import squareform


def clean_distance_matrix(dist: pd.DataFrame, ids: Iterable[int] | None = None) -> pd.DataFrame:
    df = dist.copy().astype(float)
    df.index = df.index.astype(int)
    df.columns = df.columns.astype(int)
    common = [x for x in df.index if x in set(df.columns)]
    if ids is not None:
        wanted = set(int(x) for x in ids)
        common = [x for x in common if x in wanted]
    df = df.loc[common, common]
    arr = df.to_numpy(float)
    arr = np.nan_to_num(arr, nan=np.nanmax(arr[np.isfinite(arr)]) if np.isfinite(arr).any() else 1.0)
    arr = (arr + arr.T) / 2.0
    arr[arr < 0] = 0.0
    np.fill_diagonal(arr, 0.0)
    return pd.DataFrame(arr, index=df.index, columns=df.columns)


def hierarchical_recluster(
    dist: pd.DataFrame,
    k: int,
    method: str = "average",
    renumber_by_size: bool = True,
) -> pd.DataFrame:
    dist = clean_distance_matrix(dist)
    condensed = squareform(dist.to_numpy(float), checks=False)
    z = linkage(condensed, method=method)
    labels = cut_tree(z, n_clusters=int(k)).ravel().astype(int) + 1
    out = pd.DataFrame({"bodyId": dist.index.astype(int), "cluster": labels})
    if renumber_by_size:
        order = out["cluster"].value_counts().sort_values(ascending=False).index.tolist()
        mapping = {old: i + 1 for i, old in enumerate(order)}
        out["cluster"] = out["cluster"].map(mapping).astype(int)
    sizes = out["cluster"].value_counts()
    out["cluster_size"] = out["cluster"].map(sizes).astype(int)
    out["linkage_method"] = method
    out["k"] = int(k)
    return out.sort_values(["cluster", "bodyId"]).reset_index(drop=True)


def recluster_sweep(dist: pd.DataFrame, methods: Iterable[str], k_values: Iterable[int]) -> dict[tuple[str, int], pd.DataFrame]:
    return {
        (method, int(k)): hierarchical_recluster(dist, int(k), method=method)
        for method in methods for k in k_values
    }


def compute_umap_from_distance(
    dist: pd.DataFrame,
    n_neighbors: int = 20,
    min_dist: float = 0.0,
    random_state: int = 42,
) -> pd.DataFrame:
    try:
        import umap
    except ImportError as e:
        raise ImportError("Install umap-learn to compute UMAP embeddings") from e
    dist = clean_distance_matrix(dist)
    reducer = umap.UMAP(
        metric="precomputed",
        n_neighbors=int(n_neighbors),
        min_dist=float(min_dist),
        random_state=int(random_state),
    )
    xy = reducer.fit_transform(dist.to_numpy(float))
    return pd.DataFrame({"bodyId": dist.index.astype(int), "umap1": xy[:, 0], "umap2": xy[:, 1]})
