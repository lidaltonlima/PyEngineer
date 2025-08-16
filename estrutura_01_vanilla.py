"""Cálculo do pórtico 3"""
import numpy as np

import pyengineer as pg
from pyengineer import analysis


np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)



material = pg.Material('steel', 2e11, 7.692308e10, 0.3, 7850)
# section = pg.Section('w150x13', area=15.74e-4, ix=1.15e-8, iy=596.48e-8, iz=81.76e-8)
section = pg.Section('w150x13', area=1.66026e-3, ix=1.968782e-8, iy=6.34966e-6, iz=8.19534e-7)

# Nodes
nodes: list[pg.Node] = []
n1 = pg.Node('N1', [0, 0, 0])
nodes.append(n1)
n2 = pg.Node('N2', [5, 0, 0])
nodes.append(n2)

# Bars
bars: list[pg.Bar] = []
b1 = pg.Bar('B1', n1, n2, section, material, 23)
bars.append(b1)


# Loads
loads: list[pg.Load] = []
load = pg.Load('L1')
load.add_node_load('FN1', n2, 10e3, 11e3, 12e3, 10e3, 11e3, 12e3)
loads.append(load)

# Supports
support = pg.Support()
support.add_support(n1, dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)

linear_analysis = analysis.Linear(nodes, bars, loads, support)

print(linear_analysis.get_displacements('N2', 'L1'))
