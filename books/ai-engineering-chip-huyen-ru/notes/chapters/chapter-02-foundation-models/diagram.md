# Диаграммы главы 2

## Откуда берется поведение базовой модели

~~~mermaid
flowchart TD
    DATA["Training data<br/>language · domain · quality · quantity"] --> PRE["Pretraining"]
    DESIGN["Model design<br/>architecture · parameters · tokens · FLOP"] --> PRE
    PRE --> BASE["Pretrained foundation model"]
    BASE --> SFT["SFT<br/>demonstration data"]
    SFT --> PREF["Preference finetuning<br/>RLHF / DPO / RLAIF"]
    PREF --> READY["Post-trained model"]
    READY --> SAMPLE["Sampling / inference<br/>temperature · top-k · top-p · stop"]
    SAMPLE --> OUTPUT["Output"]
    OUTPUT --> RISKS["Probabilistic effects<br/>inconsistency · hallucinations"]
~~~

Эта схема отражает логику главы: наблюдаемый output формируется цепочкой решений от данных и архитектуры до post-training и sampling.

## Выбор и адаптация для приложения

~~~mermaid
flowchart TD
    NEED["Application requirement"] --> DATAFIT{"Training-data fit?<br/>language / domain"}
    DATAFIT -- "нет / неизвестно" --> MODELALT["Искать другую или domain/language-specific model"]
    DATAFIT -- "да" --> SCALE["Compare architecture + scale<br/>parameters · training tokens · FLOP"]
    MODELALT --> SCALE
    SCALE --> POST{"Post-training подходит?"}
    POST -- "нет" --> ADAPT["SFT / preference tuning<br/>если оправдано"]
    POST -- "да" --> INFER["Set sampling baseline"]
    ADAPT --> INFER
    INFER --> STRUCT{"Structured output required?"}
    STRUCT -- "нет" --> REL["Measure consistency / hallucination risk"]
    STRUCT -- "да" --> STRAT["prompt → check/regenerate → post-process<br/>→ constrained sampling → fine-tuning"]
    STRAT --> REL
    REL --> MEASURE["Evaluate on target workload"]
~~~

## Сэмплирование и structured output

~~~mermaid
flowchart LR
    LOGITS["logits"] --> TEMP["temperature"]
    TEMP --> FILTER["top-k / top-p"]
    FILTER --> TOKEN["sample next token"]
    TOKEN --> STOP{"stop?"}
    STOP -- "нет" --> LOGITS
    STOP -- "да" --> RESULT["generated result"]
    RESULT --> VALID{"format valid?"}
    VALID -- "да" --> USE["use output"]
    VALID -- "нет" --> FIX["regenerate / post-process / constrain / fine-tune"]
~~~

Конкретный troubleshooting/rollback workflow для production-систем глава не задает.
