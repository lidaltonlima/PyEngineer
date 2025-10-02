"""Módulo para criar seções que serão usadas na estrutura"""
from typing import TypedDict

class ISectionProperties(TypedDict):
    """Typing for section properties"""
    area: float
    Ix: float
    Iy: float
    Iz: float

class Section:
    """Seções que serão usadas na estrutura"""
    def __init__(self,
                 name: str,
                 area: float,
                 ix: float, iy: float, iz: float):
        """Seção

        Args:
            name (str): Section name
            area (float): Section area
            ix (float): Inertia in 'x' of the section
            iy (float): Inertia in 'y' of the section
            iz (float): Inertia in 'z' of the section
        """
        self.name = name
        self.properties: ISectionProperties = {'area': area, 'Ix': ix, 'Iy': iy, 'Iz': iz}
