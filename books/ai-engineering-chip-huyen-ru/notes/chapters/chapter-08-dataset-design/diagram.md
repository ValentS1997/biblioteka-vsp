# Диаграммы главы 8

## Dataset lifecycle

~~~mermaid
flowchart TD
    BEH["Desired model behavior"] --> STAGE["Choose training stage / data format"]
    STAGE --> TARGETS["Define quality · coverage · quantity targets"]
    TARGETS --> SEED["Collect representative seed data"]
    SEED --> GUIDE["Create labeling/evaluation guidelines"]
    GUIDE --> PILOT["Small pilot + manual inspection"]
    PILOT --> GAP{"Coverage / quality gaps?"}
    GAP -- "yes" --> ADD["Collect / label / augment / synthesize targeted data"]
    ADD --> VERIFY["Verify generated/annotated data"]
    VERIFY --> PROCESS["Deduplicate → clean/filter → format"]
    GAP -- "no" --> PROCESS
    PROCESS --> TRAIN["Train / finetune"]
    TRAIN --> EVAL["Evaluate model on target workload"]
    EVAL --> KEEP{"Improvement?"}
    KEEP -- "yes" --> VERSION["Keep version + provenance"]
    KEEP -- "no" --> TARGETS
~~~

## Synthetic-data validation

~~~mermaid
flowchart TD
    GEN["Generate synthetic example"] --> EXACT{"Programmatic verifier available?"}
    EXACT -- "yes" --> CHECK["Parser / linter / tests / execution"]
    EXACT -- "no" --> AI["AI/factuality/anomaly/heuristic checks"]
    CHECK --> PASS{"Pass?"}
    AI --> PASS
    PASS -- "no" --> REPAIR["Repair / regenerate / discard"]
    REPAIR --> GEN
    PASS -- "yes" --> MIX["Add to candidate dataset"]
    MIX --> MODEL["Train candidate model"]
    MODEL --> DOWN["Downstream evaluation"]
~~~

## Processing order

~~~mermaid
flowchart TD
    RAW["Immutable raw data"] --> INSPECT["Inspect distributions + provenance"]
    INSPECT --> PLAN["Choose cheapest sensible processing order"]
    PLAN --> TRIAL["Trial run on subset"]
    TRIAL --> OK{"Expected result?"}
    OK -- "no" --> PLAN
    OK -- "yes" --> DEDUP["Deduplicate"]
    DEDUP --> CLEAN["Clean / compliance filter"]
    CLEAN --> FORMAT["Format for target tokenizer/chat template"]
    FORMAT --> FINAL["Versioned training dataset"]
~~~

## Data-quality triad

~~~mermaid
flowchart LR
    Q["Quality"] --> MODEL["Useful training dataset"]
    C["Coverage / diversity"] --> MODEL
    N["Quantity"] --> MODEL
    MODEL --> PERF["Measured model performance"]
~~~
