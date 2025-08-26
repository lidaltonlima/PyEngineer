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

# Bars
bars: list[pg.Bar] = []
b1 = pg.Bar('B1', n1, n2, section, material, 23)
b1.releases['Dyi'] = True
b1.releases['Rxi'] = True
b1.releases['Ryi'] = True
b1.releases['Rzi'] = True
bars.append(b1)
b2 = pg.Bar('B2', n2, n3, section, material, 0)
bars.append(b2)


# Loads
loads: list[pg.Load] = []
load = pg.Load('L1')
load.add_node_load('FN1', n2, 1e3, 2e3, 3e3, 4e3, 5e3, 6e3)
loads.append(load)

# Supports
support = pg.Support()
support.add_support(n1, dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)
support.add_support(n3, dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)

# Analysis
linear_analysis = analysis.Linear(nodes, bars, loads, support)

# Results
print(linear_analysis.get_displacements('N2', 'L1'))
