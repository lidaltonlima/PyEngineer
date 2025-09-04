"""
Functions to calculate reactions in bars.
All functions fo point loads in "Análise de Estruturas" by
    Umberto Lima Soriano and Silvio de Souza Lima.
Distributed loads done with point load equivalents.
"""
from typing import Dict, Literal

from .space_2d import root_line

# Point loads /////////////////////////////////////////////////////////////////////////////////////
# Forces ******************************************************************************************
# Force in x direction ----------------------------------------------------------------------------
def pt_force_x(length: float,
               x: float,
               p: float) -> Dict[Literal['Rxa', 'Rxb'], float]:
    """Calculates the reactions of a bar with a point axial load in x direction.

    Args:
        length (float): Length of the bar
        x (float): Position of the load
        p (float): Intensity of the load

    Raises:
        ValueError: If the position is not in the range 0 <= x <= L

    Returns:
        Dict[Literal['Rxa', 'Rxb'], float]: The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x <= length) is False:
        raise ValueError("Need 0 <= x <= L.")

    a = x
    b = length - x
    l = length
    reaction_a = -p * b / l
    reaction_b = -p * a / l

    return {'Rxa': reaction_a, 'Rxb': reaction_b}

# Force in y direction ----------------------------------------------------------------------------
def pt_force_y(length: float,
               x: float,
               p: float) -> Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
    """Calculates the reactions of a bar with a point transverse load in y direction.

    Args:
        length (float): Length of the bar
        x (float): Position of the load
        p (float): Intensity of the load

    Raises:
        ValueError: If the position is not in the range 0 <= x <= L

    Returns:
        Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x <= length) is False:
        raise ValueError("Need 0 <= x <= L.")

    a = x
    b = length - x
    l = length

    moment_a = -(p * a * b**2) / l**2
    moment_b = (p * a**2 * b) / l**2
    reaction_a = -((p * b / l) - (moment_a + moment_b) / l)
    reaction_b = -((p * a / l) + (moment_a + moment_b) / l)

    return {'Rya': reaction_a, 'Ryb': reaction_b, 'Mza': moment_a, 'Mzb': moment_b}

# Force in z direction ----------------------------------------------------------------------------
def pt_force_z(length: float,
               x: float,
               p: float) -> Dict[Literal['Rza', 'Rzb', 'Mya', 'Myb'], float]:
    """Calculates the reactions of a bar with a point transverse load in z direction.

    Args:
        length (float): Length of the bar
        x (float): Position of the load
        p (float): Intensity of the load

    Raises:
        ValueError: If the position is not in the range 0 <= x <= L

    Returns:
        Dict[Literal['Rza', 'Rzb', 'Mya', 'Myb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x <= length) is False:
        raise ValueError("Need 0 <= x <= L.")

    a = x
    b = length - x
    l = length

    moment_a = (p * a * b**2) / l**2
    moment_b = -(p * a**2 * b) / l**2
    reaction_a = -((p * b / l) + (moment_a + moment_b) / l)
    reaction_b = -((p * a / l) - (moment_a + moment_b) / l)

    return {'Rza': reaction_a, 'Rzb': reaction_b, 'Mya': moment_a, 'Myb': moment_b}

# Moments *****************************************************************************************
# Moment in x direction ---------------------------------------------------------------------------
def pt_moment_x(length: float,
                x: float,
                m: float) -> Dict[Literal['Mxa', 'Mxb'], float]:
    """Calculates the reactions of a bar with a point moment around x axis.
    Args:
        length (float): Length of the bar
        x (float): Position of the moment
        m (float): Intensity of the moment
    Raises:
        ValueError: If the position is not in the range 0 <= x <= L
    Returns:
        Dict[Literal['Mxa', 'Mxb'], float]: The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x <= length) is False:
        raise ValueError("Need 0 <= x <= L.")

    a = x
    b = length - x
    l = length

    torque_a = -m * b / l
    torque_b = -m * a / l

    return {'Mxa': torque_a, 'Mxb': torque_b}

