import numpy as np

from pyengineer import *
from pyengineer import analysis


np.set_printoptions(formatter={'float_kind': '{: .2e}'.format}, linewidth=200)

m = Material('M1', 2e11, 7.6923e10, 0.3, 7850)

supports = Section('S1', 3.91e-3, 3.891e-5, 2.836e-6, 1.295e-7)

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
b1 = Bar('B1', n1, n2, supports, m)
bars.append(b1)
b2 = Bar('B2', n2, n3, supports, m)
bars.append(b2)

# Loads
loads = list()
load = Load('L1')
load.add_node_load('FN1', n2, 8000, 9000)
loads.append(load)

# Supports
supports = Support('SP1')
supports.add_node_fixed(n1)
supports.add_node_fixed(n3)

a = analysis.Linear(nodes, bars, loads, supports)

print(a.calculate().values())
