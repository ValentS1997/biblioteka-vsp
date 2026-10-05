# Команды и интерфейсы главы 9

Только команды и инструменты, явно подтверждённые RAG главы 9. Environment-specific addresses, interfaces and hostnames заменены placeholders.

| Команда / интерфейс | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `ip address show` | Показать interfaces, MAC и IP addresses | read-only | Не меняет state | Нет state change | Сопоставить interface/address/prefix | N/A |
| `ip -6 address show` | Показать IPv6 addresses | read-only | Не меняет state | Нет state change | Проверить global/link-local addresses | N/A |
| `ip route show` | Показать IPv4 routing table | read-only | Не меняет state | Нет state change | Найти connected/default/specific routes | N/A |
| `ip -6 route show` | Показать IPv6 routes | read-only | Не меняет state | Нет state change | Проверить IPv6 route/default | N/A |
| `route -n` | Legacy route-table view | read-only | Не меняет state | Legacy interface | Сравнить с kernel route state | N/A |
| `ping <host>` | ICMP echo test | workload-generating | Отправляет ICMP echo requests | Отсутствие reply не доказывает service failure | Проверить replies/ICMP errors | N/A |
| `ping -4 <host>` / `ping -6 <host>` | Принудительно IPv4/IPv6 ICMP | workload-generating | Отправляет ICMP по выбранному family | То же ограничение ping | Сравнить family-specific path | N/A |
| `host <name-or-ip>` | DNS forward/reverse lookup | workload-generating | Выполняет resolver query | DNS result может включать несколько addresses | Проверить returned names/addresses | N/A |
| `nmcli` | Краткая сводка NetworkManager | read-only | Не меняет state при запуске без аргументов | Нет state change | Проверить interface/connection summary | N/A |
| `nm-online` | Проверить network-online state NetworkManager | read-only | Возвращает status code | NetworkManager-specific signal | Проверить exit status | N/A |
| `resolvectl status` | Показать resolver/DNS state | read-only | Не меняет state | Может называться иначе в старых systems | Проверить per-link/global DNS state | N/A |
| `nslookup -debug <host>` | Диагностический DNS lookup | workload-generating | Выполняет DNS query с debug output | Нет state change | Проверить used resolver/details | N/A |
| `netstat -nt` | Показать active TCP connections без DNS | read-only | Не меняет state | Legacy tool in source | Проверить local/foreign address:port/state | N/A |
| `netstat -ntl` | Показать listening TCP ports | read-only | Не меняет state | Legacy tool in source | Проверить LISTEN endpoints | N/A |
| `sysctl net.ipv4.ip_forward` | Проверить IPv4 forwarding | read-only | Не меняет state | Нет state change | Проверить value | N/A |
| `iptables -L` | Показать firewall chains/policies/rules | read-only | Не меняет state | Output order критичен для interpretation | Зафиксировать baseline | N/A |
| `ip -4 neigh` | Показать IPv4 neighbor/ARP cache | read-only | Не меняет state | Cache entries динамические | Проверить IP/MAC/state | N/A |
| `iw dev <interface> scan` | Сканировать доступные wireless networks | workload-generating | Выполняет scan | Interface должен быть up | Проверить scan output | N/A |
| `iw dev <interface> link` | Показать текущую wireless association | read-only | Не меняет state | Нет state change | Проверить AP/link state | N/A |
| `ip address add <address>/<prefix> dev <interface>` | Добавить address к kernel interface | state-changing | Меняет interface network-layer state | Ошибка address/prefix может нарушить connectivity | `ip address show` | `[Needs confirmation]` |
| `ip route add default via <gateway> dev <interface>` | Добавить default route | state-changing | Меняет routing table | Неверный gateway может перенаправить/сломать traffic | `ip route show` | `ip route del default` |
| `ip route del default` | Удалить default route | state-changing | Удаляет default route | Remote/internet connectivity может исчезнуть | `ip route show` | `[Needs confirmation]` без сохранённого прежнего route |
| `ip route add <subnet>/<prefix> via <router>` | Добавить specific route | state-changing | Меняет routing table | Нужен корректный reverse path; иначе route бесполезен | `ip route show` | `ip route del <subnet>/<prefix>` |
| `ip route del <subnet>/<prefix>` | Удалить specific route | state-changing | Удаляет route | Может разорвать path | `ip route show` | `[Needs confirmation]` без сохранённого previous route |
| `dhclient <interface>` | Ручной DHCP client test | state-changing | Меняет interface/DHCP lease-related configuration | Source требует перед test удалить existing gateway route | Проверить resulting address/routes | `[Needs confirmation]` |
| `sysctl -w net.ipv4.ip_forward=1` | Включить IPv4 forwarding | state-changing | Host начинает route packets между networks | Меняет network role/security boundary | `sysctl net.ipv4.ip_forward` | `[Needs confirmation]` |
| `iptables -P FORWARD DROP` | Установить default FORWARD policy DROP | state-changing | Меняет forwarding firewall policy | Может немедленно блокировать routed traffic | `iptables -L` | `[Needs confirmation]` без previous policy |
| `iptables -t nat -A POSTROUTING -o <external_if> -j MASQUERADE` | Добавить NAT masquerade rule | state-changing | Меняет source translation для outgoing traffic | Меняет packet path/state tracking | `iptables -L` + expected connectivity | `[Needs confirmation]` |
| `iptables -A FORWARD -i <external_if> -o <internal_if> -m state --state ESTABLISHED,RELATED -j ACCEPT` | Разрешить return traffic NAT example | state-changing | Добавляет FORWARD rule | Ошибка interface/state logic меняет access | `iptables -L` | `[Needs confirmation]` |
| `iptables -A FORWARD -i <internal_if> -o <external_if> -j ACCEPT` | Разрешить outbound forwarding NAT example | state-changing | Добавляет FORWARD rule | Может разрешить больше traffic, чем intended | `iptables -L` | `[Needs confirmation]` |
| `iptables -P INPUT DROP` | Default INPUT policy DROP | state-changing | Отбрасывает unmatched incoming packets | **Source warning:** remote-only access can be cut immediately | `iptables -L` + required access checks | `[Needs confirmation]` |
| `iptables -A INPUT -s <source> -j DROP` | Добавить source block rule | state-changing | Добавляет INPUT rule | Rule ordering matters | `iptables -L` | `[Needs confirmation]` |
| `iptables -A INPUT -s <subnet>/<prefix> -p tcp --destination-port <port> -j DROP` | Block TCP port from subnet | state-changing | Добавляет scoped DROP rule | Может block legitimate clients | `iptables -L` | `[Needs confirmation]` |
| `iptables -A INPUT -s <source> -j ACCEPT` | Добавить source allow rule | state-changing | Добавляет ACCEPT rule at end | Может не сработать, если earlier rule уже matches | `iptables -L` | `[Needs confirmation]` |
| `iptables -D INPUT <rule_number>` | Удалить INPUT rule по номеру | state-changing | Удаляет rule | Wrong rule number changes wrong policy | `iptables -L` | Recreate rule only if exact previous rule known; otherwise `[Needs confirmation]` |
| `iptables -I INPUT -s <source> -j ACCEPT` | Insert allow rule at chain start | state-changing | Меняет rule order | Earlier match changes firewall semantics | `iptables -L` | `[Needs confirmation]` |
| `iptables -A INPUT -p icmp -j ACCEPT` | Разрешить ICMP | state-changing | Добавляет INPUT rule | Policy scope depends on other rules | `iptables -L` | `[Needs confirmation]` |
| `iptables -A INPUT -s 127.0.0.1 -j ACCEPT` | Разрешить localhost-source traffic | state-changing | Добавляет INPUT rule | Part of restrictive-policy sequence | `iptables -L` | `[Needs confirmation]` |
| `iptables -A INPUT -p tcp --destination-port 22 -j ACCEPT` | Разрешить inbound SSH example | state-changing | Добавляет SSH allow rule | Exposes SSH according to other constraints | `iptables -L` | `[Needs confirmation]` |
| `ip neigh del <host> dev <interface>` | Удалить stale neighbor entry | state-changing | Removes ARP/neighbor cache entry | Temporary connectivity resolution delay possible | `ip -4 neigh` | `[Needs confirmation]` |
| `ifconfig <interface> up` | Поднять wireless interface для scan example | state-changing | Changes interface state | Legacy command in source | `ip address show` | `[Needs confirmation]` |
| `iw <interface> connect <network_name>` | Подключиться к unsecured Wi-Fi network | state-changing | Changes wireless association | Source limits this example to unsecured network; WEP discouraged | `iw dev <interface> link` | `[Needs confirmation]` |

