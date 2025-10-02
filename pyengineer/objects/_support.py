"""Apoios que serão usados na estrutura"""
from typing import TypedDict
from ._node import Node

class ISupportSupports(TypedDict):
    """Typing for supports"""
    Dx: bool | float
    Dy: bool | float
    Dz: bool | float
    Rx: bool | float
    Ry: bool | float
    Rz: bool | float

class Support:
    """Supports for the structure"""
    nodes_support: dict[Node, ISupportSupports] # Node supports

    def __init__(self):
        """Supports for the structure

        Args:
            name (str): Name of the support set
        """
        self.nodes_support = {}

    def add_support(self,
                    node: Node,
                    dx: bool | float = False, dy: bool | float = False, dz: bool | float = False,
                    rx: bool | float = False, ry: bool | float = False, rz: bool | float = False):
        """Adiciona um apoio

        Args:
            node (Node): Nó em que estará o apoio.
            supports (list[bool | float]): (Dx, Dy, Dz, Rx, Ry, Rz)
                Restrições a deslocamentos e rotações nos eixo x, y e z respectivamente.
                Pode ser fixo/livre (bool) ou uma mola (float).
        """
        supports: ISupportSupports = {'Dx': dx, 'Dy': dy, 'Dz': dz, 'Rx': rx, 'Ry': ry, 'Rz': rz}
        for value in supports.values():
            if not isinstance(value, bool) and value == 0:
                raise ValueError("Um apoio não pode ter uma mola com valor '0'." \
                                 "Para apoio nulo use 'False'")

        self.nodes_support[node] = supports

    def add_fixed_support(self, node: Node):
        """Adiciona um apoio do tipo fixo

        Args:
            node (Node): Nó em que será colocado o apoio
        """

        self.nodes_support[node] = {'Dx': True, 'Dy': True, 'Dz': True,
                                    'Rx': True, 'Ry': True, 'Rz': True}

    def add_pinned_support(self, node: Node):
        """Adiciona um apoio fixo, mas que permite rotações

        Args:
            node (Node): Nó em ue será colocado o apoio
        """

        self.nodes_support[node] = {'Dx': True, 'Dy': True, 'Dz': True,
                                    'Rx': False, 'Ry': False, 'Rz': False}
    # def add_node_cantilever_roller_x(self, node: Node):
    #     if not node.name in self.nodes_support:
    #         self.nodes_support[node.name] = list()
    #     self.nodes_support[node.name] = [False, True, True, False, False, False]
