# Шпаргалка: NFS server, client, security и automount

## 1. Что такое NFS

NFS дает приложениям удаленную filesystem через обычный file API.

~~~text
application
→ VFS / NFS client
→ RPC
→ network
→ NFS server
→ exported filesystem
~~~

NFS работает на уровне files/directories, не disk blocks.

## 2. Версии: главное различие

NFSv2/v3:
- server model преимущественно stateless;
- mountd отделен от file service;
- lockd/statd нужны для locking;
- v3 может использовать UDP или TCP.

NFSv4:
- stateful;
- locking входит в основной protocol;
- TCP;
- единая exported pseudofilesystem;
- stronger security architecture.

## 3. Security baseline

AUTH_SYS:
- client передает UID/GID;
- server доверяет этим identity values;
- требует согласованных identities;
- не является сильной authentication model.

RPCSEC_GSS + Kerberos:
- krb5 = authentication;
- krb5i = authentication + integrity;
- krb5p = authentication + integrity + confidentiality.

Глава рекомендует Kerberos/RPCSEC_GSS для NFSv4.

## 4. Network boundary

NFSv4:
- TCP;
- обычно port 2049.

Если Internet access не нужен:
- ограничить source/destination firewall rules;
- не публиковать service наружу без необходимости.

NFSv2/v3:
- дополнительные RPC dependencies;
- portmap historically uses port 111;
- security boundary сложнее.

## 5. Linux exports

Формат:

~~~text
<path> <client>(<options>) <client>(<options>)
~~~

Пример:

~~~text
/home *.users.admin.com(rw) 172.17.0.0/24(ro)
~~~

Apply:

~~~bash
exportfs -a
exportfs -v
~~~

Проверить:
- path;
- client/network;
- ro/rw;
- security mode;
- root squashing.

## 6. Linux export hazards

Danger:
- export без client specification;
- пробел между client и (options) может изменить meaning;
- no_root_squash;
- async.

Defaults/important:
- root_squash обычно включен;
- sync — safe default в контексте главы.

## 7. root_squash

Remote UID/GID 0 отображается на anonymous account.

~~~text
client root
→ NFS server
→ anonymous/nobody identity
~~~

Это снижает privilege of remote root, но не исправляет фундаментальные weaknesses AUTH_SYS.

## 8. FreeBSD exports

Синтаксис отличается от Linux.

Пример:

~~~text
/var/www -ro,alldirs www*.admin.com
~~~

Kerberos-protected example:

~~~text
/var/www -alldirs,sec=krb5p -network 2001:db8::/32
~~~

NFSv4 root:

~~~text
V4:/exports ...
~~~

Не использовать V4:/ для local root filesystem /.

## 9. Server change workflow

~~~text
edit /etc/exports
→ check client scope/options
→ apply
→ verify active exports
→ client mount test
~~~

Linux:

~~~bash
exportfs -a
exportfs -v
~~~

FreeBSD:

~~~bash
service nfsd restart
service mountd reload
~~~

## 10. Client discovery

NFSv2/v3:

~~~bash
showmount -e <server>
~~~

NFSv4:
- showmount не отражает pseudofilesystem model;
- на server: exportfs -v;
- remote: mount pseudoroot/subtree и inspect paths.

## 11. Client mount

v2/v3:

~~~bash
mount -o rw,hard,intr,bg server:/home/ben /nfs/ben
~~~

v4 Linux:

~~~bash
mount -o rw,hard,intr,bg server:/ /nfs/ben
~~~

v4 FreeBSD:

~~~bash
mount -t nfs -o nfsv4 server:/ /mnt
~~~

## 12. hard vs soft

hard:
- blocked I/O waits for server return;
- preserves retry semantics;
- can hang processes.

soft:
- returns error after retry/timeouts;
- suitable only when that failure model is acceptable.

Do not choose mechanically.

## 13. Persistent mount

fstab example:

~~~text
monk:/home /nfs/home nfs rw,bg,intr,hard,nodev,nosuid 0 0
~~~

Apply without reboot:

~~~bash
mount -a -t nfs
~~~

Before persisting:
- manual mount must already work;
- security mode and failure behavior must be understood.

## 14. Unmount troubleshooting

Normal:

~~~bash
umount <mountpoint>
~~~

If busy:

~~~bash
fuser <mountpoint>
lsof <mountpoint>
~~~

Resolve users/processes first.

Last resort:

~~~bash
umount -f <mountpoint>
~~~

## 15. Identity mapping in NFSv4

~~~text
server UID/GID
↔ user@nfs-domain / group@nfs-domain
↔ client UID/GID
~~~

Identity mapping:
- affects ownership/attribute representation;
- does not itself perform authentication/authorization.

All participants should use the same NFS domain.

## 16. NFSv4 identity components

Linux:
- rpc.idmapd;
- /etc/idmapd.conf.

FreeBSD:
- nfsuserd;
- nfsuserd_flags in /etc/rc.conf.

Restart command after change: [Needs confirmation].

## 17. nfsstat

Server:

~~~bash
nfsstat -s
~~~

Client:

~~~bash
nfsstat -c
~~~

Interpretation from chapter:
- high failures/timeouts = investigate;
- low badxid + high timeout → network loss suspected;
- badxid near timeout → slow server suspected.

## 18. Tuning boundary

Possible parameters:
- rsize;
- wsize;
- timeo;
- retrans;
- nfsd thread count.

Only tune after evidence from:
- nfsstat;
- netstat;
- ps;
- uptime.

Rollback:
- restore previous values.

## 19. nfsd thread tuning

Signal:
- nfsd often in D;
- CPU idle exists.

Then source suggests trying more threads.

If load average rises after adding threads:
- revert toward previous count.

No universal thread number is given.

## 20. Automount architecture

~~~text
access path
→ autofs intercept
→ automount daemon
→ mount NFS
→ application continues
→ idle timeout
→ unmount
~~~

Purpose:
- fewer permanent mounts;
- less blast radius when one server fails;
- centralized mapping.

## 21. Map types

Indirect map:
- multiple subdirectories under common root.

Direct map:
- full mount paths.

Master map:
- points to direct/indirect maps.

Linux default master:
- /etc/auto.master.

FreeBSD default master:
- /etc/auto_master.

## 22. Validate automount

Dry-run:

~~~bash
automount -L
~~~

Verbose apply:

~~~bash
automount -v
~~~

Linux reload:

~~~bash
/etc/init.d/autofs reload
~~~

Acceptance:
- access exact mapped path;
- verify correct server/path/options.

## 23. Replicated automount sources

Use only for read-only identical data.

Why:
- automount can select among replicas;
- it does not synchronize writes.

Do not use replicated read-write mounts as if they were a coherent replicated filesystem.

## 24. Incident flow

~~~text
NFS path unavailable
→ is export active?
→ is correct version/security mode used?
→ can client mount?
→ is server reachable?
→ nfsstat/netstat
→ only then tune or restart
~~~

## 25. Canonical operational rule

~~~text
manual export + manual mount first
→ verify access/security/failure semantics
→ persist in fstab or autofs only after that
~~~
