# Команды и инструменты — глава 8

Source policy: `rag_only`.

## UDP/TCP sample startup

Source uses a single executable with role selected through `os.Args`:

~~~bash
go run .\main.go 1
go run .\main.go 2
~~~

Meaning in chapter examples:
- `1` → server;
- `2` → client.

Type: launches network listeners/connections.

Verification:
- server prints that it is running/listening;
- client connects to expected address;
- echo messages are exchanged;
- `STOP` terminates the sample server path.

## Multi-client TCP server

Core APIs:

~~~go
net.Listen("tcp", ":8081")
listener.Accept()
go handleConnection(connection)
~~~

Verification:
- multiple terminals/clients can connect;
- one client does not block acceptance of another.

## TCP chat

Source uses:

~~~go
net.Dial("tcp", addr)
bufio.NewReader(conn).ReadString('\n')
conn.Write([]byte(message))
~~~

Client runs send/receive in separate goroutines.

Server keeps active `net.Conn` values and broadcasts to other clients.

## ToDo REST service dependencies

~~~bash
go get github.com/gorilla/mux
go get github.com/mattn/go-sqlite3
go get gorm.io/gorm
go get gorm.io/driver/sqlite
~~~

Type: state-changing/network.

Effect:
- downloads dependencies;
- updates module dependency state.

Rollback: `[Needs confirmation]`.

## REST service listener

~~~go
log.Fatal(http.ListenAndServe(":8080", router))
~~~

Verification:
- browser/client reaches `/api/v1/todo`;
- handler returns expected response;
- route-specific handlers return documented status codes.

## OpenAPI tooling

Source uses VS Code OpenAPI/Swagger extensions to:
- create YAML spec;
- preview `info`, `paths`, `components`;
- inspect endpoint/request/response structures.

No shell command for extension installation is given in the retrieved source.

## Final game v.7 startup

Server mode:

~~~bash
go run .\main.go
~~~

Client mode:

~~~bash
go run .\main.go -mode=client
~~~

Source also defines:

~~~text
-addr
~~~

for network address selection.

## Final game primitives

### Client connect

~~~go
conn, err := net.Dial("tcp", addr)
~~~

### Client receive loop

~~~go
go c.readFromServer()
decoder := json.NewDecoder(c.conn)
decoder.Decode(&msg)
~~~

### Server routing

~~~go
switch msg.Cmd {
case network.CmdNickname:
case network.CmdMakeMoveRequest:
case network.CmdListRoomsRequest:
case network.CmdJoinRoomRequest:
case network.CmdLeaveRoomRequest:
...
}
~~~

### Synchronization

Source uses `sync.Mutex`/`sync.RWMutex` around shared server/client state.

## Operational risk matrix

| Action | Risk | Verification |
|---|---|---|
| start listener | port already in use | listener starts successfully |
| client connect | wrong address/server absent | `net.Dial` succeeds |
| goroutine per client | shared-state race | source mutex/RWMutex + functional test |
| `go get` | modifies dependency state | inspect module files |
| REST route | wrong method/path/status | compare with OpenAPI/source contract |
| client-server protocol | command/payload mismatch | decode + handler path works |
