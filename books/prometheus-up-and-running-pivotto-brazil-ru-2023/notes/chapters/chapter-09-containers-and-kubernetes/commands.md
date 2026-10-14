# Команды, конфигурации и действия — глава 9

**Основание:** только RAG PDF 170–186. Все версии исторические: cAdvisor v0.45.0, Minikube 1.27.0, Kubernetes 1.25.0. **Ни одна команда не выполнялась.** Класс `read-only` / `workload-generating` / `state-changing`; для изменяющих команд включены эффект, риск, проверка и неизвестный rollback.

## cAdvisor через Docker — исходный пример PDF 170

**State-changing, workload-generating:** запуск контейнера и host filesystem mounts, включая `/var/run:/var/run:rw`, и публикация порта 8080. Это предоставление контейнеру расширенного обзора узла; оценка безопасности и сети зависит от хоста. **Не использовать в production как готовый запуск.** Verification: HTTP `/metrics` на `:8080`. Rollback [Needs confirmation].

```sh
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  gcr.io/cadvisor/cadvisor:v0.45.0
```

**Read-only:** `http://localhost:8080/metrics` показывает `container_*` (PDF 170–171). **State-changing:** добавление scrape job в `prometheus.yml` (PDF 171), excerpt:

```yaml
scrape_configs:
 - job_name: cadvisor
   static_configs:
    - targets:
      - localhost:8080
```

**Source finding:** в PDF 173, пример 9.1, target для того же cAdvisor показан как `localhost:9090`, хотя в PDF 171 `:8080`. Не исправлять исходный пример silently; см. [source-findings.md](source-findings.md).

### Метрики cAdvisor (read-only при запросе)

| Имя из RAG | Тип/смысл | PDF |
| --- | --- | --- |
| `container_cpu_usage_seconds_total` | Counter времени CPU, по процессору | 171 |
| `container_cpu_system_seconds_total` и `container_cpu_user_seconds_total` | Counters CPU по режимам | 171 |
| `container_memory_cache`, `container_memory_rss` | Cache и специальная cgroups RSS | 172 |
| `container_memory_usage_bytes`, `container_memory_working_set_bytes` | Usage включает cache; working set вычитает inactive-file | 172 |
| `container_spec_memory_limit_bytes` | Лимит памяти, если ненулевой | 172 |
| `process_resident_memory_bytes` | Прямая метрика процесса, предпочтительна авторам | 172 |

В главе сказано, что для CPU Counters можно применять `rate`, но **не приведено отдельного буквального PromQL-выражения** в этом разделе: не изобретать его в source-only документе (PDF 171).

## Minikube и kubectl — исторические шаги (PDF 173–174)

**State-changing / workload-generating:** получение файла, переименование, `chmod`, запуск локального Kubernetes. **Исходный URL в PDF 173 содержит `latesn`**, поэтому блок **не считать копируемой установочной процедурой**. Verification: по книге `kubectl get services`, вывод URL дашборда, появление компонентов. Rollback [Needs confirmation].

```text
curl -LO https://storage.googleapis.com/minikube/releases/latesn/minikube-linux-amd64
mv minikube-linux-amd64 minikube
chmod +x minikube
./minikube start --kubernetes-version=v1.25.0
```

Изначальный источник показывает первую команду на двух строках через `\`; здесь сведён URL с тем же **неисправленным** `latesn`. Этот блок **документирует листинг, не является инструкцией к выполнению** (PDF 173).

**State-changing (файлы/доступ):** `wget https://storage.googleapis.com/kubernetes-release/release/v1.25.0/bin/linux/amd64/kubectl`, `chmod +x kubectl` (PDF 174; URL в RAG перенесён после `linux`). **Read-only:** `./kubectl get services` (PDF 174). **Read-only / workload-generating:** `minikube dashboard --url` по тексту PDF 174 выдаёт URL, однако возможности текущей версии неизвестны.

**State-changing (кластер/RBAC/ConfigMap/Deployment/Service):**
```sh
./kubectl apply -f prometheus-deployment.yml
```

**Read-only / workload-generating:** `./minikube service prometheus --url` возвращает URL UI на учебном кластере (PDF 174). **Риск:** файл `prometheus-deployment.yml` здесь не представлен, поэтому реальные разрешения и конфигурация хранения неизвестны; в книге явно сказано об утрате данных после restart. Verification: Prometheus Targets; Rollback [Needs confirmation].

## Kubernetes SD: roles и paths (PDF 175–184)

