# Команды главы 5

Только команды и формы команд, подтверждённые RAG главы 5.

| Команда | Назначение | Что смотреть / проверять | Тип |
|---|---|---|---|
| `cd <dir>` | Перейти в промежуточный каталог и использовать относительный path | current directory/process context | state-changing |
| `sudo mount <device> <mountpoint>` | Присоединить filesystem к дереву | mount point и доступность content | state-changing |
| `mount` | Показать mounted filesystems | device/type/options/mount points | read-only |
| `mount /usr` | Использовать `/etc/fstab` для короткой формы mount | filesystem успешно смонтирована | state-changing |
| `umount <mountpoint>` | Демонтировать filesystem | отсутствие busy references | state-changing |
| `umount -l <mountpoint>` | Linux lazy unmount | namespace detached, references могут остаться | state-changing |
| `umount -f <mountpoint>` | Force unmount | high-risk; глава советует сначала найти holders | state-changing |
| `fuser -c <mountpoint>` | Найти PID, использующие filesystem | PIDs + access codes | read-only |
| `fuser -cv <mountpoint>` | Linux verbose view holders | user/PID/access/command | read-only |
| `ps ... <PID list>` | Идентифицировать процессы, найденные `fuser` | USER/PID/COMMAND | read-only |
| `lsof` | Показать open files и process ownership | process ↔ open file | read-only |
| `lsof -F` | Machine-friendly output | parseable open-file data | read-only |
| `file <path>` | Определить тип/format объекта | directory, executable и др. | read-only |
| `ls -ld <path>` | Посмотреть type/mode/owner/group для объекта или directory | first char + permissions + metadata | read-only |
| `ls -b` | Показать control chars в filename в escaped/octal form | сложные имена | read-only |
| `rm -- -f` | Удалить файл, имя которого начинается с `-` | удалён именно literal filename | state-changing |
| `rm -i <pattern>` | Удалять по pattern с подтверждением каждого файла | confirmation before each removal | state-changing |
| `mkdir <dir>` | Создать каталог | directory exists | state-changing |
| `rmdir <dir>` | Удалить пустой каталог | directory removed | state-changing |
| `rm -r <dir>` | Рекурсивно удалить непустой каталог | destructive recursive deletion | state-changing |
| `ln <old> <new>` | Создать hard link | одинаковый inode/link count | state-changing |
| `ln -s <target> <link>` | Создать symbolic link | literal target path | state-changing |
| `ls -li <path>` | Показать inode и hard-link count | inode number + link count | read-only |
| `find <mount> -xdev -inum <inode> -print` | Найти hard-link peers по inode | paths с тем же inode | read-only |
| `ls -l <path>` | Просмотреть mode, links, owner, group, size/time | permission bits и metadata | read-only |
| `chmod 711 myprog` | Установить octal permissions | owner rwx, others execute | state-changing |
| `chmod -R g+w mydir` | Рекурсивно добавить group write | только требуемый bit изменён | state-changing |
| `find mydir -type f -exec chmod a-x {} ';'` | Убрать execute только у regular files | directories не затронуты | state-changing |
| `chmod --reference=filea fileb` | Linux: скопировать mode с reference file | fileb mode соответствует filea | state-changing |
| `sudo chown -R matt <path>` | Рекурсивно изменить owner | ownership tree | state-changing |
| `sudo chgrp -R staff <path>` | Рекурсивно изменить group | group ownership tree | state-changing |
| `sudo chown -R matt:staff <path>` | Рекурсивно изменить owner и group | обе identity fields | state-changing |
| `umask 027` | Изменить default permission mask процесса/shell | permissions новых files | state-changing |
| `lsattr <file>` | Linux: посмотреть filesystem flags | append-only/immutable и др. | read-only |
| `chattr ... <file>` | Linux: изменить filesystem flags | new flags | state-changing |
| `chattr -ia <file>` | Снять immutable/append-only flags в приведённом предупреждении | flags removed | state-changing |
| `touch example` | Создать тестовый файл | file exists | state-changing |
| `getfacl <file>` | Просмотреть POSIX ACL | user/group/mask/other entries | read-only |
| `getfacl --omit-header <file>` | Linux: ACL без header comments | ACL entries | read-only |
| `getfacl -q <file>` | FreeBSD: compact ACL output | ACL/ACE entries | read-only |
| `getfacl -qv <file>` | FreeBSD NFSv4 ACL с long permission names | ACE permissions/flags/type | read-only |
| `setfacl -m <entries> <file>` | Добавить/изменить ACL entries | generated/effective mask | state-changing |
| `setfacl -n ...` | Не пересчитывать ACL mask автоматически | mask остаётся заданной вручную | state-changing |
| `setfacl -bn <file>` | Удалить ACL и вернуться к traditional permissions | ACL removed/minimal state | state-changing |
| `setfacl -dm <entries> <dir>` | Установить default ACL inheritance entries | defaults у новых children | state-changing |
| `setfacl -a <position> <entry> <file>` | FreeBSD NFSv4: вставить ACE в заданную позицию | ACE ordering | state-changing |
| `getfacl -q file > /tmp/file.acl` | Сохранить текущий NFSv4 ACL в текстовый файл | backup copy | read-only/output-generating |
| `vi /tmp/file.acl` | Отредактировать сохранённый ACL | desired ACE list | state-changing |
| `setfacl -b -M /tmp/file.acl file` | Заменить ACL содержимым файла | final ordered ACL | state-changing |

## Ключевые semantics

### Traditional mode

~~~text
owner   group   other
 rwx     rwx     rwx

4 = read
2 = write
1 = execute
~~~

Для directory:

- `r` — получить list entries;
- `x` — проход/search;
- `w+x` — создавать, удалять и переименовывать entries.

Удаление/rename regular file определяется permissions parent directory, потому что filename хранится в directory.

### Special bits

- setuid = octal 4000;
- setgid = 2000;
- sticky = 1000.

Setgid на directory заставляет новые files наследовать group directory. Sticky на directory ограничивает delete/rename владельцем directory, владельцем file или root.

## Safety / rollback

- Перед force/lazy unmount сначала использовать `fuser`/`lsof`; глава описывает half-unmounted state как потенциально семантически проблемный.
- `rm`, `rm -r`, recursive `chmod/chown/chgrp` — destructive/state-changing. Универсального rollback в главе нет: `[Needs confirmation]`.
- Не использовать recursive `chown .../.*`: pattern может захватить `..` и изменить parent tree.
- Для `chmod -R` помнить: execute имеет разные semantics для file и directory; при необходимости фильтровать regular files через `find`.
- Перед сложным NFSv4 ACL change глава показывает export через `getfacl -q > file.acl`; сохранённый ACL можно использовать как known-good source для восстановления.
- ACL и mode взаимосвязаны: `chmod` на file с extended ACL может изменить ACL mask и effective rights.
