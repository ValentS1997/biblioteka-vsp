# Шпаргалка: инсталляция и управление программным обеспечением

Цель: делать installation/update воспроизводимыми, dependency-aware и проверяемыми до массового rollout.

## 1. Полный lifecycle главы

~~~text
Provision OS
  ↓
Choose package source
  ↓
Resolve dependencies
  ↓
Install / update
  ↓
Apply local configuration
  ↓
Test on limited scope
  ↓
Promote by groups
  ↓
Verify / document
~~~

Главная ошибка — воспринимать software management только как `install package`. Глава связывает provisioning, repositories, package metadata, localization и testing в один процесс.

## 2. PXE: сетевой boot/install pipeline

По главе:

~~~text
client
  ↓ DHCP request with PXE
DHCP/proxy response
  ↓ boot server + boot filename
TFTP
  ↓ bootloader/config
HTTP / NFS / FTP / other
  ↓ installation image/packages
installer
~~~

DHCP, TFTP и file server могут находиться на разных hosts.

PXELINUX использует PXE API и загружает boot file/config с TFTP server.

## 3. Kickstart: Red Hat/CentOS automation

Конфигурация обычно `ks.cfg`.

Три части:

~~~text
commands
%packages
%pre / %post
~~~

Глава подчёркивает:

- `text` нужен для unattended/non-GUI flow;
- root password лучше задавать через `--iscrypted`;
- package groups можно задавать через `@...`;
- `%pre` выполняется до install;
- `%post` — после install;
- `%post` выполняется в chrooted environment;
- config можно генерировать программно, например через Pykickstart.

## 4. Debian/Ubuntu preseed

Сначала можно получить answers существующей interactive install:

~~~bash
debconf-get-selections --installer > preseed.cfg
debconf-get-selections >> preseed.cfg
~~~

Передача installer:

~~~text
preseed/url=http://host/path/preseed.cfg
~~~

Preseed может задавать locale, network, disk partitioning, users/passwords, task selection и reboot flow.

Security point главы: password hashes предпочтительнее plaintext, но опубликованный hash всё равно остаётся объектом brute-force.

## 5. Cobbler

Cobbler объединяет:

- DHCP;
- DNS;
- TFTP;
- installation images;
- host profiles;
- templates/snippets;
- integration с configuration management.

Смысл — уменьшить повторяемость configuration fragments между разными host profiles.

## 6. FreeBSD automated install

Workflow главы:

~~~text
download ISO
  ↓
extract to local tree
  ↓
modify files / installerconfig
  ↓
build new ISO or PXE image
~~~

Пример extract:

~~~bash
sudo mkdir FreeBSD
sudo tar xpCf FreeBSD <FreeBSD.iso>
~~~

Automation у `bsdinstall` описана как более rudimentary, чем Kickstart/preseed.

## 7. Зачем package system

Пакет обычно включает:

- binaries/files;
- dependency metadata;
- configuration templates;
- install/remove scripts.

Package manager стремится:

- делать install максимально atomic;
- сохранять локальные config changes;
- управлять dependencies;
- поддерживать upgrade/rollback-like behavior.

Но chapter предупреждает: dependency graph несовершенен, а rollback нельзя считать гарантированным без test.

## 8. Linux: low-level tools

### RPM

Read-only:

~~~bash
rpm -qa
rpm -q <package>
rpm -q --whatrequires <package>
~~~

Change:

~~~bash
sudo rpm -U <package.rpm>
~~~

Не использовать `--force` как обычный способ обхода dependency conflict.

### dpkg

Read-only:

~~~bash
dpkg -l
dpkg -l <pattern>
~~~

Change:

~~~bash
sudo dpkg --install <package.deb>
~~~

Low-level tools полезны для direct package operations, но daily administration глава связывает прежде всего с high-level systems.

## 9. APT

Базовый flow:

~~~bash
sudo apt update
sudo apt install <package>
apt upgrade
~~~

APT:

- знает repositories;
- загружает packages;
- разрешает dependencies;
- может модернизировать system package set.

Если package source требует проверки:

~~~text
download only
   ↓
review
   ↓
install
~~~

Глава упоминает `apt-get --download-only`.

## 10. Local mirror

Для большого числа hosts глава предлагает local repository mirror.

APT mirror:

~~~bash
sudo apt install apt-mirror
sudo apt-mirror
~~~

Operational risk: если сотни machines запускают update одновременно, repository/network load может резко вырасти. Scheduled jobs нужно распределять по времени.

## 11. yum

Пример:

~~~bash
yum install <package>
yum update
yum upgrade
yum makecache
~~~

Важно не переносить semantics имён между APT и yum механически: глава отдельно обращает внимание, что одинаково звучащие `update/upgrade` могут означать разные действия.

## 12. FreeBSD software model

Три области:

~~~text
base system
binary packages (pkg)
ports
~~~

### Base system

Проверка:

~~~bash
uname -r
~~~

Update RELEASE:

~~~bash
sudo freebsd-update fetch install
~~~

Release upgrade:

~~~bash
sudo freebsd-update -r <RELEASE> upgrade
~~~

Глава указывает, что RELEASE — production-oriented branch; STABLE/CURRENT имеют другую роль.

## 13. FreeBSD pkg

Preferred path для additional software, если package существует.

Read-only:

~~~bash
pkg info
pkg info <package>
pkg search -i <term>
pkg audit -F
pkg which <file>
pkg version -vIL=
~~~

Changes:

~~~bash
pkg install -y <package>
pkg upgrade
pkg delete <package>
pkg autoremove
pkg clean -ay
~~~

Package database важна; глава рекомендует:

~~~bash
pkg backup
~~~

## 14. FreeBSD ports

Использовать, когда binary package отсутствует или нужны compile-time options.

~~~bash
portsnap fetch extract
portsnap fetch update
whereis <port>
cd /usr/ports/<category>/<port>
make install clean
~~~

Updates:

~~~bash
portmaster -L
portmaster -a
~~~

Build from ports = workload-generating operation; chapter не предлагает считать ports default path, если подходящий `pkg` package существует.

## 15. Localization

Локализация — адаптация distribution/package к local environment без нарушения security, filesystem layout и network topology.

Глава требует structured/reproducible approach.

Исходные данные localization должны находиться в change-control system, чтобы было понятно:

- что изменилось;
- кем;
- что протестировано;
- что готово к deploy.

## 16. Staged rollout

Не развертывать новые releases сразу на все hosts.

~~~text
candidate change
  ↓
test host / limited group
  ↓
observe failures
  ↓
next group
  ↓
critical systems last
~~~

Для critical systems chapter не рекомендует слепое vendor auto-update.

## 17. Testing

Главный тезис:

> тестировать изменения, пока их ещё можно отменить.

Проверять:

- собственную localization;
- system software updates;
- regional/language behavior;
- compatibility;
- behavior before mass rollout.

Пользователи должны иметь канал для быстрого сообщения о проблемах.

## Operational acceptance criteria

- installation source и package repository известны;
- dependency changes просмотрены до install/update;
- sensitive unattended-install secrets не лежат plaintext;
- candidate changes проходят limited-scope test;
- mass updates распределены во времени;
- local configuration находится под change control;
- critical systems не получают untested rollout;
- package database/known-good state сохранены там, где chapter это поддерживает;
- неизвестный rollback помечен `[Needs confirmation]`.
