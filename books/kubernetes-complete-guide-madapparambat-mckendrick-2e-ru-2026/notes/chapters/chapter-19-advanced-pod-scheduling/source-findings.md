# Source findings — Глава 19, продвинутое планирование Pod

**RAG-only:** p0641:c01–p0667:c01, PDF 641–667. Категории: [Source contradiction], [Source code mismatch], [Source wording/code mismatch], [Source extraction issue], [Needs confirmation]. Не исправлять по внешней документации или памяти модели.

## F-01 — [Source contradiction] — scheduler version/config mismatch
**p0664:** источник поясняет, что старые predicate/priority policies заменены конфигурацией планировщика в Kubernetes v1.23. **p0666:** якобы пример актуальной конфигурации `apiVersion: kubescheduler.config.k8s.io/v1alpha1`, `algorithmSource.provider: DefaultProvider` и `percentageOfNodesToScore: 50`. **Boundary:** фрагмент со старой формой рядом с описанием современного подхода; нет проверки schema, запуска scheduler или совместимости. Не применять как работающий конфиг [Needs confirmation].

## F-02 — [Source extraction issue] — удаление двух taints на p662
**p0662:** «удалите оба ограничения» и поврежденная строка `kubectl taint node minikube machine-check-exception-node/ minikube untainted`. **p0658:** отдельно показаны корректно оформленные для источника effect-qualified удаления `machine-check-exception=memory:NoExecute-` и `machine-check-exception:NoExecute-`. **Boundary:** указание p662 нельзя исполнить как есть; не реконструировать команду молча и не заявлять успешное снятие обоих эффектов [Needs confirmation].

## F-03 — [Source code mismatch] — generic taint syntax p658
**p0658:** общий шаблон напечатан как `kubectl taint node =:<имяУзла> <ключ>=<значение>:<эффект>`. **p0658:** реальный пример `kubectl taint node minikube machine-check-exception=memory:NoExecute` не содержит `=:`. **Boundary:** формула повреждена и не эквивалентна рабочему примеру; использовать лишь подтверждённый конкретный вариант для чтения.

## F-04 — [Source code mismatch] — nodeSelector manifest path
**p0650:** file heading `02_nodeselector/nginx-deployment.yaml`, но инструкция apply извлечена как `02_nodeselector/nginx deployment.yaml` (между nginx и deployment пробел). **p0651:** отдельный `02_nodeselector/nginx-deployment-slow.yaml`. **Boundary:** команда p650 требует проверки точного имени файла в оригинальном репозитории [Needs confirmation].

## F-05 — [Source contradiction] — Kubernetes version changes in sample
**p0644–p0645:** minikube запускается с `--kubernetes-version=v1.30.0`, три `kubectl get nodes` показывают `v1.30.0`. **p0649:** тот же по названиям узлов вывод `kubectl get nodes --show-labels` показывает `v1.31.0`. **Boundary:** между примерами отсутствует шаг upgrade; это не одна подтвержденная неизменная сессия/версия. [Needs confirmation].

## F-06 — [Source extraction issue] — truncated node label/run output
**p0656:** последний `NODE` из пяти Running Pod после rollout restart обрывается на `mi`; текст говорит, что все на `minikube`. **Boundary:** текстовая интерпретация присутствует, но полный последний Pod NODE не доступен в извлеченной таблице; не считать пять полных табличных доказательств.

## F-07 — [Needs confirmation] — rollout restart availability guarantee
**p0655–p0656:** source считает `kubectl rollout restart deployment nginx-app` способом перезапуска без уменьшения доступных экземпляров. **p0651:** при несовместимом `nodeSelector` rollout уже блокировался. **Boundary:** доступность зависит от стратегии, readiness, ресурсов и совместимых узлов; нулевой downtime не подтвержден источником для произвольной конфигурации.

## F-08 — [Source wording/code mismatch] — nodeName apply `created` twice
**p0646:** `kubectl apply -f 01_nodename/nginx-deployment.yaml` создаёт `nginx-app`; **p0647:** после изменения `template.spec.nodeName` та же `kubectl apply` снова показывает `deployment.apps/nginx-app created`, хотя проза говорит об обновлении существующего Deployment и появлении нового ReplicaSet. **Boundary:** текстовая последовательность и вывод `created` vs update расходятся; не утверждать оба вывода как последовательный факт без дополнительного шага.

