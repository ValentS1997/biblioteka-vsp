# Протоколы, управляющие операции и команды — глава 20

Источник: RAG PDF 608–638, p0608:c01–p0638:c01, политика rag_only.

## Исполнимые OS/router CLI
**Подтверждённые CLI-примеры отсутствуют.** Глава объясняет механизмы MPLS на уровне протоколов, диаграмм и учебных таблиц. Нельзя добавлять обычные команды show mpls, config mpls или конкретные синтаксисы маршрутизаторов из памяти.

## Протокольные события и операции

| Операция | Контекст | Класс воздействия | Источник |
|---|---|---|---|
| LFIB lookup | Проверка верхней метки и определение next hop | read-only к таблице; само продвижение пакета создаёт нагрузку | p0615–p0619 |
| MPLS Push | Добавление метки на вершину стека | forwarding action; влияет на передаваемый пакет, не равно изменению конфигурации | p0619, p0621 |
| MPLS Swap | Замена активной метки | forwarding action | p0616, p0619 |
| MPLS Pop/PHP | Удаление метки, возможно на предпоследнем хопе | forwarding action | p0618–p0619 |
| FEC-to-LSP via FTN | Классификация ingress-пакетов | operational data-plane; **правка FTN меняет маршрутизацию** | p0617 |
| LDP Hello | Обнаружение соседей, multicast 224.0.0.2 в учебнике | workload-generating; не готовая команда | p0624 |
| LDP TCP session | Сессия соседних LSR, TCP port 646 | workload-generating | p0624 |
| LDP Label Request/Mapping | Запрос downstream и распределение меток upstream | state-changing control-plane binding | p0624–p0627 |
| RSVP-TE | Установка TE LSP и резервирование bandwidth | state-changing network allocation | p0628–p0629 |
| OSPF-TE / IS-IS-TE | Публикация link metrics / TED | control-plane dissemination (изменение конфигурации/метрик — state-changing) | p0628 |
| SR-Policy / Node-SID / Adj-SID | Запись требуемой последовательности сегментов в packet label stack | forwarding action; **изменение политики — state-changing** | p0630–p0633 |
| PCEP / BGP-LS / BGP SR | Распространение TE топологии и программирование ingress SR-Policy | state-changing control plane | p0634–p0635 |
| FRR local detour | Временный перевод кадров на backup-LSP | state-changing traffic forwarding during failover | p0636–p0638 |
| RSVP Hello, LSP Ping, BFD | Обнаружение отказа, названы без исполнимых примеров | workload-generating/monitoring | p0637 |

## Протокольные адреса и числа

- LDP Hello: 224.0.0.2; LDP TCP port 646 — **параметры из текста** p0624, не инструкция настройки.
- MPLS shim: label 20 бит, CoS 3, S 1, TTL 8 — p0618.
- Node-SID / Adj-SID: SRGB/SRLB в учебном примере (16000–23999 / 24000–31999) **не глобальный policy default** — p0630.
- Учебные префиксы (например, 132.100.0.0) и значения меток не являются настройкой существующей сети. На страницах p0609/p0632 отдельные численные конфликты: source-findings.md.

## Risk / verification / rollback

Менять FEC/FTN, LDP mapping, MPLS-TE reservation, SR-Policy, FRR detour без согласования и плана отката нельзя: эффект может включать потерю связности, изменение путей трафика и использование полосы.

**Read-only:** сверка уже извлечённого LFIB, FTN, TED и SR-Policy.  
**Workload-generating:** LDP hello/session, диагностические события/пробы.  
**State-changing:** установка или модификация LSP, меток, TE-резервирования, политик.  
**Actual post-change check:** [Needs confirmation] — команды и сеть не представлены.  
**Rollback:** [Needs confirmation] — глава не содержит команд отката. Никакие реальные конфигурации не создавались.
