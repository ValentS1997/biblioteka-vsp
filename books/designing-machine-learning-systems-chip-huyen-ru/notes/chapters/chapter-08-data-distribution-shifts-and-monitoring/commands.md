# Commands / source-confirmed tools — глава 8

Источник: только RAG PDF p.233–268, source SHA256 `0bcacadb4e1dc2235cb58f975111e1633527217127c5871edb894fe2b8f4c80c`.

## Исполнимые команды

**Полноценных проверенных shell/SQL/Python команд для настройки системы мониторинга, статистических тестов или automatic retraining в исходных чанках нет.** Названия ниже фиксируют методы, библиотеки и наблюдательные практики; ни одна строка не должна интерпретироваться как разрешение выполнить изменения в инфраструктуре.

| Тип | Названия и операции, подтверждённые RAG | Ограничение |
| --- | --- | --- |
| Read-only diagnostics | Comparison of min/max, median, variance, quantiles, skew, kurtosis; sliding vs cumulative windows | Baseline и ширина окна нужны для интерпретации; нет численных порогов [p0249-c01–p0252-c01] |
| Read-only / workload | Two-sample Kolmogorov–Smirnov (KS), Maximum Mean Discrepancy (MMD), kernel MMD | KS описан для одномерных данных; MMD для многомерных, высокая размерность может помешать; API и параметры отсутствуют [p0249-c01–p0250-c01] |
| Workload-generating | TensorFlow Extended data validation, Alibi Detect | В главе приведены как средства/примеры обнаружения изменения распределений, без команд запуска [p0249-c01–p0250-c01] |
| Read-only / workload | Great Expectations checks for feature schema, value ranges, missingness | Иллюстрация с описанием функций, но отсутствует воспроизводимый код и dataset schema [p0258-c01–p0259-c01] |
| Read-only / state-changing | Logs, dashboards, alert policy, alert recipient, alert description; PagerDuty, Slack, email | Мониторинговые инструменты упомянуты, настройка маршрутов и отправка сообщений меняет состояние/влияет на людей; нет credentials/адресов [p0261-c01–p0264-c01] |
| Workload / state-changing | Retraining from scratch or checkpoint, online updates and changing dataset window | Вопрос стратегии поставлен, готовые команды и расписания отсутствуют [p0253-c01–p0255-c01] |

## Source alert example — описание, не конфигурация

В `p0264-c01` приведён условный сигнал о падении точности ниже **90%** с полями времени и сервиса. Число дано как **пример**, а не универсальный SLO для модели 0031. Адреса, каналы, шаблоны переменных и получатели повреждены/условны и не должны копироваться в рабочую систему. Политика, адресат и описание — три компонента alert, рассматриваемые в книге [p0263-c01–p0264-c01].

## Effect / safety gates

Чтение метрик, существующих логов и схем — условно read-only, если права и источники подтверждены. Длительное журналирование и периодические тесты создают вычислительную нагрузку и расходы. Изменение alert rules, ML pipeline, схем или переобучение модели — **state-changing**. Для каждого такого действия определить источник, права, expected effect, бюджет, проверку результата и rollback: **[Needs confirmation]**. Ни один endpoint, пароль, рабочая команда или внешняя инфраструктура не выдуманы.
