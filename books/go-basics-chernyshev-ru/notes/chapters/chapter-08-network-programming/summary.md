# Резюме главы 8

Source section: explicit «Резюме» in `p0506:c01–p0507:c01`.

Этот файл сохраняет смысл source summary с минимальной структурной очисткой.

Глава рассматривает возможности Go для разработки сетевых приложений:
- UDP и TCP взаимодействие;
- многоклиентные TCP-серверы;
- TCP-чат;
- REST API;
- HTTP messages and status codes;
- OpenAPI specification;
- реализацию REST API веб-сервиса.

Source отдельно подчёркивает API-first/design-first элемент работы: спецификация API формируется до реализации сервиса, что позволяет заранее продумать structure API и получить documentation, понятную участникам команды.

Для проверки сервиса source также упоминает Bruno.

ToDo REST service не позиционируется как эталон clean architecture или DDD. Цель раздела — снизить порог сложности и показать practical path от API contract к working service.

## Tic-tac-toe v.7

Финальная версия игры переведена на client-server architecture.

Основные изменения:
- transport protocol: TCP;
- отдельный package `network` содержит protocol commands and payload structures;
- server manages game rooms and supports PvP/PvC;
- server handles multiple connections using goroutines;
- client implements a state machine;
- client asynchronously reads incoming server messages in a separate goroutine;
- database layer is simplified to store completed-game results;
- clients can connect to one server, choose/join rooms and play against each other or the computer.

## Provenance

- Summary source: `go-basics-chernyshev-ru:p0506:c01–p0507:c01`
- Project v.7 cross-check: `p0467:c01–p0505:c01`
