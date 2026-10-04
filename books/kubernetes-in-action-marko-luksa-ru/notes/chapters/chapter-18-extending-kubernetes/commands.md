# Глава 18 — команды и инструменты

Только команды, явно подтвержденные RAG главы 18.

> Важно: это source-era Kubernetes/Helm examples. Совместимость с современными API и CLI — **[Needs confirmation]**.

| Команда | Класс | Назначение | Effect / risk | Verification | Rollback |
|---|---|---|---|---|---|
| `kubectl create -f website-crd-definition.yaml` | state-changing | Регистрирует CRD `Website` | Добавляет новый API resource type | `kubectl get websites` после создания экземпляра | [Needs confirmation] |
| `kubectl create -f kubia-website.yaml` | state-changing | Создает экземпляр `Website` | При активном controller может породить Deployment/Service | `kubectl get website kubia -o yaml` | `kubectl delete website kubia` |
| `kubectl get websites` | read-only | Список custom resources | Нет изменения | Вывод содержит `kubia` | Not applicable |
| `kubectl get website kubia -o yaml` | read-only | Полное представление custom resource | Нет изменения | YAML содержит metadata/spec | Not applicable |
| `kubectl delete website kubia` | state-changing | Удаляет экземпляр Website | Custom controller может реагировать на удаление; точное cleanup behavior source example не раскрывает | Проверка отсутствия объекта: [Needs confirmation] | [Needs confirmation] |
| `kubectl create serviceaccount website-controller` | state-changing | Создает ServiceAccount контроллера | Добавляет identity в namespace | [Needs confirmation] | [Needs confirmation] |
| `kubectl create clusterrolebinding website-controller --clusterrole=cluster-admin --serviceaccount=default:website-controller` | state-changing | Дает controller права через ClusterRoleBinding | **Высокий риск:** привязка к `cluster-admin` | Controller получает доступ к нужным resources | [Needs confirmation] |
| `kubectl logs website-controller-2429717411-q43zs -c main` | read-only | Читает logs main container controller | Нет изменения | В source видны ADDED и HTTP 201 Created | Not applicable |
| `kubectl get deploy,svc,po` | read-only | Проверяет объекты, созданные controller | Нет изменения | Deployment, Service и Pods присутствуют | Not applicable |
| `kubectl get serviceclass postgres-database -o yaml` | read-only | Показывает Service Catalog class | Нет изменения | YAML класса доступен | Not applicable |
| `kubectl get secret postgres-secret -o yaml` | read-only | Показывает Secret binding credentials | Нет изменения, но вывод содержит чувствительные данные | Secret существует | Not applicable |
| `git push deis master` | workload-generating / state-changing | Инициирует deployment через Deis Workflow | Запускает delivery pipeline Workflow | [Needs confirmation] | Source упоминает rollbacks как feature, конкретная команда не дана |
| `helm install --name my-database stable/mysql` | state-changing | Устанавливает MySQL из Helm chart | Создает Deployments, Services, Secrets и PVC | Проверить созданные resources | [Needs confirmation] |

## Source-specific YAML/API identifiers

В главе явно используются:

- `apiextensions.k8s.io/v1beta1`
- `apps/v1beta1`
- `apiregistration.k8s.io/v1beta1`
- `servicecatalog.k8s.io/v1alpha1`

Эти версии следует воспринимать как часть источника. Их актуальность в текущем Kubernetes не подтверждалась.

## Security boundary

Команда с `cluster-admin` демонстрационная и предоставляет широкие кластерные полномочия. Источник не приводит минимальный набор RBAC permissions для controller.

Least-privilege вариант: **[Needs confirmation]**.
