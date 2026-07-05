# Workflow

## Dataset A — selected raphe

Curated ~234 body IDs. The morphology analysis uses cached FishFuncEM/NBLAST distances, hierarchical reclustering, UMAP visualization, cluster lookup, and 3D rendering.

## Dataset B — Raphe-superior soma-in-ROI

1. Query neurons touching exact `Raphe_Superior` / `Raphe_Superior1` ROIs.
2. Filter to neurons whose soma/cell-body location is inside the intended Raphe-superior region using the notebook's current soma-in-ROI logic.
3. Fetch/QC skeletons.
4. Compute NBLAST once.
5. Explore hierarchical linkage methods, cluster counts, and UMAP hyperparameters without rerunning NBLAST.
6. Render soma locations, cluster-colored soma maps, individual clusters, and checked IDs in the clean brain shell.

## Next layer — connectivity and function

Planned analyses:

- input/output partners per neuron and per morphology cluster;
- connection matrices among raphe clusters and target populations;
- ROI-resolved connectivity;
- transmitter / annotation metadata where available;
- integration with functional imaging or activity-derived labels;
- comparison of connectivity-defined and morphology-defined classes.
