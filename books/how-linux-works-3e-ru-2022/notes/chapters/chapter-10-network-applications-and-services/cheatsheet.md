# Шпаргалка: сетевые приложения и службы по главе 10

## Symptom / problem framing

Типовые симптомы:

- service ожидается, но port не слушается;
- port слушается, но client не соединяется;
- connection есть, application protocol не отвечает как ожидается;
- неизвестно, какой process владеет port;
- SSH выдаёт host-key mismatch;
- remote login подвергается repeated brute-force attempts;
- нужно увидеть packet flow;
- нужно проверить exposed ports;
- непонятно, использует application TCP/UDP или Unix domain socket.

## Baseline / context

Source-derived service stack:

```text
application client
    ↓
socket
    ↓
TCP / UDP
    ↓
IP network
    ↓
server listening endpoint
    ↓
server process / application protocol
```

Для local IPC возможен другой путь:

```text
process A
   ↓
Unix domain socket
   ↓
process B
```

Security baseline:
- минимальное число exposed services;
- known server identity;
- supported software;
- firewall limits;
- no plaintext remote-login service.

## Read-only checks

### Endpoint / process ownership

```bash
netstat -nt
netstat -ntl
lsof -n -i
lsof -i:<port>
lsof -iTCP:<port>
lsof -iTCP -sTCP:LISTEN
```

Use `-n` to avoid hostname lookup during diagnosis.

### HTTP/application exchange

```bash
curl --trace-ascii <trace_file> http://<host>/
```

Creates a trace file, so classify as workload-generating rather than pure read-only.

### Packet observation

```bash
tcpdump
tcpdump tcp
tcpdump 'udp or port 80 or port 443'
```

Source warning: packet capture can expose packet contents. Capture only on networks you own or are authorized to inspect.

### RPC

```bash
rpcinfo -p localhost
```

Shows RPC program/port registrations.

### Unix domain sockets

```bash
ls -l /var/run/dbus/system_bus_socket
lsof -U
```

## Interpretation

### Listener vs connection

A server must have a process listening on the intended endpoint before a client connection can succeed.

`netstat -ntl` identifies listening TCP ports.  
`lsof -iTCP -sTCP:LISTEN` maps listeners to processes/users.

### Application protocol

A successful TCP connection proves transport connectivity, not correctness of application protocol.

Source uses direct HTTP text over `telnet` and structured `curl --trace-ascii` to reveal the application exchange.

### SSH trust

Client and server maintain host-key trust state.

If SSH reports that remote host identification changed:
1. do not silently bypass the warning;
2. confirm legitimate key change;
3. only then replace/remove the stale `known_hosts` entry.

### Packet-level troubleshooting

Use `tcpdump` only when endpoint/process state is insufficient.

Filter by protocol, host, network or port to minimize irrelevant/sensitive capture.

### netcat

`netcat` can:
- connect to TCP/UDP port;
- listen on a port;
- select IPv4/IPv6;
- expose stdin/stdout to connection.

A listener is an active service surface, even if temporary.

### Port scanning

`nmap <host>` finds open ports.

Source requires permission when scanning a network controlled by someone else.

### RPC

RPC program numbers are mapped to transport ports by `rpcbind`. If an RPC service is involved, `rpcinfo -p localhost` exposes registered mappings.

### Security

Source priorities:
- run fewer services;
- firewall unnecessary exposure;
- update exposed services;
- use supported server releases;
- restrict accounts;
- avoid untrusted binaries;
- avoid plaintext remote-login/file-transfer services.

### Sockets

TCP → stream socket.  
UDP → datagram socket.

Typical incoming stream-server flow:
`listen → accept() → connection socket → handler process`.

Unix domain sockets provide local IPC without traversing the IP network.

## Next action

1. Confirm expected service/process exists.
2. Confirm expected listening endpoint.
3. Test client connection/application exchange.
4. Map endpoint to process with `lsof`.
5. Use packet capture only if needed.
6. For SSH, validate host identity before editing trust state.
7. For exposure questions, scan only authorized hosts.
8. If no IP listener exists, inspect Unix domain sockets.

## Modifying action

Source-confirmed modifying/workload actions include:

```bash
systemctl enable sshd
systemctl start sshd
ssh-keygen -t rsa -N '' -f /etc/ssh/ssh_host_rsa_key
ssh-keygen -t dsa -N '' -f /etc/ssh/ssh_host_dsa_key
ssh <user>@<host>
scp <user>@<host>:<file> .
scp <file> <user>@<host>:<dir>
netcat -l <port>
nmap <host>
```

Source also allows editing/removing a stale `known_hosts` line only after legitimate host-key change is confirmed.

Do not expose private host keys.

## Verification / acceptance checks

| Action/change | Verification |
|---|---|
| start sshd | confirm listener/process using `lsof -i` / listener report |
| enable sshd | boot-persistence verification is `[Needs confirmation]` within chapter |
| host-key creation | verify expected key files exist; never disclose private key contents |
| SSH trust correction | reconnect and verify expected host identity |
| file transfer | verify destination file/path |
| netcat listener | confirm connection/listener behavior |
| packet diagnosis | confirm expected packets/protocol fields |
| RPC diagnosis | confirm expected program mapping via `rpcinfo -p localhost` |
| Unix socket | verify path/owner/process via `ls -l` and `lsof -U` |

## Rollback

- `systemctl enable sshd` → source does not supply inverse command here: `[Needs confirmation]`.
- `systemctl start sshd` → source does not supply inverse command here: `[Needs confirmation]`.
- Host-key generation/replacement → restore only from a verified previous key backup; otherwise `[Needs confirmation]`.
- `known_hosts` edit → restore the previous verified line/file backup; generic source procedure `[Needs confirmation]`.
- `scp`/remote file writes → depends on overwritten/created destination data: `[Needs confirmation]`.
- `netcat -l` listener → terminate the foreground process; no persistent configuration is described.
- `nmap`, `tcpdump`, `rpcinfo`, `lsof` → no persistent rollback when only used for observation.