## F-09 — [Needs confirmation] — Node labels affect unrelated workloads
**p0649–p0655:** `kubectl label nodes --overwrite` меняет `node-type` на трёх узлах. **Boundary:** не предоставлено RBAC/scope validation или анализ чужих Pod, которым требуются эти labels. Удаление или возврат старых значений не описаны в source [Needs confirmation].

## F-10 — [Needs confirmation] — NoExecute evicts existing Pods
**p0657–p0662:** `kubectl taint node minikube machine-check-exception=memory:NoExecute` выселяет Pod, сочетание с `NoSchedule` устраняет churn. **Boundary:** эксперимент на живых узлах разрушителен для workload; источник не содержит проверки PDB/backup/гарантированного восстановления данных [Needs confirmation].

## F-11 — [Source wording/code mismatch] — sample node vs node metadata consistency
**p0644–p0645:** кластер назван v1.30.0; **p0649:** labels содержат `minikube.k8s.io/version=v1.33.1` и `node VERSION=v1.31.0`, при этом текст не отделяет минikube tool version от Kubernetes node version. **Boundary:** поля представляют разные сведения, не выводить единый version факт из одного `minikube.k8s.io/version` [Needs confirmation].

## F-12 — [Needs confirmation] — static Pod URL delivery
**p0663:** kubelet якобы может считывать YAML с веб-сервера или с файловой системы, создаёт mirror Pods, не поддерживает Secret/ConfigMap. **Boundary:** конкретные kubelet флаги, URL verification, CA/pinning, файл, ServiceAccount и демонстрация работоспособности отсутствуют. Current support и security [Needs confirmation].

## F-13 — [Needs confirmation] — managed control plane access
**p0642:** для AKS/EKS авторы говорят, что kube-scheduler config не доступна напрямую; **p0664–p0666:** описаны ручные scheduler profiles/plugins. **Boundary:** эти главы не показывают как применить настройку к managed control plane. Live support/access [Needs confirmation].

## F-14 — [Needs confirmation] — protected node labels
**p0665:** `NodeRestriction` + Node authorizer запрещают kubelet самовольную модификацию защищённых labels. **Boundary:** source не включает эти механизмы командой и не доказывает actual protected labels на указанном lab; изоляция зависит от реальной конфигурации [Needs confirmation].

## F-15 — [Needs confirmation] — performance parameter and benchmark
**p0665–p0666:** `percentageOfNodesToScore` значения 50% для 100 узлов, 10% для 5000 узлов и диапазон 1–100; `50` в YAML. **Boundary:** нет бенчмарка планировщика, валидного deployment config и результата исполнения; число анализируемых узлов и точное поведение для живой версии не установлены [Needs confirmation].

## F-16 — [Needs confirmation] — toleration operator version claim
**p0659 footnote:** утверждается, что в v1.35 для toleration появились числовые `Gt`/`Lt`. **p0644:** демонстрация v1.30.0 и вывод v1.31.0. **Boundary:** данное утверждение относится к другой версии, не проверено на лабораторном кластере; source experiments используют только `Equal`, не `Gt`/`Lt`.

## F-17 — [Source wording/code mismatch] — NotIn and absence of label
**p0653–p0654:** жёсткое правило `NotIn extremelyslow` трактуется как исключение лишь узлов с этим значением; source уже назначает конкретный `node-type` всем трём узлам. **Boundary:** поведение для **узлов без ключа** `node-type` в опыте не проверено; не выводить универсальный результат для отсутствующей метки без проверки [Needs confirmation].

## F-18 — [Needs confirmation] — capacity and automatic fallback
**p0653:** preferred fast/superfast допускает `slow` fallback при нехватке ресурсов; hard rules исключают extremelyslow. **p0656:** все пять Pod размещены на `minikube`. **Boundary:** источником не испытана ситуация фактического resource pressure и Pod Pending, приоритеты и веса не дают гарантии вместимости или оптимальности для другой рабочей нагрузки [Needs confirmation].

**Execution boundary:** не было live изменения minikube, labels, Deployment, taints или scheduler; оригинал, RAG, registry и чтение не менялись.
