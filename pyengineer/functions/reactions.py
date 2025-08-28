"""Functions to calculate reactions in bars."""
from typing import Tuple

def dist_x_force(length: float,
                     x1: float,
                     p1:float,
                     x2: float,
                     p2: float) -> Tuple[float, float]:
    """Calculates the reactions of a bar with a distributed axial load that varies linearly
    between two points (x1, p1) and (x2, p2).

    Args:
        length (float): Length of the bar
        x1 (float): Initial position of the load
        p1 (float): Initial intensity of the load
        x2 (float): Final position of the load
        p2 (float): Final intensity of the load

    Raises:
        ValueError: If the positions are not in the range 0 <= x1 < x2 <= L

    Returns:
        Tuple[float, float]: The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x1 < x2 <= length) is False:
        raise ValueError("Need 0 <= x1 < x2 <= L.")

    dx = x2 - x1
    # Resulting (área of the distributed load)
    w = 0.5 * (p1 + p2) * dx
    if abs(w) < 1e-14:
        return 0.0, 0.0

    # Angular coefficient of the linear load distribution
    m = (p2 - p1) / dx

    # First point: ∫ s*w(s) ds in [x1, x2]
    num = (
        p1 * ( (x2**2 - x1**2) / 2.0 )
        + m  * ( ( (x2**3 - x1**3) / 3.0 ) - x1 * ( (x2**2 - x1**2) / 2.0 ) )
    )
    x_bar = num / w  # Centroid (baricentro) of the load in along the bar

    # Compatibility (u(L)-u(0)=0) => ra = -w*(L - x_bar)/L ; RB = -w*x_bar/L
    reaction_a = -w * (length - x_bar) / length
    reaction_b = -w *  x_bar      / length
    return reaction_a, reaction_b

# # Example of usage
# L = 5.0   # Length of the bar
# x1, p1 = 1, 1e3  # Load starts at 1m with intensity of 1kN/m
# x2, p2 = 2.5, 3e3 # LOad ends at 2.5m with intensity of 3kN/m

# RA, RB = dist_x_force(L, x1, p1, x2, p2)
# print("Reação no apoio A:", RA)
# print("Reação no apoio B:", RB)
