# Команды главы 2

Команды ниже основаны только на RAG главы 2. OCR-искажения пробелов и латинских символов нормализованы только там, где команда однозначно восстанавливается из соседнего текста.

## Read-only / observation

| Команда | Что проверяет | Effect / risk | Acceptance |
|---|---|---|---|
| `docker --version` / `docker -v` | Наличие/версию Docker CLI | read-only | version string или ошибка отсутствия команды |
| `docker ps` | Running containers | read-only | таблица containers со status |
| `docker ps --all` | Все containers | read-only | видны Created/Exited/Paused и др. |
| `docker container ls -a` | То же через object syntax | read-only | список всех containers |
| `docker container inspect <container>` | Детальный JSON container | read-only | State, image, PID, ExitCode, storage/network fields |
| `docker inspect <container>` | Сокращённый inspect | read-only | JSON object |
| `docker info --format '{{.LoggingDriver}}'` | Default logging driver | read-only | в примере `json-file` |
| `docker logs <container>` | Container logs | read-only | stdout/stderr records |
| `docker logs <container> --follow` | Новые log records | read-only, long-running | поток новых записей |
| `docker logs <container> --details` | Дополнительные log details | read-only | details при наличии |
| `docker logs <container> --tail 8` | Последние N строк | read-only | последние 8 записей |
| `docker logs <container> -t` | Logs с timestamp | read-only | timestamps |
| `docker logs <container> -t --tail 10` | Последние 10 с timestamp | read-only | bounded output |
| `docker logs <container> \| grep -i error` | Фильтрация logs | read-only | строки с error |
| `docker info` | В т.ч. storage driver | read-only | storage driver в info |
| `docker image ls` | Локальные images | read-only | image list |
| `docker image ls --all` | Все local images | read-only | полный список |
| `docker image ls --digests` | Images + digest | read-only | digest column |
| `docker image history <image-id>` | Layer/build history | read-only | history rows |
| `docker image inspect <image-id>` | JSON image metadata | read-only | image configuration/rootfs |
| `docker image inspect <image-id> \| jq '.[0].RootFS'` | RootFS/layer digests | read-only | Layers array |
| `ls -ltr`, `ls -sh <file>`, `cat <file>` | Files/size/log content в примерах | read-only | filesystem output |

## Container lifecycle

### Run

```bash
docker run --name my_first_container busybox:latest
docker run -dit --name alpine alpine:latest
docker run -dit --name my_container busybox:latest
```

Effect: создаёт и запускает container; если image отсутствует локально, Docker извлекает его из registry.

Verification:

```bash
docker ps
docker ps --all
```

Rollback по модели главы: остановить container. Удаление container отдельной процедурой в этой границе не описано: `[Needs confirmation]`.

### Pause / unpause

```bash
docker container pause my_container
docker container unpause my_container
```

Effect: приостанавливает/возобновляет выполнение.

Verification:

```bash
docker ps
docker container ls -a
```

Rollback: `pause` ↔ `unpause`.

### Stop

```bash
docker container stop my_container
```

Effect: останавливает running container; в примере state становится Exited.

Verification:

```bash
docker ps --all
```

Rollback: текст говорит, что Exited container можно перезапустить вручную, но точная команда `start` в главе не приведена: `[Needs confirmation]`.

### Create without start

```bash
docker container create --name my_container2 alpine:latest
```

Effect: создаёт object container без запуска.

Verification:

```bash
docker ps --all
```

Expected: `Created`.

## Exec / commands inside container

```bash
docker run -dit --name test_cont busybox:latest
docker exec -it test_cont sh
```

Внутри container источник использует:

```bash
ps
ls
mkdir test
cd test
touch myfile
```

- `ps`, `ls`: observation.
- `mkdir`, `touch`: изменяют writable layer container.
- rollback для примера не описан: `[Needs confirmation]`.

## Logging workload

```bash
docker run --name test_logs -dit alpine:latest sh -c "while true; do $(echo time) sleep 10; done"
```

Effect: создаёт long-running container, генерирующий вывод примерно каждые 10 секунд.

Verification:

```bash
docker ps
docker logs <container>
```

Локальное расположение `json-file` logs по модели главы:

```text
/var/lib/docker/containers/<container-id>/<container-id>-json.log
```

Изменение default logging driver через `/etc/docker/daemon.json` и restart daemon упоминается, но готовая процедура/rollback в главе не дана: `[Needs confirmation]`.

## Image pull / inspect / history

```bash
docker image pull ubuntu:latest
docker image ls --digests
docker image history <image-id>
docker image inspect <image-id>
```

`pull` — state-changing: добавляет/обновляет local image content.

Verification: `docker image ls --digests`.

Rollback: `docker image rm <image-id>` упоминается далее для очистки local image.

## Host filesystem paths

Источник показывает:

```bash
cd /var/lib/docker/overlay2
ls -ltr
```

При использовании только `cd`/`ls` это read-only. Ручное изменение содержимого этого каталога в главе не предлагается.

## Save image as tar

```bash
docker image save <image-id> > mynginx.tar
docker save --output mynginx.tar nginx
```

Effect: создаёт tar-файл на host.

Verification:

```bash
ls -ltr
ls -sh mynginx.tar
```

Rollback: удалить созданный tar-файл обычными средствами; конкретная команда удаления в этом разделе источника не приведена.

## Commit container to image

Внутри Ubuntu-container источник устанавливает пакет:

```bash
apt update && apt install iputils-ping -y
```

Затем на host:

```bash
docker commit ubuntu myubuntu
docker images
```

Effect:
- package install меняет writable layer container;
- `docker commit` создаёт новый local image.

Verification: `docker images`.

Rollback: удалить созданный image через `docker image rm <image-id>`; rollback изменения container отдельно не описан.

## jq installation

```bash
apt install jq
```

Effect: изменяет package state host.

Verification и rollback в источнике не заданы: `[Needs confirmation]`.

## Dockerfile build

Пример источника:

```Dockerfile
FROM ubuntu:latest
ENV HOME /root
LABEL ubuntu=myubuntu
ENTRYPOINT ["sleep"]
CMD ["50"]
RUN useradd -m -G root testuser
USER root
RUN apt-get update && apt-get install net-tools -y
RUN apt-get install iputils-ping -y
```

Build:

```bash
docker build --tag myubuntu_image .
```

Effect: создаёт image и intermediate/cache artifacts.

Verification:

```bash
docker images
docker image ls --digests
```

Rollback:

```bash
docker image rm <image-id>
```

## Layer-size experiment

Вариант 1 — создание и удаление в разных layers:

```Dockerfile
FROM ubuntu:latest
RUN truncate -s 100M mytext.txt
RUN rm -rf mytext.txt
```

Вариант 2 — в одном layer:

```Dockerfile
FROM ubuntu:latest
RUN truncate -s 100M mytext.txt && rm -rf mytext.txt
```

Build:

```bash
docker build -t test_size .
docker build -t test_size1 .
docker images
```

Interpretation источника: второй вариант не сохраняет отдельный 100-MB layer, тогда как удаление в следующем layer не отменяет размер предыдущего immutable layer.
