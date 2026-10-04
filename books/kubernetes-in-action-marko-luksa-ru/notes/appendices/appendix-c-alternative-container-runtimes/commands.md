# Приложение C — команды

| Команда | Класс | Назначение | Риск / effect | Verification | Rollback |
|---|---|---|---|---|---|
| `minikube start --container-runtime=rkt --network-plugin=cni` | state-changing | Запускает Minikube с rkt + CNI | Меняет runtime baseline | `kubectl describe pods` | [Needs confirmation] |
| `minikube delete` | destructive | Удаляет существующую Minikube VM | Потеря локального cluster state | VM отсутствует | [Needs confirmation] |
| `kubectl run kubia --image=luksa/kubia --port 8080` | state-changing | Создает workload | Создает Deployment | `kubectl describe pods` | [Needs confirmation] |
| `kubectl describe pods` | read-only | Показывает runtime/container IDs | Нет | `rkt://...` в source example | N/A |
| `minikube ssh` | interactive/read-only by itself | Вход в Minikube VM | Дальнейшие команды могут менять VM | shell opened | exit |
| `rkt list` | read-only | Список Pods/containers rkt | Нет | table output | N/A |
| `rkt image list` | read-only | Список images rkt | Нет | image list | N/A |

Упомянутый параметр Kubelet `--container-runtime=rkt` и Minikube `--container-runtime=crio` — source-era configuration. Current applicability: **[Needs confirmation]**.
