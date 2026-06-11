"""
Testes do nucleo do AG (Pessoa 3).

Cobre:
  - geracao da populacao inicial (tamanho e validade das permutacoes)
  - selecao por torneio e por roleta
  - cruzamento OX (validade e preservacao do segmento do pai)
  - ciclo do AG: nao piora (elitismo) e converge ao otimo em N pequeno
  - robustez para N=1, N=2 e N grande

Execucao:
  python test_nucleo_ag.py
Sai com codigo 0 se tudo passar, 1 caso contrario.
"""

import random

from leitor import ler_arquivo
from heuristica import aptidao, melhor_solucao_forca_bruta
import nucleo_ag as ag


_falhas = []


def checa(condicao, descricao):
    status = "OK  " if condicao else "FALHA"
    print(f"  [{status}] {descricao}")
    if not condicao:
        _falhas.append(descricao)


def eh_permutacao(s, n):
    return sorted(s) == list(range(n))


# ---------------------------------------------------------------------------

def teste_populacao():
    print("teste_populacao")
    random.seed(1)
    n, tam = 5, 30
    pop = ag.gerar_populacao(n, tam)
    checa(len(pop) == tam, "populacao tem o tamanho pedido")
    checa(all(eh_permutacao(ind, n) for ind in pop),
          "todo individuo e permutacao valida de tamanho N")

    erro = False
    try:
        ag.gerar_populacao(n, 0)
    except ValueError:
        erro = True
    checa(erro, "tamanho_populacao invalido (0) levanta ValueError")


def teste_selecao_torneio():
    print("teste_selecao_torneio")
    random.seed(2)
    populacao = [[0, 1, 2], [2, 1, 0], [1, 0, 2]]
    aptidoes = [1, 99, 5]  # indice 1 e claramente o melhor
    # Com k = tamanho da populacao, o torneio sempre devolve o melhor.
    vencedores = [ag.selecao_torneio(populacao, aptidoes, k=3) for _ in range(20)]
    checa(all(v == [2, 1, 0] for v in vencedores),
          "torneio com k=N sempre escolhe o de maior aptidao")
    um = ag.selecao_torneio(populacao, aptidoes, k=1)
    checa(um in populacao, "torneio com k=1 devolve individuo da populacao")


def teste_selecao_roleta():
    print("teste_selecao_roleta")
    random.seed(3)
    populacao = [[0, 1], [1, 0]]
    # aptidoes degeneradas (soma 0) -> escolha uniforme, sem erro
    escolhido = ag.selecao_roleta(populacao, [0, 0])
    checa(escolhido in populacao, "roleta com soma 0 nao quebra e devolve valido")
    # com peso quase todo no indice 1, deve sair muito mais o segundo
    cont = {0: 0, 1: 0}
    for _ in range(2000):
        e = ag.selecao_roleta(populacao, [1, 99])
        cont[populacao.index(e)] += 1
    checa(cont[1] > cont[0], "roleta favorece o individuo de maior aptidao")


def teste_crossover_ox():
    print("teste_crossover_ox")
    random.seed(4)
    n = 8
    for _ in range(200):
        p1 = list(range(n)); random.shuffle(p1)
        p2 = list(range(n)); random.shuffle(p2)
        filho = ag.crossover_ox(p1, p2)
        if not eh_permutacao(filho, n):
            checa(False, "OX gera permutacao valida")
            break
    else:
        checa(True, "OX gera permutacao valida (200 amostras)")

    # N == 1 deve devolver copia do pai
    checa(ag.crossover_ox([0], [0]) == [0], "OX trata N=1 sem erro")

    # tamanhos diferentes -> erro
    erro = False
    try:
        ag.crossover_ox([0, 1], [0, 1, 2])
    except ValueError:
        erro = True
    checa(erro, "OX com pais de tamanhos diferentes levanta ValueError")


