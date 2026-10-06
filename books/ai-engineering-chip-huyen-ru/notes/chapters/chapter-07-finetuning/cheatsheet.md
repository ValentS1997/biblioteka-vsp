# Шпаргалка: дообучение по главе 7

Цель: применять finetuning только к тем failure modes, где изменение весов оправдано, и заранее учитывать memory/data/compute budget.

## Symptom / problem framing

Типовые симптомы:

- модели не хватает приватной или актуальной информации;
- модель знает нужные факты, но стабильно нарушает формат/стиль/behavior;
- few-shot prompt становится слишком длинным и дорогим;
- full finetuning не помещается в available GPU memory;
- quantized model теряет качество;
- LoRA дешевле, но не достигает нужной quality;
- sequential multi-task finetuning ухудшает предыдущие навыки;
- training loss нестабилен или не сходится;
- validation loss растет, пока training loss продолжает падать.

## Baseline / context

Перед дообучением зафиксировать:

1. Evaluation criteria и baseline.
2. Failure taxonomy:
   - missing information;
   - stale information;
   - behavioral failure;
   - format/style/safety failure.
3. Prompt/few-shot baseline.
4. RAG baseline, если проблема информационная.
5. Base model/version.
6. Dataset size/quality.
7. Available GPU/CPU memory.
8. Numeric format.
9. Finetuning method.
10. Trainable parameter count.
11. Hyperparameters.
12. Training/validation losses.
13. Inference cost/latency after adaptation.

## Read-only checks

### 1. Определить, нужен ли finetuning

Если проблема — отсутствие/устаревание знаний:

- сначала RAG.

Если проблема — устойчивое поведение модели:

- finetuning становится кандидатом.

Дообучение и RAG можно комбинировать.

### 2. Проверить memory budget

Approximate inference-weight memory:

~~~text
weights ≈ N × M
~~~

где:

- `N` — number of parameters;
- `M` — bytes per parameter.

Для некоторых scenarios глава использует грубую оценку:

~~~text
inference memory ≈ N × M × 1.2
~~~

Training:

~~~text
training memory =
weights
+ activations
+ gradients
+ optimizer states
~~~

Для Adam: gradient + два optimizer-state values на каждый trainable parameter.

### 3. Проверить число trainable parameters

Если full finetuning не помещается:

- partial finetuning;
- PEFT;
- LoRA/adapter methods;
- quantization;
- gradient checkpointing;
- CPU offload — если это поддерживает выбранная platform.

### 4. Проверить numeric representation

Не загружать модель в произвольном dtype.

Проверить intended format:

- FP32;
- FP16;
- BF16;
- INT8/INT4;
- other model-specific representation.

Неверный format может заметно изменить quality.

### 5. Проверить LoRA configuration

Зафиксировать:

- target matrices;
- rank `r`;
- scaling `α`;
- trainable parameter count;
- base model dtype;
- whether adapter is merged for inference.

### 6. Проверить training dynamics

Learning rate:

- oscillating loss → rate, вероятно, слишком высокая;
- loss стабильна, но снижается слишком медленно → rate, вероятно, слишком низкая.

Epochs:

- train + validation losses снижаются → обучение еще может быть полезно;
- train loss ↓, validation loss ↑ → overfitting; сократить epochs/изменить training setup.

## Interpretation

### Missing/stale knowledge

Не считать это автоматически аргументом за finetuning. По логике главы это типичная RAG-задача.

### Correct facts, wrong behavior/format

Более сильный кандидат на finetuning.

### Full finetuning не помещается

Снизить trainable parameter count и/или memory per value, а не начинать с произвольного hardware scaling.

### LoRA почти достигает baseline

Сравнить gain от full finetuning с дополнительными compute/data/ops costs.

### Quantization экономит memory, но обучение стало медленнее

Это допустимый trade-off: conversion/dequantization могут добавлять compute overhead.

### Training loss нестабилен

Проверить learning rate и effective batch size.

### Validation loss растет

Признак overfitting в описанной source logic.

## Next action

Рекомендуемый chapter flow:

1. Определить evaluation criteria.
2. Prompt-only baseline.
3. Добавить few-shot examples.
4. При information failures — простой RAG.
5. При необходимости улучшить retrieval.
6. При persistent behavior failures — finetuning.
7. При memory limits — PEFT/LoRA + quantization/checkpointing.
8. Сравнить adapted model с baseline.
9. Измерить quality + cost + latency.
10. Сохранять configuration и training artifacts для repeatability.

## Modifying action

### Full finetuning

Что меняется: все или большая часть model weights.

Risk:

- высокий memory/data/compute cost;
- может ухудшить другие capabilities;
- выше operational burden.

Verification:

- fixed evaluation pipeline;
- cross-task regression;
- training/validation losses;
- inference cost/latency.

Rollback: возврат к предыдущей base/model checkpoint — exact lifecycle `[Needs confirmation]`.

### PEFT / LoRA

Что меняется: небольшое число adapter/low-rank parameters; base weights остаются frozen.

Effect: значительно меньше trainable parameters.

Risk:

- может не достигнуть full-finetuning quality;
- нужна корректная architecture/target-matrix configuration.

Verification:

- task metrics;
- trainable parameter count;
- memory use;
- adapter merge/inference test.

Rollback: disable/remove adapter or revert to previous adapter version — exact mechanism `[Needs confirmation]`.

### Quantization / QLoRA

Что меняется: numeric representation base weights/operations.

Effect: memory reduction.

Risk:

- quality loss;
- quant/dequant overhead;
- training can become more complex.

Verification:

- model-quality regression;
- measured memory;
- training/inference latency.

Rollback: restore higher-precision checkpoint/config — `[Needs confirmation]`.

### Model merging

Что меняется: parameters/layers/adapters нескольких models объединяются.

Risk:

- interference between tasks;
- experimental behavior;
- evaluation required across all source capabilities.

Verification:

- per-task metrics;
- regression set;
- memory/inference cost.

Rollback: retain and redeploy source models/adapters — exact deployment procedure `[Needs confirmation]`.

## Verification / acceptance checks

Finetuning workflow соответствует логике главы, если:

- evaluation pipeline существовал до finetuning;
- failure mode оправдывает изменение weights;
- RAG рассмотрен для information failures;
- base model/version зафиксированы;
- dataset quality/size известны;
- memory budget рассчитан;
- trainable parameters известны;
- dtype/quantization format известны;
- learning rate/batch/epochs логируются;
- train + validation losses анализируются;
- adapted model сравнивается с baseline на тех же criteria;
- regression по другим задачам проверена.

## Rollback

- Read-only evaluation: `[Not applicable]`.
- Full finetuning: checkpoint/model rollback `[Needs confirmation]`.
- LoRA/adapter update: adapter-version rollback `[Needs confirmation]`.
- Quantization change: precision/checkpoint rollback `[Needs confirmation]`.
- Hyperparameter change: rerun from previous controlled configuration; exact artifact management `[Needs confirmation]`.

## Минимальная карта памяти

~~~text
Adaptation
├─ prompt
├─ few-shot
├─ RAG
│  └─ missing / stale information
└─ finetuning
   ├─ behavior / format / safety
   ├─ memory constraints
   │  ├─ trainable params
   │  ├─ dtype / quantization
   │  └─ activations
   ├─ PEFT
   │  ├─ adapters
   │  └─ soft prompts
   ├─ LoRA / QLoRA
   ├─ model merging
   └─ hyperparameters
~~~
