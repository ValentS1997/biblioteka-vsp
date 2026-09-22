# Команды главы 8

Только команды и формы команд, подтверждённые RAG главы 8. Команды создания, удаления, блокировки, изменения password/group/ownership помечены как state-changing.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `sudo authconfig --passalgo=sha512 --update` | RHEL-era example: изменить default password hashing policy | policy updated; existing hashes не меняются автоматически | state-changing |
| `chage -d 0 <user>` | Аннулировать дату старого password и принудить к смене | user должен изменить password при следующем login/use | state-changing |
| `chfn` | Изменить GECOS/personal information там, где tool поддерживается | changed fields и backend applicability | state-changing |
| `chsh` | Изменить login shell | shell field changed; backend may limit applicability | state-changing |
| `vipw` | Безопасно редактировать passwd/master.passwd с locking | account records remain syntactically consistent | state-changing |
| `vipw -s` | Linux: редактировать shadow через vipw workflow | passwd/shadow остаются согласованными | state-changing |
| `vigr` | Безопасно редактировать `/etc/group` с locking | group record correct | state-changing |
| `vigr -s` | Редактировать shadow group database | group/gshadow consistency | state-changing |
| `newgrp` | Присоединиться к group при использовании group password | resulting group context | state-changing in session |
| `gpasswd` | Установить/изменить group password | group credential updated | state-changing |
| `groupadd` | Linux: создать group | new group/GID exists | state-changing |
| `groupmod` | Linux: изменить group | intended group fields changed | state-changing |
| `groupdel` | Linux: удалить group | group removed without unintended references | state-changing |
| `sudo pw groupmod staff -m dan` | FreeBSD: добавить user dan в group staff | membership updated | state-changing |
| `pw groupshow staff` | FreeBSD: проверить group record | expected member list | read-only |
| `sudo passwd <user>` | Установить password пользователя | account now has intended credential state | state-changing |
| `sudo pw usermod raphael -w random` | FreeBSD: назначить random temporary password | generated password delivered securely and later changed | state-changing |
| `mkdir <home>` | Создать отсутствующий home directory | directory exists before ownership/mode setup | state-changing |
| `sudo chown -R <user>:<group> ~<user>` | Назначить ownership всему home tree | owner/group correct for startup files and home | state-changing |
| `pwd` | После login новым пользователем проверить home directory | current directory is intended home | read-only |
| `ls -la` | Проверить startup files и их ownership/group | hidden files and ownership are correct | read-only |
| `useradd -D` | Linux: показать current useradd defaults | home/shell/default policy values | read-only |
| `sudo useradd -D -s /bin/bash` | Изменить default shell для новых users | future useradd uses intended shell | state-changing |
| `sudo useradd hilbert` | Создать Linux account с defaults | passwd/shadow/group/home behavior as configured | state-changing |
| `sudo useradd -c "David Hilbert" -d /home/math/hilbert -g hilbert -G faculty -m -s /bin/tcsh hilbert` | Создать account с явными GECOS/home/groups/shell | UID/GID, supplementary group, home and shell | state-changing |
| `sudo adduser` | Interactive account creation в Debian/Ubuntu/FreeBSD variants | resulting account/group/home/password state | state-changing |
| `newusers <input-file>` | Linux bulk account creation from prepared file | all intended accounts created; plaintext input file protected | state-changing |
| `userdel <user>` | Linux low-level account removal tool, used by higher-level wrappers | account removed according to local policy | state-changing |
| `deluser <user>` | Debian/Ubuntu higher-level account removal | configured home/mail/backup policy applied | state-changing |
| `rmuser <user>` | FreeBSD account removal workflow | user processes/files/account references handled as intended | state-changing |
| `sudo find <filesystem> -xdev -nouser` | Найти files с UID, которому больше не соответствует user | orphaned ownership after offboarding | read-only / workload-generating |
| `sudo pw lock <user>` | FreeBSD: lock password-based account access | hash receives locked marker; actual access paths reviewed | state-changing |
| `usermod -L <user>` | Linux: lock password by prefixing hash marker | password authentication blocked | state-changing |
| `usermod -U <user>` | Linux: unlock password | password authentication restored | state-changing |

## Не включено как canonical command

В RAG есть OCR-искажённая FreeBSD-команда для компиляции `/etc/login.conf`. Точный token не восстанавливается из RAG с достаточной уверенностью, поэтому команда не нормализована и помечается как `[Needs confirmation]`.

## Критические предостережения главы

- Изменение hashing algorithm не обновляет уже существующие password hashes.
- При ручном создании account placeholder password должен оставлять account неактивным до установки реального password.
- `vipw`/`vigr` предпочтительнее прямого редактирования: они блокируют database и снижают риск конфликтов.
- Не использовать recursive pattern вида `~user/.*` с `chown -R`: он может включить `..` и затронуть parent directory.
- Bulk input для `newusers` содержит initial password в plaintext; файл должен быть защищён.
- Password lock не гарантирует блокировку всех access mechanisms.
- До удаления home/mail data сохранить то, что может понадобиться организации.
- После удаления account искать orphaned files через `find -xdev -nouser`.
- Не переиспользовать UID бывшего пользователя.

## Rollback

- Для создания/удаления/locking account универсальный rollback в RAG не задан: `[Needs confirmation]`.
- До destructive offboarding chapter рекомендует сохранить home/mail data; это recovery point для данных, но не полный rollback identity state.
- Для ошибочного ownership change rollback требует known-good ownership map: `[Needs confirmation]`.
