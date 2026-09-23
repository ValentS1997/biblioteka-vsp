# Команды главы 25

Только команды и формы команд, подтверждённые RAG главы 25. Глава основана на Docker 1.13.1; version-specific applicability вне контекста книги — [Needs confirmation].

## Read-only / observation

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| docker info | Сводка daemon/runtime configuration | storage driver, containers/images, daemon state | read-only |
| docker version | Версии client/server | version mismatch/context | read-only |
| docker ps | Running containers | name, image, status, published ports | read-only |
| docker ps -a | Running + stopped containers | stale/stopped inventory before cleanup | read-only |
| docker images | Local images | tags, image IDs, size | read-only |
| docker inspect <container> | Effective container JSON configuration | mounts, network, image/config | read-only |
| docker logs <container> | Container STDOUT/STDERR logs | application errors/events | read-only |
| docker logs -f <container> | Follow container logs | live diagnostic stream | read-only |
| docker top <container> | Container process state | expected process tree | read-only |
| docker network ls | List Docker networks | bridge/host/none/custom networks | read-only |
| docker volume ls | List Docker volumes | persistent volumes before cleanup | read-only |
| docker volume ls -f dangling=true | List dangling volumes | candidates for removal | read-only |
| ip addr show | Inspect host interfaces/bridge/veth | docker0, host NICs, veth | read-only |
| dockerd -h | Show daemon options | supported daemon arguments | read-only |
| systemctl status docker | Verify Docker service after change | active/running and actual ExecStart | read-only |

## Container/image lifecycle

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo systemctl start docker | Start Docker daemon in chapter CentOS example | daemon becomes active | state-changing |
| docker pull debian | Pull base image | digest/tag and successful download | workload-generating |
| docker pull debian:jessie | Pull explicit tagged image | expected tag/digest | workload-generating |
| docker run debian /bin/echo "Hello World" | Create/run short-lived container | expected command output | workload-generating |
| sudo docker run --hostname debian -it debian /bin/bash | Interactive container shell | isolated process/filesystem view | workload-generating |
| docker run -p 80:80 --hostname nginx --name nginx -d nginx | Start background nginx with published port | running status and port mapping | workload-generating |
| docker stop nginx | Stop named container | state becomes stopped | state-changing |
| docker start nginx | Restart existing container with original run args | state becomes running | state-changing |
| docker rm nginx | Remove stopped container | container no longer listed | state-changing |
| docker rmi nginx:ulsah | Remove image | no dependent containers remain | state-changing |
| docker create -v /mnt/data:/data --name nginx-data nginx | Create data-only container from chapter pattern | volume mapping recorded | state-changing |

Before rm/rmi:
- inventory with docker ps -a / docker images;
- verify correct object name/ID;
- persistent data rollback without external copy: [Needs confirmation].

## Diagnostics inside an existing container

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| docker exec -ti <container> bash | Open targeted interactive shell | filesystem/config/process state | workload-generating |
| curl localhost | Verify host-published HTTP endpoint in nginx example | expected HTTP response | read-only |

Chapter anti-pattern:
- do not run sshd merely to administer container;
- connect to host, then use docker exec.

## Volumes / bind mounts

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| docker run -v /data --rm --hostname web --name web -d nginx | Start container with Docker-managed volume | mount exists and survives container lifecycle as expected | workload-generating |
| docker run -v /mnt/data:/data --rm --name web -d nginx | Bind-mount host path into container | correct host path and intended write exposure | workload-generating |
| docker run --volumes-from nginx-data -p 80:80 --name web -d nginx | Reuse volumes from data container | expected persistent data visible | workload-generating |

Bind mount risk:
- directly exposes host path to container;
- verify path and permissions before run.

Filtered docker inspect templates in the source contain OCR-sensitive formatting. Exact copy/paste template: [Needs confirmation].

## Network modes

Source-supported docker run option:
- --net selects network mode;
- bridge is default;
- host shares host network stack;
- none leaves network unconfigured.

Publishing:
~~~text
-p <host-port>:<container-port>
~~~

