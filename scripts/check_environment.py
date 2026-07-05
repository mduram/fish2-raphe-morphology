from __future__ import annotations

import importlib
import sys

PACKAGES = [
    "numpy", "pandas", "scipy", "sklearn", "matplotlib", "plotly",
    "umap", "neuprint", "navis", "tqdm", "yaml",
]

failed = []
for pkg in PACKAGES:
    try:
        mod = importlib.import_module(pkg)
        print(f"OK  {pkg:12s} {getattr(mod, '__version__', '')}")
    except Exception as e:
        failed.append((pkg, repr(e)))
        print(f"ERR {pkg:12s} {e}")

print("Python:", sys.version)
if failed:
    raise SystemExit(1)
