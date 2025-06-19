"""Funções úteis para para manipulação de objetos no espaço tridimensional"""
import numpy as np

def rotate_point_around_line(point_p: list[float] | np.ndarray,
                             point_a: list[float] | np.ndarray,
                             point_b: list[float] | np.ndarray,
                             angle: float) -> np.ndarray:
    """Rotaciona um ponto "p" em torno de uma reta definida pelos pontos "a" e "b"

    Args:
        point_p (list[float] | np.ndarray): (x, y, z) Ponto a ser rotacionado
        point_a (list[float] | np.ndarray): (x, y, z) Ponto da reta
        point_b (list[float] | np.ndarray): (x, y, z) Ponto da reta
        angle (float): ângulo de rotação em radianos

    Returns:
        np.ndarray: novas coordenadas do ponto "p"
    """
    point_p = np.array(point_p, dtype=float)
    point_a = np.array(point_a, dtype=float)
    point_b = np.array(point_b, dtype=float)

    # Vetor unitário da direção da reta (eixo de rotação)
    u = point_b - point_a
    u = u / np.linalg.norm(u)

    # Translada para a origem (reta passa pela origem)
    p_relative = point_p - point_a

    # Fórmula de Rodrigues para rotação em torno de um eixo arbitrário
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    cross = np.cross(u, p_relative)
    dot = np.dot(u, p_relative)
    rotated = (p_relative * cos_theta +
               cross * sin_theta +
               u * dot * (1 - cos_theta))

    # Translada de volta
    return rotated + point_a
