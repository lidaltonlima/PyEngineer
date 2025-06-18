"""Módulo para carregamentos/esforços"""
from ._node import Node

class Load:
    """Casos de carga que serão usadas na estrutura"""
    def __init__(self, name: str):
        """Construtor

        Args:
            name (str): nome da carga
        """
        self.name = name
        self.nodes_loads = {}
        self.bars_loads_pt = {}
        self.bars_loads_dist = {}

    def add_node_load(self, name: str, node: Node,
                      fx: float = 0, fy: float = 0, fz: float = 0,
                      mx: float = 0, my: float = 0, mz: float = 0):
        """Adiciona carregamentos e esforços

        Args:
            name (str): _description_
            node (Node): _description_
            fx (float, optional): _description_. Defaults to 0.
            fy (float, optional): _description_. Defaults to 0.
            fz (float, optional): _description_. Defaults to 0.
            mx (float, optional): _description_. Defaults to 0.
            my (float, optional): _description_. Defaults to 0.
            mz (float, optional): _description_. Defaults to 0.
        """

        if not node in self.nodes_loads:
            self.nodes_loads[node] = {}

        self.nodes_loads[node][name] = [fx, fy, fz, mx, my, mz]

    # def add_bar_load_pt(self, name: str, bar: Bar, position: float,
    #                        fx: float = 0, fy: float = 0, fz: float = 0,
    #                        mx: float = 0, my: float = 0, mz: float = 0,
    #                        local_reference: bool = False):

    #     if not bar.name in self.bars_loads_pt:
    #         self.bars_loads_pt[bar.name] = dict()

    #     self.bars_loads_pt[bar.name][name] = {'position': position,
    #                                       'forces': [fx, fy, fz, mx, my, mz],
    #                                       'local_reference': local_reference}

    # def add_bar_load_dist(self, name: str, bar: Bar,
    #                       start_position: float, end_position: float,
    #                       start_forces: list = [0, 0, 0, 0, 0, 0],
    #                       end_forces: list = [0, 0, 0, 0, 0, 0],
    #                       local_reference: bool = False):

    #     if not bar.name in self.bars_loads_dist:
    #             self.bars_loads_dist[bar.name] = dict()

    #     self.bars_loads_dist[bar.name][name] = {'start_position': start_position,
    #                                             'end_position': end_position,
    #                                             'start_forces': start_forces,
    #                                             'end_forces': end_forces,
    #                                             'local_reference': local_reference}
