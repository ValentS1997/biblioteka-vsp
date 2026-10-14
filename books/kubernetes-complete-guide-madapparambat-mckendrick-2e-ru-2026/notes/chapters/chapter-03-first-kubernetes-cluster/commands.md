# Команды и инструменты — Глава 3 (source-confirmed)

**Формат:** дословно приведенные в RAG команды нормализованы только по однозначным переносам PDF. **Ни одна из них не выполнялась.** Код в блоках ниже — учебные фрагменты, **не готовые безопасные production runbooks**.

## Read-only / observation

| Команда из RAG | Классификация | Назначение / provenance |
|---|---|---|
| `which minikube` | read-only | Проверка пути к исполняемому minikube (p0117) |
| `minikube config view driver` | read-only | Текущая настройка драйвера (p0119) |
| `minikube status` | read-only | Статусы host, kubelet, apiserver, kubeconfig (p0122, p0126) |
| `kubectl config view` | read-only, sensitive output | Отображение конфигурации, может содержать сведения об учетных данных (p0125) |
| `kubectl config current-context` | read-only | Проверка целевого кластера (p0125) |
| `kubectl get nodes` | read-only | Список и состояние узлов (p0125, p0127, p0128, p0133) |
| `kubectl get componentstatuses` | read-only, deprecated | В самой книге warning `v1 ComponentStatus is deprecated in v1.19+` (p0125) |
| `minikube profile list` | read-only | Список minikube профилей (p0129) |
| `kind version` | read-only | Версия установленного kind (p0131) |
| `kubectl cluster-info` | read-only | Информация о контрольной плоскости и DNS (p0134) |
| `kubectl cluster-info --context kind-my-kind-cluster` | read-only | Явно заданный контекст в выводе kind (p0133) |
| `kubectl get --raw='/readyz?verbose'` | read-only | Readiness endpoint API, в примере `readyz check passed` (p0134) |
| `cat ~/.kube/config` | read-only, sensitive output | Пример просмотра kubeconfig, не распространять содержимое (p0124) |

`kubectl cluster-info dump` **упоминается текстом** на p0134, но сопровожден примером **другой** команды (`kubectl get --raw='/readyz?verbose'`); не приписывать им идентичную семантику. См. [source-findings.md](source-findings.md).

## Установка minikube — state-changing на локальном хосте

**Linux, p0117:**

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
which minikube
```

**macOS, p0118** (в образце `amd64`, в сноске предлагается `arm64` для Apple Silicon):

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
which minikube
```

**Windows, p0118 — альтернативы, не совместный сценарий:**

```powershell
winget install minikube
choco install minikube
```

**Эффект:** загрузка и установка исполняемых файлов/пакетов. **Риски:** права администратора, совместимость архитектуры, PATH, непроверенная версия `latest` и отсутствие процедуры проверки скачанного файла в главе. **Verification:** `which minikube` (Linux/macOS, p0117–p0118). **Rollback:** [Needs confirmation].

## Настройки minikube — state-changing configuration

Примеры p0118–p0119:

```bash
minikube config set cpus 4
minikube config set memory 16000
minikube config set container-runtime containerd
minikube config set driver docker
minikube config set driver virtualbox
minikube config view driver
```

`config set` модифицирует настройки. В образцах CLI сообщает `These changes will take effect upon a minikube delete and then a minikube start`. **Риск:** `delete` уничтожает кластер. **Verification:** `minikube config view driver` подтверждена только для драйвера; остальные детали [Needs confirmation]. **Rollback:** [Needs confirmation], не пересоздавать без согласованного плана.

## Создание кластера — workload-generating / state-changing

В RAG присутствуют следующие полные вызовы:

```bash
minikube start --driver=docker
minikube start --driver=virtualbox --memory=8000m --cpus=2
minikube start --driver=virtualbox --memory=8000m --cpus=2 --kubernetes-version=1.29.0
minikube start --driver=docker --kubernetes-version=1.29.0
minikube start --driver=podman
minikube start --driver=podman --nodes=3
```

