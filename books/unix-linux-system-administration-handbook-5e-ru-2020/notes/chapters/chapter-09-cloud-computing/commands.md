# Команды главы 9

Только команды и формы команд, подтверждённые RAG главы 9. Исторические cloud CLI examples отражают состояние инструментов на момент издания.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `pip install awscli` | Установить AWS CLI | command `aws` доступна в environment | state-changing / network |
| `aws configure` | Настроить AWS API credentials, default region и output format | credentials/region записаны корректно и защищены | state-changing / sensitive |
| `aws help` | Общая справка AWS CLI | available command hierarchy | read-only |
| `aws ec2 help` | Справка по EC2 subcommands | syntax/options | read-only |
| `aws ec2 describe-instances` | Показать instances в current region | IDs, state, addresses, metadata | read-only / network |
| `aws ec2 describe-images` | Найти/декодировать AMI identifiers | image ID и intended OS/image | read-only / network |
| `aws ec2 run-instances --image-id <ami> --instance-type <type> --associate-public-ip-address --key-name <key>` | Создать EC2 instance | instance ID, subnet/security group, IP, region, image/type | state-changing / billable |
| `aws ec2 get-console-output --instance-id <id>` | Получить boot/console output instance | low-level boot errors/output | read-only / network |
| `aws ec2 get-console-output --instance-id <id> \| sed 's/\\r\\n/\\n/g'` | Сделать console JSON output читаемее | line breaks rendered usefully | read-only |
| `aws ec2 stop-instances --instance-id <id>` | Остановить EC2 instance, сохранив его для later use | state переходит через stopping к stopped | state-changing / billable implications |
| `aws ec2 wait ...` | Дождаться AWS event/state, как указано в footnote главы | automation waits for target state | read-only / blocking |
| `gcloud init` | Аутентифицировать и настроить project/zone/defaults | active project, zone и local config | state-changing / auth |
| `gcloud help` | Общая справка gcloud | available commands | read-only |
| `gcloud -h` | Краткая справка | command usage | read-only |
| `gcloud help compute` | Справка по Compute Engine commands | compute subcommands/options | read-only |
| `gcloud compute images list --regexp 'debian.*'` | Найти подходящие Debian images | image name/alias/status | read-only / network |
| `gcloud compute instances create <name> --image <image>` | Создать GCE instance | operation completed, internal/external IP, status | state-changing / billable |
| `gcloud compute ssh <name>` | Подключиться по SSH через gcloud wrapper | login succeeds to intended instance | read-only session / network |
| `gem install tugboat` | Установить historical DigitalOcean CLI used in chapter | `tugboat` command available | state-changing / network |
| `ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa_do` | Создать SSH key pair для droplets | private/public key files created and protected | state-changing / credential-generating |
| `tugboat authorize` | Связать CLI с DigitalOcean API token и SSH settings | API authentication succeeds; token stored locally | state-changing / sensitive |
| `tugboat images \| grep -i ubuntu` | Найти Ubuntu image/slugs | desired image slug/id | read-only / network |
| `tugboat keys` | Показать uploaded SSH keys и numeric IDs | intended key ID | read-only / network |
| `tugboat create -i <image> -k <key-id> <droplet-name>` | Создать DigitalOcean droplet | droplet created with intended image/key | state-changing / billable |
| `tugboat ssh <droplet-name>` | SSH login to droplet | connection reaches intended droplet | read-only session / network |
| `tugboat snapshot <droplet-name> <snapshot-name>` | Создать snapshot перед destroy/recreate workflow | snapshot successfully created | state-changing / storage cost |
| `tugboat destroy <droplet-name>` | Удалить droplet | droplet removed; needed state preserved separately | state-changing / destructive |

## Cloud control-plane safety

- `aws configure` и `tugboat authorize` работают с credentials/tokens. Не публиковать их и не включать в repository.
- Перед `run-instances`/instance create проверять region/zone, image, instance type, SSH key и network exposure.
- Public IP сам по себе не означает доступность: EC2 security group должен разрешать нужный traffic.
- Chapter рекомендует public-key SSH authentication; default image account после bootstrap лучше заменить персональными accounts.
- Instance state меняется не мгновенно; scripts должны учитывать transitional states.
- `stop` и `destroy/terminate` имеют разную semantics. Для destructive delete универсальный rollback отсутствует.
- DigitalOcean chapter workflow отдельно указывает snapshot перед destroy, если later recreation нужна.
- Любой созданный cloud resource может порождать billing даже когда он не используется; lifecycle cleanup является частью acceptance check.

## Cost-oriented verification

После provisioning проверить:

- не создано ли лишних instances/resources;
- нужен ли public IP;
- выбран ли правильный region/zone;
- storage persistent или ephemeral;
- существует ли платный inter-zone/inter-region traffic;
- нужен ли instance постоянно или его можно stop/destroy/scale down;
- billable storage/snapshots не остались без владельца.

## Rollback

- EC2 `stop-instances` — reversible lifecycle transition, не deletion.
- Для полного instance termination конкретная rollback-команда в RAG главы не приведена: `[Needs confirmation]`.
- DigitalOcean workflow поддерживает snapshot before destroy как recovery source.
- Для GCP instance creation explicit rollback command в RAG главы не приведена: `[Needs confirmation]`.
