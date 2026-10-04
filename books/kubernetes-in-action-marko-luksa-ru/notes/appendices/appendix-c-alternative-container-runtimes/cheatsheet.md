# Приложение C — cheatsheet

## Symptom / problem framing

Нужно понять, как Kubernetes отделяет orchestration API от конкретной container runtime.

## Baseline / context

Source progression:

```text
Direct runtime integration
  → CRI
  → pluggable runtimes
```

## Read-only checks

```bash
kubectl describe pods
minikube ssh
rkt list
rkt image list
```

## Interpretation

- `Container ID: rkt://...` в `kubectl describe` подтверждает source-era rkt runtime.
- `rkt list` группирует containers по Pod.
- `rkt image list` показывает runtime images.
- CRI делает Kubelet/runtime boundary подключаемым.

## Next action

Для source-era эксперимента:
1. запустить Minikube с rkt + CNI;
2. создать workload;
3. проверить `kubectl describe pods`;
4. войти в Minikube VM;
5. проверить `rkt list` и images.

## Modifying action

```bash
minikube start --container-runtime=rkt --network-plugin=cni
minikube delete
kubectl run kubia --image=luksa/kubia --port 8080
```

Source также упоминает Minikube parameter `--container-runtime=crio`.

## Verification / acceptance checks

```bash
kubectl describe pods
rkt list
```

Acceptance в source: workload Running, container/image IDs указывают на rkt.

## Rollback

`minikube delete` удаляет существующую Minikube VM; это destructive action.
Полный migration rollback к другой runtime source не описывает: **[Needs confirmation]**.
