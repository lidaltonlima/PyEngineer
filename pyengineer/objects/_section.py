"""Módulo para criar seções que serão usadas na estrutura"""

class Section:
    """Seções que serão usadas na estrutura"""
    def __init__(self, name: str, area: float, inertias: list[float]):
        """Construtor

        Args:
            name (str): Nome da seção
            area (float): Área da seção
            inertias (list[float]): Inércias em x, y e z (Ix, Iy, Iz)
        """
        self.name = name
        self.area = area
        self.ix = inertias[0]
        self.iy = inertias[1]
        self.iz = inertias[2]
