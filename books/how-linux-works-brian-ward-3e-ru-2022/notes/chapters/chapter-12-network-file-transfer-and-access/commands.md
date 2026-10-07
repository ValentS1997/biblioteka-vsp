# Команды и интерфейсы — глава 12 «Передача файлов по сети и доступ к ним»

**Provenance:** `p0368:c01`–`p0389:c01`, PDF/печатные страницы 368–389. Только явно поддержанные chapter RAG команды/интерфейсы.

Классы: **RO** — read-only / dry-run; **WG** — active network workload; **SC** — state-changing; **SC-D** — potentially destructive state-changing.

## 1. Быстрая раздача файлов

Источник:

```sh
python -m SimpleHTTPServer
```

**Class:** WG/runtime exposure.

Source behavior:
- serves the current directory over HTTP;
- default port in source: 8000;
- intended only for a protected/private network;
- no persistent configuration is described.

Current command/module availability outside the source edition: **[Needs confirmation]**.

## 2. rsync — baseline and safe preview

```sh
rsync file1 file2 ... host:
rsync file1 file2 ... user@host:
rsync -a dir host:dest_dir
rsync -nva dir host:dest_dir
rsync --help
```

| Option | Meaning in source |
|---|---|
| `-a` | Archive-style directory transfer including links/permissions/modes/devices described by source |
| `-n` | Dry-run: simulate without copying files |
| `-v` | Verbose output |
| `--rsync-path=path` | Explicit remote rsync path if remote shell cannot find it |

**Safety rule from chapter:** when unsure what will happen, use `-nv` before applying.

## 3. rsync — exact mirrors and path semantics

```sh
rsync -a --delete dir host:dest_dir
rsync -a dir host:dest_dir
rsync -a dir/ host:dest_dir
```

- `dir` creates/copies the directory itself below the destination.
- `dir/` copies only the contents.
- `--delete` removes destination items that do not exist in the mapped source tree.

**Class:** `--delete` is **SC-D**.

The source explicitly warns that trailing-slash mistakes combined with `--delete` can remove unrelated files.

## 4. rsync — include/exclude

```sh
rsync -a --exclude=.git src host:
rsync -a --exclude=/src/.git src host:
```

Source options:
- repeated `--exclude`;
- `--exclude-from=file`;
- `--exclude=item/`;
- `--include`.

Patterns are relative to the transfer tree as described in the chapter; the leading slash in the example is not the host filesystem root.

## 5. rsync — verification / overwrite controls

Source options:

| Option | Effect |
|---|---|
| `--checksum` / `-c` | Compare file checksums instead of relying only on size+mtime |
| `--ignore-existing` | Do not overwrite files already present at destination |
| `--backup` / `-b` | Rename destination file with backup suffix before replacement |
| `--suffix=s` | Change backup suffix |
| `--update` / `-u` | Do not overwrite destination file newer than source |
| `-v`, `-vv` | Increasing verbosity |
| `--stats` | Transfer summary |

These alter comparison/overwrite behavior; confirm intended semantics before automation.

## 6. rsync — compression, bandwidth, pull mode

```sh
rsync -az dir host:dest_dir
rsync --bwlimit=100000 -a dir host:dest_dir
rsync -a host:src_dir dest_dir
```

Source notes:
- compression can help slower/high-latency links but cost CPU on fast LANs;
- bandwidth limiting protects competing upstream traffic;
- remote source in first argument switches to pull direction.

## 7. Samba account management

```sh
smbpasswd -a username
smbpasswd -x username
smbpasswd -d username
smbpasswd -e username
smbpasswd username
```

**Class:** SC authentication state.

Meanings:
- `-a`: add Samba user;
- `-x`: remove;
- `-d`: disable;
- `-e`: enable;
- bare username as superuser: change that user's Samba password.

Source warning: `unix password sync = yes` may make Samba password changes affect the normal Unix password too.

## 8. Samba service state and diagnostics

```sh
systemctl --type=service
nmbd -D -s smb_config_file
smbd -D -s smb_config_file
```

- `systemctl --type=service`: source uses it to check service presence/state.
- Manual `nmbd`/`smbd` launch is for source-built installations in the chapter.
- Runtime logs commonly include `log.nmbd` and `log.smbd` under `/var/log/samba`.

Editing `smb.conf` is **SC configuration**. Source says systemd-managed deployments should normally let systemd control service lifecycle.

## 9. Samba client

List shares:

```sh
smbclient -L -U username SERVER
```

Connect to one share:

```sh
smbclient -U username '\\SERVER\sharename'
```

Interactive source commands:

```text
get file
put file
cd dir
lcd localdir
pwd
!command
help
```

- `get`: remote → local copy;
- `put`: local → remote copy;
- `cd`: remote cwd;
- `lcd`: local cwd;
- `!command`: run local command.

These are active file-transfer operations, not purely observational once `get`/`put` are used.

## 10. CIFS mount

Literal source form:

```sh
mount -t cifs SERVER:sharename mountpoint -o user=username,pass=password
```

**Class:** SC mount state; credential-sensitive.

The chapter explicitly contrasts this with `\\SERVER\sharename`, but gives no additional validation of the mount-source syntax. Current environment applicability: **[Needs confirmation]**; see `source-findings.md`.

The literal example places credential text in the option string. No safer credential-storage command is supplied by this chapter.

## 11. SSHFS

```sh
sshfs username@host:dir mountpoint
fusermount -u mountpoint
```

Source variations:
- omit `username@` if local/remote usernames match;
- omit `:dir` to mount the remote home directory.

The chapter recommends ordinary-user mounting for consistency of permissions/security in this use case.

## 12. NFS

```sh
mount -t nfs server:directory mountpoint
```

Source notes:
- `-t nfs` is technically optional in its described environment;
- security options are documented via `nfs(5)`;
- stronger authentication such as Kerberos requires additional setup;
- systemd automount units can replace older automount/amd workflows.

NFS server setup is described conceptually through `mountd`, `nfsd` and `/etc/exports`, but no complete server command sequence is provided.

## 13. Samba configuration keys from source

Examples under `[global]`:

```ini
netbios name = name
server string = My server via Samba
workgroup = MYNETWORK
interfaces = 10.23.2.0/255.255.255.0
interfaces = enp0s31f6
bind interfaces only = yes
valid users = jruser, bill
guest ok = true
browseable = no
security = user
passdb backend = tdbsam
obey pam restrictions = yes
smb passwd file = /etc/samba/passwd_smb
```

Share example:

```ini
[label]
path = path
comment = share description
guest ok = no
writable = yes
printable = no
```

Home-share example:

```ini
[homes]
comment = home directories
browseable = no
writable = yes
```

Printer-share example includes `printing = CUPS`, `printable = yes`, `writable = no`.

These are **SC configuration** if applied. Real interfaces, users, workgroups and paths are **[Needs confirmation]**.

## Command discipline

- Dry-run before destructive rsync changes.
- Treat `dir` and `dir/` as different source mappings.
- Do not assume a share/mount is safe merely because it is convenient.
- Preserve prior Samba account/config state before modification.
- Treat credentials, writable guest access and network mounts as security boundaries.
- Do not modernize or replace source commands silently; edition/applicability gaps are recorded in `source-findings.md`.
