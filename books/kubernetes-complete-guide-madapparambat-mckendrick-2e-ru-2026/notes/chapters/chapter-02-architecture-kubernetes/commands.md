# Команды главы 2 — RAG-verified inventory

**Source only:** PDF 71–114; никаких команд из внешней документации и памяти модели. Использование в реальной среде требует контроля версии, прав, namespace и контекста: **[Needs confirmation]**.

## Read-only / observation

| Команда из книги | Воздействие | Provenance |
|---|---|---|
| `echo $PATH` | read-only, печать PATH | p0097:c01 |
| `kubectl version` | read-only; также пытается обратиться к серверу | p0097:c01 |
| `kubectl config view` | read-only; может содержать конфигурационные/аутентификационные сведения — не публиковать без проверки | p0102:c01 |
| `kubectl get pods` | read-only, список Pod в контексте клиента (конкретная область видимости в главе не уточнена) | p0103:c01 |
| `kubectl get rs -n my-namespace` | read-only, ReplicaSet заданного namespace | p0104:c01 |
| `kubectl explain pod.spec.containers.image` | read-only, справка API-поля | p0107:c01 |

## Workload-generating / state-changing

```bash
kubectl run nginx --restart Never --image nginx
kubectl run my-pod --restart Never --image busybox:latest
kubectl run my-pod --restart=Never --image busybox:latest
kubectl create -f pod.yaml
kubectl delete pods my-pod
```

- `kubectl run` — создает Pod с образом (p0085, p0103–p0105). `--restart Never` и `--restart=Never` представлены источником в двух формах; **не нормализовать источник без проверки**.
- `kubectl create -f pod.yaml` — создает объекты из YAML (p0106), сам `pod.yaml` приведен в книге как Pod с `apiVersion`, `kind`, `metadata`, `spec`.
- `kubectl delete pods my-pod` — удаляет Pod, авторы указывают пространство имен default (p0104); **проверьте target, context и namespace до изменений**.
- **Риск:** удаление существующего ресурса, изменение состояния, нагрузки или доступности кластера.
- **Verification:** книга приводит `kubectl get pods`; адекватные критерии готовности приложения/rollback **[Needs confirmation]**.
- **Rollback:** [Needs confirmation] — безопасного детального восстановления исходник не предоставляет.

## Установка kubectl: изменяет локальную систему

Буквальная логика Linux-примера (p0097), где в исходнике приведены команды загрузки, разрешения на исполнение, перемещения файла и проверки версии:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version
```

| Команда | Класс | Эффект / риск / проверка / rollback |
|---|---|---|
| `curl -LO ...` | state-changing local | Скачивает бинарник в рабочий каталог; версия, целостность, источник и система — [Needs confirmation]; откат — [Needs confirmation] |
| `chmod +x ./kubectl` | state-changing local | Меняет права исполнения; доверенность файла не подтверждена; откат — [Needs confirmation] |
| `sudo mv ./kubectl /usr/local/bin/kubectl` | state-changing local | Устанавливает или заменяет двоичный файл; риск перезаписи; версию можно наблюдать `kubectl version`; откат — [Needs confirmation] |
| `curl -LO https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl` | state-changing local | Фиксированная версия из примера, а не совет брать эту версию сейчас; rollback — [Needs confirmation] |
| `curl.exe -LO https://dl.k8s.io/release/v1.30.0/bin/windows/amd64/kubectl.exe` | state-changing local | Пример Windows-загрузки, p0098; установка в PATH вручную — [Needs confirmation] |

macOS-примеры p0098 показывают разные двоичные файлы для Intel `darwin/amd64` и Apple Silicon `darwin/arm64`; далее `chmod +x`, `sudo mv` и `sudo chown root: /usr/local/bin/kubectl`. **До выполнения проверить архитектуру и существующую установку: [Needs confirmation].**

Официальные репозитории `apt.kubernetes.io` / `yum.kubernetes.io` описаны как устаревшие, `pkgs.k8s.io` — как замена (p0097). Эти положения **приведены по книге; внешне не проверены на текущую дату**.

## Автодополнение Bash: изменяет хост / профиль

```bash
sudo yum install bash-completion
sudo apt install bash-completion
echo 'source <(kubectl completion bash)' >> ~/.bashrc
```

- `yum` и `apt` — взаимоисключающие альтернативы для разных дистрибутивов (p0104); **не запускать обе**.
- `echo ... >> ~/.bashrc` — дописывает строку в конфигурацию Bash и будет повторно дописывать при повторном выполнении; проверить содержимое до изменения. Точный безопасный rollback не приведен: **[Needs confirmation]**.
- `kubectl completion bash` — встраиваемая в конфиг генерация кода автодополнения; проверка авторов: запуск новой оболочки и Tab, без формальных критериев.

## KUBECONFIG: изменение окружения процесса

```bash
export KUBECONFIG="/custom/path/.kube/config"
```

Это изменяет выбор конфигурации клиента **для текущего окружения и дочерних процессов**, не состояние кластера; p0102. Источник приводит форму `kubectl --kubeconfig="/custom/path/.kube/config"` **без завершающего subcommand** — не считать ее самостоятельной исполняемой операцией. Проверка через `kubectl config view` с учетом чувствительных сведений; rollback **[Needs confirmation]**.

## Декларативный пример (p0105–p0106)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: busybox-container
      image: busybox:latest
```

В главе создается как `kubectl create -f pod.yaml`, **не `apply`**. Второй YAML-документ в том же файле отделяется `---` и определяет Pod `my-second-pod` с образом `nginx:latest` (p0106). Используемые `latest`-теги не закрепляют конкретную сборку; это **примеры книги**, не проверенные deploy-артефакты.

## Упомянутые средства без полной команды

`minikube`, `kind`, `kubeadm`, `ctr`, `crictl`, `curl` как HTTP-клиент и `systemd` описаны, но на страницах главы 2 нет полной проверенной процедуры управления кластером/его восстановления. Нельзя дописывать команды из памяти.

## Safety / source findings

Реальные имена кластеров, секреты `kubeconfig` и содержимое `etcd` в артефакты не попадают. Спорные точные значения polling и путей отмечены в [source-findings.md](source-findings.md).
