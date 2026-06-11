# Pessoa 3 — Núcleo do Algoritmo Genético

Documento da minha parte do trabalho: **população inicial, seleção, cruzamento e o ciclo do AG** integrado com a função heurística da Pessoa 2.

Arquivos desta entrega:
- `nucleo_ag.py` — implementação do núcleo do AG
- `test_nucleo_ag.py` — bateria de testes do núcleo

---

## 1. Visão geral

O Algoritmo Genético resolve o problema de distribuir alunos da Escola A e da Escola B em duplas heterogêneas, buscando a distribuição que melhor respeita as preferências de todos.

Minha parte cuida do **ciclo evolutivo**: criar uma população de soluções, selecionar as melhores como pais, cruzá-las para gerar filhos e repetir isso ao longo das gerações, sempre guiado pela função de aptidão (Pessoa 2).

```
população inicial ──► [ avalia aptidão ] ──► seleção ──► cruzamento ──► mutação ──► nova população
                                  ▲                                                        │
                                  └────────────────────── repete por geração ─────────────┘
```

A **mutação** e o **critério de parada** são da Pessoa 4 e entram por parâmetro. A **leitura** é da Pessoa 1 e a **aptidão/codificação** é da Pessoa 2.

---

## 2. Codificação usada (definida com a Pessoa 2)

Cada solução é uma **permutação** de tamanho N:

```
s[i] = j   →   aluno A(i+1) forma dupla com aluno B(j+1)
```

Exemplo (N=4): `[3, 0, 2, 1]` → `A1-B4`, `A2-B1`, `A3-B3`, `A4-B2`.

Usar permutação é importante para o meu núcleo porque garante que **toda solução já nasce válida**: cada aluno da Escola B aparece exatamente uma vez, então nenhuma dupla se repete. Por isso os operadores de cruzamento e mutação precisam **preservar a permutação** — não basta cruzar listas como em um AG binário comum.

---

## 3. Componentes implementados

### 3.1 População inicial — `gerar_populacao(n, tamanho_populacao)`

Cria `tamanho_populacao` permutações aleatórias usando `codificar(n)` da Pessoa 2 (que embaralha os índices). Cada indivíduo é uma solução válida e diferente, dando diversidade ao ponto de partida.

### 3.2 Seleção

Implementei duas estratégias:

- **`selecao_torneio(populacao, aptidoes, k=3)`** — *padrão escolhido*. Sorteia `k` indivíduos e devolve o de maior aptidão. É simples, rápida e permite controlar a **pressão seletiva** pelo tamanho do torneio: `k` maior favorece mais os melhores (converge mais rápido, mas arrisca perder diversidade); `k` menor mantém mais variedade. Outra vantagem é que ela depende só da **ordem** das aptidões, não dos valores absolutos, então funciona bem para qualquer N e qualquer escala de custo.
- **`selecao_roleta(populacao, aptidoes)`** — alternativa. A chance de ser escolhido é proporcional à aptidão. Como a aptidão da Pessoa 2 já é sempre ≥ 0, dá para usá-la direto como peso. Mantida como opção comparativa e como prova de que o ciclo aceita trocar a estratégia de seleção.

**Por que torneio como padrão:** menos sensível a "super-indivíduos" (que na roleta dominariam cedo a seleção) e robusto quando muitas soluções têm aptidão parecida — situação comum neste problema.

### 3.3 Cruzamento — `crossover_ox(pai1, pai2)` (Order Crossover, OX)

Crossover clássico de um ponto não serve para permutações (geraria alunos repetidos). O **OX** resolve isso:

1. Sorteia dois pontos de corte `[a, b]`.
2. Copia o segmento `pai1[a..b]` para o filho, na mesma posição.
3. Preenche o resto com os genes de `pai2`, na ordem em que aparecem a partir de `b+1` (de forma circular), **pulando** os que já estão no filho.

O resultado é **sempre uma permutação válida** e herda informação dos dois pais: a *posição absoluta* de um trecho do pai 1 e a *ordem relativa* do pai 2. Para N=1 ele devolve uma cópia do pai (não há o que cruzar).

### 3.4 Ciclo do AG — `algoritmo_genetico(...)`

Junta tudo:

1. Gera a população inicial.
2. A cada geração: avalia a aptidão de todos, registra o melhor global e (se `callback`) reporta o estado.
3. Aplica **elitismo**: o melhor indivíduo passa direto para a próxima geração.
4. Preenche o resto da nova população selecionando pais, aplicando OX (com probabilidade `taxa_cruzamento`) e mutação.
5. Repete por `num_geracoes` gerações.
6. Retorna `(melhor_solucao, melhor_aptidao, historico)`.

O `historico` é a lista da melhor aptidão acumulada por geração — é o que a Pessoa 5 usa para mostrar a **evolução da função heurística**.

---

## 4. Parâmetros e justificativas

