"""Period measurement, calibration and limit-cycle characterisation (Stage 1)."""
import numpy as np
from scipy.optimize import brentq

from .oscillators import integrate_vdp, period_guess
from .params import Stage1Settings, VdPParams

DEFAULT_IC = (0.5, 0.0)


def upward_zero_crossings(t, x):
    """Times of upward zero-crossings of x, by linear interpolation between samples."""
    i = np.nonzero((x[:-1] < 0.0) & (x[1:] >= 0.0))[0]
    return t[i] + (0.0 - x[i]) * (t[i + 1] - t[i]) / (x[i + 1] - x[i])


def _settled_trajectory(p, y0, s, extra_cycles):
    """Integrate past the transient; return (t, x, v) restricted to the post-transient part.

    Window is sized from a rough period guess; extended if too few crossings are found."""
    Tg = period_guess(p.mu_dimensionless, p.omega0_rad_per_s, s)
    n_cycles = s.transient_cycles + extra_cycles
    for _ in range(4):
        t_end = 1.3 * n_cycles * Tg
        n = int(s.samples_per_period * n_cycles * 1.3)
        t, x, v = integrate_vdp(p, y0, t_end, n_samples=n, s=s)
        zc = upward_zero_crossings(t, x)
        if len(zc) >= s.transient_cycles + extra_cycles + 1:
            return t, x, v, zc
        n_cycles *= 2
    raise RuntimeError("could not find enough zero crossings")


def measure_period(p: VdPParams, y0=DEFAULT_IC, s: Stage1Settings = Stage1Settings()):
    """Return (mean_period, std_period) from upward zero-crossings after discarding the
    first `transient_cycles` cycles."""
    t, x, v, zc = _settled_trajectory(p, y0, s, s.measure_cycles)
    zc = zc[s.transient_cycles:]
    periods = np.diff(zc)
    return float(periods.mean()), float(periods.std())


def limit_cycle(p: VdPParams, y0=DEFAULT_IC, s: Stage1Settings = Stage1Settings()):
    """One converged cycle (uniformly sampled) plus its period and extrema.

    Returns dict(t, x, v, period, x_min, x_max, v_min, v_max)."""
    t, x, v, zc = _settled_trajectory(p, y0, s, 3)
    zc = zc[s.transient_cycles:]
    a, b = zc[0], zc[1]
    m = (t >= a) & (t <= b)
    return dict(t=t[m] - a, x=x[m], v=v[m], period=float(b - a),
                x_min=float(x[m].min()), x_max=float(x[m].max()),
                v_min=float(v[m].min()), v_max=float(v[m].max()))


def limit_cycle_extrema(p: VdPParams, s: Stage1Settings = Stage1Settings()):
    """(x_min, x_max) of the converged limit cycle, measured over many cycles."""
    t, x, v, zc = _settled_trajectory(p, DEFAULT_IC, s, s.measure_cycles)
    m = t >= zc[s.transient_cycles]
    return float(x[m].min()), float(x[m].max())


def calibrate_omega0(mu, T_target, s: Stage1Settings = Stage1Settings(), xtol=1e-12):
    """Find omega0 such that the measured VdP period at `mu` equals `T_target` [s].

    Note: at fixed mu the period is NOT simply 1/omega0-scaled (rescaling time maps
    mu -> mu/omega0), hence the root find."""
    def f(w):
        return measure_period(VdPParams(mu_dimensionless=mu, omega0_rad_per_s=w), s=s)[0] - T_target

    # Period >= ~2*pi/omega0 and <= ~(2*pi + 1.614*mu)/omega0, so the root is bracketed by:
    lo = 0.98 * 2.0 * np.pi / T_target
    hi = 1.2 * (2.0 * np.pi + s.asymptotic_large_mu_coeff * mu) / T_target
    while f(lo) < 0:
        lo *= 0.8
    while f(hi) > 0:
        hi *= 1.5
    return float(brentq(f, lo, hi, xtol=xtol, rtol=1e-12))
