# Команды и конфигурационные точки главы 3

Таблица включает только команды, формы команд и конфигурационные механизмы, подтверждённые RAG главы 3. Команды, которые изменяют identity, пароли, `sudoers` или security policy, явно помечены как state-changing.

| Команда / механизм | Назначение | Что проверить | Тип |
|---|---|---|---|
| `ls -l <file>` | Посмотреть владельца, группу и mode файла | owner, group, permission bits | read-only |
| `/bin/su` или `/usr/bin/su` | Получить оболочку другого пользователя; без аргумента — root | в какой identity/context перешла оболочка | state-changing |
| `su - <user>` | Войти в login-like environment другого пользователя | окружение и воспроизводимость пользовательской сессии | state-changing |
| `exit` | Завершить `su`-сессию | возврат к исходной identity | state-changing |
| `echo $PATH` | Проверить PATH привилегированного пользователя | отсутствие `.` в PATH | read-only |
| `sudo <command>` | Выполнить разрешённую команду с повышенными или делегированными правами | кто, где, от кого и что запускается; journal/log | state-changing |
| `sudo -u <user> <command>` | Выполнить разрешённую команду от имени конкретного пользователя | target user и разрешённая команда | state-changing |
| `visudo` | Безопасно редактировать `sudoers` с блокировкой и syntax check | файл успешно проходит проверку | state-changing |
| `visudo -c -f newsudoers` | Проверить новый `sudoers` перед установкой | синтаксис приемлем для локального sudo | read-only |
| `scp ...` | Доставить централизованный `sudoers` на хост | источник файла и host key | state-changing |
| `hostname` | Получить имя хоста, которое sudo может использовать при matching | совпадает ли имя с sudoers policy | read-only |
| `sudo EDITOR=emacs vipw` | Пример явной передачи разрешённой переменной окружения в sudo-команду | ожидаемый editor и изменение password database | state-changing |
| `passwd -l root` | Заблокировать парольный вход root в Linux | root password hash становится непроходимым | state-changing |
| `sudo passwd -u root` | Разблокировать root account в приведённом примере Ubuntu | root account снова допускает парольный вход | state-changing |
| `semodule -d <module>` | Отключить SELinux policy module | нужный модуль отключён | state-changing |
| `yum install selinux-policy-mls` | Установить MLS policy package в Red Hat-среде | пакет установлен | state-changing |
| `audit2allow` | Создавать policy definitions на основе журналов нарушений SELinux | generated policy нужно проверять, покрытие может быть неполным | read-only / output-generating |

## Конфигурационные точки sudoers

Подтверждённые главой конструкции:

```text
User_Alias
Host_Alias
Cmnd_Alias
NOPASSWD
Defaults env_keep += "..."
Defaults requiretty
Defaults !requiretty
```

Логика matching: учитываются пользователь, хост, target user и команда. Если подходят несколько строк, глава указывает, что применяется последняя соответствующая строка.

### Правила безопасности sudo из главы

- Указывать команды полными путями.
- Редактировать `sudoers` через `visudo`.
- Держать типичную конфигурацию простой.
- Не считать отрицательные списки команд («ALL, кроме shell») настоящей security boundary.
- Избегать `NOPASSWD: ALL`; если passwordless действительно требуется, максимально ограничивать набор команд.
- С осторожностью расширять `env_keep`: окружение привилегированной команды — часть attack surface.
- При централизованной раздаче сначала проверить новый файл через `visudo -c -f`.
- Журнал sudo полезен для accountability, но не гарантирует полного аудита действий после выхода в дочернюю оболочку.

## SELinux / AppArmor reference

Подтверждённые конфигурационные элементы:

```text
/etc/selinux/config

SELINUX=enforcing
SELINUX=permissive
SELINUX=disabled
SELINUXTYPE=targeted
```

- `enforcing` — policy применяется и нарушения блокируются.
- `permissive` — нарушения допускаются, но журналируются; глава связывает это с отладкой и разработкой policy.
- `disabled` — SELinux выключен.
- AppArmor profiles находятся под `/etc/apparmor.d`.

## Rollback coverage

- `su` → `exit` явно даёт возврат из временной shell identity.
- `passwd -l root` ↔ `sudo passwd -u root` представлены как блокировка/разблокировка root account.
- Для изменения `sudoers` глава не даёт универсальной rollback-команды; защита — `visudo`, предварительная проверка и централизованный known-good файл.
- Для `semodule -d` обратная команда в RAG этой главы не приведена: `[Needs confirmation]`.
- Для изменения `SELINUX=` rollback зависит от исходного состояния: `[Needs confirmation]`.
