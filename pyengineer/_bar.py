"""Módulo para operações matemáticas"""
from numpy import sqrt

from ._material import Material
from ._node import Node
from ._section import Section

class Bar:
    """Cria uma barra para ser usada na estrutura"""
    def __init__(self,
                 name: str,
                 start_node: Node,
                 end_node: Node,
                 section: Section,
                 material: Material):
        """Construtor

        Args:
            name (str): nome da barra
            start_node (Node): nó inicial (i)
            end_node (Node): nó final (j)
            section (Section): seção
            material (Material): material
        """
        self.name = name
        self.start_node = start_node
        self.end_node = end_node
        self.dx = end_node.x - start_node.x
        self.dy = end_node.y - start_node.y
        self.dz = end_node.z - start_node.z
        self.length = sqrt(self.dx**2 + self.dy**2 + self.dz**2)
        self.section = section
        self.material = material
        self.klg = None
        self.kl = None
        self.r = None
