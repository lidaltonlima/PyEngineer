class Section:
    def __init__(self, name: str, area: float, inertias: list[float]):
        self.name = name
        self.area = area
        self.ix = inertias[0]
        self.iy = inertias[1]
        self.iz = inertias[2]