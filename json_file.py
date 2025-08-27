"""Load and calculate json file"""
import numpy as np

from pyengineer.fetch import calculate_json

np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)

analysis = calculate_json('./pyengineer/examples/no_linear.json')
print(analysis.get_displacements('N2', 'L1'))
