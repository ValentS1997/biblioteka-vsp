# Команды и интерфейсы главы 10

Только команды и tools, явно подтверждённые RAG главы 10. Hostnames, usernames, paths and ports are generalized with placeholders where appropriate.

| Команда / интерфейс | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `telnet <host> 80` | Direct TCP/application-protocol experiment | workload-generating | Opens plaintext TCP connection | Source notes telnet is not secure for remote login | Observe connection/application response | N/A |
| `curl --trace-ascii <trace_file> http://<host>/` | Trace HTTP exchange | workload-generating | Sends HTTP request and writes trace file | Trace may contain application data | Inspect trace + response | Remove trace file if appropriate; source rollback otherwise N/A |
| `ssh-keygen -t rsa -N '' -f /etc/ssh/ssh_host_rsa_key` | Generate RSA SSH host key pair example | state-changing | Creates host identity files | Private key disclosure compromises host identity; source says installer usually handles keys | Verify expected key files without exposing private contents | `[Needs confirmation]` without prior-key backup |
| `ssh-keygen -t dsa -N '' -f /etc/ssh/ssh_host_dsa_key` | Generate DSA SSH host key pair example | state-changing | Creates host identity files | Same private-key risk; algorithm example reflects source | Verify expected key files without exposing private contents | `[Needs confirmation]` |
| `systemctl enable sshd` | Enable sshd at boot | state-changing | Changes service enablement | Increases persistent network attack surface | Source does not provide exact enablement check: `[Needs confirmation]` | `[Needs confirmation]` |
| `systemctl start sshd` | Start sshd immediately | state-changing | Starts network server | Opens SSH service according to configuration/firewall | Confirm listener/process with network tools | `[Needs confirmation]` |
| `ssh <user>@<host>` | Connect with SSH client | workload-generating | Opens authenticated remote session | Host-key mismatch may indicate legitimate rebuild or attack | Expected host identity + successful login | End session; no persistent rollback unless client state changed |
| `scp <user>@<host>:<file> .` | Copy remote file locally | state-changing | Writes local destination file | May overwrite destination depending on path/state | Verify local file | `[Needs confirmation]` |
| `scp <file> <user>@<host>:<dir>` | Copy local file to remote host | state-changing | Writes remote destination | May overwrite/create remote data | Verify remote destination | `[Needs confirmation]` |
| `scp <user1>@<host1>:<file> <user2>@<host2>:<dir>` | Remote-to-remote copy example | state-changing | Writes remote destination | Changes remote data | Verify destination | `[Needs confirmation]` |
| `netstat -nt` | Active TCP connections, numeric output | read-only | No state change | Legacy tool in source | Inspect endpoints/state | N/A |
| `netstat -ntl` | Listening TCP ports, numeric output | read-only | No state change | Legacy tool in source | Inspect LISTEN ports | N/A |
| `lsof -i` | Network-using/listening processes | read-only | No state change | Normal user sees own processes only | Map PID/user/endpoint | N/A |
| `lsof -n -i` | Same without hostname resolution | read-only | No state change | None | Faster raw-address view | N/A |
| `lsof -i:<port>` | Filter by port | read-only | No state change | None | Identify owning process | N/A |
| `lsof -iTCP:<port>` | Filter TCP port | read-only | No state change | None | Identify TCP endpoint/process | N/A |
| `lsof -iTCP -sTCP:LISTEN` | Show TCP listening processes | read-only | No state change | None | Confirm listener/PID/user | N/A |
| `tcpdump` | Capture/print packets | workload-generating | Places interface in capture/promiscuous observation context | Can reveal sensitive packet contents; authorization/privacy boundary | Confirm expected traffic | Stop capture |
| `tcpdump tcp` | Capture TCP packets only | workload-generating | Packet capture with filter | Same capture/privacy risk | Confirm TCP exchange | Stop capture |
| `tcpdump 'udp or port 80 or port 443'` | Filter UDP/web-port traffic | workload-generating | Packet capture with expression | May expose traffic metadata/content | Confirm target traffic | Stop capture |
| `netcat <host> <port>` | Open TCP connection | workload-generating | Opens connection and maps stdio | Can interact with arbitrary service | Observe remote response/exit status | Ctrl+C/connection close |
| `netcat -l <port>` | Listen on port | workload-generating | Temporarily opens listener | Exposes a temporary service endpoint | Confirm incoming connection | Terminate process |
| `nmap <host>` | Scan host ports | workload-generating | Sends probes to target | Source requires permission on networks controlled by others | Review open-port report | N/A |
| `rpcinfo -p localhost` | Show local RPC registrations | read-only | No state change | None | Review program/port mapping | N/A |
| `ls -l /var/run/dbus/system_bus_socket` | Inspect Unix socket file | read-only | No state change | None | Check socket file metadata | N/A |
| `lsof -U` | List Unix domain sockets | read-only | No state change | Large output possible | Map process/socket path | N/A |

## Source-confirmed configuration and trust surfaces

- Server configuration: `/etc/ssh/sshd_config`.
- Client configuration: `/etc/ssh/ssh_config`.
- SSH host/public key files under `/etc/ssh`.
- User host trust: `.ssh/known_hosts`.
- Legacy TCP wrappers: `/etc/hosts.allow`, `/etc/hosts.deny`.
- Example D-Bus Unix socket: `/var/run/dbus/system_bus_socket`.

## Source-described but not fully operationalized

- `fail2ban` monitors failed-login logs and creates/removes firewall blocks.
- `sftp` provides secure file transfer with `get`/`put`.
- `inetd/xinetd` provide legacy on-demand service activation.
- `tcpd` provides legacy TCP-wrapper access control.
- TLS/SSL and Stunnel are referenced as encryption/security mechanisms.
- `accept()`, `fork()`, `recv()`, `send()` are conceptual socket-programming interfaces, not shell commands.

## Safety notes

1. Never expose SSH private host keys.
2. Do not treat a changed SSH host key as harmless until legitimate change is confirmed.
3. Packet capture can expose sensitive traffic; inspect only authorized networks.
4. Port scanning on infrastructure controlled by others requires permission.
5. Minimize internet-facing services and keep required services updated.
6. Source identifies plaintext services such as `ftpd`, `telnetd`, `rlogind`, `rexecd` as services to deactivate/avoid.
