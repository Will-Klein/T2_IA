def ler_arquivo(caminho):
    with open(caminho, 'r') as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]

    n = int(linhas[0])

    linhas_necessarias = 1 + 2 * n
    if len(linhas) < linhas_necessarias:
        raise ValueError(
            f"Arquivo incompleto: esperado {linhas_necessarias} linhas, encontrado {len(linhas)}."
        )

    escola_a = []
    for i in range(1, n + 1):
        valores = list(map(int, linhas[i].split()))
        if len(valores) != n:
            raise ValueError(
                f"Linha {i + 1} da Escola A tem {len(valores)} valores, esperado {n}."
            )
        escola_a.append(valores)

    escola_b = []
    for i in range(n + 1, 2 * n + 1):
        valores = list(map(int, linhas[i].split()))
        if len(valores) != n:
            raise ValueError(
                f"Linha {i + 1} da Escola B tem {len(valores)} valores, esperado {n}."
            )
        escola_b.append(valores)

    return n, escola_a, escola_b


def exibir_matrizes(n, escola_a, escola_b):
    print(f"Numero de duplas: {n}\n")

    print("Preferencias da Escola A:")
    print("       " + "  ".join([f"B{j+1}" for j in range(n)]))
    for i, linha in enumerate(escola_a):
        print(f"  A{i+1}   " + "   ".join(map(str, linha)))

    print("\nPreferencias da Escola B:")
    print("       " + "  ".join([f"A{j+1}" for j in range(n)]))
    for i, linha in enumerate(escola_b):
        print(f"  B{i+1}   " + "   ".join(map(str, linha)))


if __name__ == "__main__":
    import sys

    caminho = sys.argv[1] if len(sys.argv) > 1 else "preferencias.txt"

    try:
        n, escola_a, escola_b = ler_arquivo(caminho)
        exibir_matrizes(n, escola_a, escola_b)
        print("\nArquivo lido com sucesso!")
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' nao encontrado.")
    except ValueError as e:
        print(f"Erro no formato do arquivo: {e}")