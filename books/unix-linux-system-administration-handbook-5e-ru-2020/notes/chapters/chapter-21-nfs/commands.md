# Команды главы 21

Только команды и формы команд, подтвержденные RAG главы 21.

## Read-only / observation

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| showmount -e <server> | Показать exports сервера для NFSv2/v3 | нужный path и client visibility | read-only |
| exportfs -v | Показать активные Linux exports локально | path, clients, export options | read-only |
| df <mountpoint> | Показать capacity смонтированной NFS filesystem | mount доступен и отвечает | read-only |
| fuser <mountpoint> | Найти процессы, использующие mount | кто блокирует umount | read-only |
| lsof <mountpoint> | Найти открытые файлы/processes | кто удерживает filesystem | read-only |
| nfsstat | Общая NFS statistics | errors/retrans/timeouts по версиям | read-only |
| nfsstat -s | Server-side NFS statistics | server calls/errors | read-only |
| nfsstat -c | Client-side NFS statistics | retrans, badxid, timeout и операции | read-only |
| netstat | Дополнительная network statistics | network symptoms совместно с nfsstat | read-only |
| ps | Наблюдать состояния nfsd threads/processes | частое состояние D как один из сигналов | read-only |
| uptime | Проверить load average при tuning nfsd | не ухудшилась ли load после изменения thread count | read-only |
| automount -L | Dry-run проверки automount configuration | parsing/config problems без применения | read-only |

Ограничение: showmount относится к традиционной модели NFSv2/v3. Для NFSv4 глава прямо указывает, что корректного remote-equivalent discovery через showmount нет.

## Apply server exports

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| exportfs -a | Перечитать /etc/exports в Linux | exportfs -v и client access | state-changing |
| service nfsd restart | Перезапустить NFS server во FreeBSD | service вернулся; export доступен | state-changing |
| service mountd reload | Перечитать mountd после изменения FreeBSD exports для v3 clients | v3 export visibility восстановлена | state-changing |
| service mountd restart | Перезапустить mountd после изменения параметров FreeBSD nfsd | mount service восстановлен | state-changing |
| systemctl restart nfs-config.service nfs-server.service | Применить Linux nfsd configuration changes | services restarted; NFS доступен | state-changing |

Rollback:
- вернуть предыдущий /etc/exports или nfsd config;
- повторно применить reload/restart;
- если предыдущая версия конфигурации не сохранена: [Needs confirmation].

## Client mount / unmount

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo mount -o rw,hard,intr,bg <server>:/<path> <mountpoint> | Смонтировать NFSv2/v3 export | access mode, failure semantics, mount works | state-changing |
| sudo mount -o rw,hard,intr,bg <server>:/ <mountpoint> | Смонтировать NFSv4 pseudoroot в Linux | exported hierarchy visible | state-changing |
| sudo mount -t nfs -o nfsv4 <server>:/ <mountpoint> | Смонтировать NFSv4 во FreeBSD | mount active and hierarchy accessible | state-changing |
| mount <server>:/ <mountpoint> | Упрощенная форма, когда wrapper определяет NFS | expected version negotiated | state-changing |
| mount -a -t nfs | Применить NFS entries из /etc/fstab | все ожидаемые NFS mounts доступны | state-changing |
| umount <mountpoint> | Штатно размонтировать NFS filesystem | filesystem больше не используется | state-changing |
| umount -f <mountpoint> | Принудительно размонтировать при недоступном server/безвыходной ситуации | mount удален; application impact оценен | state-changing |

Перед umount -f:
1. проверить fuser/lsof;
2. устранить active users/processes, если возможно;
3. использовать force только как крайний вариант.

Rollback после mount change:
- umount нового mount;
- вернуть предыдущую fstab entry;
- если active I/O уже нарушено: [Needs confirmation].

## Mount options из главы

