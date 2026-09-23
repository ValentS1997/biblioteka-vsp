# Шпаргалка: Virtualization

## 1. Core architecture

~~~text
hardware
→ hypervisor
→ guest OS / VM
~~~

Hypervisor mediates:
- CPU;
- memory;
- I/O;
- virtual devices.

Guest OS is isolated from other guests.

## 2. Virtualization modes

Full virtualization:
- emulates virtual hardware;
- guest does not need modification;
- higher emulation overhead.

Paravirtualization:
- guest knows it is virtualized;
- cooperates with hypervisor;
- better performance;
- guest modifications required.

Hardware-assisted:
- CPU virtualization extensions;
- Intel VT / AMD-V;
- guest need not know it is virtualized.

Modern systems combine hardware virtualization, paravirtualized drivers and limited emulation.

## 3. Hypervisor type 1 vs type 2

Type 1:
~~~text
hardware → hypervisor → guests
~~~

Type 2:
~~~text
hardware → host OS → hypervisor → guests
~~~

Chapter warning:
- distinction is conceptually useful;
- operational significance is limited;
- KVM blurs the boundary.

## 4. Live migration

~~~text
source host
→ copy VM memory
→ synchronize changes
→ destination host
→ switch execution
~~~

Use cases from chapter:
- load balancing;
- high availability;
- disaster recovery;
- host maintenance.

## 5. VM images

Image:
- configured OS template;
- bootable by hypervisor;
- basis for cloning;
- can be created from snapshot.

Image format is often hypervisor-specific.

## 6. VM vs container

VM:
- own kernel;
- full OS;
- full boot;
- stronger guest isolation;
- image usually measured in GB.

Container:
- shared host kernel;
- isolated process/filesystem view;
- no full OS boot;
- lower overhead;
- image usually much smaller.

Chapter pattern:
~~~text
physical host
→ VM
→ containers
~~~

## 7. Xen

Architecture:
~~~text
hardware
→ Xen hypervisor
→ dom0
→ domU guests
~~~

dom0:
- privileged;
- hardware access;
- drivers;
- guest management.

Paths:
- /etc/xen;
- /etc/xen/auto;
- /var/log/xen;
- /usr/sbin/xl.

Check:
~~~bash
xl list
~~~

Console:
~~~bash
xl console <current-id>
~~~

Always obtain current ID first.

## 8. Xen storage

VBD can be:
- dedicated disk/logical volume;
- file-backed image.

Tradeoff from chapter:
- dedicated storage → higher performance;
- file-backed → easier movement/management.

## 9. KVM

~~~text
Linux kernel = hypervisor
guest VMs = Linux processes
QEMU = virtual hardware
~~~

Requirements:
- Intel VT or AMD-V.

Paravirtualized network/disk/video drivers are recommended for performance.

Management:
- virt-install → create guest;
- virsh → lifecycle;
- top/ps → observe VM processes.

## 10. virsh workflow

~~~text
virsh --connect qemu:///system
→ list --all
→ start / shutdown
→ quit
~~~

Do not use kill as normal graceful lifecycle control.

## 11. bhyve

Chapter context:
- included in FreeBSD 10.0;
- BSD/Linux/Windows guests;
- limited hardware/features at publication time.

Authors advise another solution unless embedded FreeBSD virtualization is specifically needed.

## 12. VMware

ESXi:
- mature virtualization platform;
- centralized management ecosystem;
- live migration technology emphasized in chapter.

Some advanced capabilities require paid licensing.

## 13. VirtualBox

Use case:
- workstation;
- developer/test environments;
- cross-platform.

Chapter does not treat it as normal production virtualization platform.

Headless tool:
~~~text
VBoxHeadless
~~~

Exact invocation: [Needs confirmation].

## 14. Packer

~~~text
JSON template
→ builder
→ temporary instance
→ provisioner
→ configured VM
→ new image
→ cleanup
~~~

Exact build example:
~~~bash
packer build custom_ami.json
~~~

Result:
- new image identifier on success;
- cleanup after failure.

## 15. Image as code

Packer spec in repository gives:
- transparency;
- repeatability;
- audit trail;
- rollback-friendly history.

Do not manually mutate image if reproducible template can express the change.

## 16. Packer debugging

Chapter supports -debug for packer build:
- pauses each stage;
- useful for build troubleshooting.

Exact argument placement: [Needs confirmation].

## 17. Vagrant

Vagrant:
- wrapper around virtualization providers;
- not a hypervisor;
- creates portable preconfigured development environments.

Useful relation:
~~~text
Packer builds standard base image
→ Vagrant distributes developer environment
~~~

## 18. Safe operational flow

~~~text
choose VM/container boundary
→ choose platform
→ define resources
→ create guest/image
→ verify boot/state
→ test lifecycle
→ automate repeatable image build
~~~

## 19. Rollback

Preferred baseline:
- known-good VM image;
- versioned Packer specification;
- snapshot when source-supported by local workflow.

Exact rollback command for each hypervisor is not provided by chapter: [Needs confirmation].
