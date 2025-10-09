"""Example generate calculate structure from Excel."""
# pylint: disable=C0413
# Add project root to sys.path for imports ////////////////////////////////////////////////////////
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
sys.path.append(project_root)
# /////////////////////////////////////////////////////////////////////////////////////////////////

import numpy as np

import pyengineer as pg
from pyengineer import analysis
from pyengineer.functions.engineering.efforts import point_load

# Output format
np.set_printoptions(formatter={'float_kind': '{: .2f}'.format}, linewidth=200)

# Materials
material = pg.Material('steel', 2e11, 7.692308e10, 0.3, 7850)

# Sections
section = pg.Section('w150x13', area=1.63e-3, ix=1.39e-8, iy=6.2e-6, iz=8.28e-7)

# Nodes
nodes: list[pg.Node] = []
n1 = pg.Node('N1', [0, 0, 0])
nodes.append(n1)
n2 = pg.Node('N2', [3, 3, 3])
nodes.append(n2)

# Bars
bars: list[pg.Bar] = []
b1 = pg.Bar('B1', n1, n2, section, material)
bars.append(b1)


# Loads
loads: list[pg.Load] = []
load = pg.Load('L1')
loads.append(load)
load.add_bar_load_pt('PT1', b1, 1, 'local', fx=100, fy=200, fz=300, mx=100, my=200, mz=300)
load.add_bar_load_pt('PT2', b1, 3, 'local', fx=123, fy=123, fz=123, mx=123, my=123, mz=123)

# Supports
support = pg.Support()
support.add_support(n1, dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)
support.add_support(n2, dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)

# Analysis
linear_analysis = analysis.Linear(nodes, bars, loads, support)

# Results
bar_loads = list(loads[0].bars_loads_pt[b1].values())
bar_extreme_forces = bars[0].extreme_forces['L1']

# print(point_load.moment_y(0.0, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(0.5, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(1.0, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(1.5, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(2.0, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(2.5, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(3.0, b1.length, bar_loads, bar_extreme_forces))
print(point_load.moment_y(3.5, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(4.0, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(4.5, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(5.0, b1.length, bar_loads, bar_extreme_forces))
# print(point_load.moment_y(b1.length, b1.length, bar_loads, bar_extreme_forces))