## Source-confirmed configuration surfaces

- NetworkManager global configuration: `/etc/NetworkManager/NetworkManager.conf`.
- NetworkManager connections: `/etc/NetworkManager/system-connections`.
- Dispatcher scripts: `/etc/NetworkManager/dispatcher.d`.
- Host mapping: `/etc/hosts`.
- Traditional resolver configuration: `/etc/resolv.conf`.
- Name-service ordering: `/etc/nsswitch.conf`.
- systemd-resolved configuration: `/etc/systemd/resolved.conf`.
- systemd-networkd configuration: `/etc/systemd/network`.
- Persistent sysctl examples: `/etc/sysctl.conf` or distribution-dependent `/etc/sysctl.d`.
- wpa_supplicant default configuration mentioned by source: `/etc/wpa_supplicant.conf`.

## Referenced but not operationalized with a concrete command sequence

The chapter names these tools/interfaces but does not provide a complete safe write workflow for them:

- `ethtool`;
- `nft` / nftables;
- `iptables-translate`;
- `wpa_supplicant`;
- Netplan.

Do not synthesize missing commands from model knowledge.

## Safety notes

1. Manual network configuration is described as error-prone; source recommends experimenting on a noncritical system.
2. A route is only useful when the return path is also valid.
3. Multiple DHCP servers in one subnet can create conflicting configuration.
4. Firewall chains use first-match semantics; rule order is part of policy.
5. Source explicitly warns against applying restrictive INPUT rules sequentially on a remote-only machine.
6. NAT/firewall examples alter packet flow and require a known-good baseline before changes.
7. WEP and old insecure WPA should not be used; source points to WPA2/WPA3 through `wpa_supplicant`.
