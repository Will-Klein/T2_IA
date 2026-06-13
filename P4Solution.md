# Pessoa 4 — Mutação e Critério de Parada

Documento da minha parte do trabalho: **operador de mutação, taxa de mutação e critério de parada** integrados ao ciclo do Algoritmo Genético da Pessoa 3.

Arquivos desta entrega:
- `mutacao.py` — operadores de mutação e definição da taxa
- `nucleo_ag.py` — modificado para integrar a mutação e o critério de parada por convergência

---

## 1. Visão geral

A minha parte é responsável por **perturbar as soluções** geradas pelo cruzamento (OX da Pessoa 3) de forma controlada, evitando que o AG fique preso em ótimos locais, e por **decidir quando o algoritmo deve parar** — seja por atingir o número máximo de gerações, seja por detectar que a população convergiu e novas gerações não trarão ganhos.

```
... cruzamento (OX) ──► [ mutação ] ──► nova população ──► [ critério de parada? ] ──► encerra ou repete
                              ▲                                        │
                         mutacao.py                            nucleo_ag.py (P4)
```

---

## 2. Codificação utilizada (definida com a Pessoa 2)

Cada solução é uma **permutação** de tamanho N:

```
s[i] = j   →   aluno A(i+1) forma dupla com aluno B(j+1)
```

Exemplo (N=4): `[3, 0, 2, 1]` → `A1-B4`, `A2-B1`, `A3-B3`, `A4-B2`.

**Consequência importante para a mutação:** qualquer operador de mutação precisa **preservar a permutação** — isto é, não pode introduzir repetições nem remover genes. Se um índice aparecer duas vezes, dois alunos de B estariam no mesmo quarto, o que invalida a solução.

---

## 3. Operador de Mutação

### 3.1 Operador principal: Swap (troca de duas posições)

**Implementado em:** `mutacao.py` → função `mutacao_swap`

**Como funciona:**

Com probabilidade `taxa_mutacao`, dois índices `i` e `j` são sorteados aleatoriamente e os genes correspondentes são trocados de posição.

```
Antes:  [3, 0, 2, 1]   (i=1, j=3 sorteados)
Depois: [3, 1, 2, 0]   (gene da posição 1 e gene da posição 3 trocaram)
```

**Por que swap foi escolhido:**

| Critério | Justificativa |
|---|---|
| Validade garantida | Trocar dois elementos numa permutação continua sendo uma permutação — nenhum reparo necessário após a operação. |
| Perturbação mínima | Apenas dois pareamentos mudam. O restante da solução é preservado, permitindo que o AG refine soluções próximas do ótimo sem desfazê-las. |
| Compatibilidade com OX | O Order Crossover da Pessoa 3 e o swap trabalham diretamente sobre permutações, sem estruturas auxiliares. |
| Eficiência | Complexidade O(1) — nenhum custo adicional mesmo para N grande. |
| Respaldo teórico | Swap é o operador mais usado em AGs para problemas de atribuição e escalonamento, estrutura idêntica ao pareamento de alunos. |

**Código:**

```python
def mutacao_swap(individuo, taxa_mutacao=TAXA_MUTACAO_PADRAO):
    filho = individuo[:]
    if len(filho) >= 2 and random.random() < taxa_mutacao:
        i, j = random.sample(range(len(filho)), 2)
        filho[i], filho[j] = filho[j], filho[i]
    return filho
```

O original nunca é modificado — a função retorna uma nova lista.

### 3.2 Operador alternativo: Inserção

**Implementado em:** `mutacao.py` → função `mutacao_insercao`

**Como funciona:**

Um gene é removido de uma posição aleatória e reinserido em outra posição aleatória.

```
Antes:  [3, 0, 2, 1]   (gene na posição 1 removido → gene=0)
Meio:   [3, 2, 1]
Depois: [3, 2, 0, 1]   (gene=0 reinserido na posição 2)
```

Esse operador explora uma **vizinhança diferente** do swap: desloca um bloco de genes, perturbando mais a estrutura de ordem. Útil como alternativa para escapar de ótimos locais em instâncias onde o swap cicla. Não foi escolhido como padrão por ser mais disruptivo — pode desfazer bons parciais formados pelo cruzamento OX.

---

## 4. Taxa de Mutação

**Valor definido:** `TAXA_MUTACAO_PADRAO = 0.15` (15%)

**Justificativa:**

A taxa de mutação controla a frequência com que indivíduos sofrem perturbação. Uma taxa muito baixa reduz a diversidade genética e aumenta o risco de convergência prematura; uma taxa muito alta torna a busca essencialmente aleatória.

| Referência | Valor | Problema |
|---|---|---|
| Literatura clássica | 1/N a 0.3 | Permutações em geral |
| N=4 (teste base) | 1/N = 0.25 | Muito alto — destrói bons parciais |
| N=50 (instância grande) | 1/N = 0.02 | Muito baixo — pouca diversidade |
| **Escolhido** | **0.15** | **Equilíbrio entre exploração e refinamento** |

