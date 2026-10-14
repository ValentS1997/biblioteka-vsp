# Cheatsheet — Глава 3. Установка первого кластера Kubernetes

**RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0115:c01` — `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0142:c01`; PDF/printed 115–142. Все команды ниже **из этой главы**, а не из внешней документации.

## Symptom / problem framing

Для выполнения упражнений нужен доступный кластер Kubernetes, но ручная установка компонентов управляющего слоя трудоемка. Глава выбирает инструменты быстрого локального развертывания `minikube` и `kind`, а затем показывает проверку узлов и доступности API (p0115–p0116, p0120–p0125, p0129–p0135).

## Baseline / context

**Минимум из книги** (p0116): установленный `kubectl`, ≥2 CPU, ≥2 ГБ RAM, ≥20 ГБ disk, надежный Интернет и подходящий контейнерный движок или гипервизор. Многоузловой/HA-кластер расходует больше ресурсов (p0127–p0128).

| Сценарий | Источник | Важная граница |
|---|---|---|
| `minikube` одноузловой | p0116–p0126 | Локальное обучение, выбор драйвера VirtualBox/Docker/Podman |
| `minikube --nodes=3` | p0127 | 1 control plane, 2 worker в примере |
| `minikube --ha=true --nodes=5` | p0128 | 3 control plane, 2 worker в примере, повышенные ресурсы |
| `kind` + YAML | p0129–p0134 | Контейнеры играют роль узлов; 1 control plane + 3 worker |
| Killercoda | p0135 | Временная браузерная лаборатория, не долговременное хранилище |
| GKE, AKS, EKS | p0136 | Управляемые облачные production-решения, подробнее — главы 15–17 |
| on-prem, kubeadm, kops, Kubespray, IaC | p0137–p0141 | Самостоятельное обслуживание: HA, storage, сеть, security, upgrade |

**Контексты kubectl:** `minikube start` и `kind create cluster` в примерах настраивают `~/.kube/config` и переключают контекст; контекст перед командами всегда следует проверять (p0124–p0125, p0133).

## Read-only checks

```bash
which minikube
minikube config view driver
minikube status
minikube profile list
kubectl config current-context
kubectl config view
kubectl get nodes
kind version
kubectl cluster-info
kubectl get --raw='/readyz?verbose'
```

Это команды из p0117, p0119, p0122, p0125, p0129, p0131, p0134. Некоторые обращаются к активному контексту Kubernetes; не считать результатом проверку другой среды. `cat ~/.kube/config` в исходнике тоже демонстрируется (p0124), **но содержимое kubeconfig может включать учетные данные; не публиковать вывод**.

Команда `kubectl get componentstatuses` показана в p0125, но сам пример содержит предупреждение **`ComponentStatus is deprecated in v1.19+`** — не использовать как универсальную гарантию health современного кластера без уточнения.

## Interpretation

- `minikube status` с `host/kubelet/apiserver: Running` и `kubeconfig: Configured` в примере указывает на запущенную локальную среду (p0122).
- `kubectl config current-context` должен указывать на задуманный учебный кластер. Если не так, **не запускать команды изменения** (p0125, p0133).
- `kubectl get nodes` в образце minikube показывает один узел `Ready`; для трех узлов пример возвращает три; kind YAML создает четыре (p0125, p0127, p0133).
- `kubectl get --raw='/readyz?verbose'` в книге возвращает `readyz check passed` (p0134); это диагностический пример, не формальный production acceptance.
- Ошибка `PROVIDER_PODMAN_NOT_FOUND` означает, что драйвер Podman не обнаружен в `PATH` в показанной конфигурации (p0123).
- Состояние `Stopped` после `minikube stop` не означает удаления; `minikube delete` состояние уничтожает (p0126–p0127).

## Next action

Выбрать среду (`minikube`, `kind`, временный Killercoda либо отдельный production-путь), проверить ресурсы хоста и установленный драйвер, выполнить создание **только в разрешенной учебной среде**, затем read-only проверки контекста и узлов. Для production по книге требуется отдельная архитектурная оценка (p0136–p0141).

## Modifying action

**Примеры учебной установки из источника, не запускать автоматически:**

```bash
minikube start --driver=docker --kubernetes-version=1.29.0
minikube start --driver=podman --nodes=3
kind create cluster --name test-kind
```

**Эффект:** создание Kubernetes-кластера, загрузка образов, изменение локального `kubeconfig`; при некоторых драйверах создание ВМ/контейнеров (p0121–p0125, p0127, p0131–p0133). **Риски:** потребление ресурсов, переключение активного контекста, несовместимость версий/драйвера, потенциальный конфликт с существующим профилем; платформа/разрешение **[Needs confirmation]**.

Конфигурационные изменения `minikube config set` также модифицируют настройки; по p0118–p0119 некоторые вступают в силу только после `minikube delete` и повторного `minikube start`: **не делать это с кластером с ценными данными**.

## Verification / acceptance checks

После `start` источник предлагает `minikube status`, `kubectl config current-context`, `kubectl get nodes` (p0122, p0125). Для kind используются `kubectl get nodes`, `kubectl cluster-info`, `kubectl get --raw='/readyz?verbose'` (p0133–p0134). Проверять соответствие **фактически созданному профилю/кластеру**, а не обещать точные имена и версии из снимков книги.

Для production потребуются отдельные критерии надежности, резервного копирования, хранения, мониторинга и безопасности; точные значения и тесты **[Needs confirmation]** (p0136–p0141).

## Rollback

| Действие | Источник | Что подтверждено |
|---|---|---|
| `minikube stop` | p0126 | Кластер останавливается, состояние сохраняется; возобновление `minikube start` |
| `minikube pause` | p0126–p0127 | `minikube unpause` возвращает работу |
| `minikube delete` | p0127 | Состояние удаляется без обратимого восстановления по тексту главы; rollback **[Needs confirmation]** |
| `kind delete cluster` | p0132, p0134 | Данные и локальные узлы удаляются; восстановление **[Needs confirmation]** |
| `minikube config set` | p0118–p0119 | Требуется контролируемое пересоздание; обратимая процедура и сохранение данных **[Needs confirmation]** |
| Установка бинарников и пакетов | p0117–p0118, p0130–p0131 | Откат установленной версии **[Needs confirmation]** |

**Особое внимание:** в p0134 заявлен `kind stop`; подтвержденного воспроизводимого механизма в RAG нет. Он зарегистрирован в [source-findings.md](source-findings.md) и **не предлагается как проверенная команда остановки**.

## Source boundaries

Только главы 3 и RAG, без проверки ссылок из перечня «Дополнительные источники». Текущие версии/реальная установка [Needs confirmation]. Команды изменения кластера должны рассматриваться только после подтверждения цели и ее допуска.
