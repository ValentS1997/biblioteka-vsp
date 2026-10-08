# Cheatsheet — глава 31: защита транспортной инфраструктуры сети

Source: `computer-networks-olifer-7e-ru-2026`, PDF 991–1022, RAG 33 чанка (p0991:c01–p1022:c01 + p1019:c02); **rag_only**. Ниже — учебные критерии и безопасная диагностика, **не** руководство по атакам или вмешательству в работающий трафик.

## Symptom / problem framing

Возможные симптомы: новые TCP-сессии не устанавливаются, а half-open backlog растёт; внезапные RST, потери ICMP/UDP и latency; хост использует неожиданный next hop; DNS выдаёт неподтверждённое соответствие; увеличивается отражённый трафик; BGP изменяет origin/prefix/AS path; IPsec SA не создаётся или inbound SPD отклоняет пакеты.

Отделять **симптом сервиса**, механизм TCP/IP/DNS/BGP, возможную атаку/ошибку конфигурации, наблюдаемые данные и требуемое защитное решение.

## Baseline / context

| Поверхность | Что фиксировать read-only | RAG |
|---|---|---|
| TCP | новые vs завершённые handshake, backlog, RST, retransmission | p0991–p0994 |
| Anti-spoofing | источники, интерфейсы, reverse-path behavior, multihoming | p0992–p0993 |
| ICMP / UDP | rate, unreachable, unexpected redirect; адреса, направление | p0995–p0999 |
| IP | IPv4 options, IPv6 extension headers, fragmentation/reassembly errors | p0999–p1000 |
| Recon | baseline discovery logs и авторизованные inventory events | p1000–p1002 |
| DNS | ответ/авторитетность, signed response status, recursive access, transfer ACL | p1002–p1006 |
| BGP | announced origin, prefix specificity, AS path, intended routing policy | p1006–p1009 |
| Channel | end-host vs gateway trust boundary, transport vs tunnel mode | p1009–p1016 |
| IPsec | AH/ESP/IKE, SA directions, SPI/SN, selector SPD, SAD, expiry | p1013–p1022 |

## Read-only checks

1. **TCP availability.** Есть ли рост незавершённых соединений и ошибки легального подключения; как correlate это с метриками сервера/edge? SYN cookies и лимиты — только потенциальные меры, не настройки из учебника. [p0991–p0993]
2. **Source validation.** Сопоставить source IP, interface, routing и провайдерскую топологию. Reverse Path Check может ошибочно отбрасывать legitimate traffic при asymmetric/multihomed routing; конкретная политика неизвестна. [p0992–p0993]
3. **TCP sessions.** Разделить неожиданный RST и retransmission, факты подделки от обычной потери/timeout. Не утверждать injection без evidence. [p0993–p0994]
4. **ICMP/UDP.** Проверить неожиданное redirect, growth echo/unreachable, reflection patterns. Наличие ICMP не означает автоматически attack, а фильтрация любого ICMP может нарушить работу сети. [p0995–p0999]
5. **IP/options/fragments.** Связаны ли packet drops или IDS misclassifications с unusual headers/reassembly? Исторические crashes из книги не подтверждают текущую уязвимость. [p0999–p1000]
6. **Recon event.** Сопоставить inventory/log owner, scheduled network scans и признаки чужой активности; не проводить сторонних probes без разрешения. [p1000–p1002]
7. **DNS.** Наблюдался ли аномальный ответ, корректна ли zone/recursive policy, есть ли подтверждённая DNSSEC validation и защита auth-zone transfer? Не брать риск из одной подозрительной записи за факт компрометации. [p1002–p1006]
8. **BGP.** Кто authoritative owner prefix; соответствуют ли announced more-specific prefix/AS path change policy? Исторические AS7007 и YouTube incidents — иллюстрации, не IOC. [p1006–p1009]
9. **Secure channel.** Между кем завершается защита — host или gateways? Какая часть пути вне криптографической границы? Не называть tunnel end-to-end между приложениями, если шифрование начинается лишь на SG. [p1009–p1016]
10. **IPsec processing.** Какие inbound/outbound SPD selectors, SAD/SA, AH или ESP, transport/tunnel, SPI, sequence/replay window, IKE status? Для двустороннего трафика требуются две направленные SA. [p1013–p1022]

## Interpretation

- Traffic spike сам по себе не идентифицирует злоумышленника; source spoofing и отражение затрудняют attribution.
- Устаревшие сценарии Ping of Death / Smurf нельзя трактовать как текущий дефект любой ОС или глобальной routing policy.
- DNSSEC подтверждает данные в описанных предпосылках; само по себе не обеспечивает uptime при DDoS.
- BGP hijack и ошибка route advertisement могут иметь одинаковые последствия и разную причинность.
- AH не шифрует данные; ESP поддерживает confidentiality и дополнительные функции; IKE согласует параметры SA.
- SPD отвечает на вопрос **что делать с пакетом**, SAD — **с какими текущими параметрами SA**, SPI — идентификатор входящей SA.
- DES, MD5, SHA-1, PPTP, SSL и raw illustrative IPSec details — описание версии книги, а не безопасная современная конфигурация.

## Next action

Только при наличии разрешённого доступа составить read-only evidence matrix: service baseline, relevant logs, expected BGP/DNS changes, ingress source validation, approved route/prefix inventory, trusted channel endpoints и фактические SA/SPD/SAD summaries **без секретов**. Отделять observed, source claim, inference и unknown. Все live values **[Needs confirmation]**.

## Modifying action

Не менять router anti-spoofing, TCP mitigation, DNSSEC keys, DNS recursor/zone transfer, BGP import/export, IPsec selectors, IKE, SA algorithms/keys, tunnel endpoint или client routes на основании этого конспекта. Любое изменение может разорвать доступ, нарушить BGP reachability или утратить секреты. Не выполнять нагрузочные тесты и не генерировать трафик атак.

## Verification / acceptance checks

- Для каждого suspect event подтверждены baseline и corroborating evidence.
- Различены TCP/ICMP/UDP/IP атаки, DNS/BGP control-plane и IPsec data plane.
- Документированы границы tunnel/transport, AH vs ESP vs IKE, SA/SPI/SPD/SAD.
- Не сделано выводов «уязвимость доказана», «атака идёт» или «канал безопасен» без фактических измерений.
- Книжные крипто-алгоритмы не приняты как нормативные defaults.

## Rollback

Read-only анализ: **[Not applicable]**. Реальные изменения: owner, approved scope, сохранённая конфигурация и ключевая политика, out-of-band access, validation, окно работ и tested rollback: **[Needs confirmation]**. Реальные системы не изменялись.