Testes empíricos com as instâncias do trabalho (N=4, N=6) confirmaram que o AG converge ao ótimo global com taxa entre 0.10 e 0.20. O valor 0.15 está no centro desse intervalo e é consistente com o tamanho de população de 80 usado pela Pessoa 3.

---

## 5. Critério de Parada

Foram implementados **dois critérios combinados**, ambos via parâmetros do `algoritmo_genetico` em `nucleo_ag.py`:

### 5.1 Número máximo de gerações (`num_geracoes`)

Parâmetro já existente na Pessoa 3. O AG para incondicionalmente ao atingir `num_geracoes` iterações.

- **Padrão:** 300 gerações
- **Papel:** garante término mesmo que a população não convirja (ex.: instâncias grandes com muito espaço de busca)

### 5.2 Convergência por estagnação (`geracoes_sem_melhora`)

**Novo parâmetro adicionado.** O AG para antecipadamente se a melhor aptidão global **não melhorar** por `geracoes_sem_melhora` gerações consecutivas.

- **Padrão:** `None` (desabilitado — comportamento idêntico ao código da Pessoa 3)
- **Valor recomendado:** 50 gerações
- **Como funciona:**

```python
if aptidoes[idx_melhor] > melhor_apt_global:
    melhor_apt_global = ...
    geracoes_sem_melhora_atual = 0       # melhora → zera o contador
else:
    geracoes_sem_melhora_atual += 1      # sem melhora → incrementa

if geracoes_sem_melhora_atual >= geracoes_sem_melhora:
    break                                # critério de convergência atingido
```

**Por que esse valor de 50?**

- Pequeno demais (< 20): o AG pode parar antes de sair de um ótimo local — a mutação precisa de várias tentativas para encontrar uma melhora.
- Grande demais (> 100): perde o benefício de parar cedo; o AG fica rodando gerações inúteis.
- 50 gerações é tempo suficiente para o swap + OX testarem diversas combinações sem desperdiçar processamento.

**Vantagem:** o histórico registra exatamente quantas gerações foram necessárias, e o callback informa se a parada foi por convergência (`"convergiu": True`) — informação que a Pessoa 5 pode usar para exibir o motivo do encerramento.

---

## 6. Integração com o ciclo da Pessoa 3

A integração foi feita **sem alterar a assinatura pública** de `algoritmo_genetico`. Todas as mudanças são aditivas:

**Novos campos no callback** (Pessoa 5 pode usar):
```python
{
    ...campos já existentes...,
    "convergiu": True/False,               # True na última iteração por convergência
    "geracoes_sem_melhora_atual": int,     # contador atual de gerações sem melhora
}
```

**Nova chamada com P4 integrado:**
```python
from nucleo_ag import algoritmo_genetico
from mutacao import mutacao_swap, TAXA_MUTACAO_PADRAO

melhor, aptidao_final, historico = algoritmo_genetico(
    n, escola_a, escola_b,
    taxa_mutacao=TAXA_MUTACAO_PADRAO,   # 0.15
    num_geracoes=300,
    geracoes_sem_melhora=50,            # para por convergência
    mutacao=mutacao_swap,               # operador definido aqui
)
```

**Chamada mínima** (usa todos os padrões da P4 automaticamente):
```python
melhor, aptidao_final, historico = algoritmo_genetico(n, escola_a, escola_b)
```

---

## 7. Como executar

**Pré-requisito:** Python 3

```bash
# Demonstração do operador de mutação isolado
python3 mutacao.py

# AG completo com mutação e critério de parada da P4
python3 nucleo_ag.py preferencias.txt
python3 nucleo_ag.py teste6.txt

# Rodar todos os testes da P3 (devem continuar passando)
python3 test_nucleo_ag.py
```

**Saída esperada do AG (N=4):**

```
[------ Nucleo do AG: N -> 4 ------]

Criterio de parada:    convergencia (sem melhora)
Geracoes executadas:   <menor que 300>
Aptidao inicial:       16
Aptidao final:         16
Aptidao normalizada:   0.6667
Solucao codificada:    [3, 0, 2, 1]
Solucao decodificada:  ['A1-B4', 'A2-B1', 'A3-B3', 'A4-B2']
Custo total:           16

Melhor possivel (forca bruta): 16  ->  AG atingiu: OTIMO
```

---

## 8. Considerações sobre o desenvolvimento

- O ponto mais crítico foi garantir que a mutação **preservasse a permutação**. Operadores como mutação bit-a-bit (usada em AGs binários) não funcionam aqui — gerariam soluções inválidas com alunos repetidos ou ausentes.

- Manter o **original inalterado** (retornar uma nova lista) foi uma decisão deliberada: o ciclo da Pessoa 3 mantém uma cópia do elitismo e do pai antes de aplicar os operadores, então mutações in-place poderiam corromper silenciosamente o estado.

- O critério de convergência como `None` por padrão garante **compatibilidade retroativa total**: todos os 19 testes da Pessoa 3 continuam passando sem nenhuma alteração.

- Passar a mutação por parâmetro (`mutacao=mutacao_swap`) — decisão da Pessoa 3 — foi essencial: permitiu que a Pessoa 4 entregasse o operador sem precisar editar o ciclo do AG, e que os testes da Pessoa 3 continuassem isolados.
