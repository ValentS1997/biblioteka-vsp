# Приложение A — команды

| Команда | Класс | Назначение | Риск / effect | Verification | Rollback |
|---|---|---|---|---|---|
| `minikube start` | state-changing | Запускает Minikube и перенастраивает kubectl | Меняет active kubeconfig context | `kubectl config current-context` | [Needs confirmation] |
| `gcloud container clusters get-credentials my-gke-cluster` | state-changing | Настраивает kubectl для GKE cluster | Меняет kubeconfig | `kubectl config current-context` | Переключить context обратно |
| `kubectl config current-context` | read-only | Показывает active context | Нет | Вывод context | N/A |
| `kubectl config get-contexts` | read-only | Список contexts | Нет | Таблица contexts | N/A |
| `kubectl config get-clusters` | read-only | Список clusters | Нет | Список cluster names | N/A |
| `kubectl config set-cluster ...` | state-changing | Добавляет/перезаписывает cluster entry | Может перезаписать существующую конфигурацию | `get-clusters` | [Needs confirmation] |
| `kubectl config set-credentials ...` | state-changing | Добавляет/меняет credentials | Изменяет auth data; секреты чувствительны | [Needs confirmation] | [Needs confirmation] |
| `kubectl config set-context ...` | state-changing | Создает/меняет context | Меняет cluster/user/default namespace mapping | `get-contexts` | [Needs confirmation] |
| `kubectl config use-context my-other-context` | state-changing | Переключает active context | Следующие kubectl-команды идут в другой cluster/namespace | `current-context` | `use-context <previous>` |
| `kubectl config delete-context ...` | state-changing | Удаляет context | Потеря kubeconfig entry | `get-contexts` | [Needs confirmation] |
| `kubectl config delete-cluster ...` | state-changing | Удаляет cluster entry | Потеря kubeconfig entry | `get-clusters` | [Needs confirmation] |

Source-era syntax; current compatibility: **[Needs confirmation]**.
