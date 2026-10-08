# Cheatsheet — глава 27: Сети дронов (FANET)

Source: `computer-networks-olifer-7e-ru-2026`, RAG p0844:c01–p0883:c01, PDF pp. 844–883; **rag_only**. В документе **нет** живых наблюдений, команд полёта и конфигурации сети.

## Symptom / problem framing

Проблему «рой теряет связь» сначала разложить на:
- radio reachability между БПЛА и наземной сетью; канал **drone–drone**, **gateway–gateway** или **drone–infrastructure**;
- централизованную/Ad Hoc/cluster topology, жизнеспособность шлюза или cluster head;
- смену положения, скорости, направление движения, межузловую дистанцию, энергию;
- IP-связность, mobility/session continuity и время обнаружения маршрута;
- длительную network partition, при которой нужен **DTN**, а не обычная end-to-end маршрутизация.

## Baseline / context

| Граница | Что различать | RAG |
|---|---|---|
| Назначение | UAV-assisted (вспомогательные узлы) и UAV-supported (ядро сети) | p0846–p0848 |
| Режим связи | Single UAV, centralized star, FANET mesh, multicluster/gateway | p0848–p0855 |
| Мобильность | 3D position, GNSS/IMU, speed/direction, nav-routing coupling | p0858–p0861 |
| Радио | Wi-Fi mesh, Sidelink, mmWave, SATCOM; coverage/LoS/BLoS | p0862–p0869 |
| IP/service | DHCP/self-config IPv6, Mobile IP, UDP/TCP/QUIC, apps | p0870–p0873 |
| Route discovery | AODV RREQ/RREP/RERR, B-ID, TTL, sequence number SN | p0874–p0880 |
| Partitioned delivery | store-carry-forward, epidemic, PROPHET, ferry | p0880–p0883 |

## Read-only checks

1. **Тип архитектуры.** Дрон только улучшает покрытие наземной сети или сам маршрутизирует пакеты в FANET? Есть ли зависимость всего роя от центра? [p0847–p0852]
2. **Топология.** Существуют ли физические соседства и логические peer links; какие кластерные лидеры и шлюзы могут перейти в другой cluster? Как обнаруживается потеря головы? [p0852–p0856]
3. **Роли полётной системы.** Что подтверждено по батарее, навигации и автопилоту отдельно от интерфейсов связи? Не диагностировать проблему управления полётом как «не работает маршрутизатор» без доказательств. [p0859–p0861]
4. **Радиоинтерфейс.** Какие фактические Wi-Fi/mesh, LTE/NR sidelink, mmWave или SATCOM, RSSI/interference/antenna geometry? Нет ли расхождения между channel design и требованиями управления vs payload throughput? [p0862–p0869]
5. **IP и mobility.** Адрес назначается DHCP/infrastructure или автоматически IPv6, есть ли смена IP между подсетями? Требуется непрерывная сессия или достаточно reconnect на уровне приложения? [p0870–p0872]
6. **AODV.** Существует ли путь в текущем connectivity graph? Получает ли узел RREP после ограниченных TTL RREQ; актуальны ли SN и next hop; было ли RERR при link break? [p0875–p0880]
7. **DTN.** Если граф разделён и route discovery не помогает, допускается ли задержка минут/часов и имеются ли storage, контактные окна, копии/дубли и лимиты передачи? Для real-time traffic DTN не является эквивалентом канала управления. [p0881–p0883]
8. **Safety boundary.** Законность полёта, бортовые системы, физические расстояния, текущие частоты, управление двигателями/миссиями — **[Needs confirmation]**; источник не является действующим эксплуатационным регламентом. [p0844]

## Interpretation

- Прохождение ping между двумя соседями не доказывает наличие полного многоскачкового маршрута; даже маршрут AODV может устареть из-за движения.
- Gateway FANET отличается от выделенной base station: внутри Ad Hoc он остаётся равноправным участником, выполняя дополнительную функцию.
- Reactive routing экономит постоянную signaling нагрузку ценой дополнительного поиска перед данными; AODV не гарантирует кратчайший путь в учебном примере.
- Наземный handover и сохранение application session — разные проблемы.
- DTN предполагает доставку при **отсутствии непрерывного пути**, но не гарантию задержки, пригодной для безопасности полёта.
- Характеристики спутников, mmWave, Sidelink и названных RFC являются данными издания, не проверенными как live/spec compliance.

## Next action

Составить read-only dependency graph: node identifier → position/time → neighbor links → interface/antenna type → role/cluster/gateway → IP → routing (AODV or other) → transport/application, отдельно обозначить storage/contact intervals DTN. Для всех полевых данных отметить источник и время. Без телеметрии и разрешённого доступа **[Needs confirmation]**.

## Modifying action

Смена траекторий, управление миссией, SATCOM/sidelink channel, TX power, лидером кластера, IP/gateway и маршрутизирующим протоколом — это **state-changing и потенциально критичные для безопасности полёта операции**. В данной главе нет платформенных CLI, подтверждённых прав доступа, flight-safety prechecks, change window или верифицированного rollback. **Не выполнять** на реальных аппаратах по учебной сводке.

## Verification / acceptance checks

- Роль assisted/supported, архитектура, failure domain и service path указаны отдельно.
- Position/mobility, radio, IP, routing и transport не смешиваются.
- RREQ/RREP/RERR отличены от DTN buffering/carrying.
- Реальные RTT, устойчивость, автономность, юридический статус и безопасность **не считаются подтверждёнными**.
- Source-findings.md отражает неточности спутников, radio standards и терминологии.

## Rollback

Для read-only анализа: **[Not applicable]**. Для любых реальных изменений нужно отдельно согласовать authority, сохранение безопасного состояния, связь с оператором, emergency procedure, исходные конфигурации, acceptance и rollback: **[Needs confirmation]**. Изменений БПЛА и сетевых элементов не проводилось.
