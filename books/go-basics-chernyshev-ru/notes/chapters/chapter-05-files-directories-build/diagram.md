# Диаграмма — глава 5: filesystem → persistence → build → application state

~~~mermaid
flowchart TD
    A["Raw filesystem"] --> B["Files"]
    A --> C["Directories"]
    B --> B1["Create/Open/OpenFile"]
    B --> B2["Read/Write/Scan"]
    B --> B3["Rename/Remove/Copy"]
    C --> C1["Mkdir/MkdirAll/MkdirTemp"]
    C --> C2["ReadDir/Stat/IsNotExist"]

    B --> D["Structured data"]
    D --> D1["JSON Marshal"]
    D --> D2["JSON Unmarshal"]
    D --> D3["tags / omitempty / pointers"]

    D --> E["Persistence examples"]
    E --> E1["linked-list DB + text files"]
    E --> E2["JSON key:value store"]

    E --> F["Build/config"]
    F --> F1["go build"]
    F --> F2["CLI flags"]
    F --> F3["-ldflags"]
    F --> F4["go:embed"]
    F --> F5[".env"]

    F --> G["Tic-tac-toe v.3"]
    G --> G1["IGameLoader / IGameSaver"]
    G1 --> G2["JsonGameStorage"]
    G2 --> G3["save/load session"]

    G --> H["Tic-tac-toe v.4"]
    H --> H1["board"]
    H --> H2["player"]
    H --> H3["game"]
    H --> H4["model: GameSnapshot"]
    H --> H5["storage"]
    H2 --> H6["Human / Computer"]
    H6 --> H7["easy / medium / minimax"]
~~~

## Persistence decision map

~~~text
Need raw bytes/text?
→ file APIs

Need portable structured format?
→ JSON

Known JSON schema?
├─ yes → struct + tags
└─ no  → map[string]any

Need application save/load?
→ storage interface
→ concrete JSON storage
→ inject dependency into game layer
~~~

## Build/config map

~~~text
runtime user option
→ package flag

compile-time variable
→ -ldflags -X

static bundled file
→ go:embed

local key=value configuration
→ .env loader
~~~

## Provenance

- file/dir operations: `p0213:c01–p0238:c01`
- JSON: `p0239:c01–p0249:c01`
- persistence examples: `p0249:c01–p0271:c01`
- build/config: `p0271:c01–p0280:c01`
- v.3: `p0281:c01–p0286:c01`
- v.4: `p0287:c01–p0305:c01`
