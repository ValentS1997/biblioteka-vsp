# Диаграммы: storage drivers и volumes

## Writable layer vs persistent storage

```mermaid
flowchart TB
    C["Container"] --> RW["Thin read-write layer"]
    RW --> SD["Storage driver"]
    C --> V["Docker volume"]
    C --> B["Bind mount"]
    C --> T["tmpfs"]
    V --> H1["Docker-managed host storage"]
    B --> H2["Arbitrary host path"]
    T --> RAM["Host RAM"]
```

## Overlay2

```mermaid
flowchart TB
    L1["lowerdir: image layer 1"] --> M["Merged / union mount"]
    L2["lowerdir: image layer 2"] --> M
    U["upperdir: changes / diff"] --> M
    W["work: OverlayFS internal"] --> U
    M --> C["Container filesystem view"]
```

Lower layers остаются неизменяемыми; изменения записываются в upperdir.

## Backing filesystem dependency

```mermaid
flowchart LR
    DISK["Host filesystem / backing filesystem"] --> ROOT["/var/lib/docker"]
    ROOT --> DRV["Storage driver"]
    DRV --> IMG["Images"]
    DRV --> RW["Container writable layers"]
```

Совместимость storage driver зависит от backing filesystem и kernel support.

## Bind mount

```mermaid
flowchart LR
    HOST["Host: /root/testing"] <-->|bind| CONT["Container: /test1"]
```

Путь выбирается на host и не обязан находиться в Docker-managed area.

## Named volume

```mermaid
flowchart LR
    VOL["Docker volume: myvolume"] --> MP["/var/lib/docker/volumes/myvolume/_data"]
    MP <-->|mount| C1["Container A"]
    MP <-->|mount| C2["Container B"]
```

Один volume может использоваться несколькими containers.

## tmpfs

```mermaid
flowchart LR
    RAM["Host RAM"] <-->|tmpfs mount| C["Container /testing"]
    STOP["Container stops"] --> DROP["tmpfs data unavailable"]
```

tmpfs не предоставляет persistence после остановки container.

## Storage-driver change

```mermaid
flowchart LR
    S["Stop Docker"] --> B["Backup /var/lib/docker"]
    B --> E["Edit daemon.json"]
    E --> ST["Start Docker"]
    ST --> V["Verify docker info"]
```

Это disruptive workflow; backup — обязательная точка возврата в логике главы.
