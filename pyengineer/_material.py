"""Módulo para materiais que serão usados na estrutura"""
class Material:
    """Cria um material"""
    def __init__(self, name: str, e: float, g: float, ni: float, rho: float):
        """Construtor

        Args:
            name (str): Nome do material
            e (float): Módulo de elasticidade
            g (float): Módulo de elasticidade transversal
            ni (float): Coeficiente de Poisson
            rho (float): Massa específica
        """
        self.name = name
        self.e = e
        self.g = g
        self.ni = ni
        self.rho = rho
