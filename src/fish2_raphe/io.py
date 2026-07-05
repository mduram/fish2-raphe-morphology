from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


def find_first_existing(paths: Iterable[str | Path]) -> Path:
    checked = []
    for p in paths:
        p = Path(p)
        checked.append(p)
        if p.exists():
            return p
    msg = "\n".join(f"  - {p}" for p in checked)
    raise FileNotFoundError(f"None of the candidate paths exist:\n{msg}")


def load_distance_matrix(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() in {".pkl", ".pickle"}:
        df = pd.read_pickle(path)
    else:
        df = pd.read_csv(path, index_col=0)
    df.index = df.index.astype(int)
    df.columns = df.columns.astype(int)
    return df.astype(float)


def load_assignments(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"bodyId", "cluster"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Assignments file missing columns: {sorted(missing)}")
    df = df.copy()
    df["bodyId"] = df["bodyId"].astype(int)
    df["cluster"] = df["cluster"].astype(int)
    return df


def read_swc(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    rows = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 7:
                continue
            try:
                rows.append([
                    int(float(parts[0])), int(float(parts[1])),
                    float(parts[2]), float(parts[3]), float(parts[4]),
                    float(parts[5]), int(float(parts[6])),
                ])
            except ValueError:
                continue
    return pd.DataFrame(rows, columns=["node_id", "type", "x", "y", "z", "radius", "parent"])


def find_swc_path(body_id: int, candidate_dirs: Iterable[str | Path]) -> Path | None:
    body_id = int(body_id)
    seen = set()
    for d in candidate_dirs:
        d = Path(d)
        key = str(d.resolve()) if d.exists() else str(d)
        if key in seen:
            continue
        seen.add(key)
        if not d.exists():
            continue
        direct = d / f"{body_id}.swc"
        if direct.exists():
            return direct
        matches = sorted(d.glob(f"*{body_id}*.swc"))
        if matches:
            return matches[0]
    return None


def soma_or_root_xyz(swc: pd.DataFrame) -> np.ndarray | None:
    if swc is None or swc.empty:
        return None
    soma = swc.loc[swc["type"] == 1]
    if len(soma):
        return soma.iloc[0][["x", "y", "z"]].to_numpy(float)
    if swc["radius"].notna().any():
        row = swc.loc[swc["radius"].idxmax()]
        return row[["x", "y", "z"]].to_numpy(float)
    root = swc.loc[swc["parent"] < 0]
    if len(root):
        return root.iloc[0][["x", "y", "z"]].to_numpy(float)
    return swc[["x", "y", "z"]].median().to_numpy(float)
