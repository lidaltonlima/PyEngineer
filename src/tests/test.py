import pyvista as pv
import numpy as np

def desenhar_triangulo_com_base(plotter, base_point=(0,0,0), size=1.0, color='red', plano='xy', rot_deg=0):
    half = size / 2
    height = size * np.sqrt(3) / 2

    # Triângulo equilátero no plano XY com base centrada na origem e vértice oposto em cima
    points_xy = np.array([
        [-half, -height/3, 0],  # canto esquerdo da base
        [half, -height/3, 0],   # canto direito da base
        [0, 2*height/3, 0],     # vértice oposto (topo)
        [-half, -height/3, 0]   # fecha o triângulo
    ])

    # Linha "chão": ligeiramente maior que a base
    base_extra = size * 0.2  # 20% maior que a base
    base_line_xy = np.array([
        [-half - base_extra/2, -height/3 - 0.05, 0],  # um pouco abaixo da base
        [half + base_extra/2, -height/3 - 0.05, 0]
    ])

    # Escolhe e reorganiza pontos para o plano correto
    def map_to_plane(points):
        if plano == 'xy':
            return points
        elif plano == 'xz':
            return points[:, [0, 2, 1]]
        elif plano == 'yz':
            return points[:, [2, 0, 1]]
        else:
            raise ValueError("Plano deve ser 'xy', 'xz' ou 'yz'.")

    tri_pts = map_to_plane(points_xy)
    base_line_pts = map_to_plane(base_line_xy)

    # O ponto base é o vértice oposto à base (no nosso pts_xy é o 3º ponto - índice 2)
    # Ajustamos triângulo para que esse ponto fique na origem (0,0,0) para rotacionar em torno dele
    pivot = tri_pts[2].copy()  # vértice oposto à base
    tri_pts -= pivot
    base_line_pts -= pivot

    # Rotaciona os pontos em torno do eixo perpendicular ao plano, usando ângulo em graus
    theta = np.radians(rot_deg)
    c, s = np.cos(theta), np.sin(theta)

    # Matriz rotação 2D no plano XY (no plano escolhido, o eixo perpendicular é o eixo “não usado”)
    # Identificamos qual é o eixo que fica fixo (perpendicular)
    axes = {'xy': 2, 'xz': 1, 'yz': 0}
    perp_axis = axes[plano]

    def rotacionar_pontos(pontos):
        pts_rot = pontos.copy()
        for i, _j in enumerate(pts_rot):
            p = pts_rot[i]
            # Componentes do plano
            v1 = (perp_axis + 1) % 3
            v2 = (perp_axis + 2) % 3
            x, y = p[v1], p[v2]
            # Rotaciona 2D
            x_new = c*x - s*y
            y_new = s*x + c*y
            pts_rot[i, v1] = x_new
            pts_rot[i, v2] = y_new
        return pts_rot

    tri_pts = rotacionar_pontos(tri_pts)
    base_line_pts = rotacionar_pontos(base_line_pts)

    # Agora volta para a posição base_point
    tri_pts += np.array(base_point)
    base_line_pts += np.array(base_point)

    # Desenha triângulo
    tri_lines = pv.lines_from_points(tri_pts, close=False)
    plotter.add_mesh(tri_lines, color=color, line_width=2)

    # Desenha linha "chão"
    base_line = pv.lines_from_points(base_line_pts, close=False)
    plotter.add_mesh(base_line, color=color, line_width=3, opacity=0.5)

# Exemplo de uso:
plotter = pv.Plotter()
plotter.add_axes()

# Define a coordenada do ponto
ponto = [[0, 0, 0]]  # formato de lista de listas
nuvem_de_pontos = pv.PolyData(ponto)
plotter.add_mesh(nuvem_de_pontos, color='blue', point_size=15)

# Triângulo no plano XY, base_point no vértice oposto (0,0,0), rotacionado 30 graus
desenhar_triangulo_com_base(plotter, base_point=(-0.5,0,0), size=1, color='red', plano='xy', rot_deg=-90)
desenhar_triangulo_com_base(plotter, base_point=(0,0,0), size=1, color='blue', plano='xz', rot_deg=0)
desenhar_triangulo_com_base(plotter, base_point=(0,0,0), size=1, color='green', plano='yz', rot_deg=90)


plotter.show()
