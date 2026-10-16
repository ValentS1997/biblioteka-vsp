# Глава 8 — команды, операции UI и оценка эффекта

**Источник:** RAG-only PDF 336–370. Команды здесь воспроизводят текст книги либо ясно обозначенные placeholders. Это **реестр**, не пошаговый production-script. `Read-only` / `Workload-generating` / `State-changing` / `Destructive` — классы воздействий. Учебные адреса не переносить в сеть пользователя.

## 1. Установка, база и конфигурация proxy

**Пути пакетов из текста** ([p0337](../../../rag/chunks/p0301-p0400/p0337-c01.md)–[p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md)):

```sh
# State-changing: только подготовленная RHEL 8 lab, repo URL из издания Zabbix 7.0
rpm -Uvh https://repo.zabbix.com/zabbix/7.0/rhel/8/x86_64/zabbix-release-7.0-1.el8.noarch.rpm
dnf clean all
dnf install zabbix-proxy-sqlite3 zabbix-selinux-policy

# State-changing: только Ubuntu 22.04 lab, repo URL из книги
wget https://repo.zabbix.com/zabbix/7.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_7.0-1+ubuntu22.04_all.deb
dpkg -i zabbix-release_7.0-1+ubuntu22.04_all.deb
apt update
apt install zabbix-proxy-sqlite3
```

Эти строки — исторические **конкретные версии ОС и пакетов из источника**, не подтверждённый текущий способ установки. Пакеты/ссылки извне не проверялись. Установка затрагивает репозитории и сервисы, rollback/удаление пакетов `[Needs confirmation]`. Примечание p338 допускает SELinux permissive или отключение AppArmor в lab; **нельзя переносить ослабление MAC в production** без политики безопасности.

```ini
# /etc/zabbix/zabbix_proxy.conf — State-changing при записи
ProxyMode=1
Server=<AUTHORIZED_ZABBIX_SERVER_ADDRESS>
Hostname=<EXACT_PROXY_HOSTNAME>
DBName=<PERSISTENT_PROXY_DB_PATH>
# ProxyMode=0 означает active, ProxyMode=1 означает passive
# ProxyBufferMode=<MODE_TO_VALIDATE> — источник обсуждает hybrid/memory/disk
```

Для примера авторы используют `Server=10.16.16.152`, `Hostname=lar-book-proxy-passive`, `DBName=/tmp/zabbix_proxy.sqlite3` ([p0338](../../../rag/chunks/p0301-p0400/p0338-c01.md)). **Источник не подтверждает, что `/tmp` годится для устойчивой эксплуатации.** При HA несколько Zabbix server разделяются `;`, а не `,` ([p0338](../../../rag/chunks/p0301-p0400/p0338-c01.md)).

```sh
# State-changing — включение и запуск сервиса
systemctl enable zabbix-proxy
systemctl start zabbix-proxy
# Read-only — наблюдение журнала
tail -f /var/log/zabbix/zabbix_proxy.log
```

Проверить фактическое состояние в `Administration → Proxies`: `Last seen (age)` перестаёт быть `Never` ([p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md)–[p0343](../../../rag/chunks/p0301-p0400/p0343-c01.md)). **Не выполнять** `rm /tmp/zabbix_proxy.sqlite3` из p339 как maintenance: удаляет несинхронизированный cache и может привести к необратимой потере values ([p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md)); destructive.

## 2. Пассивный и активный режимы

| Действие | Класс | Назначение и критерий |
|---|---|---|
| `Administration → Proxies → Create proxy` / `Add` | State-changing | Регистрирует proxy, имя должно соответствовать `Hostname`; Last seen возрастает/обновляется по исходному соединению ([p0341](../../../rag/chunks/p0301-p0400/p0341-c01.md)–[p0343](../../../rag/chunks/p0301-p0400/p0343-c01.md)) |
| `Encryption: No encryption` | State-changing | Только начальный учебный baseline, **plaintext** может содержать чувствительные macros; позже PSK recipe ([p0342](../../../rag/chunks/p0301-p0400/p0342-c01.md), [p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md)) |
| `Timeouts` | State-changing при сохранении | Override глобальных check timeouts в Zabbix 7, значения рисунков 8.4/8.10 = `RAG_MISS`; [p0342](../../../rag/chunks/p0301-p0400/p0342-c01.md), [p0346](../../../rag/chunks/p0301-p0400/p0346-c01.md) |
| `ProxyMode=0`, `Hostname=<EXACT_ACTIVE_PROXY>` | State-changing | Active proxy инициирует соединение с server:10051, `Proxy address` в UI — optional/whitelist по тексту; [p0345](../../../rag/chunks/p0301-p0400/p0345-c01.md)–[p0347](../../../rag/chunks/p0301-p0400/p0347-c01.md) |
| `ProxyMode=1` | State-changing | Passive proxy принимает соединение server:10051; [p0343](../../../rag/chunks/p0301-p0400/p0343-c01.md) |
| `systemctl restart Zabbix-proxy` | **Source code mismatch** | На p347 `Zabbix-proxy` написано с прописной буквы (при `systemctl start zabbix-proxy` на p339). Не считать гарантированно рабочим unit; `[Needs confirmation]` |

Изменение работы proxy — риск потери связи/сбора; `Last seen` может обновиться не сразу. Полная процедура rollback не дана.

## 3. Переключение мониторинга на proxy

`Data collection → Hosts → <HOST> → Monitored by → Proxy → Select <PROXY> → Update` — **State-changing**. Source p348–349 связывает SNMP host с passive proxy, другой active agent host с active proxy. Для active Agent 2:

```ini
# /etc/zabbix/zabbix_agent2.conf — State-changing при записи
ServerActive=<AUTHORIZED_PROXY_ADDRESS>
```

