"""Figure 1b: one period of x(t) for a sweep of mu, time normalised by the period.

Run:  python driver/figures/fig1b_mu_sweep.py [--show]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root, so this runs standalone

import numpy as np

from driver.analysis import limit_cycle
from driver.params import VdPParams
from driver.plotting import finish, plt, save_metrics

MUS = [0.1, 0.5, 1.0, 2.0, 3.0, 5.0]


def main():
    fig, axes = plt.subplots(2, 3, figsize=(11, 5.5), sharex=True, sharey=True)
    metrics = {}
    for ax, mu in zip(axes.ravel(), MUS):
        lc = limit_cycle(VdPParams(mu_dimensionless=mu))
        ax.plot(lc["t"] / lc["period"], lc["x"], lw=2)
        ax.set_title(f"mu = {mu:g}   (T = {lc['period']:.2f})")
        ax.grid(alpha=0.3)
        metrics[str(mu)] = {"period": lc["period"], "x_min": lc["x_min"], "x_max": lc["x_max"]}
    for ax in axes[1]:
        ax.set_xlabel("t / T")
    for ax in axes[:, 0]:
        ax.set_ylabel("x")
    fig.suptitle("Fig 1b: van der Pol waveform vs mu (omega0 = 1): sinusoidal -> relaxation")
    fig.tight_layout()
    finish(fig, "stage1", "fig1b_mu_sweep")
    save_metrics("stage1", "fig1b_metrics", metrics)


if __name__ == "__main__":
    main()
