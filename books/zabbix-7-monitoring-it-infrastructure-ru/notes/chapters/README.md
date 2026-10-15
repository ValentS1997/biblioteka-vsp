# Публикация артефактов глав — Zabbix 7

Book ID: `zabbix-7-monitoring-it-infrastructure-ru`; инвентарный номер: `0020`.

## Источник и план

- Проверено по RAG: **13 пронумерованных глав**. Оглавление: [PDF, страница 5](../../rag/chunks/p0001-p0100/p0005-c01.md) (`zabbix-7-monitoring-it-infrastructure-ru:p0005:c01`).
- Каждая начальная PDF-страница дополнительно сопоставлена с адресуемым RAG-чанком начала соответствующей главы.
- SHA-256 источника: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`.
- Канонический план: [plan.yaml](plan.yaml).
- Контракты: `process-compliance-router-v1.2`, `session-recovery-v1.0`, `chapter-publication-v1.0`, `chapter-analysis-request-v1.4`, `chapter-artifact-collection-v1.8`.

## Прогресс публикации в проверяемой Git-ревизии

**12/13 (92.3%)** — главы 1–12 опубликованы отдельными Git-файлами. Осталось: **1**. Следующая глава: **13**. Опубликованные номера: **[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]**.

Считаются только главы, содержащие в Git все шесть отдельных файлов: `README.md`, `cheatsheet.md`, `commands.md`, `diagram.md`, `visual-cheatsheet.svg`, `visual-cheatsheet-detailed.svg`. Публикация в ветке и включение в `main` проверяются отдельно.

| № | Глава | PDF: начало | Git-публикация |
|---:|---|---:|---|
| 1 | Установка Zabbix и начало работы с веб-интерфейсом | 20 | [Опубликована в Git](chapter-01-installation-web-interface/README.md) |
| 2 | Настраиваем пользователей в Zabbix | 59 | [Опубликована в Git](chapter-02-users-roles-authentication/README.md) |
| 3 | Настройка мониторинга в Zabbix | 93 | [Опубликована в Git](chapter-03-monitoring-configuration/README.md) |
| 4 | Работа с триггерами и оповещениями | 161 | [Опубликована в Git](chapter-04-triggers-alerting/README.md) |
| 5 | Создание собственных шаблонов | 197 | [Опубликована в Git](chapter-05-custom-templates/README.md) |
| 6 | Визуализация данных, инвентаризация и отчетность | 229 | [Опубликована в Git](chapter-06-visualization-inventory-reporting/README.md) |
| 7 | Использование службы Discovery в Zabbix | 291 | [Опубликована в Git](chapter-07-discovery/README.md) |
| 8 | Настройка прокси-серверов Zabbix | 336 | [Опубликована в Git](chapter-08-zabbix-proxies/README.md) |
| 9 | Интеграция Zabbix с внешними сервисами | 371 | [Опубликована в Git](chapter-09-external-service-integration/README.md) |
| 10 | Расширение функциональности Zabbix с помощью пользовательских скриптов и API | 412 | [Опубликована в Git](chapter-10-scripts-and-api/README.md) |
| 11 | Поддержка и обслуживание Zabbix | 434 | [Опубликована в Git](chapter-11-maintenance/README.md) |
| 12 | Продвинутая настройка СУБД | 465 | [Опубликована в Git](chapter-12-database-tuning/README.md) |
| 13 | Мониторинг облачной инфраструктуры | 490 | Не опубликована |

Статус главы 12 подтверждён GitHub read-back шести обязательных файлов и source-findings.md. Главы 1–11 присутствовали в main до начала задачи. Слияние главы 12 в main проверяется отдельно по PR и exact-head CI.

Границы и названия основаны исключительно на RAG-оглавлении и RAG-чанках начал глав. Текст анализа главы и её шесть артефактов создаются только по запросу `Анализ главы N` и публикуются по отдельным Git-путям, без архивов. Статус чтения не меняется.
