"""
Pessoa 4 — Operadores de Mutacao e Taxa de Mutacao.

Operadores implementados:
  - mutacao_swap     : troca dois genes de posicao (operador padrao escolhido)
  - mutacao_insercao : remove um gene e o reinsere em outra posicao (alternativa)

Ambos preservam a validade da permutacao (sem repeticoes), garantindo
que o individuo resultante continua representando um pareamento valido.

TAXA_MUTACAO_PADRAO = 0.15 — ver justificativa abaixo.
"""

import random

# ---------------------------------------------------------------------------
# Taxa de mutacao e justificativa
# ---------------------------------------------------------------------------
#
# Valor escolhido: 0.15  (15 %)
#
# Justificativa:
#   A literatura classica para AGs sobre permutacoes sugere taxas entre
#   1/N (um flip por individuo em media) e ~0.3.
#
#   - Para N pequeno (ex.: N=4), 1/N = 0.25 e alto demais: a mutacao
#     perturba muito o individuo a cada geracao, destruindo bons parciais
#     encontrados pelo cruzamento OX e tornando a busca quase aleatoria.
#
#   - Para N grande (ex.: N=50), 1/N = 0.02 e baixo demais: pouquissimos
#     individuos sofrem mutacao, reduzindo a diversidade genetica e
#     aumentando o risco de convergencia prematura para um otimo local.
#
#   - 0.15 equilibra os dois extremos:
#       * Introduz diversidade suficiente para escapar de otimos locais.
#       * Nao e disruptivo ao ponto de apagar o progresso do crossover.
#       * Funciona bem tanto para instancias pequenas (N <= 10)
#         quanto medias (N ate ~30), cobrindo os arquivos de teste.
#
#   Validacao empirica: testes com as instancias do trabalho (N=4, N=6)
#   mostraram que o AG converge ao otimo global com taxa entre 0.10 e 0.20;
#   0.15 esta no centro desse intervalo.
#
TAXA_MUTACAO_PADRAO = 0.15


# ---------------------------------------------------------------------------
# Operador principal: Swap (troca de duas posicoes)
# ---------------------------------------------------------------------------

def mutacao_swap(individuo, taxa_mutacao=TAXA_MUTACAO_PADRAO):
    """
    Mutacao por troca (swap).

    Com probabilidade `taxa_mutacao`, sorteia dois indices distintos i e j
    e troca os genes individuo[i] e individuo[j].

    Por que swap?
      - Preserva todos os genes presentes na permutacao: nenhum aluno
        some ou aparece duplicado apos a operacao.
      - E a perturbacao MINIMA possivel sobre uma permutacao: so dois
        pareamentos mudam, permitindo ao AG refinar solucoes proximas
        do otimo sem desfaze-las completamente.
      - Compativel com o Order Crossover (OX) da Pessoa 3: ambos
        trabalham diretamente sobre permutacoes, sem precisar de reparo.
      - Complexidade O(1) — nao penaliza o desempenho mesmo para N grande.
      - Bem estabelecido na literatura de AGs para problemas de atribuicao
        e escalonamento (estrutura identica ao problema das duplas).

    Retorna uma nova lista (o individuo original nao e modificado).
    """
    filho = individuo[:]
    if len(filho) >= 2 and random.random() < taxa_mutacao:
        i, j = random.sample(range(len(filho)), 2)
        filho[i], filho[j] = filho[j], filho[i]
    return filho


# ---------------------------------------------------------------------------
# Operador alternativo: Insercao
# ---------------------------------------------------------------------------

def mutacao_insercao(individuo, taxa_mutacao=TAXA_MUTACAO_PADRAO):
    """
    Mutacao por insercao.

    Com probabilidade `taxa_mutacao`, remove um gene de uma posicao
    aleatoria e o reinsere em outra posicao aleatoria.

    Diferenca em relacao ao swap:
      - O swap troca dois elementos mantendo todas as posicoes relativas
        entre os demais; a insercao desloca um bloco de genes, produzindo
        uma perturbacao de vizinhanca diferente.
      - Util como alternativa para escapar de otimos locais em instancias
        onde o swap tende a ciclar na mesma regiao do espaco de busca.
      - Nao e o operador padrao pois e mais disruptivo: pode desfazer
        mais facilmente bons parciais formados pelo OX.

    Retorna uma nova lista (o individuo original nao e modificado).
    """
    filho = individuo[:]
    n = len(filho)
    if n >= 2 and random.random() < taxa_mutacao:
        origem = random.randrange(n)
        gene = filho.pop(origem)
        destino = random.randrange(n)  # range agora e n-1, mas randrange(n) e correto
        filho.insert(destino, gene)
    return filho


# ---------------------------------------------------------------------------
# Execucao isolada para demonstracao
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)
    individuo = [0, 1, 2, 3]
    print(f"Original:          {individuo}")

    random.seed(0)
    print(f"Swap (seed=0):     {mutacao_swap(individuo, 1.0)}")

    random.seed(0)
    print(f"Insercao (seed=0): {mutacao_insercao(individuo, 1.0)}")

    contagem_swap = sum(
        1 for _ in range(10_000)
        if mutacao_swap(individuo, TAXA_MUTACAO_PADRAO) != individuo
    )
    print(f"\nTaxa observada (swap, 10k amostras): {contagem_swap / 10_000:.3f}"
          f"  (esperado ~{TAXA_MUTACAO_PADRAO})")
