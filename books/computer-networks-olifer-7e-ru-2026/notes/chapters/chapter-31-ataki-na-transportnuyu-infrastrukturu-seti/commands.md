# Команды и протокольные операции — глава 31

Канонический источник: PDF 991–1022, RAG p0991:c01–p1022:c01 + p1019:c02; **rag_only**.

## Исполнимые CLI

**В главе нет подтверждённого безопасного runbook для диагностики или изменения DNS, BGP, IPsec и транспортных протоколов на конкретной платформе.** Приёмы сканирования, подделки сегментов и генерации отказов в обслуживании являются *описаниями угроз*, а не допустимыми командами для исполнения. Здесь они не воспроизводятся пошагово.

## Сетевые механизмы и признаки (source-only)

| Механизм | Что означает в тексте | Режим наблюдения и безопасность | RAG |
|---|---|---|---|
| TCP SYN / SYN-ACK / ACK | Establishment state, риск half-open exhaustion | read-only counters/telemetry; тест нагрузки запрещён без scope | p0991–p0993 |
| SYN cookies | Защитная концепция, снижающая потребление server state до handshake | настройка state-changing, platform verification required | p0993 |
| Reverse Path Check (RPC, название автора) | Проверка допустимости source route на ingress; multihoming caveat | изменение source validation state-changing | p0992–p0993 |
| TCP sequence number / RST | Маркеры целостности TCP exchange и завершения | читать только санкционированную телеметрию | p0993–p0994 |
| ICMP Redirect / Echo / Unreachable | Control-plane/diagnostic messages | избегать широкого blanket-block без проверки зависимостей | p0995–p0998 |
| UDP / ICMP reflection | Категория нежелательного отражённого трафика | анализ counters/flow records, не генерация отражения | p0998–p0999 |
| IPv4 IP options / IPv6 hop-by-hop | Пакетные параметры, влияющие на forwarding performance | filtering state-changing | p0999–p1000 |
| Fragment overlap / reassembly | Различия в обработке фрагментов, потенциальный bypass/ошибка | analysis only; не формировать аномальные фрагменты | p1000 |
| Discovery/recon indicators | События инвентаризации, scans и контроля доступа | owner/scope должен быть установлен до любых probes | p1000–p1002 |

## DNS/BGP: защитные операции

| Элемент | Назначение в источнике | Класс | RAG |
|---|---|---|---|
| DNS authoritative/recursive role | Область доверия источника DNS-ответов | чтение конфигурации и audit, write state-changing | p1002–p1006 |
| Zone transfer restrictions | Передача зон только уполномоченным secondary | конфигурация state-changing | p1006 |
| DNSSEC validation/signatures | Проверка подлинности ответов DNS | текущий trust chain unknown | p1006 |
| BGP AS-path/origin/prefix | Принадлежность и распространение маршрута | read-only route inventory | p1007–p1009 |
| BGP import/export filtering | Ограничения доверия маршрутов и policy | state-changing; риск глобальной недоступности | p1007–p1009 |
| DNS/BGP historical incidents | Примеры для моделирования рисков, не текущие IOC | read-only historical learning | p1003–p1009 |

## IPsec: компоненты SA

| Компонент | Назначение по RAG | Side effect | RAG |
|---|---|---|---|
| AH | Подлинность/целостность и optional anti-replay без шифрования | security operation, read-only review possible | p1013, p1017–p1018 |
| ESP | Конфиденциальность; отдельная optional integrity/authentication | security operation | p1013, p1018–p1019 |
| IKE | Согласование параметров/секретов по сторонам канала | setup и key-management state-changing | p1013–p1014 |
| SA | Однонаправленная ассоциация — пары для duplex traffic | создание/удаление state-changing | p1014 |
| Transport mode | Исходный IP header остаётся для forwarding | выбор tunnel mode state-changing | p1015 |
| Tunnel mode | Original IP packet внутри outer IP packet | gateway/host endpoint config state-changing | p1015–p1016 |
| SPI / SN | SA index и счётчик anti-replay | значения read-only без ключевого материала | p1017–p1021 |
| SAD | Параметры действующих входящих/исходящих SA | contains secrets; **не экспортировать ключи** | p1020–p1022 |
| SPD selector / protect / bypass / discard | Матрица политики для IP packets, исходящий/inbound decision | policy modifications state-changing | p1020–p1022 |

## Обозначения, но НЕ шаблоны конфигурации

- `SA` — Security Association (направленная); `SAD` — Security Associations Database, `SPD` — Security Policy Database.
- `SPI` — Security Parameters Index; `SN` — Sequence Number. Source-only anti-replay window приведён как иллюстративный диапазон, не настройка по умолчанию.
- `AH`, `ESP`, `IKE` — отдельные функции IPsec. Пример MD5/SHA-1/DES/Triple DES историчен; current cipher suites **[Needs confirmation]**.
- `S/MIME`, `TLS`, `PPTP`, `IPsec` приведены в иерархии автора, а не как взаимозаменяемые safe protocols.

## Preconditions / verification / rollback

Не проводить активное сетевое сканирование, DDoS testing, подделку DNS/BGP/transport packets, изменение маршрутизации, IKE/SA или закрытых ключей на основании данного файла. Read-only проверка разрешённых журналов и сводных telemetry counters возможна только при подтверждённых полномочиях. Действительная платформа, тесты, change approval, backup конфигурации и rollback **[Needs confirmation]**. Никаких команд не выполнялось.
