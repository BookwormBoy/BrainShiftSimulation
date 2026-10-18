import numpy as np
import pytest

from driver.analysis import calibrate_omega0, limit_cycle, measure_period
from driver.oscillators import integrate_vdp, period_guess
from driver.params import Stage1Settings, VdPParams

S = Stage1Settings()


def test_small_mu_period_is_2pi():
    T, _ = measure_period(VdPParams(mu_dimensionless=0.05))
    assert T == pytest.approx(2 * np.pi, rel=2e-3)


def test_large_mu_period_matches_asymptote():
    T, _ = measure_period(VdPParams(mu_dimensionless=30.0))
    assert T == pytest.approx(S.asymptotic_large_mu_coeff * 30.0, rel=0.05)


@pytest.mark.parametrize("y0", [(0.01, 0.0), (4.0, 4.0), (-3.0, 2.0), (1.0, -3.0), (-4.0, -4.0)])
def test_all_ics_reach_same_limit_cycle(y0):
    p = VdPParams(mu_dimensionless=1.0)
    ref = limit_cycle(p)["x_max"]
    T = period_guess(1.0, 1.0)
    t, x, v = integrate_vdp(p, y0, (S.transient_cycles + 5) * T, n_samples=40000)
    assert x[t > S.transient_cycles * T].max() == pytest.approx(ref, rel=0.01)


@pytest.mark.parametrize("mu,T", [(0.5, 0.5), (1.0, 0.857), (5.0, 1.5), (5.0, 0.5)])
def test_calibration(mu, T):
    w = calibrate_omega0(mu, T)
    Tm, _ = measure_period(VdPParams(mu_dimensionless=mu, omega0_rad_per_s=w))
    assert Tm == pytest.approx(T, rel=1e-3)
