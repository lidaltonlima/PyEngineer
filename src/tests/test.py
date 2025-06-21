import numpy as np
import pyvista as pv
from scipy.spatial.transform import Rotation as R

def desenhar_momento_fletor_vetorial(
    centro=(0, 0, 0),
    raio=1.0,
    eixo=(0, 0, 1),
    sentido="positivo",  # 'positivo' = regra da mão direita
    valor=None,  # valor numérico exibido no "pé" do momento
    cor_linha="blue",
    cor_seta="red",
    cor_texto="black",
    escala_seta=0.2,
    n_pontos=100,
    plotter=None
):
    """
    Desenha um momento fletor como um arco semicircular com uma seta, usando PyVista,
    com base em um vetor eixo qualquer.

    Parâmetros:
        centro (tuple): Centro do arco (x, y, z).
        raio (float): Raio do arco.
        eixo (tuple): Vetor que define a direção do momento (eixo de rotação).
        sentido (str): 'positivo' ou 'negativo', segundo a regra da mão direita.
        valor (float | str): Valor do momento a ser exibido no pé do arco.
        cor_linha (str): Cor do arco.
        cor_seta (str): Cor da seta.
        cor_texto (str): Cor do texto do valor.
        escala_seta (float): Escala da seta.
        n_pontos (int): Número de pontos do arco.
        plotter (pv.Plotter): Um plotter opcional.
    
    Retorno:
        pv.Plotter: Plotter com o momento desenhado.
    """
    centro = np.array(centro, dtype=float)
    eixo = np.array(eixo, dtype=float)
    norm = np.linalg.norm(eixo)
    if norm == 0:
        raise ValueError("O vetor do eixo não pode ser nulo.")
    eixo_unit = eixo / norm

    # Geração dos ângulos para o arco
    if sentido == "positivo":
        theta = np.linspace(0, np.pi, n_pontos)
    else:
        theta = np.linspace(0, -np.pi, n_pontos)

    # Criar um arco no plano XY
    x = raio * np.cos(theta)
    y = raio * np.sin(theta)
    z = np.zeros_like(x)
    arco_local = np.vstack((x, y, z)).T

    # Rotacionar o arco para o plano definido pelo eixo
    r = R.align_vectors([eixo_unit], [[0, 0, 1]])[0]
    arco_rotacionado = r.apply(arco_local)

    # Transladar para o centro
    arco_final = arco_rotacionado + centro

    # Criar curva e seta
    arco_spline = pv.Spline(arco_final, n_points=len(arco_final))
    ponta = arco_final[-1]
    anterior = arco_final[-2]
    direcao = ponta - anterior
    direcao /= np.linalg.norm(direcao)
    seta = pv.Arrow(start=ponta - direcao * escala_seta * 0.5, direction=direcao, scale=escala_seta)

    # Criar ou usar plotter
    if plotter is None:
        plotter = pv.Plotter()
        externo = True
    else:
        externo = False

    plotter.add_mesh(arco_spline, color=cor_linha, line_width=3)
    plotter.add_mesh(seta, color=cor_seta)

    # Adicionar valor (texto) no pé do arco (início da curva)
    if valor is not None:
        texto_pos = arco_final[0] - 0.1 * raio * eixo_unit  # deslocar um pouco na direção oposta ao eixo
        plotter.add_point_labels([texto_pos], [str(valor)], font_size=14, text_color=cor_texto, point_color=None, shape_opacity=0)

    if externo:
        plotter.show_axes()
        plotter.show()

    return plotter

desenhar_momento_fletor_vetorial(
    centro=(0, 0, 0),
    eixo=(0, 0, 1),
    sentido='positivo',
    valor="120 kNm"
)
