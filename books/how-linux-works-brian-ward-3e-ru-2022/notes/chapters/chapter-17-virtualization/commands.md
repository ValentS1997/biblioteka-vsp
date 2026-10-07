# Команды и интерфейсы — глава 17 «Виртуализация»

**Provenance:** `p0458:c01`–`p0477:c01`, PDF/печатные страницы 458–477. Включены только команды/интерфейсы, явно поддержанные chapter RAG.

Классы: **RO** — read-only; **WG** — workload-generating; **SC** — state-changing.

## 1. Dockerfile example

```Dockerfile
FROM alpine:latest
RUN apk add bash
CMD ["/bin/bash"]
```

Source semantics:
- `FROM` chooses the base image.
- `RUN` executes during image build and creates a layer/change.
- `CMD` defines the command used when a container is started from the image.

The source later warns that `latest` can move and recommends a specific base-image version tag for stability.

## 2. Build image

```sh
docker build -t hlw_test .
```

**Class:** SC/WG.

- reads `Dockerfile` from the current directory;
- builds image layers;
- tags the resulting image as `hlw_test`.

Verification:

```sh
docker images
```

## 3. List images

```sh
docker images
```

**Class:** RO.

Used both immediately after build and later to identify old/untagged images.

## 4. Run interactive container

```sh
docker run -it hlw_test
```

**Class:** SC/WG.

Source notes:
- `-i` keeps interaction;
- `-t` connects a terminal;
- without `-it` this particular shell-based example exits almost immediately.

The shell in the example runs as root inside the container.

## 5. Inspect process namespace

```sh
ps aux
```

**Class:** RO.

In the chapter example, the shell appears as PID 1 inside the container even though the same process has a different PID on the host.

The text also names `ps` generally as an inspection command.

## 6. Inspect overlay filesystem

```sh
mount
```

**Class:** RO.

The Docker example exposes an overlay root with `lowerdir`, `upperdir` and `workdir`.

Do not treat the concrete paths printed in the book as portable current-system paths.

## 7. Docker network interfaces

The source discusses:
- `docker0`;
- loopback `lo`;
- container-side interfaces such as `eth0`;
- rootless Podman TAP interface such as `tap0`;
- netns and NAT.

No chapter command is supplied for enumerating/configuring these interfaces, so none is invented.

## 8. List running containers

```sh
docker ps
```

**Class:** RO.

Source model: a Docker container is considered running while it has a running process.

## 9. List all containers

```sh
docker ps -a
```

**Class:** RO.

Used to see exited containers that normal `docker ps` omits.

## 10. Export container filesystem

The text names:

```text
docker export
```

**Class:** RO/SC-to-output-file depending on invocation.

The complete syntax/target is not shown in the retrieved chapter text, therefore operands and output handling are **[Needs confirmation]**.

## 11. Remove stopped container

The text names:

```text
docker rm
```

**Class:** SC.

Used for exited containers. Exact operand syntax is **[Needs confirmation]** because the source does not print a complete command line.

Verification: `docker ps -a`.

Rollback: not supplied; removal should be treated as destructive container-state cleanup.

## 12. Remove image

The text names:

```text
docker rmi
```

**Class:** SC.

Source says old/untagged images can accumulate and consume disk space.

Exact operand syntax is **[Needs confirmation]**.

Verification: `docker images`.

Rollback: not supplied; image recreation/re-pull details are **[Needs confirmation]**.

## 13. Automatic container removal

The source refers to the `--rm` parameter as an option that causes Docker not to retain the container after its process exits.

```text
docker run --rm ...
```

**Class:** SC/WG with automatic cleanup.

The complete command is not shown; remaining arguments are **[Needs confirmation]**.

## 14. PID-1 helper

The source says to add `--init` to `docker run` when a simple init process is needed to reap completed descendants.

```text
docker run --init ...
```

**Class:** SC/WG.

The exact full invocation is not supplied.

## 15. Docker/Podman command compatibility statement

The chapter says Podman CLI commands correspond to Docker commands, but the surrounding wording about which name replaces which conflicts with the actual Docker examples. Do not infer a normalized substitution rule from this text; see `source-findings.md`.

## 16. Python virtual environment

Create:

```sh
python3 -m venv test-venv
```

**Class:** SC filesystem.

Literal activation line printed by the source:

```sh
. test-env/bin/activate
```

**Class:** SC shell environment.

This does not match the directory name `test-venv` created immediately beforehand. The mismatch is preserved, not corrected.

Exit:

```sh
deactivate
```

**Class:** SC shell environment.

Source effect:
- activation changes the shell environment;
- `VIRTUAL_ENV` points to the environment base directory;
- newly installed packages go to the environment library instead of the system library.

## 17. Named interfaces/tools without a complete command sequence

The chapter names or discusses:
- VirtualBox;
- `VBoxManage`;
- Docker;
- Podman;
- LXC;
- LXD;
- Kubernetes;
- Minikube;
- Supervisor/`supervisord`;
- `slirp4netns`;
- `fuse-overlayfs`.

No complete operational command sequence is supplied for these interfaces, so this artifact does not invent one.

## Command discipline

- Preserve the chapter's image/container distinction.
- Treat build/run/remove operations as state-changing.
- Use inventory commands before cleanup.
- Keep `latest` as source example context; the chapter itself recommends version pinning.
- Do not silently repair the `test-env` / `test-venv` mismatch.
- Do not extend 2022-era Docker/Podman/Kubernetes behavior with model memory.
