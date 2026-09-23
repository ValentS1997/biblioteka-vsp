# Команды главы 16

Только команды и формы команд, подтвержденные RAG главы 16.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| dig <name> <type> | Запрос DNS resource record | ANSWER/AUTHORITY, status, flags, returned RR | read-only |
| dig @<server> <name> <type> | Запросить конкретный DNS server | authoritative/non-authoritative answer и распространение изменений | read-only |
| dig +trace <name> | Показать iterative resolution от root вниз | delegation chain и сервер, где цепочка ломается | read-only |
| dig -x <address> | Reverse lookup | PTR/reverse-zone result | read-only |
| dig +norecurse @<server> <name> NS | Увидеть, что конкретный server знает без recursion | delegation/authoritative data | read-only |
| dig <name> NS | Получить name servers домена | NS set | read-only |
| drill -T <name> | Проследить DNS resolution от root | referral/delegation chain | read-only |
| drill -s -k <keyfile> <name> SOA | Проследить DNSSEC signatures к root | chain of trust | read-only |
| delv <name> | DNSSEC-aware lookup/validation tool | DNSSEC validation chain/result | read-only |
| nslookup | Простой DNS query tool | returned name/address data | read-only |
| host | Простой DNS query tool | returned name/address data | read-only |
| rndc status | Показать status демона named | daemon state | read-only |
| rndc reload | Перечитать named.conf и reload zone files | static-zone changes loaded; SOA serial was updated beforehand | state-changing |
| rndc reload <zone> | Reload одной зоны | only intended zone reloaded | state-changing |
| rndc reconfig | Перечитать configuration и загрузить новые zones | newly added zone becomes known without reloading existing zones | state-changing |
| rndc freeze <zone> | Остановить dynamic updates и синхронизировать journal с zone file | zone frozen before manual edit | state-changing |
| rndc thaw <zone> | Reload zone file и снова принимать dynamic updates | dynamic updates resume | state-changing |
| rndc flush | Очистить caches | cached data removed | state-changing |
| rndc trace | Увеличить BIND debug level | debug output increases | workload-generating |
| rndc notrace | Отключить runtime debugging | debug output stops | state-changing |
| rndc querylog | Переключить query logging | query log starts/stops; disk usage | workload-generating |
| rndc dumpdb | Записать database/cache dump | large named_dump.db created | workload-generating |
| rndc stats | Записать statistics | named.stats written | workload-generating |
| rndc stop | Сохранить pending updates и остановить named | daemon stopped cleanly | state-changing |
| sudo named -d2 | Запустить named с debug level 2 | named.run; file can grow quickly | workload-generating |
| sudo named -u 53 | Запустить named и drop privileges to UID 53 после privileged initialization | daemon runs under intended UID | state-changing |
| nsupdate | Выполнять dynamic DNS updates interactively/batch | intended RR additions/removals only | state-changing |
| nsupdate -k <keydir>:<keyfile> | Dynamic update с key-based authentication | correct key and authorized update scope | state-changing |
| rndc-confgen -a | Сгенерировать local rndc authentication key | key file/permissions and matching named/rndc config | state-changing |
| dnssec-keygen ... | Генерировать TSIG/DNSSEC key material | algorithm, purpose, generated .key/.private files | state-changing |
| dnssec-signzone ... | Подписать zone и создать signed copy | SOA serial behavior, signatures, signed output file | state-changing |
| sudo rndc reconfig | Reload BIND configuration after switching to signed zone | signed zone configuration loaded | state-changing |
| sudo rndc flush | Очистить cache after DNSSEC configuration change | stale cached state removed | state-changing |

## Read-only baseline

Resolver/client:

~~~text
/etc/resolv.conf
/etc/nsswitch.conf
~~~

Query examples:

~~~bash
dig example.com A
dig example.com NS
dig -x 192.0.2.1
dig +trace example.com
dig @ns.example.com example.com SOA
rndc status
~~~

dig and drill use the name servers from /etc/resolv.conf unless @server is supplied.

## Static master-zone change

Source-supported flow:

~~~text
edit master zone data
→ increment SOA serial
→ rndc reload
→ query master/slaves or local/remote servers with dig
~~~

If forward data changes, remember the reverse zone when applicable. If SOA serial is not increased, slaves do not learn the changed data.

Exact universal rollback command: [Needs confirmation].

## Dynamic zone manual edit

Do not edit a dynamically updated zone directly.

~~~bash
rndc freeze <zone>
# edit zone file
rndc thaw <zone>
~~~

freeze synchronizes the journal into the master file and disables dynamic updates; thaw reloads the file and resumes updates.

## Dynamic update

~~~bash
nsupdate -k <keydir>:<keyfile>
~~~

The chapter warns that dynamic update is dangerous and recommends cryptographic authentication rather than source-IP trust.

Rollback for an arbitrary dynamic update: [Needs confirmation].

## BIND reload vs reconfig

~~~text
rndc reload
→ reread named.conf + reload existing zone files

rndc reload <zone>
→ reload only named zone

rndc reconfig
→ reread config and load new zones without reloading existing zones
~~~

## Debugging workload

~~~bash
rndc trace
rndc notrace
rndc querylog
rndc dumpdb
rndc stats
sudo named -d2
~~~

Risks from the chapter:
- debug output can grow rapidly;
- query logging is high-volume on active servers;
- database dump can be very large.

## DNSSEC

Key generation and signing are modifying operations because they create or replace key/signature files.

~~~text
dnssec-keygen
→ .key + .private

dnssec-signzone
→ signed zone copy with RRSIG + NSEC/NSEC3

named.conf zone file → signed file
→ rndc reconfig
→ rndc flush
~~~

Exact rollback procedure for a signed production zone: [Needs confirmation].
