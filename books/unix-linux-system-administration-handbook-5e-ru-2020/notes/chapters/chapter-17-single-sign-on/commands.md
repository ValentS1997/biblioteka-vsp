# Команды главы 17

Только команды и формы команд, подтвержденные RAG главы 17.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| slapd | Запустить демон OpenLDAP без аргументов после подготовки конфигурации | daemon starts with intended server configuration | state-changing |
| ldapsearch -h <host> -p 389 -x -D "<bind-DN>" -W -b "<baseDN>" "<filter>" | Выполнить LDAP query из примера главы | ожидаемые LDAP entries/attributes в LDIF | read-only |
| sudo realm join --user=<user> <AD-DOMAIN> | Присоединить Linux-систему к Active Directory realm | join completed; затем realm list | state-changing |
| realm list | Показать сконфигурированные realms | realm-name, configured membership, client software | read-only |
| kinit <principal>@<REALM> | Получить Kerberos ticket | ticket creation; затем klist | state-changing |
| klist | Показать Kerberos ticket cache | principal, validity interval, service principal | read-only |
| kdestroy | Аннулировать Kerberos ticket | ticket removed | state-changing |
| net ads join -U <user> | Присоединить систему к AD через Samba tools | сообщение Joined ... to domain ... | state-changing |
| getent passwd | Проверить NSS user lookup из всех configured sources | локальные и directory users присутствуют в выводе | read-only |
| rsync -gopt -e ssh /etc/passwd /etc/shadow <host>:/etc | Скопировать passwd/shadow на удаленный хост | целевые файлы изменены ожидаемо; права/владельцы/mtime сохранены | state-changing |

## LDAP query

Пример структуры запроса из главы:

~~~bash
ldapsearch -h atlantic.atrust.com -p 389   -x -D "cn=trent,cn=users,dc=boulder,dc=atrust,dc=com" -W   -b "cn=users,dc=boulder,dc=atrust,dc=com" "cn=ned*"
~~~

В примере:
- server и port задают endpoint LDAP;
- bind DN задает identity для запроса;
- baseDN задает точку начала поиска;
- filter ограничивает найденные записи;
- вывод формируется в LDIF.

Из-за несовпадения пояснения одного password flag с фактической строкой примера в RAG здесь сохраняется именно форма команды, показанная в примере, без дополнительной реконструкции.

## Linux + Active Directory

До state-changing join глава требует проверить:
- realmd установлен;
- sssd установлен;
- ntpd установлен и работает;
- AD domain name известен и корректен;
- используемая AD account имеет право присоединять систему.

Изменение:

~~~bash
sudo realm join --user=<user> <AD-DOMAIN>
~~~

Проверка:

~~~bash
realm list
~~~

Rollback/leave command в RAG главы не приведена: [Needs confirmation].

## Kerberos test

Предусловия для показанного FreeBSD flow:
- корректный FQDN присутствует в /etc/hosts;
- NTP настроен и работает;
- /etc/krb5.conf содержит нужный realm/KDC mapping.

Получение ticket:

~~~bash
kinit administrator@<REALM>
~~~

Проверка:

~~~bash
klist
~~~

Удаление локального ticket:

~~~bash
kdestroy
~~~

kdestroy отменяет ticket cache, но не является rollback присоединения системы к домену.

## Domain join через net ads

После успешного Kerberos test:

~~~bash
net ads join -U <user>
~~~

Source-supported acceptance check: команда должна вывести успешное присоединение к domain.

Rollback command: [Needs confirmation].

## NSS verification

После настройки nsswitch.conf с источником sss:

~~~bash
getent passwd
~~~

Ожидание: вывод содержит пользователей из configured NSS sources, включая directory accounts.

## OpenLDAP

Глава показывает server configuration через slapd.conf и client defaults через ldap.conf. После подготовки server configuration демон может быть запущен без аргументов:

~~~bash
slapd
~~~

Команда запускает сервис и потому является state-changing.

Точная команда остановки/rollback в главе не приведена: [Needs confirmation].

## rsync legacy distribution

Показанная команда:

~~~bash
rsync -gopt -e ssh /etc/passwd /etc/shadow lollipop:/etc
~~~

Effect:
- изменяет authentication-related files удаленного хоста;
- сохраняет permissions, ownership IDs и modification time согласно описанию главы;
- использует ssh как transport.

Risk:
- схема требует настройки sshd так, чтобы запуск не требовал пароля;
- глава прямо предупреждает, что это нарушает правила безопасности.

Rollback:
- [Needs confirmation].
