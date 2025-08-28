"""Módulo para carregamentos/esforços"""
from __future__ import annotations

import typing as tp

from ._node import Node

if tp.TYPE_CHECKING:
    from ._bar import Bar

class INodalLoadData(tp.TypedDict):
    """Type of loads"""
    Fx: float
    Fy: float
    Fz: float
    Mx: float
    My: float
    Mz: float

class IBarPointLoadData(tp.TypedDict):
    """Type of point loads in bars"""
    position: float
    system: tp.Literal['local', 'global']
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
        self.nodes_loads: dict[Node, dict[str, INodalLoadData]] = {}
        self.bars_loads_pt: dict[Bar, dict[str, INodalLoadData]] = {}
        self.bars_loads_dist = {}

    def add_node_load(self, name: str, node: Node,
                      fx: float = 0, fy: float = 0, fz: float = 0,
                      mx: float = 0, my: float = 0, mz: float = 0):
        """Adiciona carregamentos e esforços

        Args:
            name (str): Name of the load
            node (Node): Node where the load will be applied
            fx (float, optional): Force in "x". Defaults to 0.
            fy (float, optional): Force in "y". Defaults to 0.
            fz (float, optional): Force in "z". Defaults to 0.
            mx (float, optional): Moment in "x". Defaults to 0.
            my (float, optional): Moment in "y". Defaults to 0.
            mz (float, optional): Moment in "z". Defaults to 0.
        """

        if not node in self.nodes_loads:
            self.nodes_loads[node] = {}

        self.nodes_loads[node][name] = {'Fx': fx, 'Fy': fy, 'Fz': fz, 'Mx': mx, 'My': my, 'Mz': mz}

    def add_bar_point_load(self, name: str, bar: Bar,
                           position: float, system: tp.Literal['local', 'global'] = 'local',
                           fx: float = 0, fy: float = 0, fz: float = 0,
                           mx: float = 0, my: float = 0, mz: float = 0):
        """Adiciona carregamento pontual na barra

        Args:
            name (str): Name of the load
            bar (Bar): Bar where the load will be applied
            position (float): Position of the load in the bar
            fx (float, optional): Force in "x". Defaults to 0.
            fy (float, optional): Force in "y". Defaults to 0.
            fz (float, optional): Force in "z". Defaults to 0.
            mx (float, optional): Moment in "x". Defaults to 0.
            my (float, optional): Moment in "y". Defaults to 0.
            mz (float, optional): Moment in "z". Defaults to 0.
        """
        if not bar in self.bars_loads_pt:
            self.bars_loads_pt[bar] = {}

        self.bars_loads_pt[bar][name] = {"position": position, "system": system,
                                         'Fx': fx, 'Fy': fy, 'Fz': fz,
                                         'Mx': mx, 'My': my, 'Mz': mz}
