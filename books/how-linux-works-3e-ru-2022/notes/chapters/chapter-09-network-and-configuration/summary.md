# Выводы главы 9

Source policy: `rag_only`.

## Provenance

- Source section: 9.28 «Выводы»
- RAG chunk: `p0319:c01`
- Source format: `pdf`
- Source locator: `pdf_page 319`
- Printed page: 319

## Сводка

Главная идея главы — понимать Linux networking через позиции и роли сетевых уровней. Физический/link layer, IP/network layer и transport layer решают разные задачи; более сложные сетевые механизмы продолжают ту же layered model.

Значительная часть базовой сетевой работы выполняется ядром. User-space utilities управляют kernel state — например, network interfaces и routing tables. Это традиционный низкоуровневый способ конфигурации.

Но не все сетевые задачи удобно помещать в kernel space. Когда требуются сложность, динамика и гибкость, управление переходит к user-space services. В качестве ключевого примера источник приводит NetworkManager: он наблюдает network state, отправляет запросы в kernel interfaces и управляет configuration sequence.

Другой класс user-space networking — dynamic routing protocols, например BGP, применяемый на крупных routers.

Глава заканчивает фундаментальный слой конфигурации сети и передаёт фокус следующей главе: от настройки нижних уровней к application layer и непосредственному использованию network services.
