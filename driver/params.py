"""All driver parameters live here. Field names carry their units."""
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "outputs"


@dataclass(frozen=True)
class VdPParams:
    """Van der Pol oscillator  x'' - mu(1 - x^2)x' + omega0^2 x = A_r cos(omega_r t)."""

    mu_dimensionless: float = 1.0
    omega0_rad_per_s: float = 1.0
    A_r_dimensionless: float = 0.0          # respiratory forcing amplitude (Stage 2)
    f_r_Hz: float = 0.25                    # respiratory frequency (Stage 2)


@dataclass(frozen=True)
class Stage1Settings:
    """Numerical settings for period measurement and calibration."""

    transient_cycles: int = 20              # cycles discarded before measuring
    measure_cycles: int = 20                # cycles used for period statistics
    samples_per_period: int = 4000          # uniform output sampling density
    rtol: float = 1e-9
    atol: float = 1e-11
    solver: str = "LSODA"                   # stiff-capable
    asymptotic_large_mu_coeff: float = 3.0 - 2.0 * 0.6931471805599453  # 1.614
