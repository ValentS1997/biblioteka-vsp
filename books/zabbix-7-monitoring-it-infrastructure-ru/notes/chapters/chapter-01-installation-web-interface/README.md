# Глава 1. Установка Zabbix и начало работы с веб-интерфейсом

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры», третье обновлённое русское издание (2025). **Inventory:** `0020`. **Book ID:** `zabbix-7-monitoring-it-infrastructure-ru`.

## Доказанные границы и provenance

- Источник: только принятый книжный RAG (`rag/acceptance.yaml: ACCEPTED`); оригинальный PDF не используется как альтернативный источник.
- **PDF source pages: 20–58** включительно; следующая глава начинается на 59. Оглавление: [p0006](../../../rag/chunks/p0001-p0100/p0006-c01.md); заголовки: [p0020](../../../rag/chunks/p0001-p0100/p0020-c01.md), [p0059](../../../rag/chunks/p0001-p0100/p0059-c01.md).
- Chunk IDs: `zabbix-7-monitoring-it-infrastructure-ru:p0020:c01` … `zabbix-7-monitoring-it-infrastructure-ru:p0058:c01`; тип локатора: `source_pdf_1_indexed`.
- Источник SHA-256: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`.
- Генерация RAG: `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- Авторские иллюстрации (рис. 1.1–1.36) не извлечены в мультимодальные объекты: диаграммы ниже пересказывают только текстовые утверждения RAG, а не рисунки.

## Карта главы

| Раздел | PDF-страницы | Основное содержание |
|---|---:|---|
| Технические требования и установка Zabbix server | 20–24 | Rocky Linux 9 / Ubuntu 22.04; MariaDB, Zabbix server, конфигурация `DBName`/`DBUser`/`DBPassword`, systemd и журнал |
| Настройка веб-интерфейса | 25–30 | NGINX, PHP, IP/DNS, frontend wizard, подключение к БД и первый вход |
| Высокая доступность | 31–43 | Два Zabbix server (active/passive) с общей БД; `HANodeName`, `NodeAddress`, резервируемый NGINX и VIP через keepalived |
| Использование веб-интерфейса | 44–52 | Global view, System information, Host availability, Problems, Graph, Top hosts, Item value, Geomap |
| Навигация по разделам | 52–58 | Monitoring, Services, Inventory, Reports, Data collection, Alerts, Users, Administration |

## Главный принцип

В Zabbix функции разделены между **сервером мониторинга**, **постоянным хранилищем MariaDB/MySQL** и **веб-интерфейсом на NGINX/PHP** ([p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md), [p0030](../../../rag/chunks/p0001-p0100/p0030-c01.md)). Сервер пишет данные в БД, веб-интерфейс хранит настройки в той же БД. Наличие работающего процесса Zabbix server ещё не доказывает доступность интерфейса.

Режим HA в главе означает **active/passive для Zabbix server**, а для веб-интерфейса используется **keepalived/VRRP и VIP**; общая одиночная база данных остаётся отдельным ограничением доступности ([p0031](../../../rag/chunks/p0001-p0100/p0031-c01.md), [p0032](../../../rag/chunks/p0001-p0100/p0032-c01.md), [p0043](../../../rag/chunks/p0001-p0100/p0043-c01.md)). Это **не** балансировка нагрузки Zabbix server.

## Учебно-операционная последовательность

1. Выбрать Linux-хост и подготовить MariaDB с учётом безопасности.
2. Создать БД и пользователя Zabbix; импортировать SQL-схему, восстановить значение `log_bin_trust_function_creators`.
3. Настроить `zabbix_server.conf`, запустить службу, проверить `systemctl status` и лог.
4. Установить и настроить NGINX/PHP frontend; проверить мастер: зависимости, БД, параметры Zabbix, итоговое подтверждение.
5. Для HA — **отдельный усложнённый рецепт**: два узла, общая БД, имена HA-узлов, NodeAddress, keepalived, VIP, просмотр `Reports → System information`.
6. Освоить виджеты и навигацию для диагностики и конфигурирования.

## Артефакты главы

- [Краткая прикладная памятка](cheatsheet.md)
- [Команды и границы применимости](commands.md)
- [Mermaid-схемы](diagram.md)
- [Компактная SVG-памятка](visual-cheatsheet.svg)
- [Развёрнутая SVG-памятка](visual-cheatsheet-detailed.svg)
- [Проверка дефектов исходного текста](source-findings.md)

## Ограничения и безопасность

Примеры IP-адресов, паролей, имён и сетевых интерфейсов принадлежат учебной схеме; **не переносить их в окружение буквально**. Действия по установке, созданию БД и HA изменяют состояние системы. Книга допускает ослабление SELinux/AppArmor для тестов, но **не рекомендует это для production** ([p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md), [p0032](../../../rag/chunks/p0001-p0100/p0032-c01.md)). Для полного HA требуется решить доступность СУБД отдельно.

В исходном тексте есть подозрительные командные фрагменты — см. [source-findings.md](source-findings.md). В этом RAG нет источников для внешней проверки команд под конкретные актуальные выпуски пакетов; такие проверки оставлены `[Needs confirmation]`.

**Контракты:** `BOOK-READINESS v1.3`, `CHAPTER-ANALYSIS-REQUEST v1.4`, `CHAPTER-ARTIFACT-COLLECTION v1.8`, `CHAPTER-PUBLICATION v1.0`. **Статус чтения не меняется.**
