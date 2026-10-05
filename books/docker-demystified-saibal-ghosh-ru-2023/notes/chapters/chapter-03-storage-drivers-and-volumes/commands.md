# Команды главы 3

Команды основаны только на RAG главы 3. OCR-нормализация применена только к очевидным и подтверждённым формам.

## Read-only checks

| Команда | Что проверяет | Риск | Acceptance |
|---|---|---|---|
| `lsmod \| grep overlay` | Наличие OverlayFS kernel module | read-only | строка `overlay` |
| `docker info \| grep Storage` | Current storage driver | read-only | например `Storage Driver: overlay2` |
| `docker image pull redis` | Загружает image для примера Overlay2 | state-changing local cache | image pull completes |
| `ls -ltr /var/lib/docker/overlay2` | Структура Overlay2 directories | read-only | layer directories + `l` |
| `cat link` | Short layer link identifier | read-only | identifier |
| `docker container ls -a` | Containers/status | read-only | container list |
| `docker inspect -f '{{ json .Mounts }}' <container>` | Mount mappings | read-only | Type/Source/Destination/RW |
| `docker volume inspect myvolume` | Named volume metadata | read-only | Mountpoint/Driver/Scope |
| `ls -ltr` / `cat <file>` | Persistence verification | read-only | expected file/data |

## Storage driver switch: modifying / disruptive

Источник демонстрирует смену `overlay2` на `overlay`.

### 1. Stop Docker

```bash
systemctl stop docker
```

Effect: останавливает Docker daemon и container workloads.

Verification: в главе отдельная команда проверки daemon state не дана: `[Needs confirmation]`.

### 2. Backup Docker data

```bash
cp -au /var/lib/docker /var/docker.bkp
```

Effect: создаёт backup copy Docker data root.

Acceptance: наличие backup-каталога; отдельная checksum-проверка в источнике не приведена.

### 3. Change daemon config

В `/etc/docker/daemon.json`:

```json
{
  "storage-driver": "overlay"
}
```

Effect: меняет storage backend, используемый Docker после restart.

### 4. Start Docker

```bash
systemctl start docker
```

### 5. Verify

```bash
docker info | grep Storage
```

Expected по примеру: `Storage Driver: overlay`.

### Rollback

Источник говорит, что аналогично можно вернуться к `overlay2`. Минимальная логика rollback:

- остановить Docker;
- вернуть `"storage-driver": "overlay2"`;
- запустить Docker;
- проверить через `docker info | grep Storage`.

Полная процедура восстановления `/var/lib/docker` из backup в главе не описана: `[Needs confirmation]`.

## Overlay2 inspection

После pull Redis:

```bash
docker image pull redis
cd /var/lib/docker/overlay2
ls -ltr
cd l
ls -ltr
```

Далее источник исследует конкретный layer directory:

```bash
ls -ltr <layer-directory>
cd <layer-directory>
ls -ltr
cat link
cd diff
ls
```

Это read-only, если не изменять содержимое `/var/lib/docker/overlay2`.

## Bind mount

### Host preparation

```bash
mkdir -p /root/testing
```

Effect: создаёт host directory.

### Run container

```bash
docker run -it --name myalpine -v /root/testing/:/test1 alpine:latest
```

Effect: создаёт container и bind-mounts host directory.

Inside container source creates a file in `/test1`.

Verification on host:

```bash
cd /root/testing
ls -ltr
cat myfile
```

Inspect mapping:

```bash
docker container ls -a
docker inspect -f '{{ json .Mounts }}' <container-id>
```

Expected:

- Type = `bind`;
- Source = `/root/testing`;
- Destination = `/test1`.

### Container deletion test

```bash
docker container rm myalpine -f
```

Risk: force-removes container.

Verification:

```bash
cd /root/testing
ls -ltr
cat myfile
```

Acceptance: host file remains after container removal.

Rollback: deleted container object itself is not restored by any command in this chapter. Data persists because it was outside the container.

## Anonymous volume

Create:

```bash
docker run -dit --name test_vol --volume /myapp alpine:latest
```

Inspect:

```bash
docker container ls -a
docker inspect -f '{{ json .Mounts }}' <container-id> | jq
```

Expected: Type = `volume` and Source under `/var/lib/docker/volumes/.../_data`.

Inside container:

```bash
docker exec -it test_vol sh
```

Source then creates data under `/myapp` and verifies the same data directly under Docker volume path on host.

Container removal:

```bash
docker container rm <container-id> -f
```

Acceptance: data remains in the volume directory after container removal.

## Install jq

```bash
apt update && apt install jq -y
```

Effect: modifies host package state.

Source note: skip if jq is already installed.

Verification/rollback not provided: `[Needs confirmation]`.

## Named volume

Create:

```bash
docker volume create myvolume
```

Verify:

```bash
docker volume inspect myvolume
```

Attach:

```bash
docker container run -dit --name mycentos --volume myvolume:/test centos:latest
```

Effect: creates container and mounts named volume at `/test`.

Rollback/removal of the volume is not described in the chapter: `[Needs confirmation]`.

## --mount volume syntax

```bash
docker run -dit --name mynginx --mount source=myvol2,target=/test nginx:latest
docker ps
docker inspect -f '{{ json .Mounts }}' <container-id> | jq
```

Effect: creates/uses volume `myvol2` and mounts it into container.

Verification: inspect Mounts.

## tmpfs

```bash
docker run -it --name test_tmpfs --mount type=tmpfs,destination=/testing centos:latest
```

Effect: creates temporary mount in host memory.

Acceptance: `/testing` exists in container while it runs.

Persistence boundary: when container stops, tmpfs disappears and files become unavailable.

## Safety boundary

Do not treat direct inspection of `/var/lib/docker/overlay2` or `/var/lib/docker/volumes` as permission to edit those directories manually. The chapter uses them for inspection and demonstration; direct mutation is not part of its workflow.
