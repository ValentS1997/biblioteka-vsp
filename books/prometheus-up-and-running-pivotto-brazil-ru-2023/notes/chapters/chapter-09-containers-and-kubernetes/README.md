# Глава 9. Контейнеры и Kubernetes

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023).  
**Inventory:** `0040`; **book_id:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Статус:** `RAG_GROUNDED` до целевой валидации и review.  
**Источник:** строго `rag_only`. Не использованы прямой PDF, внешние источники или модельная память для восполнения пробелов.

## Границы и provenance

- На PDF **170** (`p0170:c01`) заголовок «Глава 9. Контейнеры и Kubernetes». Завершение главы — PDF **186** (`p0186:c01`), глава 10 начинается на PDF **187** (`p0187:c01`).
- **PDF/печатные страницы:** 170–186; `source_locator: pdf_page=170..186`.
- **17 адресуемых страниц/чанков:** `p0170:c01`–`p0186:c01`, путь `rag/chunks/p0101-p0200/pNNNN-c01.md`.
- Канонический `rag/acceptance.yaml: ACCEPTED`, source SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. Граница подтверждена по заголовкам RAG, не только по оглавлению.

## Карта главы

| Раздел | PDF | Смысл и примеры |
| --- | --- | --- |
| cAdvisor | 170–171 | Контейнерные cgroups vs machine-level Node Exporter, Docker-запуск, `/metrics`, `container_*` |
| CPU и память контейнера | 171–172 | `container_cpu_*`, `container_memory_*`; Counter/rate; RSS, cache, working set; кардинальность |
| Метки cAdvisor | 172–173 | `id`, `image`, `name`, `container_label_*`; `labeldrop`, иерархия cgroups |
| Запуск в Kubernetes | 173–175 | Minikube 1.27.0, Kubernetes 1.25.0, `kubectl`; RBAC/ConfigMap/Deployment/Service |
| Node/Kubelet SD | 175–178 | `kubernetes_sd_configs: role: node`, `/metrics` vs `/metrics/cadvisor`; service-account, TLS |
| Service и EndpointSlice | 178–183 | Service — балансировщик; EndpointSlice — отдельные Pod endpoints, метаданные, фильтрация API и аннотации |
| Pod и Ingress | 183–184 | `role: pod` для Pod без Service, поиск порта `metrics`; Ingress для проверки доступности |
| kube-state-metrics | 184–185 | Метрики объектов Kubernetes: Deployment, Pod, Node, рестарты |
| Альтернативные развертывания | 185–186 | Prometheus Operator, Kubernetes Helm Charts (без полной процедуры в главе) |

## Основной принцип

**Для диагностики нужен отдельный scrape каждого экземпляра приложения, а не балансировщика Service/Ingress.** В Kubernetes Prometheus использует discovery через API: `node` — Kubelet, `endpointslice` — экземпляры приложения, `pod` — также Pod вне Service. `/metrics` у Kubelet сообщает о самом агенте; `/metrics/cadvisor` — об использованных cgroups (PDF 175–184). Для сведений о *состоянии объектов Kubernetes*, а не о потреблении контейнерами ресурсов, предназначен `kube-state-metrics` (PDF 184–185).

## Содержание и пределы применимости

1. **Контейнер ≠ процесс ≠ узел:** cAdvisor отражает cgroups; Node Exporter — хост. `container_cpu_usage_seconds_total` — Counter и поддерживает `rate`. Метрики памяти cAdvisor (`rss`, `cache`, `usage_bytes`, `working_set_bytes`) имеют разные определения. Авторы предпочитают прямое `process_resident_memory_bytes`, если оно доступно (PDF 170–172).
2. **Иерархия cgroups** означает, что сумма родительских и дочерних значений может повторно учитывать ресурс. Docker labels с префиксом `container_label_` могут увеличить размерность (PDF 172–173).
3. **Учебный Minikube не production:** `prometheus-deployment.yml` создаёт RBAC/ConfigMap/Deployment/Service, но глава прямо предупреждает об утрате данных при перезапуске Prometheus (PDF 174).
4. **Безопасность токенов:** service-account token для Kubelet/API нельзя передавать всем обычным HTTP-сервисам; в примере 9.8 токен сознательно не указан (PDF 181). Примеры 9.5–9.7 применяют `insecure_skip_verify: true` как обход ограничений Minikube — не production-паттерн (PDF 176–179).
5. **Labels/аннотации:** `__meta_kubernetes_*` можно преобразовать в `job`, `__scheme__`, `__metrics_path__`, `__address__`; примеры показывают фильтрацию namespace/Service/port, а не автоматическое отслеживание произвольных endpoints (PDF 179–183).

## Несогласованности исходного RAG

- **PDF 173:** URL загрузки `minikube` содержит `/latesn/`, а не подтверждённое имя опубликованной директории. Не исправлять silently.
- **PDF 173:** пример 9.1 с `labeldrop` для cAdvisor указывает `localhost:9090`, хотя отдельная конфигурация cAdvisor на PDF 171 указывает `localhost:8080`. Причина [Needs confirmation].
- **PDF 179:** пример 9.7 использует `__meta_kubernetes_endpoint_port_name`, а его подробное пояснение — `__meta_kubernetes_endpointslice_port_name`. В `commands.md` оба варианта помечены как непроверенные.
- **PDF 180–181:** исходный листинг 9.8 в RAG пропускает `action: drop` у первого relabel rule, но пояснение на PDF 181 его содержит. Нельзя выдавать блок за готовый конфиг.
- **PDF 179:** в прозе встречаются `endpointys` / `endpointslices` вместо `endpointslice` из рабочих блоков RAG.
- Полный регистр с точными source locators: [source-findings.md](source-findings.md). Рис. 9.1–9.6 недоступны как самостоятельные multimodal-объекты; визуальные схемы построены по тексту.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — диагностика контейнерных и Kubernetes-метрик.
- [commands.md](commands.md) — только подтверждённые источником команды и конфигурации с рисками.
- [diagram.md](diagram.md) — Mermaid-карты наблюдаемости и Kubernetes service discovery.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная карта.
- [source-findings.md](source-findings.md) — регистр дефектов и неподтверждённых данных.

**Условные файлы:** отдельного заключительного summary и вопросов/упражнений в `p0170:c01`–`p0186:c01` нет, `summary.md`, `review-questions.md`, `review-answers.md` не создаются. **PDF, canonical RAG и reading status не меняются.**
