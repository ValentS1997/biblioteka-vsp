# Команды главы 5

Команды ниже основаны только на RAG главы 5. Cluster operations могут менять distributed state сразу на нескольких nodes; поэтому observation и modifying actions разделены.

## Read-only / observation

| Команда | Что показывает | Scope/risk | Acceptance |
|---|---|---|---|
| `ifconfig -a eth0` | IP/interface manager candidate | read-only | address visible |
| `docker node ls` | Nodes, status, availability, manager role | manager-side read-only | expected nodes Ready/Active |
| `docker node inspect self` | Full node JSON | read-only | node metadata |
| `docker node inspect --pretty self` | Human-readable node info | read-only | role/resources/status |
| `docker node inspect --pretty <node>` | Target node info | read-only | Availability/State |
| `docker service ls` | Services and replica status | read-only | service list |
| `docker service ps <service>` | Tasks, nodes, desired/current state | read-only | task placement |
| `docker service inspect --pretty <service>` | Service specification | read-only | mode/image/config |
| `docker info \| grep Autolock` | Autolock state | read-only | true/false |
| `docker network ls` | Swarm/local networks | read-only | ingress/docker_gwbridge etc. |
| `docker network inspect <network>` | Overlay subnet/gateway/details | read-only | network JSON |
| `docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container-id>` | Container/task IP | read-only | IP address |
| `docker container ls -a` | Containers/tasks on node | read-only | local container list |

## Initialize cluster

```bash
docker swarm init --advertise-addr <manager-ip>:2377 --listen-addr <manager-ip>:2377
```

Effect:
- enables Swarm mode;
- current node becomes manager;
- emits manager/worker join guidance.

Verification:

```bash
docker node ls
```

Rollback command for leaving/removing initialized manager is not provided in the retrieved chapter sequence: `[Needs confirmation]`.

## Join token retrieval

```bash
docker swarm join-token manager
docker swarm join-token worker
```

Effect: exposes join instructions/token. Treat output as sensitive.

## Join worker

```bash
docker swarm join --token <worker-token> <manager-ip>:2377
```

Effect: node joins cluster as worker.

Verification from manager:

```bash
docker node ls
```

Rollback shown in autolock experiment:

```bash
docker swarm leave
```

This changes membership and is disruptive to Swarm work on that node.

## Create and inspect service

```bash
docker service create --name myredis redis:latest
docker service ls
docker service ps myredis
docker service inspect --pretty myredis
```

Effect: creates desired service state and a task/container.

Rollback/removal command is not given in the retrieved chapter text: `[Needs confirmation]`.

## Replicated service / failure experiment

```bash
docker service create --name myredis_replica --replicas=5 redis:latest
docker service ps myredis_replica
```

Source stops Docker on one worker:

```bash
systemctl stop docker
```

Risk: stops Docker Engine and all Docker workloads on that node.

Verification:

```bash
docker service ps myredis_replica
```

Acceptance: replacement task appears on another available node.

Rollback: restart Docker on worker is conceptually discussed, but exact `systemctl start docker` command is not shown in that experiment: `[Needs confirmation]`.

## Scale service

```bash
docker service create --name mynginx --replicas=4 nginx:latest
docker service scale mynginx=7
docker service ps mynginx
docker service scale mynginx=5
```

Effect: changes desired replica count.

Verification: `docker service ps mynginx` and service convergence output.

Rollback: scale back to prior replica count.

## Replicated and global modes

Replicated:

```bash
docker service create --name replicated --replicas 3 --mode replicated redis:latest
docker service ps replicated
```

Global:

```bash
docker service create --name global --mode global nginx:latest
docker service ps global
```

Global behavior: when eligible node joins, manager schedules a global task there.

## Drain node

```bash
docker node update --availability drain <node>
docker service ps <service>
```

Effect:
- node stops receiving new Swarm tasks;
- existing Swarm service tasks move to other ACTIVE nodes.

Verification: source shows old task Shutdown on drained node and replacement Running elsewhere.

Rollback:

```bash
docker node update --availability active <node>
docker node inspect --pretty <node>
```

Acceptance: Availability = Active.

## Autolock

Check:

```bash
docker info | grep Autolock
```

Enable:

```bash
docker swarm update --autolock=true
```

Effect: enables manager autolock and outputs unlock key.

Critical requirement: store unlock key securely.

Source then restarts Docker:

```bash
systemctl restart docker
```

Risk: manager restart; Swarm becomes locked after restart when autolock is enabled.

Verification while locked:

```bash
docker node ls
```

Expected source behavior: Swarm command fails and asks for unlock.

Unlock:

```bash
docker swarm unlock
```

Interactive input: unlock key.

Verification:

```bash
docker node ls
```

Key rotation procedure is mentioned conceptually but command is not included in retrieved text: `[Needs confirmation]`.

## Create custom overlay

```bash
docker network create --driver overlay new_overlay
```

Effect: defines Swarm-scoped overlay network.

Verification manager-side:

```bash
docker network ls
```

Source notes worker may not show custom overlay until a service/task uses it.

Attach service:

```bash
docker service create --name test --replicas 4 --network new_overlay ubuntu:latest sleep infinity
```

Verification on worker:

```bash
docker network ls
docker network inspect new_overlay
```

## Inspect task/container networking

```bash
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container-id>
```

Read-only. Returns private IP for task container.

## Connectivity test inside task

```bash
docker container ls -a
docker container exec -it <container-id> sh
```

Package install from source:

```bash
apt-get update
apt-get install iputils-ping -y
apt-get install traceroute
```

Effect: modifies that task container writable layer/package state.

Verification:

```bash
ping <peer-task-ip>
traceroute <peer-task-ip>
```

Rollback for package changes is not specified: `[Needs confirmation]`.

## Publish service ports

Short syntax:

```bash
docker service create --name myserv_ingress -p 8081:80 nginx
```

Long syntax:

```bash
docker service create --name myservice_ingress --publish published=8080,target=80 nginx
```

Source also demonstrates UDP and TCP selection, conceptually:

```text
published=<host-port>,target=<container-port>,protocol=udp
published=<host-port>,target=<container-port>,protocol=tcp
```

Effect: exposes service via Swarm ingress/routing mesh.

## DNSRR bypass

Source says routing mesh can be bypassed for an external load balancer using endpoint mode:

```text
--endpoint-mode dnsrr
```

A complete command is not explicitly present in retrieved text: `[Needs confirmation]`.

## Overlay data encryption

Source flag:

```text
--opt encrypted
```

Used during overlay network create/update to encrypt application traffic via the mechanism described in the chapter.

Risk: source explicitly warns about performance cost.

## Safety boundary

- Join tokens and autolock unlock keys are credentials; do not paste them into documentation/logs unnecessarily.
- `systemctl stop/restart docker` affects all Docker workloads on target node.
- `docker node update --availability drain` deliberately moves Swarm workloads.
- Published ports change external exposure.
- Network encryption changes data-plane overhead.
