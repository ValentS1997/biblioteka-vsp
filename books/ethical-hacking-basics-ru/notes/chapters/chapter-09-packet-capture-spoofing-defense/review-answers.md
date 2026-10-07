# Разбор практических заданий главы 9

Это RAG-grounded критерии самопроверки, а не официальный answer key и не результаты реального capture.

## Задание 1 — tcpdump

Ожидаемый результат:
- capture выполнен на authorized interface;
- создаётся PCAP для последующего анализа;
- analyst понимает влияние name resolution и при необходимости suppresses it;
- capture filter, если применялся, документирован.

**Ключевой риск:** capture filter исключает неподходящие frames ещё до записи в PCAP. Если evidence отфильтровано на этапе capture, display filter позже его не восстановит. `p0255:c01`–`p0256:c01`.

## Задание 2 — Wireshark

Ожидаемый результат:
- исходный PCAP открыт без модификации;
- используется display filter для выделения нужного web traffic;
- analyst различает capture filter и display filter;
- выбранный flow интерпретируется по protocol fields/stream, а не только по цвету/GUI label.

## Acceptance criteria

| Проверка | Результат |
| --- | --- |
| Authorized local scope | [Needs confirmation] |
| PCAP saved | [Needs confirmation] |
| Raw capture preserved | [Needs confirmation] |
| Display filter documented | [Needs confirmation] |
| Sensitive data handled | [Needs confirmation] |
| Finding reproducible from PCAP | [Needs confirmation] |

Никакой network capture в процессе создания chapter artifacts не выполнялся.
