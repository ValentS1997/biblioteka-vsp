# Диаграмма — глава 4: error path vs panic path

~~~mermaid
flowchart TD
    A["Call operation"] --> B{"Outcome"}
    B -->|success| C["value + nil"]
    B -->|recoverable failure| D["value/zero + error"]
    D --> E{"err != nil?"}
    E -->|yes| F["handle / classify"]
    E -->|no| C
    F --> F1["errors.Is"]
    F --> F2["errors.As"]
    F --> F3["wrap with fmt.Errorf + %w"]
    F3 --> F4["errors.Unwrap"]

    B -->|panic-level failure| G["panic"]
    G --> H["run registered defer calls"]
    H --> I{"recover in deferred handler?"}
    I -->|no| J["process may terminate"]
    I -->|yes| K["handle panic"]
    K --> L{"re-panic?"}
    L -->|yes| M["higher-level deferred recover may handle"]
    L -->|no| N["continue after recovered function path"]
~~~

## Error classification flow

~~~text
err
├─ known package-level value?
│  └─ errors.Is
├─ custom structured type?
│  └─ errors.As
└─ lower-level cause with added context?
   └─ fmt.Errorf("%w") → errors.Unwrap
~~~

## Provenance

- panic: `p0200:c01–p0202:c01`
- defer/recover: `p0202:c01–p0205:c01`
- error creation/handling: `p0205:c01–p0207:c01`
- `errors.Is` / `errors.As`: `p0207:c01–p0209:c01`
- wrapping/unwrapping: `p0209:c01–p0211:c01`