| Опция | Эффект | Риск/проверка |
|---|---|---|
| rw | read-write mount | server export должен разрешать запись |
| ro | read-only mount | проверить, что write действительно запрещен |
| bg | retries mount в фоне | mount может появиться позже |
| hard | operations ждут возвращения server | процессы могут зависать при outage |
| soft | после retry/timeouts возвращается ошибка | меняет failure semantics application |
| intr | позволяет прервать blocked operation | проверить поведение клиента |
| retrans=n | число retries перед ошибкой для soft | tuning только по evidence |
| timeo=n | request timeout | tuning только по nfsstat evidence |
| rsize=n | read buffer size | workload-specific tuning |
| wsize=n | write buffer size | workload-specific tuning |
| sec=<mode> | security mode | соответствует server export policy |
| nfsvers=n | explicit NFS version | client/server support |
| proto=tcp | transport | NFSv4 использует TCP |

Не представлять rsize/wsize/timeo как универсальные рекомендации.

## Linux /etc/exports — configuration actions

Пример, подтвержденный главой:

~~~text
/home  *.users.admin.com(rw)  172.17.0.0/24(ro)
~~~

После изменения:

~~~bash
exportfs -a
exportfs -v
~~~

Safety:
- client specification должна быть explicit;
- export без clients открывает mount всем hosts;
- не вставлять пробел между client и его (options), если он меняет semantics;
- no_root_squash — опасная опция;
- async может ответить до записи на disk и повредить данные при crash.

## FreeBSD /etc/exports — configuration actions

Примеры из главы:

~~~text
/var/www -ro,alldirs www*.admin.com
/var/www -alldirs,sec=krb5p -network 2001:db8::/32
V4:/exports -network 10.0.0.0 -mask 255.255.255.0
/exports/www -network 10.0.0.0 -mask 255.255.255.0
~~~

После изменения:

~~~bash
service nfsd restart
service mountd reload
~~~

Для NFSv4 не назначать локальный / как V4 root: источник предупреждает об exposure всей root filesystem.

## nfsd configuration / tuning

Для отключения старой версии глава поддерживает option form:

~~~text
-N 2 -N 3
~~~

Она добавляется в соответствующую server configuration, затем services restart.

Количество nfsd threads:
- меняется через system-specific config;
- exact numeric value не является универсальным;
- наблюдать ps, uptime, nfsstat;
- rollback = вернуть прежнее thread count.

## Identity mapping

Linux:
- daemon: /usr/sbin/rpc.idmapd
- config: /etc/idmapd.conf

FreeBSD:
- daemon: /usr/sbin/nfsuserd
- flags: nfsuserd_flags в /etc/rc.conf

Глава требует одинаковый NFS domain между участниками NFSv4. Exact restart command для identity-mapping daemon: [Needs confirmation].

## Automount

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| automount | Перечитать master/direct maps в системах с этой командой | mapped paths после изменения | state-changing |
| automount -v | Применить configuration с verbose output | какие mappings изменены | state-changing |
| automount -L | Dry-run configuration | syntax/logic без применения | read-only |
| /etc/init.d/autofs reload | Применить Linux autofs map changes | access к конкретному mapped path | state-changing |

Timeout option:
- automount/autounmountd использует -t <seconds>;
- default в главе: 300 s;
- не менять без operational reason.

## Automount map examples

Indirect map:

~~~text
users  harp:/harp/users
devel  -soft  harp:/harp/devel
info   -ro    harp:/harp/info
~~~

Direct map:

~~~text
/usr/src   harp:/usr/src
/cs/tools  -ro monk:/cs/tools
~~~

Master map:

~~~text
/harp  /etc/auto.harp -proto=tcp
/-     /etc/auto.direct
~~~

Для Linux NFSv4 source требует указывать -fstype=nfs4 в master-map context.

Replicated automount sources:
- использовать только read-only;
- automount не синхронизирует writes между replicas.

## Workload-generating commands

Глава не приводит отдельной команды, которую следует однозначно классифицировать как workload-generating по самому факту запуска.

Однако следующие state-changing действия могут создавать network/application load:
- service restart NFS;
- mount -a -t nfs;
- automount reload;
- изменение nfsd thread count.

Их не следует выполнять массово без проверки после каждого шага.
