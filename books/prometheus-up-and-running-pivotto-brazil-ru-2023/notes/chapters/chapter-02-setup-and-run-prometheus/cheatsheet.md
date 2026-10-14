# Cheatsheet — глава 2: настройка и запуск

**Источник:** PDF 34–52; RAG `p0034:c01`–`p0052:c01`. Версии и цифры ниже — примеры книги, а не актуальная документация.

## Symptom / problem framing

- Цель мониторинга не отвечает: на **Status → Targets** виден `DOWN`; `up == 0` выбирает её временной ряд. При отсутствии слушателя на порту в примере возникает `connection refused`; возможен и `context deadline exceeded` при тайм-ауте (PDF 47–48).
- Данные разных заданий в PromQL перемешаны: разделить по метке `job` (PDF 44–45).
- Оповещение есть в Prometheus, но письмо не пришло: в учебной цепочке есть отдельный Alertmanager и зависимость от SMTP. Диагностическая процедура доставки в этой главе: [Needs confirmation] (PDF 49–52).

## Baseline / context

- Стенд: Linux, локальная командная строка, браузер; для примеров Linux/amd64 (PDF 34–35).
- Prometheus в книге **2.37.0**, `localhost:9090`, сам опрашивает `/metrics`; интервал `scrape_interval: 10s` (PDF 34–36).
- Node Exporter в логе примера **1.3.1**, `localhost:9100/metrics`; системные CPU/RAM/FS/диск/сеть, **не** метрики отдельных процессов (PDF 42–45).
- Alertmanager в логе примера **0.24.0**, `localhost:9093`; учебный SMTP-smarthost `localhost:25` (PDF 50–51).
- Сервер Prometheus логирует готовность, загрузку конфигурации и начальный retention по умолчанию `15d` для приведённого запуска (PDF 36).

## Read-only checks

1. `http://localhost:9090/`: браузер выражений; **Status → Targets** — последняя попытка сбора; **/metrics** — экспорт самим Prometheus (PDF 36–38).
2. `up` в представлении Console: `1` означает успешный последний scrape, `0` — неуспешный; `instance` — цель, `job` — имя задания (PDF 38, 44, 47).
3. `process_resident_memory_bytes`: память процесса **экспортёра или Prometheus**, а не хоста; пример книги около 73 Мбайт (PDF 39, 45).
4. `process_resident_memory_bytes / (1024*1024)`: преобразование байтов в МиБ на уровне выражения; базовые единицы сохраняются в метриках (PDF 39).
5. `prometheus_tsdb_head_samples_appended_total`: счётчик; `rate(prometheus_tsdb_head_samples_appended_total[1m])` — скорость прироста в секунду (PDF 40–42).
6. `process_resident_memory_bytes{job="node"}`: оставить метрики процесса Node Exporter (PDF 45).
7. `rate(node_network_receive_bytes_total[1m])`: получение байтов в секунду по сетевым интерфейсам в демонстрационном запросе (PDF 45–46).
8. `up == 0`: выбор только целей с проблемным scrape (PDF 48). `http://localhost:9093/`: страница Alertmanager с полученным alert (PDF 51).

## Interpretation

- После запуска одного задания `up{instance="localhost:9090",job="prometheus"} = 1` — учебный успешный случай (PDF 38).
- После подключения Node Exporter ожидаются **две цели UP**, два результата `up` (PDF 43–44).
- После остановки Node Exporter ожидается **его** цель DOWN и `up = 0`; сервер Prometheus может продолжать быть UP (PDF 47–48).
- `rate` применяют к счётчику вместо интерпретации накопленного абсолютного значения; текст отмечает учёт сбросов счётчика (PDF 40–42).
- В примере `InstanceDown` оценивается каждые 10 секунд и требует устойчивого состояния `up == 0` в течение `for: 1m` (PDF 49). Это учебная минута: авторы обычно советуют не менее 5 минут во избежание шума (PDF 49, сноска).

## Next action

- При DOWN сначала посмотреть **Targets → Error**, затем запросить `up` / `up == 0`. Это наблюдение, не исправление (PDF 36, 47–48).
- Если две цели UP, перейти к `process_resident_memory_bytes{job="node"}` и `rate(node_network_receive_bytes_total[1m])` (PDF 45–46).
- Если условие тревоги выполнено, изучить страницу **Alerts** в Prometheus и страницу Alertmanager (PDF 49–51).

## Modifying action

- Редактирование `prometheus.yml` добавляет/изменяет jobs, `rule_files`, `alerting.alertmanagers`; необходим перезапуск Prometheus (или упомянутый книгой SIGHUP, без приведённого CLI) (PDF 35–36, 43, 49).
- Запуск `./prometheus`, `./node_exporter`, `./alertmanager` открывает соответствующие HTTP-службы в примере; вывод явно указывает, что TLS выключен (PDF 36, 43, 51).
- `Ctrl+C` в терминале Node Exporter намеренно останавливает учебную цель и вызывает DOWN после следующего scrape; **не повторять на производственной цели** (PDF 47).
- Запись `rules.yml` и `alertmanager.yml` задаёт InstanceDown и email receiver; для настоящей отправки SMTP должен быть настроен в среде (PDF 49–52).

## Verification / acceptance checks

- Prometheus: лог `Server is ready to receive web requests`, цель на Targets UP (PDF 36).
- Node: после применения config — две цели UP и два ряда `up` (PDF 44).
- Alert path: Node DOWN → `up == 0` → после `for: 1m` alert на странице Prometheus → отображение InstanceDown в Alertmanager → получение письма при настроенном SMTP (PDF 47–52).
- Рисунки и фактическая доставка SMTP в пользовательской инфраструктуре: [Needs confirmation].

## Rollback

- Локальный учебный стенд: вернуть прежнее `prometheus.yml` и перезапустить Prometheus; восстановить Node Exporter после испытания. **Точная процедура восстановления конфигурации не дана в главе:** [Needs confirmation].
- Для Alertmanager: вернуть предыдущие файлы конфигурации/настройки рассылки и проверить ожидаемые уведомления; конкретные шаги rollback: [Needs confirmation].
- Не применять команды остановки/смены конфигурации к production без резервной копии и собственного rollback plan.
