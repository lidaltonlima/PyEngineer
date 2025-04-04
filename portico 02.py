import numpy as np

from pyengineer import *
from pyengineer import analysis


np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)


material = Material('M1', 2e11, 7.692308e10, 0.3, 7850)
section = Section('S1', 1.660260e-3, 6.349660e-6, 8.195340e-7, 1.968782e-8)

# Nodes
nodes = list()
n1 = Node('N1', 0, 0, 0)
nodes.append(n1)
n2 = Node('N2', 0, 0, 10)
nodes.append(n2)
n3 = Node('N3', 10, 0, 10)
nodes.append(n3)
n4 = Node('N4', 0, 10, 10)
nodes.append(n4)

# Bars
bars = list()
b1 = Bar('B1', n1, n2, section, material)
bars.append(b1)
b2 = Bar('B2', n2, n3, section, material)
bars.append(b2)
b2 = Bar('B3', n2, n4, section, material)
bars.append(b2)

# Loads
loads = list()
load = Load('L1')
load.add_node_load('FN1', n2, 8000, 9000, 10000, 11000, 12000, 13000)
loads.append(load)

# Supports
section = Support('SP1')
section.add_node_fixed(n1)
section.add_node_fixed(n3)
section.add_node_fixed(n4)

a = analysis.Linear(nodes, bars, loads, section)

print(a.calculate().values())
