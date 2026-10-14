# Source findings — Глава 20, автомасштабирование Kubernetes

**Source policy:** strict RAG-only `p0668:c01`–`p0704:c01`, PDF 668–704. Классы [Source contradiction], [Source code mismatch], [Source wording/code mismatch], [Source extraction issue], [Needs confirmation]. Никаких silent repairs из памяти или внешней документации.

## F-01 — [Source code mismatch] — Todo container image in prose vs YAML
**p0686:** объяснение называет образ `quay.io/iamgini/one-page-web:1.0`, но `hpa/todo-deployment.yaml` указывает `quay.io/ginigangadharan/todo-app:2.0`. **Boundary:** два разных image/port assumptions, текущий digest и работоспособность не проверены; не выбирать «правильный» вариант без подтверждения.

## F-02 — [Source extraction issue] — Todo resources indentation
**p0686:** `ports: - containerPort: 3000` и затем `resources:` визуально вложен под ports entry, а `limits:` отступлен несогласованно с `requests:`. **p0685:** HPA требует корректного CPU request для процента загрузки. **Boundary:** extracted YAML нельзя считать валидным; последующий скриншот Running Pod не доказывает, что приведённые точные байты применялись. [Needs confirmation].

## F-03 — [Source code mismatch] — CA RoleBinding ServiceAccount namespace
**p0697:** ServiceAccount `elastic-hamster` создан в `ca-demo`, Role/RoleBinding в `ca-demo`, но `subjects[].namespace` в RoleBinding задан **`default`**. **p0698–p0699:** Deployment использует `serviceAccountName: elastic-hamster`, его скрипт должен читать Deployment через API. **Boundary:** манифест привязывает права другому namespaced subject, чем показанная workload; успешный API read/динамика генератора не доказаны. Не исправлять без согласованной проверки.

## F-04 — [Source code mismatch] — CA HPA apiVersion/metrics
**p0698:** `ca/elastic-hamster-hpa.yaml` использует `apiVersion: autoscaling/v1` вместе с `spec.metrics` и `type: Resource`/target/`averageUtilization`, в отличие от `autoscaling/v2` Todo HPA p0689. **Boundary:** исходник не подтверждает, что такое поле поддерживается конкретным API в указанной версии. Невозможно назвать этот точный YAML валидированным, хотя p0698–p0699 сообщает `created`. [Needs confirmation].

## F-05 — [Source code mismatch] — kubectl top pod prints nodes
**p0699:** перед таблицей с `gke-k8sdemo-default-pool-...` node names, колонками `CPU(cores)`, `CPU%`, `MEMORY(bytes)`, `MEMORY%` напечатана команда **`kubectl top pod -n ca-demo`**. **p0696:** node metrics and allocatable обсуждаются отдельно. **Boundary:** формат таблицы не соответствует заявленному объекту Pod, а число узлов не подтверждено именно этой командой; возможна подмена фрагмента вывода.

## F-06 — [Source wording/code mismatch] — GKE --region vs zonal location
**p0693:** команда создания `gcloud container clusters create k8sbible ... --region=us-central1-a`, объяснение называет `us-central1-a` регионом, но JSON endpoint вывода `/zones/us-central1-a/clusters/k8sbible` и столбец LOCATION `us-central1-a`. **p0694:** другая команда использует `--zone=us-central1-a`. **Boundary:** выбор flag/location противоречив; нельзя выполнять как проверенный GKE CLI рецепт [Needs confirmation].

## F-07 — [Source wording/code mismatch] — GKE CA verification targets another cluster/pool
**p0694:** `gcloud container clusters update k8sforbeginners --node-pool=nodepool1`, затем «проверить CA» через `gcloud container node-pools describe default-pool --cluster=k8sdemo`. **Boundary:** два разных имени кластера и пула; `autoscaling.enabled:true` в выводе не доказывает успешную настройку `k8sforbeginners/nodepool1`.

## F-08 — [Source contradiction] — in-place resizing alpha vs stable footnote
**p0675–p0676:** InPlacePodVerticalScaling описан как alpha, требующий `--feature-gates` на узлах и редактирования API server manifest. **p0676 footnote:** прямо говорит, что с выходом Kubernetes v1.35 функционал **stable** и флаг больше не нужен. **Boundary:** это разные version-scoped утверждения в одной инструкции; определять подход по версии/провайдеру без внешней проверки нельзя. Изменение API-server манифеста может быть разрушительным.

## F-09 — [Source wording/code mismatch] — VPA Auto future vs deprecated note
**p0680:** `Auto` представлен как текущий эквивалент `Recreate`, который **в будущем** перейдёт к in-place обновлениям. Сноска к этому же разделу называет Auto **deprecated** с заменой `InPlaceOrRecreate`. **Boundary:** описание и сноска относятся к разным этапам развития API; текущая семантика `Auto`/роллаута в целевой платформе [Needs confirmation].

## F-10 — [Needs confirmation] — VPA requires pod restart / source version
**p0675:** сказано, что единственный способ изменить requests/limits — удалить/пересоздать Pod; **p0675–p0676:** затем описана InPlacePodVerticalScaling и версия 1.35. **Boundary:** первое утверждение не может быть универсальным для всех указанных источником версий; VPA admission/updater behavior требует version-scoped проверки. Источник демонстрирует только пересоздание p0682.

