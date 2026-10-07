# Mermaid — глава 10 «Сетевые приложения и службы»

Источник: **RAG `p0320:c01`–`p0343:c01`**, PDF/печатные страницы 320–343. Диаграммы синтезированы из текста главы; исходный рис. 10.1 не реконструируется.

## 1. Application protocol over TCP

```mermaid
flowchart TD
  CLIENT["Client application"] --> CPROTO["Application protocol logic"]
  CPROTO --> TCP["TCP byte stream"]
  TCP --> SERVER["Server process"]
  SERVER --> SPROTO["Server application protocol logic"]
  SPROTO --> RESP["Response headers + body"]
  RESP --> TCP
  TCP --> CLIENT
```

HTTP header/body distinction is interpreted by user-space applications; lower layers carry bytes without knowing those semantic boundaries (§10.1–10.2).

## 2. Typical network-server process model

```mermaid
flowchart TD
  MAIN["Main server process"] --> LISTEN["Listening socket / port"]
  LISTEN --> NEW["Incoming connection"]
  NEW --> ACCEPT["accept connection"]
  ACCEPT --> WORKER["Worker / child process"]
  WORKER --> RW["Read/write connected socket"]
  MAIN --> LISTEN
```

The chapter notes that some high-performance servers pre-create workers; UDP services do not need a per-connection fork model (§10.3).

## 3. SSH trust boundary

```mermaid
flowchart TD
  CLIENT["ssh client"] --> KH["known_hosts / stored host key"]
  SERVER["sshd"] --> HK["Server host public/private keypair"]
  KH --> CMP{"Presented key matches stored identity?"}
  HK --> CMP
  CMP -->|Yes| SESSION["Encrypted/authenticated session"]
  CMP -->|No| WARN["Host-key warning"]
  WARN --> VERIFY["Verify new key independently"]
  VERIFY -->|Confirmed| UPDATE["Update stored key"]
  VERIFY -->|Not confirmed| STOP["STOP"]
```

A host-key mismatch is security-significant; the source explicitly mentions possible interception (§10.3.4).

## 4. SSH service lifecycle

```mermaid
flowchart TD
  CFG["/etc/ssh/sshd_config"] --> SSHD["sshd"]
  KEYS["Host keys"] --> SSHD
  ENABLE["systemctl enable sshd"] --> BOOT["Start on boot"]
  START["systemctl start sshd"] --> SSHD
  SSHD --> PORT["Listening SSH port"]
  PORT --> CLIENT["ssh / scp / sftp clients"]
```

Configuration and host identity are separate inputs to the server (§10.3.2–10.3.4).

## 5. Diagnostic ladder

```mermaid
flowchart TD
  S["Service symptom"] --> P["Process/port ownership: lsof / netstat"]
  P --> T["Transport probe: telnet / netcat / ssh"]
  T --> APP["Application exchange: curl / protocol request"]
  APP --> PKT["Packet path if needed: tcpdump"]
  PKT --> EXT["External exposure: Nmap from authorized vantage point"]
  EXT --> EVID["Correlated evidence"]
```

Each tool answers a different layer/question; an open port does not prove application health.

## 6. lsof correlation

```mermaid
flowchart LR
  PROC["Process / PID / user"] --> FD["File descriptor"]
  FD --> ENDPOINT["TCP / UDP / Unix socket"]
  ENDPOINT --> STATE["LISTEN / ESTABLISHED / local IPC"]
  FILTER["Protocol / port / state filters"] --> ENDPOINT
```

The chapter uses lsof to connect application processes with network or Unix-domain endpoints (§10.5.1, §10.10).

## 7. Packet capture versus application state

```mermaid
flowchart TD
  APP["Application"] --> K["Kernel networking"]
  K --> NIC["Network interface"]
  CAP["tcpdump"] --> NIC
  CAP --> HDR["Packet/header evidence"]
  HDR --> Q{"Does capture prove app behavior?"}
  Q -->|No| APPLOG["Need listener/process/protocol evidence too"]
```

tcpdump sees packet traffic, not full application intent/health. Packet payload may also be sensitive (§10.5.2).

## 8. Exposure/security model

```mermaid
flowchart TD
  SERVICE["Potential network service"] --> NEED{"Required?"}
  NEED -->|No| OFF["Do not run/expose it"]
  NEED -->|Yes| PATCH["Keep software supported/updated"]
  PATCH --> FILTER["Restrict exposure with firewall"]
  FILTER --> AUTH["Use secure authentication/encryption"]
  AUTH --> MON["Monitor failures / logs"]
```

This condenses the chapter's security guidance: minimize services, filter unnecessary traffic, maintain exposed software and avoid plaintext legacy remote-login services (§10.7).

## 9. Network socket boundary

```mermaid
flowchart LR
  USER["User-space process"] --> SOCK["Socket API"]
  SOCK --> KERNEL["Kernel transport/network stack"]
  KERNEL --> NET["Network"]
  SOCK --> STREAM["SOCK_STREAM → TCP-like stream"]
  SOCK --> DGRAM["SOCK_DGRAM → UDP-like datagram"]
```

Sockets form the interface between user space and the kernel's networking machinery (§10.9).

## 10. Unix domain socket IPC

```mermaid
flowchart TD
  P1["Local process A"] --> UDS["Unix domain socket"]
  UDS --> P2["Local process B"]
  FILE["Optional filesystem socket path"] --> UDS
  PERM["Filesystem permissions"] --> FILE
  UDS -.-> NONET["No IP network required"]
```

Unix-domain sockets can be filesystem-backed or unnamed and are used for local IPC (§10.10).