# Moment in y direction ---------------------------------------------------------------------------
def pt_moment_y(length: float,
                x: float,
                m: float) -> Dict[Literal['Mya', 'Myb', 'Rza', 'Rzb'], float]:
    """Calculates the reactions of a bar with a point moment around y axis.
    Args:
        length (float): Length of the bar
        x (float): Position of the moment
        m (float): Intensity of the moment
    Raises:
        ValueError: If the position is not in the range 0 <= x <= L
    Returns:
        Dict[Literal['Mya', 'Myb', 'Rza', 'Rzb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x <= length) is False:
        raise ValueError("Need 0 <= x <= L.")

    a = x
    b = length - x
    l = length

    moment_a = ((m * b) / l**2) * (2*a - b)
    moment_b = ((m * a) / l**2) * (2*b - a)
    reaction_a = -(6 * m * a * b) / l**3
    reaction_b = (6 * m * a * b) / l**3

    return {'Mya': moment_a, 'Myb': moment_b, 'Rza': reaction_a, 'Rzb': reaction_b}

# Moment in z direction ---------------------------------------------------------------------------
def pt_moment_z(length: float,
                x: float,
                m: float) -> Dict[Literal['Mza', 'Mzb', 'Rya', 'Ryb'], float]:
    """Calculates the reactions of a bar with a point moment around z axis.
    Args:
        length (float): Length of the bar
        x (float): Position of the moment
        m (float): Intensity of the moment
    Raises:
        ValueError: If the position is not in the range 0 <= x <= L
    Returns:
        Dict[Literal['Mza', 'Mzb', 'Rya', 'Ryb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x <= length) is False:
        raise ValueError("Need 0 <= x <= L.")

    a = x
    b = length - x
    l = length

    moment_a = ((m * b) / l**2) * (2*a - b)
    moment_b = ((m * a) / l**2) * (2*b - a)
    reaction_a = (6 * m * a * b) / l**3
    reaction_b = -(6 * m * a * b) / l**3

    return {'Mza': moment_a, 'Mzb': moment_b, 'Rya': reaction_a, 'Ryb': reaction_b}

# Distributed loads ///////////////////////////////////////////////////////////////////////////////
# Force in all length of the bar ******************************************************************
# y direction -------------------------------------------------------------------------------------
def all_dist_force_y_rec(
        length: float,
        p: float
    ) -> Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
    """Calculates the reactions of a bar with a distributed load in x direction and in all length
        of the bar.

    Args:
        length (float): Length of the bar
        x (float): Position of the load
        p (float): Intensity of the load

    Returns:
        Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    l = length

    moment_a = -(p * l**2) / 12
    moment_b = (p * l**2) / 12
    reaction_a = -(p * l) / 2
    reaction_b = -(p * l) / 2

    return {'Rya': reaction_a, 'Ryb': reaction_b, 'Mza': moment_a, 'Mzb': moment_b}

def all_dist_force_y_tri(
        length: float,
        p: float,
        direction: Literal['up', 'down']
    ) -> Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
    """Calculates the reactions of a bar with a distributed load in y direction and in all length
        of the bar.

    Args:
        length (float): Length of the bar
        x (float): Position of the load
        p (float): Intensity of the load

    Raises:
        ValueError: If the direction is not 'up' or 'down'

    Returns:
        Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    l = length

    reactions: Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float] = \
        {'Rya': 0, 'Ryb': 0, 'Mza': 0, 'Mzb': 0}

    match direction:
        case 'up':
            reactions['Mza'] = -(p * l**2) / 30
            reactions['Mzb'] = (p * l**2) / 20
            reactions['Rya'] = -(3 * p * l) / 20
            reactions['Ryb'] = -(7 * p * l) / 20
        case 'down':
            reactions['Mza'] = -(p * l**2) / 20
            reactions['Mzb'] = (p * l**2) / 30
            reactions['Rya'] = -(7 * p * l) / 20
            reactions['Ryb'] = -(3 * p * l) / 20
        case _:
            raise ValueError('Direction only "up" and "down"')

    return reactions

def all_dist_force_y_trap(
        length: float,
        p1: float, p2: float
    ) -> Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
    """Calculates the reactions of a bar with a trapezoidal distributed axial load in y direction
        and all length of the bar.
    Args:
        length (float): Length of the bar
        p1 (float): Intensity of the load at the start position
        p2 (float): Intensity of the load at the end position
    Raises:
        ValueError: If the positions are not in the range 0 <= x1 < x2 <= L
    Returns:
        Dict[Literal['Rxa', 'Rxb'], float]: The reactions at the two ends of the bar (A and B)
    """
    if p1 == p2 == 0:
        return {'Rya': 0, 'Ryb': 0, 'Mza': 0, 'Mzb': 0}

    rectangular_reactions: Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float] = \
        {'Rya': 0, 'Ryb': 0, 'Mza': 0, 'Mzb': 0}
    triangular_reactions: Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float] = \
        {'Rya': 0, 'Ryb': 0, 'Mza': 0, 'Mzb': 0}
    if p1 >= 0 and p2 >= 0:
        # If both loads are positive then we can have a rectangular and a triangular load.
        # Both positive loads.
        if p1 != 0 and p2 != 0:
            rectangular_reactions = all_dist_force_y_rec(length, min(p1, p2))

        # Verify if we have an ascending or descending triangle.
        if p1 < p2:
            triangular_reactions = all_dist_force_y_tri(length, p2 - p1, 'up')
        elif p1 > p2:
            triangular_reactions = all_dist_force_y_tri(length, p1 - p2, 'down')
    elif p1 <= 0 and p2 <= 0:
        # If both loads are positive then we can have a rectangular and a triangular load.
        # Both negative loads.
        if p1 != 0 and p2 != 0:
            rectangular_reactions = all_dist_force_y_rec(length, max(p1, p2))

        # Verify if we have an ascending or descending triangle.
        if abs(p1) < abs(p2):
            triangular_reactions = all_dist_force_y_tri(length, -(abs(p2) - abs(p1)), 'up')
        elif abs(p1) > abs(p2):
            triangular_reactions = all_dist_force_y_tri(length, -(abs(p1) - abs(p2)), 'down')
    else:
        # If the loads have different signs we have to split the trapezoid in two triangles.
        # One positive load and one negative load.
        root = root_line((0, p1), (length, p2)) # Find the root of the line

        # Add reaction directly to the start of the bar
        triangular_reactions_1 = all_dist_force_y_tri(root, p1, 'down')
        triangular_reactions['Rya'] += triangular_reactions_1['Rya']
        triangular_reactions['Mza'] += triangular_reactions_1['Mza']

        # Add reaction directly to the end of the bar
        triangular_reactions_2 = all_dist_force_y_tri(length - root, p2, 'up')
        triangular_reactions['Ryb'] += triangular_reactions_2['Ryb']
        triangular_reactions['Mzb'] += triangular_reactions_2['Mzb']

        # Get reaction global because the reaction force local and add
        force = -(triangular_reactions_1['Ryb'] + triangular_reactions_2['Rya'])
        triangular_reactions_aux_1 = pt_force_y(length, root, force)
        triangular_reactions['Rya'] += triangular_reactions_aux_1['Rya']
        triangular_reactions['Ryb'] += triangular_reactions_aux_1['Ryb']
        triangular_reactions['Mza'] += triangular_reactions_aux_1['Mza']
        triangular_reactions['Mzb'] += triangular_reactions_aux_1['Mzb']

        # Get reaction global because the reaction moment local and add
        moment = -(triangular_reactions_1['Mzb'] + triangular_reactions_2['Mza'])
        triangular_reactions_aux_2 = pt_moment_z(length, root, moment)
        triangular_reactions['Rya'] += triangular_reactions_aux_2['Rya']
        triangular_reactions['Ryb'] += triangular_reactions_aux_2['Ryb']
        triangular_reactions['Mza'] += triangular_reactions_aux_2['Mza']
        triangular_reactions['Mzb'] += triangular_reactions_aux_2['Mzb']


    reactions: Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float] = {
        'Rya': rectangular_reactions['Rya'] + triangular_reactions['Rya'],
        'Ryb': rectangular_reactions['Ryb'] + triangular_reactions['Ryb'],
        'Mza': rectangular_reactions['Mza'] + triangular_reactions['Mza'],
        'Mzb': rectangular_reactions['Mzb'] + triangular_reactions['Mzb']
    }

    return reactions

