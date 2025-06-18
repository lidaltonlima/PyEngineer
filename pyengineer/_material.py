"""Módulo para materiais que serão usados na estrutura"""
class Material:
    """Cria um material"""
    def __init__(self, name: str, e: float, g: float, ni: float, rho: float):
        """Construtor

        Args:
            name (str): nome do material
            e (float): módulo de elasticidade
            g (float): módulo de elasticidade transversal
            ni (float): coeficiente de Poisson
            rho (float): massa específica
        """
        self.name = name
        self.e = e
        self.g = g
        self.ni = ni
        self.rho = rho
