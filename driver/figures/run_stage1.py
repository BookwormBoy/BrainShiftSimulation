"""Run every Stage 1 figure and the calibration acceptance check.

Run:  python driver/figures/run_stage1.py [--show]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root, so this runs standalone

import numpy as np

from driver.analysis import calibrate_omega0, measure_period
from driver.params import VdPParams
from driver.plotting import save_metrics
from driver.figures import fig1a_phase_portrait, fig1b_mu_sweep, fig1c_period_vs_mu


def calibration_check():
    rows = []
    for mu in [0.5, 1.0, 2.0, 5.0]:
        for T in [0.5, 0.857, 1.5]:
            w = calibrate_omega0(mu, T)
            Tm, _ = measure_period(VdPParams(mu_dimensionless=mu, omega0_rad_per_s=w))
            rows.append({"mu": mu, "T_target_s": T, "omega0_rad_per_s": w, "T_measured_s": Tm,
                         "rel_error": abs(Tm - T) / T})
            print(f"mu={mu:<4} T={T:<6} omega0={w:9.5f}  T_meas={Tm:.6f}  err={rows[-1]['rel_error']:.1e}")
    ok = all(r["rel_error"] < 1e-3 for r in rows)
    save_metrics("stage1", "calibration_check", {"pass_within_0.1pct": ok, "rows": rows})
    print("calibration acceptance (<0.1%%): %s" % ("PASS" if ok else "FAIL"))


if __name__ == "__main__":
    fig1a_phase_portrait.main()
    fig1b_mu_sweep.main()
    fig1c_period_vs_mu.main()
    calibration_check()
