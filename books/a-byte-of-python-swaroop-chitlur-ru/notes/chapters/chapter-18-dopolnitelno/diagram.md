# Chapter logic diagram — «Дополнительно»

```mermaid
flowchart TD
    A["Additional Python idioms"] --> B["18.1 Unpacking"]
    B --> B1["tuple return"]
    B1 --> B2["a, *b"]
    B2 --> B3["swap a,b = b,a"]

    A --> C["18.2 Special methods"]
    C --> C1["__str__ / __len__ / __getitem__ / ..."]

    A --> D["18.3–18.5 Compact forms"]
    D --> D1["single-line block"]
    D --> D2["lambda"]
    D --> D3["list comprehension"]

    A --> E["18.6 Variable args"]
    E --> E1["*args"]
    E --> E2["**kwargs"]

    A --> F["18.7 Runtime source execution"]
    F --> F1["exec"]
    F --> F2["eval"]
    F --> F3["execution-risk boundary"]

    A --> G["18.8–18.9 Checks / representation"]
    G --> G1["assert"]
    G --> G2["repr / __repr__"]

    A --> H["18.10–18.11 Strings"]
    H --> H1["escape sequences"]
    H --> H2["raw strings"]

    B3 --> I["18.12 Summary"]
    C1 --> I
    D3 --> I
    E2 --> I
    F3 --> I
    G2 --> I
    H2 --> I
    I --> J["Chapter 19: Что дальше"]
```

## Source boundary

`p0137:c01` → `p0144:c01`.

Substantive content ends at `p0143:c01`; `p0144:c01` contains only the running
footer for chapter 18. The next chunk `p0145:c01` begins chapter 19 «Что дальше».
