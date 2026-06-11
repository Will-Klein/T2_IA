# Decisões — Módulo Heurística

## Codificação

Representamos a solução como uma permutação de tamanho N (índices 0 até N-1).
O índice representa o aluno da Escola A, e o valor naquele índice representa o aluno da Escola B com quem ele é pareado.

Exemplo com N=4: `[3, 0, 1, 2]` → A1-B4, A2-B1, A3-B2, A4-B3

Optamos por permutação porque ela garante naturalmente que cada aluno aparece exatamente uma vez, sem repetição e sem solução inválida.

## Decodificação

Percorremos a permutação e convertemos cada par (índice, valor) em texto legível no formato "Ai-Bj" (1-based para facilitar a leitura).

## Função de Aptidão

Para cada par (Ai, Bj), somamos a posição de preferência de Ai por Bj (`escola_a[i][j]`) com a posição de preferência de Bj por Ai (`escola_b[j][i]`). Quanto menor essa soma, melhor a solução.

Como o AG precisa maximizar, usamos a fórmula:

```
aptidao = 2·N² − custo_total
```

O intervalo vai de 0 (pior caso) até 2·N·(N−1) (melhor caso).

## Aptidão Normalizada

Dividimos a aptidão pelo valor máximo possível, resultando em um valor entre 0 e 1. Isso permite comparar a qualidade de soluções entre arquivos com N diferentes.

## Força Bruta

Implementamos uma função que enumera todas as N! permutações e retorna a melhor encontrada. Usamos apenas para validar que a função de aptidão está correta, limitada a N ≤ 8 por desempenho.
