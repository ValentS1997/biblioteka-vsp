# Диаграммы главы 9

## Inference path

~~~mermaid
flowchart LR
    Q["Request"] --> PRE["Prefill<br/>usually compute-bound"]
    PRE --> DEC["Decode<br/>usually memory-bandwidth-bound"]
    DEC --> OUT["Output tokens"]
    PRE --> TTFT["TTFT"]
    DEC --> TPOT["TPOT"]
~~~

## Bottleneck localization

~~~mermaid
flowchart TD
    BASE["Measure baseline:<br/>TTFT · TPOT · p95/p99 · TPS · goodput · cost"] --> CLASS{"Primary bottleneck?"}
    CLASS -- "compute" --> C["Check FLOP/s · prefill · kernels · tensor parallelism"]
    CLASS -- "memory bandwidth" --> M["Check model size · precision · KV cache · HBM bandwidth"]
    CLASS -- "memory capacity / OOM" --> O["Check weights + KV cache + batch<br/>compression / partitioning"]
    C --> CHANGE["Apply one targeted change"]
    M --> CHANGE
    O --> CHANGE
    CHANGE --> RE["Remeasure same workload"]
    RE --> OK{"SLO/cost/quality improved?"}
    OK -- "yes" --> KEEP["Keep"]
    OK -- "no" --> RB["Rollback / try another layer"]
~~~

## Model optimization

~~~mermaid
flowchart TD
    MODEL["Model-level optimization"] --> SIZE["Compression<br/>quantize · distill · prune"]
    MODEL --> DEC["Decode<br/>speculative · reference · parallel"]
    MODEL --> ATTN["Attention / KV cache"]
    ATTN --> ARCH["Architecture changes"]
    ATTN --> CACHE["Paged/cache compression/quantization"]
    ATTN --> KERNEL["FlashAttention / custom kernels"]
    MODEL --> VERIFY["Quality regression required"]
~~~

## Service optimization

~~~mermaid
flowchart TD
    SERVICE["Inference service"] --> BATCH["Batching"]
    BATCH --> STATIC["Static"]
    BATCH --> DYN["Dynamic"]
    BATCH --> CONT["Continuous"]
    SERVICE --> SPLIT["Prefill / decode disaggregation"]
    SERVICE --> CACHE["Prompt / prefix cache"]
    SERVICE --> PAR["Parallelism"]
    PAR --> REP["Replica"]
    PAR --> TEN["Tensor"]
    PAR --> PIPE["Pipeline"]
    PAR --> CTX["Context / sequence"]
    SERVICE --> MET["Measure latency · goodput · cost"]
~~~

## Optimization hierarchy

~~~mermaid
flowchart LR
    M["Model"] --> H["Hardware"]
    H --> S["Service"]
    S --> U["User-visible latency / cost"]
    U --> E["Evaluation"]
    E --> M
~~~
