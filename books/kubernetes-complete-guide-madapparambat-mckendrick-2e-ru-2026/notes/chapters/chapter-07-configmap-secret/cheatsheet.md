# Cheatsheet — Глава 7. ConfigMap и Secret

**Provenance:** RAG-only, PDF 248–280; `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0248:c01` … `…:p0280:c01`.

## Symptom / problem framing

Один образ контейнера нужен для dev/test/prod, но параметры (адрес БД, оформление, пароль) различаются. Вшивать конфигурацию в образ — означает собирать его заново при изменении среды. Решение авторов: `ConfigMap` для открытых параметров и `Secret` для чувствительных; Pod получает значения через `env`, `envFrom` или том (p0248–p0253).

## Baseline / context

- Доступный Kubernetes-кластер и настроенный `kubectl` (p0248–p0249). Текущий namespace, контекст, RBAC и реальные настройки хранения данных **[Needs confirmation]**.
- **Сначала создаётся ConfigMap/Secret, затем Pod**, ссылающийся на него (p0251–p0252, p0276–p0278).
- **ConfigMap**: литералы `--from-literal`, файл `--from-file`, `--from-env-file`, YAML с полем `data` (p0254–p0260).
- **Secret**: императивный `create secret generic`; декларативные `data` (Base64) и `stringData` (открытый текст до отправки в API), импорт файла (p0270–p0273).
- **В контейнере:** `valueFrom.configMapKeyRef`, `envFrom.configMapRef`, `valueFrom.secretKeyRef`, `envFrom.secretRef`, `volumes[*].configMap`/`volumes[*].secret` и `volumeMounts` (p0262–p0265, p0275–p0278).
- **Base64 не является шифрованием.** Source p0269/p0274–p0275 советует RBAC, encryption/KMS, ротацию и внешние системы.
- **Namespace scope:** имя объекта конфигурации в ссылке Pod должно быть доступно в целевом namespace; реальные namespaces [Needs confirmation]. В книге примеры идут в default.

## Read-only checks

```bash
kubectl get configmaps
kubectl get cm
kubectl get configmaps -A
kubectl get cm my-fourth-configmap -o yaml
kubectl describe cm my-fourth-configmap
kubectl get pod
kubectl describe pod flask-pod-with-configmap-volume
kubectl get secrets
kubectl get secret -A
kubectl describe secret/mypassword
```

Команды встречаются p0254–p0256, p0260–p0261, p0267, p0270, p0274. **Вывод YAML ConfigMap/Secret и раскрываемых переменных не публиковать.** `get secret` может показывать доступные для декодирования значения; `describe secret` в книге показывает в основном имена/размеры, не раскрывая plaintext (p0274).

## Interpretation

- `DATA` у `get cm` показывает число элементов, а не их безопасность (p0255–p0256).
- `kubectl exec pod/flask-pod-with-configmap -- env` демонстрирует `COLOR=blue` от `configMapKeyRef` (p0262). Это **наблюдение**, но вывод окружения потенциально чувствителен.
- `envFrom` вносит все допустимые ключи как env; имена наследуются из ConfigMap/Secret (p0264, p0277).
- При mount ConfigMap каждая запись появляется файлом в `/etc/conf`; книга проверяет `ls`, `cat` (p0265).
- После удаления `my-sixth-configmap` воссозданный Pod останавливается на `ContainerCreating`, `describe` сообщает `FailedMount` и `configmap not found` (p0266–p0267).
- Секрет, закодированный Base64, можно декодировать; p0274–p0275 прямо предупреждают о доступности значений для пользователей, читающих объект.

## Next action

В разрешённой учебной среде: подтвердить context и namespace; создать несекретный ConfigMap; проверить ключи; связать Pod через `env` или том и проверить результат; отдельно проверить Secret без экспонирования значения. Для production — RBAC, шифрование в покое, ротация, аудит и контролируемое хранение манифестов (p0268–p0269).

## Modifying action

```bash
kubectl create cm my-third-configmap --from-literal=color=blue
kubectl apply -f flask-pod-with-configmap.yaml
kubectl apply -f flask-pod-with-configmap-volume.yaml
kubectl apply -f secret-from-file.yaml
kubectl apply -f flask-pod-with-secret-volume.yaml
```

Все команды **меняют Kubernetes** (p0256, p0262, p0265, p0271, p0278). Последние две предполагают подготовленный манифест с демонстрационными, а не рабочими секретами. Риски: раскрытие конфигурации/пароля, утрата зависимости при удалении, ошибки монтирования, произвольное содержимое внешнего образа. **Не запускать автоматически**.

`kubectl expose pod flask-pod-with-configmap --port=8081 --target-port=5000 --type=NodePort` **создаёт сетевой Service** (p0263). `kubectl port-forward flask-pod-with-configmap 20000:5000` открывает временный локальный порт, завершается Ctrl+C; не считать publish и tunnel одним и тем же.

## Verification / acceptance checks

- `kubectl get cm my-sixth-configmap`: количество ключей 2 (p0258).
- `kubectl exec pod/flask-pod-with-configmap-volume -- ls /etc/conf`: `color`, `configfile.txt` (p0265).
- `kubectl exec pod/flask-pod-with-configmap-volume -- cat /etc/conf/color`: в демонстрации `yellow` (p0265); не использовать для реальных секретов.
- `kubectl describe pod flask-pod-with-configmap-volume`: отсутствие события `FailedMount` при корректном ConfigMap (p0267).
- Для Secret: `kubectl describe secret/mypassword` подтверждает тип и размер; тест чтения реального значения в лог **не рекомендуется**. Книга p0278 проверяет через `cat`, но это потенциальное разглашение.

## Rollback

`kubectl delete cm my-first-configmap` и `kubectl delete cm my-sixth-configmap` (p0266) уничтожают конфигурационный объект; это **не безопасный откат** Pod, который от него зависит. `kubectl delete secret my-first-secret` (p0278) удаляет чувствительную зависимость; для реальных workloads восстановление [Needs confirmation]. Порядок восстановления секретов, re-create и ротация приложения в главе полностью не описаны. `immutable: true` делает содержимое ConfigMap неизменяемым; авторы рекомендуют пересоздание (p0268) — риск остановки Pod. `port-forward` прекращается Ctrl+C (p0263).

## Limits / source findings

Не переназначать автоматически несовпадающие пути тома Secret p0277–p0278. Текст p0271 содержит недоказанное обещание защиты при `stringData` — пароль там явно показан. Источник p0270 ошибочно описывает значение `DATA` как «хешированное», одновременно поясняя Base64. Все caveats вынесены в [source-findings.md](source-findings.md).