# Forces in x direction ***************************************************************************
# Rectangular distributed load --------------------------------------------------------------------
def dist_force_x_rec(length: float,
                     x1: float, x2: float,
                     p: float,) -> Dict[Literal['Rxa', 'Rxb'], float]:
    """Calculates the reactions of a bar with a distributed axial load in x direction.

    Args:
        length (float): Length of the bar
        x1 (float): Start position of the load
        x2 (float): End position of the load
        p (float): Intensity of the load

    Raises:
        ValueError: If the positions are not in the range 0 <= x1 < x2 <= L

    Returns:
        Dict[Literal['Rxa', 'Rxb'], float]: The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x1 < x2 <= length) is False:
        raise ValueError("Need 0 <= x1 < x2 <= L.")

    c = x2 - x1  # length of the distributed load

    equivalent_force = p * c  # equivalent point force
    point_application = x1 + c / 2 # point of application of the equivalent force

    reactions = pt_force_x(length, point_application, equivalent_force)

    return reactions

# Triangular distributed load ---------------------------------------------------------------------
def dist_force_x_tri(length: float,
                     x1: float, x2: float,
                     p: float,
                     direction: Literal['up', 'down']) -> Dict[Literal['Rxa', 'Rxb'], float]:
    """Calculates the reactions of a bar with a triangular distributed axial load in x direction.
        Ascending or descending.
    Args:
        length (float): Length of the bar
        x1 (float): Start position of the load
        x2 (float): End position of the load
        p (float): Intensity of the load at the larger end
        direction (Literal['up', 'down']): Direction of the load.
            'up' for ascending, 'down' for descending.
    Raises:
        ValueError: If the positions are not in the range 0 <= x1 < x2 <= L
        ValueError: If the direction is not 'up' or 'down'
    Returns:
        Dict[Literal['Rxa', 'Rxb'], float]: The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x1 < x2 <= length) is False:
        raise ValueError("Need 0 <= x1 < x2 <= L.")

    c = x2 - x1  # length of the distributed load
    equivalent_force = (p * c) / 2  # equivalent point force

    point_application: float = 0
    if direction == 'up':
        point_application = x1 + (2/3) * c # point of application of the equivalent force
    elif direction == 'down':
        point_application = x1 + (1/3) * c # point of application of the equivalent force
    else:
        raise ValueError("Direction must be 'up' or 'down'.")

    reactions = pt_force_x(length, point_application, equivalent_force)

    return reactions

