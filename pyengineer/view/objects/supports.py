"""Module for support objects"""
from typing import Literal
import numpy as np
import pyvista as pv

def map2plane(points: np.ndarray, axis: Literal['x', 'y', 'z']) -> np.ndarray | None:
    """Coloca os pontos um dos planos principais:
    x == xy, y == yz, z == xz

    Args:
        points (np.ndarray): Pontos a serem transformados
        axis (Literal[&#39;x&#39;, &#39;y&#39;, &#39;z&#39;]): Eixo

    Returns:
        np.ndarray | None: Pontos transformados
    """
    match axis:
        case 'x':
            return points
        case 'z':
            return points[:, [0, 2, 1]] # Muda as colunas de lugar
        case 'y':
            return points[:, [2, 0, 1]]
    return None


def rotate_points(points: np.ndarray, axis: Literal['x', 'y', 'z'], rotation: float) -> np.ndarray:
    """Rotaciona os pontos em um plano.

    Args:
        points (np.ndarray): Pontos a serem rotacionados
        axis (Literal[&#39;x&#39;, &#39;y&#39;, &#39;z&#39;]): Eixo
        rotation (float): Ângulo de rotação em radianos

    Returns:
        np.ndarray: Pontos rotacionados
    """
    perpendicular_axis = {'x': 2, 'z': 1, 'y': 0}
    pts_rot = points.copy()
    for index, point in enumerate(pts_rot):
        # Componentes do plano
        v1 = (perpendicular_axis[axis] + 1) % 3
        v2 = (perpendicular_axis[axis] + 2) % 3
        x, y = point[v1], point[v2]
        # Rotaciona 2D
        x_new = np.cos(rotation)*x - np.sin(rotation)*y
        y_new = np.sin(rotation)*x + np.cos(rotation)*y
        pts_rot[index, v1] = x_new
        pts_rot[index, v2] = y_new
    return pts_rot


def fixed_displacement(plotter: pv.Plotter,
                       base_point: list[float] | np.ndarray,
                       axis: Literal['x', 'y', 'z'],
                       size: float = 1.0) -> None:
    """Desenha um apoio fixo no eixo

    Args:
        plotter (pv.Plotter): Plotter em que o desenho será inserido
        base_point (list[float] | np.ndarray): Ponto do apoio
        axis (Literal[&#39;x&#39;, &#39;y&#39;, &#39;z&#39;]): Eixo
        size (float, optional): Tamanho. Defaults to 1.0.
    """
    if not(axis == 'x' or axis == 'y' or axis == 'z'):
        raise ValueError("O eixo deve ser 'x', 'y' ou 'z'.")

    half = size / 2
    height = size * np.sqrt(3) / 2

    # Rotação para fica apontando para o sentido positivo
    match axis:
        case 'x':
            rotation = np.deg2rad(-90)
        case 'y':
            rotation = np.deg2rad(-90)
        case 'z':
            rotation = 0

    # Triângulo equilátero no plano XY com base centrada na origem e vértice oposto em cima
    points_xy = np.array([
        [-half, -height/3, 0],  # canto esquerdo da base
        [half, -height/3, 0],   # canto direito da base
        [0, 2*height/3, 0],     # vértice oposto (topo)
        [-half, -height/3, 0]   # fecha o triângulo
    ], dtype=float)

    # Linha "chão"
    base = size * 0.3  # 30% maior que a base
    base_line_xy = np.array([
        [-half - base/2, -height/3 - 0.1, 0],  # um pouco abaixo da base
        [half + base/2, -height/3 - 0.1, 0]
    ], dtype=float)

    tri_pts = map2plane(points_xy, axis)
    base_line_pts = map2plane(base_line_xy, axis)

    # Colocar o ponto base na origem (vértice superior)
    pivot = tri_pts[2].copy()  # vértice oposto à base
    tri_pts -= pivot
    base_line_pts -= pivot



    tri_pts = rotate_points(tri_pts, axis, rotation)
    base_line_pts = rotate_points(base_line_pts, axis, rotation)

    # Agora volta para a posição base_point
    tri_pts += np.array(base_point, dtype=float)
    base_line_pts += np.array(base_point, dtype=float)

    # Desenhos
    match axis:
        case 'x':
            color = 'red'
        case 'y':
            color = 'green'
        case 'z':
            color = 'blue'

    tri_lines = pv.lines_from_points(tri_pts, close=False)
    plotter.add_mesh(tri_lines, color=color, line_width=2)

    base_line = pv.lines_from_points(base_line_pts, close=False)
    plotter.add_mesh(base_line, color=color, line_width=2)


