# Шпаргалка: облачные вычисления

Цель: понимать cloud как программируемую инфраструктуру с явными boundaries ответственности, state, exposure и cost.

## 1. Базовая модель главы

~~~text
shared provider capacity
        ↓
API / CLI / web control plane
        ↓
virtual compute + network + storage + managed services
        ↓
automation / infrastructure as code
~~~

Cloud отличается от традиционного provisioning прежде всего тем, что ресурсы создаются и удаляются программно.

## 2. IaaS / PaaS / SaaS

Чем выше abstraction, тем меньше слоев управляет пользователь.

~~~text
On-prem:
power → hardware → virtualization → network/storage → OS → runtime → DB → app

IaaS:
provider: physical + virtualization
user: virtual network/storage + OS + runtime + DB + app

PaaS:
provider: infrastructure + OS/platform
user: application/code + часть application data/config

SaaS:
provider: почти весь stack
user: service usage/configuration/data
~~~

Для sysadmin work chapter считает IaaS наиболее близким к традиционному администрированию.

## 3. Выбор provider

Chapter рассматривает три illustrative platforms:

- AWS — широкая service surface и развитый control plane;
- GCP — технически сильная глобальная платформа с похожими базовыми cloud primitives;
- DigitalOcean — более минималистичная модель и быстрый path к VPS.

Это описание отражает период издания, а не текущий market state.

## 4. Control plane

Типы interface:

~~~text
web console
API
CLI
SDK
third-party automation
~~~

Web UI полезен для первых действий.

CLI/API предпочтительны для:

- repeatability;
- scripting;
- bulk operations;
- machine-readable output;
- integration with automation.

## 5. SSH access

Типичный UNIX/Linux cloud access:

~~~text
SSH + public-key authentication
~~~

Проверить:

- правильный username image;
- key pair;
- security group/firewall;
- public/private reachability.

Browser console может помочь при broken SSH/firewall, но chapter предупреждает, что это не полноценная физическая console для BIOS/early boot debugging.

## 6. Regions и availability zones

~~~text
provider
  ↓
region
  ↓
availability zones
  ↓
instances/services
~~~

Region — geographic service area.

Zone — fault-isolated datacenter grouping inside region.

Multi-zone / multi-region повышает resilience, но добавляет:

- deployment complexity;
- network latency;
- traffic charges;
- replication overhead.

## 7. VPS / instances / images

Instance создается из image.

Image содержит как минимум OS/root filesystem + boot state, а может включать дополнительные prepared components.

Instance parameters:

- CPU;
- memory;
- storage;
- network;
- image;
- zone/region;
- access keys;
- firewall/security groups.

Operationally instance — disposable resource only if application/data architecture действительно допускает replacement.

## 8. Virtual network

Cloud virtual network может включать:

- address ranges;
- subnets;
- routes;
- firewall rules;
- VPN connectivity;
- public/private addresses.

Security principle из главы:

~~~text
Internet-exposed perimeter должен быть минимальным
~~~

Hosts без public IP могут администрироваться через:

~~~text
bastion / jump host
или
VPN
~~~

## 9. Storage types

### Object storage

- objects в flat namespace;
- network/API access;
- high durability/large scale;
- не ведет себя как обычный local block disk.

### Block storage

- virtual disk;
- attach to instance;
- suitable for filesystems/databases depending on design;
- capacity и I/O могут тарифицироваться отдельно.

### Ephemeral storage

- local instance storage;
- fast/local;
- данные теряются при deletion instance.

Использовать только для disposable/temp data.

## 10. Managed data services

Provider может отдельно предоставлять:

- relational DB;
- analytical DB;
- in-memory/NoSQL services.

Chapter рассматривает их как альтернативу самостоятельному build/operate соответствующего stack.

## 11. IAM / least privilege

Cloud control plane сам является security boundary.

Цель:

~~~text
каждый user/service получает только нужные permissions
~~~

AWS IAM в chapter используется как пример:

- users;
- groups;
- machine roles;
- policies;
- API key management.

Machine role предпочтительнее ручного распространения long-lived credentials, если platform/service это поддерживает в описанном chapter model.

## 12. Infrastructure as Code

Raw CLI/API удобны для единичных операций, но сложны для большого resource graph.

Chapter показывает:

~~~text
template/config
   ↓
dependency resolution
   ↓
provider API calls
   ↓
desired infrastructure
~~~

Примеры chapter:

- CloudFormation;
- Troposphere для generation CloudFormation;
- Terraform для provider-independent infrastructure definition.

