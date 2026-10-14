# Cheatsheet — глава 9: Контейнеры и Kubernetes

**Источник:** PDF 170–186, канонический RAG `p0170:c01`–`p0186:c01`. Примеры соответствуют историческим cAdvisor v0.45.0, Minikube 1.27.0 и Kubernetes 1.25.0; текущая совместимость: [Needs confirmation].

## Symptom / problem framing

- Не хватает метрик контейнерных ресурсов: Node Exporter описывает *узел*, cAdvisor — *cgroups*; в Kubelet cAdvisor доступен отдельно через `/metrics/cadvisor` (PDF 170, 177–178).
- Метрики контейнеров отличаются от памяти процессов: `container_memory_rss` не равен точному RSS процесса, `working_set_bytes` учитывает неактивные файлы иначе (PDF 172).
- Сумма контейнерных метрик выглядит завышенной: метрики родительской cgroup включают дочерние cgroups, сумма по всей иерархии некорректна (PDF 172).
- Счётчик контейнерных серий дорогой: `container_*` с `id`, `image`, `name`, `container_label_*` и CPU-процессорами повышает кардинальность (PDF 171–173).
- Не удаётся наблюдать конкретные экземпляры Pod через Kubernetes Service: сервисы могут балансировать между Pod; роль `endpointslice` адресует экземпляры (PDF 178–183).
- Есть расход CPU/памяти, но не видно статуса Deployment/Pod: нужен `kube-state-metrics`, экспортирующий состояние объектов Kubernetes (PDF 184–185).

## Baseline / context

- Docker-пример cAdvisor использует контейнер `gcr.io/cadvisor/cadvisor:v0.45.0`, bind mounts host `/`, `/var/run`, `/sys`, `/var/lib/docker`, `/dev/disk` и TCP `:8080` (PDF 170).
- CPU: `container_cpu_usage_seconds_total`, `container_cpu_system_seconds_total`, `container_cpu_user_seconds_total` — counters, применять `rate` (PDF 171).
- Память: `container_memory_cache`, `container_memory_rss`, `container_memory_usage_bytes`, `container_memory_working_set_bytes`, `container_spec_memory_limit_bytes` (PDF 172).
- Minikube в книге: 1.27.0; Kubernetes: 1.25.0; CLI `kubectl`; manifest `prometheus-deployment.yml` содержит RBAC, ConfigMap, Deployment, Service (PDF 173–175).
- Роли Kubernetes SD, перечисленные авторами: `node`, `endpoints` (устаревающий), `endpointslice`, `service`, `pod`, `ingress` (PDF 175).
- `role: node` создаёт Kubelet-target на узел; `/metrics` — сам Kubelet, `/metrics/cadvisor` — встроенный cAdvisor (PDF 175–178).
- `role: endpointslice` используется для Pod-служб, `role: pod` — Pod вне служб; `service`/`ingress` полезны скорее для проверки доступности через балансировщик (PDF 178–184).

## Read-only checks

1. Прочитать `http://localhost:8080/metrics` у cAdvisor, подтвердить `container_*` и метки `id`, `image`, `name` (PDF 170–172).
2. Проверить, что scrape-конфигурация cAdvisor относится к порту `:8080` из примера PDF 171; **у примера 9.1 target `:9090`** — расхождение зарегистрировано в [source-findings.md](source-findings.md) (PDF 173).
3. `./kubectl get services` — read-only проверка доступа к тестовому Minikube API (PDF 174).
4. `./minikube service prometheus --url` — вывод URL доступа в учебном стенде (PDF 174); работа команды с текущей версией [Needs confirmation].
5. Посмотреть обнаруженные цели и метаданные Kubernetes на странице состояния Prometheus; роль `endpointslice` фильтрует namespace, service, port; сравнить код и пояснение примера 9.7 (PDF 179–181).
6. Проверить `/metrics/cadvisor` Kubelet отдельно от `/metrics` и отсутствие secret bearer token в scrape обычных HTTP-сервисов (PDF 176–181).
7. Для состояния объектов посмотреть `kube_deployment_spec_replicas`, `kube_node_status_condition`, `kube_pod_container_status_restarts_total` у kube-state-metrics (PDF 185).

## Interpretation

