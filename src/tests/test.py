"""Only for testing purposes"""
from typing import Tuple

def dist_axial_force(length: float, x1: float, p1: float, x2: float, p2: float) -> Tuple[float, float]:
    if not (0 <= x1 < x2 <= length):
        raise ValueError("Need 0 <= x1 < x2 <= L.")

    dx = x2 - x1
    # Resulting (área of the distributed load)
    W = 0.5 * (p1 + p2) * dx
    if abs(W) < 1e-14:
        return 0.0, 0.0

    # Angular coefficient of the linear load distribution
    m = (p2 - p1) / dx

    # First point: ∫ s*w(s) ds in [x1, x2]
    num = (
        p1 * ( (x2**2 - x1**2) / 2.0 )
        + m  * ( ( (x2**3 - x1**3) / 3.0 ) - x1 * ( (x2**2 - x1**2) / 2.0 ) )
    )
    xbar = num / W  # Centroid (baricentro) of the load in along the bar

    # Compatibility (u(L)-u(0)=0) => RA = -W*(L - xbar)/L ; RB = -W*xbar/L
    ra = -W * (length - xbar) / length
    rb = -W *  xbar      / length
    return ra, rb

L = 5   # comprimento da barra
x1_test, p1_test = 1, 5e3  # início da carga
x2_test, p2_test = 2.5, 3e3 # fim da carga

RA, RB = dist_axial_force(L, x1_test, p1_test, x2_test, p2_test)
print("Reação no apoio A:", RA)
print("Reação no apoio B:", RB)
