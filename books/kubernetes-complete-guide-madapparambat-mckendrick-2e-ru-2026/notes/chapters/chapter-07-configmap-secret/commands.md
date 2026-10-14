# Commands — глава 7. ConfigMap и Secret

**Source:** RAG PDF 248–280. Команды классифицированы; никакая не выполнялась. Все имена из книжного сценария. При использовании `-n` и текущего контекста реальные значения [Needs confirmation]. **Любые реальные секретные значения в файлах, CLI, выводе и логах запрещено коммитить.** Демонстрационные значения из книги в примерах ниже обозначены placeholders.

## Read-only / observation

| Команда из RAG | Наблюдение и риск | PDF |
|---|---|---:|
| `kubectl get configmaps`, `kubectl get cm` | список ConfigMap | 254–255 |
| `kubectl get configmaps -A` | все namespaces | 254 |
| `kubectl get cm my-sixth-configmap` | DATA count | 258 |
| `kubectl get configmap/my-seventh-configmap` | DATA count | 259 |
| `kubectl get cm my-eight-configmap` | DATA count | 259 |
| `kubectl get cm my-fourth-configmap -o yaml` | весь ConfigMap: не публиковать | 256 |
| `kubectl describe cm my-fourth-configmap` | включает значения ConfigMap | 260–261 |
| `kubectl get pod` | Pod READY/status | 262, 267 |
| `kubectl describe pod flask-pod-with-configmap-volume` | события `FailedMount` | 267 |
| `kubectl get secret -A`, `kubectl get secrets` | наличие/тип/количество Secret | 270 |
| `kubectl get secret my-first-secret -o yaml` | Base64, может раскрыть конфиденциальное | 270 |
| `kubectl get secret my-second-secret -o yaml` | Base64, **sensitive** | 272, 274 |
| `kubectl get secret my-secret-stringdata -o yaml` | Base64, **sensitive** | 272 |
| `kubectl describe secret/mypassword` | размер/имя, не plaintext в примере | 274 |

Осторожно: `kubectl exec ... -- env` и `-- cat /etc/password-mounted-path/...` формально читают контейнер, **но раскрывают значения**. В исходной книге это диагностические примеры; в реальной среде вывод секретов в терминал или CI нельзя считать безопасным.

## ConfigMap creation — state-changing cluster

```bash
kubectl create configmap my-first-configmap
kubectl apply -f my-second-configmap.yaml
kubectl create cm my-third-configmap --from-literal=color=blue
kubectl create cm my-fourth-configmap \
    --from-literal=color=blue \
    --from-literal=version=1 \
    --from-literal=environment=prod
kubectl apply -f my-fifth-configmap.yaml
kubectl create cm my-sixth-configmap \
    --from-literal=color=yellow \
    --from-file=$HOME/configfile.txt
kubectl apply -f my-seventh-configmap.yaml
kubectl create cm my-eight-configmap --from-env-file=my-env-file.env
```

Provenance p0254–p0259. **Effect:** создаёт ConfigMap с нулём, одним или несколькими ключами; разные объекты в namespace. **Risk:** случайное использование паролей в ConfigMap, выбор неправильного namespace, конфликты имён. **Verification:** `get cm`, `get cm ... -o yaml` или `describe cm` (последние могут раскрывать содержимое). **Rollback:** удаление уничтожает данные, поэтому возможное восстановление только при наличии сохранённого не-чувствительного источника, прочее [Needs confirmation].

Создание локального файла перед `--from-file` (p0258), **state-changing local**, повторный запуск дописывает строку:
```bash
echo "I'm just a dummy config file" >> $HOME/configfile.txt
```

Файл `my-env-file.env` (p0259), демонстрационные несекретные данные:
```dotenv
hello=world
color=blue
release=1.0
production=true
```

YAML ConfigMap из p0257:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-fifth-configmap
data:
  color: "blue"
  version: "1"
  environment: "prod"
```

## ConfigMap in Pod — workload-generating

```yaml
# flask-pod-with-configmap.yaml (p0262)
apiVersion: v1
kind: Pod
metadata:
  name: flask-pod-with-configmap
  labels:
    app: my-flask-app
spec:
  containers:
    - name: flask-with-configmap
      image: quay.io/iamgini/my-flask-app:1.0
      env:
        - name: COLOR
          valueFrom:
            configMapKeyRef:
              name: my-third-configmap
              key: color
```

```bash
kubectl apply -f flask-pod-with-configmap.yaml
kubectl exec pod/flask-pod-with-configmap -- env
kubectl expose pod flask-pod-with-configmap --port=8081 --target-port=5000 --type=NodePort
kubectl port-forward flask-pod-with-configmap 20000:5000
```

p0262–p0263. `apply`: **создание Pod**; `exec -- env`: read-only по фактическому исполнению, но может раскрывать env; `expose`: **создание Service NodePort**, увеличивает поверхность доступа; `port-forward`: **локальное подключение**, останавливается Ctrl+C. Verification: Pod Running, `COLOR=blue` у книжного Flask, страница по `http://127.0.0.1:20000`. Полный rollback объекта Pod/Service исходником здесь не описан: **[Needs confirmation]**.

Все значения ConfigMap (p0264):
```yaml
envFrom:
  - configMapRef:
      name: my-fourth-configmap
```
Полный пример называется `flask-pod-with-configmap-all.yaml`, вызывается `kubectl apply -f flask-pod-with-configmap-all.yaml`. Риск наследования всех ключей и конфликтов имён env.

