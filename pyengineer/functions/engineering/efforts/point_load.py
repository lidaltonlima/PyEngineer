"""Efforts in segment"""
from typing import TypedDict

import numpy as np
from numpy import float64
from numpy.typing import NDArray


class PointLoad(TypedDict):
    """Point load in segment"""
    position: float  # Position of the load in the segment (0 to 1)
    system: str     # Coordinate system ('local' or 'global')
    Fx: float      # Force in X direction
    Fy: float      # Force in Y direction
    Fz: float      # Force in Z direction
    Mx: float      # Moment about X axis
    My: float      # Moment about Y axis
    Mz: float      # Moment about Z axis



def shear_y(x: float,
            length: float,
            pt_loads: list[PointLoad],
            extreme_forces: NDArray[float64] = \
                np.array([0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0], dtype=float64)) -> NDArray[float64]:
    """Shear force at position x due to point loads"""
    if x < 0 or x > length:
        raise ValueError("Position x is out of bounds")

    if x == 0:
        return np.array([0, extreme_forces[1]], dtype=float64)
    if x == length:
        return np.array([extreme_forces[7], 0], dtype=float64)

    vy = np.array([extreme_forces[1], extreme_forces[1]], dtype=float64)
    for load in pt_loads:
        if load['position'] < x:
            vy[0] += load['Fy']
        if load['position'] <= x:
            vy[1] += load['Fy']
    return vy

def shear_z(x: float,
            length: float,
            pt_loads: list[PointLoad],
            extreme_forces: NDArray[float64] = \
                np.array([0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0], dtype=float64)) -> NDArray[float64]:
    """Shear force at position x due to point loads"""
    if x < 0 or x > length:
        raise ValueError("Position x is out of bounds")

    if x == 0:
        return np.array([0, extreme_forces[2]], dtype=float64)
    if x == length:
        return np.array([extreme_forces[8], 0], dtype=float64)

    vz = np.array([extreme_forces[2], extreme_forces[2]], dtype=float64)
    for load in pt_loads:
        if load['position'] < x:
            vz[0] += load['Fz']
        if load['position'] <= x:
            vz[1] += load['Fz']
    return vz

def moment_y(x: float,
             length: float,
             pt_loads: list[PointLoad],
             extreme_forces: NDArray[float64] = \
                 np.array([0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0], dtype=float64)) -> NDArray[float64]:
    """Bending moment at position x due to point loads"""
    if x < 0 or x > length:
        raise ValueError("Position x is out of bounds")

    if x == 0:
        return np.array([0, extreme_forces[4]], dtype=float64)
    if x == length:
        return np.array([extreme_forces[10], 0], dtype=float64)

    disc = sorted([load['position'] for load in pt_loads if 0 < load['position'] < length])

    my = np.array([extreme_forces[4], extreme_forces[4]], dtype=float64)

    for load in pt_loads:
        if load['position'] < x:
            my[0] += load['My']
        if load['position'] <= x:
            my[1] += load['My']

    for i in range(len(disc) + 1):
        # Initial position of the segment
        if i == 0:
            x0 = 0
        else:
            x0 = disc[i - 1]

        # Final position of the segment
        if i == len(disc):
            x1 = length
        else:
            x1 = disc[i]

        if x0 < x <= x1:
            my[0] += shear_z(x, length, pt_loads, extreme_forces)[0] * (x - x0)
            my[1] += shear_z(x, length, pt_loads, extreme_forces)[0] * (x - x0)
            break

        my[0] += shear_z(x1, length, pt_loads, extreme_forces)[0] * (x1 - x0)
        my[1] += shear_z(x1, length, pt_loads, extreme_forces)[0] * (x1 - x0)


    return my

def moment_z(x: float,
             length: float,
             pt_loads: list[PointLoad],
             extreme_forces: NDArray[float64] = \
                 np.array([0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0], dtype=float64)) -> NDArray[float64]:
    """Bending moment at position x due to point loads"""
    if x < 0 or x > length:
        raise ValueError("Position x is out of bounds")

    if x == 0:
        return np.array([0, extreme_forces[5]], dtype=float64)
    if x == length:
        return np.array([extreme_forces[11], 0], dtype=float64)

    disc = sorted([load['position'] for load in pt_loads if 0 < load['position'] < length])

    mz = np.array([extreme_forces[5], extreme_forces[5]], dtype=float64)

    for load in pt_loads:
        if load['position'] < x:
            mz[0] -= load['Mz']
        if load['position'] <= x:
            mz[1] -= load['Mz']

    for i in range(len(disc) + 1):
        # Initial position of the segment
        if i == 0:
            x0 = 0
        else:
            x0 = disc[i - 1]

        # Final position of the segment
        if i == len(disc):
            x1 = length
        else:
            x1 = disc[i]

        if x0 < x <= x1:
            mz[0] += shear_y(x, length, pt_loads, extreme_forces)[0] * (x - x0)
            mz[1] += shear_y(x, length, pt_loads, extreme_forces)[0] * (x - x0)
            break

        mz[0] += shear_y(x1, length, pt_loads, extreme_forces)[0] * (x1 - x0)
        mz[1] += shear_y(x1, length, pt_loads, extreme_forces)[0] * (x1 - x0)


    return mz

# forces01 = np.array([0, -164.80, 0, 0, 0, 194.5,
#                             0, 435.20, 0, 0, 0, 320.5], dtype=float64)
# loads01: list[PointLoad] = [
#     {'position': 3, 'system': 'local',
#      'Fx': 0, 'Fy': 200, 'Fz': 0,
#      'Mx': 0, 'My': 0, 'Mz': 0},
#     {'position': 1, 'system': 'local',
#      'Fx': 0, 'Fy': 100, 'Fz': 0,
#      'Mx': 0, 'My': 0, 'Mz': 0},
#     {'position': 4.5, 'system': 'local',
#      'Fx': 0, 'Fy': 300, 'Fz': 0,
#      'Mx': 0, 'My': 0, 'Mz': 0},
#     {'position': 3.5, 'system': 'local',
#      'Fx': 0, 'Fy': 0, 'Fz': 0,
#      'Mx': 0, 'My': 0, 'Mz': -100},
#     {'position': 2, 'system': 'local',
#      'Fx': 0, 'Fy': 0, 'Fz': 0,
#      'Mx': 0, 'My': 0, 'Mz': 100}
# ]
# print(moment_z(4.5, 5, loads01, forces01))

forces02 = np.array([0, 0, -172, 0, 152.5, 0,
                     0, 0, 428, 0, 242.5, 0], dtype=float64)
loads02: list[PointLoad] = [
    {'position': 3, 'system': 'local',
     'Fx': 0, 'Fy': 0, 'Fz': 200,
     'Mx': 0, 'My': 0, 'Mz': 0},
    {'position': 1, 'system': 'local',
     'Fx': 0, 'Fy': 0, 'Fz': 100,
     'Mx': 0, 'My': 0, 'Mz': 0},
    {'position': 4.5, 'system': 'local',
     'Fx': 0, 'Fy': 0, 'Fz': 300,
     'Mx': 0, 'My': 0, 'Mz': 0},
    {'position': 3.5, 'system': 'local',
     'Fx': 0, 'Fy': 0, 'Fz': 0,
     'Mx': 0, 'My': -100, 'Mz': 0},
    {'position': 2, 'system': 'local',
     'Fx': 0, 'Fy': 0, 'Fz': 0,
     'Mx': 0, 'My': 100, 'Mz': 0}
]

print(moment_y(5, 5, loads02, forces02))
