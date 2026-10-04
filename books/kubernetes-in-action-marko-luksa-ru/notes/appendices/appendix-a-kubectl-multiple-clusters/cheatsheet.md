# Приложение A — cheatsheet

## Symptom / problem framing

Нужно безопасно переключаться между несколькими Kubernetes clusters и namespaces, не передавая каждый раз вручную `--server`, credentials и `--namespace`.

## Baseline / context

```text
cluster entry   user entry
      \          /
       \        /
        context
           ↓
    current-context
           ↓
        kubectl
```

## Read-only checks

```bash
kubectl config current-context
kubectl config get-contexts
kubectl config get-clusters
```

## Interpretation

- `cluster` хранит endpoint API server и CA information.
- `user` хранит authentication data.
- `context` связывает cluster, user и default namespace.
- `current-context` определяет, какой context kubectl использует по умолчанию.
- `KUBECONFIG` может указывать на иной файл или несколько файлов, разделенных двоеточием.

## Next action

Перед работой с другим кластером:
1. проверить `current-context`;
2. проверить target context в `get-contexts`;
3. переключить context;
4. повторно проверить `current-context`.

## Modifying action

```bash
kubectl config set-cluster my-other-cluster --server=https://k8s.example.com:6443 --certificate-authority=path/to/the/cafile
kubectl config set-credentials foo --username=foo --password=<PASSWORD>
kubectl config set-credentials foo --token=<TOKEN>
kubectl config set-context some-context --cluster=my-other-cluster --user=foo --namespace=bar
kubectl config set-context minikube --namespace=another-namespace
kubectl config use-context my-other-context
kubectl config delete-context my-unused-context
kubectl config delete-cluster my-old-cluster
```

Credentials заменены placeholders.

## Verification / acceptance checks

После переключения:
```bash
kubectl config current-context
```

Ожидаемо: имя target context.

После изменения namespace:
```bash
kubectl config get-contexts
```

Ожидаемо: нужный namespace в target context.

## Rollback

- Для переключения context: выполнить `kubectl config use-context <previous-context>`.
- Для удаления/перезаписи cluster/context source не дает автоматического rollback: **[Needs confirmation]**.
