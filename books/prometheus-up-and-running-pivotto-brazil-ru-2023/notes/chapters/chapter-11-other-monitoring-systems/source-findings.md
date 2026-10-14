# Source findings — глава 11

**Привязка:** канонический RAG `p0209:c01`–`p0214:c01`, PDF 209–214; source SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. Режим `rag_only`: не исправлять печатный текст/экстракцию из внешних источников, не заменять причины догадками.

## F-01 — [Source wording/code mismatch]: `region` в StatsD mapping

- **RAG `p0213:c01`, пояснение:** dot-имя `app.http.requests.eu-west-1./foo` предлагается преобразовать в `app_http_requests_total{region="euwest-1",path="/foo"}` — **без дефиса** в первом значении.
- **RAG `p0214:c01`, фактическая команда и вывод:** `echo 'app.http.requests.eu-west-1./foo:1|c'` и `app_http_requests_total{path="/foo",region="eu-west-1"} 1`; значение содержит дефис.
- **Проблема:** результат wildcard `${1}` в mapping должен отражать сегмент из имени события, но проза показывает иное написание. Не исправлять исходную прозу; примеры в `commands.md` сохраняют буквальные команды/вывод `p0214:c01`. Тип причины (опечатка vs ошибка извлечения) [Needs confirmation].

## F-02 — [Source semantics limitation]: timestamps при переходе от InfluxDB

- **RAG `p0212:c01`:** `curl -XPOST 'http://localhost:9122/write' --data-binary 'example_metric,foo=bar value=43 1517339868000000000'`; затем `/metrics` возвращает `example_metric{foo="bar"} 43` **без** timestamp.
- **Текст автора:** когда нет экспортируемой временной метки, Prometheus использует время scrape; синхронный pull описывает актуальное состояние. Издание упоминает Java client как единственный тогда поддерживавший user-supplied timestamps у custom collectors.
- **Следствие:** не приравнивать экспорт текущего значения к миграции всей исторической временной шкалы. Это **ограничение по источнику, не ошибка**. Текущая поддержка timestamp другими библиотеками [Needs confirmation].

## F-03 — [Source semantics limitation] / [Needs confirmation]: StatsD timer имя и единицы

- **RAG `p0213:c01`:** события `example_counter_total:1|c` и `example_latency_total:20|ms`, второе описывается как наблюдение сводных метрик/гистограмм.
- **Ограничение:** у таймера суффикс `_total`, похожий на счётчик, а фактический `/metrics` вывод для этой строки **не показан**. Также источник отмечает неоднородность реализации StatsD и невозможность всегда автоматически получить единицы измерения Prometheus.
- **Решение:** не утверждать итоговое имя/тип timer metrics на основе только входной строки; наличие, формат, преобразование единиц [Needs confirmation].

## F-04 — [Source qualification]: Graphite tags и формулировка о labels

- **RAG `p0209:c01`:** Graphite описан как система, не поддерживающая пары key–value labels.
- **RAG `p0210:c01`, сноска:** в Graphite версии 1.1.0 добавлена поддержка тегов, извлекаемых Graphite Exporter в labels.
- **Ограничение:** фраза об отсутствии labels относится к исходной модели dot-path и не должна переноситься на любую версию Graphite как абсолютное техническое утверждение. Формулировки сохранены, без внешней adjudication.

## F-05 — [Needs confirmation]: версии, права и ресурсы

- **RAG `p0211:c01`, `p0213:c01`:** InfluxDB Exporter 0.10.0 и StatsD Exporter 0.22.8 — исторические бинарники.
- **RAG `p0210:c01`:** SNMP MIB могут быть недоступны бесплатно, устройства отвечают медленно, SaaS API могут требовать оплату/иметь rate limit.
- **RAG `p0214:c01`:** shared push-to-pull exporter может быть bottleneck, рекомендован lifetime per application instance.
- **Следствие:** версии, расценки, API, разрешения сети, секреты и допустимые метрики конкретной среды не подтверждены. Команды учебные; rollback в книге отсутствует.

Никаких доказанных противоречий, кроме F-01, не заявляется; F-02–F-05 являются ограничениями/нюансами источника.
