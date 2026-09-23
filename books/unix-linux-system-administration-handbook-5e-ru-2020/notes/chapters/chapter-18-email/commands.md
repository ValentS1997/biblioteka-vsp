# Команды главы 18

Только команды и формы команд, подтвержденные RAG главы 18.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| telnet <mail-host> 25 | Открыть SMTP session для ручной диагностики | banner, EHLO/HELO response, SMTP codes | workload-generating |
| telnet <submission-host> 587 | Проверить submission endpoint/MSA | banner, SMTP extensions/auth behavior | workload-generating |
| newaliases | Перестроить hash database aliases после изменения файла | ошибки форматирования отсутствуют; alias DB обновлена | state-changing |
| mailq | Показать mail queue | queue IDs, age, sender/recipient, deferred reason | read-only |
| mailq -Aa | Показать client submission queue sendmail | client queue state | read-only |
| sendmail -d0.1 -bt < /dev/null | Показать версию/compile options и базовую identity sendmail | version, compiled features, system identity | read-only |
| sendmail -bv <address> | Проверить mail address без отправки | address resolution/result | read-only |
| sendmail -q | Немедленно обработать sendmail queue | delivery attempts and queue reduction | workload-generating |
| sendmail -q -v | Обработать queue с подробным выводом | per-message delivery result | workload-generating |
| sudo kill -HUP <sendmail-pid> | Заставить running sendmail перечитать конфигурацию через restart/exec behavior | process returns with intended config | state-changing |
| sudo chroot /jail /usr/sbin/sendmail -bd -q30m | Запустить sendmail daemon в chroot из примера главы | jail files/config complete; daemon listens/queue runner works | state-changing |
| exim -bv | Проверить syntax errors конфигурации | parser reports no syntax errors | read-only |
| exim -bp | Показать Exim mail queue | queued messages and reasons | read-only |
| exim -bt <address> | Тестировать address routing | router/address result | read-only |
| exim -q | Запустить Exim queue runner | attempted deliveries/retries | workload-generating |
| exiqgrep | Искать сообщения в Exim queue | intended queue matches | read-only |
| exiqsumm | Сводка Exim queue | queue distribution | read-only |
| exiwhat | Показать running Exim processes | process roles/state | read-only |
| exigrep | Искать по Exim main log | message history/errors | read-only |
| eximstats | Получить statistics из Exim log | aggregate mail statistics | read-only |
| postconf | Показать текущие Postfix parameters | effective configuration | read-only |
| postconf <parameter> | Показать значение одного Postfix parameter | intended effective value | read-only |
| postconf -d <parameter> | Показать default value параметра | compare default vs configured | read-only |
| postconf -n | Показать только non-default Postfix settings | local configuration delta | read-only |
| postconf -m | Показать supported lookup-table types | intended map type available | read-only |
| sudo postmap hash:/etc/postfix/access | Скомпилировать lookup table | binary map rebuilt without errors | state-changing |
| postmap -q <key> hash:/etc/postfix/access | Запросить lookup table | expected lookup result | read-only |
| postalias | Создать/модифицировать alias table | exact action/arguments depend on invocation | state-changing |
| postcat | Показать contents of Postfix queue file | queued message metadata/content | read-only |
| postsuper | Управлять Postfix queues | exact subcommand effect must be known before use | state-changing |
| sudo qshape deferred | Показать age/domain distribution deferred queue | queue concentration by destination and age | read-only |

## SMTP manual check

SMTP/ESMTP uses text commands, so chapter allows direct interactive diagnostics:

~~~text
telnet <server> 25
EHLO <client-name>
MAIL FROM:<sender>
RCPT TO:<recipient>
DATA
...
.
QUIT
~~~

Risk:
- MAIL/RCPT/DATA can create a real delivery attempt;
- use only when intentional;
- exact rollback for a submitted SMTP message: [Needs confirmation].

Response interpretation:
- 2xx — success;
- 4xx — temporary failure;
- 5xx — permanent failure;
- extended DSN uses X.X.X format.

## Aliases

After editing the aliases file:

~~~bash
newaliases
~~~

Source warning: retain/report its error output when automated because formatting errors can occur.

Aliases that deliver to files or programs are security-sensitive.

Rollback of alias changes: [Needs confirmation].

## sendmail

Read-only diagnostics:

~~~bash
/usr/sbin/sendmail -d0.1 -bt < /dev/null
sendmail -bv <address>
mailq
mailq -Aa
~~~

Queue processing:

~~~bash
sendmail -q
sendmail -q -v
~~~

These commands generate delivery attempts and therefore workload/network side effects.

Configuration reload path from the chapter:
- sendmail reads sendmail.cf at start;
- after config change, restart it or send HUP;
- exact safe service-manager command is not supplied: [Needs confirmation].

Queue risks:
- queue filesystem can fill;
- stuck/deferred mail can accumulate;
- do not place queue and logs in the same filesystem partition according to the chapter guidance.

## Exim

Read-only:

~~~bash
exim -bv
exim -bp
exim -bt <address>
exiqgrep
exiqsumm
exiwhat
exigrep
eximstats
~~~

Queue run:

~~~bash
exim -q
~~~

This triggers delivery/retry work.

Exact rollback for Exim configuration: [Needs confirmation].

## Postfix

Configuration inspection:

~~~bash
postconf
postconf <parameter>
postconf -d <parameter>
postconf -n
postconf -m
~~~

Lookup table:

~~~bash
sudo postmap hash:/etc/postfix/access
postmap -q <key> hash:/etc/postfix/access
~~~

Queue inspection:

~~~bash
mailq
sudo qshape deferred
~~~

Utilities explicitly listed by the chapter:
- postalias — alias tables;
- postcat — queue-file inspection;
- postconf — main.cf inspection/editing;
- postfix — starts/stops mail system;
- postmap — lookup tables;
- postsuper — queue administration.

Where the source does not provide an exact state-changing subcommand, do not invent it: [Needs confirmation].

## Postfix soft bounce

soft_bounce=yes is a configuration test mode, not a command.

Effect:
- permanent failures are treated as temporary;
- delivery is retried instead of immediately losing legitimate mail during testing.

Critical source warning:
- disable it after testing, otherwise rejected mail continues retrying.

Rollback/change command: [Needs confirmation].
