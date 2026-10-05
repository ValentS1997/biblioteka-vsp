# Ответы к контрольным материалам — глава 7

## Контрольный тест: ключ из источника

| № | Ответ |
|---:|:---:|
| 1 | C |
| 2 | B |
| 3 | D |
| 4 | A |
| 5 | B |
| 6 | D |
| 7 | C |
| 8 | B |

Ключ `1-C, 2-B, 3-D, 4-A, 5-B, 6-D, 7-C, 8-B` приведён в `p0183:c01`.

## Ответы на открытые вопросы

### 1. Какие security options предоставляет OS для Docker?

Source groups them around Linux namespaces, cgroups, capabilities, Mandatory Access Control through AppArmor/SELinux, and seccomp.

### 2. Что такое kernel namespaces?

Kernel namespace — isolation mechanism that gives a process/container its own view of a class of OS resources. Chapter lists PID, NET, MNT, IPC, USR and UTS.

### 3. В чём концепция cgroups?

cgroups group processes so resource use can be limited, prioritized, accounted and controlled. Docker runtime flags translate into host cgroup settings.

### 4. Что такое MAC и чем он отличается от DAC?

MAC is centrally enforced mandatory policy that users/programs cannot simply override. Source contrasts it with discretionary policies, where access is based on discretionary permission mechanisms. It also notes SELinux does not perform its check if DAC has already denied access.

### 5. Что такое seccomp?

Seccomp is a Linux kernel mechanism that restricts system calls available to a container process through a profile/filter.

### 6. Что такое capabilities?

Capabilities split traditional root privileges into individual permissions that can be enabled or disabled independently for a process/thread.

### 7. Как Docker containers работают с capabilities?

Source says Docker exposes only a limited default set needed by common applications. Operator can remove privileges with `--cap-drop` or add required ones with `--cap-add`.

### 8. Какие преимущества SELinux даёт Docker containers?

SELinux labels processes/objects and enforces policy between them. In source Docker integration adds process/mount labels; MCS categories can further separate containers and reduce cross-container access.

### 9. Как настроить AppArmor profile для container?

```text
create/edit profile
→ load with apparmor_parser
→ verify with aa-status
→ start container with --security-opt apparmor=<profile>
→ test expected allow/deny behavior
```

Source custom profile body is OCR-ambiguous, so a full copy/paste profile is intentionally not reconstructed.

### 10. Как source контролирует memory и CPU consumption?

Memory:
- `--memory`;
- `--memory-reservation`;
- `--memory-swap`.

CPU:
- `--cpus`;
- `--cpuset-cpus`;
- `--cpu-shares`.

These options use cgroup controls on host.

## Operational map

```text
isolation       → namespaces
resource limits → cgroups
privileges      → capabilities
access policy   → AppArmor / SELinux
syscalls        → seccomp
```

## Provenance

Ответы сформированы только по chapter RAG `p0152:c01`–`p0184:c01`. External sources и model-memory не использовались.
