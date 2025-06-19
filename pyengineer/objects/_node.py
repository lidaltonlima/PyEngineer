"""Nós da estrutura"""
import numpy as np

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
        self.position = np.array(position, dtype=float)
        self.x = float(position[0])
        self.y = float(position[1])
        self.z = float(position[2])
