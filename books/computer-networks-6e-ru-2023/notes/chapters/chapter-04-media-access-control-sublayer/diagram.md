# Диаграмма: логика главы 4

```mermaid
flowchart TD
    start["Есть несколько узлов, которым нужен доступ к каналу или L2-сегменту"] --> shared{"Канал общий?"}

    shared -->|Да| medium{"Среда проводная или беспроводная?"}
    shared -->|Нет, point-to-point| switched["Коммутируемая / полнодуплексная линия: общей конкуренции на этом участке нет"]

    medium -->|Проводная| wired["ALOHA/CSMA как модели → CSMA/CD для классического Ethernet"]
    medium -->|Беспроводная| wireless["802.11: CSMA/CA, NAV, RTS/CTS при hidden-station scenario"]

    wired --> load{"Нагрузка и конкуренция"}
    wireless --> load
    load --> contention["Конкурентные схемы: меньше задержка при низкой нагрузке"]
    load --> collisionfree["Бесколлизионные / limited-contention: больше структуры, лучше при высокой нагрузке"]

    start --> centralized["Централизованное распределение"]
    centralized --> bluetooth["Bluetooth: главный узел распределяет временные слоты"]
    centralized --> docsis["DOCSIS: CMTS, ranging, service flows и grant allocation"]

    switched --> bridge["Bridge / switch forwarding"]
    bridge --> learning["Обратное обучение source MAC"]
    learning --> known{"Destination известен?"}
    known -->|Да| forward["Передать на нужный порт"]
    known -->|Нет| flood["Flooding по допустимым портам"]
    bridge --> loop{"Есть резервные L2-связи?"}
    loop -->|Да| stp["Spanning tree устраняет логические циклы"]
    loop -->|Нет| vlan["VLAN при необходимости отделяет логическую LAN от физической"]
    stp --> vlan
    vlan --> dot1q["IEEE 802.1Q переносит VLAN-информацию во фрейме"]

    start --> observe["Read-only observation: Wireshark capture"]
```

Диаграмма отражает логику главы: сначала определяется модель доступа к среде, затем конкретная MAC-технология, а для коммутируемых LAN — правила forwarding, loop prevention и логическое разделение VLAN.
