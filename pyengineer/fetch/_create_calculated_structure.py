"""
Contains the create_json_calculated_structure function.
This function is responsible for creating a JSON file that represents the calculated structure.
"""
import json

from typing import List, Dict

from pyengineer.objects._load import INodalLoadData
from pyengineer.objects._support import ISupportSupports

from ..analysis._linear import Linear
from ..objects import Material, Section

def create_calculated_structure(path: str, analysis: Linear) -> None:
    """Create a JSON file representing the calculated structure.

    Args:
        path (str): _description_
        analysis (Linear): _description_
    """
    structure = {}

    # Materials and Sections //////////////////////////////////////////////////////////////////////
    # Get materials and sections from bars
    materials: List[Material]  = []
    sections: List[Section] = []
    for bar in analysis.bars:
        if bar.material not in materials:
            materials.append(bar.material)
        if bar.section not in sections:
            sections.append(bar.section)

    # Materials ***********************************************************************************
    material_dict: List[Dict[str, str | Dict[str, float]]] = []
    for material in materials:
        material_dict.append({
            'name': material.name,
            'properties': {
                'E': material.properties['E'],
                'G': material.properties['G'],
                'nu': material.properties['nu'],
                'rho': material.properties['rho']
            }
        })
    structure['materials'] = material_dict

    # Sections ************************************************************************************
    sections_dict: List[Dict[str, str | float | Dict[str, float]]] = []
    for section in sections:
        sections_dict.append({
            'name': section.name,
            'area': section.properties['area'],
            'inertias': {
                'Ix': section.properties['Ix'],
                'Iy': section.properties['Iy'],
                'Iz': section.properties['Iz']
            }
        })
    structure['sections'] = sections_dict

    # Nodes ///////////////////////////////////////////////////////////////////////////////////////
    nodes_dict: List[Dict[str, str | List[float]]] = []
    for node in analysis.nodes:
        nodes_dict.append({
            'name': node.name,
            'position': [node.position[0], node.position[1], node.position[2]]
        })
    structure['nodes'] = nodes_dict

    # Bars ////////////////////////////////////////////////////////////////////////////////////////
    bars_dict: List[Dict[str, str | float | List[str]]] = []
    for bar in analysis.bars:
        releases: List[str] = []
        for key, value in bar.releases.items():
            if value:
                releases.append(key)
        bars_dict.append({
            'name': bar.name,
            'start_node': bar.start_node.name,
            'end_node': bar.end_node.name,
            'section': bar.section.name,
            'material': bar.material.name,
            'rotation': bar.rotation,
            'releases': releases
        })
    structure['bars'] = bars_dict

    # Supports ////////////////////////////////////////////////////////////////////////////////////
    supports_dict: List[Dict[str, str | ISupportSupports]] = []
    for key, value in analysis.supports.nodes_support.items():
        supports_dict.append({
            'node': key.name,
            'supports': value
        })
    structure['supports'] = supports_dict

    # Loads ///////////////////////////////////////////////////////////////////////////////////////
    loads_dict: List[Dict[str,
                          str |
                          List[Dict[str,
                                    str | INodalLoadData]] |
                          Dict[str,
                               List[Dict[str, str | float | Dict[str, float]]] |
                               List[Dict[str, str | List[float] | Dict[str, List[float]]]]]
                          ]] = []
    for load in analysis.loads:
        # Nodal Loads *****************************************************************************
        node_load_dict: List[Dict[str, str | INodalLoadData]] = []
        for node in load.nodes_loads:
            for name, node_load in load.nodes_loads[node].items():
                node_load_dict.append({
                    'name': name,
                    'node': node.name,
                    'loads': node_load
                })

        # Bar Loads *******************************************************************************
        # Point loads -----------------------------------------------------------------------------
        bar_load_pt_dict: List[Dict[str, str | float | Dict[str, float]]] = []
        for bar in load.bars_loads_pt:
            for name, bar_load in load.bars_loads_pt[bar].items():
                bar_load_pt_dict.append({
                    'name': name,
                    'bar': bar.name,
                    'system': bar_load['system'],
                    'position': bar_load['position'],
                    'loads': {
                        'Fx': bar_load['Fx'],
                        'Fy': bar_load['Fy'],
                        'Fz': bar_load['Fz'],
                        'Mx': bar_load['Mx'],
                        'My': bar_load['My'],
                        'Mz': bar_load['Mz']
                    }
                })
        # Distributed loads -----------------------------------------------------------------------
        bar_load_dist_dict: List[Dict[str, str | List[float] | Dict[str, List[float]]]] = []
        for bar in load.bars_loads_dist:
            for name, bar_load in load.bars_loads_dist[bar].items():
                bar_load_dist_dict.append({
                    'name': name,
                    'bar': bar.name,
                    'system': bar_load['system'],
                    'position': [bar_load['x1'], bar_load['x2']],
                    'loads': {
                        'Fx': [bar_load['Fx'][0], bar_load['Fx'][1]],
                        'Fy': [bar_load['Fy'][0], bar_load['Fy'][1]],
                        'Fz': [bar_load['Fz'][0], bar_load['Fz'][1]],
                        'Mx': [bar_load['Mx'][0], bar_load['Mx'][1]],
                        'My': [bar_load['My'][0], bar_load['My'][1]],
                        'Mz': [bar_load['Mz'][0], bar_load['Mz'][1]]
                    }
                })

        # Append bar loads to the loads dictionary ************************************************
        loads_dict.append({
            'name': load.name,
            'nodes': node_load_dict,
            'bars': {
                'point': bar_load_pt_dict,
                'distributed': bar_load_dist_dict
            }
        })
    structure['loads'] = loads_dict

    # Results /////////////////////////////////////////////////////////////////////////////////////
    results: Dict[str, Dict[str, Dict[str, List[float]]]] = {}

    # Create dictionary structure for results *****************************************************
    for load in analysis.loads:
        # Get displacements for each node under the current load case -----------------------------
        displacements: Dict[str, List[float]] = {}
        for node in analysis.nodes:
            disp_vector = analysis.get_displacements(node.name, load.name)
            displacements[node.name] = disp_vector.tolist()
        results[load.name] = {'displacements': displacements}

        # Get reactions for each support under the current load case -----------------------------
        reactions: Dict[str, List[float]] = {}
        for node in analysis.supports.nodes_support.keys():
            reactions_vector = analysis.get_reactions(node.name, load.name)
            reactions[node.name] = reactions_vector.tolist()
        results[load.name]['reactions'] = reactions

        # Get extreme forces for each bar under the current load case -----------------------------
        extreme_forces: Dict[str, List[float]] = {}
        for bar in analysis.bars:
            forces_vector = bar.extreme_forces[load.name]
            extreme_forces[bar.name] = forces_vector.tolist()
        results[load.name]['extreme_forces'] = extreme_forces

    structure['results'] = results

    # Write results to JSON file //////////////////////////////////////////////////////////////////
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(structure, file, indent=2)