Security:
- host mode reduces isolation and may produce port conflicts;
- exposing a port changes host network reachability.

## Client / remote daemon security

Chapter example:

~~~bash
export DOCKER_HOST=tcp://10.0.0.10:2376
export DOCKER_CONTENT_TRUST=1
~~~

Rules:
- always use TLS for remote dockerd;
- plain remote HTTP effectively exposes root-equivalent control;
- docker group membership is also root-equivalent in practice;
- prefer sudo-controlled access.

TLS argument names supported by chapter:
- --tlsverify;
- --tlscert;
- --tlskey;
- --tlscacert.

Exact certificate-generation workflow is outside this chapter: [Needs confirmation].

## Capabilities / root filesystem

Source-supported forms:

~~~bash
docker run --read-only <image>
docker run --cap-drop SETUID --cap-drop SETGID debian:jessie
docker run --cap-drop ALL --cap-add NET_RAW debian:jessie
~~~

Danger boundary:
- --privileged grants a much broader capability set and disables many isolation advantages;
- do not present it as a normal recommendation.

## Docker daemon configuration

Read-only baseline:

~~~bash
dockerd -h
docker info
~~~

Chapter systemd flow:

~~~bash
systemctl edit docker
sudo systemctl restart docker
sudo systemctl status docker
~~~

Historical override example changes storage driver, DNS and bridge IP range. The example uses Docker 1.13.1-era daemon syntax; exact modern ExecStart form: [Needs confirmation].

Effects:
- restart interrupts Docker daemon;
- storage/network changes can affect all containers;
- preserve previous unit override before edit.

Rollback:
- restore previous override;
- restart daemon;
- verify with systemctl status docker and docker info.

## Image build

Dockerfile is canonical build input.

Chapter build command, normalized from unambiguous OCR spacing:

~~~bash
docker build -t nginx:ulsah .
~~~

Verification:
~~~bash
docker images
~~~

Run resulting image:
~~~bash
docker run -p 80:80 --name nginx-ulsah -d nginx:ulsah
curl localhost
~~~

Cleanup:
~~~bash
docker stop nginx-ulsah
docker rm nginx-ulsah
docker rmi nginx:ulsah
~~~

Build/run are workload-generating; cleanup is state-changing.

## Registry operations

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| docker login | Authenticate to registry | intended registry/account | state-changing |
| docker tag debian:jessie registry.admin.com/debian:jessie | Add registry-qualified tag | target name correct | state-changing |
| docker push registry.admin.com/debian:jessie | Upload image | authenticated TLS registry and expected tag | workload-generating |
| docker pull registry.admin.com/debian:jessie | Pull from private registry | trusted source and expected image | workload-generating |
| docker run -d -p 5000:5000 --name registry registry:2 | Start local registry container | port 5000 exposure and storage/auth plan | workload-generating |

Chapter rule: run private registry with TLS.

## Logging

Supported concepts:
- daemon --log-driver;
- docker run --logging-driver;
- --log-opt for driver-specific options;
- application normal output → STDOUT;
- errors → STDERR.

Exact OCR rendering of max-size log option is damaged. Copy/paste form: [Needs confirmation].

## Destructive cleanup

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| docker system prune | Remove unused Docker objects | inventory/impact before execution | state-changing |
| docker image prune | Remove unused images | required images not needed for rollback | state-changing |
| docker volume rm $(docker volume ls -qf dangling=true) | Remove dangling volumes | data is not needed and backup exists if required | state-changing |

These are destructive. Do not run blind or on an unknown production host.

Rollback after deletion without external image/volume copy: [Needs confirmation].

## Cluster management

Chapter provides:

~~~bash
docker swarm init
~~~

Effect:
- initializes Docker Swarm state on a node;
- changes cluster role/state;
- classify as state-changing.

Exact rollback/leave command is not provided in chapter: [Needs confirmation].

Kubernetes kubectl is mentioned as the CLI, but no executable kubectl command is given in the chapter. Mesos/Marathon and ECS are described conceptually/API-wise; do not invent CLI commands.
