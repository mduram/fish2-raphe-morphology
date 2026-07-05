# Fish2 Raphe Morphology

Private analysis repository for Fish2 EM raphe morphology, NBLAST clustering, 3D rendering, and upcoming connectivity/functional integration.

## Current datasets

1. **Selected raphe** — curated ~234 body IDs.
2. **Raphe-superior soma-in-ROI** — exact Raphe-superior-touching candidates filtered to the intended cell-body population.

## Repository layout

```text
notebooks/
  00_consolidated_workflow.ipynb
  01_selected_raphe_figures.ipynb
  02_raphe_superior_soma_in_roi_full.ipynb
  03_raphe_superior_soma_in_roi_recluster_figures.ipynb
  04_connectivity_next_steps.ipynb
src/fish2_raphe/
  clustering.py
  config.py
  io.py
  neuprint_tools.py
  plotting.py
configs/default.yaml
scripts/check_environment.py
```

## Setup

```bash
conda env create -f environment.yml
conda activate fish2_raphe
python scripts/check_environment.py
jupyter lab
```

## Authentication

Do **not** commit neuPrint tokens. Configure authentication through your local environment or the same secure token mechanism already used by your working FishFuncEM setup.

## Data policy

Large SWCs, meshes, NBLAST matrices, and generated figures are ignored by git. Keep them local or move them to a separate data store. The repository should contain code, small tables/configuration, and documentation.

## Recommended execution order

1. Run the full soma-in-ROI pipeline only when the candidate population or NBLAST result needs to change.
2. Use the consolidated/reclustering notebooks for rapid exploration without rerunning NBLAST.
3. Choose active linkage / `k` / UMAP settings.
4. Generate static top / true-lateral / angled 3D figures.
5. Run checked-ID overlays.
6. Next: connectivity and functional integration.
