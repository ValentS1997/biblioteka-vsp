# Cheatsheet — Глава 2. Архитектура Kubernetes

**Source:** PDF 71–114; RAG chunks `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0071:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0114:c01`. **No live cluster inspected.**

## Symptom / problem framing

Как распределенный Kubernetes превращает описание нового Pod в рабочую нагрузку на конкретном узле и что произойдет при отказе управляющего слоя? В главе ответ строится через взаимодействия `kubectl → kube-apiserver → etcd → scheduler/controllers → kubelet → CRI/runtime` (стр. 79–96, 99–103, 113).

## Baseline / context

| Компонент | Функция из главы | RAG |
|---|---|---|
| `kube-apiserver` | API-вход: HTTP, аутентификация/авторизация, чтение и запись состояния | p0079–p0083 |
| `etcd` | Персистентное распределенное key-value хранилище кластера | p0083–p0085 |
| `kube-scheduler` | Подбирает узел для Pod без `nodeName` | p0086–p0087 |
| `kube-controller-manager` | Контроллеры выполняют reconciliation desired/actual state | p0088–p0089 |
| `cloud-controller-manager` | Контроллеры интеграции с облачной инфраструктурой | p0089–p0090 |
| `kubelet` | Агент узла: получает спецификацию Pod через API и обращается к локальной runtime | p0094–p0095 |
| `kube-proxy` | Участник сетевого слоя и механизма Service | p0095 |
| `containerd` / `CRI-O` | Среды выполнения контейнеров, интегрируемые через CRI | p0091–p0093 |
| `kubectl` | Клиент API; работает с `kubeconfig` и контекстами | p0096–p0107 |
| Multi-control-plane / etcd Raft | Отказоустойчивость управляющего слоя и согласованность реплик etcd | p0111–p0113 |

**Ключевой workflow:** `kubectl run` создает объект Pod через API; объект сохраняется в etcd; scheduler назначает узел; kubelet запускает контейнер через CRI. Подробности расписаны в главах p0085–p0095, p0103.

## Read-only checks

Только команды, **буквально приведенные в источнике**:

```bash
kubectl version
kubectl config view
kubectl get pods
kubectl get rs -n my-namespace
kubectl explain pod.spec.containers.image
echo $PATH
```

- `kubectl version`: информация о версии клиента; при отсутствии настроенного кластера источник показывает ошибку подключения (p0097).
- `kubectl config view`: просмотр используемой конфигурации/контекстов (p0102). **Конфигурация может относиться к учетным данным; ее вывод не публиковать без редактирования секретов.**
- `kubectl get pods`: список подов через API (p0103). **Область видимости результата нуждается в проверке**: глава не дает здесь явной namespace.
- `kubectl get rs -n my-namespace`: список ReplicaSet в указанном пространстве имен (p0104).
- `kubectl explain ...`: справка по полю API (p0107).
- `echo $PATH`: пути поиска двоичных файлов (p0097).

Для живого кластера не предоставлены достоверные выводы команд; **[Needs confirmation]**.

## Interpretation

- Pod **Pending/unscheduled**, `nodeName` пустой: по модели главы возможная зона — scheduler/доступность его экземпляров (p0086–p0087). Не ставить диагноз без наблюдений.
- Недоступен API-server: уже запущенные контейнеры могут оставаться работающими, но управляющие действия недоступны (p0082–p0083).
- Потеря данных etcd: критический риск для состояния кластера; редактирование etcd напрямую не рекомендуется (p0084).
- kubelet связывает спецификацию Pod с container runtime по Unix-сокету; доступ к сокету из контейнеров опасен (p0094–p0095).
- Одноузловой кластер — учебный; единственный управляющий узел — SPOF; несколько управляющих узлов требуют балансировки API и HA etcd (p0108–p0113).
- Описание исходником отдельных default-настроек требует проверки на целевой версии, см. [source-findings.md](source-findings.md).

## Next action

Уточнить фактическую топологию кластера, контекст/права `kubectl`, выбранную runtime и тип control plane. Следующая глава содержит практическую установку; не переносить из нее команды без RAG отдельного запроса (p0114).

## Modifying action

Примеры RAG (учебные, **не выполнять на рабочем кластере**):

```bash
kubectl run nginx --restart Never --image nginx
kubectl create -f pod.yaml
kubectl delete pods my-pod
```

Создают/удаляют ресурсы Pod через API (p0085, p0103–p0106). **Эффект:** состояние кластера изменится; **риск:** затронуты реальные Pod и выделяемые ресурсы. Точный контекст, namespace, полномочия и имена существующих ресурсов **[Needs confirmation]**.

## Verification / acceptance checks

В качестве наблюдения RAG дает `kubectl get pods` (p0103), однако его вывод не доказывает успешность приложения, готовность всех контейнеров и доступность сервиса. Четкие acceptance thresholds и дополнительные read-only проверки **[Needs confirmation]**.

При установке `kubectl` проверка `kubectl version` приводится в исходнике (p0097). Проверка скачанного файла на целостность в главе **[Needs confirmation]**.

## Rollback

Точные процедуры возврата после `kubectl create`, `kubectl run`, `kubectl delete`, изменений оболочки и системных пакетов **не описаны**; **[Needs confirmation]**. Порядок восстановления etcd в главе 2 также не приводится (p0113). Не считать удаление Pod автоматически безопасным rollback.

## Operational boundary

В исходнике есть команды `curl`, `chmod`, `sudo mv`, `sudo apt/yum install`, `echo >> ~/.bashrc`; они изменяют хост и требуют контролируемого плана (p0097–p0104). Никаких изменений среды этим набором артефактов не выполнялось.
