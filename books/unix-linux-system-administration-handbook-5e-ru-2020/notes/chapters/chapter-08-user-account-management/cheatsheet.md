# Шпаргалка: управление учетными записями пользователей

Цель: управлять account lifecycle так, чтобы identity, authentication, groups, filesystem ownership и external directories оставались согласованными.

## 1. Модель учетной записи

Базовая identity в UNIX/Linux — UID.

~~~text
login name
   ↓
UID
   ↓
process ownership
file ownership
account lookup
backup/restore identity
~~~

Имя пользователя удобно человеку, но ownership и многие системные связи опираются на UID.

Критическое правило главы:

~~~text
не переиспользовать UID бывших пользователей
~~~

## 2. Основные локальные файлы

Linux:

~~~text
/etc/passwd   → public account attributes
/etc/shadow   → password hash + password/account aging
/etc/group    → groups + members
/etc/gshadow  → protected group credentials
~~~

FreeBSD:

~~~text
/etc/master.passwd
/etc/passwd
/etc/group
/etc/login.conf
~~~

При использовании LDAP/другой directory service локальные файлы могут быть только частью общей identity model.

## 3. Поля /etc/passwd

Семь полей:

~~~text
login : password-placeholder : UID : GID : GECOS : home : shell
~~~

Что помнить:

- login name должен быть unique;
- UID должен быть consistent across organization;
- primary GID задаёт default group;
- GECOS хранит descriptive information;
- home определяет пользовательскую среду;
- shell может быть любой login program, но обычно command interpreter.

## 4. Password storage

Password hash не должен находиться в world-readable `/etc/passwd`.

Linux:

~~~text
/etc/passwd → x placeholder
/etc/shadow → real hash
~~~

FreeBSD:

~~~text
/etc/passwd → * placeholder
/etc/master.passwd → protected credential data
~~~

Изменение hashing policy не перехеширует старые passwords автоматически.

Принудить смену:

~~~bash
chage -d 0 <user>
~~~

## 5. Shadow: lifecycle password/account

Ключевые поля `/etc/shadow`:

- login name;
- password hash;
- last password change;
- minimum age;
- maximum age;
- warning interval;
- inactive/grace period;
- account expiration;
- reserved field.

Важно различать:

~~~text
password expiration ≠ account expiration
~~~

## 6. UID и consistency

Глава рекомендует:

- real users — из non-system UID range;
- одинаковый UID должен означать того же человека на всех relevant hosts;
- UID не переиспользовать после offboarding;
- при large fleet — централизованный source of truth предпочтительнее ручной coordination.

Причина: backup, NFS и filesystem ownership часто видят UID, а не login name.

## 7. Groups

`/etc/group`:

~~~text
group-name : password-placeholder : GID : members
~~~

Практическая модель:

~~~text
primary group      → default group при создании files
supplementary      → additional access
project/role group → deliberate sharing
personal group     → restrictive default
~~~

Проверка FreeBSD example:

~~~bash
pw groupshow staff
~~~

Изменение:

~~~bash
sudo pw groupmod staff -m dan
~~~

## 8. Personal groups

Chapter рекомендует отдельную personal group для каждого пользователя, чтобы новые files случайно не становились group-shared.

Для intentional sharing создавайте отдельные shared groups.

## 9. Ручное создание account: правильный порядок

~~~text
1. account record
2. groups
3. initial password
4. home directory
5. startup files
6. ownership/mode
7. roles/privileges
8. login verification
9. administrative record
~~~

Для ручного редактирования:

~~~bash
vipw
vipw -s
vigr
vigr -s
~~~

Преимущество — locking и controlled update.

## 10. Initial password

~~~bash
sudo passwd <user>
~~~

Не оставлять новый account в состоянии, где первый login может быть перехвачен посторонним.

FreeBSD example:

~~~bash
sudo pw usermod raphael -w random
~~~

Random temporary password имеет смысл только при secure delivery и subsequent change.

## 11. Home directory

После создания home:

- deploy standard startup files;
- выставить ownership;
- проверить hidden files;
- проверить shell startup behavior.

~~~bash
sudo chown -R <user>:<group> ~<user>
~~~

После login новым пользователем:

~~~bash
pwd
ls -la
~~~

## 12. Опасный recursive chown

Не делать:

~~~text
chown -R user:group ~user/.*
~~~

Причина: pattern может включить `..` и затронуть parent directory.

Это один из главных filesystem-risk examples главы.

## 13. Startup files

Chapter упоминает типичные files:

