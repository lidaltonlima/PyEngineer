"""Add rotule"""
import numpy as np

np.set_printoptions(formatter={'float_kind': '{: .4e}'.format}, linewidth=200)

# Matriz de ações
a = np.array([0, 5, 750, 0, 5, -750])
a_linha = np.zeros(6)

# Matriz de rigidez
s = np.zeros([6, 6])
s[0, 0] = 42e3
s[0, 3] = -42e3
s[1, 1] = 105
s[1, 2] = 31500
s[1, 4] = -105
s[1, 5] = 31500
s[2, 2] = 12.6e6
s[2, 4] = -31500
s[2, 5] = 6.3e6
s[3, 3] = 42e3
s[4, 4] = 105
s[4, 5] = -31500
s[5, 5] = 12.6e6
s = s + s.T - np.diag(s.diagonal())
s_linha = np.zeros([6, 6])

# Calculate rotule
releases: list[int] = [2, 5]
releases_calculates: list[int] = []
for release in releases:
    for j in range(6):
        if j in releases_calculates:
            continue
        s_barra = s[j, release] / s[release, release]

        for k in range(6):
            if k in releases_calculates:
                continue
            s_linha[j, k] = s[j, k] - s_barra * s[release, k]

        a_linha[j] = a[j] - s_barra * a[release]

    for k in range(6):
        s[release, k] = 0

    a[release] = 0

    a = a_linha
    s = s_linha
    releases_calculates.append(release)

print(s)
