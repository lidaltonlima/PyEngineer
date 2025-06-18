"""Nós da estrutura"""
class Node:
    """Cria um nó que será usado na estrutura
    Observações:
        - Todos nós devem esta associados a uma barra;
        - Não pode haver nós soltos;
        - Um único nó pode ser usado para vários elementos
    """
    def __init__(self, name: str, coordinates: list[float]):
        """Construtor

        Args:
            name (str): nome para pegar dados do nó
            coordinates (list[float]): coordenada do nó
        """
        self.name = name
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
