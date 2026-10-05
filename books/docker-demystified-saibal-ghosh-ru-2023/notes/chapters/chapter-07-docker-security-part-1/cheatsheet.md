# Шпаргалка: Docker security — Linux layer

## 1. Security layers

```text
Namespaces   → isolate
Cgroups      → limit/prioritize resources
Capabilities → split privileged operations
AppArmor /
SELinux      → mandatory access policy
Seccomp      → restrict syscalls
```

## 2. Kernel namespaces

| Namespace | Изолирует |
|---|---|
| `PID` | process tree / process IDs |
| `NET` | network stack |
| `MNT` | filesystem/mount namespace |
| `IPC` | shared memory / IPC |
| `USR` | users / UID mapping |
| `UTS` | hostname/NIS domain data |

IPC sharing example from source:

```bash
docker run -dit --name shared --ipc shareable centos
docker run -dit --name shared1 --ipc container:shared centos
```

USR namespace risk in source: container UID may correspond to the same host UID if remapping is not enabled. Mitigations discussed: `userns-remap` and non-root application users.

## 3. Cgroups

Source functions:
- resource limiting;
- prioritization;
- accounting;
- pause/resume resource control.

Memory controls:
- `--memory` / `-m` — hard limit;
- `--memory-reservation` — soft limit;
- `--memory-swap` — memory+swap boundary.

Example:

```bash
docker run -dit --name test   --memory 768m   --memory-reservation 512m   --memory-swap 1024m   centos:latest
```

CPU controls:

```bash
lscpu | grep CPU
docker run -dit --name test --cpus 2.4 busybox:latest
docker run -dit --name test1 --cpuset-cpus 0,3 busybox:latest
docker run -dit --name test2 --cpu-shares 1096 busybox:latest
```

## 4. Capabilities

Observe:

```bash
cat /proc/sys/kernel/cap_last_cap
capsh --print
docker run --rm centos:latest sh -c "capsh --print"
```

Drop a capability:

```bash
docker run -dit --name test1 --cap-drop cap_chown centos:latest
```

Source expected result: `chown` inside this container returns `Operation not permitted`.

Add a capability:

```bash
docker run -dit --name test --cap-add linux_immutable ubuntu:latest
```

Then source demonstrates `chattr +i` preventing file removal until the immutable flag is cleared.

## 5. AppArmor

Observe:

```bash
apparmor_status
aa-status
```

Source default Docker profile: `docker-default`.

Profile workflow:

```text
aa-autodep → complain → aa-logprof → aa-enforce
```

Explicit Docker profile:

```bash
docker run -dit --name test_profile1   --security-opt apparmor=docker-default   ubuntu:latest
```

Custom profile load:

```bash
apparmor_parser -r -W /etc/apparmor.d/myprofile
```

Attach:

```bash
docker run -dit --name test_myprofile   --security-opt "apparmor=myprofile"   alpine:latest
```

## 6. SELinux

Status:

```bash
getenforce
sestatus
```

Modes described: enforcing, permissive, disabled.

Docker security options:

```bash
docker info --format '{{ .SecurityOptions }}'
```

Source enables Docker integration via `/etc/docker/daemon.json`:

```json
{
  "selinux-enabled": true
}
```

Then:

```bash
systemctl restart docker
```

Inspect labels:

```bash
docker inspect <container-id> | grep "Label"
```

MCS example:

```bash
docker run -dit --name max   --security-opt label=level:s0:c0,c3   busybox
```

## 7. Seccomp

Kernel support:

```bash
grep CONFIG_SECCOMP= /boot/config-$(uname -r)
```

Source defines seccomp as a kernel mechanism for restricting system calls available to a container.

## Acceptance

Нужно уметь объяснить six namespaces, cgroups vs namespaces, memory/CPU limits, capabilities, AppArmor complain vs enforce, SELinux labels/MCS, and seccomp syscall filtering.
