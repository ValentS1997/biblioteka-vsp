# Диаграмма: сетевые приложения и службы по главе 10

## Client / server flow

~~~mermaid
flowchart LR
    C["Client process"] --> CS["Client socket"]
    CS --> T["TCP / UDP"]
    T --> SS["Server listening endpoint"]
    SS --> S["Server process"]
    S --> APP["Application protocol"]
~~~

## Service troubleshooting

~~~mermaid
flowchart TD
    X["Service symptom"] --> P{"Process/listener exists?"}
    P -->|No| START["Service activation/configuration"]
    P -->|Yes| ENDPOINT["Confirm address/port with netstat/lsof"]
    ENDPOINT --> CONN["Test client connection"]
    CONN --> PROTO{"Application exchange correct?"}
    PROTO -->|No| TRACE["curl trace / netcat / protocol check"]
    PROTO -->|Yes| OK["Service path works"]
    TRACE --> PKT["tcpdump only if lower-level evidence is needed"]
~~~

## SSH trust path

~~~mermaid
flowchart TD
    CLI["ssh client"] --> KEY["Server presents host key"]
    KEY --> KNOWN{"Matches known_hosts?"}
    KNOWN -->|Yes| AUTH["Continue authentication"]
    KNOWN -->|No| STOP["Stop and verify legitimate key change"]
    STOP -->|Confirmed| UPDATE["Replace/remove stale trust entry"]
    STOP -->|Not confirmed| REJECT["Do not trust connection"]
~~~

## SSH server lifecycle

~~~mermaid
flowchart LR
    CFG["/etc/ssh/sshd_config"] --> SSHD["sshd"]
    KEYS["Host key pairs"] --> SSHD
    SYSTEMD["systemctl start/enable"] --> SSHD
    SSHD --> LISTEN["Listening SSH endpoint"]
    LOG["Authentication logs"] --> F2B["fail2ban"]
    F2B --> FW["Temporary firewall block"]
~~~

## Diagnostic escalation

~~~mermaid
flowchart LR
    NETSTAT["netstat<br/>endpoint state"] --> LSOF["lsof<br/>process ownership"]
    LSOF --> NC["netcat/curl<br/>application interaction"]
    NC --> TCPDUMP["tcpdump<br/>packet visibility"]
    LSOF --> NMAP["nmap<br/>authorized exposure scan"]
~~~

## Network security principle

~~~mermaid
flowchart TD
    SERVICES["All installed/possible services"] --> MIN["Run only required services"]
    MIN --> FW["Firewall unnecessary exposure"]
    FW --> PATCH["Update exposed services"]
    PATCH --> ACC["Restrict accounts"]
    ACC --> TRUST["Avoid untrusted binaries/plaintext services"]
~~~

## Stream socket server

~~~mermaid
flowchart TD
    LS["Listening socket"] --> ACCEPT["accept()"]
    ACCEPT --> CS["Per-connection socket"]
    CS --> FORK["fork() handler pattern"]
    FORK --> IO["recv()/send() application I/O"]
    LS --> NEXT["Continue listening for next connection"]
~~~

## Unix domain socket

~~~mermaid
flowchart LR
    A["Local process A"] --> U["Unix domain socket"]
    U --> B["Local process B"]
    FS["Filesystem socket permissions"] --> U
    LSOFU["lsof -U"] --> U
~~~
