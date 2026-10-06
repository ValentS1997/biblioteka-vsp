# Шпаргалка — глава 8: сетевое программирование

## Fast map

~~~text
UDP / TCP sockets
→ multi-client TCP
→ TCP chat
→ HTTP / REST
→ OpenAPI contract
→ REST service
→ final TCP client-server game
~~~

Scope: PDF 417–507.

## TCP vs UDP — source framing

| Property | TCP | UDP |
|---|---|---|
| Connection | established/persistent | no persistent connection |
| Delivery | source emphasizes reliable session behavior | source emphasizes no delivery guarantee |
| Server handling | connection-oriented, blocking socket calls | independent messages |
| Example | echo, chat, game v.7 | echo |

## UDP

Client:

~~~go
addr, _ := net.ResolveUDPAddr("udp4", "localhost:8081")
conn, err := net.DialUDP("udp4", nil, addr)
conn.Write(data)
conn.ReadFromUDP(buffer)
~~~

Server:

~~~go
addr, _ := net.ResolveUDPAddr("udp4", ":8081")
conn, err := net.ListenUDP("udp4", addr)
n, client, err := conn.ReadFromUDP(buffer)
conn.WriteToUDP(buffer[:n], client)
~~~

## TCP

Client:

~~~go
conn, err := net.Dial("tcp", "localhost:8081")
~~~

Server:

~~~go
listener, err := net.Listen("tcp", ":8081")
conn, err := listener.Accept()
go handleConnection(conn)
~~~

## TCP chat

~~~text
client
├─ goroutine: stdin → socket
└─ goroutine: socket → terminal

server
├─ []net.Conn
├─ Mutex around connection list changes
└─ broadcast message to other clients
~~~

## HTTP methods

| Method | Source role |
|---|---|
| GET | retrieve resource |
| PUT | create/write or update |
| POST | create/write |
| DELETE | delete |

## HTTP message

~~~text
headers
body (optional)
~~~

Response status line:

~~~text
HTTP/1.1 404 Not Found
~~~

Common source codes:

~~~text
200 201 400 401 404 405 409 500
~~~

## REST URL

Prefer resource nouns:

~~~text
/api/v1/todo/projects/3/tasks/1
~~~

Query form:

~~~text
/api/v1/todo/projects/3/tasks?id=1
~~~

## OpenAPI v3

Main sections:

~~~text
info
paths
components
~~~

Path parameter:

~~~yaml
- in: path
  name: id
  required: true
~~~

Query parameter:

~~~yaml
- in: query
  name: projectID
~~~

POST body:

~~~yaml
requestBody:
  content:
    application/json:
      schema:
        $ref: "#/components/schemas/Project"
~~~

## ToDo REST service

~~~bash
go get github.com/gorilla/mux
go get github.com/mattn/go-sqlite3
go get gorm.io/gorm
go get gorm.io/driver/sqlite
~~~

Handler signature:

~~~go
func(w http.ResponseWriter, r *http.Request)
~~~

Router:

~~~go
router := mux.NewRouter()
http.ListenAndServe(":8080", router)
~~~

## Tic-tac-toe v.7

~~~text
client
↕ TCP + JSON command protocol
server
├─ rooms
├─ players
├─ repository
└─ goroutines per connection
~~~

Protocol package:

~~~text
Command + Payload
→ nickname
→ rooms
→ join/leave
→ make move
→ update/end game
→ finished-game queries
~~~

Client:

~~~text
state machine
+ readFromServer goroutine
+ command-specific handlers
~~~

Run:

~~~bash
go run .\main.go
go run .\main.go -mode=client
~~~

## Acceptance

After chapter you should be able to:
- explain TCP/UDP source differences;
- create UDP and TCP client/server examples;
- handle multiple TCP clients concurrently;
- explain TCP chat architecture;
- describe HTTP request/response structure and common methods/statuses;
- design resource-oriented REST URLs;
- write OpenAPI path/query/body examples;
- explain mux-based ToDo service;
- explain v.7 TCP protocol, rooms, server routing and client state machine.

## Rollback / safety

Network examples open listeners and external dependencies can modify module state. Verify ports and process ownership before tests. Close listeners/connections cleanly. VCS rollback is not specified by source → `[Needs confirmation]`.
