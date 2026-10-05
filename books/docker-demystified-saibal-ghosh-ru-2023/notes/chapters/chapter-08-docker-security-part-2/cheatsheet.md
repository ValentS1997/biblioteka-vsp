# Шпаргалка: Docker Enterprise security

## 1. Components

```text
Docker Enterprise
├─ Docker Engine Enterprise
├─ Universal Control Plane (UCP)
└─ Docker Trusted Registry (DTR)
```

| Component | Source role |
|---|---|
| Docker Engine Enterprise | image/container runtime |
| UCP | centralized cluster/application management |
| DTR | enterprise image registry + scanning |

Source explicitly notes the 2019 Mirantis acquisition. Treat this chapter as source-era architecture.

## 2. Source lab topology

```text
Node 1
├─ Docker EE
├─ UCP
└─ Swarm manager

Node 2
├─ Docker EE
├─ Swarm worker
└─ DTR
```

Minimum lab design in source: two Linux servers.

## 3. UCP requirements from source

- 16 GB RAM;
- 4 vCPU;
- 25–100 GB free disk;
- Docker Engine Enterprise 19.03;
- Linux kernel ≥ 3.10;
- static IP.

These are historical/source requirements, not current guidance.

## 4. UCP installation pattern

Source pulls UCP image:

```bash
docker image pull docker/ucp:latest
```

Install pattern:

```bash
docker container run --rm -it --name ucp   -v /var/run/docker.sock:/var/run/docker.sock   docker/ucp:latest install   --host-address <manager-ip>   --interactive
```

Effect: major cluster/control-plane change.

## 5. Worker join

UCP generates a `docker swarm join --token ...` command.

Security rule for artifacts:
- join token = credential;
- do not store it in documentation;
- represent as `<worker-token>`.

## 6. DTR

Source installs DTR from a UCP-generated command and registers it against UCP.

The source lab includes disabled TLS verification during setup. Preserve as lab fact only; do not use it as secure baseline.

## 7. Client Bundle

Purpose:
- authenticate CLI requests to UCP;
- configure Docker CLI and Kubectl for UCP;
- provide client certificate/key material.

Source environment variables:

```text
DOCKER_HOST
DOCKER_CERT_PATH
DOCKER_TLS_VERIFY
```

Verification:

```bash
echo "$DOCKER_HOST"
echo "$DOCKER_CERT_PATH"
echo "$DOCKER_TLS_VERIFY"
docker version --format '{{ .Server.Version }}'
```

Private key and bundle files are sensitive.

## 8. DTR vulnerability scanning

Flow:

```text
docker pull
   ↓
docker tag for DTR
   ↓
docker login
   ↓
docker push
   ↓
DTR vulnerability scan
   ↓
CVE findings
```

Source enables:
- Image Scanning;
- Online Syncing;
- manual scan;
- Scan on push.

Offline source model: upload/install a tar-file containing CVE database updates.

## 9. Image push pattern

```bash
docker pull busybox:latest
docker tag busybox:latest <dtr>/<user>/<repo>:busybox
docker login --username <user> <dtr>
docker push <dtr>/<user>/<repo>:busybox
```

Old-image experiment:

```bash
docker pull busybox:1.25.1
docker tag busybox:1.25.1 <dtr>/<user>/<repo>:busybox_old
docker push <dtr>/<user>/<repo>:busybox_old
```

Source-era result: old image shows critical/major CVE findings. Do not generalize exact findings to current registries/databases.

## 10. RBAC mental model

```text
WHO?        WHAT?       WHERE?
Subject  +  Role   +   Collection
              ↓
            Grant
```

Subjects:
- users;
- organizations;
- teams.

Role = permissions.  
Collection = resources controlled by that grant.

## 11. Built-in Swarm roles in source

| Role | Source meaning |
|---|---|
| View Only | view resources, no create |
| Restricted Control | change resources with safety restrictions |
| Scheduler | schedule workloads / view nodes; viewing workloads needs separate permission |
| Full Control | broadest granted resource control |

## 12. Custom grant flow

```text
create collection My_collection
        ↓
create role My_role
        ↓
select subject itops
        ↓
select collection
        ↓
select role
        ↓
create grant
```

## 13. Built-in collections in source

- `/`
- `/System`
- `/Shared`
- `/Shared/Private/`
- `/Shared/Legacy/`

## Acceptance

Нужно уметь объяснить:
- Docker EE / UCP / DTR roles;
- why Client Bundle exists;
- three environment variables;
- CVE scanning flow;
- scan-on-push;
- subject / role / collection / grant;
- users vs organizations vs teams;
- predefined roles and collections from source.