Это определяет, куда агент будет передавать данные. После переноса источник допускает временно серый индикатор SNMP до получения новой конфигурации ([p0348](../../../rag/chunks/p0301-p0400/p0348-c01.md)–[p0350](../../../rag/chunks/p0301-p0400/p0350-c01.md)). Подтверждать факт новых значений через Latest data и конфигурацию, а не только UI status.

## 4. PSK — источник содержит дефектные команды

```ini
# /etc/zabbix/zabbix_proxy.conf — State-changing
TLSConnect=psk
TLSAccept=psk
TLSPSKIdentity=<UNIQUE_PROXY_IDENTITY>
TLSPSKFile=/etc/zabbix/proxy_psk.key
```

```sh
# State-changing, secret material; источник p353
openssl rand -hex 128 > /etc/zabbix/proxy_psk.key
```

**Не показывать/копировать секрет** из файла с помощью `cat`, хотя книга предлагает это для проверки ([p0353](../../../rag/chunks/p0301-p0400/p0353-c01.md)). Исходная строка p354 `chmod 400/etc/zabbix/proxy_psk.key` имеет слитные аргументы, `Systemctl restart zabbix-proxy` — ошибочный регистр команды. Обе **не приводятся здесь как исполнимые**; варианты и исходниковое `chown zabbix:zabbix /etc/zabbix/proxy_psk.key` сохранены в [source-findings.md](source-findings.md). Корректные права/ключевая ротация требуют `[Needs confirmation]`.

`Administration → Proxies → Encryption`: для passive `Connections to proxy: PSK`, для active `Connections from proxy: PSK`; должны совпасть identity и secret. **State-changing**, переключение обеих сторон может временно прервать соединение; критерий — обновляющийся Last seen. Не включать «No encryption» вместо корректировки PSK.

## 5. Proxy groups, HA, failover

`Administration → Proxy groups → Create proxy group` → задать name `lar-proxy-group`; затем `Administration → Proxies` привязать оба proxy к группе и заполнить `Address for active agents`, а для host выбрать `Monitored by → Proxy group`. Всё **State-changing** ([p0356](../../../rag/chunks/p0301-p0400/p0356-c01.md)–[p0358](../../../rag/chunks/p0301-p0400/p0358-c01.md)).

Источник показывает:

```ini
# /etc/zabbix/zabbix_agent2.conf — учебная конфигурация из p358,
# State-changing; адреса нужно заменить на согласованный lab scope.
ServerActive=192.168.2.175,192.168.2.174
Hostname=lar-book-proxyha-test
```

Условия: оба proxy работают и имеют адреса для active agents; source не даёт точных UI-policies в изображениях. `Minimum number of proxies` и `Failover period` выбираются с учётом доступной мощности и поведения группы. При SNMP trapper автор прямо предупреждает, что стандартного group failover может быть недостаточно — может потребоваться доставка traps на все proxy ([p0359](../../../rag/chunks/p0301-p0400/p0359-c01.md)–[p0360](../../../rag/chunks/p0301-p0400/p0360-c01.md)). Возврат прежнего состояния/избежание потерь `[Needs confirmation]`.

## 6. Network Discovery и active agent autoregistration через proxy

`Data collection → Discovery → Discover Zabbix Agent Hosts → Discovery by → Proxy → Update` (**State-changing**) делегирует сканирование proxy. Agent config `Server` с разрешёнными адресами / `ServerActive=<PROXY>`, restart agent — **State-changing**. На Linux p361 — `systemctl restart zabbix-agent2`; Windows p361 — `zabbix_agent2.exe --stop` / `zabbix_agent2.exe --start` (State-changing). Источниковое имя Windows config пути отличается от главы 7, см. findings.

**Destructive:** p361–362 предлагает **удалить** ранее созданные `lar-book-disc-lnx`, `lar-book-disc-win`, `lar-book-lnx-agent-auto` для демонстрации, чтобы избежать дублей. Это не безопасная операция при наличии истории. Не исполнять без экспорта/backup и заранее доказанного восстановления. `RAG_MISS` — точные условия в рисунках.

## 7. Мониторинг proxy local и remote

| Операция | Класс | Что проверять |
|---|---|---|
| `dnf install zabbix-agent2` / `apt install zabbix-agent2` на proxy | State-changing | Установка локального агента, host monitored by proxy; p364 |
| `Server=127.0.0.1`, `ServerActive=127.0.0.1`, `Hostname=lar-book-proxy-active` | State-changing | Локальный мониторинг и внутренние проверки proxy, p364 |
| Добавить host с `Monitored by proxy` и шаблонами | State-changing | Проверить `Latest data` values/percent fill, p364–366 |
| `StatsAllowedIP=127.0.0.1,<ZABBIX_SERVER_IP>` в proxy config | State-changing, security-sensitive | Разрешает remote stats только указанным источникам, p366 |
| Отдельный host + `Remote Zabbix proxy health` + адрес/порт в Macros | State-changing | Проверка server→proxy, p366–369 |
| `Administration → Queue → Queue overview by proxy` | Read-only | Задержки 5s, 10s, 30s, 1m, 5m, >10m; p368–370 |

Источник **не предоставляет** всех значений двух remote macros на рис. 8.38: `RAG_MISS`; не выдумывать их названия/значения. Как применить изменения `StatsAllowedIP` в конкретном режиме и проверить аутентификацию `[Needs confirmation]`.

## Приёмка и rollback

До модификаций фиксировать исходную конфигурацию, owners/secrets/кэш. После каждой — проверять журнал, Last seen, Latest data, queue и нужный monitoring path. Не трактовать автоматическое `rm` SQLite, отключение SELinux/AppArmor или удаление hosts как рутинную диагностику. **Полный rollback и восстановление потерянных данных не описаны**.
