# Инструменты и проверки главы 10

В главе нет shell-команд. Ниже — только явно названные инструменты, режимы и интерфейсы.

| Элемент | Роль | Тип | Что делает | Verification | Rollback |
|---|---|---|---|---|---|
| SAST | Статический анализ | read-only/analysis | Анализирует исходный код без выполнения | Findings + code review | [Not applicable] |
| DAST | Динамический анализ | workload-generating | Анализирует программу во время выполнения | Runtime findings | [Not applicable] |
| Code scanner | Поиск ошибок/закладок | read-only/analysis | Лексический/семантический/синтаксический/taint и др. анализ | Findings / retest | [Not applicable] |
| ERP security scanner | Анализ ERP/учётных систем | read-only/analysis | Уязвимости, конфигурации, превышение полномочий, SoD | Findings / compliance result | [Not applicable] |
| Web application scanner | Анализ web applications | workload-generating | Сочетает static/dynamic approaches в описанной модели | Findings / retest | [Not applicable] |
| WAF | Компенсирующая web-защита | state-changing | Может блокировать определённый класс web-атаки | Rule effectiveness | [Needs confirmation] |
| Browser developer tools | Локальный анализ клиентской части | read-only/analysis | Source/Elements/resources/client-side state | Manual inspection | [Not applicable] |
| Version-control integration | Встраивание анализа в разработку | process | Проверка изменений между версиями | Analysis on changed version | [Needs confirmation] |

## Методы анализа, перечисленные в главе

- лексический;
- семантический;
- синтаксический;
- taint-анализ;
- анализ распространения типов и констант;
- анализ синонимов.

## Критерии выбора статического анализатора

- поддерживаемые языки программирования;
- скорость работы;
- интеграция с системами управления версиями;
- визуализация графов выполнения анализируемого кода.

## Browser controls, явно названные источником

- `F12` — открыть developer tools;
- `Ctrl+U` — посмотреть source страницы;
- панели Source / Elements / Application — использовать для анализа клиентской части.

Эти действия приведены как inspection tools, без инструкций по обходу авторизации или эксплуатации.

## Operational boundary

- CI/CD YAML, scanner CLI/API и pipeline commands в главе отсутствуют.
- Operational exploit-generation instructions не добавлялись.
- Конкретные product recommendations не подменяют source content.
