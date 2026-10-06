# Шпаргалка: оптимизация вывода по главе 9

Цель: сначала локализовать bottleneck, затем менять только соответствующий слой и повторно измерять latency, throughput, cost и quality.

## Symptom / problem framing

Типовые симптомы:

- высокий TTFT;
- высокий TPOT;
- хорошие p50, но плохие p95/p99;
- throughput высокий, но SLO нарушается;
- GPU utilization высокий, но система медленная;
- OOM при длинном context/batch;
- decode масштабируется хуже prefill;
- batching снижает cost, но портит latency;
- long-context workload упирается в KV cache;
- модель помещается только на несколько devices;
- после model compression throughput вырос, но quality снизилась.

## Baseline / context

Перед изменениями зафиксировать:

1. Model/version/precision.
2. Hardware/accelerator.
3. Input length distribution.
4. Output length distribution.
5. Concurrency.
6. Batch policy.
7. TTFT p50/p90/p95/p99.
8. TPOT p50/p90/p95/p99.
9. End-to-end latency.
10. Output throughput TPS.
11. RPS/RPM.
12. Goodput against SLO.
13. MFU / MBU where available.
14. Cost per request / per token.
15. Model quality baseline.

## Read-only checks

### 1. Разделить prefill и decode

Source model:

- prefill → обычно compute-bound;
- decode → обычно memory-bandwidth-bound.

Высокий TTFT при длинных inputs указывает на prefill path.  
Высокий TPOT — на decode path.

### 2. Проверить percentiles

Среднее скрывает outliers.

Минимум:

- p50;
- p90;
- p95;
- p99.

Полезно строить TTFT против input length.

### 3. Проверить throughput и goodput

Throughput:

- output TPS;
- RPS/RPM.

Goodput:

- только requests, которые удовлетворяют SLO.

Высокий throughput при низком goodput означает, что система обрабатывает много запросов, но недостаточно быстро.

### 4. Не путать GPU utilization с efficiency

`nvidia-smi` показывает active-time utilization, но не доказывает эффективное использование compute.

Дополнительные показатели:

- MFU;
- MBU.

### 5. Проверить hardware fit

Для compute-bound workload важны FLOP/s.  
Для bandwidth-bound workload — memory bandwidth.  
Для oversized model/KV cache — memory capacity.

### 6. Проверить KV-cache pressure

Без оптимизации source formula:

~~~text
KV cache bytes = 2 × B × S × L × H × M
~~~

где:

- `B` — batch size;
- `S` — sequence length;
- `L` — transformer layers;
- `H` — model dimension;
- `M` — bytes per numeric value.

KV cache растет с batch и sequence length.

## Interpretation

### Высокий TTFT, нормальный TPOT

Вероятный bottleneck: prefill/compute/input length.

Проверить:

- long inputs;
- prefill capacity;
- disaggregated prefill;
- prompt caching.

### Нормальный TTFT, высокий TPOT

Вероятный bottleneck: decode/memory bandwidth.

Проверить:

- model size/precision;
- memory bandwidth;
- speculative decoding;
- KV-cache path;
- decode resources.

### Высокий GPU utilization, низкий throughput

Не считать utilization доказательством эффективности. Проверить MFU/MBU и фактический bottleneck.

### OOM при длинном context

Проверить model weights + KV cache + batch. Рассмотреть KV-cache optimization, smaller batch, model compression or parallelism.

### Throughput растет, latency ухудшается

Обычный throughput/latency trade-off batching. Сравнивать goodput, а не только TPS.

### Quality падает после optimization

Model-level optimization затронула behavior. Откатить или перенастроить technique.

## Next action

Source-grounded sequence:

1. Measure TTFT/TPOT/latency percentiles.
2. Measure throughput/goodput/cost.
3. Classify compute vs memory-bandwidth bottleneck.
4. Check hardware capacity/bandwidth.
5. Apply lowest-risk matching optimization.
6. Remeasure.
7. If model-level optimization was used, run quality regression.
8. Keep only improvement that satisfies SLO and cost/quality constraints.

## Modifying action

### Quantization / pruning / distillation

