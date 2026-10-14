# Подтверждённые инструменты и команды — часть I

**Правило:** только команды/функции, явно присутствующие в RAG части I. В каждой строке указана категория: **RO** — наблюдение локального состояния; **WG** — генерирует сетевую/вычислительную нагрузку; **SC** — изменяет систему или её конфигурацию. `IFACE`, `ADDR`, `GW`, `HOST` — плейсхолдеры, а не готовые значения. Перед использованием замените плейсхолдеры только на собственные разрешённые параметры. Книга демонстрирует примеры из авторской среды, их результаты не универсальны.

## Наблюдение (RO)

| Команда из источника | Назначение | RAG |
|---|---|---|
| `ip link`, `ip addr show`, `ip -4 a s dev IFACE` | интерфейсы, адреса и статусы | [PDF p. 17](../../../rag/chunks/p0001-p0100/p0017-c01.md), [PDF p. 41](../../../rag/chunks/p0001-p0100/p0041-c01.md), [PDF p. 50](../../../rag/chunks/p0001-p0100/p0050-c01.md) |
| `ip -4 neigh show`, `ip -6 neigh show` | ARP/NDP, состояния соседей | [PDF p. 20](../../../rag/chunks/p0001-p0100/p0020-c01.md) |
| `arp -en`, `arp -vn` | таблица IPv4 ARP | [PDF p. 19](../../../rag/chunks/p0001-p0100/p0019-c01.md) |
| `ip route show`, `ip -6 route show` | IPv4/IPv6 маршруты отдельно | [PDF p. 47](../../../rag/chunks/p0001-p0100/p0047-c01.md) |
| `route -n`, `route -n -6` | представление таблиц маршрутизации | [PDF p. 46](../../../rag/chunks/p0001-p0100/p0046-c01.md) |
| `ifconfig`, `ifconfig lo` | диагностика интерфейсов/loopback | [PDF p. 39](../../../rag/chunks/p0001-p0100/p0039-c01.md), [PDF p. 54](../../../rag/chunks/p0001-p0100/p0054-c01.md) |
| `inxi -Nxxx`, `macchanger -s IFACE`, `ipv6calc --showinfo -i -m MAC` | устройство, MAC и его сведения | [PDF p. 17](../../../rag/chunks/p0001-p0100/p0017-c01.md), [PDF p. 18](../../../rag/chunks/p0001-p0100/p0018-c01.md) |
| `iwconfig`, `iw IFACE info`, `rfkill list` | беспроводной интерфейс и блокировки | [PDF p. 42](../../../rag/chunks/p0001-p0100/p0042-c01.md) |
| `nmcli --help`, `man 1 nmcli` | справка по NetworkManager | [PDF p. 45](../../../rag/chunks/p0001-p0100/p0045-c01.md) |
| `cat /etc/services` | локальный каталог имён служб и портов | [PDF p. 59](../../../rag/chunks/p0001-p0100/p0059-c01.md) |
| `ip addr help`, `route --help`, `ip -V` | справка/версия перед операциями | [PDF p. 42](../../../rag/chunks/p0001-p0100/p0042-c01.md), [PDF p. 49](../../../rag/chunks/p0001-p0100/p0049-c01.md), [PDF p. 58](../../../rag/chunks/p0001-p0100/p0058-c01.md) |

Заметка: `RO` означает отсутствие намеренного изменения конфигурации, а не отсутствие любой фоновой активности системы.

## Генерируют запросы или нагрузку (WG)

| Синтаксис в части I | Что выясняет / границы | RAG |
|---|---|---|
| `ping -c3 ADDR`, `ping -6 -c3 fe80::...%IFACE` | ограниченный ICMP-тест; для IPv6 link-local важна зона интерфейса | [PDF p. 30](../../../rag/chunks/p0001-p0100/p0030-c01.md), [PDF p. 54](../../../rag/chunks/p0001-p0100/p0054-c01.md) |
| `nslookup HOST DNS_SERVER`, `host HOST`, `dig @DNS_SERVER HOST` | запросы разрешения имени; факт ответа зависит от DNS | [PDF p. 36](../../../rag/chunks/p0001-p0100/p0036-c01.md) |
| `telnet HOST 80`, `telnet HOST 443` | попытка TCP-подключения, не полноценная проверка HTTP/HTTPS | [PDF p. 60](../../../rag/chunks/p0001-p0100/p0060-c01.md) |
| `nmap -6 HOST`, `nmap -sP PREFIX` | активное сканирование хоста/сети; только при разрешении | [PDF p. 32](../../../rag/chunks/p0001-p0100/p0032-c01.md), [PDF p. 53](../../../rag/chunks/p0001-p0100/p0053-c01.md) |
| `curl [IPv6]`, `wget http://[IPv6]:80/index.php -O -` | сетевое обращение к IPv6-веб-узлу; URL и экранирование согласовываются со средой; результат в книге относится к определённому тестовому узлу | [PDF p. 31](../../../rag/chunks/p0001-p0100/p0031-c01.md) |
| `./adr i6 ADDR`, `./adr i4 ADDR` | примеры собственного двунаправленного преобразования адреса; исполняемый файл должен быть сначала создан из авторского исходника | [PDF p. 34](../../../rag/chunks/p0001-p0100/p0034-c01.md), [PDF p. 35](../../../rag/chunks/p0001-p0100/p0035-c01.md) |