- `.profile`;
- `.bashrc`;
- `.bash_profile`;
- `.login`;
- `.cshrc`;
- `.vimrc`.

Linux часто использует fragments under:

~~~text
/etc/profile.d/
~~~

Локальные defaults должны поддерживать usable environment, но user может переопределить свои files.

## 14. useradd

Read defaults:

~~~bash
useradd -D
~~~

Set default shell:

~~~bash
sudo useradd -D -s /bin/bash
~~~

Create account:

~~~bash
sudo useradd hilbert
~~~

Explicit example:

~~~bash
sudo useradd -c "David Hilbert" \
  -d /home/math/hilbert \
  -g hilbert \
  -G faculty \
  -m \
  -s /bin/tcsh \
  hilbert
~~~

Проверить:

- passwd/shadow records;
- groups;
- home;
- owner/group;
- shell.

## 15. adduser / newusers

`adduser` — higher-level onboarding wrapper в некоторых systems.

~~~bash
sudo adduser
~~~

`newusers` — bulk provisioning from prepared file.

Risk:

~~~text
input file contains initial password in plaintext
~~~

Такой input — sensitive temporary artifact.

## 16. Safe offboarding

Удаление account — не просто `userdel`.

Проверить и обработать:

- identity database records;
- mail aliases/forwarding;
- cron;
- at jobs;
- print jobs;
- running processes;
- groups;
- home/mail data;
- shared files;
- external calendars/services;
- mailing lists;
- administrative records.

До удаления data:

~~~text
preserve what the organization may still need
~~~

## 17. Orphaned files после удаления

После account removal:

~~~bash
sudo find <filesystem> -xdev -nouser
~~~

`-xdev` ограничивает scan одной filesystem.

Цель — найти files, owner UID которых больше не разрешается в user identity.

## 18. Lock ≠ delete

Temporary lock:

FreeBSD:

~~~bash
sudo pw lock <user>
~~~

Linux:

~~~bash
usermod -L <user>
usermod -U <user>
~~~

Но password lock блокирует только access paths, которые действительно зависят от password authentication.

Нужно проверить другие mechanisms отдельно.

## 19. PAM boundary

PAM централизует authentication policy для:

- `login`;
- `sudo`;
- `passwd`;
- `su`;
- других PAM-aware programs.

Если account tool ведёт себя не так, как ожидается по `login.defs` или local defaults, chapter советует проверить, не переопределяет ли policy PAM.

## 20. Centralized identity

Для medium/large organization chapter предпочитает centralized management.

Цели:

- globally unique UID/GID;
- consistent login names;
- rapid propagation of disable/delete;
- centralized password/authentication policy;
- auditable provisioning/deprovisioning.

## 21. LDAP / Active Directory

LDAP:

~~~text
centralized hierarchical repository
→ users / groups / attributes
→ multiple clients
→ organization-wide consistency
~~~

Active Directory использует LDAP + Kerberos и может участвовать в mixed Windows/UNIX environments.

## 22. SSO

Плюсы:

- меньше credentials;
- проще user experience;
- можно применять stronger centrally managed credentials.

Риски:

- compromise одного credential имеет больший blast radius;
- authentication service становится critical dependency;
- integration сложнее, чем сама идея SSO.

## 23. Identity management

Хорошая identity-management system должна помогать:

- provision/deprovision accounts;
- generate unique identities;
- map users ↔ privileges;
- implement RBAC;
- record admin actions;
- integrate with HR/business lifecycle;
- support global password change/reset;
- provide audit/reporting.

## 24. Минимальный operational workflow

~~~text
Need new identity
   ↓
verify authorization/policy
   ↓
allocate unique login + UID/GID
   ↓
create account + groups
   ↓
set credential
   ↓
create/configure home
   ↓
set ownership/roles
   ↓
login as user and verify
   ↓
record account in admin source of truth
~~~

Offboarding:

~~~text
disable first if needed
   ↓
preserve business data
   ↓
remove account references
   ↓
remove account
   ↓
find -xdev -nouser
   ↓
verify no orphan access/data
~~~

## Acceptance criteria

- login name/UID/GID mapping is unique and consistent;
- passwd/shadow/group records agree;
- initial account is not exposed through unset/weak credential flow;
- home ownership and startup files are verified;
- recursive ownership changes do not cross parent boundaries;
- group membership is intentional;
- new account passes real login verification;
- offboarding handles jobs/processes/mail/data, not only passwd entry;
- orphaned files are checked;
- password lock is not assumed to block every access path;
- centralized identity changes propagate according to expected scope;
- unknown rollback remains `[Needs confirmation]`.