## F-11 — [Needs confirmation] — VPA installation runs mutable remote script
**p0677:** `git clone https://github.com/kubernetes/autoscaler` и `./hack/vpa-up.sh`, без pin SHA/review. **Boundary:** установка CRD/controllers в `kube-system`, RBAC/admission и совместимость текущего Kubernetes непроверены, supply chain и безопасная деинсталляция отсутствуют.

## F-12 — [Source wording/code mismatch] — manual scale demo target differs
**p0688:** приведена ручная `kubectl scale deployment one-page-web -n hpa-demo --replicas 3`, в то время как actual Deployment в p0686 и HPA scaleTargetRef p0689 — **`todo-app`**. **Boundary:** это разные Deployment имена; пример ручного масштабирования не является тестом HPA для `todo-app`.

## F-13 — [Needs confirmation] — resource Pending has multiple causes
**p0672:** запрос CPU `2000m` на Pod; **p0673:** события `FailedScheduling` говорят `1 node(s) had untolerated taint machine-check-exception:memory`, `2 Insufficient cpu`. **Boundary:** вывод не доказывает, что исключительно CPU request виноват во всём кластере; учебный taint из предыдущей главы явно присутствует.

## F-14 — [Needs confirmation] — sample VPA memory recommendation with top zero
**p0679:** `kubectl top pod` выводит для hamster `0Mi` памяти, **p0681:** VPA рекомендует `Memory 262144k` (~256 MiB) и верхнюю границу 500Mi. **Boundary:** источником не объясняется расхождение метрик памяти и target; не выводить точный алгоритм VPA из этих двух строк.

## F-15 — [Source wording/code mismatch] — Node scale-up count and command
**p0699:** текст сообщает «в кластере их всего десять», сопровождая таблицей **команды top pod**, не `kubectl get nodes`; таблица обрезана после нескольких node имен. **p0700:** в конце показано 2 node через `kubectl get nodes`. **Boundary:** десять узлов описаны автором, но строгий список 10 Ready узлов в приведённом p0699 output не доказан.

## F-16 — [Source contradiction] — eight-node versus ten-node cost wording
**p0699–p0700:** CA достиг указанного `--max-nodes 10` и затем сократился до 2. **p0700:** сравнение стоимости неожиданно говорит о «постоянной эксплуатации восьмиузлового кластера». **Boundary:** источник сравнивает разные размеры; нельзя приписывать этому опыту проверенную разницу в цене для точного node count.

## F-17 — [Needs confirmation] — CA scaling estimates vs actual CPU
**p0691:** CA принимает решения с учётом запросов контейнеров; **p0692:** сказано «на основе requests и limits ... не фактической нагрузки». **p0699:** 25 Pod × 500m CPU requests и max 10 nodes описаны как причина расширения. **Boundary:** роль limits относительно requests дана неоднозначно; алгоритм/квоты и решение для конкретной VM capacity [Needs confirmation]. Не выводить цену или ресурсы одного GKE node из скриншота.

## F-18 — [Needs confirmation] — HPA source target unknown at initial stage
**p0689:** `kubectl get hpa` показывает `cpu: <unknown>/80%`, `REPLICAS 0`; далее текст утверждает baseline **1** replica и source p0690 после нагрузки показывает **3**. **Boundary:** начальные `<unknown>/0` могут быть временным состоянием, но синхронизация метрик в момент скриншота не установлена; не считать этот вывод исправным стабильным HPA.

## F-19 — [Needs confirmation] — autoscaler scale-down timing and cost
**p0695:** для AKS упомянуты 10s scan и 10m scale-down delay; **p0700:** в GKE опыте «через 10 минут» CA уменьшает nodes до 2. **Boundary:** одинаковый таймер/порог не доказаны для обеих платформ; реальная задержка, eviction behavior, PDB и расходы [Needs confirmation].

## F-20 — [Needs confirmation] — KEDA/Karpenter no runbook
**p0701–p0703:** описаны возможности KEDA и Karpenter, но **не** предоставлены ни установка, ни `ScaledObject`, ни Karpenter node provisioning YAML, ни проверочный тест. **Boundary:** преимущества и интеграции авторские концептуальные тезисы, не validated deployment recipes; нельзя дополнять эти разделы командами по памяти.

## F-21 — [Needs confirmation] — HPA/CA Kubernetes names and workload
**p0696–p0700:** CA lab names GKE cluster `k8sdemo` и Deployment `elastic-hamster`, HPA `elastic-hamster-hpa`; другой GKE example создаёт кластер `k8sbible` (p0693) и обновляет `k8sforbeginners` (p0694). **Boundary:** три разных кластера в одном разделе без промежуточного детального transition, нельзя выполнять команды как одну непрерывную последовательность.

## F-22 — [Needs confirmation] — cleanup incomplete for cloud autoscalers
**p0690:** явная команда удаления HPA namespace, **p0700:** предлагает очистить кластер/отключить CA, но без точных GKE/AKS cleanup commands; VPA demo cleanup тоже отсутствует. **Boundary:** full rollback/guaranteed zero billing не продемонстрированы; cloud deletion разрушительна, её нельзя домысливать.

**No execution:** вся проверка основана только на текстовых страницах источника. Canonical PDF, RAG, registry/metadata и reading progress/status не затронуты.
