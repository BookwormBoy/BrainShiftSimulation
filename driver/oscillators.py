"""Van der Pol oscillator (Stage 1). Pressure sources for later stages will live here too."""
import numpy as np
from scipy.integrate import solve_ivp

from .params import Stage1Settings, VdPParams


def vdp_rhs(t, y, p: VdPParams):
    """dx/dt = v ; dv/dt = mu(1-x^2)v - omega0^2 x + A_r cos(omega_r t)."""
    x, v = y
    forcing = 0.0
    if p.A_r_dimensionless:
        forcing = p.A_r_dimensionless * np.cos(2.0 * np.pi * p.f_r_Hz * t)
    return [v, p.mu_dimensionless * (1.0 - x * x) * v - p.omega0_rad_per_s ** 2 * x + forcing]


def integrate_vdp(p: VdPParams, y0, t_end, n_samples=None, t_eval=None,
                  s: Stage1Settings = Stage1Settings()):
    """Integrate on a uniform grid (stiff-capable solver). Returns (t, x, v)."""
    if t_eval is None:
        t_eval = np.linspace(0.0, t_end, n_samples)
    sol = solve_ivp(vdp_rhs, (t_eval[0], t_eval[-1]), y0, args=(p,), method=s.solver,
                    t_eval=t_eval, rtol=s.rtol, atol=s.atol)
    if not sol.success:
        raise RuntimeError(f"VdP integration failed: {sol.message}")
    return sol.t, sol.y[0], sol.y[1]


def period_guess(mu, omega0, s: Stage1Settings = Stage1Settings()):
    """Rough period used only to size the integration window (not a result)."""
    return max(2.0 * np.pi / omega0, s.asymptotic_large_mu_coeff * mu / omega0)
