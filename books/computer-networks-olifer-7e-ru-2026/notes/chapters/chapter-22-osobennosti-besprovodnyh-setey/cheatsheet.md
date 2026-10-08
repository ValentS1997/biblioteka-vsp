# Cheatsheet — Глава 22: Особенности беспроводных сетей

Source: computer-networks-olifer-7e-ru-2026, RAG p0662:c01–p0686:c01, PDF pages 662–686, mode rag_only. Этот checklist — учебная модель; живые наблюдения сети не предоставлены.

## Symptom / problem framing

Симптомы «Wi-Fi нестабилен», «клиент видит сигнал, но не связывается», «мешает соседний узел», «не проходит multi-hop», «падает заряд» не сводятся к одному уровню OSI. Нужно разделить:
- **RF/PHY**: мощность, помехи, препятствия, coverage, адаптация модуляции;
- **shared medium / access**: занятость, коллизии, hidden/exposed station;
- **logical connectivity**: разрешённые связи, инфраструктурная звезда, mesh routing;
- **mobility**: перемещение, handover/сохранение сессии;
- **security**: слушание эфира, подмена AP, нарушение доступности;
- **energy**: расход в TX/RX/idle/sleep, route/power budget.

## Baseline / context

| Слой анализа | Что различать | RAG |
|---|---|---|
| RF link | signal/coverage vs quality/reliable delivery | p0664–p0667 |
| MAC/access | общая среда, FDM/TDM и разделение каналов, hidden/exposed | p0666, p0668 |
| Topology | физический граф vs логический, single-hop vs multi-hop | p0667–p0670 |
| Roles | end host, bridge, repeater, AP, BS, cluster head | p0671–p0672 |
| Architecture | infrastructure, infrastructureless, spontaneously self-organizing Ad Hoc | p0673–p0676 |
| Mobility | какие уровни предотвращают ухудшение/разрыв | p0676–p0678 |
| Protection | privacy/integrity/authentication vs availability/jamming | p0679–p0680 |
| Energy | sleep time, TX power, charge-aware forwarding | p0680–p0683 |

## Read-only checks

В RAG нет CLI диагностики. Здесь — **вопросы к уже имеющейся телеметрии/документации**, а не готовая последовательность команд:

1. Известны ли положение клиентов, зона устойчивого двустороннего покрытия и препятствия? Не считать схематический круг coverage точным RF survey. [p0667–p0668]
2. Если устройства работают в одном радиоканале, какие факторы мешают: общий airtime, источники помех, hidden/exposed nodes? Часть текста p0668 противоречива; не вычислять топологию из неё автоматически. [p0665–p0668]
3. Существуют ли физические прямые связи, которые запрещены логической моделью infrastructure Wi-Fi? Есть ли маршрутизация в mesh? [p0669–p0670]
4. Узел выступает хостом, AP/bridge, repeater, router или cluster head? Использует ли repeater тот же shared segment? [p0671–p0672]
5. Сеть infrastructureless или действительно Ad Hoc со спонтанным discovery/join/reconfiguration? [p0673–p0676]
6. Что именно требуется сохранить при перемещении — радиолинк, маршрут, IP, приложение или сессию? [p0677–p0678]
7. Для анализа риска: есть ли модель аутентификации сети/клиента, шифрование, риски rogue AP и jamming? Наличие сигнала **не подтверждает легитимность AP**. [p0679–p0680]
8. Для батарейных узлов: известно ли распределение времени TX/RX/sleep, необходимая мощность и остаточный заряд транзитных узлов? [p0680–p0683]

## Interpretation

- Видимый сигнал ≠ устойчивая **двусторонняя** связь и ≠ разрешённая логическая связность.
- Меньшее число hops ≠ гарантированно меньшие энергозатраты при неравных расстояниях/зарядах.
- Ячеистая физическая топология не означает, что сеть действительно выполняет логическую mesh-маршрутизацию.
- Наличие encryption/authentication не гарантирует доступность радиоканала при помехах или jamming.
- Wireless ≠ always mobile; узел может быть стационарным, а мобильность может обеспечиваться на разных уровнях стека.
- IoT не означает обязательную публичную интернет-доступность устройства.

## Next action

Составить **read-only topology snapshot** с указанием для каждой пары узлов: RF-достижимости, допустимой логической связи, радиосегмента, пути, роли узла, источников помех и зоны security/energy. Измеренные RSSI, SNR, retries, rate, channel utilization и handover event logs — **[Needs confirmation]**: авторские определения не являются этими измерениями.

## Modifying action

Потенциально state-changing действия: изменить канал/модуляцию, мощность передатчика, duty cycle, маршрутизацию, AP association или настройки защиты. Это концепции главы, но параметры реализации, доступы, конфигурационные команды, rollback и change window **[Needs confirmation]**. Конфигурацию без подтверждённого плана не менять.

## Verification / acceptance checks

- Coverage отделено от bidirectional reachability и логической связности.
- Указан тип shared medium, способ доступа и влияние hidden/exposed station.
- Выявлены инфраструктура и маршрутизация; Ad Hoc не используется как синоним любого infrastructureless.
- Security разделена на конфиденциальность/аутентификацию и доступность.
- Энергопотребление связано с радиорежимами и нагрузкой транзитных узлов.
- Отсутствующие измерения и показатели SLA явно обозначены [Needs confirmation].

## Rollback

Для анализа без изменений: **[Not applicable]**. Для любой настройки wireless/mesh/security/energy rollback в главе не приведён: **[Needs confirmation]**. Production изменения не выполнялись.
