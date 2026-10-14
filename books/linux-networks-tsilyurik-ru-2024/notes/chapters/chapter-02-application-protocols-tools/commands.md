# Команды части II: только подтверждённое RAG

**Классы:** RO = наблюдение конфигурации; WG = сетевые запросы / нагрузка / передача данных; SC = изменение конфигурации, файлов, правил или процессов. Placeholder'ы `HOST`, `USER`, `SERVICE`, `IFACE`, `PROXY`, `FILE`, `DNS_SERVER` заменяются на данные **разрешённого** тестового окружения. Копирование может относиться одновременно к WG и SC (запись файла); удалённая команда SSH классифицируется по содержимому команды.

## Read-only — RO

| Команда/утилита из части II | Назначение | RAG |
|---|---|---|
| `ip link`, `route -n`, `ifconfig` | сетевые интерфейсы, таблица маршрутов | [PDF 62](../../../rag/chunks/p0001-p0100/p0062-c01.md), [PDF 63](../../../rag/chunks/p0001-p0100/p0063-c01.md) |
| `netstat -i`, `netstat -t` | статистика адаптеров, TCP-сессии | [PDF 65](../../../rag/chunks/p0001-p0100/p0065-c01.md) |
| `systemctl status SERVICE`, `pgrep sshd` | состояние службы и процессы | [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md), [PDF 72](../../../rag/chunks/p0001-p0100/p0072-c01.md) |
| `cat /etc/resolv.conf`, `resolvectl status` | системное разрешение DNS | [PDF 90](../../../rag/chunks/p0001-p0100/p0090-c01.md), [PDF 95](../../../rag/chunks/p0001-p0100/p0095-c01.md), [PDF 96](../../../rag/chunks/p0001-p0100/p0096-c01.md) |
| `sudo iptables -L -v -n`, `ufw status numbered` | правила пакетной фильтрации | [PDF 102](../../../rag/chunks/p0101-p0200/p0102-c01.md), [PDF 104](../../../rag/chunks/p0101-p0200/p0104-c01.md) |
| `netstat -lptu`, `sockstat -4` | слушатели и клиентские сокеты | [PDF 112](../../../rag/chunks/p0101-p0200/p0112-c01.md), [PDF 130](../../../rag/chunks/p0101-p0200/p0130-c01.md) |
| `systemctl status pure-ftpd.socket` | состояние socket activation | [PDF 117](../../../rag/chunks/p0101-p0200/p0117-c01.md) |
| `update-alternatives --display nc`, `nc.traditional -h`, `nc.openbsd -h` | вариант Netcat и доступные опции | [PDF 69](../../../rag/chunks/p0001-p0100/p0069-c01.md), [PDF 70](../../../rag/chunks/p0001-p0100/p0070-c01.md) |
| `dhcpd -t -cf /etc/dhcp/dhcpd.conf` | синтаксис DHCP-конфига, до запуска демона | [PDF 85](../../../rag/chunks/p0001-p0100/p0085-c01.md) |

## Workload-generating — WG