def fixed_rotation(plotter: pv.Plotter,
                   base_point: list[float] | np.ndarray,
                   axis: Literal['x',  'y', 'z'],
                   size: float = 0.5) -> None:
    """Desenha um apoio tipo "rotação fixa" no eixo.

    Args:
        plotter (pv.Plotter): Plotter em que será desenhado
        base_point (list[float] | np.ndarray): Ponto base
        axis (Literal[&#39;x&#39;,  &#39;y&#39;, &#39;z&#39;]): Eixo
        size (float, optional): Tamanho do desenho. Defaults to 0.3.

    Raises:
        ValueError: Se o valor para 'axis' for diferente de 'x', 'y' ou 'z'.

    Returns:
        None: Sem retorno
    """
    if not('x' in axis or 'y' in axis or 'z' in axis):
        raise ValueError("O eixo deve ser 'x', 'y' ou 'z'.")

    points_line = np.array([[0.0, 0.0, 0.0],
                            [2*size, 0.0, 0.0]], dtype=float)

    points_square = np.array([[2*size, size, size],
                              [2*size, -size, size],
                              [2*size, -size, -size],
                              [2*size, size, -size]], dtype=float)

    # Desenho para fica apontando para o sentido positivo
    match axis:
        case 'x':
            rotation = 0
        case 'y':
            rotation = 0
        case 'z':
            rotation = np.deg2rad(-90)

    points_line = rotate_points(map2plane(points_line, axis), axis, rotation)
    points_line += np.array(base_point, dtype=float)
    points_square = rotate_points(map2plane(points_square, axis), axis, rotation)
    points_square += np.array(base_point, dtype=float)

    # Color
    match axis:
        case 'x':
            color = 'red'
        case 'y':
            color = 'green'
        case 'z':
            color = 'blue'

    lines_line = pv.lines_from_points(points_line, close=False)
    plotter.add_mesh(lines_line, color=color, line_width=2)

    lines_square = pv.lines_from_points(points_square, close=True)
    plotter.add_mesh(lines_square, color=color, line_width=2)


def spring_displacement(plotter: pv.Plotter,
                        base_point: list[float] | np.ndarray,
                        axis: Literal['x',  'y', 'z'],
                        size: float = 0.3) -> None:
    """Desenha um apoio tipo "mola" no eixo.

    Args:
        plotter (pv.Plotter): Plotter em que será desenhado
        base_point (list[float] | np.ndarray): Ponto base
        axis (Literal[&#39;x&#39;,  &#39;y&#39;, &#39;z&#39;]): Eixo
        size (float, optional): Tamanho do desenho. Defaults to 0.3.

    Raises:
        ValueError: Se o valor para 'axis' for diferente de 'x', 'y' ou 'z'.

    Returns:
        None: Sem retorno
    """
    if not('x' in axis or 'y' in axis or 'z' in axis):
        raise ValueError("O eixo deve ser 'x', 'y' ou 'z'.")

    points_base = np.array([[0.0, 0.0, 0.0],
                            [size, size, 0.0],
                            [2*size, -size, 0.0],
                            [3*size, size, 0.0],
                            [4*size, -size, 0.0],
                            [5*size, size, 0.0],
                            [6*size, -size, 0.0],
                            [7*size, 0.0, 0.0],
                            [7*size, 2*size, 0.0],
                            [7*size, -2*size, 0.0]], dtype=float)

    # Desenho para fica apontando para o sentido positivo
    match axis:
        case 'x':
            rotation = np.deg2rad(180)
        case 'y':
            rotation = np.deg2rad(180)
        case 'z':
            rotation = np.deg2rad(90)

    points = rotate_points(map2plane(points_base, axis), axis, rotation)
    points += np.array(base_point, dtype=float)

    # Color
    match axis:
        case 'x':
            color = 'red'
        case 'y':
            color = 'green'
        case 'z':
            color = 'blue'

    lines_line = pv.lines_from_points(points, close=False)
    plotter.add_mesh(lines_line, color=color, line_width=2)


def spring_rotation(plotter: pv.Plotter,
                    base_point: list[float] | np.ndarray,
                    axis: Literal['x',  'y', 'z'],
                    size: float = 1) -> None:
    """Desenha um apoio tipo "mola" no eixo.

    Args:
        plotter (pv.Plotter): Plotter em que será desenhado
        base_point (list[float] | np.ndarray): Ponto base
        axis (Literal[&#39;x&#39;,  &#39;y&#39;, &#39;z&#39;]): Eixo
        size (float, optional): Tamanho do desenho. Defaults to 0.3.

    Raises:
        ValueError: Se o valor para 'axis' for diferente de 'x', 'y' ou 'z'.

    Returns:
        None: Sem retorno
    """
    if not('x' in axis or 'y' in axis or 'z' in axis):
        raise ValueError("O eixo deve ser 'x', 'y' ou 'z'.")

    # Points of line
    points_line_base = np.array([[0, 0, 0], [size, 0, 0]], dtype=float)

    # Parâmetros da espiral
    points_number = 100 # Número de pontos para suavizar a curva
    initial_radius = 0.0001
    end_radius = size
    laps_number = 3 # Número de voltas

    # Criar os ângulos da espiral
    theta = np.linspace(0, 2 * np.pi * laps_number, points_number)
    raio = np.linspace(initial_radius, end_radius, points_number)

    # Coordenadas no plano YZ
    x = np.zeros(points_number) + size # Espiral plana no YZ afastada 'size' unidades
    y = raio * np.cos(theta)
    z = raio * np.sin(theta)

    # Criar os pontos da espiral
    points_spiral_base = np.column_stack((x, y, z))

    # Desenho para fica apontando para o sentido positivo
    match axis:
        case 'x':
            rotation = 0
        case 'y':
            rotation = 0
        case 'z':
            rotation = np.deg2rad(-90)

    points_spiral = rotate_points(map2plane(points_spiral_base, axis), axis, rotation)
    points_spiral += np.array(base_point, dtype=float)

    points_line = rotate_points(map2plane(points_line_base, axis), axis, rotation)
    points_line += np.array(base_point, dtype=float)

    # Color
    match axis:
        case 'x':
            color = 'red'
        case 'y':
            color = 'green'
        case 'z':
            color = 'blue'

    lines_spiral = pv.lines_from_points(points_spiral)
    plotter.add_mesh(lines_spiral, color=color, line_width=2)

    lines_line = pv.lines_from_points(points_line)
    plotter.add_mesh(lines_line, color=color, line_width=2)
