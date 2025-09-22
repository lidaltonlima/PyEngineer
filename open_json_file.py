"""Load and calculate json file"""
import numpy as np

from pyengineer.fetch import calculate_json, create_json_results

np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)

analysis = calculate_json('./pyengineer/examples/structure_010.json')
# print(analysis.get_displacements('N2', 'L1'))

create_json_results('./pyengineer/examples/structure_010_results.json', analysis)
