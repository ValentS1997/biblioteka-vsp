# Глава 10 — R-пример АСД и operational boundary

**Provenance:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 41–42; RAG `e0041:c01–c04`, `e0042:c01–c05`.

## Infrastructure commands

**[Not applicable].** Глава не содержит команд изменения firewall/SIEM/endpoint/production systems. Единственные исполняемые фрагменты относятся к учебному R-анализу.

## Package installation — как извлечено

В `e0042:c03` источник предлагает:

```text
install.packages(«LearnBayes»).
```

В этой записи используются типографские кавычки и завершающая точка; как literal R command она требует отдельной сверки. Не нормализуется в canonical artifact.

## Source R sequence

### Load package

```r
library(LearnBayes)
```

### Select prior beta parameters

Источник:

```text
beta.par <– beta.select(list(p=0.5, x=0.40), list(p=0.90, x=.60))
```

Затем:

```r
triplot(beta.par, c(3,7))
```

Source output для `beta.par`:

```text
[1] 4.31 6.30
```

### Update with 5 successes / 30 failures

```text
triplot(beta.par, c(5,30))
```

### Posterior parameters and 90% interval

Источник `e0042:c05`:

```text
beta.post.par <– beta.par + c(5, 30)

qbeta(c(0.05, 0.95), beta.post.par[1], beta. post.par[2])
```

Source output:

```text
[1] 0.1148617 0.3082632
```

В variable reference `beta. post.par[2]` есть пробел; не исправлять молча.

### Posterior sampling — source line

```text
post.sample <– rbeta(1000, beta.post.par[1], beta.post.par[1], beta.post.par[2])
```

Следом:

```r
quantile(post.sample, c(0.05, 0.95))
```

Source output:

```text
5%        95%
0.1178466 0.3027499
```

Строка `rbeta(...)` внутренне не согласуется с предыдущим использованием двух posterior beta parameters: `beta.post.par[1]` повторяется, а `beta.post.par[2]` передаётся дополнительным аргументом. **Не исправлять/исполнять как verified code**, см. `source-findings.md`.

### Predict next 200 audits

```text
num <– 200
sample <– 0:num
pred.probs <– pbetap(beta.post.par, num, sample)
discint(cbind(sample, pred.probs), 0.90)
```

Source output:
- returned probability: `0.9084958`;
- set of successes: **17…56**.

## Classification

| Действие | Класс |
|---|---|
| Локальный R calculation на учебных данных | `workload-generating` |
| Установка package | локально `state-changing` для R environment |
| Изменение SIEM/logging/data-mart pipeline | `state-changing`, но команды в главе отсутствуют |
| Автоматизация response action | potentially high-impact; source gives concept only |

## Verification before execution

До практического запуска source code:
1. сверить typographic operators/quotes;
2. сверить `qbeta` variable name;
3. отдельно проверить `rbeta` argument list;
4. закрепить package/R version;
5. использовать test dataset;
6. проверить outputs независимым расчётом.

Глава не даёт validated environment lockfile, package version или reproducibility seed: **[Needs confirmation]**.
