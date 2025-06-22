"""Cálculo do pórtico 3"""
import json

import numpy as np

import pyengineer as pg
from pyengineer import analysis

np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)

FILE_PATH: str = './pyengineer/examples/portico_01.json'

with open(FILE_PATH, encoding='utf-8') as file:
    data = json.load(file)

# Create objects //////////////////////////////////////////////////////////////////////////////////
# Materials ***************************************************************************************
materials: list[pg.Material] = []
for material in data['materials']:
    materials.append(pg.Material(material['name'],
                                 material['properties']['E'],
                                 material['properties']['G'],
                                 material['properties']['ni'],
                                 material['properties']['rho']))
# Sections ****************************************************************************************
sections: list[pg.Section] = []
for section in data['sections']:
    sections.append(pg.Section(section['name'],
                               section['area'],
                               section['inertias']['Ix'],
                               section['inertias']['Iy'],
                               section['inertias']['Iz']))

# Nodes *******************************************************************************************
nodes: list[pg.Node] = []
for node in data['nodes']:
    nodes.append(pg.Node(node['name'], node['position']))

# Bars ********************************************************************************************
start_node = pg.Node('ERROR', [0, 0, 0])
end_node = pg.Node('ERROR', [0, 0, 0])
section_bar = pg.Section('ERROR', 0, 0, 0, 0)
material_bar = pg.Material('ERROR', 0, 0, 0, 0)
bars: list[pg.Bar] = []
for bar in data['bars']:
    for node in nodes:
        if node.name == bar['start_node']:
            start_node: pg.Node = node
        elif node.name == bar['end_node']:
            end_node: pg.Node = node

    for section in sections:
        if section.name == bar['section']:
            section_bar = section

    for material in materials:
        if material.name == bar['material']:
            material_bar = material

    bars.append(pg.Bar(bar['name'],
                       start_node,
                       end_node,
                       section_bar,
                       material_bar,
                       np.deg2rad(bar['rotation'])))

# Supports ****************************************************************************************
supports = pg.Support()
node_support = pg.Node('ERROR', [0, 0, 0])
for sup in data['supports']:
    for node in nodes:
        if node.name == sup['node']:
            node_support = node
    supports.add_support(node_support,
                        sup['supports']['Dx'],
                        sup['supports']['Dy'],
                        sup['supports']['Dz'],
                        sup['supports']['Rx'],
                        sup['supports']['Ry'],
                        sup['supports']['Rz'])

# Loads *******************************************************************************************
loads: list[pg.Load] = []
for index, load in enumerate(data['loads']):
    loads.append(pg.Load(load['name']))

    for node in nodes:
        for node_data in load['nodes_loads']:
            if node.name == node_data['node']:
                loads[index].add_node_load(node_data['name'],
                                           node,
                                           node_data['loads']['Fx'],
                                           node_data['loads']['Fy'],
                                           node_data['loads']['Fz'],
                                           node_data['loads']['Mx'],
                                           node_data['loads']['My'],
                                           node_data['loads']['Mz'])


# for node in nodes:
#     print(node.position)
linear_analysis = analysis.Linear(nodes, bars, loads, supports)
print(linear_analysis.get_displacements('N2', 'L1'))
