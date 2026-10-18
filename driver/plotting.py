"""Shared figure helpers: consistent output directory and optional display."""
import json
import sys
from pathlib import Path

import matplotlib

if "--show" not in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .params import OUTPUT_DIR


def stage_dir(stage: str) -> Path:
    d = OUTPUT_DIR / stage
    d.mkdir(parents=True, exist_ok=True)
    return d


def finish(fig, stage: str, name: str):
    """Save fig as PNG (and PDF); show it if the script was run with --show."""
    d = stage_dir(stage)
    fig.savefig(d / f"{name}.png", dpi=170, bbox_inches="tight")
    fig.savefig(d / f"{name}.pdf", bbox_inches="tight")
    print(f"saved {d / name}.png")
    if "--show" in sys.argv:
        plt.show()
    plt.close(fig)


def save_metrics(stage: str, name: str, metrics: dict):
    d = stage_dir(stage)
    with open(d / f"{name}.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"saved {d / name}.json")