**Ограничения WG:** не запускать публичное сканирование/сетевые запросы к чужим адресам без разрешения. `ping`/DNS/`telnet` — диагностический трафик, не read-only по внешнему эффекту. В `curl [IPv6]` сохранён синтаксис примера книги; применимость без адаптации к конкретной оболочке **[Needs confirmation]**.

## Меняют состояние (SC)

| Операция, структура команды по источнику | Эффект и риск | Проверка | Rollback |
|---|---|---|---|
| `sudo macchanger -m NEW_MAC IFACE` | меняет MAC работающего интерфейса; может разорвать сетевой обмен/соседние соответствия | `macchanger -s IFACE`, `ip addr show`, соседние записи | **[Needs confirmation]**: исчерпывающая обратная процедура в части не показана; [PDF p. 18](../../../rag/chunks/p0001-p0100/p0018-c01.md) |
| `sudo apt install macchanger` | устанавливает пакет; влияет на состояние системы и зависимости | `macchanger --help` | **[Needs confirmation]**; [PDF p. 17](../../../rag/chunks/p0001-p0100/p0017-c01.md) |
| `sudo ip address add ADDR_IPV6/PREFIX dev IFACE` | добавляет IPv6-адрес, меняет связные маршруты | `ip addr show`, `ip -6 route show` | **[Needs confirmation]**; [PDF p. 48](../../../rag/chunks/p0001-p0100/p0048-c01.md) |
| `sudo ip -6 route add PREFIX_IPV6 via GW_IPV6` | добавляет IPv6-маршрут; может изменить путь трафика | `ip -6 route show`, авторский тест `ping` | **[Needs confirmation]**; [PDF p. 48](../../../rag/chunks/p0001-p0100/p0048-c01.md) |
| `sudo ifconfig IFACE:1 ADDR_IPV4 up` | создаёт alias-адрес; видимый префикс без маски в примере отличается от описания `/24` | `ifconfig`, `ip -4 a s dev IFACE`, `route -n` | **[Needs confirmation]**; [PDF p. 50](../../../rag/chunks/p0001-p0100/p0050-c01.md), [PDF p. 52](../../../rag/chunks/p0001-p0100/p0052-c01.md) |
| `sudo ifconfig IFACE down`, затем `sudo ip link set dev IFACE name NEW_IFACE` | останавливает и переименовывает интерфейс, риск утраты удалённого доступа | `ip link`, `ip -4 a s dev NEW_IFACE` | **[Needs confirmation]**; восстановление IP/шлюза разобрано отдельно; [PDF p. 55](../../../rag/chunks/p0001-p0100/p0055-c01.md), [PDF p. 56](../../../rag/chunks/p0001-p0100/p0056-c01.md) |
| `sudo ifconfig NEW_IFACE ADDR_IPV4 up` | восстанавливает адрес после переименования | `ip -4 a s dev NEW_IFACE` | **[Needs confirmation]**; [PDF p. 56](../../../rag/chunks/p0001-p0100/p0056-c01.md) |
| `sudo ip route add default via GW_IPV4` | добавляет маршрут по умолчанию, может изменить всю внешнюю связность | `route -n`, проверка связи `ping` с интерфейсом | **[Needs confirmation]**; [PDF p. 56](../../../rag/chunks/p0001-p0100/p0056-c01.md), [PDF p. 57](../../../rag/chunks/p0001-p0100/p0057-c01.md) |
| `sudo ip link property add dev IFACE altname ALIAS` | назначает альтернативное имя без down | `ip link show dev IFACE` | В части показана зеркальная команда `sudo ip link property del dev ALIAS altname OLD_ALIAS` для удаления altname, **но** точные идентификаторы и ограничения проверяются до применения; [PDF p. 58](../../../rag/chunks/p0001-p0100/p0058-c01.md) |

Ни одна строка `SC` не является «готовым безопасным рецептом» для рабочего сервера: нужен out-of-band доступ и план восстановления, особенно при изменении активной сетевой конфигурации. Реальные MAC/IP интерфейсов авторских машин не используются как параметры для читателя.

## API и заголовки языка C

| Объект | Назначение | RAG |
|---|---|---|
| `htonl`, `htons`, `ntohl`, `ntohs` в `<arpa/inet.h>` | порядок байтов хоста/сети | [PDF p. 15](../../../rag/chunks/p0001-p0100/p0015-c01.md) |
| `inet_pton`, `inet_ntop` в `<arpa/inet.h>` | текстовый ↔ бинарный IPv4/IPv6, `AF_INET`/`AF_INET6` | [PDF p. 33](../../../rag/chunks/p0001-p0100/p0033-c01.md), [PDF p. 34](../../../rag/chunks/p0001-p0100/p0034-c01.md) |
| `gethostbyname`, `gethostbyaddr`, `getaddrinfo`, `freeaddrinfo` в `<netdb.h>` | разрешение имён и освобождение результата | [PDF p. 37](../../../rag/chunks/p0001-p0100/p0037-c01.md) |

**Проверка принятия:** команды остаются классифицированными по эффекту; каждое изменение отделено от наблюдения, снабжено риском, проверкой и `[Needs confirmation]` для неописанного отката. См. также [реестр расхождений](source-findings.md).
