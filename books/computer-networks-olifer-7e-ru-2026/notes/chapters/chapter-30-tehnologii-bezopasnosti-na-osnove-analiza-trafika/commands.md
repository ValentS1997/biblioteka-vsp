# Команды и протокольные операции — глава 30

Источник: PDF 955–990, RAG p0955:c01–p0990:c01 и p0978:c02; **rag_only**.

## Граница применимости

В главе **есть** Cisco ACL и Linux `iptables` примеры. Их формат относится к показанной модели/версии издания и иногда повреждён текстовым извлечением. Ни один не является безопасным production runbook. **Прямое выполнение ACL может заблокировать удалённое управление или сделать уязвимую зону доступной**. Требуются права, платформа, версии, окно работ и verified rollback: [Needs confirmation].

## Непосредственно приведённые исходником элементы

| Элемент / пример источника | Смысл | Режим / caveat | RAG |
|---|---|---|---|
| `access-list` | Cisco-style numbered ACL | конфигурация, **state-changing** | [p0957](../../../rag/chunks/p0901-p1000/p0957-c01.md) |
| `permit`, `deny` | принять/отбросить совпавший пакет | порядок условий до первого match; **state-changing** | [p0957](../../../rag/chunks/p0901-p1000/p0957-c01.md)–[p0958](../../../rag/chunks/p0901-p1000/p0958-c01.md) |
| `any`, `host`, wildcard mask | source/destination match | текст `апу` повреждён OCR | [p0957](../../../rag/chunks/p0901-p1000/p0957-c01.md)–[p0958](../../../rag/chunks/p0901-p1000/p0958-c01.md) |
| `eq`, `lt`, `gt` | port/comparison qualifiers | валидность и позиция требуют vendor check | [p0958](../../../rag/chunks/p0901-p1000/p0958-c01.md) |
| `in`, `out` | ingress/egress direction | строка `access-list 1 in` о привязке к interface **не подтверждена как исполнимая** | [p0958](../../../rag/chunks/p0901-p1000/p0958-c01.md) |
| `established` | условие ACK-bit в модели книги | **не** stateful session proof | [p0958](../../../rag/chunks/p0901-p1000/p0958-c01.md) |
| `log` | опциональная запись срабатывания ACL в syslog | мониторинг может добавить нагрузку; **state-changing** | [p0959](../../../rag/chunks/p0901-p1000/p0959-c01.md) |
| `iptables -L` | **в тексте** получение списка текущих Linux-фильтров | read-only display на соответствующей платформе; не универсален по дистрибутивам | [p0966](../../../rag/chunks/p0901-p1000/p0966-c01.md) |
| INPUT / OUTPUT / FORWARD | входящий/исходящий/транзитный traffic на host | изменения rule-chain **state-changing** | [p0966](../../../rag/chunks/p0901-p1000/p0966-c01.md) |
| RELATED / ESTABLISHED / NEW | присутствуют в source `iptables` listing | противоречит фразе о «stateless host firewall» | [p0966](../../../rag/chunks/p0901-p1000/p0966-c01.md) |

## Source-only конфигурационные фрагменты

Исторический образец **не применять**: `access-list 1 deny 192.78.46.0 0.0.0.255` — в учебном описании запрещает пакет с source в указанной сети; [p0957](../../../rag/chunks/p0901-p1000/p0957-c01.md). Далее книга ставит permit конкретного host **перед** deny остальной подсети [p0958](../../../rag/chunks/p0901-p1000/p0958-c01.md). Это иллюстрация важности порядка, не утверждение о соответствии действующей device config.

Другой проблемный source fragment — `access-list 1 in` как якобы команда включения фильтрации на интерфейсе [p0958](../../../rag/chunks/p0901-p1000/p0958-c01.md). В findings зарегистрирована **непроверенная валидность**. Не подставлять предполагаемые рабочие аналоги по памяти модели.

Листинг `iptables -L` на [p0966](../../../rag/chunks/p0901-p1000/p0966-c01.md) содержит `ACCEPT`, `REJECT`, `state NEW`, `RELATED,ESTABLISHED`. Приведённые там имена порта/интерфейса, таблицы и положения правил нельзя переносить в другую ОС без отдельной верификации.

## Другие именованные операции (не shell CLI)

| Операция | Класс | Опора RAG |
|---|---|---|
| Proxy policy, application cache, user authentication | state-changing configuration / read-only inspect | p0967–p0970 |
| DHCP reservation for server | state-changing address mapping | p0967 |
| Basic NAT / NAPT binding (IP, port) | state-changing translation / read-only table check | p0972–p0976 |
| Switch mirror/SPAN + promiscuous capture | workload, **privacy-sensitive**; enable state-changing | p0977–p0978 |
| Wireshark capture filter / display filter, PCAP | capture **privacy-sensitive**, display read-only for existing sample | p0978–p0979 |
| NetFlow exporter / collector / analyzer / sampling | enabling telemetry state-changing; reading reports read-only | p0979–p0981 |
| IDS alert vs IPS blocking | reading alert read-only; automatic block state-changing | p0982–p0984 |
| Audit log retention/verification | evidence operations; changing retention state-changing | p0984–p0986 |
| Firewall DMZ/interzone policy | state-changing, may disrupt service | p0986–p0990 |

## Prechecks, verification and rollback

**Read-only:** inspect existing approved policy/flow tables, logs, counters, PCAP files within permissions. **Potential workload/collection:** packet capture, port mirroring, NetFlow export and IPS analysis. **State-changing:** ACL/firewall/NAT/DHCP/proxy/IDS/IPS interzone rule changes. Preserve out-of-band management access; define expected allowed/denied flows and rollback before modifying anything. Actual device vendor/version, interface, policy authorizations and post-check: **[Needs confirmation]**. No commands were run.
