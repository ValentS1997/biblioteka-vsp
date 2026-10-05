# Шпаргалка: Docker Swarm

## 1. Mental model

```text
Docker Swarm cluster
├─ managers
│  ├─ leader
│  ├─ scheduler / orchestration
│  └─ consensus / cluster state
└─ workers
   └─ run assigned tasks
```

Service — desired-state description.  
Task / replica — concrete execution unit, mapped to a container.

## 2. Preflight network ports from source

| Port | Protocol | Назначение по главе |
|---|---|---|
| 2377 | TCP | cluster management / manager connection |
| 7946 | TCP + UDP | communication between nodes |
| 4789 | UDP | overlay/VXLAN traffic |

Firewall implementation: `[Needs confirmation]` — vendor-specific commands в chapter не приведены.

## 3. Initialize Swarm

Read IP first (source example):

```bash
ifconfig -a eth0
```

Initialize manager:

```bash
docker swarm init --advertise-addr <manager-ip>:2377 --listen-addr <manager-ip>:2377
```

Effect: current node becomes manager and emits join instructions/tokens.

Verification:

```bash
docker node ls
```

## 4. Join tokens and workers

Retrieve token instructions:

```bash
docker swarm join-token manager
docker swarm join-token worker
```

Join worker:

```bash
docker swarm join --token <worker-token> <manager-ip>:2377
```

Treat token as sensitive credential.

## 5. Node observation

```bash
docker node ls
docker node inspect self
docker node inspect --pretty self
docker node inspect --pretty <node>
```

`docker node ls` is executed from manager according to source.

Key fields:

- STATUS;
- AVAILABILITY;
- MANAGER STATUS;
- Leader;
- platform/resources.

## 6. Consensus / quorum

Source model:

- use odd number of managers;
- usually 3 or 5;
- Raft failure tolerance ≈ `(N-1)/2`;
- quorum required for cluster state changes;
- without quorum existing tasks may continue, but scheduler cannot safely reconcile failures.

## 7. Services and tasks

Create:

```bash
docker service create --name myredis redis:latest
```

Observe:

```bash
docker service ls
docker service ps myredis
docker service inspect --pretty myredis
```

Relationship:

```text
service
  ├─ desired state
  └─ tasks/replicas
       └─ containers on nodes
```

## 8. Replicas and self-healing

```bash
docker service create --name myredis_replica --replicas=5 redis:latest
docker service ps myredis_replica
```

Failure experiment in source stops Docker on a worker:

```bash
systemctl stop docker
```

Manager then observes replacement task on another available node.

This is disruptive on the target worker.

## 9. Scaling

```bash
docker service create --name mynginx --replicas=4 nginx:latest
docker service scale mynginx=7
docker service ps mynginx
docker service scale mynginx=5
```

Acceptance: service converges to requested replica count.

## 10. Replicated vs global

Replicated:

```bash
docker service create --name replicated --replicas 3 --mode replicated redis:latest
```

Global:

```bash
docker service create --name global --mode global nginx:latest
```

Difference:

- replicated → target count chosen by user;
- global → one task per eligible node; new node gets a task automatically.

## 11. ACTIVE / DRAIN

Drain:

```bash
docker node update --availability drain <node>
docker service ps <service>
```

Effect:
- no new Swarm tasks on drained node;
- current Swarm service tasks are rescheduled to ACTIVE nodes.

Return:

```bash
docker node update --availability active <node>
docker node inspect --pretty <node>
```

Important: tasks moved away do not necessarily return immediately.

## 12. Autolock

Check:

```bash
docker info | grep Autolock
```

Enable:

```bash
docker swarm update --autolock=true
```

This outputs an unlock key. Store it securely.

To make restart behavior visible, source restarts Docker:

```bash
systemctl restart docker
```

Unlock:

```bash
docker swarm unlock
```

Command prompts for unlock key.

## 13. Swarm networks

Default objects described by source:

- `docker_gwbridge` — bridge to external world;
- `ingress` — default overlay/routing ingress network.

Observe:

```bash
docker network ls
```

Create custom overlay:

```bash
docker network create --driver overlay new_overlay
```

Attach service:

```bash
docker service create --name test --replicas 4 --network new_overlay ubuntu:latest sleep infinity
```

Inspect:

```bash
docker network inspect new_overlay
```

Container IP:

```bash
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container-id>
```

## 14. Overlay reachability

Enter task container:

```bash
docker container ls -a
docker container exec -it <container-id> sh
```

Source installs ping/traceroute inside Ubuntu example:

```bash
apt-get update
apt-get install iputils-ping -y
apt-get install traceroute
```

Then uses `ping` and `traceroute` between task container addresses.

## 15. Published ports / routing mesh

Short syntax:

```bash
docker service create --name myserv_ingress -p 8081:80 nginx
```

Long syntax from source:

```bash
docker service create --name myservice_ingress --publish published=8080,target=80 nginx
```

Protocols can be selected with `protocol=udp` / `protocol=tcp`.

Routing mesh distributes incoming requests without client knowledge of target task location.

To bypass mesh when an external load balancer is used, source points to DNSRR:

```text
--endpoint-mode dnsrr
```

Exact full service command for DNSRR is not shown in the retrieved chapter text: `[Needs confirmation]`.

## 16. Overlay encryption

Source states that application data encryption can be enabled on overlay network create/update with:

```text
--opt encrypted
```

It describes IPSec over VXLAN and warns about performance impact.

## 17. Troubleshooting

First direction in chapter: inspect service logs if logging driver supports them.

Source mentions:

- default example: `json-file`;
- follow stream: `--follow`;
- limit output: `--tail`.

Exact complete troubleshooting command is not reproduced in the retrieved text: `[Needs confirmation]`.

## Acceptance

Нужно уметь объяснить:

- manager vs worker;
- leader/quorum/Raft;
- service vs task/replica;
- desired state reconciliation;
- replicated vs global;
- DRAIN vs ACTIVE;
- autolock and unlock key;
- `docker_gwbridge` vs `ingress`/overlay;
- routing mesh vs DNSRR;
- required Swarm ports from chapter.