RAG p0119–p0128. **Эффект:** создает/запускает учебную кластерную среду, изменяет kubeconfig, загружает образы. **Риски:** ресурсная нагрузка, переключение активного контекста, несовместимость драйвера/версии. **Verification:** `minikube status`, `kubectl config current-context`, `kubectl get nodes`. **Rollback:** `minikube stop` останавливает, но не удаляет; уничтожение данных `delete` — не безопасный rollback.

**HA minikube, дословная логика многострочного вызова p0128:**

```bash
minikube start \
  --driver=virtualbox \
  --nodes=5 \
  --ha=true \
  --cni=calico \
  --cpus=2 \
  --memory=2g \
  --kubernetes-version=v1.30.0 \
  --container-runtime=containerd
```

По книге создает 3 управляющих и 2 вычислительных узла. **Не запускать без оценки ресурсов**. Возможность и совместимость на текущих версиях [Needs confirmation].

**Несколько профилей, p0128–p0129:** опция `--profile=cluster-vbox` для VirtualBox и `--profile=clusterdocker` для Docker. В PDF перенос строк между опциями неполон; **не реконструируем автоматически готовую команду**. Проверенный вызов для списка: `minikube profile list`.

## Lifecycle minikube — state-changing

```bash
minikube stop
minikube pause
minikube unpause
minikube delete
minikube stop --profile=cluster-docker
minikube delete --profile=cluster-docker
```

- `stop`: останавливает кластер, **сохраняет состояние**; по p0126 возобновление `minikube start`. Проверка `minikube status`.
- `pause`: приостанавливает рабочие компоненты; `unpause` — подтвержденное возвращающее действие (p0126–p0127).
- `delete`: **уничтожает кластер и его состояние**, по книге восстановление недоступно (p0127). **Rollback:** [Needs confirmation]; **допуск:** только явно идентифицированный disposable-кластер.
- Параметр `--profile` задает конкретный minikube-профиль; перед удалением проверить `minikube profile list` (p0129).

## Установка kind — state-changing на локальном хосте

**Linux, p0130–p0131:**

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind version
```

**macOS (версия v0.20.0 в примере) / Homebrew, p0131:**

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-darwin-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/kind
brew install kind
```

**Windows / Chocolatey / Go, альтернативные варианты p0131:** `curl.exe -Lo kind-windows-amd64.exe ...`, `Move-Item`, `choco install kind`, `go install sigs.k8s.io/kind@v0.22.0 && kind create cluster`. Последний вызов **одновременно устанавливает инструмент и создает кластер**: это workload-generating. Схема контроля целостности скачанного файла и rollback установки в главе отсутствует: **[Needs confirmation]**.

## kind cluster — workload-generating / state-changing

```bash
kind create cluster --name test-kind
KIND_EXPERIMENTAL_PROVIDER=podman kind create cluster
kind create cluster --config ~/.kube/kind_cluster
kind delete cluster
```

Источник p0131–p0132. `kind create cluster` создает контейнерные узлы; `kind delete cluster` удаляет локальный кластер. **Внимание:** p0131 создает именованный `test-kind`, но p0132 дает `kind delete cluster` без `--name`, сохраняя вывод `Deleting cluster "kind"`; **не считать эту команду подтвержденным удалением ранее созданного `test-kind`**. См. source-findings.

Конфигурация **из p0132**, учебный пример, сохраняется в `~/.kube/kind_cluster`:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
  - role: worker
```

Книга также дает отдельный `kind create cluster --name=my-kind-cluster --config=~/.kube/kind_cluster --image=kindest/node:v1.29.0@sha256:...` (p0133): полный digest присутствует в RAG, но он **не подменяется непроверенным текущим образом** и не приводится как универсальная инструкция. **Verification:** `kubectl get nodes`, `kubectl cluster-info`, `kubectl get --raw='/readyz?verbose'` (p0133–p0134). **Rollback после delete:** [Needs confirmation]; состояние стирается.

## Source findings / boundaries

`kind stop` упоминается на p0134 как команда остановки, но не доказана и **не предлагается здесь для выполнения** до разрешения [Needs confirmation]. `kubectl get componentstatuses` сам источник помечает deprecated. Не исправлять исходные варианты молча. Актуальность URL/версий, безопасность загружаемых бинарников и производственные требования за пределами RAG — [Needs confirmation].
