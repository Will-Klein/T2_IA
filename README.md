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

---

# Núcleo do Algoritmo Genético (Pessoa 3)

Esta parte implementa o coração do Algoritmo Genético: a geração da população inicial, a seleção dos pais, o cruzamento (crossover) para permutações e o ciclo do AG que junta tudo e usa a função de aptidão da Pessoa 2.

O código fica em `nucleo_ag.py`. A explicação completa, os parâmetros e como testar estão documentados em `P3Solution.md`.

## O que foi entregue

| Componente | Função em `nucleo_ag.py` |
|---|---|
| População inicial | `gerar_populacao(n, tamanho_populacao)` |
| Seleção por torneio (padrão) | `selecao_torneio(populacao, aptidoes, k)` |
| Seleção por roleta (alternativa) | `selecao_roleta(populacao, aptidoes)` |
| Cruzamento Order Crossover (OX) | `crossover_ox(pai1, pai2)` |
| Ciclo completo do AG | `algoritmo_genetico(n, escola_a, escola_b, ...)` |

## Integração com os outros módulos

- **Pessoa 1 (leitura):** o ciclo recebe `n`, `escola_a`, `escola_b` produzidos por `ler_arquivo`.
- **Pessoa 2 (heurística):** a seleção e a evolução usam `aptidao(s, escola_a, escola_b)` diretamente.
- **Pessoa 4 (mutação e parada):** `algoritmo_genetico` aceita a função de mutação via parâmetro `mutacao` e o critério de parada via `num_geracoes` (a P4 substitui sem mexer no arquivo). Enquanto isso, há uma mutação por troca (swap) e parada por número de gerações como **padrões provisórios**, só para o núcleo rodar de forma isolada.
- **Pessoa 5 (modos de execução):** `algoritmo_genetico` aceita um `callback` chamado a cada geração (com melhor solução, aptidão e média), e devolve o `historico` da aptidão por geração — base para o modo passo a passo e para o gráfico de evolução.

## Parâmetros definidos

| Parâmetro | Valor padrão | Justificativa |
|---|---|---|
| `tamanho_populacao` | 80 | Diversidade suficiente sem custo alto; funciona para N pequeno e grande |
| `taxa_cruzamento` | 0.9 | Alta recombinação, faixa clássica de AG (0.6–0.95) |
| `k_torneio` | 3 | Pressão seletiva moderada, mantém diversidade |
| `elitismo` | `True` | O melhor indivíduo nunca se perde; a aptidão nunca piora |

> `taxa_mutacao` e `num_geracoes` aparecem como parâmetros, mas a definição e justificativa finais são responsabilidade da Pessoa 4.

## Como executar e testar

```bash
# Roda o núcleo do AG de forma isolada sobre um arquivo de preferências
python nucleo_ag.py preferencias.txt

# Roda a bateria de testes do núcleo
python test_nucleo_ag.py
```

Nos testes, o AG atinge o **ótimo global** (validado por força bruta) tanto em N=4 (`preferencias.txt`) quanto em N=6 (`teste6.txt`).

---

# Mutação e Critério de Parada (Pessoa 4)

Esta parte implementa o operador de mutação, define a taxa de mutação e integra o critério de parada ao ciclo do AG da Pessoa 3.

O código fica em `mutacao.py` e as alterações de integração estão em `nucleo_ag.py`. A explicação completa está em `P4Solution.md`.

## O que foi entregue

| Componente | Onde |
|---|---|
| Operador de mutação por troca — swap (padrão) | `mutacao.py` → `mutacao_swap` |
| Operador de mutação por inserção (alternativo) | `mutacao.py` → `mutacao_insercao` |
| Taxa de mutação definida e justificada | `mutacao.py` → `TAXA_MUTACAO_PADRAO = 0.15` |
| Critério de parada por número de gerações | `nucleo_ag.py` → parâmetro `num_geracoes` |
| Critério de parada por convergência | `nucleo_ag.py` → parâmetro `geracoes_sem_melhora` |

## Integração com os outros módulos

- **Pessoa 3 (núcleo):** `mutacao_swap` é injetado via parâmetro `mutacao` — nenhuma linha do núcleo foi reescrita. O novo parâmetro `geracoes_sem_melhora` encerra o loop antecipadamente quando a melhor aptidão não melhora por N gerações consecutivas.
- **Pessoa 5 (modos de execução):** o callback recebeu dois novos campos — `convergiu` (booleano, `True` na última iteração por convergência) e `geracoes_sem_melhora_atual` (contador atual) — para que a P5 possa exibir o motivo do encerramento.

## Parâmetros definidos

| Parâmetro | Valor | Justificativa |
|---|---|---|
| `TAXA_MUTACAO_PADRAO` | 0.15 | Equilíbrio entre diversidade e preservação de bons parciais; literatura clássica sugere 1/N a 0.3; 0.15 funciona bem para N entre 4 e 30 |
| `geracoes_sem_melhora` | 50 (recomendado) | Tempo suficiente para o swap + OX testarem variações sem desperdiçar gerações inúteis |

## Como executar

```bash
# Demonstra os operadores de mutação isolados
python mutacao.py

# AG completo com mutação e critério de parada da P4
python nucleo_ag.py preferencias.txt
```
