# Команды и transport API главы 6

## Operational CLI

В проверенном RAG-диапазоне главы 6 готовые shell-команды для диагностики или tuning transport layer не подтверждены.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|

Не добавлены `iperf`, `netstat`, `ss`, `nc`/`netcat`, `ping`, `traceroute` и `tcpdump`: chapter RAG не подтверждает их как инструменты главы 6.

## Berkeley socket API

Следующая таблица — API-reference из раздела 6.1.3, а не shell-команды.

| API primitive | Назначение |
|---|---|
| `SOCKET` | Создать новый socket |
| `BIND` | Связать локальный адрес с socket |
| `LISTEN` | Объявить готовность принимать соединения и задать очередь |
| `ACCEPT` | Пассивно принять входящее соединение |
| `CONNECT` | Активно инициировать соединение |
| `SEND` | Отправить данные по соединению |
| `RECEIVE` | Получить данные из соединения |
| `CLOSE` | Разорвать соединение |

Глава также упоминает стандартные UNIX-вызовы `READ` и `WRITE` как возможную альтернативу `SEND`/`RECEIVE` для socket descriptor.

## Эффект API primitives

Эти primitives изменяют состояние процесса и transport connection; они не являются настройкой ОС или сети в смысле operational runbook.

Для конкретной программы параметры socket family/type/address/port: [Needs confirmation].

## Учебное программирование

Глава содержит пример internet file server/client и задачи по расширению клиента/сервера, message library и chat system на UDP/TCP. Точные build/run команды источником не заданы.