Infrastructure config следует хранить в version control.

## 13. AWS CLI workflow

Установка:

~~~bash
pip install awscli
~~~

Настройка:

~~~bash
aws configure
~~~

Read-only:

~~~bash
aws ec2 describe-images
aws ec2 describe-instances
aws ec2 get-console-output --instance-id <id>
~~~

Create:

~~~bash
aws ec2 run-instances   --image-id <ami>   --instance-type <type>   --associate-public-ip-address   --key-name <key>
~~~

Stop:

~~~bash
aws ec2 stop-instances --instance-id <id>
~~~

## 14. AWS state semantics

Create/stop are not instantaneous.

Automation должна учитывать transition states:

~~~text
pending / starting
running
stopping
stopped
...
~~~

Не считать successful API call равным completed infrastructure state.

## 15. AWS network exposure

В chapter default security group не дает нужного inbound SSH автоматически.

Перед login:

- instance must be reachable;
- security group must allow TCP/22 from intended source;
- intended key pair must match;
- correct image username must be known.

## 16. Console output as diagnostic path

~~~bash
aws ec2 get-console-output --instance-id <id>
~~~

Useful when:

- instance fails boot;
- SSH unavailable;
- low-level startup error suspected.

Это read-only diagnostic path before destructive recovery actions.

## 17. GCP workflow

Initialize:

~~~bash
gcloud init
~~~

Help:

~~~bash
gcloud help
gcloud help compute
~~~

Find image:

~~~bash
gcloud compute images list --regexp 'debian.*'
~~~

Create:

~~~bash
gcloud compute instances create <name> --image <image>
~~~

SSH:

~~~bash
gcloud compute ssh <name>
~~~

Chapter отмечает synchronous behavior `gcloud compute` в показанном create workflow: CLI ждет completion.

## 18. Preemptible / spot-style capacity

Chapter рассматривает discounted compute, которое может быть interrupted.

Suitable only when workload tolerates interruption.

Нельзя переносить этот model на stateful/critical workload без специальной architecture.

## 19. DigitalOcean workflow из chapter

Historical third-party CLI:

~~~bash
gem install tugboat
ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa_do
tugboat authorize
tugboat images | grep -i ubuntu
tugboat keys
tugboat create -i <image> -k <key-id> <name>
tugboat ssh <name>
~~~

Before destroy:

~~~bash
tugboat snapshot <name> <snapshot>
tugboat destroy <name>
~~~

Это artifact chapter period; не считать current provider tooling without separate verification.

## 20. Cost model

Cloud bill может включать:

~~~text
compute
+ load balancers / managed compute services
+ Internet egress/ingress model
+ inter-zone/inter-region traffic
+ block/object storage
+ snapshots
+ I/O operations / provisioned performance
~~~

Low hourly instance price не означает low total system cost.

## 21. Common cost multipliers

Chapter выделяет:

- always-on oversized instances;
- cross-zone/cross-region replication;
- serving large objects directly instead of suitable distribution layer;
- unnecessary stored snapshots/data;
- expensive high-performance storage;
- resources forgotten after experiments.

## 22. Cost-control loop

~~~text
measure
  ↓
monitor
  ↓
understand usage pattern
  ↓
right-size
  ↓
scale down / remove idle capacity
  ↓
re-measure
~~~

Chapter recommends:

- smaller instances for finer control;
- autoscaling down when demand falls;
- monitor before long reserved commitments;
- inspect storage/IOPS costs;
- attribute spending by tags/service/location when environment grows.

## 23. Operational workflow

~~~text
Need workload
  ↓
choose abstraction/provider
  ↓
choose region/zone
  ↓
design network + IAM
  ↓
choose image/storage
  ↓
read-only inspect defaults
  ↓
provision
  ↓
wait for target state
  ↓
verify network/SSH/service
  ↓
monitor usage + cost
  ↓
scale / stop / snapshot / destroy
~~~

## Acceptance criteria

- responsibility boundary IaaS/PaaS/SaaS understood;
- region/zone selected intentionally;
- network exposure minimized;
- IAM follows least privilege;
- persistent vs ephemeral storage is explicit;
- credentials are not committed or logged;
- provisioning state is verified after API/CLI call;
- destructive delete has known recovery point or `[Needs confirmation]`;
- idle/billable resources are reviewed;
- cost monitoring is part of lifecycle, not an afterthought;
- historical provider commands are not assumed current without external verification.
