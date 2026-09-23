# Шпаргалка: Containers / Docker

## 1. Container mental model

~~~text
host kernel
→ namespaces
→ cgroups
→ capabilities / seccomp
→ isolated process group
→ private filesystem/network view
~~~

Container is not a VM:
- shared host kernel;
- no independent OS boot;
- processes are the workload.

## 2. Image model

~~~text
read-only base layers
+ per-container writable layer
= container filesystem
~~~

Copy-on-write:
- unchanged layers are shared;
- writes stay in container layer;
- base image remains unchanged.

## 3. Docker architecture

~~~text
docker CLI
→ UNIX socket or TLS TCP
→ privileged dockerd
→ images / containers / networks / volumes
~~~

Default data directory in chapter:
~~~text
/var/lib/docker
~~~

## 4. Security boundary: daemon

Access to dockerd ≈ root-level host control.

Preferred chapter model:
~~~text
trusted admin
→ sudo
→ docker CLI
→ local UNIX socket
~~~

Avoid casual membership in docker group.

Remote daemon:
- port 2375 = ordinary HTTP;
- port 2376 = TLS form in chapter;
- always use TLS.

## 5. Baseline checks

~~~bash
docker info
docker version
docker ps
docker ps -a
docker images
docker network ls
docker volume ls
~~~

Before changing/cleaning anything, inventory runtime state.

## 6. Pull and run

~~~bash
docker pull debian
docker run debian /bin/echo "Hello World"
~~~

Interactive:
~~~bash
docker run --hostname debian -it debian /bin/bash
~~~

Container exits when PID 1 exits.

## 7. Long-running service

~~~bash
docker run -p 80:80 --hostname nginx --name nginx -d nginx
docker ps
curl localhost
docker logs nginx
~~~

Server process should remain foreground.

## 8. Diagnose running container

Start with logs:
~~~bash
docker logs <container>
~~~

Then, if required:
~~~bash
docker exec -ti <container> bash
~~~

Do not install sshd merely for administration.

## 9. Stop / start / remove

~~~bash
docker stop <container>
docker start <container>
docker ps -a
docker rm <container>
~~~

Container state is not the same as image state.

## 10. Volumes

Docker-managed volume:
~~~text
container /data
→ persistent volume
→ survives container deletion
~~~

Bind mount:
~~~text
host /mnt/data
↔ container /data
~~~

Bind mount increases coupling and host-data exposure.

## 11. Data container pattern

Chapter historical pattern:

~~~bash
docker create -v /mnt/data:/data --name nginx-data nginx
docker run --volumes-from nginx-data ...
~~~

Conceptual goal:
- decouple persistent data mapping from disposable application container.

## 12. Docker networking

Default bridge:
~~~text
external network
→ host NIC
→ docker0
→ veth
→ container eth0
~~~

Modes:
- bridge;
- host;
- none.

host mode:
- shares host network stack;
- less isolation;
- possible port conflicts.

## 13. Inspect network

~~~bash
docker network ls
ip addr show
docker inspect <container>
~~~

If bridge subnet collides with external routing, chapter points to dockerd --fixed-cidr.

## 14. Storage drivers

Chapter compares:
- aufs;
- btrfs;
- devicemapper;
- overlay;
- vfs;
- zfs.

Rule:
- storage driver affects performance/stability;
- stay with distribution default unless team deeply understands alternative.

## 15. Daemon changes

~~~text
read current docker info
→ save current systemd override
→ systemctl edit docker
→ restart docker
→ systemctl status docker
→ docker info
~~~

Daemon restart is service-impacting.

Chapter syntax is Docker 1.13.1-era; modern applicability: [Needs confirmation].

## 16. Dockerfile

Image build should be code, not manual mutation.

Core instructions:
- FROM;
- RUN;
- ENV;
- COPY / ADD;
- EXPOSE;
- CMD;
- USER;
- VOLUME;
- WORKDIR;
- ARG.

Security:
- ARG is not for secrets;
- USER should be non-root where possible.

## 17. Build image

~~~bash
docker build -t nginx:ulsah .
docker images
~~~

Then:
~~~bash
docker run -p 80:80 --name nginx-ulsah -d nginx:ulsah
curl localhost
~~~

## 18. Registry

Flow:
~~~text
build
→ tag registry/name
→ login
→ push
→ pull by other hosts
~~~

Private registry:
- authenticate;
- use TLS;
- plan storage/cleanup/authorization.

## 19. Content trust

~~~bash
export DOCKER_CONTENT_TRUST=1
~~~

Purpose:
- verify image integrity;
- verify expected publisher.

Unknown/unsigned public images are supply-chain risk.

## 20. Logging

Container convention:
~~~text
normal logs → STDOUT
errors      → STDERR
~~~

Docker logging driver handles routing.

Use:
~~~bash
docker logs <container>
docker logs -f <container>
~~~

Configure rotation so logs do not fill disk.

## 21. Least privilege

Prefer:
- unprivileged USER;
- read-only root filesystem when possible;
- drop capabilities;
- add back only required capability.

Examples:
~~~bash
docker run --read-only <image>
docker run --cap-drop ALL --cap-add NET_RAW debian:jessie
~~~

Avoid --privileged unless explicitly justified.

## 22. Disposable container rule

Bad:
~~~text
enter running container
→ manually patch
→ forget what changed
~~~

Good:
~~~text
diagnose
→ fix Dockerfile/image automation
→ build new image
→ replace container
~~~

## 23. Disk leak troubleshooting

Check:
~~~bash
docker ps -a
docker images
docker volume ls
docker volume ls -f dangling=true
~~~

Cleanup commands are destructive:
- docker system prune;
- docker image prune;
- docker volume rm ...

Do not automate blindly without predictable workload and retention logic.

## 24. Cluster scheduler model

~~~text
desired workload
→ scheduler
→ choose node with capacity
→ run container
→ health monitoring
→ service discovery / routing
~~~

Standalone dockerd manages containers, not a distributed HA application platform.

## 25. Kubernetes

Building blocks in chapter:
- API server;
- scheduler;
- controller manager;
- kubelet;
- cAdvisor;
- proxy.

Pod:
- one or more co-located containers;
- disposable;
- pod IP is not a durable service identity.

Service:
- stable address over changing pods.

## 26. Mesos / Marathon

Mesos:
- masters;
- agents;
- frameworks.

Marathon:
- container/application framework;
- JSON/REST-oriented deployment model.

Cluster HA commonly adds ZooKeeper complexity.

## 27. Docker Swarm

Chapter:
~~~bash
docker swarm init
~~~

Swarm:
- integrated with Docker;
- desired-state scheduling;
- built-in load balancing;
- TLS between nodes by default.

Rollback command not in chapter: [Needs confirmation].

## 28. AWS ECS

Model:
~~~text
AWS-managed cluster manager
→ ECS agent on EC2 nodes
→ JSON task definition
→ scheduling
→ AWS load balancing / IAM / registry integration
~~~

## 29. Canonical operational rule

~~~text
understand one container on one host
→ make image reproducible
→ externalize persistent data
→ secure daemon and image supply chain
→ make logs observable
→ only then add orchestration
~~~
