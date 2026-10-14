# Шпаргалка: часть II — сетевые сервисы Linux

Основание: accepted RAG PDF стр. 62–131. Предмет — эксплуатация и инструменты, не автоматический плейбук для продакшена.

## 1. Symptom / problem framing

Распределите симптом между: интерфейсами/маршрутами; DNS; состоянием сервиса; слушающим сокетом; брандмауэром; выбранным прокси или конечным клиентом. Сам факт успешного ping не доказывает работу сервиса. [PDF 63](../../../rag/chunks/p0001-p0100/p0063-c01.md), [PDF 64](../../../rag/chunks/p0001-p0100/p0064-c01.md), [PDF 101](../../../rag/chunks/p0101-p0200/p0101-c01.md), [PDF 112](../../../rag/chunks/p0101-p0200/p0112-c01.md), [PDF 130](../../../rag/chunks/p0101-p0200/p0130-c01.md).

## 2. Baseline / context

- Наблюдение: `ip link`, `route -n`, `netstat -i`, `netstat -t`; для пакетов `tcpdump`/Wireshark, для имён `host`/`dig`/`nslookup`. [PDF 62](../../../rag/chunks/p0001-p0100/p0062-c01.md), [PDF 65](../../../rag/chunks/p0001-p0100/p0065-c01.md), [PDF 66](../../../rag/chunks/p0001-p0100/p0066-c01.md), [PDF 67](../../../rag/chunks/p0001-p0100/p0067-c01.md).
- Проверки с трафиком: `ping`, `traceroute`, `nc`, `sftp`, `scp`. Netcat имеет различающиеся реализации (traditional и OpenBSD): опции следует проверять по `nc*. -h`. [PDF 64](../../../rag/chunks/p0001-p0100/p0064-c01.md), [PDF 68](../../../rag/chunks/p0001-p0100/p0068-c01.md), [PDF 69](../../../rag/chunks/p0001-p0100/p0069-c01.md), [PDF 70](../../../rag/chunks/p0001-p0100/p0070-c01.md).
- Службы: установка → конфигурация → `systemctl start` → `systemctl status` → опциональное `enable`. [PDF 70](../../../rag/chunks/p0001-p0100/p0070-c01.md), [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md).
- SSH: защищённое подключение, удалённая команда, копирование, X11; DHCP: динамические адреса с арендой; DNS: имена/кеш; UFW: правила доступа; inetd/socket units: сервис по запросу; SOCKS: посредник. [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md), [PDF 83](../../../rag/chunks/p0001-p0100/p0083-c01.md), [PDF 87](../../../rag/chunks/p0001-p0100/p0087-c01.md), [PDF 101](../../../rag/chunks/p0101-p0200/p0101-c01.md), [PDF 108](../../../rag/chunks/p0101-p0200/p0108-c01.md), [PDF 113](../../../rag/chunks/p0101-p0200/p0113-c01.md), [PDF 119](../../../rag/chunks/p0101-p0200/p0119-c01.md).

## 3. Read-only checks

~~~sh
ip link
route -n
netstat -i
netstat -t
systemctl status sshd
systemctl status dnsmasq
resolvectl status
cat /etc/resolv.conf
sudo iptables -L -v -n
ufw status verbose
sockstat -4
~~~

Наличие команды не гарантируется для каждого дистрибутива. Корни: [PDF 62](../../../rag/chunks/p0001-p0100/p0062-c01.md), [PDF 65](../../../rag/chunks/p0001-p0100/p0065-c01.md), [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md), [PDF 90](../../../rag/chunks/p0001-p0100/p0090-c01.md), [PDF 95](../../../rag/chunks/p0001-p0100/p0095-c01.md), [PDF 102](../../../rag/chunks/p0101-p0200/p0102-c01.md), [PDF 104](../../../rag/chunks/p0101-p0200/p0104-c01.md), [PDF 130](../../../rag/chunks/p0101-p0200/p0130-c01.md). `sudo` указан лишь там, где исходник требует административного доступа.

## 4. Interpretation

1. **Маршрут:** настройки интерфейса и таблица маршрутов согласуются? [PDF 63](../../../rag/chunks/p0001-p0100/p0063-c01.md).
2. **DNS:** исходный `/etc/resolv.conf` выбран? резолвер `systemd-resolved` действительно обслуживает запросы, а не просто запущен? Проверить прямым запросом `host`. [PDF 90](../../../rag/chunks/p0001-p0100/p0090-c01.md), [PDF 95](../../../rag/chunks/p0001-p0100/p0095-c01.md), [PDF 96](../../../rag/chunks/p0001-p0100/p0096-c01.md), [PDF 97](../../../rag/chunks/p0001-p0100/p0097-c01.md).
3. **Сервис:** `systemctl status SERVICE` показывает ошибку? Для DHCP книга даёт явную офлайн-проверку `dhcpd -t -cf /etc/dhcp/dhcpd.conf`. [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md), [PDF 84](../../../rag/chunks/p0001-p0100/p0084-c01.md), [PDF 85](../../../rag/chunks/p0001-p0100/p0085-c01.md).
4. **Доступ:** `iptables`/UFW управляют пакетами; активная служба не равна доступной; проверять статус правил и реальное клиентское соединение. [PDF 101](../../../rag/chunks/p0101-p0200/p0101-c01.md), [PDF 102](../../../rag/chunks/p0101-p0200/p0102-c01.md), [PDF 104](../../../rag/chunks/p0101-p0200/p0104-c01.md), [PDF 112](../../../rag/chunks/p0101-p0200/p0112-c01.md).
5. **Прокси:** режим `socksmethod: none` в книге назван небезопасным для публикации; сверять `socksify` и конфигурацию с фактическим сервером и `sockstat`. [PDF 121](../../../rag/chunks/p0101-p0200/p0121-c01.md), [PDF 123](../../../rag/chunks/p0101-p0200/p0123-c01.md), [PDF 128](../../../rag/chunks/p0101-p0200/p0128-c01.md), [PDF 130](../../../rag/chunks/p0101-p0200/p0130-c01.md).

