# Cheatsheet — глава 17 «Виртуализация»

**Provenance:** `p0458:c01`–`p0477:c01`, PDF/печатные страницы 458–477. Политика **rag_only**.

## Symptom / problem framing

Сначала определить, **что именно требуется изолировать**:

| Задача | Source-grounded boundary |
|---|---|
| Полная операционная система и ее ядро | Virtual machine |
| Набор процессов на общем ядре Linux | Container |
| Зависимости одного приложения/языкового runtime | Runtime virtual environment |

Контейнеры не являются автоматическим решением проблем производительности, данных, логирования, безопасности или управления версиями. Глава прямо перечисляет эти ограничения.

## Baseline / context

Перед изменениями зафиксировать контекст, который реально влияет на решение:

- нужен ли отдельный гостевой kernel или достаточно общего kernel;
- Docker/Podman privilege model: root/rootless — **[Needs confirmation]** для конкретной установки;
- какой image/tag используется;
- какие процессы должны выполняться в контейнере;
- где должны жить изменяемые данные и журналы;
- какие ресурсы хоста являются ограничивающими;
- нужна ли сеть между контейнерами и наружу;
- требуется ли orchestration множества контейнеров.

Конкретные live-system значения в главе не заданы и остаются **[Needs confirmation]**.

## Read-only checks

### Docker image inventory

```sh
docker images
```

**Class:** RO.

Показывает доступные образы и позволяет увидеть untagged/старые образы.

### Running containers

```sh
docker ps
```

**Class:** RO.

Показывает контейнеры, в которых еще выполняются процессы.

### All containers

```sh
docker ps -a
```

**Class:** RO.

Добавляет завершившие работу контейнеры; источник предупреждает, что они могут накапливаться.

### Inside-container process view

```sh
ps aux
```

**Class:** RO.

В примере внутри контейнера видны только процессы его PID namespace; shell имеет PID 1.

### Filesystem view

```sh
mount
```

**Class:** RO.

В Docker-примере root filesystem показана как overlay с `lowerdir`, `upperdir` и `workdir`.

## Interpretation

### VM

Использовать модель VM, когда нужен отдельный полный OS environment. Глава связывает VM с:
- тестированием;
- application compatibility;
- server/cloud workloads.

Operational cost:
- full OS startup;
- updates/security for every guest;
- possible dependency conflicts;
- cost of many isolated VM instances.

### Container

Контейнер в главе — ограниченное окружение выполнения для процессов на общем Linux kernel.

Изоляция складывается из нескольких механизмов:
- control groups;
- devices/filesystem isolation;
- process namespace isolation;
- network namespace/interfaces.

### Runtime environment

Python `venv` применяется для изоляции пакетов приложения внутри одной системы, а не для создания отдельной машины или контейнера.

## Next action

1. Выбрать необходимую isolation boundary: VM / container / runtime environment.
2. Для контейнера определить image/tag и модель privileges.
3. Собрать/запустить минимальный пример.
4. Проверить process view, filesystem view и container/image inventory.
5. Проверить data/log/resource/version/security boundaries.
6. Только после этого масштабировать через LXC/LXD/Kubernetes-style management if required by the workload.

## Modifying action

### Build the chapter Docker example

Dockerfile:

```Dockerfile
FROM alpine:latest
RUN apk add bash
CMD ["/bin/bash"]
```

Build:

```sh
docker build -t hlw_test .
```

**Class:** SC/WG.

Effect: creates image layers and the tagged image `hlw_test`.

Risk/source boundary:
- example uses `latest`;
- later §17.2.5 recommends a specific version tag because `latest` may change unexpectedly.

### Run interactively

```sh
docker run -it hlw_test
```

**Class:** SC/WG.

Effect: creates and runs a container from the image.

### Init helper pattern

Source says to add `--init` to `docker run` when PID 1 must reap orphaned/finished descendants:

```text
docker run --init ...
```

The complete invocation is not supplied by the source; additional arguments are **[Needs confirmation]**.

### Cleanup

Source names:
- `docker rm` for stopped containers;
- `docker rmi` for images.

Exact operands are not supplied in the retrieved text and remain **[Needs confirmation]**.

### Python runtime environment

```sh
python3 -m venv test-venv
```

**Class:** SC filesystem.

The source then prints:

```sh
. test-env/bin/activate
```

but the created directory is `test-venv`. This is preserved as a source mismatch; do not silently normalize it. See `source-findings.md`.

Exit command named by the source:

```sh
deactivate
```

## Verification / acceptance checks

After image build:
- `docker images` shows the tagged image.

After container start:
- `docker ps` shows it while a process is running.
- inside the container, `ps aux` shows the namespaced process view.
- `mount` exposes the overlay model in the Docker example.

After cleanup:
- `docker ps -a` should no longer list a container removed with the appropriate `docker rm` invocation.
- `docker images` should no longer list an image removed with the appropriate `docker rmi` invocation.

For Python virtual environments:
- the source states that activation selects the environment interpreter/library and sets `VIRTUAL_ENV`;
- an exact verification command is not supplied: **[Needs confirmation]**.

## Rollback

| Change | Source-supported rollback/recovery |
|---|---|
| Running container | Allow process to end; container lifecycle then becomes stopped/exited. Persistence semantics contain a source contradiction; see `source-findings.md`. |
| Stopped container | Remove with `docker rm`; exact operand syntax **[Needs confirmation]**. |
| Built image | Remove with `docker rmi`; exact operand syntax **[Needs confirmation]**. |
| Python venv activation | `deactivate`. |
| Python venv directory creation | Removal procedure is not supplied by the chapter: **[Needs confirmation]**. |
| VM/container host configuration | **[Needs confirmation]**; no universal rollback procedure is provided. |

## High-value operator rules

- Do not confuse image state with running container state.
- Do not infer host PID/network/filesystem directly from the container view.
- Track exited containers and old images.
- Treat `latest` as an example tag, not stable version control.
- Plan persistent data and logging explicitly.
- Shared host resources remain finite even with container isolation.
- Repository/base-image trust remains a security boundary.
- Current implementation-specific behavior beyond the 2022 source remains **[Needs confirmation]**.
