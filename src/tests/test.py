from typing import Tuple

def reacoes_biengastada_torcao(L: float, x1: float, m1: float, x2: float, m2: float) -> Tuple[float, float]:
    """
    Calcula as reações de torção (momentos torsores) em uma barra biengastada
    submetida a um momento distribuído trapezoidal ao longo do eixo x local.

    Parâmetros
    ----------
    L : float
        Comprimento total da barra (>0)
    x1, x2 : float
        Posições do início e fim do trecho carregado (0 <= x1 < x2 <= L)
    m1, m2 : float
        Intensidades do momento distribuído no início e no fim (N·m/m)

    Retorno
    -------
    (MA, MB) : tuple[float, float]
        Reações de torção nos apoios A (x=0) e B (x=L), em N·m.
    """
    if not (0 <= x1 < x2 <= L):
        raise ValueError("Exige 0 <= x1 < x2 <= L.")

    dx = x2 - x1
    # resultante do carregamento torsor (N·m)
    Mres = 0.5 * (m1 + m2) * dx
    if abs(Mres) < 1e-14:
        return 0.0, 0.0

    # posição do centroide (m)
    xbar = x1 + dx/3 * (2*m1 + m2) / (m1 + m2)

    # reações de torção
    MA = -Mres * (L - xbar) / L
    MB = -Mres * xbar / L

    return MA, MB


L = 5.0
x1, m1 = 0.5, 1e3   # início da carga de torção (N·m/m)
x2, m2 = 2.5, 3e3   # fim da carga

MA, MB = reacoes_biengastada_torcao(L, x1, m1, x2, m2)
print("Reação torsora no apoio A:", MA)
print("Reação torsora no apoio B:", MB)
