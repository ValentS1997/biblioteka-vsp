# Диаграмма — глава 8: sockets → REST → final client/server game

~~~mermaid
flowchart TD
    A["Network interaction"] --> B["UDP"]
    A --> C["TCP"]
    B --> B1["DialUDP / ListenUDP"]
    B1 --> B2["independent datagrams"]
    C --> C1["Dial / Listen / Accept"]
    C1 --> C2["persistent connection"]
    C2 --> C3["goroutine per connection"]
    C3 --> D["TCP chat"]
    D --> D1["send goroutine"]
    D --> D2["receive goroutine"]
    D --> D3["server broadcast + mutex"]

    A --> E["HTTP / REST"]
    E --> E1["GET / PUT / POST / DELETE"]
    E --> E2["headers / body / status"]
    E --> E3["resource URLs + query"]
    E --> F["OpenAPI v3"]
    F --> F1["info"]
    F --> F2["paths"]
    F --> F3["components"]
    F --> G["ToDo REST service"]
    G --> G1["gorilla/mux"]
    G --> G2["handlers"]
    G --> G3["GORM/SQLite repository"]

    C3 --> H["Tic-tac-toe v.7"]
    H --> H1["network protocol package"]
    H --> H2["server rooms + players"]
    H --> H3["client state machine"]
    H --> H4["JSON command payloads"]
    H --> H5["finished-games DB"]
~~~

## TCP server flow

~~~text
Listen
→ Accept connection
→ go handleConnection(conn)
→ read bytes/messages
→ route/handle
→ write response
→ close connection on exit
~~~

## REST design flow

~~~text
resource model
→ URL paths
→ HTTP methods
→ request params/body
→ response codes/schemas
→ OpenAPI spec
→ implementation
→ verification
~~~

## Game v.7 protocol flow

~~~text
client action
→ network.Message{Cmd, Payload}
→ TCP
→ server handleCommand
→ room/repository/player operation
→ response message
→ TCP
→ client readFromServer
→ state-specific handler
~~~

## Provenance

- UDP/TCP: `p0417:c01–p0425:c01`
- chat: `p0426:c01–p0428:c01`
- REST/OpenAPI: `p0429:c01–p0447:c01`
- ToDo service: `p0448:c01–p0466:c01`
- game v.7: `p0467:c01–p0505:c01`
