# Команды главы 24

Только команды и формы команд, подтвержденные RAG главы 24.

## Xen

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo xl list | Показать running Xen domains | dom0/domU, IDs, memory, VCPUs, state | read-only |
| sudo xl console 19 | Подключиться к console guest с ID 19 из примера | expected guest console | workload-generating |

Guest IDs динамические и после reboot host нумеруются заново. Не использовать ID из примера без xl list.

Глава приводит virt-install для Xen guest creation, но OCR короткого флага перед HTTP source неоднозначен (-l/-1). Полная executable строка поэтому не нормализуется без подтверждения: [Needs confirmation].

Source-supported parameters:
- guest name;
- VBD image path;
- HTTP installation source;
- RAM 512 MiB;
- --nographics.

## KVM

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo virsh --connect qemu:///system | Открыть virsh shell для system KVM | correct hypervisor connection | workload-generating |
| list --all | Показать running и stopped domains внутри virsh | domain names and state | read-only |
| start Windows2016Server | Запустить stopped guest из примера | state becomes running | state-changing |
| shutdown CentOS | Инициировать graceful shutdown guest из примера | state transitions to shut off | state-changing |
| quit | Выйти из virsh shell | shell closed | read-only |
| top | Наблюдать Linux processes, включая KVM guests | VM process resource usage | read-only |
| ps | Наблюдать VM processes | expected process exists | read-only |
| kill <pid> | Завершить VM process как Linux process | only when intentional; guest impact understood | state-changing |

Risk для kill:
- может аварийно завершить guest;
- rollback: [Needs confirmation].

### KVM virt-install

Глава приводит полный пример установки Ubuntu через virt-install с:
- --connect qemu:///system;
- guest name;
- 512 MiB RAM;
- image file;
- 12 GB maximum image size;
- /dev/dvd as installation media;
- --os-type linux;
- --accelerate;
- --hvm;
- --vnc.

В RAG присутствуют OCR-искажения short options и path token, поэтому точную copy/paste строку не реконструируем из model memory. Exact normalized command: [Needs confirmation].

## Packer

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| packer build custom_ami.json | Создать image по Packer template | build stages, cleanup, resulting image ID | workload-generating |

Глава также подтверждает аргумент -debug для packer build. Он приостанавливает execution на каждом этапе для troubleshooting. Полное положение аргумента в строке отдельно не показано, поэтому copy/paste form: [Needs confirmation].

Packer build в примере:
1. создаёт temporary key pair и security group;
2. запускает instance;
3. использует scp/ssh для provisioning;
4. вызывает image creation API;
5. завершает temporary instance.

Rollback:
- использовать предыдущий known-good image/specification;
- exact deletion command для созданного image в главе не приведён: [Needs confirmation].

## VirtualBox / Vagrant

Глава упоминает VBoxHeadless как CLI tool для headless VirtualBox, но не приводит command line.

Vagrant в главе описан концептуально; CLI commands не приведены.

Следовательно:
- VBoxHeadless exact command: [Needs confirmation];
- Vagrant exact commands: [Needs confirmation].
