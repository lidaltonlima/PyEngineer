"""Analysis structure in json file"""
import json

from ..objects import Node
from ..objects import Bar
from ..objects import Material
from ..objects import Section
from ..objects import Support
from ..objects import Load
from ..analysis import Linear

def calculate_json(path: str) -> Linear:
    """Analysis structure in json file

    Args:
        path (str): path to file

    Returns:
        Linear: the result of linear analysis
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create objects ///////////////////////////////////////////////////////////////////////////////
    # Materials ************************************************************************************
    materials: list[Material] = []
    for material in data['materials']:
        materials.append(Material(material['name'],
                                  material['properties']['E'],
                                  material['properties']['G'],
                                  material['properties']['ni'],
                                  material['properties']['rho']))
    # Sections *************************************************************************************
    sections: list[Section] = []
    for section in data['sections']:
        sections.append(Section(section['name'],
                                section['area'],
                                section['inertias']['Ix'],
                                section['inertias']['Iy'],
                                section['inertias']['Iz']))

    # Nodes ****************************************************************************************
    nodes: list[Node] = []
    for node in data['nodes']:
        nodes.append(Node(node['name'], node['position']))

    # Bars *****************************************************************************************
    start_node = Node('ERROR', [0, 0, 0])
    end_node = Node('ERROR', [0, 0, 0])
    section_bar = Section('ERROR', 0, 0, 0, 0)
    material_bar = Material('ERROR', 0, 0, 0, 0)
    bars: list[Bar] = []
    for index, bar in enumerate(data['bars']):
        for node in nodes:
            if node.name == bar['start_node']:
                start_node: Node = node
            elif node.name == bar['end_node']:
                end_node: Node = node

        for section in sections:
            if section.name == bar['section']:
                section_bar = section

        for material in materials:
            if material.name == bar['material']:
                material_bar = material

        bars.append(Bar(bar['name'],
                        start_node,
                        end_node,
                        section_bar,
                        material_bar,
                        bar['rotation']))
        bars[index].releases = bar['releases']

    # Supports *************************************************************************************
    supports = Support()
    node_support = Node('ERROR', [0, 0, 0])
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

    # Loads ***************************************************************************************
    loads: list[Load] = []
    for index, load in enumerate(data['loads']):
        loads.append(Load(load['name']))

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


    # Analysis and return /////////////////////////////////////////////////////////////////////////
    linear_analysis = Linear(nodes, bars, loads, supports)
    return linear_analysis
