# -*- coding: utf-8 -*-
"""Shared style + I/O helpers for the bioinf plot gallery.

Every figure:
  - English labels (publication convention), DejaVu Sans (bundled, no font install)
  - "Simulated data" watermark bottom-right
  - PNG 200 dpi into source/img/bio-plots/
Every dataset:
  - defined as a verbatim CSV string here in the script and echoed to stdout by
    dump(), so the article can quote it exactly as it appears
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(os.environ.get("BIO_PLOTS_REPO", "/mnt/g/CODE/BOHUYESHAN-APB.github.io")).resolve()
OUT = (REPO / "source" / "img" / "bio-plots").resolve()
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 200,
    "savefig.directory": str(OUT),
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 12.5,
    "axes.titlepad": 8,
    "axes.labelsize": 11.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.6,
    "legend.frameon": False,
    "legend.fontsize": 9.5,
    "figure.facecolor": "white",
    "axes.unicode_minus": False,
})

CAT = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
       "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]
UP, DOWN, NS = "#C0392B", "#2471A3", "#B0B0B0"


def _safe_name(name, ext):
    """Only a plain basename inside OUT is allowed - no separators, no dot-dot."""
    if os.sep in name or "/" in name or ".." in name:
        raise ValueError("figure name must be a plain basename: %r" % name)
    if not name.endswith(ext):
        name += ext
    target = (OUT / name).resolve()
    if not target.is_relative_to(OUT):
        raise ValueError("resolved path escapes output directory")
    return str(target)


def save(fig, name, watermark=True, mark=None):
    """Save figure as OUT/<name>.png with a data-provenance watermark.

    Default stamp is "Simulated data"; real-data figures pass their own
    mark (e.g. mark="Real structure data: PDB 6A15") so the figure itself
    states its provenance.
    """
    text = mark if mark is not None else (
        "Simulated data, for teaching only" if watermark else None)
    if text:
        fig.text(0.995, 0.003, text,
                 ha="right", va="bottom", fontsize=8, color="#9AA0A6", style="italic")
    fig.savefig(_safe_name(name, ".png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def dump(name, text):
    """Echo the verbatim dataset used by a figure to stdout as a fenced block."""
    print("=== DATA %s ===" % name)
    print(text.strip("\n"))
    print("=== END %s ===" % name)


def csv_cols(text):
    """Parse a verbatim CSV string -> (header list, {col: list of str})."""
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    header = lines[0].split(",")
    cols = {h: [] for h in header}
    for ln in lines[1:]:
        for h, v in zip(header, ln.split(",")):
            cols[h].append(v.strip())
    return header, cols


def num(cols, key):
    return np.array([float(x) for x in cols[key]])
