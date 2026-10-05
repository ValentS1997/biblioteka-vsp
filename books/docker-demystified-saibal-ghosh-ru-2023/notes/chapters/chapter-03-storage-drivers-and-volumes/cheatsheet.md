# Шпаргалка: storage drivers и persistence

## 1. Сначала определить тип данных

```text
Небольшие / временные изменения
  → container writable layer
  → storage driver

Данные должны пережить container removal
  → volume или bind mount

Данные должны жить только в RAM
  → tmpfs
```

## 2. Storage drivers

Источник перечисляет:

| Driver | Контекст главы |
|---|---|
| `overlay2` | предпочтительный вариант |
| `overlay` | более старый вариант OverlayFS |
| `aufs` | старые Ubuntu-сценарии |
| `Device Mapper` | требует LVM-конфигурации |
| `btrfs` | требует btrfs backing filesystem |
| `zfs` | требует zfs backing filesystem |
| `vfs` | медленный, без Copy-On-Write |

## 3. Backing filesystem

```text
Docker data root
/var/lib/docker/
      ↓
backing filesystem
      ↓
storage driver compatibility
```

Из таблицы главы:

- overlay/overlay2 → XFS, ext4;
- XFS для overlay2: `ftype=1`;
- btrfs → btrfs;
- zfs → zfs;
- Device Mapper → direct-lvm;
- vfs → любая filesystem, но с низкой производительностью.

## 4. Read-only checks

OverlayFS kernel module:

```bash
lsmod | grep overlay
```

Current storage driver:

```bash
docker info | grep Storage
```

Inspect Docker-managed volume:

```bash
docker volume inspect myvolume
```

Inspect mount mapping:

```bash
docker inspect -f '{{ json .Mounts }}' <container>
```

С `jq`:

```bash
docker inspect -f '{{ json .Mounts }}' <container> | jq
```

## 5. Overlay2 mental model

```text
lowerdir
  ├─ lower image layers
  └─ immutable

upperdir
  └─ changed/new files

work
  └─ OverlayFS internal work area

merged
  └─ combined view
```

Ключ: upper layer хранит diff относительно lower layers.

## 6. Risky storage-driver change

Источник показывает переход `overlay2 → overlay`:

1. stop Docker;
2. backup `/var/lib/docker`;
3. edit/create `/etc/docker/daemon.json`;
4. start Docker;
5. verify driver.

```bash
systemctl stop docker
cp -au /var/lib/docker /var/docker.bkp
systemctl start docker
docker info | grep Storage
```

Изменение `daemon.json`:

```json
{
  "storage-driver": "overlay"
}
```

Risk: disruptive state change. До выполнения нужен backup и rollback point.

Rollback по логике источника: вернуть `storage-driver` на `overlay2` и снова запустить Docker. Подробная restore-процедура из backup в главе не описана: `[Needs confirmation]`.

## 7. Bind mount

Host path выбирается пользователем:

```text
/root/testing/   <── bind ──>   /test1 inside container
```

Create host directory:

```bash
mkdir -p /root/testing
```

Run:

```bash
docker run -it --name myalpine -v /root/testing/:/test1 alpine:latest
```

Verification:

```bash
docker inspect -f '{{ json .Mounts }}' <container>
```

Expected mount type: `bind`.

Persistence check источника: файл, созданный внутри `/test1`, остаётся в `/root/testing` после удаления container.

## 8. Anonymous volume

```bash
docker run -dit --name test_vol --volume /myapp alpine:latest
```

Docker сам выбирает source path в `/var/lib/docker/volumes/.../_data`.

Verification:

```bash
docker inspect -f '{{ json .Mounts }}' <container> | jq
```

Expected type: `volume`.

## 9. Named volume

Create:

```bash
docker volume create myvolume
```

Inspect:

```bash
docker volume inspect myvolume
```

Attach:

```bash
docker container run -dit --name mycentos --volume myvolume:/test centos:latest
```

Источник подчёркивает: один named volume можно подключать к нескольким containers, если им нужны общие данные.

## 10. --mount

Источник рекомендует более явный синтаксис:

```bash
docker run -dit --name mynginx --mount source=myvol2,target=/test nginx:latest
```

Docker может создать volume автоматически.

## 11. tmpfs

```bash
docker run -it --name test_tmpfs --mount type=tmpfs,destination=/testing centos:latest
```

Properties:

- data lives in host memory;
- no persistence after container stops;
- data is outside container writable layer.

## Acceptance

Нужно уметь объяснить:

- storage driver vs volume;
- backing filesystem;
- lowerdir / upperdir / union mount;
- почему container writable layer не подходит для крупных persistent workloads;
- volume vs bind mount;
- anonymous vs named volume;
- tmpfs persistence boundary;
- почему storage-driver change требует backup.
