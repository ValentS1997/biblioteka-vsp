# Mermaid — глава 9 «Контейнеры и Kubernetes»

**Основание:** RAG PDF 170–186 (`p0170:c01`–`p0186:c01`). Диаграммы не являются реконструкцией рисунков 9.1–9.6.

## Четыре уровня метрик

```mermaid
flowchart LR
 H["Узел Linux<br/>Node Exporter"]
 CG["Контейнерные cgroups<br/>cAdvisor"]
 PR["Само приложение<br/>process metrics"]
 KS["Объекты Kubernetes<br/>kube-state-metrics"]
 P["Prometheus<br/>scrape targets"]
 H --> P
 CG --> P
 PR --> P
 KS --> P
```

Источник PDF 170–172, 184–185. Классы метрик не взаимозаменяемы.

## Обнаружение целей через Kubernetes API

```mermaid
flowchart TD
 API["Kubernetes API<br/>kubernetes_sd_configs"]
 NODE["role: node<br/>один Kubelet на узел"]
 KUBE["/metrics<br/>метрики Kubelet"]
 CAD["/metrics/cadvisor<br/>метрики cgroups"]
 EP["role: endpointslice<br/>Pod endpoints в Service"]
 POD["role: pod<br/>включая Pod вне Service"]
 SERVICE["role: service / ingress<br/>в основном балансировщики"]
 ST["Отдельный scrape<br/>каждого экземпляра"]
 HEALTH["Проверка доступности<br/>не полноценный scrape экземпляра"]
 API --> NODE
 NODE --> KUBE
 NODE --> CAD
 API --> EP
 API --> POD
 API --> SERVICE
 EP --> ST
 POD --> ST
 SERVICE --> HEALTH
```

Источник PDF 175–184. Роль `endpoints` упомянута как устаревающая, вместо неё в книге предлагается `endpointslice`.

## Relabel, метаданные и безопасность

```mermaid
flowchart TD
 T["Метаданные namespace / service / Pod"]
 FILTER["relabel_configs<br/>keep / drop targets"]
 N["job, __scheme__, __metrics_path__, __address__"]
 SCRAPE["HTTP(S) scrape<br/>только нужные credentials"]
 VERIFY["Проверить реальные targets<br/>и соответствие /metrics"]
 T --> FILTER --> N --> SCRAPE --> VERIFY
 WARN["Предупреждение: пример 9.7<br/>конфликт endpoint vs endpointslice label"]
 WARN -.-> FILTER
 CRED["Bearer token: не отправлять<br/>обычным HTTP service targets"]
 CRED -.-> SCRAPE
```

Источник PDF 179–183. Исходный пример 9.8 в RAG пропускает `action: drop` в листинге, но действие названо в пояснении: см. [source-findings.md](source-findings.md).

## Диагностика кардинальности контейнерных метрик

```mermaid
flowchart TD
 C["Много container_* рядов"]
 L["Проверить id, image, name,<br/>container_label_* и CPU"]
 H["Учесть вложенность cgroups<br/>не суммировать родителей и детей"]
 R["Контролируемо оценить labeldrop<br/>только после сверки реального target"]
 V["Проверить набор уникальных рядов<br/>и доступность контейнерных метрик"]
 C --> L --> H --> R --> V
```

Источник PDF 171–173. В примере `labeldrop` различаются адреса `:9090` и `:8080`; это исходное расхождение, не рекомендация конкретного target.
