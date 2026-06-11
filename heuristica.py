"""
Codificação:
  permutação de comprimento n
  s[i] = j  →  aluno A_(i+1) pareado com aluno B_(j+1)
  Exemplo (n=4): [2, 0, 3, 1] → A1-B3, A2-B1, A3-B4, A4-B2

Aptidão: maior valor significa amelhor solução
  Intervalo: [0, 2·N·(N−1)]
"""

import random
from itertools import permutations as _permutations


def codificar(n):
    s = list(range(n))
    random.shuffle(s)
    return s


def decodificar(s):
    _s = []
    for i, j in enumerate(s):
      _s.append(f"A{i + 1}-B{j + 1}")

    return _s


def custo(s, escola_a, escola_b):
    """
    Soma total das posições de preferência de todos os pares.
    Intervalo: [2·N, 2·N²] — menor custo = melhor solução.
    """
    total = 0
    for i, j in enumerate(s):
        total += escola_a[i][j] + escola_b[j][i]
    return total


def aptidao(s, escola_a, escola_b):
    """
    Aptidão para o Algoritmo Genético: maior valor = melhor.
    Fórmula: 2·N² − custo_total
    """
    n = len(s)
    return 2 * n * n - custo(s, escola_a, escola_b)


def aptidao_normalizada(s, escola_a, escola_b):
    """Aptidão em [0, 1], comparável entre instâncias de N diferentes."""
    n = len(s)
    if n <= 1:
        return 1.0
    return aptidao(s, escola_a, escola_b) / (2 * n * (n - 1))


def melhor_solucao_forca_bruta(n, escola_a, escola_b):
    """
    Encontra a melhor solução por enumeração completa.
    Retorna (solucao, aptidao). Use apenas para N ≤ 8.
    """
    melhor, melhor_apt = None, -1
    for perm in _permutations(range(n)):
        s = list(perm)
        apt = aptidao(s, escola_a, escola_b)
        if apt > melhor_apt:
            melhor_apt = apt
            melhor = s
    return melhor, melhor_apt


if __name__ == "__main__":
    import sys
    from leitor import ler_arquivo

    caminho = sys.argv[1] if len(sys.argv) > 1 else "preferencias.txt"

    try:
        n, escola_a, escola_b = ler_arquivo(caminho)
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' nao encontrado.")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro no formato do arquivo: {e}")
        sys.exit(1)

    print(f"[------ Heuristica: N -> {n} ------]\n")

    def _print(label, s):
        print(f"{label}")
        print(f"  Codificada:      {s}")
        print(f"  Decodificada:    {decodificar(s)}")
        print(f"  Custo:           {custo(s, escola_a, escola_b)}")
        print(f"  Aptidao:         {aptidao(s, escola_a, escola_b)}")
        print(f"  Aptidao normalizada:   {aptidao_normalizada(s, escola_a, escola_b):.4f}")

    _print("Solução identidade (0, ..., n-1):", list(range(n)))
    print()

    random.seed(20)
    _print("Solucao (pseudo)aleatoria (seed=20):", codificar(n))
    print()

    if n <= 8:
        s_ot, apt_ot = melhor_solucao_forca_bruta(n, escola_a, escola_b)
        _print("Melhor solucao (forca bruta):", s_ot)
    else:
        print(f"n -> {n}: forca bruta omitida (muito grande).")
