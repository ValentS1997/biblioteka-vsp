# Шпаргалка: контейнеры и образы

Цель: быстро локализовать объект Docker, его состояние, storage layer или build stage по модели главы 2.

## 1. Image → Container

```text
immutable image layers
        ↓
thin read-write container layer
        ↓
running / paused / exited / ...
```

Image — read-only template filesystem. Container — динамический экземпляр image.

## 2. Lifecycle

| State | Смысл |
|---|---|
| Created | создан, но не запущен |
| Running | выполняется; отображается как Up |
| Paused | выполнение приостановлено |
| Exited | процесс container завершился |
| Restarting | идёт перезапуск |
| Dead | удаление завершилось некорректно/частично |
| Stopped | остановлен |

```text
create → Created
run → Running
Running → pause → Paused
Paused → unpause → Running
Running → stop → Exited
process exits → Exited
```

## 3. Read-only checks

```bash
docker --version
docker -v
docker ps
docker ps --all
docker container ls -a
docker container inspect <container>
docker inspect <container>
```

Inspect выдаёт JSON с State, image, PID, ExitCode, storage/network fields и служебными путями.

Logging driver:

```bash
docker info --format '{{.LoggingDriver}}'
```

Logs:

```bash
docker logs <container>
docker logs <container> --follow
docker logs <container> --details
docker logs <container> --tail 8
docker logs <container> -t
docker logs <container> -t --tail 10
docker logs <container> | grep -i error
```

Images:

```bash
docker info
docker image ls
docker image ls --all
docker image ls --digests
docker image history <image-id>
docker image inspect <image-id>
```

## 4. State-changing actions

Run:

```bash
docker run --name my_first_container busybox:latest
docker run -dit --name alpine alpine:latest
```

`-d` = detach, `-i` = interactive, `-t` = TTY.

Pause/unpause/stop:

```bash
docker container pause my_container
docker container unpause my_container
docker container stop my_container
```

Create without start:

```bash
docker container create --name my_container2 alpine:latest
```

Expected state: `Created`.

Exec:

```bash
docker exec -it test_cont sh
```

Дальнейший effect зависит от команд внутри container.

## 5. Logs

```text
container stdout / stderr
          ↓
logging driver
          ↓
json-file
          ↓
/var/lib/docker/containers/<container-id>/<container-id>-json.log
```

Для больших сред книга рекомендует централизованный aggregator/data pipeline.

## 6. Runtime stack

```text
Docker CLI
   ↓
REST API
   ↓
dockerd
   ↓
containerd
   ↓
runC
   ↓
namespaces / cgroups / Linux security
```

## 7. Image layers и COW

- image layers immutable;
- container добавляет upper read-write layer;
- изменяемый файл копируется в writable layer;
- механизм называется Copy-On-Write;
- digest layer вычисляется SHA-256;
- configuration object содержит упорядоченный список digest-значений.

## 8. Хранение image

Источник указывает:

```text
/var/lib/docker/<storage-driver>
```

Пример для `overlay2`:

```text
/var/lib/docker/overlay2
```

## 9. Save / commit

```bash
docker image save <image-id> > mynginx.tar
docker save --output mynginx.tar nginx
docker commit ubuntu myubuntu
```

Verification:

```bash
docker images
```

## 10. Dockerfile

| Instruction | Роль |
|---|---|
| `FROM` | base image / новый stage |
| `LABEL` | metadata |
| `ENV` | environment variables |
| `RUN` | build-time command; создаёт layer |
| `CMD` | default command/args |
| `ENTRYPOINT` | entry point |
| `ADD` | copy/download content |
| `EXPOSE` | сообщает port; не публикует его |
| `WORKDIR` | working directory |
| `USER` | UID/GID |
| `VOLUME` | mount point |

Build:

```bash
docker build --tag myubuntu_image .
```

## 11. Cache и size

Docker читает Dockerfile сверху вниз и ищет подходящий intermediate result в cache.

```text
RUN create 100 MB file
RUN delete file
→ предыдущий immutable layer остаётся

RUN create 100 MB file && delete file
→ временные данные не закрепляются отдельным layer
```

Multi-stage build использует несколько `FROM`, чтобы переносить в final image только нужные artifacts.

## Acceptance

Нужно уметь объяснить:

- image vs container;
- writable layer + COW;
- lifecycle states;
- inspect/logs;
- dockerd/containerd/runC;
- digest/configuration object;
- Dockerfile layer semantics;
- build cache/intermediate images;
- влияние layer boundaries на size.
