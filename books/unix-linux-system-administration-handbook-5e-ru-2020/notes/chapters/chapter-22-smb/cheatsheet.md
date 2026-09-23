# Шпаргалка: Samba / SMB

## 1. Архитектура

~~~text
Windows/UNIX client
→ SMB
→ smbd
→ authentication/authorization
→ UNIX filesystem permissions
→ files
~~~

Дополнительно:
- nmbd → name service / service announcement;
- smbd → file service, auth, locking.

Samba работает в userspace.

## 2. SMB vs NFS в главе

SMB:
- cross-platform;
- особенно полезен Windows + UNIX/Linux;
- per-user style access;
- relies on underlying OS permissions.

NFS:
- tighter UNIX/Linux integration;
- kernel-oriented server architecture;
- рассматривается отдельно в главе 21.

## 3. Configuration baseline

Linux:
~~~text
/etc/samba/smb.conf
~~~

FreeBSD:
~~~text
/usr/local/etc/smb4.conf
~~~

Read-only inspection:

~~~bash
testparm -v
~~~

Глава отмечает, что Samba периодически перечитывает config; отдельный restart после обычной правки не требуется.

## 4. Local authentication

~~~text
UNIX account
+
Samba password hash
=
SMB local identity workflow
~~~

Create SMB password record:

~~~bash
smbpasswd -a <user>
~~~

Precondition:
- UNIX account already exists.

Current user password change:

~~~bash
smbpasswd
~~~

## 5. AD authentication

Relevant smb.conf concepts:

~~~text
security = ads
realm = ...
dedicated keytab file = FILE:...
kerberos method = dedicated keytab
~~~

Dependencies described in chapter:
- sssd;
- NSS/PAM;
- Kerberos/AD integration.

Keytab is security-sensitive.

## 6. Simple share

~~~text
[bookshare]
path = /storage/bookshare
read only = no
~~~

Share name = section name.

## 7. Home shares

~~~text
[homes]
browseable = no
valid users = %S
read only = no
~~~

%S maps to share/user name and restricts access to the corresponding owner.

## 8. Project share

Access boundary:

~~~text
valid users = @eng
force group = eng
create mask = 0660
directory mask = 2770
force directory mode = 2000
guest ok = no
~~~

Filesystem:

~~~bash
chown root:eng /home/eng
chmod u=rwx,g=rwxs,o= /home/eng
~~~

Setgid behavior keeps project group inheritance.

## 9. Authorization principle

Samba does not replace UNIX filesystem permissions.

~~~text
SMB authenticated user
→ Samba share policy
→ UNIX user/group/mode or ACL
→ final file access
~~~

Both layers must agree.

## 10. Linux mount

~~~bash
mount -t cifs -o username=<user> //<server>/<share> <mountpoint>
~~~

Client-side mapping options:
- uid;
- gid;
- fmask;
- dmask.

Use them to match intended local ownership/mode presentation.

## 11. FreeBSD mount

~~~bash
mount -t smbfs //<user>@<server>/<share> <mountpoint>
~~~

SMB mount is user-credential-oriented, unlike system-wide NFS semantics described in previous chapter.

## 12. Browse without mount

List shares:

~~~bash
smbclient -L //<server> -U <user>
~~~

Open share:

~~~bash
smbclient //<server>/<share> -U <user>
~~~

Inside:
~~~text
help
~~~

Useful to separate:
- authentication;
- share discovery;
- filesystem-mount problem.

## 13. Network security

smb.conf:
- hosts allow;
- hosts deny.

Rule:
- deny has priority over allow.

Firewall boundary from chapter:
- UDP 137–139;
- TCP 137, 139, 445.

Do not expose SMB beyond trusted network without appropriate protection.

## 14. Transport confidentiality boundary

Chapter context:
- password authentication is protected;
- file data transport in the described setup is not encrypted.

Therefore Internet exposure is explicitly discouraged.

## 15. First troubleshooting command

~~~bash
smbstatus
~~~

Shows:
- sessions/users;
- mounted shares;
- smbd PID;
- locked files.

For lock incidents:
- identify client/user/file;
- resolve offending application on client first.

Do not kill smbd merely to clear a lock unless the application impact is understood.

## 16. Logging

Key smb.conf controls:

~~~text
log file
max log size
syslog only
syslog
~~~

More verbosity:
- more diagnostic detail;
- more resource usage;
- more sensitive material.

## 17. Runtime debug

~~~bash
smbcontrol smbd debug "4 auth:10"
~~~

Use smbstatus first if only one connection needs debug.

After investigation:
- restore previous debug level.

Above log level 100, chapter warns that encrypted passwords may appear in logs.

## 18. Authentication failure workflow

~~~text
smbclient/test connection
→ smbstatus
→ Samba auth log
→ verify UNIX account / Samba password / AD identity
→ verify share restrictions
→ verify filesystem permissions
~~~

Do not change all layers at once.

## 19. Share access workflow

~~~text
testparm -v
→ validate share definition
→ smbclient -L
→ connect to share
→ verify read/write
→ mount only after browse/auth works
~~~

## 20. Character sets

Samba 3+ uses UTF-8 filenames.

Check locale:

~~~bash
echo $LANG
~~~

If server locale is non-UTF-8, align Samba charset settings from the beginning.

Accumulated wrong filenames are difficult to repair later.

## 21. Security-sensitive artifacts

- smb.conf;
- Samba password database;
- AD keytab;
- logs at high debug levels;
- project-share UNIX permissions.

Treat configuration and logs as part of the security boundary.

## 22. Rollback

For config/permissions:
- restore previous smb.conf;
- restore previous owner/group/mode;
- restore previous debug level.

If baseline was not recorded:
- [Needs confirmation].
