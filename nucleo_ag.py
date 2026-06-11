"""
Nucleo do Algoritmo Genetico (Pessoa 3).

Responsabilidades desta parte:
  - Gerar a populacao inicial de solucoes aleatorias
  - Selecao dos pais (torneio e roleta)
  - Cruzamento (crossover) para permutacoes: Order Crossover (OX)
  - Montar o ciclo do AG integrado com a funcao de aptidao da P2

Codificacao (definida pela P2):
  permutacao de tamanho N, onde s[i] = j significa A_(i+1) pareado com B_(j+1).

Pontos de extensao (responsabilidade de outras pessoas):
  - mutacao .......... Pessoa 4 (passada via parametro `mutacao`)
  - criterio de parada Pessoa 4 (parametros `num_geracoes` / `geracoes_sem_melhora`)
  - modos de execucao  Pessoa 5 (via parametro `callback`, chamado a cada geracao)

Para o nucleo funcionar de forma isolada e testavel, este modulo traz uma
mutacao por troca (swap) e um criterio de parada por numero de geracoes como
PADROES PROVISORIOS. A Pessoa 4 substitui ambos sem alterar este arquivo.
"""

import random

from heuristica import codificar, aptidao, decodificar, custo


# ---------------------------------------------------------------------------
# 1. Populacao inicial
# ---------------------------------------------------------------------------

def gerar_populacao(n, tamanho_populacao):
    """
    Cria `tamanho_populacao` solucoes aleatorias (permutacoes de tamanho N).

    Usa `codificar(n)` da P2, que ja embaralha os indices, garantindo que
    todo individuo e uma permutacao valida (pareamento heterogeneo valido).
    """
    if tamanho_populacao < 1:
        raise ValueError("tamanho_populacao deve ser >= 1.")
    return [codificar(n) for _ in range(tamanho_populacao)]


# ---------------------------------------------------------------------------
# 2. Selecao
# ---------------------------------------------------------------------------

def selecao_torneio(populacao, aptidoes, k=3):
    """
    Selecao por torneio: sorteia `k` individuos e devolve o de maior aptidao.

    Escolhida como padrao por ser simples, eficiente e por permitir controlar
    a pressao seletiva pelo tamanho `k` do torneio (k maior = mais pressao).
    Nao depende dos valores absolutos de aptidao, so da ordem relativa, o que
    a torna robusta para qualquer N.
    """
    if k < 1:
        raise ValueError("k do torneio deve ser >= 1.")
    k = min(k, len(populacao))
    competidores = random.sample(range(len(populacao)), k)
    vencedor = max(competidores, key=lambda i: aptidoes[i])
    return populacao[vencedor]


def selecao_roleta(populacao, aptidoes):
    """
    Selecao por roleta (fitness proportionate), oferecida como alternativa.

    A probabilidade de um individuo ser escolhido e proporcional a sua aptidao.
    Como a aptidao da P2 ja e >= 0, pode ser usada diretamente como peso. Se a
    soma das aptidoes for 0 (caso degenerado), cai para escolha uniforme.
    """
    total = sum(aptidoes)
    if total <= 0:
        return populacao[random.randrange(len(populacao))]
    sorteio = random.uniform(0, total)
    acumulado = 0
    for individuo, apt in zip(populacao, aptidoes):
        acumulado += apt
        if acumulado >= sorteio:
            return individuo
    return populacao[-1]


# ---------------------------------------------------------------------------
# 3. Cruzamento (Order Crossover - OX)
# ---------------------------------------------------------------------------

def crossover_ox(pai1, pai2):
    """
    Order Crossover (OX), apropriado para permutacoes.

    Passos:
      1. Sorteia dois pontos de corte [a, b].
      2. Copia o segmento pai1[a..b] para o filho na mesma posicao.
      3. Preenche as posicoes restantes com os genes de pai2, na ordem em que
         aparecem a partir de b+1 (circular), pulando os ja presentes.

    O resultado e sempre uma permutacao valida (sem repeticao), preservando
    parte da ordem de cada pai. Para N == 1 devolve uma copia do pai.
    """
    n = len(pai1)
    if n != len(pai2):
        raise ValueError("Os pais devem ter o mesmo tamanho.")
    if n <= 1:
        return pai1[:]

    a, b = sorted(random.sample(range(n), 2))

    filho = [None] * n
    filho[a:b + 1] = pai1[a:b + 1]
    presentes = set(pai1[a:b + 1])

    pos = (b + 1) % n
    for desloc in range(n):
        gene = pai2[(b + 1 + desloc) % n]
        if gene not in presentes:
            filho[pos] = gene
            presentes.add(gene)
            pos = (pos + 1) % n

    return filho


# ---------------------------------------------------------------------------
# Padroes provisorios (serao substituidos pela Pessoa 4)
# ---------------------------------------------------------------------------