def teste_ciclo_nao_piora():
    print("teste_ciclo_nao_piora (elitismo)")
    n, escola_a, escola_b = ler_arquivo("preferencias.txt")
    _, _, hist = ag.algoritmo_genetico(
        n, escola_a, escola_b, num_geracoes=100, semente=7
    )
    nao_piora = all(hist[i] <= hist[i + 1] for i in range(len(hist) - 1))
    checa(nao_piora, "historico de aptidao e monotonico nao-decrescente")


def teste_convergencia():
    print("teste_convergencia (vs forca bruta)")
    for arquivo in ["preferencias.txt", "teste6.txt"]:
        n, escola_a, escola_b = ler_arquivo(arquivo)
        sol, apt, _ = ag.algoritmo_genetico(
            n, escola_a, escola_b,
            tamanho_populacao=80, num_geracoes=300, semente=123,
        )
        _, apt_ot = melhor_solucao_forca_bruta(n, escola_a, escola_b)
        checa(eh_permutacao(sol, n), f"{arquivo}: solucao final e permutacao valida")
        checa(apt == apt_ot,
              f"{arquivo}: AG atinge o otimo ({apt} == {apt_ot})")
        # aptidao calculada de novo bate com a retornada
        checa(aptidao(sol, escola_a, escola_b) == apt,
              f"{arquivo}: aptidao retornada e consistente")


def teste_casos_extremos():
    print("teste_casos_extremos")
    # N=1: unica solucao possivel [0]
    sol, apt, hist = ag.algoritmo_genetico(1, [[1]], [[1]], num_geracoes=10, semente=1)
    checa(sol == [0], "N=1 resolve para [0]")
    # N=2
    ea = [[1, 2], [2, 1]]
    eb = [[1, 2], [2, 1]]
    sol2, apt2, _ = ag.algoritmo_genetico(2, ea, eb, num_geracoes=50, semente=1)
    _, ot2 = melhor_solucao_forca_bruta(2, ea, eb)
    checa(apt2 == ot2, "N=2 atinge o otimo")


def teste_callback():
    print("teste_callback (hook da Pessoa 5)")
    n, escola_a, escola_b = ler_arquivo("preferencias.txt")
    eventos = []
    ag.algoritmo_genetico(
        n, escola_a, escola_b, num_geracoes=15,
        callback=lambda info: eventos.append(info), semente=2,
    )
    checa(len(eventos) == 15, "callback chamado uma vez por geracao")
    chaves = {"geracao", "melhor_solucao", "melhor_aptidao", "aptidao_media", "aptidoes"}
    checa(chaves.issubset(eventos[0].keys()), "callback recebe as chaves esperadas")


def teste_mutacao_injetada():
    print("teste_mutacao_injetada (hook da Pessoa 4)")
    n, escola_a, escola_b = ler_arquivo("preferencias.txt")
    chamadas = {"n": 0}

    def mutacao_falsa(ind, taxa):
        chamadas["n"] += 1
        return ind

    ag.algoritmo_genetico(
        n, escola_a, escola_b, num_geracoes=5,
        mutacao=mutacao_falsa, semente=1,
    )
    checa(chamadas["n"] > 0, "mutacao fornecida externamente e utilizada pelo ciclo")


if __name__ == "__main__":
    import sys

    testes = [
        teste_populacao,
        teste_selecao_torneio,
        teste_selecao_roleta,
        teste_crossover_ox,
        teste_ciclo_nao_piora,
        teste_convergencia,
        teste_casos_extremos,
        teste_callback,
        teste_mutacao_injetada,
    ]

    print("==== Testes do nucleo do AG (Pessoa 3) ====\n")
    for t in testes:
        t()
        print()

    if _falhas:
        print(f"RESULTADO: {len(_falhas)} verificacao(oes) FALHARAM:")
        for f in _falhas:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("RESULTADO: todos os testes passaram.")
        sys.exit(0)
