"""Figure 1a: phase portrait -- many initial conditions converge to one limit cycle.

Run:  python driver/figures/fig1a_phase_portrait.py [--show]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root, so this runs standalone

import numpy as np

from driver.analysis import limit_cycle
from driver.oscillators import integrate_vdp, period_guess
from driver.params import Stage1Settings, VdPParams
from driver.plotting import finish, plt, save_metrics

MU = 1.0
S = Stage1Settings()
ICS = [(0.01, 0.0), (4.0, 4.0), (-3.0, 2.0), (1.0, -3.0), (-4.0, -4.0), (0.5, 0.5), (2.0, 0.0)]


def main():
    p = VdPParams(mu_dimensionless=MU)
    T = period_guess(MU, p.omega0_rad_per_s)
    lc = limit_cycle(p)
    fig, ax = plt.subplots(figsize=(6.5, 6))
    cmap = plt.get_cmap("tab10")
    metrics = {"mu": MU, "limit_cycle_x_max": lc["x_max"], "initial_conditions": []}
    amp_err = []
    for i, y0 in enumerate(ICS):
        # transient (drawn thin) ...
        t, x, v = integrate_vdp(p, y0, 4 * T, n_samples=4000, s=S)
        ax.plot(x, v, lw=0.9, color=cmap(i), label=f"IC = ({y0[0]:g}, {y0[1]:g})")
        ax.plot(*y0, "o", color=cmap(i), ms=5)
        # ... then amplitude after the transient has been discarded
        t2, x2, v2 = integrate_vdp(p, y0, (S.transient_cycles + 5) * T, n_samples=40000, s=S)
        x_amp = x2[t2 > S.transient_cycles * T].max()
        err = abs(x_amp - lc["x_max"]) / lc["x_max"]
        amp_err.append(err)
        metrics["initial_conditions"].append({"y0": list(y0), "x_max_after_transient": float(x_amp),
                                              "relative_amplitude_error": float(err)})
    ax.plot(lc["x"], lc["v"], "k-", lw=3.5, label="limit cycle", zorder=5)
    ax.set_xlabel("x"); ax.set_ylabel("v = dx/dt")
    ax.set_title(f"Fig 1a: van der Pol phase portrait (mu = {MU:g}, omega0 = 1)")
    ax.grid(alpha=0.3); ax.legend(fontsize=7, loc="upper right"); ax.set_aspect("equal")
    metrics["max_relative_amplitude_error"] = float(max(amp_err))
    metrics["pass_within_1pct"] = bool(max(amp_err) < 0.01)
    finish(fig, "stage1", "fig1a_phase_portrait")
    save_metrics("stage1", "fig1a_metrics", metrics)
    print("max amplitude error across ICs: %.2e (criterion < 1e-2)" % max(amp_err))


if __name__ == "__main__":
    main()