## 5. Next action

После безопасного baseline — адресный тест для собственной разрешённой сети: `ping HOST`/ `traceroute HOST`; `host HOST DNS_SERVER`; `nc` на loopback в двух терминалах; SSH-запрос или `curl -x socks5://PROXY:PORT URL` при готовом разрешённом прокси. Все эти действия порождают трафик; передача файла также меняет содержимое целевой файловой системы. [PDF 64](../../../rag/chunks/p0001-p0100/p0064-c01.md), [PDF 68](../../../rag/chunks/p0001-p0100/p0068-c01.md), [PDF 74](../../../rag/chunks/p0001-p0100/p0074-c01.md), [PDF 94](../../../rag/chunks/p0001-p0100/p0094-c01.md), [PDF 123](../../../rag/chunks/p0101-p0200/p0123-c01.md).

## 6. Modifying action

- `apt install`, `systemctl start/enable` изменяют систему и службы; особенно DHCP-сервер может раздавать адреса клиентам LAN. Проверка: `dhcpd -t`, `systemctl status`, клиентские признаки выдачи аренды. [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md), [PDF 84](../../../rag/chunks/p0001-p0100/p0084-c01.md), [PDF 85](../../../rag/chunks/p0001-p0100/p0085-c01.md), [PDF 86](../../../rag/chunks/p0001-p0100/p0086-c01.md).
- Изменение `/etc/resolv.conf`, `resolved.conf`, dnsmasq-конфигурации меняет разрешение имён. Проверить текущий резолвер, затем конкретный `host` запрос. [PDF 91](../../../rag/chunks/p0001-p0100/p0091-c01.md), [PDF 95](../../../rag/chunks/p0001-p0100/p0095-c01.md), [PDF 96](../../../rag/chunks/p0001-p0100/p0096-c01.md), [PDF 97](../../../rag/chunks/p0001-p0100/p0097-c01.md).
- `iptables -A/-I`, `ufw enable/allow/disable` могут прекратить SSH-сеанс либо раскрыть доступ; обязательно фиксировать прежние правила и иметь альтернативный доступ. [PDF 102](../../../rag/chunks/p0101-p0200/p0102-c01.md), [PDF 104](../../../rag/chunks/p0101-p0200/p0104-c01.md), [PDF 105](../../../rag/chunks/p0101-p0200/p0105-c01.md).
- Публикация `danted` без аутентификации на общедоступном интерфейсе прямо подвергается критике самим автором; не повторять. [PDF 121](../../../rag/chunks/p0101-p0200/p0121-c01.md), [PDF 123](../../../rag/chunks/p0101-p0200/p0123-c01.md), [PDF 124](../../../rag/chunks/p0101-p0200/p0124-c01.md).
- FTP через `systemd.socket` требует исключить конкурирующий самостоятельный демон и inetd, иначе возможен конфликт порта. [PDF 115](../../../rag/chunks/p0101-p0200/p0115-c01.md), [PDF 116](../../../rag/chunks/p0101-p0200/p0116-c01.md), [PDF 117](../../../rag/chunks/p0101-p0200/p0117-c01.md).

## 7. Verification / acceptance checks

Проверки различаются: синтаксис DHCP (`dhcpd -t`), статус сервиса, слушающий порт, разрешение имени, клиентская функциональность, активные фильтры, маршрут и путь через прокси. Приведённые в книге временные задержки DNS и прокси не являются обещанием конкретных чисел в другой сети. [PDF 85](../../../rag/chunks/p0001-p0100/p0085-c01.md), [PDF 94](../../../rag/chunks/p0001-p0100/p0094-c01.md), [PDF 102](../../../rag/chunks/p0101-p0200/p0102-c01.md), [PDF 117](../../../rag/chunks/p0101-p0200/p0117-c01.md), [PDF 125](../../../rag/chunks/p0101-p0200/p0125-c01.md).

## 8. Rollback

Источник показывает `ufw delete 4` (номер конкретного правила из демонстрации) и `ufw disable`, а также остановку некоторых сервисов (`systemctl stop pure-ftpd`, `systemctl stop inetd`). Это **не** полная универсальная процедура возврата конфигурации. Для DHCP, DNS, интерфейсов, socket-unit, прокси полный точный rollback: **[Needs confirmation]**. До любых модификаций сохраняйте baseline и доступ для восстановления. [PDF 105](../../../rag/chunks/p0101-p0200/p0105-c01.md), [PDF 116](../../../rag/chunks/p0101-p0200/p0116-c01.md), [PDF 117](../../../rag/chunks/p0101-p0200/p0117-c01.md).

**Риски первоисточника:** несовпадающие `1085/1080` в SOCKS, упоминание DNS вместо DHCP, формулировка об `ssh -Y`; см. [source-findings.md](source-findings.md). Реальные пароли, токены, учётные данные и адреса автора не копируются в примеры исполнения.
