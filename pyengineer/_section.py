"""Módulo para criar seções que serão usadas na estrutura"""

class Section:
    """Seções que serão usadas na estrutura"""
    def __init__(self, name: str, area: float, inertias: list[float]):
        """Construtor

        Args:
            name (str): nome da seção
            area (float): área da seção
            inertias (list[float]): inércias em x, y e z
        """
        self.name = name
        self.area = area
        self.ix = inertias[0]
        self.iy = inertias[1]
        self.iz = inertias[2]
