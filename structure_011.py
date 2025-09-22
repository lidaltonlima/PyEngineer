"""Cálculo do pórtico 3"""
import numpy as np

import pyengineer as pg
from pyengineer import analysis

# Output format
np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)

# Materials
material = pg.Material('steel', 2e11, 7.692308e10, 0.3, 7850)

# Sections
section = pg.Section('w150x13', area=1.63e-3, ix=1.39e-8, iy=6.2e-6, iz=8.28e-7)

# Nodes
nodes: list[pg.Node] = []
n1 = pg.Node('N1', [0, 0, 0])
nodes.append(n1)
n2 = pg.Node('N2', [0, 0, 5])
nodes.append(n2)
n3 = pg.Node('N3', [5, 0, 5])
nodes.append(n3)
n4 = pg.Node('N4', [5, 0, 0])
nodes.append(n4)

# Bars
bars: list[pg.Bar] = []
b1 = pg.Bar('B1', n1, n2, section, material, 23)
bars.append(b1)
b2 = pg.Bar('B2', n2, n3, section, material)
bars.append(b2)
b3 = pg.Bar('B3', n3, n4, section, material, 30)
bars.append(b3)


# Loads
loads: list[pg.Load] = []
load = pg.Load('L1')
loads.append(load)

load.add_bar_load_pt('FPB1', b3, 2.5, fz=1e3)

# Supports
support = pg.Support()
support.add_support(n1, dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)
support.add_support(n4, dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)

# Analysis
linear_analysis = analysis.Linear(nodes, bars, loads, support)

# Results
print(linear_analysis.get_displacements('N2', 'L1'))
