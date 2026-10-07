# Команды и интерфейсы — глава 10 «Сетевые приложения и службы»

**Provenance:** `p0320:c01`–`p0343:c01`, PDF/печатные страницы 320–343. Только явно поддержанные chapter RAG команды/интерфейсы.

Классы: **RO** — read-only observation; **WG** — workload-generating / active probe / capture; **SC** — state-changing.

## 1. Application-layer probes

| Команда | Класс | Назначение | PDF |
|---|---|---|---:|
| `telnet example.org 80` | WG | Open raw TCP connection to HTTP service | 321 |
| manual `GET / HTTP/1.1` + `Host:` | WG | Exercise HTTP/1.1 request syntax over established TCP stream | 321 |
| `curl --trace-ascii trace_file http://www.example.org/` | WG | Trace transport/application exchange into a file | 322–323 |

The chapter uses these examples to show that HTTP header/body distinctions are application semantics, not separate lower-layer message types.

## 2. SSH server and host identity

Configuration paths/items:

- server config: `/etc/ssh/sshd_config`;
- client config: `/etc/ssh/ssh_config`;
- source host-key examples under `/etc/ssh`;
- server/client known-host databases: `ssh_known_hosts`, `.ssh/known_hosts`.

Source state-changing commands:

```sh
ssh-keygen -t rsa -N '' -f /etc/ssh/ssh_host_rsa_key
ssh-keygen -t dsa -N '' -f /etc/ssh/ssh_host_dsa_key
systemctl enable sshd
systemctl start sshd
```

| Action | Класс | Boundary |
|---|---|---|
| Generate host key | SC critical identity state | Do not overwrite an existing key without explicit backup/identity plan |
| Enable sshd | SC persistent | Increases remote attack surface |
| Start sshd | SC runtime | Opens SSH service if configuration/network permit |
| Edit `sshd_config` | SC security config | Can break remote access or weaken authentication policy |

The chapter's DSA/RSA key material is preserved as edition/source content, not treated as a current recommendation; see `source-findings.md`.

## 3. SSH client / file transfer

| Команда | Класс | Назначение |
|---|---|---|
| `ssh remote_username@remote_host` | WG | Interactive remote login |
| `ssh remote_host command` pattern | WG | Remote command execution |
| source tar/ssh pipeline | WG/SC on remote filesystem | Stream archive to remote extraction process |
| `scp user@host:file .` | WG/SC file copy | Copy remote file locally |
| `scp file user@host:dir` | WG/SC file copy | Copy local file remotely |
| `scp user1@host1:file user2@host2:dir` | WG/SC file copy | Remote-to-remote copy |
| `sftp` | WG/SC file transfer | Interactive secure file transfer |

A changed host key is not a routine nuisance: source warning text explicitly raises man-in-the-middle risk. Do not remove/replace a `known_hosts` entry until the new identity is independently confirmed.

## 4. Service/port observation

Source refers back to `netstat` and gives useful option semantics:

| Option | Meaning |
|---|---|
| `-t` | TCP |
| `-u` | UDP |
| `-l` | listening ports |
| `-a` | all active ports |
| `-n` | disable name resolution |
| `-4`, `-6` | restrict address family |

Common source-grounded combinations from surrounding chapters/examples: `netstat -nt`, `netstat -ntl`.

## 5. lsof network diagnostics

```sh
lsof -i
lsof -n -i
lsof -i:port
lsof -iTCP:443
lsof -iTCP -sTCP:LISTEN
lsof -iUDP
lsof -U
```

Full source-described filter form:

```text
lsof -iprotocol@host:port
```

Additional source options:
- `-P` disables service-name lookup via `/etc/services`;
- `-i4` / `-i6` filter by IP version.

The text gives a malformed-looking service-name example rendered as `-tcp:ssh`; it is not promoted to executable syntax. See `source-findings.md`.

## 6. tcpdump packet observation

```sh
tcpdump
tcpdump tcp
tcpdump udp or port 80 or port 443
```

Source filter primitives include `tcp`, `udp`, `ip`, `ip6`, `port`, `host`, `net`; operators include `or`, `and`, `!`, grouping.

**Class:** WG/RO capture. It may place an interface in promiscuous mode and can expose packet contents. Use only on hosts/networks you own or are authorized to inspect.

## 7. netcat

```sh
netcat host port
netcat -l port_number
```

Source options:
- `-v` verbose diagnostics;
- `-4` / `-6` force address family;
- `-u` use UDP instead of TCP.

Client use is **WG**. Listener mode is **SC/WG runtime exposure** because it opens a network endpoint.

## 8. Nmap / port scanning

```sh
nmap host
nmap -6 host
```

**Class:** WG active scan.

Source explicitly instructs users to obtain permission before scanning a network controlled by someone else. The chapter recommends comparing scans from more than one vantage point to understand firewall exposure.

## 9. RPC

```sh
rpcinfo -p localhost
```

**Class:** RO/WG local query. Lists RPC services registered through rpcbind.

## 10. Unix domain sockets

```sh
ls -l /var/run/dbus/system_bus_socket
lsof -U
```

**Class:** RO. Used to inspect filesystem-backed and unnamed Unix-domain sockets.

## 11. Historical service frameworks

Source-discussed but without a complete executable workflow:

- inetd;
- xinetd;
- tcpd / TCP wrappers;
- `/etc/hosts.allow`;
- `/etc/hosts.deny`;
- systemd socket activation.

No extra commands are invented where the chapter only describes architecture.

## Command discipline

- Hostnames, ports, paths, usernames and service names in examples are source context, not live-system facts.
- Prefer listener/process correlation before changing daemon configuration.
- Preserve SSH host identity and remote-access recovery before any server-key/config change.
- Packet capture and network scans require authorization.
- Do not use source examples of legacy plaintext services as deployment recommendations.
