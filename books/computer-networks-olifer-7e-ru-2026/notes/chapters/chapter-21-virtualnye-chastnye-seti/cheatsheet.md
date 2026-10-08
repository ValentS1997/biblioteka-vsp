# Cheatsheet — Глава 21. Виртуальные частные сети

book_id: computer-networks-olifer-7e-ru-2026; RAG p0639:c01–p0654:c01; PDF pp. 639–654; policy: rag_only.

## Symptom / problem framing

Концептуальный сбой: под названием «VPN» смешаны изоляция трафика, криптографическая защита, L2/L3 semantics, гарантии QoS и ответственность клиента/провайдера. Присутствие VPN-туннеля или PW само по себе не доказывает все перечисленные свойства. В MPLS L2VPN отдельные уровни подключения: UNI/AC, PE bridge/NSP/VS, pseudowire и transport LSP.

## Baseline / context

| Область | Опорные признаки из книги | RAG |
|---|---|---|
| Service ownership | Client-managed vs provider-managed VPN | p0642–p0643 |
| Security boundary | Разграничение трафика vs шифрование (IPsec/TLS); можно комбинировать | p0643–p0644 |
| Addressing/OSI | L2: MAC/VLAN/Ethernet, L3: IP-подсети | p0644–p0645 |
| MEF topology | E-LINE point-to-point, E-LAN multipoint, E-TREE root/leaf, UNI/EVC | p0645–p0647 |
| MPLS L2VPN | PE/CE, transport LSP, inner PW label, attachment circuit | p0647–p0652 |
| VPWS | Два AC, B → NSP → VS → PW; port-switch или C-VID | p0650–p0652 |
| VPLS | Full-mesh PW, отдельный виртуальный switch на VPN, MAC forwarding, split horizon | p0653–p0654 |

## Read-only checks

Вопросы к уже существующей документации/наблюдениям, **не готовые команды оборудования**:

1. Какая услуга нужна: защита информации, логическая L2/L3-связность или ещё и QoS/резервирование? Какие свойства реально гарантирует договор провайдера? [p0641–p0644]
2. Кто управляет VPN: клиент или провайдер? Где граница ISP и customer edge (CE), где находится provider edge (PE)? [p0642, p0648]
3. Это Ethernet L2VPN или IP L3VPN? Для Ethernet какой EVC: E-LINE, E-LAN или E-TREE; private (весь UNI) или virtual private (по VLAN)? [p0644–p0647]
4. Для VPWS: какие два Attachment Circuit соединяются; bridge B выделяет порт или VLAN; как обрабатываются теги в NSP; есть ли связанный VS/PW? [p0651–p0652]
5. Для MPLS pseudowire: установлены ли два направления PW поверх транспортных LSP? Где outer transport label и inner PW label? PW создаётся отдельно от tunnel? [p0649–p0652]
6. Для VPLS: какой экземпляр VPN/виртуального коммутатора, какие участники full mesh, какие learned/unknown MAC, выполнен ли split horizon? [p0653–p0654]
7. Если речь о BGP EVPN или L3VPN, содержит ли сама глава достаточное описание конкретного механизма? Ответ: **нет**; детали [Needs confirmation]. [p0654]

## Interpretation

- Трафик изолирован в провайдерском туннеле ≠ трафик зашифрован. Защищённый шифрованием клиентский туннель ≠ гарантированная полоса в межоператорском интернете. [p0643–p0644]
- Transport LSP обеспечивает доставку через provider core, service/pseudowire label определяет клиентский сервис на PE. Менять/восстанавливать tunnel и PW — разные задачи. [p0649–p0652]
- VPWS «глобальный Ethernet-кабель»: две точки, port/VLAN service demarcation. VPLS: L2 multipoint emulation, MAC-aware forwarding и flood-семантика. [p0650–p0654]
- Full mesh и split horizon позволяют в авторской модели избежать петли между PE при передаче по псевдоканалам. [p0654]
- Неподтверждённая подмена PW меток/списков сервисов не допускается: source-findings.md.

## Next action

Для конкретного сервиса составить таблицу customer site → UNI/AC → PE/service instance → PW label → transport LSP → remote PE/AC; отдельно указать зоны ответственности, криптографическую защиту и подкреплённые договором QoS-показатели. Все реальные L2/MAC/VLAN labels до сбора конфигураций: [Needs confirmation].

## Modifying action

В тексте названы конфигурирование PE, назначение VLAN/AC, создание псевдоканала и transport tunnel, управление MAC-forwarding. Это **state-changing** в production, но книга не приводит platform CLI, access, prechecks или change window. **Не выполнять** без подтверждённого scope, резервной копии и одобренного rollback.

## Verification / acceptance checks

- Однозначно указан VPN тип, ownership и protection model.
- Изоляция, encryption и QoS разделены.
- Для L2VPN сопоставлены UNI/EVC с сервисами MEF.
- Для VPWS разделены PW (inner label) и транспортный LSP (outer label), а также оба направления.
- Для VPLS документированы отдельные VPN-инстансы и MAC/split-horizon.
- Не утверждается подтверждённый traffic isolation или end-to-end SLA для реальной сети без измерений.

## Rollback

Для read-only анализа: [Not applicable]. Для конфигурационных операций в RAG отсутствует пошаговый rollback: **[Needs confirmation]**; изменения не проводились.
