# Cheatsheet — глава 30: traffic-based security

Source: `computer-networks-olifer-7e-ru-2026`, PDF 955–990; 37 RAG chunks (p0955:c01–p0990:c01, включая p0978:c02). **rag_only**. Ни один результат мониторинга или теста реальной сети не предполагается известным.

## Symptom / problem framing

Симптомы: разрешённый трафик не проходит через firewall; заблокированный трафик обходит его; клиент не работает через proxy; после DHCP lease filter применяет старый IP; внешний сервис не видит NAPT reply; NetFlow показывает неполные/необычные потоки; IDS не видит подозрительное событие; audit logs отсутствуют; компрометация DMZ позволяет обратиться к внутреннему серверу.

Определить компонент: **routing/filter → stateful firewall → application proxy → NAT/NAPT → packet capture/flow exporter → IDS/IPS → audit → interzone policy**. Сходные симптомы имеют разные места отказа.

## Baseline / context

| Уровень | Проверяемые объекты | RAG |
|---|---|---|
| Filtering | IP src/dst, ports, protocols, interface, direction, ACL match order | p0955–p0959 |
| Firewall | stateless/stateful, session table, network/session/app inspection | p0959–p0966 |
| Host/DHCP | INPUT/OUTPUT/FORWARD, RELATED/ESTABLISHED/NEW, lease/static binding | p0966–p0967 |
| Proxy | клиентский путь, user/content policy, cache, application/session | p0967–p0970 |
| NAT/NAPT | internal/global IP, source port translation, mapping table, reply | p0971–p0976 |
| Packet analyzer | SPAN/mirror, promiscuous mode, capture/display filter, PCAP | p0977–p0979 + p0978:c02 |
| NetFlow | exporter, collector, analyzer, full/sampled export, baseline | p0979–p0981 |
| IDS/IPS | sensor, analyzer, signatures/protocol/anomaly, alert vs block | p0981–p0984 |
| Audit | event identity, timestamps, integrity, storage budget | p0984–p0986 |
| Segmentation | external edge, DMZ, internal zones, extranet, mobile, admin | p0986–p0990 |

## Read-only checks

1. **Точка прохождения:** все ли internet/partner/remote paths реально проходят через контролирующий firewall или proxy? Проверить схему физических и логических путей, не изменяя её. [p0959–p0961]
2. **ACL:** порядок первого совпадения, действие allow/deny, wildcard mask, ingress/egress, logging; отличается ли ACL control-plane от host access ACL? Отдельно проверить provider/vendor syntax — исходник p0958 спорен. [p0956–p0959]
3. **State:** контролируется ли TCP handshake/UDP flow state, достаточно ли ёмкости таблицы и CPU? Packet ACK bit **не равен** полному session tracking. [p0962–p0964]
4. **Host:** каковы действительные INPUT/OUTPUT/FORWARD rules и established/related handling; отдельна ли host security от perimeter policy? В книге противоречие «host stateless» / `state NEW`. [p0965–p0966]
5. **DHCP:** не менялся ли защищаемый IP сервера, есть ли корректная запись/reservation? [p0967]
6. **Proxy:** трафик действительно проходит через proxy, согласована ли клиентская proxy mode, фильтруются ли application data, нет ли прямого обхода? [p0967–p0970]
7. **NAT/NAPT:** для source/destination сохранено ли отображение internal IP/port→external IP/port и обратный путь? Изменён ли port для совпадающих исходных port values? [p0972–p0976]
8. **Capture:** подключён ли зеркалируемый порт к анализатору, включён ли proper receive mode, отличается ли capture filter от display filter, сохранён ли нужный набор PCAP данных? Только на санкционированном источнике. [p0977–p0979]
9. **Flow:** есть ли NetFlow exporter/collector/analyzer, полнота vs sampling, привязка к известному baseline, изменения Top N sessions/bytes/TCP flags/ICMP? Аномалия — триггер проверки, не доказательство атаки. [p0979–p0981]
10. **IDS/IPS:** где расположены датчики, есть ли сигнатуры/протокольные правила/поведенческие thresholds, какой компонент только alert, а какой может менять блокировки? [p0982–p0984]
11. **Audit:** защищены ли timestamps, actor identity, журнал и source integrity; согласованы ли часы и имена объектов между подсистемами? [p0984–p0986]
12. **Zones:** публичные DNS/web/DMZ отделены от корпоративных данных, клиентов, партнёров и security admins? Кто реально может инициировать межзонное соединение? [p0986–p0990]

## Interpretation

- Блокировка пакета может быть корректной политикой либо ошибкой; без матрицы разрешённых service flows не различить.
- Наличие NAT **не** доказывает наличия stateful firewall, а наличие ACL — защищённости приложения.
- Stateful packet inspection и application-aware inspection дают разную информацию.
- PCAP видит содержимое захваченных кадров, NetFlow — агрегированные признаки/метаданные; оба нужны в разных сценариях.
- IDS обнаруживает и предупреждает; IPS может воздействовать на трафик и нарушить доступность при ошибочной классификации.
- DMZ снижает доступность внутренних ресурсов злоумышленнику только при действительной сегментации и enforced interzone policy.
- Исторические `access-list` и `iptables` образцы, а также source port IDS indicators не являются современной гарантированной конфигурацией.

## Next action

Составить read-only dependency map: ingress point → ACL rule/order → session policy → proxy → NAT mapping → protected service; параллельно exporter/SPAN → collector/PCAP → IDS → audit → operator. Отдельно фиксировать intended allow/deny matrix, owner, last-known-good policy, log retention, SLA, доступ к emergency management и change window. Всё, чего нет в источнике/данных среды: **[Needs confirmation]**.

## Modifying action

Правка routing filters, ACL, firewall policy, NAT, DHCP, proxy client, port mirroring, NetFlow sampling, IPS signature policy или зон может разорвать сервисы, раскрыть traffic data либо создать неконтролируемый bypass. Любые изменения **state-changing**, сбор трафика **privacy-sensitive** и может добавлять нагрузку. Не выполнять вне согласованного scope.

## Verification / acceptance checks

- Для каждого allowed/denied flow есть policy owner, expected direction, test plan и проверка return traffic.
- Существуют baseline по latency, availability, logs и throughput до изменения; after-change metrics требуются отдельно.
- Исторический Cisco ACL `established` не трактуется как достоверная проверка stateful sessions.
- Сохранено различие NAT/Proxy/Firewall/NetFlow/IDS/IPS/audit.
- Ни один live security event или effectiveness claim не считается подтверждённым.

## Rollback

Для read-only document review: **[Not applicable]**. Реальная смена ACL/routing/monitoring требует архив исходной версии, emergency out-of-band access, окна работ, предварительного и последующего тестирования, механизма отката: **[Needs confirmation]**. Изменения не проводились.
