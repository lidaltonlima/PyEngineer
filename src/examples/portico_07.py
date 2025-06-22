"""Cálculo do pórtico 3"""
import numpy as np

import pyengineer as pg
from pyengineer import analysis


np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)


material = pg.Material('M1', 2e11, 7.692308e10, 0.3, 7850)
section = pg.Section('S1', area=1.660260e-3, ix=1.968782e-8, iy=6.349660e-6, iz=8.195340e-7)

# Nodes
nodes: list[pg.Node] = []
n1 = pg.Node('N1', [0, 0, 0])
nodes.append(n1)
n2 = pg.Node('N2', [0, 0, 10])
nodes.append(n2)
n3 = pg.Node('N3', [10, 0, 10])
nodes.append(n3)
n4 = pg.Node('N4', [0, 10, 10])
nodes.append(n4)
# Bars
bars: list[pg.Bar] = []
b1 = pg.Bar('B1', n2, n1, section, material)
bars.append(b1)
b2 = pg.Bar('B2', n2, n3, section, material, rotation=np.pi / 4)
bars.append(b2)
b3 = pg.Bar('B3', n2, n4, section, material)
bars.append(b3)


# Loads
loads: list[pg.Load] = []
load = pg.Load('L1')
load.add_node_load('FN1', n2, 8000, 9000, 10000, 11000, 12000, 13000)
loads.append(load)

# Supports
support = pg.Support('SP1')
support.add_support(n1, dx=5e6, dy=False, dz=True, rx=True, ry=True, rz=True)
support.add_pinned_support(n3)
support.add_support(n4, dx=True, dy=10e6, dz=True, rx=True, ry=True, rz=10e6)

# Barra solta
n5 = pg.Node('N5', [3, 3, 3])
nodes.append(n5)
n6 = pg.Node('N6', [10, 3, 3])
nodes.append(n6)
b4 = pg.Bar('B3', n5, n6, section, material, rotation=np.deg2rad(37))
bars.append(b4)
support.add_support(n5, dx=True, dy=True, dz=True, rx=10e6, ry=True, rz=True)
load.add_node_load('FN2', n6, fz=10000)

linear_analysis = analysis.Linear(nodes, bars, loads, support)
linear_analysis.calculate_structure()

print(linear_analysis.get_displacements('N6', 'L1'))