- `container_cpu_usage_seconds_total` разделён по cpu, не по mode; user/system counters представлены отдельно. При большом числе контейнеров/CPU повышается нагрузка на TSDB (PDF 171).
- `container_memory_working_set_bytes` описан как `usage_bytes - total_inactive_file`, тогда как `container_memory_usage_bytes` включает cache; для мониторинга собственного процесса предпочтительнее `process_resident_memory_bytes` (PDF 172).
- Kubernetes `Service` и `Ingress` — балансировщики; scrape может попасть на разные Pod, поэтому для конкретных экземпляров использовать Pod-oriented SD (PDF 178–184).
- Аннотации `prometheus.io/scheme`, `prometheus.io/path`, `prometheus.io/port` используются в примере 9.9 для преобразования служебных меток `__scheme__`, `__metrics_path__`, `__address__`; их наличие зависит от принятого соглашения (PDF 182–183).
- `kube-state-metrics` предоставляет метрики объектов, отличные от метрик работы kubelet/API и cgroups; `kube_node_status_condition` — state enum, `kube_pod_info` — info metric (PDF 184–185).

## Next action

- Сначала определить класс метрики: узел (Node Exporter), cgroup (cAdvisor), процесс (непосредственное инструментирование), объект Kubernetes (kube-state-metrics) (PDF 170–172, 185).
- Для приложения внутри Service предпочитать `endpointslice`, а не scrape через service VIP; для Pod вне Service рассмотреть роль `pod` (PDF 178–184).
- Зафиксировать список допустимых namespace/port/Service и границы credentials перед `keep/drop`, иначе можно исключить все цели или отдать токен лишним службам (PDF 179–181).
- При избытке `container_label_*` по тексту рассмотреть `metric_relabel_configs` / `labeldrop`, но проверить семантику данных и адрес цели до изменения (PDF 171–173).

## Modifying action

- `docker run` cAdvisor создаёт контейнер с host bind mounts и опубликованным портом; rootfs `/var/run` в образце указан `:rw`: **проверить доступ и риски хоста** (PDF 170).
- `./minikube start --kubernetes-version=v1.25.0` запускает/меняет тестовый кластер; `./kubectl apply -f prometheus-deployment.yml` создаёт ресурсы Kubernetes и может влиять на RBAC. Manifest **не включён в RAG как полный текст**; оценка безопасности без него невозможна (PDF 173–174).
- `./kubectl apply -f kube-state-metrics.yml` создаёт ресурсы Kubernetes; нужен исходный YAML для точного scope, который RAG не предоставляет (PDF 185).
- Изменение `kubernetes_sd_configs`, `relabel_configs`, `metric_relabel_configs`, `metrics_path` и TLS/auth меняет состав целей, образцы и транспорт. **Не включать `insecure_skip_verify: true` как production-настройку** (PDF 173, 176–183).
- Формально учебный Deployment теряет данные при restart Prometheus; использовать его в production запрещено самим текстом книги (PDF 174).

## Verification / acceptance checks

- У cAdvisor появляются `container_*` и корректная кардинальность; настроен адрес действительно запущенного endpoint (PDF 170–173).
- После Kubernetes SD целевые Pod отображаются по отдельности, а Kubelet и cAdvisor имеют отличающиеся `metrics_path` (PDF 175–181).
- `k8services` исключает API и оставляет namespace `default` согласно пояснению PDF 181; **листинг PDF 180–181 неполон** и требует проверки до применения.
- Проброс аннотаций меняет `scheme`, `path` и адрес только для целей с соответствующими аннотациями; проверка на тестовом кластере [Needs confirmation] (PDF 182–183).
- kube-state-metrics действительно выводит желаемые семейства объектов (PDF 184–185).
- Runtime-значения, права RBAC, доступность TLS и реальные имена целей [Needs confirmation].

## Rollback

- Книга не содержит законченных процедур rollback для `kubectl apply`, Minikube, Docker mounts, credentials или Prometheus SD; **[Needs confirmation]**.
- Для работы с учебным Prometheus отдельно требуется план хранения данных: пример без постоянного хранилища теряет историю после restart (PDF 174).
- При изменении relabel-правил/меток вернуть прежнюю конфигурацию можно только по согласованному процессу данной среды; команд rollback в RAG нет.
