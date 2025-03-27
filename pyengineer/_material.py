class Material:
    def __init__(self, name: str, e: float, g: float, ni: float, rho: float):
        self.name = name
        self.e = e
        self.g = g
        self.ni = ni
        self.rho = rho