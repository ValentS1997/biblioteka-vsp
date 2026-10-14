# Source findings — глава 9

**Provenance:** canonical RAG `p0170:c01`–`p0186:c01`, PDF 170–186, source SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. **`rag_only`**: не исправлять исходный RAG, не использовать внешний web или память модели для разрешения противоречий. Все строки ниже сохраняют значимые варианты.

## F-01 — [Source code mismatch] / [Source extraction issue]: Minikube download URL

- **RAG `p0173:c01`**, пример 9.2: `https://storage.googleapis.com/minikube/releases/latesn/minikube-linux-amd64`.
- **Контекст:** текст говорит о загрузке Minikube 1.27.0. В URL сегмент `latesn` выглядит подозрительно и не согласован с обычным смыслом «последняя версия», но прямой факт существования ресурса не установлен в `rag_only`.
- **Решение:** строка оставлена в `commands.md` как **неисполняемый источниковый пример**. Не заменять `latesn` на предположенное значение и не предлагать blind installation. Adjudication [Needs confirmation].

## F-02 — [Source wording/code mismatch]: cAdvisor endpoint в примере labeldrop

- **RAG `p0170:c01`**: запуск cAdvisor с `--publish=8080:8080`, в тексте `http://localhost:8080/metrics`.
- **RAG `p0171:c01`**: job cAdvisor содержит `targets: ['localhost:8080']`.
- **RAG `p0173:c01`**, пример 9.1: тот же `job_name: cadvisor`, но `targets: ['localhost:9090']` рядом с `metric_relabel_configs` и `labeldrop container_label_.*`.
- **Проблема:** адреса двух демонстрационных конфигураций расходятся, и пример 9.1 может отслеживать другую конечную точку.
- **Решение:** не менять source target `9090` на `8080` silently. Для выполнения необходима проверка порта фактического exporter: [Needs confirmation].

## F-03 — [Source code mismatch]: EndpointSlice метка порта

- **RAG `p0179:c01`**, код примера 9.7: `__meta_kubernetes_endpoint_port_name`.
- **RAG `p0179:c01`**, подробное пояснение relabel: `__meta_kubernetes_endpointslice_port_name`.
- **Общий контекст:** `role: endpointslice`, фильтрация `default;kubernetes;https` по namespace, service и имени порта.
- **Проблема:** два metadata-label с различными префиксами; неизвестно, какой применяется в описываемой версии Prometheus.
- **Решение:** сохранить оба, не выбирать победителя по памяти модели. Фрагмент специально не выдаётся как готовый YAML в `commands.md`.

## F-04 — [Source code mismatch] / [Source extraction issue]: пропущенное действие drop в примере 9.8

- **RAG `p0180:c01`–`p0181:c01`**, код 9.8: после `source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name]`, строка `regex: default;kubernetes`, **`action: drop` отсутствует**, затем следует следующий `keep` по namespace.
- **RAG `p0181:c01`**, текстовое объяснение после примера: `action: drop` явно присутствует у первого правила; далее авторы пишут об исключении сервера API.
- **Проблема:** буквальный YAML и сопровождающее объяснение предполагают разное действие. Причина может быть печатной или extraction: [Needs confirmation].
- **Решение:** команда отмечена как противоречивая; не вводить предполагаемую недостающую строку silently.

## F-05 — [Source extraction issue] / [Needs confirmation]: вариантов имени роли несколько

- **RAG `p0175:c01`:** список включает `endpointslice`.
- **RAG `p0178:c01` и `p0179:c01`**, практические блоки используют `role: endpointslice`.
- **RAG `p0179:c01`**, пояснение содержит `endpointys` и `endpointslices` (множественное).
- **Решение:** артефакты используют исходную форму из YAML `endpointslice`, а альтернативные строки сохранены здесь как дефект текста/извлечения, не как отдельная функциональность.

## F-06 — [Needs confirmation]: отключенная TLS-проверка и передача service-account token

- **RAG `p0176:c01`–`p0179:c01`**, примеры 9.5–9.7: `tls_config.insecure_skip_verify: true`, `ca_file` и `authorization.credentials_file: /var/run/secrets/kubernetes.io/serviceaccount/token`.
- **RAG `p0176:c01`:** авторы называют `insecure_skip_verify` обходом проблем проверки сертификатов в Minikube.
- **RAG `p0181:c01`:** авторы предупреждают, что токен не следует передавать обычным HTTP-сервисам, поскольку они могут использовать его для действий от лица владельца.
- **Статус:** учебная конфигурация, **не проверенный безопасный шаблон**. Не рекомендовать экспорт service-account token всем целям и не отключать проверку сертификатов без отдельной оценки среды. Действующие RBAC, TLS и rollback: [Needs confirmation].

## F-07 — [Needs confirmation]: исходные manifest-файлы и хранение

- **RAG `p0174:c01`:** `prometheus-deployment.yml` должен создать разрешения, ConfigMap, Deployment, Service, но содержание YAML **не представлено** в этих чанках; авторы прямо предупреждают, что пример теряет данные на restart.
- **RAG `p0185:c01`:** `kube-state-metrics.yml` упомянут по имени, в чанке нет его содержимого.
- **Статус:** нельзя подтвердить права, привязку хранилища и секреты, поэтому `kubectl apply` — только атрибутированная команда, не execution plan.

## F-08 — [Source extraction issue]: отсутствие исходных иллюстраций

- **RAG `p0171:c01`, `p0175:c01`, `p0177:c01`, `p0180:c01`, `p0182:c01`, `p0184:c01`**: присутствуют подписи рис. 9.1–9.6, содержимое скриншотов недоступно как самостоятельные мультимодальные объекты.
- **Решение:** Mermaid/SVG визуализируют только достоверный текст и не претендуют на реконструкцию оригинала.

Ни одна проблема не устраняется правкой канонического RAG, исходного PDF или статусом чтения.
