# Итог главы 7

## Заключение

Глава 7 посвящена Linux-side security mechanisms, на которых строится изоляция и ограничение Docker containers.

Namespaces дают container отдельные views/process spaces для PID, network, mounts/filesystem, IPC, users и hostname/domain. Это базовый isolation layer.

Cgroups отвечают не за namespace isolation, а за resource governance: limits, priorities, accounting и operational control. Source подробно рассматривает memory и CPU flags Docker.

Capabilities уменьшают необходимость давать process монолитный root privilege. Docker по умолчанию ограничивает available capabilities; operator может удалять ненужные или добавлять необходимые.

AppArmor и SELinux реализуют Mandatory Access Control разными моделями. AppArmor использует profiles and modes complain/enforce. Docker source example использует default `docker-default` и custom profile. SELinux использует labels, types, sensitivity/categories and policies; source включает SELinux both at host and Docker daemon level and demonstrates MCS.

Seccomp ограничивает system calls container process. Source рассматривает Docker default seccomp profile как умеренный compatibility-oriented filter.

## Основные тезисы источника

- Linux kernel security primitives directly protect Docker containers.
- Docker uses six namespaces listed in chapter.
- cgroups limit/prioritize/account resource usage.
- Memory and CPU should be bounded where needed.
- Linux capabilities split root privileges.
- Docker exposes a reduced capability set by default.
- AppArmor and SELinux enforce mandatory access controls.
- AppArmor profiles can be complain or enforce.
- SELinux isolation is label/policy based and can use MCS categories.
- Seccomp restricts system calls.

## Ключевые термины

| Термин | Смысл главы |
|---|---|
| Kernel namespace | Isolation of an OS resource/view |
| PID namespace | Separate process tree |
| NET namespace | Separate network stack |
| MNT namespace | Separate mount/filesystem view |
| IPC namespace | Isolated/shared IPC resources |
| USR namespace | User/UID isolation/remapping |
| UTS namespace | Hostname/domain isolation |
| cgroup | Resource grouping/limits/priorities/accounting |
| Capability | Individual privileged kernel permission |
| MAC | Mandatory Access Control |
| DAC | Discretionary Access Control |
| AppArmor | Profile-based Linux MAC |
| SELinux | Label/policy-based Linux MAC |
| MCS | Multi-Category Security labels |
| AVC | SELinux Access Vector Cache |
| Seccomp | System-call filtering mechanism |
| Isolation | Separation of container resources |
| Least privilege | Keep only permissions required |

## Source-specific / version caveats

- Source environment reports 37 capabilities and a default Docker seccomp profile blocking 44 system calls; these values are preserved as source-era facts and not generalized.
- AppArmor/SELinux integration details are described for source-era Docker/Linux distributions.
- Source states AppArmor profiles are applied at container level and SELinux is enabled in Docker daemon configuration; this framing is preserved without external reconciliation.

## Provenance

- Chapter RAG: `p0152:c01`–`p0184:c01`
- PDF pages: 152–184
- Printed pages: 157–189
- Source SHA-256: `7a52f7d947347a470790c7d384390f60bf49fe5426827f5829a75757b50faaa8`