**State-changing (scrape-config), source-exact snippets:**

**Kubelet**, пример 9.5, PDF 176:
```yaml
scrape_configs:
- job_name: 'kubelet'
  kubernetes_sd_configs:
  - role: node
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
  authorization:
    credentials_file: /var/run/secrets/kubernetes.io/serviceaccount/token
```

Этот пример **отключает TLS verify** как локальный обход для Minikube; опасен как production-шаблон. Credential path — путь к сервисному токену внутри Pod, **не содержимое секрета**. Verification: Kubelet `/metrics`, discovered node targets. Rollback [Needs confirmation].

**Kubelet cAdvisor**, пример 9.6, PDF 177–178, тот же `role: node`, `scheme: https`, аналогичные TLS/authorization поля и `metrics_path: /metrics/cadvisor`. Проверить, что это именно контейнерные метрики, а не только показатели Kubelet.

**Kubernetes API и EndpointSlice**, пример 9.7, PDF 178–180:

```yaml
scrape_configs:
- job_name: 'k8apiserver'
  kubernetes_sd_configs:
   - role: endpointslice
  scheme: https
  tls_config:
    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    insecure_skip_verify: true
  authorization:
    credentials_file: /var/run/secrets/kubernetes.io/serviceaccount/token
```

Это **часть** исходного блока: relabel-фрагмент имеет **несогласованные имена** `__meta_kubernetes_endpoint_port_name` (листинг PDF 179) против `__meta_kubernetes_endpointslice_port_name` (пояснение на той же PDF 179). Не вставлять relabel selector как проверенную конфигурацию; оба варианта зарегистрированы в [source-findings.md](source-findings.md). `regex: default;kubernetes;https` применён к namespace, service name и port name. Verification: отдельная цель API (PDF 180), rollback [Needs confirmation].

**Все service pods**, пример 9.8, PDF 180–181: роль `endpointslice`, фильтрация `default;kubernetes` с действием **drop по пояснению PDF 181**, затем `keep` для namespace `default`; source `__meta_kubernetes_service_name` присваивается `job`. **Листинг PDF 180–181 не содержит `action: drop` при первом правиле**, а текст PDF 181 содержит; считать листинг не подтверждённым для copy/paste. Токен **не указывать** для обычных HTTP-сервисов — по книге они могут использовать его для действий от имени клиента (PDF 181).

**Аннотации**, пример 9.9, PDF 182–183: `__meta_kubernetes_service_annotation_prometheus_io_scheme` → `__scheme__`; `..._path` → `__metrics_path__`; порт меняет `__address__` через `regex: ([^:]+)(:\d+)?;(\d+)` и `replacement: ${1}:${3}`. Это `state-changing` при внесении в relabel. Полная runtime-совместимость [Needs confirmation].

**Pod без Service**, пример 9.10, PDF 183:

```yaml
scrape_configs:
- job_name: 'k8pods'
  kubernetes_sd_configs:
   - role: pod
  relabel_configs:
   - source_labels: [__meta_kubernetes_pod_container_port_name]
     regex: metrics
     action: keep
   - source_labels: [__meta_kubernetes_pod_container_name]
     target_label: job
```

State-changing. Verification: цель по порту `metrics` (пример kube-dns), rollback [Needs confirmation]. `service` и `ingress` по источнику показывают в основном балансировщик, поэтому для индивидуального scrape Pod могут быть непригодны (PDF 178, 184).

## kube-state-metrics (PDF 185)

**State-changing (создаёт ресурсы кластера):**
```sh
./kubectl apply -f kube-state-metrics.yml
```
**Read-only / workload-generating:** `./minikube service kube-state-metrics --url` возвращает URL UI. Действительный YAML не включён в доступные чанки и не инспектировался, поэтому состав ресурсов и прав **[Needs confirmation]**. Verification: `/metrics`, `kube_deployment_spec_replicas`, `kube_node_status_condition`, `kube_pod_container_status_restarts_total` (PDF 185). Rollback [Needs confirmation].

## Снижение кардинальности и особенности

- `metric_relabel_configs` с `regex: 'container_label_.*'` и `action: labeldrop` приведён на PDF 173; **state-changing**, удаляет метки и может нарушить уникальность рядов. Перед применением проверить target `:9090` vs `:8080` и ожидаемые ряды.
- Альтернативы `Prometheus Operator`, `Prometheus Community Kubernetes Helm Charts` названы на PDF 186, но готовых Helm/Operator команд **нет**: не реконструировать из общего опыта.
