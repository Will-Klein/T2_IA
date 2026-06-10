# Módulo de Leitura de Arquivo

## Sobre

Este módulo é responsável por ler o arquivo texto de entrada e transformá-lo em estruturas de dados prontas para serem consumidas pelo restante do sistema, especialmente pela função heurística e pelo núcleo do Algoritmo Genético.

---

## Arquivo de Entrada

O arquivo texto segue o seguinte formato:

```
N
(N linhas de preferências da Escola A)
(N linhas de preferências da Escola B)
```

Onde:
- **N** é o número de duplas, definido na primeira linha do arquivo
- Cada linha da Escola A representa um aluno, e cada valor representa a posição de preferência daquele aluno em relação a cada aluno da Escola B
- O mesmo vale para a Escola B em relação aos alunos da Escola A
- Quanto menor o número, maior a preferência

### Exemplo de arquivo (`preferencias.txt`):

```
4
1 2 4 3
2 3 1 4
4 1 3 2
3 1 2 4
3 2 4 1
3 2 4 1
2 4 3 1
1 3 4 2
```

Neste exemplo, N=4, as 4 primeiras linhas após o N são as preferências da Escola A, e as 4 linhas seguintes são as preferências da Escola B.

---

## Estrutura do Código (`leitor.py`)

O módulo contém duas funções principais.

### `ler_arquivo(caminho)`

Responsável por toda a leitura e validação do arquivo. Recebe o caminho do arquivo como parâmetro e retorna uma tupla com três elementos:

```python
n, escola_a, escola_b = ler_arquivo("preferencias.txt")
```

| Retorno | Tipo | Descrição |
|---|---|---|
| `n` | `int` | Número de duplas |
| `escola_a` | `list[list[int]]` | Matriz N×N de preferências da Escola A |
| `escola_b` | `list[list[int]]` | Matriz N×N de preferências da Escola B |

### `exibir_matrizes(n, escola_a, escola_b)`

Exibe as matrizes de forma legível no terminal, com cabeçalhos identificando os alunos de cada escola. Útil para conferência visual dos dados lidos.

---

## Decisões Técnicas

### Representação como lista de listas
As matrizes foram representadas como `list[list[int]]` por ser a estrutura mais simples e direta em Python, sem necessidade de bibliotecas externas como NumPy. O acesso por índice é intuitivo: `escola_a[i][j]` retorna a preferência do aluno `i` da Escola A pelo aluno `j` da Escola B. Além disso, é compatível com qualquer outra parte do sistema sem dependências adicionais.

### Filtragem de linhas vazias
O arquivo pode conter linhas em branco no final ou entre seções dependendo do editor utilizado. O código filtra essas linhas durante a leitura para evitar erros desnecessários.

### Validação do número de valores por linha
Arquivos gerados manualmente estão sujeitos a erros como esquecer um valor ou digitar um a mais. A validação garante que o programa falha com uma mensagem clara e precisa, em vez de produzir resultados silenciosamente incorretos que seriam difíceis de rastrear nas etapas seguintes.

---

## Validações Implementadas

O módulo detecta e reporta claramente os seguintes erros:

| Situação | Mensagem de erro |
|---|---|
| Arquivo não encontrado | `Erro: arquivo 'x' nao encontrado.` |
| Arquivo com linhas insuficientes | `Arquivo incompleto: esperado X linhas, encontrado Y.` |
| Linha com número errado de valores | `Linha X da Escola A tem Y valores, esperado Z.` |

---

## Como Executar

O módulo pode ser executado diretamente pelo terminal, recebendo o nome do arquivo como argumento:

```bash
python leitor.py preferencias.txt
```

Se nenhum argumento for passado, o programa tenta abrir `preferencias.txt` na pasta atual por padrão.

### Saída esperada:

```
Numero de duplas: 4

Preferencias da Escola A:
       B1  B2  B3  B4
  A1   1   2   4   3
  A2   2   3   1   4
  A3   4   1   3   2
  A4   3   1   2   4

Preferencias da Escola B:
       A1  A2  A3  A4
  B1   3   2   4   1
  B2   3   2   4   1
  B3   2   4   3   1
  B4   1   3   4   2

Arquivo lido com sucesso!
```

---

## Como Usar como Módulo

Os outros arquivos do sistema importam este módulo da seguinte forma:

```python
from leitor import ler_arquivo

n, escola_a, escola_b = ler_arquivo("preferencias.txt")
```

A partir disso, `escola_a[i][j]` retorna a preferência do aluno `i+1` da Escola A pelo aluno `j+1` da Escola B, e o mesmo vale para `escola_b`.

---

## Arquivos de Teste

Foram criados cinco arquivos de teste para validar o módulo em diferentes cenários:

| Arquivo | N | Objetivo |
|---|---|---|
| `preferencias.txt` | 4 | Caso base do enunciado |
| `teste_2.txt` | 2 | Caso mínimo, N pequeno |
| `teste_6.txt` | 6 | Caso maior, N grande |
| `teste_erro.txt` | 4 | Arquivo com linha faltando |
| `teste_erro2.txt` | 4 | Linha com valor faltando |

---

## Resultados dos Testes

Todos os testes produziram os resultados esperados:

- Leitura correta do arquivo base (N=4)
- Leitura correta com N=2
- Leitura correta com N=6
- Erro detectado corretamente quando o arquivo está incompleto
- Erro detectado corretamente quando uma linha tem quantidade incorreta de valores

---

## Considerações

A validação do arquivo de entrada é crítica para o funcionamento correto de todo o sistema. Um erro de leitura, como capturar índices errados ou aceitar um arquivo malformado sem avisar, causaria resultados incorretos em todos os módulos seguintes de forma silenciosa, tornando a depuração muito mais difícil. As validações implementadas garantem que o sistema falha cedo e com mensagens objetivas, facilitando a identificação de problemas nos arquivos de entrada.