def _mutacao_swap_padrao(individuo, taxa_mutacao):
    """
    Mutacao por troca de duas posicoes (PROVISORIA - placeholder da P4).

    Com probabilidade `taxa_mutacao`, troca dois genes de lugar. Mantem a
    permutacao valida. A Pessoa 4 deve fornecer a versao definitiva via o
    parametro `mutacao` de `algoritmo_genetico`.
    """
    filho = individuo[:]
    if len(filho) >= 2 and random.random() < taxa_mutacao:
        i, j = random.sample(range(len(filho)), 2)
        filho[i], filho[j] = filho[j], filho[i]
    return filho


# ---------------------------------------------------------------------------
# 4. Ciclo do Algoritmo Genetico
# ---------------------------------------------------------------------------

def algoritmo_genetico(
    n,
    escola_a,
    escola_b,
    tamanho_populacao=80,
    taxa_cruzamento=0.9,
    taxa_mutacao=0.2,
    num_geracoes=300,
    k_torneio=3,
    elitismo=True,
    selecao=selecao_torneio,
    mutacao=None,
    callback=None,
    semente=None,
):
    """
    Executa o ciclo completo do AG e devolve a melhor solucao encontrada.

    Parametros do nucleo (Pessoa 3):
      tamanho_populacao : numero de individuos por geracao.
      taxa_cruzamento   : prob. de aplicar OX entre dois pais (senao copia o pai).
      k_torneio         : tamanho do torneio na selecao.
      elitismo          : se True, o melhor individuo sempre passa para a proxima
                          geracao (garante que a aptidao nunca piora).
      selecao           : funcao de selecao (padrao: torneio; alternativa: roleta).

    Parametros de outras pessoas (com padroes provisorios):
      taxa_mutacao, num_geracoes : Pessoa 4.
      mutacao                    : Pessoa 4 (padrao: swap provisorio).
      callback                   : Pessoa 5, recebe um dicionario por geracao.

    Retorna:
      (melhor_solucao, melhor_aptidao, historico)
      onde `historico` e a lista da melhor aptidao acumulada por geracao,
      usada pela Pessoa 5 para mostrar a evolucao da funcao heuristica.
    """
    if semente is not None:
        random.seed(semente)
    if mutacao is None:
        mutacao = _mutacao_swap_padrao

    populacao = gerar_populacao(n, tamanho_populacao)
    historico = []
    melhor_global = None
    melhor_apt_global = float("-inf")

    for geracao in range(num_geracoes):
        aptidoes = [aptidao(ind, escola_a, escola_b) for ind in populacao]

        idx_melhor = max(range(len(populacao)), key=lambda i: aptidoes[i])
        if aptidoes[idx_melhor] > melhor_apt_global:
            melhor_apt_global = aptidoes[idx_melhor]
            melhor_global = populacao[idx_melhor][:]

        historico.append(melhor_apt_global)

        if callback is not None:
            callback({
                "geracao": geracao,
                "melhor_solucao": melhor_global[:],
                "melhor_aptidao": melhor_apt_global,
                "aptidao_media": sum(aptidoes) / len(aptidoes),
                "aptidoes": aptidoes,
            })

        # Monta a proxima geracao.
        nova_populacao = []
        if elitismo:
            nova_populacao.append(populacao[idx_melhor][:])

        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao(populacao, aptidoes, k_torneio) \
                if selecao is selecao_torneio else selecao(populacao, aptidoes)
            pai2 = selecao(populacao, aptidoes, k_torneio) \
                if selecao is selecao_torneio else selecao(populacao, aptidoes)

            if random.random() < taxa_cruzamento:
                filho = crossover_ox(pai1, pai2)
            else:
                filho = pai1[:]

            filho = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)

        populacao = nova_populacao

    return melhor_global, melhor_apt_global, historico


# ---------------------------------------------------------------------------
# Execucao isolada para teste rapido do nucleo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    from leitor import ler_arquivo
    from heuristica import aptidao_normalizada, melhor_solucao_forca_bruta

    caminho = sys.argv[1] if len(sys.argv) > 1 else "preferencias.txt"

    try:
        n, escola_a, escola_b = ler_arquivo(caminho)
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' nao encontrado.")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro no formato do arquivo: {e}")
        sys.exit(1)

    print(f"[------ Nucleo do AG: N -> {n} ------]\n")

    sol, apt, hist = algoritmo_genetico(n, escola_a, escola_b, semente=42)

    print(f"Geracoes executadas:   {len(hist)}")
    print(f"Aptidao inicial:       {hist[0]}")
    print(f"Aptidao final:         {apt}")
    print(f"Aptidao normalizada:   {aptidao_normalizada(sol, escola_a, escola_b):.4f}")
    print(f"Solucao codificada:    {sol}")
    print(f"Solucao decodificada:  {decodificar(sol)}")
    print(f"Custo total:           {custo(sol, escola_a, escola_b)}")

    if n <= 8:
        _, apt_ot = melhor_solucao_forca_bruta(n, escola_a, escola_b)
        marca = "OTIMO" if apt == apt_ot else f"abaixo do otimo ({apt_ot})"
        print(f"\nMelhor possivel (forca bruta): {apt_ot}  ->  AG atingiu: {marca}")