# Trapezoidal distributed load --------------------------------------------------------------------
def dist_force_x_trap(length: float,
                      x1: float, x2: float,
                      p1: float, p2: float) -> Dict[Literal['Rxa', 'Rxb'], float]:
    """Calculates the reactions of a bar with a trapezoidal distributed axial load in x direction.
    Args:
        length (float): Length of the bar
        x1 (float): Start position of the load
        x2 (float): End position of the load
        p1 (float): Intensity of the load at the start position
        p2 (float): Intensity of the load at the end position
    Raises:
        ValueError: If the positions are not in the range 0 <= x1 < x2 <= L
    Returns:
        Dict[Literal['Rxa', 'Rxb'], float]: The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x1 < x2 <= length) is False:
        raise ValueError("Need 0 <= x1 < x2 <= L.")
    if p1 == p2 == 0:
        return {'Rxa': 0, 'Rxb': 0}

    rectangular_reactions: Dict[Literal['Rxa', 'Rxb'], float] = {'Rxa': 0, 'Rxb': 0}
    triangular_reactions: Dict[Literal['Rxa', 'Rxb'], float] = {'Rxa': 0, 'Rxb': 0}
    if p1 >= 0 and p2 >= 0:
        # If both loads are positive then we can have a rectangular and a triangular load.
        # Both positive loads.
        if p1 != 0 and p2 != 0:
            rectangular_reactions = dist_force_x_rec(length, x1, x2, min(p1, p2))

        # Verify if we have an ascending or descending triangle.
        if p1 < p2:
            triangular_reactions = dist_force_x_tri(length, x1, x2, p2 - p1, 'up')
        elif p1 > p2:
            triangular_reactions = dist_force_x_tri(length, x1, x2, p1 - p2, 'down')
    elif p1 <= 0 and p2 <= 0:
        # If both loads are positive then we can have a rectangular and a triangular load.
        # Both negative loads.
        if p1 != 0 and p2 != 0:
            rectangular_reactions = dist_force_x_rec(length, x1, x2, max(p1, p2))

        # Verify if we have an ascending or descending triangle.
        if abs(p1) < abs(p2):
            triangular_reactions = dist_force_x_tri(length, x1, x2, -(abs(p2) - abs(p1)), 'up')
        elif abs(p1) > abs(p2):
            triangular_reactions = dist_force_x_tri(length, x1, x2, -(abs(p1) - abs(p2)), 'down')
    else:
        # If the loads have different signs we have to split the trapezoid in two triangles.
        # One positive load and one negative load.
        root = root_line((x1, p1), (x2, p2)) # Find the root of the line
        triangular_reactions = dist_force_x_tri(length, x1, root, p1, 'down')
        triangular_reactions_2 = dist_force_x_tri(length, root, x2, p2, 'up')
        triangular_reactions['Rxa'] += triangular_reactions_2['Rxa']
        triangular_reactions['Rxb'] += triangular_reactions_2['Rxb']


    reactions: Dict[Literal['Rxa', 'Rxb'], float] = {
        'Rxa': rectangular_reactions['Rxa'] + triangular_reactions['Rxa'],
        'Rxb': rectangular_reactions['Rxb'] + triangular_reactions['Rxb']
    }

    return reactions

# Forces in y direction ***************************************************************************
# Rectangular distributed load --------------------------------------------------------------------
def dist_force_y_rec(
        length: float,
        x1: float, x2: float,
        p: float
    ) -> Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
    """Calculates the reactions of a bar with a distributed axial load in y direction.

    Args:
        length (float): Length of the bar
        x1 (float): Start position of the load
        x2 (float): End position of the load
        p (float): Intensity of the load

    Raises:
        ValueError: If the positions are not in the range 0 <= x1 < x2 <= L

    Returns:
        Dict[Literal['Rxa', 'Rxb', 'Mza', 'Mzb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x1 < x2 <= length) is False:
        raise ValueError("Need 0 <= x1 < x2 <= L.")

    reactions_local = all_dist_force_y_rec(x2 - x1, p)

    # For local reaction calculate global reactions
    aux_1 = pt_force_y(length, x1, -reactions_local['Rya'])
    aux_2 = pt_force_y(length, x2, -reactions_local['Ryb'])
    aux_3 = pt_moment_z(length, x1, -reactions_local['Mza'])
    aux_4 = pt_moment_z(length, x2, -reactions_local['Mzb'])

    # Sum all reactions with principle of superposition of effects
    reactions: Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float] = {
        'Rya': aux_1['Rya'] + aux_2['Rya'] + aux_3['Rya'] + aux_4['Rya'],
        'Ryb': aux_1['Ryb'] + aux_2['Ryb'] + aux_3['Ryb'] + aux_4['Ryb'],
        'Mza': aux_1['Mza'] + aux_2['Mza'] + aux_3['Mza'] + aux_4['Mza'],
        'Mzb': aux_1['Mzb'] + aux_2['Mzb'] + aux_3['Mzb'] + aux_4['Mzb']
    }

    return reactions

# Triangular distributed load ---------------------------------------------------------------------
def dist_force_y_tri(
        length: float,
        x1: float, x2: float,
        p: float,
        direction: Literal['up', 'down']
    ) -> Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
    """Calculates the reactions of a bar with a triangular distributed axial load in y direction.
        Ascending or descending.
    Args:
        length (float): Length of the bar
        x1 (float): Start position of the load
        x2 (float): End position of the load
        p (float): Intensity of the load at the larger end
        direction (Literal['up', 'down']): Direction of the load.
            'up' for ascending, 'down' for descending.
    Raises:
        ValueError: If the positions are not in the range 0 <= x1 < x2 <= L
        ValueError: If the direction is not 'up' or 'down'
    Returns:
        Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x1 < x2 <= length) is False:
        raise ValueError("Need 0 <= x1 < x2 <= L.")

    reactions_local = all_dist_force_y_tri(x2 - x1, p, direction)

    # For local reaction calculate global reactions
    aux_1 = pt_force_y(length, x1, -reactions_local['Rya'])
    aux_2 = pt_force_y(length, x2, -reactions_local['Ryb'])
    aux_3 = pt_moment_z(length, x1, -reactions_local['Mza'])
    aux_4 = pt_moment_z(length, x2, -reactions_local['Mzb'])

    # Sum all reactions with principle of superposition of effects
    reactions: Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float] = {
        'Rya': aux_1['Rya'] + aux_2['Rya'] + aux_3['Rya'] + aux_4['Rya'],
        'Ryb': aux_1['Ryb'] + aux_2['Ryb'] + aux_3['Ryb'] + aux_4['Ryb'],
        'Mza': aux_1['Mza'] + aux_2['Mza'] + aux_3['Mza'] + aux_4['Mza'],
        'Mzb': aux_1['Mzb'] + aux_2['Mzb'] + aux_3['Mzb'] + aux_4['Mzb']
    }

    return reactions

# Trapezoidal distributed load --------------------------------------------------------------------
def dist_force_y_trap(length: float,
                      x1: float, x2: float,
                      p1: float, p2: float) -> Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
    """Calculates the reactions of a bar with a trapezoidal distributed axial load in y direction.
    Args:
        length (float): Length of the bar
        x1 (float): Start position of the load
        x2 (float): End position of the load
        p1 (float): Intensity of the load at the start position
        p2 (float): Intensity of the load at the end position
    Raises:
        ValueError: If the positions are not in the range 0 <= x1 < x2 <= L
    Returns:
        Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float]:
            The reactions at the two ends of the bar (A and B)
    """
    if (0 <= x1 < x2 <= length) is False:
        raise ValueError("Need 0 <= x1 < x2 <= L.")

    reactions_local = all_dist_force_y_trap(x2 - x1, p1, p2)

    # For local reaction calculate global reactions
    aux_1 = pt_force_y(length, x1, -reactions_local['Rya'])
    aux_2 = pt_force_y(length, x2, -reactions_local['Ryb'])
    aux_3 = pt_moment_z(length, x1, -reactions_local['Mza'])
    aux_4 = pt_moment_z(length, x2, -reactions_local['Mzb'])

    # Sum all reactions with principle of superposition of effects
    reactions: Dict[Literal['Rya', 'Ryb', 'Mza', 'Mzb'], float] = {
        'Rya': aux_1['Rya'] + aux_2['Rya'] + aux_3['Rya'] + aux_4['Rya'],
        'Ryb': aux_1['Ryb'] + aux_2['Ryb'] + aux_3['Ryb'] + aux_4['Ryb'],
        'Mza': aux_1['Mza'] + aux_2['Mza'] + aux_3['Mza'] + aux_4['Mza'],
        'Mzb': aux_1['Mzb'] + aux_2['Mzb'] + aux_3['Mzb'] + aux_4['Mzb']
    }

    return reactions