Что меняется: model representation/weights/architecture.

Effect:

- smaller model;
- less memory/bandwidth;
- potential speedup.

Risk: output quality may change.

Verification:

- quality regression;
- TTFT/TPOT;
- throughput;
- memory;
- cost.

Rollback: previous model artifact/checkpoint — exact procedure `[Needs confirmation]`.

### Speculative decoding

Что меняется: decoding path introduces draft model.

Effect: draft tokens are generated cheaply and verified by target model.

Risk:

- low acceptance rate can reduce or negate benefit;
- extra model/runtime complexity.

Verification:

- acceptance rate;
- TPOT/end-to-end latency;
- unchanged target-model output semantics as implemented;
- total cost.

Rollback: disable speculative path — exact configuration `[Needs confirmation]`.

### KV-cache optimization

Что меняется: KV-cache representation/placement/management.

Methods in source:

- architectural reduction;
- PagedAttention;
- quantization/compression;
- selective caching.

Verification:

- memory usage;
- batch capacity;
- TPOT;
- throughput;
- long-context quality where architecture changes are involved.

Rollback: previous attention/cache configuration — `[Needs confirmation]`.

### Batching

Что меняется: request scheduling.

Effect: higher throughput/resource utilization.

Risk: additional waiting and tail latency.

Verification:

- p50/p95/p99 TTFT/latency;
- TPS/RPS;
- goodput;
- cost/request.

Rollback: previous batch policy — `[Needs confirmation]`.

### Prefill/decode disaggregation

Что меняется: phases run on different instances.

Effect: isolates compute-heavy prefill from bandwidth-heavy decode.

Risk: transfer/coordination overhead and resource imbalance.

Verification:

- TTFT;
- TPOT;
- goodput;
- inter-instance transfer overhead.

Rollback: colocated serving topology — exact deployment procedure `[Needs confirmation]`.

### Prompt/prefix caching

Что меняется: repeated prompt/context prefixes are persisted for reuse.

Effect: less repeated prefill work.

Risk: memory/storage overhead and cache-management complexity.

Verification:

- cache hit ratio `[Needs confirmation]` if implementation exposes it;
- TTFT;
- input-token processing cost;
- memory/storage usage.

Rollback: disable/clear cache according to implementation — `[Needs confirmation]`.

### Parallelism

Replica:
- increases concurrency;
- costs more hardware.

Tensor:
- splits tensor operations across devices;
- can serve models too large for one device;
- adds communication overhead.

Pipeline:
- splits model stages;
- may increase per-request latency.

Context/sequence:
- intended for long input processing.

Verification for all:
- latency;
- throughput/goodput;
- communication overhead;
- memory fit;
- cost.

Rollback: previous placement/parallelism topology — `[Needs confirmation]`.

## Verification / acceptance checks

Optimization is accepted only if:

- baseline was recorded;
- bottleneck classification is evidence-based;
- TTFT and TPOT are measured separately;
- tail latency is included;
- throughput and goodput are both considered;
- cost is measured;
- hardware resource fit is understood;
- model-level changes include quality regression;
- new bottleneck is checked after each optimization;
- result is better under the same or explicitly documented workload.

## Rollback

- Read-only profiling: `[Not applicable]`.
- Model changes: previous model artifact/checkpoint `[Needs confirmation]`.
- Scheduler/batching: previous serving config `[Needs confirmation]`.
- Parallelism/topology: previous deployment config `[Needs confirmation]`.
- Cache changes: previous cache policy `[Needs confirmation]`.

## Минимальная карта

~~~text
Inference
├─ measure
│  ├─ TTFT
│  ├─ TPOT
│  ├─ p50/p95/p99
│  ├─ TPS/RPS
│  ├─ goodput
│  └─ MFU/MBU
├─ bottleneck
│  ├─ compute
│  ├─ memory bandwidth
│  └─ memory capacity
├─ model
│  ├─ compression
│  ├─ decoding
│  └─ attention/KV cache
├─ kernels/compilers
└─ service
   ├─ batching
   ├─ prefill/decode split
   ├─ prompt cache
   └─ parallelism
~~~