| Parâmetro | Padrão | Justificativa |
|---|---|---|
| `tamanho_populacao` | 80 | Diversidade suficiente para explorar o espaço sem custo computacional alto. Funciona bem tanto para N pequeno quanto grande. |
| `taxa_cruzamento` | 0.9 | Recombinação é o principal motor de busca do AG; taxas altas (0.6–0.95) são a faixa clássica. 0.9 dá muita exploração e ainda deixa ~10% dos filhos como cópia direta de um pai, preservando bons indivíduos. |
| `k_torneio` | 3 | Pressão seletiva moderada: empurra para os melhores sem matar a diversidade cedo demais. |
| `elitismo` | `True` | Garante que a melhor solução nunca se perde. Consequência direta: **a aptidão nunca piora entre gerações** (propriedade testada). |

> **Limite da minha parte:** `taxa_mutacao` e `num_geracoes` existem como parâmetros para o ciclo rodar de forma isolada, mas a **escolha e justificativa finais desses dois valores são da Pessoa 4** (mutação e critério de parada). No meu código eles têm padrões provisórios apenas para os testes funcionarem sozinhos.

---

## 5. Interfaces (como minha parte conversa com as outras)

```python
from leitor import ler_arquivo            # Pessoa 1
import nucleo_ag as ag                     # Pessoa 3

n, escola_a, escola_b = ler_arquivo("preferencias.txt")

melhor, aptidao_final, historico = ag.algoritmo_genetico(
    n, escola_a, escola_b,
    tamanho_populacao=80,
    taxa_cruzamento=0.9,
    mutacao=minha_mutacao_da_P4,    # opcional — Pessoa 4
    num_geracoes=300,               # opcional — Pessoa 4
    callback=minha_funcao_da_P5,    # opcional — Pessoa 5
    semente=42,                     # reprodutibilidade
)
```

**Pontos de extensão pensados para o grupo:**

- **Pessoa 4** entrega a mutação no formato `mutacao(individuo, taxa_mutacao) -> individuo` e passa via `mutacao=...`. O critério de parada entra por `num_geracoes` (e dá para evoluir para parada por convergência sem mudar minha assinatura).
- **Pessoa 5** passa um `callback(info)` que recebe, a cada geração, um dicionário com `geracao`, `melhor_solucao`, `melhor_aptidao`, `aptidao_media` e `aptidoes`. Isso atende tanto o **modo passo a passo** quanto o **gráfico de evolução**. O `historico` retornado também serve para o gráfico no modo completo.

---

## 6. Como executar

Pré-requisito: Python 3.

```bash
# Executa o núcleo isolado sobre um arquivo de preferências (aceita args)
python nucleo_ag.py preferencias.txt
python nucleo_ag.py teste6.txt
```

Saída de exemplo (N=4):

```
[------ Nucleo do AG: N -> 4 ------]

Geracoes executadas:   300
Aptidao inicial:       16
Aptidao final:         16
Aptidao normalizada:   0.6667
Solucao codificada:    [3, 0, 2, 1]
Solucao decodificada:  ['A1-B4', 'A2-B1', 'A3-B3', 'A4-B2']
Custo total:           16

Melhor possivel (forca bruta): 16  ->  AG atingiu: OTIMO
```

---

## 7. Como testar

```bash
python test_nucleo_ag.py
```

A bateria de testes cobre:

| Teste | O que valida |
|---|---|
| `teste_populacao` | Tamanho correto e cada indivíduo é permutação válida; rejeita tamanho inválido |
| `teste_selecao_torneio` | Torneio com `k=N` escolhe sempre o melhor; `k=1` devolve indivíduo válido |
| `teste_selecao_roleta` | Não quebra com soma de aptidões 0; favorece estatisticamente o melhor |
| `teste_crossover_ox` | OX gera permutação válida (200 amostras); trata N=1; rejeita pais de tamanhos diferentes |
| `teste_ciclo_nao_piora` | Com elitismo, o histórico de aptidão é monotônico não-decrescente |
| `teste_convergencia` | O AG atinge o **ótimo global** (comparado com força bruta) em N=4 e N=6 |
| `teste_casos_extremos` | Funciona para N=1 e N=2 |
| `teste_callback` | O hook da Pessoa 5 é chamado uma vez por geração com as chaves certas |
| `teste_mutacao_injetada` | O hook de mutação da Pessoa 4 é de fato usado pelo ciclo |

Resultado atual: **todos os testes passam** e o AG encontra o ótimo nos casos checáveis por força bruta.

---

## 8. Considerações sobre o desenvolvimento

- O ponto mais importante foi escolher **operadores que preservam a permutação**. Cruzamento de um ponto comum não funcionaria, por isso o OX foi essencial.
- O **elitismo** foi uma decisão deliberada: além de melhorar a qualidade, ele dá uma garantia testável (a aptidão nunca piora), o que facilita demonstrar o funcionamento na apresentação.
- Deixei o ciclo **parametrizável e com hooks** (`mutacao`, `callback`, `selecao`) justamente para encaixar limpo com as partes da Pessoa 4 e da Pessoa 5, sem que ninguém precise reescrever o núcleo.
- Validar a convergência contra **força bruta** (função da Pessoa 2) deu confiança de que a aptidão e os operadores estão corretos: em N pequeno, o AG chega exatamente ao melhor resultado possível.
