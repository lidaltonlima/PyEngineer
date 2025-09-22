"""Create JSON results file for calculated structure"""
from typing import Dict, List
import json

from ..analysis._linear import Linear


def create_json_results(path: str, analysis: Linear) -> None:
    """Create a JSON results file for the linear analysis.

    Args:
        path (str): The path to the JSON file to create.
        analysis (Linear): The linear analysis object containing results.
    """
    results: Dict[str, Dict[str, Dict[str, List[float]]]] = {}

    # Create dictionary structure for results /////////////////////////////////////////////////////
    for load in analysis.loads:
        # Get displacements for each node under the current load case *****************************
        displacements: Dict[str, List[float]] = {}
        for node in analysis.nodes:
            disp_vector = analysis.get_displacements(node.name, load.name)
            displacements[node.name] = disp_vector.tolist()
        results[load.name] = {'displacements': displacements}

        # Get reactions for each support under the current load case ******************************
        reactions: Dict[str, List[float]] = {}
        for node in analysis.supports.nodes_support.keys():
            reactions_vector = analysis.get_reactions(node.name, load.name)
            reactions[node.name] = reactions_vector.tolist()
        results[load.name]['reactions'] = reactions

        # Get extreme forces for each bar under the current load case *****************************
        extreme_forces: Dict[str, List[float]] = {}
        for bar in analysis.bars:
            forces_vector = bar.extreme_forces[load.name]
            extreme_forces[bar.name] = forces_vector.tolist()
        results[load.name]['extreme_forces'] = extreme_forces

    # Write results to JSON file //////////////////////////////////////////////////////////////////
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=2)
