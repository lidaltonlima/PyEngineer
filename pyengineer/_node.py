class Node:
    def __init__(self, name: str, coordinates: list[float]):
        self.name = name
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        