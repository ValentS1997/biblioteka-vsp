# Chapter logic diagram — «Ввод-вывод»

```mermaid
flowchart TD
    A["Program needs I/O"] --> B["15.1 User input/output"]
    B --> B1["input(prompt)"]
    B1 --> B2["reverse with [::-1]"]
    B2 --> B3["palindrome check"]
    B3 --> B4["homework: ignore punctuation/space/case"]

    A --> C["15.2 Files"]
    C --> C1["open(path, mode)"]
    C1 --> C2["write()"]
    C1 --> C3["readline()"]
    C3 --> C4["empty string → EOF"]
    C2 --> C5["close()"]
    C3 --> C5

    A --> D["15.3 Pickle"]
    D --> D1["open(..., wb)"]
    D1 --> D2["pickle.dump"]
    D2 --> D3["open(..., rb)"]
    D3 --> D4["pickle.load"]

    B4 --> E["15.4 Summary"]
    C5 --> E
    D4 --> E
    E --> F["Chapter 16: Exceptions"]
```

## Source boundary

`p0121:c01` → `p0126:c01`.

Substantive content ends at `p0125:c01`; `p0126:c01` contains only the running
footer for chapter 15. The next substantive chunk `p0127:c01` begins chapter 16
«Исключения».
