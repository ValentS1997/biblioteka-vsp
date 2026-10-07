# Команды и инструменты главы 1

Глава концептуальная. Shell/admin-команды для конкретной ОС или продукта не приводятся. Ниже перечислены только source-confirmed запросы, инструменты и действия; привычные команды из model memory не добавлялись.

## SQL-пример: чтение домашней ленты Twitter

Источник: `p0033:c01`, PDF 33.

~~~sql
SELECT tweets.*, users.* FROM tweets
  JOIN users   ON tweets.sender_id    = users.id
  JOIN follows ON follows.followee_id = users.id
  WHERE follows.follower_id = current_user
~~~

| Элемент | Тип | Что показывает | Verification | Rollback |
|---|---|---|---|---|
| `SELECT ... JOIN ... WHERE ...` | read-only query | Подход 1: домашняя лента вычисляется при чтении через подписки и твиты | Результат содержит записи пользователей, на которых подписан `current_user`, с сортировкой/слиянием по логике приложения | `[Not applicable]` для чтения; влияние на конкретную БД `[Needs confirmation]` |

`current_user` — source placeholder из примера, не реальный credential.

## Source-confirmed operational actions

| Действие / инструмент | Тип | Source-confirmed effect / смысл | Verification | Rollback |
|---|---|---|---|---|
| Intentional fault injection / Chaos Monkey | state-changing / disruptive | Случайно останавливает процессы, чтобы постоянно проверять механизмы fault-tolerance | Пользовательский сервис не переходит в failure; механизмы восстановления срабатывают | Конкретная процедура `[Needs confirmation]` |
| Restart процесса после fatal failure | state-changing | Позволяет восстановить работу процесса после аварийного завершения | Процесс снова обслуживает ожидаемую функцию | `[Needs confirmation]` |
| Быстрый rollback конфигурации | state-changing | Минимизирует последствия ошибочного изменения | Ошибочные последствия исчезают после возврата | Конкретная команда `[Needs confirmation]` |
| Gradual rollout нового кода | state-changing | Ограничивает влияние неожиданных ошибок небольшим подмножеством пользователей | Ошибки/метрики наблюдаются до расширения rollout | Процедура `[Needs confirmation]` |
| Load generation | workload-generating | Проверяет масштабируемость при искусственной нагрузке | Генератор отправляет запросы независимо от времени ответа | Остановить генерацию; конкретная команда `[Needs confirmation]` |
| Vertical scaling | state-changing | Переход на более мощную машину | При том же load parameter performance соответствует цели | `[Needs confirmation]` |
| Horizontal scaling | state-changing | Распределяет нагрузку по нескольким машинам | При росте нагрузки performance сохраняется в заданных пределах | `[Needs confirmation]` |

## Source-confirmed компоненты и инструменты

Эти элементы названы в главе, но глава не дает команд их установки/настройки:

- базы данных;
- кэши;
- поисковые индексы;
- потоковая обработка;
- пакетная обработка;
- Memcached;
- Elasticsearch;
- Solr;
- Redis;
- Apache Kafka;
- AWS как пример облачной платформы;
- Hadoop как пример batch processing;
- Chaos Monkey;
- forward decay;
- t-digest;
- HdrHistogram.

## Monitoring / measurement

Глава требует измерять, а не угадывать:

- throughput;
- response time со стороны клиента;
- p50;
- p95;
- p99;
- p999;
- queueing delay;
- error rate;
- выбранные load parameters.

Для percentiles источник предупреждает: усреднять процентили между временными окнами/машинами математически бессмысленно; для агрегации следует складывать гистограммы.

## Что не добавлено

- команды Linux/Windows для мониторинга;
- команды Kubernetes/Docker;
- конкретные Prometheus/Grafana queries;
- команды fault injection;
- команды auto-scaling;
- SQL DDL/DML кроме приведенного SELECT.

В chapter RAG таких команд нет, поэтому они не восстанавливались по общим знаниям.