| Подтверждённый синтаксис/форма | Эффект, риск и проверка | RAG |
|---|---|---|
| `ping HOST`, `traceroute HOST` | ICMP-пакеты и трассировка; оценивать потери/хопы | [PDF 64](../../../rag/chunks/p0001-p0100/p0064-c01.md) |
| `nslookup HOST`, `host HOST`, `dig HOST` | DNS-запросы; ответ зависит от резолвера | [PDF 65](../../../rag/chunks/p0001-p0100/p0065-c01.md), [PDF 66](../../../rag/chunks/p0001-p0100/p0066-c01.md) |
| `sudo tcpdump -i IFACE` | наблюдение живого трафика, может захватывать чувствительные сведения; в книге ARP/ICMP | [PDF 67](../../../rag/chunks/p0001-p0100/p0067-c01.md) |
| `nc -l 1234` и `nc 127.0.0.1 1234` | TCP-тест в двух терминалах localhost; CLI зависит от реализации | [PDF 68](../../../rag/chunks/p0001-p0100/p0068-c01.md), [PDF 69](../../../rag/chunks/p0001-p0100/p0069-c01.md) |
| `ssh USER@HOST`, `ssh USER@HOST df -h` | удалённая сессия/команда; не произвольная безопасная команда | [PDF 72](../../../rag/chunks/p0001-p0100/p0072-c01.md), [PDF 74](../../../rag/chunks/p0001-p0100/p0074-c01.md) |
| `sftp USER@HOST:FILE`, `scp USER@HOST:FILE LOCAL_FILE` | читает источник и пишет файл; опасность перезаписи цели | [PDF 68](../../../rag/chunks/p0001-p0100/p0068-c01.md), [PDF 75](../../../rag/chunks/p0001-p0100/p0075-c01.md), [PDF 76](../../../rag/chunks/p0001-p0100/p0076-c01.md) |
| `ssh -X USER@HOST xclock` | графическое X11-приложение на удалённом хосте | [PDF 80](../../../rag/chunks/p0001-p0100/p0080-c01.md) |
| `host -v HOST DNS_SERVER` | запрос к выбранному DNS, сравнение повторов | [PDF 94](../../../rag/chunks/p0001-p0100/p0094-c01.md) |
| `ssh -N -D 5555 USER@HOST` | локальный SOCKS через SSH на порту 5555; держит работающий процесс | [PDF 126](../../../rag/chunks/p0101-p0200/p0126-c01.md) |
| `curl -x socks5://127.0.0.1:5555 URL` | контроль через собственный локальный SOCKS | [PDF 126](../../../rag/chunks/p0101-p0200/p0126-c01.md) |
| `socksify curl --noproxy '*' URL` | запрос через конфигурацию Dante-клиента | [PDF 128](../../../rag/chunks/p0101-p0200/p0128-c01.md), [PDF 129](../../../rag/chunks/p0101-p0200/p0129-c01.md) |

Команды WG применяются только к ресурсам, на использование которых есть разрешение. Пароли в SSH-примерах не встраиваются; проверку копирования делайте в отдельном каталоге и не затирайте данные.

## State-changing — SC

