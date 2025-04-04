import numpy as np

from pyengineer import *
from pyengineer import analysis


np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)


material = Material('M1', 2e11, 1, 0.3, 7850)
section = Section('S1', 1.660260e-3, 1, 6.349660e-6, 1)

# Nodes
nodes = list()
n1 = Node('N1', 0, 0, 0)
nodes.append(n1)
n2 = Node('N2', 0, 10, 0)
nodes.append(n2)
n3 = Node('N3', 10, 10, 0)
nodes.append(n3)

# Bars
bars = list()
b1 = Bar('B1', n1, n2, section, material)
bars.append(b1)
b2 = Bar('B2', n2, n3, section, material)
bars.append(b2)

# Loads
loads = list()
load = Load('L1')
load.add_node_load('FN1', n2, 8000, 9000, 0, 0, 0, 10000)
loads.append(load)

# Supports
section = Support('SP1')
section.add_node_fixed(n1)
section.add_node_fixed(n3)

a = analysis.Linear(nodes, bars, loads, section)

print(a.calculate().values())
