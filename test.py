import numpy as np

from pyengineer import *
from pyengineer import analysis


np.set_printoptions(formatter={'float_kind': '{: .0e}'.format}, linewidth=200)

m = Material('M1', 2e11, 7.6923e10, 0.3, 7850)

s = Section('S1', 3.91e-3, 3.891e-5, 2.836e-6, 1.295e-7)

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
b1 = Bar('B1', n1, n2, s, m)
bars.append(b1)
b2 = Bar('B2', n2, n3, s, m)
bars.append(b2)

# Loads
loads = list()
l = Load('L1')
l.add_node_load('FN1', n2, 8000, 9000)
loads.append(l)

# Supports
s = Support('SP1')
s.add_node_fixed(n1)
s.add_node_fixed(n3)

a = analysis.Linear(nodes, bars, loads, s)

print(a.kg())
