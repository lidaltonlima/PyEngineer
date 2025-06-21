"""Módulo para carregamentos/esforços"""
import typing as tp

from ._node import Node

class ILoadLoads(tp.TypedDict):
    """Type of loads"""
    Fx: float
    Fy: float
    Fz: float
    Mx: float
    My: float
    Mz: float

class Load:
    """Casos de carga que serão usadas na estrutura"""
    def __init__(self, name: str):
        """Construtor

        Args:
            name (str): Nome da carga
        """
        self.name = name
        self.nodes_loads: dict[Node, dict[str, ILoadLoads]] = {}
        self.bars_loads_pt = {}
        self.bars_loads_dist = {}

    def add_node_load(self, name: str, node: Node,
                      fx: float = 0, fy: float = 0, fz: float = 0,
                      mx: float = 0, my: float = 0, mz: float = 0):
        """Adiciona carregamentos e esforços

        Args:
            name (str): Nome do esforço
            node (Node): Nó em que será aplicado o esforço
            fx (float, optional): Força em "x". Defaults to 0.
            fy (float, optional): Força em "y". Defaults to 0.
            fz (float, optional): Força em "z". Defaults to 0.
            mx (float, optional): Momento em "x". Defaults to 0.
            my (float, optional): Momento em "y". Defaults to 0.
            mz (float, optional): Momento em "z". Defaults to 0.
        """

        if not node in self.nodes_loads:
            self.nodes_loads[node] = {}

        self.nodes_loads[node][name] = {'Fx': fx, 'Fy': fy, 'Fz': fz, 'Mx': mx, 'My': my, 'Mz': mz}
