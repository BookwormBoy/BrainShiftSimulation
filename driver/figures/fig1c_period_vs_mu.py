"""Figure 1c: measured period vs mu (omega0 = 1) with the two asymptotes.

Run:  python driver/figures/fig1c_period_vs_mu.py [--show]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root, so this runs standalone

import numpy as np

from driver.analysis import measure_period
from driver.params import Stage1Settings, VdPParams
from driver.plotting import finish, plt, save_metrics, stage_dir

S = Stage1Settings()


def main():
    mus = np.logspace(-1.3, 1.3, 25)
    T, Tstd = np.array([measure_period(VdPParams(mu_dimensionless=m)) for m in mus]).T
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(mus, T, "ko-", ms=4, label="measured (zero crossings)")
    ax.loglog(mus, 2 * np.pi * np.ones_like(mus), "--", color="C0", label="mu << 1:  2*pi/omega0")
    ax.loglog(mus, S.asymptotic_large_mu_coeff * mus, "--", color="C3",
              label="mu >> 1:  1.614*mu/omega0")
    ax.set_xlabel("mu"); ax.set_ylabel("period [1/omega0 units, omega0 = 1]")
    ax.set_title("Fig 1c: van der Pol period vs mu"); ax.grid(alpha=0.3, which="both"); ax.legend()
    finish(fig, "stage1", "fig1c_period_vs_mu")
    np.savetxt(stage_dir("stage1") / "fig1c_period_vs_mu.csv",
               np.column_stack([mus, T, Tstd, 2 * np.pi * np.ones_like(mus),
                                S.asymptotic_large_mu_coeff * mus]),
               delimiter=",", header="mu,T_measured,T_std,T_asym_small_mu,T_asym_large_mu", comments="")
    save_metrics("stage1", "fig1c_metrics", {"mu": mus.tolist(), "T": T.tolist(), "T_std": Tstd.tolist()})


if __name__ == "__main__":
    main()
