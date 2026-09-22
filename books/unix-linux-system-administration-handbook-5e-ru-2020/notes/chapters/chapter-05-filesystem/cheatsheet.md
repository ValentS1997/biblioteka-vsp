# Шпаргалка: файловая система

Цель: понимать, какой именно слой filesystem изменяется, и проверять effective state после каждой операции.

## 1. Модель главы

Файловая система состоит из четырёх компонентов:

- namespace;
- API;
- security model;
- implementation.

UNIX использует единое дерево от `/`, а отдельные filesystems присоединяются в mount points.

## 2. Path: абсолютный или относительный

~~~text
/var/log/app.log     absolute
book5/filesystem     relative
~~~

Relative path интерпретируется относительно current directory процесса.

Если полный path превышает kernel path limit, глава предлагает перейти через `cd` в промежуточный directory и использовать shorter relative path.

## 3. Mount: сначала read-only evidence

Посмотреть существующие mounts:

~~~bash
mount
~~~

Обычная операция:

~~~bash
sudo mount <device> <mountpoint>
~~~

Важная semantics: существующее содержимое mount point временно скрывается mounted filesystem.

`/etc/fstab` задаёт filesystems для boot/check/mount и документирует disk layout.

### Busy filesystem

Перед `umount`:

~~~bash
fuser -cv <mountpoint>
lsof
~~~

Затем идентифицировать holder processes.

Глава не рекомендует сразу переходить к:

~~~bash
umount -l ...
umount -f ...
~~~

Lazy unmount может оставить half-detached state; force unmount следует рассматривать только после понимания holders.

## 4. Не перестраивать системное дерево без причины

Глава предупреждает о hidden dependencies. Для system packages предпочтительно оставлять default location.

Ориентиры:

- `/etc` — critical config/system files;
- `/bin`, `/sbin` — important utilities;
- `/lib`, `/lib64` — libraries;
- `/usr` — большинство standard programs/docs/libraries;
- `/var` — variable/growing state;
- `/tmp` — temporary files;
- `/dev` — device namespace, обычно virtual filesystem.

## 5. Тип объекта

~~~bash
file <path>
ls -ld <path>
~~~

Традиционные file types главы:

- regular;
- directory;
- character device;
- block device;
- local socket;
- FIFO;
- symbolic link.

Первый символ `ls -l` кодирует type.

## 6. Сложные filenames

Если filename начинается с `-`:

~~~bash
rm -- -f
~~~

Для control characters:

~~~bash
ls -b
rm -i <pattern>
~~~

`-i` особенно важен, потому что wildcard может match больше одного файла.

## 7. Hard link vs symbolic link

### Hard link

~~~bash
ln oldfile newfile
~~~

- дополнительное имя того же inode/object;
- shared data и attributes;
- не пересекает filesystem boundary;
- data blocks освобождаются после удаления последней hard link.

Проверка:

~~~bash
ls -li <path>
find <mount> -xdev -inum <inode> -print
~~~

### Symbolic link

~~~bash
ln -s <target> <link>
~~~

- отдельный filesystem object;
- хранит target как literal string;
- может пересекать filesystem boundary;
- может указывать на несуществующий target;
- permissions, показываемые для symlink, не управляют target access.

## 8. Traditional permissions

~~~text
u = owner
g = group
o = other
a = all

r = 4
w = 2
x = 1
~~~

Просмотр:

~~~bash
ls -l <file>
ls -ld <dir>
~~~

Изменение:

~~~bash
chmod 711 myprog
chmod u+w <file>
chmod g=u <file>
~~~

Главная ловушка: permissions directory != permissions regular file.

Для directory execute = search/traverse. Delete/rename file контролируется directory permissions.

## 9. Recursive chmod — применять выборочно

Опасный широкий вариант:

~~~bash
chmod -R ...
~~~

Глава предлагает для ordinary files фильтровать через `find`:

~~~bash
find mydir -type f -exec chmod a-x {} ';'
~~~

Acceptance check: directory traverse bits не были случайно удалены.

## 10. Owner / group

~~~bash
chown <user> <file>
chgrp <group> <file>
chown <user>:<group> <file>
~~~

Recursive example:

~~~bash
sudo chown -R matt <restore-tree>
sudo chgrp -R staff <restore-tree>
~~~

Anti-pattern главы:

~~~text
chown -R user <home>/.*
~~~

Pattern включает `..` и может затронуть parent directory.

## 11. umask

~~~bash
umask 027
~~~

`umask` — process attribute, inherited by child commands; он убирает bits из permissions, запрошенных creating program.

Глава отмечает typical default `022`, но это не enforced security policy: пользователь может изменить свой umask.

## 12. Linux filesystem flags

Read-only:

~~~bash
lsattr <file>
~~~

Change:

~~~bash
chattr ... <file>
~~~

Глава перечисляет append-only, immutable, no-atime и filesystem-specific flags.

Особое предупреждение: не использовать immutable flag как способ бороться с configuration-management tool. Исправлять нужно configuration management, а не создавать скрытую protection layer.

## 13. POSIX ACL

Просмотр:

~~~bash
getfacl <file>
~~~

Изменение:

~~~bash
setfacl -m <entries> <file>
~~~

Основные сущности:

- `user::`;
- named `user:<name>`;
- `group::`;
- named `group:<name>`;
- `mask::`;
- `other::`.

### ACL mask

Для extended ACL mode bits group-field соответствуют mask, а не обязательно `group::`.

Mask = верхний предел effective rights для named users/groups и owning group.

Поэтому `ls -l` может не показать фактические effective rights полностью.

Удаление ACL:

~~~bash
setfacl -bn <file>
~~~

Default ACL inheritance:

~~~bash
setfacl -dm <entries> <dir>
~~~

Важно: copied defaults не создают постоянной parent-child связи; later parent change не обновляет уже существующие children.

## 14. NFSv4 ACL

В главе NFSv4 ACL рассматриваются на FreeBSD.

Отличия:

- allow/deny ACE;
- более детальные permissions;
- special principals `owner@`, `group@`, `everyone@`;
- order ACE имеет значение;
- inheritance flags назначаются каждой ACE;
- нет POSIX-style mask;
- inherited ACE копируется, а не остаётся динамически linked с parent.

Просмотр:

~~~bash
getfacl -q <file>
getfacl -qv <file>
~~~

Вставка ACE в конкретную позицию:

~~~bash
setfacl -a <position> <entry> <file>
~~~

Для сложного изменения глава показывает safer workflow:

~~~bash
getfacl -q file > /tmp/file.acl
vi /tmp/file.acl
setfacl -b -M /tmp/file.acl file
~~~

Сохранённый ACL — useful rollback/reference point.

## 15. Минимальный operational flow

~~~text
Что изменяем?
    ↓
path / mount / type / link / mode / owner / flag / ACL
    ↓
read-only inspection
    ↓
понять effective semantics
    ↓
одно controlled change
    ↓
повторный ls/getfacl/mount/fuser
    ↓
keep or rollback/reference restore
~~~

## Acceptance criteria

- layer операции идентифицирован;
- busy filesystem исследована до force unmount;
- hard/symlink semantics не перепутаны;
- recursive changes ограничены необходимым scope;
- после permission change проверены owner/group/mode;
- при ACL проверены mask/effective rights;
- перед сложным NFSv4 ACL edit сохранён current ACL;
- неизвестный rollback помечен `[Needs confirmation]`.
