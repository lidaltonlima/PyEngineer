"""Nós da estrutura"""
class Node:
    """Cria um nó que será usado na estrutura
    Observações:
        - Todos nós devem esta associados a uma barra;
        - Não pode haver nós soltos;
        - Um único nó pode ser usado para vários elementos
    """
    def __init__(self, name: str, position: list[float]):
        """Construtor

        Args:
            name (str): nome para pegar dados do nó.
            coordinates (list[float]): (x, y, z) coordenada do nó.
        """
        self.name = name
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