| Команда/операция из RAG | Изменение/риск | Проверка | Откат |
|---|---|---|---|
| `sudo apt install isc-dhcp-server` | новая служба DHCP и зависимости | `systemctl status isc-dhcp-server` | [Needs confirmation]; [PDF 84](../../../rag/chunks/p0001-p0100/p0084-c01.md) |
| правка `/etc/dhcp/dhcpd.conf` и `/etc/default/isc-dhcp-server` | пулы IP, адресация клиентов LAN | `dhcpd -t -cf /etc/dhcp/dhcpd.conf`, затем статус сервиса | [Needs confirmation]; [PDF 84](../../../rag/chunks/p0001-p0100/p0084-c01.md), [PDF 85](../../../rag/chunks/p0001-p0100/p0085-c01.md) |
| `sudo systemctl start SERVICE`; `sudo systemctl enable SERVICE` | активирует службу и автозапуск, возможное открытие порта | `systemctl status SERVICE` | [Needs confirmation]; [PDF 71](../../../rag/chunks/p0001-p0100/p0071-c01.md) |
| `sudo apt install dnsmasq`; правка `/etc/dnsmasq.conf` и файлов `/etc/dnsmasq.d/` | DHCP/DNS на выбранном интерфейсе | `systemctl status dnsmasq`, `host -v HOST DNS_SERVER` | [Needs confirmation]; [PDF 90](../../../rag/chunks/p0001-p0100/p0090-c01.md), [PDF 91](../../../rag/chunks/p0001-p0100/p0091-c01.md), [PDF 92](../../../rag/chunks/p0001-p0100/p0092-c01.md), [PDF 94](../../../rag/chunks/p0001-p0100/p0094-c01.md) |
| настройка `/etc/systemd/resolved.conf`, запуск `systemd-resolved`, замена `/etc/resolv.conf` | меняет DNS-цепочку, риск потери разрешения имён | `resolvectl status`, `cat /etc/resolv.conf`, `host HOST` | источник предлагает сохранить старый конфиг, точный возврат [Needs confirmation]; [PDF 95](../../../rag/chunks/p0001-p0100/p0095-c01.md), [PDF 96](../../../rag/chunks/p0001-p0100/p0096-c01.md), [PDF 97](../../../rag/chunks/p0001-p0100/p0097-c01.md) |
| `iptables -t filter -A INPUT -s NETWORK -j DROP` | блокирует источник; риск прервать доступ | `sudo iptables -L -v -n` | [Needs confirmation]; [PDF 102](../../../rag/chunks/p0101-p0200/p0102-c01.md) |
| `ufw enable`, `ufw allow OpenSSH`, `ufw delete RULE_NO`, `ufw disable` | меняет доступность портов; при `enable` книга предупреждает о SSH | `ufw status numbered`, клиентский тест | `delete`/`disable` есть в тексте, полное восстановление [Needs confirmation]; [PDF 104](../../../rag/chunks/p0101-p0200/p0104-c01.md), [PDF 105](../../../rag/chunks/p0101-p0200/p0105-c01.md) |
| правка `/etc/inetd.conf`, `systemctl start inetd` | включает слушатель и порождает серверы по запросу | `netstat -lptu` и проверка службы | `systemctl stop inetd` показана, конфигурация [Needs confirmation]; [PDF 109](../../../rag/chunks/p0101-p0200/p0109-c01.md), [PDF 111](../../../rag/chunks/p0101-p0200/p0111-c01.md), [PDF 116](../../../rag/chunks/p0101-p0200/p0116-c01.md) |
| создание `pure-ftpd.socket` / `pure-ftpd@.service` и `systemctl start pure-ftpd.socket` | новый слушатель FTP; конфликт с имеющимся `pure-ftpd` | `systemctl status pure-ftpd.socket`, разрешённый клиент `ftp` | [Needs confirmation]; [PDF 115](../../../rag/chunks/p0101-p0200/p0115-c01.md), [PDF 116](../../../rag/chunks/p0101-p0200/p0116-c01.md), [PDF 117](../../../rag/chunks/p0101-p0200/p0117-c01.md) |
| правка `/etc/danted.conf`, `systemctl start danted` | публикует SOCKS; **без аутентификации — запрещённая практика** | `systemctl status danted`, разрешённый proxy-запрос | [Needs confirmation]; [PDF 121](../../../rag/chunks/p0101-p0200/p0121-c01.md), [PDF 122](../../../rag/chunks/p0101-p0200/p0122-c01.md), [PDF 123](../../../rag/chunks/p0101-p0200/p0123-c01.md) |
| `useradd --shell /usr/sbin/nologin USER`, `passwd USER`, `usermod -a -G proxy USER` | создаёт учётную запись и разрешения прокси | просмотр соответствующих локальных записей, без секретов | [Needs confirmation]; [PDF 124](../../../rag/chunks/p0101-p0200/p0124-c01.md) |

**Ограничение источника:** учебные примеры с `sshpass -p` и `curl -x socks5://USER:PASSWORD@...` не перепечатываются с паролями; адреса и логины исходного стенда заменены placeholders. Open-proxy с `socksmethod: none` не публиковать: автор прямо описывает злоупотребления после его запуска. [PDF 82](../../../rag/chunks/p0001-p0100/p0082-c01.md), [PDF 121](../../../rag/chunks/p0101-p0200/p0121-c01.md), [PDF 123](../../../rag/chunks/p0101-p0200/p0123-c01.md), [PDF 125](../../../rag/chunks/p0101-p0200/p0125-c01.md).

Не исправлять несогласованные значения SOСKS `1080/1085` или утверждение об `ssh -Y` на основании памяти; см. [source-findings.md](source-findings.md).
