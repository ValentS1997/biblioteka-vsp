# Команды, формулы, инструменты и действия главы 9

Source policy: `rag_only`.

## Read-only command

### `nvidia-smi`

Class: `read-only`.

Source role: NVIDIA System Management Interface for GPU monitoring.

Important limitation from the chapter: reported GPU utilization is the percentage of time the GPU is actively processing work; it is not equivalent to MFU and does not prove efficient use of available FLOP/s.

No additional command-line flags are introduced because the chapter does not provide them.

## Source-confirmed formulas

### End-to-end response time

Class: `read-only calculation`.

~~~text
response_time ≈ TTFT + TPOT × output_token_count
~~~

### KV-cache memory

Class: `read-only calculation`.

~~~text
KV_cache_bytes = 2 × B × S × L × H × M
~~~

- `B` — batch size
- `S` — sequence length
- `L` — number of transformer layers
- `H` — model dimension
- `M` — bytes per cached numeric value

### Used memory bandwidth

Class: `read-only calculation`.

~~~text
used_bandwidth ≈ parameters × bytes_per_parameter × tokens_per_second
~~~

### MBU

Class: `read-only calculation`.

~~~text
MBU =
(parameters × bytes_per_parameter × tokens_per_second)
/
theoretical_memory_bandwidth
~~~

### MFU

Class: `read-only calculation`.

Source definition: ratio of observed model throughput to theoretical maximum throughput at processor peak FLOP/s.

## Performance metrics

Source-confirmed:

- TTFT;
- TPOT;
- TBT;
- ITL;
- total response time;
- p50;
- p90;
- p95;
- p99;
- TPS;
- RPS;
- RPM;
- goodput;
- GPU utilization;
- MFU;
- MBU;
- cost per request / token workload.

## Profiling / hardware tools

| Tool / concept | Class | Source role |
|---|---|---|
| NVIDIA Nsight | read-only profiling | roofline analysis; compute vs memory-bandwidth bottleneck |
| CUDA | workload-generating / state-changing code path | NVIDIA GPU kernel programming |
| Triton | workload-generating / state-changing code path | custom GPU kernels |
| ROCm | workload-generating / state-changing runtime/code path | AMD GPU compute stack |

Exact CLI syntax is not supplied by the chapter.

## Kernel optimization actions

Source-confirmed:

- vectorization;
- parallelization;
- loop tiling/blocking;
- operator fusion.

Class: `state-changing code optimization`.

Effect: changes generated/executed kernels and memory-access pattern.

Risk: hardware-specific behavior and engineering complexity.

Verification:

- latency;
- throughput;
- correctness;
- hardware utilization.

Rollback: previous kernel/compiler implementation — `[Needs confirmation]`.

## Compiler tools

Source-confirmed:

- `torch.compile`;
- Apache TVM;
- MLIR;
- XLA / OpenXLA;
- TensorRT compiler.

### `torch.compile`

Class: `workload-generating / compilation action`.

The chapter explicitly describes calling `torch.compile` to compile a model into more efficient kernels. Exact Python signature/arguments are not supplied, so no runnable snippet is added.

Source practical sequence:

~~~text
torch.compile
→ INT8 weight quantization
→ INT4 weight quantization
→ speculative decoding
~~~

The source notes that the cited experiment did not make clear how these steps affected output quality.

## Model-level optimization actions

### Quantization

Class: `state-changing model representation`.

Effect: fewer bits per weight, lower memory footprint and bandwidth demand.

Risk: quality change.

Verification: quality + latency + throughput + memory + cost.

Rollback: prior precision/model artifact — `[Needs confirmation]`.

### Distillation

Class: `state-changing training workflow`.

Effect: train smaller model to imitate larger one.

Verification: target-task quality + inference performance.

Rollback: previous model artifact — `[Needs confirmation]`.

### Pruning

Class: `state-changing model structure/weights`.

Effect: remove nodes or set low-utility weights to zero; can reduce memory/compute.

Risk: performance loss; sparse speedups depend on hardware support.

Verification: quality + actual wall-clock performance + memory.

Rollback: unpruned checkpoint — `[Needs confirmation]`.

### Speculative decoding

Class: `workload-generating serving strategy`.

Source loop:

~~~text
draft model generates K tokens
→ target model verifies in parallel
→ accept longest valid prefix
→ target generates next token
→ repeat
~~~

Verification: acceptance rate + TPOT/latency + total cost.

### Reference-based decoding

Class: `workload-generating serving strategy`.

Purpose: reuse matching tokens from input/context instead of regenerating them.

Useful where output overlaps strongly with input.

### Parallel decoding

Class: `workload-generating / model-serving strategy`.

Source examples:

- Lookahead;
- Medusa;
- Jacobi-style verification.

No CLI syntax is supplied.

## Attention / KV-cache tools and methods

Source-confirmed:

- KV cache;
- local/windowed attention;
- multi-query attention;
- grouped-query attention;
- cross-layer key/value sharing;
- PagedAttention;
- KV-cache quantization;
- adaptive KV-cache compression;
- selective key/value caching;
- FlashAttention.

### PagedAttention

Class: `state-changing serving-memory strategy`.

Effect: splits KV cache into non-contiguous blocks to reduce fragmentation and improve memory sharing.

Verification: memory use + batch capacity + throughput + latency.

Rollback: previous KV-cache manager — `[Needs confirmation]`.

### FlashAttention

Class: `state-changing kernel path`.

Effect: hardware-aware fused attention computation.

Verification: correctness + latency/throughput on target hardware.

Rollback: previous attention kernel — `[Needs confirmation]`.

## Service-level optimization

### Static batching

Class: `state-changing scheduler policy`.

Waits for fixed batch size. Risk: request waiting time.

### Dynamic batching

Class: `state-changing scheduler policy`.

Runs when batch fills or time window expires.

### Continuous batching

Class: `state-changing scheduler policy`.

Completed requests leave immediately; new requests can fill freed slots.

Verification for batching:

- TTFT/latency percentiles;
- throughput;
- goodput;
- cost.

Rollback: previous scheduler policy — `[Needs confirmation]`.

### Prefill/decode disaggregation

Class: `state-changing serving topology`.

Runs prefill and decode on separate instances.

Verification:

- TTFT;
- TPOT;
- transfer overhead;
- goodput;
- resource ratio.

Rollback: colocated topology — `[Needs confirmation]`.

### Prompt/prefix caching

Class: `state-changing cache policy`.

Caches overlapping prompt/context segments for reuse.

Verification:

- TTFT;
- repeated input-token work;
- storage/memory overhead;
- cost.

Rollback: disable cache / restore prior cache policy — `[Needs confirmation]`.

## Parallelism

| Method | Class | Role |
|---|---|---|
| replica parallelism | state-changing serving topology | more concurrent requests |
| tensor parallelism | state-changing serving topology | split tensor operations across devices |
| pipeline parallelism | state-changing serving topology | split model stages across devices |
| context parallelism | state-changing serving topology | split input sequence across devices |
| sequence parallelism | state-changing serving topology | distribute sequence-related operators |

Verification:

- model fit;
- TTFT/TPOT;
- throughput/goodput;
- communication overhead;
- cost.

Rollback: previous topology — `[Needs confirmation]`.

## Operational boundary

- No unsupported shell commands were added.
- Only `nvidia-smi` is presented as a concrete CLI command because it is explicitly named as the NVIDIA monitoring tool in the chapter.
- Other tools are listed without invented flags or installation instructions.
- Hardware/model/service optimization must be remeasured under the same workload.
