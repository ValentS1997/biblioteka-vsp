# Cheatsheet — глава 10 «Сетевые приложения и службы»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0320:c01`–`p0343:c01`, PDF/печатные страницы 320–343. Только `rag_only`.

## Symptom / problem framing

Глава помогает разбирать проблемы вида:

1. service process запущен, но клиент не может подключиться;
2. порт слушает, но прикладной протокол не отвечает ожидаемым образом;
3. неизвестно, какой процесс владеет портом;
4. SSH выдаёт host-key warning или сервер не стартует;
5. нужно понять, что реально идёт по сети;
6. нужно отличить network socket от Unix domain socket.

Рабочая модель: **process → listener/socket → transport connection → application protocol → security policy/identity**.

## Baseline / context

| Объект | Смысл | PDF |
|---|---|---:|
| Application protocol | HTTP/SSH/RPC semantics live in user space | 320–323 |
| Listening server | Process binds/listens on a port and accepts clients | 323–324 |
| Worker model | Listener may fork/create workers for connections | 324 |
| `sshd` | OpenSSH server; separate from client `ssh` | 324–329 |
| Host key | Server identity; private part must remain secret | 326–327 |
| `known_hosts` | Client-side record of remote host identities | 327,329 |
| inetd/xinetd | Historical super-server model | 330–331 |
| `lsof -i` | Maps network endpoints to processes/users | 332–333 |
| `tcpdump` | Packet observation below application semantics | 333–335 |
| netcat | General-purpose TCP/UDP client/listener | 335–336 |
| Nmap | Remote/open-port discovery | 336–337 |
| RPC | Program-number-to-port mapping via rpcbind | 337 |
| Socket | Process/kernel interface for network I/O | 341–342 |
| Unix domain socket | Local IPC without IP networking | 342–343 |

## Read-only checks

```sh
netstat -nt
netstat -ntl
lsof -i
lsof -n -i
lsof -iTCP:443
lsof -iTCP -sTCP:LISTEN
lsof -U
rpcinfo -p localhost
```

Protocol/application probes explicitly used by the source:

```sh
telnet example.org 80
curl --trace-ascii trace_file http://www.example.org/
ssh remote_username@remote_host
```

Packet/port observation:

```sh
tcpdump
tcpdump tcp
tcpdump udp or port 80 or port 443
nmap host
```

Operational caveats:

- `telnet`, `curl`, `ssh`, netcat and Nmap generate network traffic; they are diagnostic/workload-generating, not passive.
- `tcpdump` observes packet traffic and may reveal sensitive data; authorization is required.
- Nmap should only scan hosts/networks you control or have permission to test.
- A normal-user `lsof -i` only shows that user's processes; root sees a broader system view.

## Interpretation

| Наблюдение | Интерпретация по главе | Что ещё не доказано |
|---|---|---|
| Process exists but no LISTEN endpoint | Service is not currently accepting that transport endpoint | Why it failed to bind/start |
| `lsof -iTCP -sTCP:LISTEN` shows process | Process owns a listening TCP socket | Remote reachability/firewall/app health |
| Listener bound only to loopback | Service is local-only for that address family | Whether this is intended |
| TCP connection succeeds, HTTP request fails | Transport path works; issue is higher/application layer | Server/app semantics/logs |
| `curl --trace-ascii` shows connect then request/response | Transport and application exchange both occurred | Content correctness beyond trace |
| SSH host-key warning | Stored identity differs from presented identity | Legitimate rebuild vs MITM: **[Needs confirmation]** |
| `tcpdump` sees SYN but no application response | Packets reach observation point | Listener/process/firewall response path |
| Nmap shows open port | Remote scanner can reach an open service endpoint | Which local process unless correlated with lsof |
| `rpcinfo -p localhost` lists RPC service | rpcbind knows program↔port mappings | Whether service is externally reachable/needed |
| `lsof -U` shows socket path | Local process uses Unix domain socket | Application-level protocol/permissions intent |

## Next action

1. Identify the expected service/process.
2. Confirm listener state and address family with `lsof`/netstat.
3. Probe transport/application behavior with the narrowest client.
4. If packet path is unclear, capture a focused `tcpdump` filter.
5. For SSH identity warnings, verify the remote host key independently before changing `known_hosts`.
6. For externally exposed services, confirm whether exposure is required at all.
7. If scanning/sniffing authorization is unclear, **STOP**.
8. If service ownership, host identity, or rollback is unknown → **[Needs confirmation]**.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| `systemctl enable sshd` | Persistently enables SSH server at boot | Expands remote attack surface |
| `systemctl start sshd` | Starts SSH server immediately | Opens listener if config/firewall permits |
| Generate SSH host keys with `ssh-keygen` | Creates server identity keypair | Replacing keys breaks identity continuity |
| Edit `sshd_config` | Changes SSH server behavior | Can deny access or weaken policy |
| Remove/replace bad `known_hosts` entry | Accepts a changed host identity on next connection | **High risk** if identity not independently verified |
| fail2ban deployment/config | Adds/removes firewall blocks based on auth failures | False positives can block legitimate clients |
| `netcat -l port_number` | Starts a listening endpoint | Exposes data path/port |
| Unix socket file/config changes | Changes local IPC endpoint/access | May break dependent applications |

## Verification / acceptance checks

| Change | Проверка | Acceptance |
|---|---|---|
| Start/enable sshd | listener view + successful SSH connection | Expected port/listen address and authenticated connection |
| SSH config change | new connection from known-good client + server logs | Intended policy works; recovery access preserved |
| Host-key generation/replacement | compare independently verified fingerprint/key | Clients see intended identity only |
| known_hosts correction | reconnect after out-of-band host verification | Warning disappears for verified key |
| fail2ban behavior | logs/firewall state + test from controlled client | Malicious/repeated attempts blocked without locking legitimate access |
| netcat listener | `lsof`/netstat + controlled client | Intended address/port only |
| Unix domain socket | `lsof -U` + application operation | Correct path/owner/permissions and IPC success |

## Rollback

- `systemctl start sshd`: stop/revert only if prior runtime state was captured; exact rollback command is not supplied by this chapter → **[Needs confirmation]**.
- `systemctl enable sshd`: inverse persistent action is not explicitly shown in this chapter → **[Needs confirmation]**.
- `sshd_config`: preserve the previous file and maintain an existing authenticated session before reload/restart; exact restore sequence is not given.
- Host keys: never overwrite/remove old keys without backup if continuity matters. Restoring the prior key material is the conceptual rollback; exact command sequence is **[Needs confirmation]**.
- `known_hosts`: save the original entry before deletion/replacement. If remote identity cannot be validated, do not modify it.
- fail2ban/netcat/Unix-socket state: rollback is service/tool-specific and not fully specified in the chapter.
- Pure observation tools require only terminating the command/session.

## Guardrails

- A running daemon is not proof that the expected network endpoint is reachable.
- An open port is not proof that the application protocol is healthy.
- A host-key mismatch must be treated as a security event until independently explained.
- Do not expose legacy plaintext remote-login services such as telnetd/rlogind/rexecd.
- Do not capture or scan traffic on systems/networks without authorization.
- Run as few network services as necessary and keep exposed services updated.
