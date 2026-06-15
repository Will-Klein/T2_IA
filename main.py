"""
Pessoa 5 — Modos de execucao e interface de saida.

Uso:
  python main.py <arquivo> [--passo-a-passo]

  Sem --passo-a-passo: modo completo (executa tudo e exibe resultado).
  Com --passo-a-passo: pausa a cada geracao, aguarda Enter para continuar.

Exemplo:
  python main.py preferencias.txt
  python main.py preferencias.txt --passo-a-passo
"""

import sys
import argparse

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from leitor import ler_arquivo
from heuristica import decodificar, aptidao_normalizada, custo
from nucleo_ag import algoritmo_genetico


# ---------------------------------------------------------------------------
# Helpers de exibicao
# ---------------------------------------------------------------------------

def _cabecalho(titulo):
    linha = "=" * 60
    print(f"\n{linha}")
    print(f"  {titulo}")
    print(linha)


def _exibir_estado_geracao(dados):
    g = dados["geracao"]
    apt = dados["melhor_aptidao"]
    media = dados["aptidao_media"]
    sol = dados["melhor_solucao"]
    print(
        f"  Geracao {g + 1:>4d} | "
        f"Melhor aptidao: {apt:>6.1f} | "
        f"Media: {media:>6.1f} | "
        f"Melhor: {sol}"
    )


def _exibir_resultado_final(sol, apt, escola_a, escola_b, historico):
    _cabecalho("RESULTADO FINAL")
    print(f"\n  Geracoes executadas : {len(historico)}")
    print(f"  Aptidao inicial     : {historico[0]:.1f}")
    print(f"  Melhor aptidao      : {apt:.1f}")
    apt_norm = aptidao_normalizada(sol, escola_a, escola_b)
    print(f"  Aptidao normalizada : {apt_norm:.4f}  (1.0 = solucao otima)")
    print(f"  Custo total         : {custo(sol, escola_a, escola_b)}")

    print(f"\n  Solucao codificada  : {sol}")
    dec = decodificar(sol)
    print(f"  Solucao decodificada:")
    for par in dec:
        print(f"    {par}")


# ---------------------------------------------------------------------------
# Grafico de evolucao da heuristica
# ---------------------------------------------------------------------------

def _criar_figura():
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#2a2a3e")
    ax.set_title("Evolucao da Aptidao — Algoritmo Genetico", color="white", pad=10)
    ax.set_xlabel("Geracao", color="#aaaacc")
    ax.set_ylabel("Melhor Aptidao", color="#aaaacc")
    ax.tick_params(colors="#aaaacc")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    for spine in ax.spines.values():
        spine.set_edgecolor("#555577")
    fig.tight_layout()
    return fig, ax


def _plotar_historico_final(historico):
    """Exibe grafico estatico ao final (modo completo ou pos-execucao passo a passo)."""
    fig, ax = _criar_figura()
    ax.plot(
        range(1, len(historico) + 1),
        historico,
        color="#7ec8e3",
        linewidth=1.5,
        label="Melhor aptidao",
    )
    ax.fill_between(
        range(1, len(historico) + 1),
        historico,
        alpha=0.15,
        color="#7ec8e3",
    )
    ax.legend(facecolor="#2a2a3e", labelcolor="white")
    plt.show()


# ---------------------------------------------------------------------------
# Modo completo
# ---------------------------------------------------------------------------

def modo_completo(n, escola_a, escola_b):
    _cabecalho("MODO COMPLETO — executando o AG...")

    resultados = {}

    def callback(dados):
        if dados["geracao"] % 10 == 0 or dados["geracao"] == 0:
            _exibir_estado_geracao(dados)
        resultados["ultimo"] = dados

    sol, apt, historico = algoritmo_genetico(
        n, escola_a, escola_b, callback=callback
    )

    if resultados.get("ultimo") and resultados["ultimo"]["geracao"] % 10 != 0:
        _exibir_estado_geracao(resultados["ultimo"])

    _exibir_resultado_final(sol, apt, escola_a, escola_b, historico)
    _plotar_historico_final(historico)


# ---------------------------------------------------------------------------
# Modo passo a passo
# ---------------------------------------------------------------------------

def modo_passo_a_passo(n, escola_a, escola_b):
    plt.ion()
    fig, ax = _criar_figura()
    linha, = ax.plot([], [], color="#f4a261", linewidth=1.5, label="Melhor aptidao")
    ax.legend(facecolor="#2a2a3e", labelcolor="white")
    plt.show(block=False)

    xs, ys = [], []

    _cabecalho("MODO PASSO A PASSO — pressione Enter para avancar cada geracao")
    print("  (digite 'q' + Enter para encerrar antecipadamente)\n")

    parar = [False]

    def callback(dados):
        if parar[0]:
            return

        _exibir_estado_geracao(dados)

        xs.append(dados["geracao"] + 1)
        ys.append(dados["melhor_aptidao"])
        linha.set_data(xs, ys)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()

        entrada = input("  [Enter = proxima geracao | q = encerrar] ").strip().lower()
        if entrada == "q":
            parar[0] = True

    sol, apt, historico = algoritmo_genetico(
        n, escola_a, escola_b, callback=callback
    )

    plt.ioff()

    _exibir_resultado_final(sol, apt, escola_a, escola_b, historico)

    print("\n  Exibindo grafico final...")
    ax.clear()
    ax.set_facecolor("#2a2a3e")
    ax.set_title("Evolucao da Aptidao — Algoritmo Genetico", color="white", pad=10)
    ax.set_xlabel("Geracao", color="#aaaacc")
    ax.set_ylabel("Melhor Aptidao", color="#aaaacc")
    ax.tick_params(colors="#aaaacc")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    for spine in ax.spines.values():
        spine.set_edgecolor("#555577")
    ax.plot(
        range(1, len(historico) + 1),
        historico,
        color="#f4a261",
        linewidth=1.5,
        label="Melhor aptidao",
    )
    ax.fill_between(range(1, len(historico) + 1), historico, alpha=0.15, color="#f4a261")
    ax.legend(facecolor="#2a2a3e", labelcolor="white")
    fig.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="T2 IA — Organizacao de Quartos Duplos via Algoritmo Genetico"
    )
    parser.add_argument(
        "arquivo",
        help="Caminho para o arquivo de preferencias (.txt)",
    )
    parser.add_argument(
        "--passo-a-passo",
        action="store_true",
        help="Executa o AG pausado, geracao por geracao",
    )
    args = parser.parse_args()

    try:
        n, escola_a, escola_b = ler_arquivo(args.arquivo)
    except FileNotFoundError:
        print(f"Erro: arquivo '{args.arquivo}' nao encontrado.")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro no formato do arquivo: {e}")
        sys.exit(1)

    print(f"\nArquivo carregado: {args.arquivo}")
    print(f"Numero de duplas : {n}")

    if args.passo_a_passo:
        modo_passo_a_passo(n, escola_a, escola_b)
    else:
        modo_completo(n, escola_a, escola_b)


if __name__ == "__main__":
    main()
