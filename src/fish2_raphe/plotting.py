from __future__ import annotations

from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd


PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
    "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
]


def cluster_color_map(clusters) -> dict[int, str]:
    vals = sorted(set(int(x) for x in clusters))
    return {cl: PALETTE[(cl - 1) % len(PALETTE)] for cl in vals}


def camera_for_static_3d_view(
    view: str,
    side_direction: Literal["left", "right"] = "left",
):
    view = str(view).lower()
    if view == "top":
        return dict(eye=dict(x=0.0, y=0.0, z=2.35), up=dict(x=0, y=1, z=0))
    if view == "side":
        y = 2.35 if side_direction == "left" else -2.35
        return dict(eye=dict(x=0.0, y=y, z=0.0), up=dict(x=0, y=0, z=1))
    if view == "left":
        return dict(eye=dict(x=0.0, y=2.35, z=0.0), up=dict(x=0, y=0, z=1))
    if view == "right":
        return dict(eye=dict(x=0.0, y=-2.35, z=0.0), up=dict(x=0, y=0, z=1))
    if view == "coronal":
        return dict(eye=dict(x=2.35, y=0.0, z=0.0), up=dict(x=0, y=0, z=1))
    if view == "angled":
        return dict(eye=dict(x=1.55, y=1.65, z=1.15), up=dict(x=0, y=0, z=1))
    raise ValueError(f"Unknown 3D view: {view}")


def plot_umap_clusters(
    embedding: pd.DataFrame,
    assignments: pd.DataFrame,
    highlight_ids=None,
    title: str = "UMAP",
    figsize=(7.2, 6.2),
):
    emb = embedding.copy()
    assn = assignments.copy()
    emb["bodyId"] = emb["bodyId"].astype(int)
    assn["bodyId"] = assn["bodyId"].astype(int)
    assn["cluster"] = assn["cluster"].astype(int)
    df = emb.merge(assn[["bodyId", "cluster"]], on="bodyId", how="inner")
    colors = cluster_color_map(df["cluster"])
    fig, ax = plt.subplots(figsize=figsize)
    for cl, sub in df.groupby("cluster", sort=True):
        ax.scatter(sub["umap1"], sub["umap2"], s=32, color=colors[int(cl)], alpha=0.9,
                   edgecolor="white", linewidth=0.3, label=f"C{int(cl):02d} (n={len(sub)})")
    if highlight_ids:
        ids = set(int(x) for x in highlight_ids)
        h = df.loc[df["bodyId"].isin(ids)]
        ax.scatter(h["umap1"], h["umap2"], s=150, marker="*", color="yellow",
                   edgecolor="black", linewidth=0.8, zorder=10, label="checked IDs")
        for _, r in h.iterrows():
            ax.text(r["umap1"], r["umap2"], str(int(r["bodyId"])), fontsize=6)
    ax.set_title(title)
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.legend(frameon=False, fontsize=7, bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    return fig, ax, df
