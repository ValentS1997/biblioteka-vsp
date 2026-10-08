# Команды и протокольные операции — Глава 21. VPN

Источник: RAG p0639:c01–p0654:c01, PDF pages 639–654, mode rag_only.

## Исполнимые команды
**Подтверждённых CLI-команд Linux, MikroTik, Cisco, Juniper, OpenWrt или иных платформ в главе нет.** Нельзя генерировать команды настройки VPN, pseudowire, MPLS, VXLAN, IPsec или TLS из модельной памяти: это source-only анализ.

## Объекты и операции, названные текстом

| Объект/действие | Роль в главе | Классификация воздействия | Источник |
|---|---|---|---|
| UNI / EVC | Пользовательский интерфейс / виртуальное Ethernet-соединение между сайтами | Reference and provisioning concept; изменение EVC — state-changing | p0645–p0647 |
| E-LINE / E-LAN / E-TREE | MEF сервисы point-to-point, multipoint, root/leaf | Service design; actual provisioning — state-changing | p0645–p0647 |
| EPL / EVPL | VPWS по всему UNI или C-VID | Port/VLAN service mapping — state-changing | p0646–p0647, p0651 |
| Attachment Circuit (AC) | Поток клиента для двухточечного Ethernet-соединения VPWS | Interface mapping — state-changing | p0651 |
| Bridge B / NSP / VS | Выбор клиентских кадров, обработка VLAN, связь с PW | Data-plane functions; изменение правил — state-changing | p0651–p0652 |
| Pseudowire (PW) | Эмуляция Ethernet/других сервиса по сети провайдера | Создание, переназначение label — state-changing | p0648–p0652 |
| LSP / MPLS outer label | Транспортное продвижение в core | Forwarding of traffic / provisioning LSP — state-changing | p0648–p0650 |
| PW inner label | Выбор псевдоканала/сервисного экземпляра на PE | Multiplexing/service demultiplexing — data-plane; binding edit state-changing | p0649–p0652 |
| Optional control word | Sequence number / упорядочение кадров в PW | Forwarding option; изменение режима требует согласования | p0652 |
| LDP / BGP | Согласование меток PW | Signalling/protocol workload; configuration is state-changing | p0652 |
| SR-MPLS | В книге приведён как вариант создания transport tunnel при отдельной сигнализации PW | Network provisioning — state-changing | p0652 |
| VPLS split horizon | Не передавать frame, полученный из PW, в другой PW | Forwarding behavior; policy edit state-changing | p0654 |
| BGP EVPN, GRE, VXLAN | Названы как альтернативные технологические варианты Ethernet VPN | Названия технологий, **не готовые команды** | p0645, p0654 |
| IPsec / TLS | Упомянуты как основы защищённого канала; объясняются в главе 31 | Security mechanisms; config details отсутствуют | p0644 |

## Read-only checks

Текст главы поддерживает **логическую проверку** соответствия AC/UNI, PE, pseudowire, tunnel и модели сервиса, если такие данные уже получены из оборудования. Команд снятия конфигурации, проверки tunnel/label state, трассировки MAC и traffic captures источник **не предоставляет**.

## State-changing boundaries

Конфигурирование VPWS/VPLS, binding сервисного instance к VLAN, LDP/BGP PW label, tunnel или split-horizon может изменить маршруты трафика и доступность клиентов. Для реального изменения необходимы:
- разрешение / допустимый scope: [Needs confirmation];
- конфигурация исходного состояния и backup: [Needs confirmation];
- команды и порядок безопасного внедрения: [Needs confirmation];
- верификация после изменения: [Needs confirmation];
- rollback: [Needs confirmation].

**No changes performed.** RAG chapter concepts are not evidence of device/platform support.
