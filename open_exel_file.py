"""Calculate structure from excel file."""
import numpy as np

from pyengineer.fetch import calculate_excel

np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)

analysis = calculate_excel(path='./pyengineer/examples/excel/structure_011.xlsx', load_name='L1')
print(analysis.get_displacements('N2', 'L1'))
