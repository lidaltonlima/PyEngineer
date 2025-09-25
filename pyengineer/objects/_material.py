"""Módulo para materiais que serão usados na estrutura"""
import typing as tp

class IMaterialProperties(tp.TypedDict):
    """Typing for properties attribute"""
    E: float
    G: float
    nu: float
    rho: float

class Material:
    """Cria um material"""
    def __init__(self, name: str, e: float, g: float, nu: float, rho: float):
        """Construtor

        Args:
            name (str): Nome do material
            e (float): Módulo de elasticidade
            g (float): Módulo de elasticidade transversal
            ni (float): Coeficiente de Poisson
            rho (float): Massa específica
        """
        self.name = name
        self.properties: IMaterialProperties = {'E': e, 'G': g, 'nu': nu, 'rho': rho}
