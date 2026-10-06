# Команды, формулы и инструменты главы 7

Глава 7 не содержит shell-команд или универсального CLI-runbook. Ниже приведены только source-confirmed formulas, techniques, platforms и configuration actions.

## Shell / CLI commands

`[Not applicable]`

Не добавляются команды запуска LLaMA-Factory, PEFT, Axolotl, DeepSpeed и других tools: CLI syntax в chapter RAG не приведен.

## Memory formulas / calculations

### Inference weights

Класс: `read-only`.

~~~text
weight_memory = N × M
~~~

- `N` — number of model parameters;
- `M` — bytes per parameter.

Source example: 13B parameters × 2 bytes = 26 GB for weights.

Approximation used in the chapter for some inference workloads:

~~~text
inference_memory ≈ N × M × 1.2
~~~

Source example: 13B × 2 bytes × 1.2 = 31.2 GB.

### Training memory

Класс: `read-only`.

~~~text
training_memory =
model_weights
+ activations
+ gradients
+ optimizer_states
~~~

For Adam, source logic counts:

~~~text
per trainable parameter:
1 gradient + 2 optimizer-state values
~~~

Source example:

~~~text
13B trainable params × 3 values × 2 bytes = 78 GB
~~~

For 1B trainable params with the same assumptions:

~~~text
1B × 3 × 2 bytes = 6 GB
~~~

These are approximate component calculations, not a universal hardware guarantee.

## Memory-reduction techniques

| Technique | Class | Effect | Risk / trade-off |
|---|---|---|---|
| freeze parameters | state-changing training config | fewer trainable parameters | may reduce adaptation capacity |
| PEFT | state-changing training config | near-full-finetuning quality with far fewer trainable params in supported cases | method/config dependent |
| gradient checkpointing | state-changing training config | lower activation memory | more recomputation/training time |
| quantization | state-changing model/config | fewer bits per value | possible quality loss/conversion overhead |
| mixed precision | state-changing training config | lower memory/compute for selected operations | training is sensitive to precision |
| CPU offload | state-changing runtime config | move excess data from GPU memory to CPU | added transfer/runtime overhead |

## Numeric representations

Source-confirmed formats:

- FP64;
- FP32;
- FP16;
- BF16;
- TF32;
- INT8;
- INT4;
- FP8;
- FP4.

Important source rule: load a model in the numeric representation it is intended for; arbitrary dtype conversion can materially degrade quality.

## Quantization modes

| Method | Class | Purpose |
|---|---|---|
| PTQ | state-changing model representation | quantize after training for cheaper inference |
| QAT | workload-generating / state-changing training | train while simulating low precision to preserve low-precision inference quality |
| low-precision training | workload-generating | reduce memory/compute during training |
| mixed-precision training | workload-generating | combine high/low precision for stability and efficiency |

## PEFT methods/tools

Source-confirmed PEFT categories:

- adapter-based methods;
- soft-prompt methods.

Adapter examples:

- Houlsby-style adapters;
- LoRA;
- BitFit;
- IA3;
- LongLoRA.

## LoRA configuration

Source-confirmed update:

~~~text
W' = W + (α / r) W_AB
W_AB = A × B
~~~

where:

- `W` — frozen base weight matrix;
- `A` and `B` — trainable low-rank matrices;
- `r` — LoRA rank;
- `α` — scaling hyperparameter.

Common transformer target matrices named in the chapter:

- `Wq`;
- `Wk`;
- `Wv`;
- `Wo`.

Class: `state-changing training configuration`.

Verification:

- trainable parameter count;
- task evaluation;
- memory usage;
- merged-model inference behavior.

Rollback: previous adapter/base configuration — `[Needs confirmation]`.

## QLoRA

Source-confirmed characteristics:

- 4-bit `NF4` storage for base weights;
- dequantization to `BF16` for forward/backward computation;
- paged optimizers for CPU/GPU memory movement under pressure.

Class: workload-generating / state-changing training configuration.

Risk: quantization/dequantization adds overhead and may increase training time.

## Model merging methods

Source-confirmed methods/concepts:

- linear combination / averaging;
- task vectors / delta parameters;
- SLERP;
- TIES;
- DARE;
- layer stacking / passthrough / frankenmerging;
- concatenation.

Operational note from the chapter: concatenation is not recommended as a memory-saving technique because parameter count becomes the sum of merged components.

## Finetuning platforms

Source-confirmed examples:

- LLaMA-Factory;
- unsloth;
- Hugging Face PEFT;
- Axolotl;
- LitGPT.

Distributed training examples:

- DeepSpeed;
- PyTorch Distributed;
- ColossalAI.

No CLI invocation syntax is provided by the chapter.

## Practical training tactics

### Progression

Class: workload-generating.

1. Test finetuning code on the cheapest/fastest model.
2. Validate data on a mid-level model.
3. Test performance ceiling on the strongest affordable model.
4. Run broader comparison to choose cost/performance trade-off.

### Distillation path

Class: workload-generating.

1. Start with small dataset + strongest affordable model.
2. Use adapted strong model to generate more training data.
3. Train a cheaper model on expanded data.

## Hyperparameters

### Learning rate

Source interpretation:

- oscillating loss → likely too high;
- stable but very slow decline → likely too low;
- increase until highest value that keeps loss stable.

The chapter mentions experimentation commonly across approximately `1e-7` to `1e-3`, while noting there is no universal optimum.

### Batch size

Larger batch:

- can provide more stable updates;
- requires more memory.

Source notes that very small batches, e.g. below 8, may be unstable.

### Gradient accumulation

Class: workload-generating training strategy.

Purpose: accumulate gradients over several batches before updating weights when physical batch size is memory-limited.

### Epochs

Source examples:

- millions of examples: 1–2 epochs may be enough;
- thousands of examples: improvement may continue after 4–10 epochs.

Use train/validation loss divergence to detect overfitting.

### Prompt-loss weight

For instruction finetuning:

- 100% → prompt and answer contribute equally;
- 0% → train only on answer tokens;
- chapter notes 10% as a common default example.

## Operational boundary

- No external CLI/API syntax added.
- Hardware compatibility is not inferred from approximate formulas.
- Model/platform versions are not updated beyond source content.
- All listed techniques/tools are source-confirmed by chapter RAG.
