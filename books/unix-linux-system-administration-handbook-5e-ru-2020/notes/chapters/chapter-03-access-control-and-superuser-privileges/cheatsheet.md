# Шпаргалка: доступ, root и делегирование привилегий

Цель: предоставить ровно необходимые полномочия, сохранить accountability и не расширить security boundary больше, чем требуется.

## 1. Сначала определить, какая модель решает задачу

Базовые вопросы:

- Кто выполняет операцию: пользователь, группа, system account?
- Какой объект защищается: файл, процесс, устройство, сеть, daemon?
- Достаточно ли owner/group/mode?
- Нужна ли временная административная операция?
- Нужна ли аутентификация, более точный ACL, capability или централизованная policy?

Модель главы:

```text
DAC / owner-group
    ↓
root / setuid
    ↓
sudo delegation
    ↓
PAM / Kerberos / ACL / capabilities / namespaces
    ↓
LSM / MAC / RBAC
    ↓
SELinux / AppArmor
```

## 2. Проверить традиционные права

Read-only:

```bash
ls -l <file>
```

Смотреть: владелец, группа, permission bits.

Interpretation: ядро и filesystem оперируют числовыми UID/GID; имена пользователей и групп — удобочитаемое отображение этих идентификаторов.

## 3. Root — мощный, но слишком широкий механизм

Root определяется прежде всего эффективным UID 0. Традиционно такой процесс может выполнять почти все допустимые административные операции.

Глава предупреждает:

- не создавать дополнительные UID 0 accounts;
- не переименовывать root без веской причины;
- избегать постоянного прямого root login;
- минимизировать setuid-root программы;
- для менее доверенных/home filesystems рассматривать `nosuid` как средство отключения setuid/setgid semantics.

Rollback/verification для mount option в этой главе не приводятся: `[Needs confirmation]`.

## 4. Временный переход identity через su

```bash
/usr/bin/su
su - <user>
```

`su - <user>` полезна для воспроизведения login environment пользователя.

Завершение:

```bash
exit
```

Глава рекомендует оставлять `su` главным образом как аварийный резерв, а ежедневное делегирование строить через sudo.

## 5. sudo — основной operational path

Общий паттерн:

```bash
sudo <command>
sudo -u <user> <command>
```

Что даёт:

- делегирование конкретных действий без общего root shell;
- журнал пользователя, хоста, рабочего каталога, target user и команды;
- возможность централизованной policy;
- отзыв привилегий без смены root password.

### Изменение sudoers

```bash
visudo
```

Acceptance check: редактор завершился с валидным синтаксисом.

Для staged/central file:

```bash
visudo -c -f newsudoers
```

Только после успешной проверки файл должен становиться рабочим `sudoers`.

## 6. Правила sudo, которые легко сделать небезопасными

### Не строить security boundary как «ALL, кроме ...»

Глава показывает, что разрешённая привилегированная программа может дать непрямой путь к shell. Отрицательный command list — напоминание об intent, но не надёжная изоляция.

### Не использовать широкое NOPASSWD без необходимости

```text
NOPASSWD: ALL
```

В главе это прямо приводится как опасный вариант. Если passwordless execution неизбежно, ограничивать конкретными командами.

### Environment — часть boundary

sudo по умолчанию очищает environment. Дополнительные переменные добавлять консервативно через `env_keep`.

Пример:

```text
Defaults env_keep += "SSH_AUTH_SOCK"
```

## 7. Централизованный sudoers

Workflow главы:

```text
central known-good sudoers
        ↓
copy via authenticated channel
        ↓
visudo -c -f candidate
        ↓
install only if valid
```

Дополнительно:

```bash
hostname
```

помогает понять, с каким host string будет сопоставляться policy.

Риск: поддельный или синтаксически неверный `sudoers` может быстро лишить административного доступа.

## 8. Политика root account

Linux lock:

```bash
passwd -l root
```

Приведённый в главе unlock для Ubuntu:

```bash
sudo passwd -u root
```

Interpretation:

- блокировка пароля не уничтожает UID 0 и не мешает системным процессам работать как root;
- sudo продолжает работать;
- на физических системах настоящий root password может оставаться аварийным резервом при boot/hardware failure.

## 9. System accounts

Псевдопользователи позволяют отдельным сервисам владеть своими ресурсами без root.

Главные идеи:

- system accounts обычно имеют низкие UID;
- login для них должен быть отключён;
- `/bin/false` или `/bin/nologin` упоминаются как shell для блокировки интерактивного входа;
- account `nobody` не должен владеть файлами, иначе удалённые непривилегированные mappings смогут ими управлять.

## 10. Расширения базовой модели

### PAM

Отвечает на вопрос: «Как подтвердить, что это действительно пользователь X?»

Приложение вызывает PAM, а PAM выбирает configured authentication library. Это authentication framework, не полный access-control engine.

### Kerberos

Сетевой метод аутентификации с доверенной стороной: пользователь получает криптографическое доказательство identity для предъявления другим сервисам.

### ACL

Расширяют традиционный owner/group/other и позволяют назначать права нескольким users/groups.

### Linux capabilities

Разбивают полномочия root на отдельные разрешения. Пример главы: `CAP_NET_BIND_SERVICE` для privileged ports.

### Namespaces

Не столько принимают тонкое решение доступа, сколько скрывают от процесса часть объектов. Это один из базовых механизмов контейнерной изоляции.

## 11. MAC / RBAC / LSM

### LSM

Kernel API, позволяющий подключать альтернативные access-control mechanisms. В главе перечисляются SELinux, AppArmor и другие Linux-модули.

### DAC

Владелец объекта может сам делегировать права.

### MAC

Администратор задаёт централизованную policy, которая дополняет или переопределяет discretionary permissions. Хорошая MAC policy строится по least privilege.

### RBAC

Права назначаются ролям, роли — пользователям. Это добавляет слой косвенности и упрощает управление иерархиями полномочий.

## 12. SELinux

Файл верхнего уровня:

```text
/etc/selinux/config
```

Режимы:

```text
SELINUX=enforcing
SELINUX=permissive
SELINUX=disabled
```

Перед широким внедрением глава советует понимать logging и troubleshooting model.

`audit2allow` способен генерировать policy definitions из violation logs, но глава предупреждает, что автоматически полученный профиль может не покрыть все code paths.

## 13. AppArmor

Главная цель — ограничить ущерб от скомпрометированного приложения.

Свойства из главы:

- профиль специфичен для приложения;
- default-deny для защищаемого процесса;
- программы без профиля работают без дополнительного ограничения;
- profiles хранятся в `/etc/apparmor.d`;
- path-based модель делает policy читаемой, но hard links создают компромисс.

## Минимальная схема выбора

```text
Нужен доступ?
  ↓
Хватает owner/group?
  ├─ да → стандартные permissions
  └─ нет
       ↓
Нужна конкретная admin-команда?
  ├─ да → sudo + audit + exact command/path
  └─ нет
       ↓
Нужна authentication abstraction?
  ├─ PAM/Kerberos
Нужна fine-grained file policy?
  ├─ ACL
Нужна дробная root-привилегия?
  ├─ capabilities
Нужна isolation/visibility boundary?
  ├─ namespaces
Нужна централизованная mandatory policy?
  └─ MAC/RBAC → SELinux/AppArmor
```
