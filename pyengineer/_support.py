"""Apoios que serão usados na estrutura"""
from ._node import Node

class Support:
    """Apoios da estrutura"""
    def __init__(self, name: str):
        """Construtor

        Args:
            name (str): nome do conjunto de apoios
        """
        self.name = name
        self.nodes_support = {}

    def add_support(self, node: Node, supports: list[bool | float]):
        """Adiciona um apoio

        Args:
            node (Node): nó em que estará o apoio.
            supports (list[bool | float]): (Dx, Dy, Dz, Rx, Ry, Rz)
                restrições a deslocamentos e rotações nos eixo x, y e z respectivamente.
                Pode ser fixo/livre (bool) ou uma mola (float).
        """
        if not node in self.nodes_support:
            self.nodes_support[node] = []

        self.nodes_support[node] = supports

    def add_fixed_support(self, node: Node):
        """Adiciona um apoio do tipo fixo

        Args:
            node (Node): nó em que será colocado o apoio
        """
        if not node in self.nodes_support:
            self.nodes_support[node] = []

        self.nodes_support[node] = [True, True, True, True, True, True]

    def add_pinned_support(self, node: Node):
        """Adiciona um apoio fixo, mas que permite rotações

        Args:
            node (Node): nó em ue será colocado o apoio
        """
        if not node in self.nodes_support:
            self.nodes_support[node] = []

        self.nodes_support[node] = [True, True, True, False, False, False]
    # def add_node_cantilever_roller_x(self, node: Node):
    #     if not node.name in self.nodes_support:
    #         self.nodes_support[node.name] = list()    
    #     self.nodes_support[node.name] = [False, True, True, False, False, False]
