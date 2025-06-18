"""Cálculo do pórtico 3"""
import numpy as np

import pyengineer as eng
from pyengineer import analysis


np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)


material = eng.Material('M1', 2e11, 7.692308e10, 0.3, 7850)
section = eng.Section('S1', 1.660260e-3, [1.968782e-8, 6.349660e-6, 8.195340e-7])

# Nodes
nodes = []
n1 = eng.Node('N1', [0, 0, 0])
nodes.append(n1)
n2 = eng.Node('N2', [0, 0, 10])
nodes.append(n2)
n3 = eng.Node('N3', [10, 0, 10])
nodes.append(n3)
n4 = eng.Node('N4', [0, 10, 10])
nodes.append(n4)
# Bars
bars = []
b1 = eng.Bar('B1', n2, n1, section, material)
bars.append(b1)
b2 = eng.Bar('B2', n2, n3, section, material)
bars.append(b2)
b3 = eng.Bar('B3', n2, n4, section, material)
bars.append(b3)

# Loads
loads = []
load = eng.Load('L1')
load.add_node_load('FN1', n2, 8000, 9000, 10000, 11000, 12000, 13000)
loads.append(load)

# Supports
support = eng.Support('SP1')
support.add_support(n1, [5e6, True, True, True, True, True])
support.add_pinned_support(n3)
support.add_support(n4, [True, 10e6, True, True, True, True])

a = analysis.Linear(nodes, bars, loads, support)
a.calculate_structure()

print(a.get_displacements('N1', 'L1'))