ConfigMap как том (p0265):
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: flask-pod-with-configmap-volume
spec:
  containers:
    - name: flask-with-configmap-volume
      image: quay.io/iamgini/my-flask-app:1.0
      volumeMounts:
        - name: configuration-volume
          mountPath: /etc/conf
  volumes:
    - name: configuration-volume
      configMap:
        name: my-sixth-configmap
```

```bash
kubectl apply -f flask-pod-with-configmap-volume.yaml
kubectl exec pod/flask-pod-with-configmap-volume -- ls /etc/conf
kubectl exec pod/flask-pod-with-configmap-volume -- cat /etc/conf/color
kubectl exec pod/flask-pod-with-configmap-volume -- cat /etc/conf/configfile.txt
```

**Effect:** Pod с конфигурационными файлами; **verification:** `color`, `configfile.txt` в каталоге. После удаления указанного ConfigMap следующий Pod может получить `FailedMount`, см. p0267. **Rollback:** [Needs confirmation].

## ConfigMap deletion and update — state-changing

```bash
kubectl delete cm my-first-configmap
kubectl delete cm my-sixth-configmap
```

p0266. **Risk:** Pod с отсутствующей зависимостью может остаться в `ContainerCreating` с `FailedMount` (p0267); конфигурация удаляется. Для обновления источник на p0267 описывает `kubectl apply` обновлённого YAML и `kubectl edit` существующего объекта, **не давая полного отдельного CLI**. Immutable `ConfigMap` (p0268):
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: immutable-configmap
data:
  color: "blue"
  version: "1.0"
  environment: "prod"
immutable: true
```
**Effect:** менять data этого объекта нельзя, для замены по книге требуется удаление/пересоздание, а также пересоздание зависимых Pod. **Rollback:** [Needs confirmation].

## Secret — creation and data representation

Источник p0270–p0273 использует демонстрационное парольное значение. Следующие фрагменты намеренно **с placeholders**, а не исполняемые команды с настоящими паролями:

```bash
kubectl create secret generic my-first-secret --from-literal='db_password=<DEMO_VALUE>'
kubectl apply -f secret-from-file.yaml
kubectl apply -f secret-from-file-stringData.yaml
kubectl apply -f secret-from-file-database.yaml
kubectl create secret generic mypassword --from-file=./password.txt
```

- `--from-literal` может попасть в историю оболочки и журналы процесса. **Не применять с реальными значениями** (p0270).
- `data` хранит Base64: книжный `secret-from-file.yaml` с `kind: Secret`, `type: Opaque`, `metadata.name: my-second-secret`. Демонстрационная строка Base64 здесь не воспроизводится.
- `stringData` принимает **незакодированный** текст в YAML, `metadata.name: my-secret-stringdata` (p0272). Такой манифест сам по себе чувствителен! Не коммитить его с plaintext.
- `secret-from-file-database.yaml` демонстрирует два текстовых поля `db_user`, `db_password`, которые в source заполнены учебными значениями (p0276); здесь значения не воспроизводятся.
- Создание `password.txt` источником производится через shell `echo -n ... > ./password.txt` (p0273) — **state-changing local** и риск plaintext на диске; не воспроизводить с секретом.
- Проверка создания: `kubectl get secrets`/ `describe secret/mypassword`; **не** проверять через печать секретного значения.
- Откат секретных побочных эффектов, безопасная ротация, защита файлов и централизованное шифрование **[Needs confirmation]**.

## Secret — wiring Pod and exposure caveats

Single env from p0275–p0276:
```yaml
env:
  - name: PASSWORD_ENV_VAR
    valueFrom:
      secretKeyRef:
        name: my-first-secret
        key: db_password
```

Под `flask-pod-with-secret.yaml`, команда `kubectl apply -f flask-pod-with-secret.yaml`; затем книга показывает `kubectl exec pod/flask-pod-with-secret -- env`. **Risk:** plaintext в выводе. В notes не приводится демонстрационный пароль.

All env (p0277):
```yaml
envFrom:
  - secretRef:
      name: appdb-secret
```
`kubectl apply -f flask-pod-with-secret-all.yaml`. Источник показывает `kubectl exec pod/flask-pod-with-secret-all -- env | grep -i app` — чтение **секретного plaintext**, **не выполнять как безопасную production-проверку**.

Volume from p0277–p0278:
```yaml
volumeMounts:
  - name: mysecret-volume
    mountPath: /etc/password-mounted-path
    readOnly: true
volumes:
  - name: mysecret-volume
    secret:
      secretName: my-second-secret
```
`kubectl apply -f flask-pod-with-secret-volume.yaml`. В RAG предшествующий текст указывает **другой путь** `/etc/passwords-mounted-path`; YAML использует `/etc/password-mounted-path`. `kubectl exec ... -- cat /etc/password-mounted-path/db_password` в книге **раскрывает plaintext**. Путь при проверке следует брать из фактического манифеста, расхождение отмечено в findings.

`kubectl delete secret my-first-secret` (p0278) — **state-changing destructive**: удаление конфиденциальной зависимости. `kubectl apply` изменённого YAML и `kubectl edit` как методы обновления упомянуты p0279, без полной safe-ротации. Verification: read-only metadata и состояние Pod без распечатывания значений. Rollback: **[Needs confirmation]**.

## Security boundary

RAG прямо предупреждает: **Base64 обратим** (p0269, p0274–p0275). Безопасность требует RBAC, encryption at rest/KMS, audit, rotation и/или внешнего хранилища. Снятие копии YAML, `cat`, `env`, CI-логи могут раскрыть данные. Без разрешений и конкретной среды никакие modifying-команды запускать нельзя.
