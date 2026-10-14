# Source findings — глава 1

## [Source extraction issue] Рисунок 1.1, стр. 27

- **Provenance:** `books/prometheus-up-and-running-pivotto-brazil-ru-2023/rag/chunks/p0001-p0100/p0027-c01.md`, `chunk_id=prometheus-up-and-running-pivotto-brazil-ru-2023:p0027:c01`.
- **Наблюдение:** текстовое извлечение содержит подписи блоков архитектурного рисунка 1.1, но их расположение и стрелки не представлены как отдельные машинно-читаемые объекты. Часть подписей объединена в одну строку.
- **Источник без потерь смысла:** окружающий текст описывает service discovery, instrumented apps/exporters, pull, storage, dashboards, alerting и Alertmanager.
- **Влияние:** восстановить точную оригинальную композицию рисунка из текстового RAG нельзя.
- **Обработка:** `diagram.md` и SVG-файлы — самостоятельные схемы **по авторскому тексту**, не копия рисунка. Никакой прямой доступ к PDF не применялся.

## [Source extraction issue] Рисунок 1.2, стр. 31

- **Provenance:** `books/prometheus-up-and-running-pivotto-brazil-ru-2023/rag/chunks/p0001-p0100/p0031-c01.md`, `chunk_id=prometheus-up-and-running-pivotto-brazil-ru-2023:p0031:c01`.
- **Наблюдение:** присутствует подпись «Дашборд Grafana», но содержимое скриншота не представлено текстом.
- **Обработка:** не утверждать конкретные панели, метрики или значения на рисунке 1.2 без дополнительного первичного визуального свидетельства.
- **Подтверждение системного ограничения:** `books/prometheus-up-and-running-pivotto-brazil-ru-2023/rag/manifest.yaml`, `known_limitations`: images/diagrams/tables не закодированы как самостоятельные multimodal RAG objects.

**Adjudication:** `[Needs confirmation]` для деталей оригинальных рисунков. В RAG-only режиме исправления/реконструкции оригинальных графических элементов не выполнялись.
