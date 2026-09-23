# Команды главы 22

Только команды и формы команд, подтвержденные RAG главы 22.

## Read-only / diagnostics

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| testparm -v | Показать effective Samba configuration и defaults | intended smb.conf values, share definitions | read-only |
| smbclient -L //<server> -U <user> | Показать доступные SMB shares | authentication и expected share list | read-only |
| smbstatus | Показать active sessions, shares и locks | user, share, PID, locked files | read-only |
| echo $LANG | Проверить server locale/charset context | UTF-8 или другая locale encoding | read-only |

## Installation / account state

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| pkg install samba48 | Установить Samba package во FreeBSD в примере главы | package installation completed | state-changing |
| sudo smbpasswd -a <user> | Добавить SMB password record для существующего UNIX user | UNIX account already exists; SMB auth works | state-changing |
| smbpasswd | Изменить SMB password текущего пользователя | new SMB password accepted | state-changing |

Linux exact package-manager command в главе не указан: установить пакет samba-common через используемый package manager; exact command — [Needs confirmation].

## Share filesystem permissions

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo chown root:eng /home/eng | Назначить root owner и project group | owner/group correct | state-changing |
| sudo chmod u=rwx,g=rwxs,o= /home/eng | Разрешить group collaboration и setgid inheritance | mode/setgid match policy | state-changing |

Эти команды относятся к конкретному примеру project share. Не переносить group/path без проверки.

Rollback:
- вернуть previous owner/group/mode;
- если baseline permissions не записаны: [Needs confirmation].

## Client mount

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo mount -t cifs -o username=<user> //<server>/<share> <mountpoint> | Смонтировать SMB share в Linux | remote authentication; local ownership/access semantics | state-changing |
| sudo mount -t smbfs //<user>@<server>/<share> <mountpoint> | Смонтировать SMB share во FreeBSD | remote authentication; mount accessible | state-changing |

Дополнительные mount options из главы:
- uid;
- gid;
- fmask;
- dmask.

Использовать их только для согласования local ownership/mode representation с intended access policy.

Rollback:
- обычное размонтирование exact command в главе для SMB section не приведено: [Needs confirmation];
- вернуть previous persistent mount config, если она изменялась.

## Interactive SMB access

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| smbclient //<server>/<share> -U <user> | Открыть FTP-like interactive session к share | authentication, browse/access | workload-generating |

После подключения глава предлагает команду help для просмотра interactive commands.

Session может выполнять file transfers и поэтому не считается гарантированно read-only.

## Runtime debugging

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo smbcontrol smbd debug "4 auth:10" | Изменить runtime debug level всех smbd без правки smb.conf | logs contain required diagnostic detail; revert after test | workload-generating |

Для одного connection:
1. использовать smbstatus;
2. определить smbd PID;
3. передать PID в smbcontrol вместо smbd.

Exact per-PID command template: [Needs confirmation], поскольку глава описывает действие, но не приводит отдельную полную строку.

Risk:
- повышенная verbosity использует system resources;
- при log levels >100 глава предупреждает о появлении encrypted passwords в logs.

Rollback:
- вернуть прежний debug level;
- exact previous value должен быть записан до изменения, иначе [Needs confirmation].

## smb.conf — local authentication

~~~text
[global]
workgroup = ulsah
security = user
netbios name = freebsd-book
~~~

Account workflow:

~~~text
UNIX account exists
→ smbpasswd -a <user>
→ test authentication
~~~

## smb.conf — Active Directory authentication

~~~text
[global]
workgroup = ulsah
realm = ulsah.example.com
security = ads
dedicated keytab file = FILE:/etc/samba/samba.keytab
kerberos method = dedicated keytab
~~~

Keytab creation/rotation commands в этой главе: [Needs confirmation].

## smb.conf — simple share

~~~text
[bookshare]
path = /storage/bookshare
read only = no
~~~

## smb.conf — home shares

~~~text
[homes]
comment = Home Directories
browseable = no
valid users = %S
read only = no
~~~

valid users = %S ограничивает доступ владельцем соответствующего home share.

## smb.conf — project share

~~~text
[eng]
valid users = @eng
path = /home/eng
nt acl support = no
create mask = 0660
directory mask = 2770
force directory mode = 2000
force group = eng
browseable = no
read only = no
guest ok = no
~~~

Filesystem permissions должны соответствовать share policy.

## Network security

Source-supported configuration concepts:
- hosts allow = explicit clients/networks;
- hosts deny = explicit deny list;
- deny overrides allow.

Ports из главы:
- UDP 137–139;
- TCP 137, 139, 445.

Exact firewall command в главе не приведен: [Needs confirmation].

## Logging configuration

~~~text
[global]
log file = /var/log/samba.log.%m
max log size = 10000
syslog only = no
syslog = 7
~~~

Высокий log level не является default recommendation. Увеличивать verbosity только при активной диагностике и затем возвращать baseline.

## Character set configuration

Если server не использует UTF-8, глава приводит пример:

~~~text
unix charset = ISO8859-15
display charset = ISO8859-15
~~~

Перед изменением:

~~~bash
echo $LANG
~~~

Исправление уже существующих incorrectly encoded filenames: [Needs confirmation].
