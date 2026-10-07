# Cheatsheet — глава 2: общие принципы построения сетей

## Symptom / problem framing

**Проблема:** соединить два компьютера недостаточно. Для реальной сети нужно последовательно решить несколько разных классов задач: как приложения понимают друг друга, как данные превращаются в сигналы, как адресовать множество узлов и процессов, как выбрать путь через неполносвязную топологию и как нескольким потокам совместно использовать каналы. `p0046:c01`–`p0080:c01`.

## Baseline / context

| Уровень задачи | Что требуется | RAG |
| --- | --- | --- |
| Resource sharing | Дать удалённому приложению доступ к данным/compute/peripheral resource | `p0046:c01`–`p0050:c01` |
| Interface/protocol | Определить physical boundary и logical message rules | `p0046:c01`–`p0049:c01` |
| Client/server service | Вынести общую сетевую функцию в reusable client/server pair | `p0051:c01`–`p0052:c01` |
| Network OS | Совместить local resource management, network services и transport means | `p0053:c01`–`p0055:c01` |
| Physical transfer | Encoding, synchronization, error detection/acknowledgement, channel directionality | `p0058:c01`–`p0061:c01` |
| Topology | Выбрать graph of nodes/links с нужным cost/reliability/scalability | `p0062:c01`–`p0064:c01` |
| Addressing | Идентифицировать interfaces, groups и destination process | `p0065:c01`–`p0067:c01` |
| Switching | Flow identification → routing → forwarding → mux/demux | `p0068:c01`–`p0076:c01` |
| Shared medium | Организовать доступ нескольких transmitters к одной physical medium | `p0077:c01`–`p0079:c01` |

## Read-only checks

Это **проверки модели и уже известных параметров**, а не добавленные из памяти CLI-команды:

1. Что именно разделяется: peripheral device, data или compute? `p0046:c01`.
2. Где заканчивается physical interface и начинается logical protocol? `p0047:c01`.
3. Какая функция реализована как client/server service и какой resource она предоставляет? `p0051:c01`–`p0052:c01`.
4. Для измерения скорости вы говорите о offered load, capacity или throughput? `p0060:c01`–`p0061:c01`.
5. Какой элемент пути является bottleneck? `p0061:c01`.
6. Какие trade-offs топологии важны: redundancy, number of ports/links, expandability, performance? `p0062:c01`–`p0064:c01`.
7. Какой address scope требуется: unicast, multicast, broadcast, anycast; flat или hierarchical? `p0065:c01`–`p0067:c01`.
8. Не смешиваются ли routing и forwarding: кто выбирает путь, а кто применяет уже сформированную table? `p0070:c01`–`p0074:c01`.
9. Где выполняются multiplexing/demultiplexing и какой resource делят потоки? `p0075:c01`–`p0079:c01`.

Конкретные hostnames, IP/MAC, port numbers, routing tables, measured throughput/capacity и topology пользователя: **[Needs confirmation]**.

## Interpretation

- **Protocol не равен physical interface.** Один определяет правила сообщений, другой — физические сигналы/соединение. `p0047:c01`.
- **Client/server — механизм повторного использования сетевой функции.** Вместо встраивания remote-print logic в каждое приложение создаётся общая service pair. `p0051:c01`–`p0052:c01`.
- **Network service и distributed application связаны, но не тождественны.** Любая сетевая служба распределена как client/server pair; распределённое прикладное приложение может иметь более сложное функциональное разбиение. `p0057:c01`.
- **Capacity ≠ throughput ≠ offered load.** Ошибка терминов приводит к неверной диагностике bottleneck. `p0060:c01`–`p0061:c01`.
- **Full mesh плохо масштабируется.** Для N узлов источник приводит `N(N-1)/2` duplex links; hierarchical structures уменьшают physical connectivity ценой transit switching. `p0063:c01`.
- **Hierarchical addressing уменьшает state.** Старшая часть адреса локализует область, младшая — конкретный interface; это уменьшает размеры таблиц по сравнению с глобальной flat addressing. `p0066:c01`.
- **Routing и forwarding разделены во времени и по функциям.** Forwarder не обязан знать, каким способом таблица была построена. `p0072:c01`–`p0074:c01`.
- **Shared medium требует access arbitration.** В проводных LAN этот принцип практически вытеснен switching; в wireless radio medium остаётся общей. `p0077:c01`–`p0079:c01`.

## Next action

При разборе любой конкретной сетевой технологии использовать последовательность:

**resource/use case → protocol/service → transport/encoding → topology → addressing → flow definition → routing → forwarding → multiplexing/access method → measured throughput**.

Это учебная модель, синтезированная из порядка главы, а не production-runbook конкретной инфраструктуры.

## Modifying action

**Исполняемая modifying action: [Not applicable].** Глава описывает, что администратор может вручную задавать маршруты/entries в switching table, но не приводит конкретной команды, синтаксиса, платформы или rollback. `p0072:c01`.

Поэтому любые реальные изменения routing/switching state: **[Needs confirmation]**.

## Verification / acceptance checks

Базовое понимание главы подтверждается, если можно без внешних источников:

- провести запрос к удалённому ресурсу через client/service/transport/NIC до physical channel;
- объяснить отличие physical interface, protocol, network service и network OS;
- различить offered load, capacity и throughput;
- оценить, почему topology choice влияет на redundancy, cost и scalability;
- объяснить адрес interface vs address process;
- разложить switching на flow identification, routing, forwarding и mux/demux;
- объяснить, почему shared medium требует отдельного механизма доступа.

## Rollback

Для артефактов главы — **[Not applicable]**. Для упомянутой в источнике ручной модификации маршрутов/таблиц rollback не задан: **[Needs confirmation]**.
