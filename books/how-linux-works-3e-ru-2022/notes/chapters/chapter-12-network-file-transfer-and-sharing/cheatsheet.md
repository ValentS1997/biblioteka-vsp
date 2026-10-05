# Шпаргалка: передача файлов и сетевой доступ по главе 12

## Symptom / problem framing

Типовые задачи:

- быстро отдать один файл в защищённой LAN;
- регулярно синхронизировать directory tree;
- получить exact mirror destination;
- исключить часть files из sync;
- не забить uplink большим transfer;
- предоставить Windows clients доступ к Linux files;
- подключить SMB share на Linux;
- быстро смонтировать remote Linux directory через SSH;
- подключить NFS/NAS;
- выбрать между local и network storage.

## Baseline / context

Source-derived decision tree:

```text
one-time/simple transfer
  ├─ SimpleHTTPServer
  └─ scp -r

repeatable synchronization
  └─ rsync

mounted shared filesystem
  ├─ SMB/CIFS → Windows interoperability
  ├─ SSHFS    → small/simple encrypted Linux sharing
  ├─ NFS      → Unix/NAS, trusted or explicitly secured environment
  └─ FUSE     → cloud/user-space client models
```

Before any state-changing transfer:
- identify source and destination;
- capture destination baseline;
- understand overwrite/delete behavior;
- confirm security of the network and authentication path.

## Read-only checks

### rsync dry run

```bash
rsync -nva dir host:dest_dir
```

Use before uncertain transfer, especially before `--delete`.

Useful observation options named by source:
- `-v`, `-vv`;
- `--stats`;
- `--checksum` for stronger file comparison.

### Samba service inventory

```bash
systemctl --type=service
```

Use to see whether package-managed Samba services already exist.

### Samba share discovery

```bash
smbclient -L -U username SERVER
```

Lists shares exposed by the server.

## Interpretation

### rsync source path semantics

```text
rsync -a dir  host:dest_dir
→ destination contains dest_dir/dir/...

rsync -a dir/ host:dest_dir
→ contents of dir go directly into dest_dir
```

Trailing slash is not cosmetic.

### rsync delete semantics

`--delete` removes destination entries that do not exist in source.

Always preview when uncertain:

```bash
rsync -nva --delete dir host:dest_dir
```

The exact combined example is a direct composition of source options; if strict source-only command reproduction is required, treat this combined invocation as `[Needs confirmation]`.

### rsync safety/performance controls

- `--ignore-existing` — preserve existing destination files.
- `--backup` / `-b` — rename previous destination file with backup suffix.
- `--suffix=s` — set backup suffix.
- `--update` / `-u` — preserve newer destination files.
- `-z` — compress transfer; useful only when network is the bottleneck.
- `--bwlimit` — cap bandwidth.

### Network filesystem performance

Sequential large-file workloads can perform acceptably because buffering/prefetch works well.

Many small/random accesses amplify network latency. For demanding build/edit workloads, source suggests local storage may be more efficient.

### File-sharing security

If the path crosses an untrusted network:
- authenticate/authorize both sides;
- encrypt transferred data.

Easy-to-configure sharing is often not the most secure sharing.

### Samba

Central config:
`smb.conf`.

Important exposure controls:
- `interfaces`;
- `bind interfaces only`;
- `valid users`;
- `guest ok`;
- `browseable`;
- `writable`.

Do not expose guest read/write share casually; source explicitly warns against guest write access.

### Samba password state

`smbpasswd` manages Samba users/passwords.

Watch for:

```ini
unix password sync = yes
```

This couples Samba password changes with normal Unix password changes.

### SSHFS

Pros:
- minimal server-side setup beyond SFTP/SSH;
- works across untrusted networks through SSH.

Cons:
- encryption/translation/transport overhead;
- limited multi-user suitability.

### NFS

Basic client mount is simple, but security and version/options are broader than the shown command.

Source notes:
- host-based controls common in small trusted networks;
- Kerberos-style security is stronger but more complex;
- automount helps avoid boot-time dependency problems.

### Cloud/FUSE

Cloud storage clients often run as FUSE user-space daemons.

This allows authentication/encryption logic outside kernel filesystem client code.

## Next action

1. Decide: copy, sync, or mounted sharing.
2. For sync, run dry-run first.
3. Confirm trailing-slash semantics.
4. If using `--delete`, verify destination-only files are disposable.
5. For mounted sharing, evaluate latency/workload before rollout.
6. If network is not trusted, require authentication + encryption.
7. For Samba, scope interfaces/users/shares before enabling write access.
8. For SSHFS/NFS/CIFS, confirm mountpoint and unmount/recovery path.

## Modifying action

Source-confirmed modifying actions include:

```bash
python -m SimpleHTTPServer
scp -r directory user@remote_host[:dest_dir]
rsync -a dir host:dest_dir
rsync -a --delete dir host:dest_dir
rsync -az dir host:dest_dir
rsync --bwlimit=100000 -a dir host:dest_dir
smbpasswd -a username
smbpasswd -x username
smbpasswd -d username
smbpasswd -e username
nmbd -D -s smb_config_file
smbd -D -s smb_config_file
mount -t cifs SERVER:sharename mountpoint -o user=username,pass=password
sshfs username@host:dir mountpoint
fusermount -u mountpoint
mount -t nfs server:directory mountpoint
```

Config-file changes to `smb.conf` are also state-changing.

## Verification / acceptance checks

| Action/change | Verification |
|---|---|
| SimpleHTTPServer | target browser can retrieve intended file; server exposes only intended directory/network |
| rsync copy | rerun with `-v`/dry-run and confirm no unexpected transfer |
| rsync exact mirror | dry-run confirms intended deletes before real run |
| rsync excludes | verbose/dry-run output omits intended patterns |
| Samba user add/disable/enable | authenticate with intended account/state |
| Samba service | service/process state + Samba logs |
| Samba share | `smbclient -L` then access intended share |
| CIFS mount | expected remote files visible at mountpoint |
| SSHFS mount | expected remote directory visible; `fusermount -u` succeeds |
| NFS mount | expected exported directory visible at mountpoint |

## Rollback

- Temporary SimpleHTTPServer → terminate foreground server process.
- `scp -r` / normal rsync copy → destination data rollback depends on previous contents: `[Needs confirmation]`.
- `rsync --delete` → deleted destination-only files are not generically recoverable; use backup/recovery if available: `[Needs confirmation]`.
- `smbpasswd -a` → source provides `smbpasswd -x username`, but this removes Samba user state rather than restoring previous credentials.
- `smbpasswd -d` → source provides `smbpasswd -e username`.
- `smbpasswd -e` → source provides `smbpasswd -d username`.
- Samba config edits → restore known-good `smb.conf`; exact backup/reload procedure `[Needs confirmation]`.
- Manual `nmbd/smbd` startup → source does not provide explicit stop command: `[Needs confirmation]`.
- SSHFS mount → `fusermount -u mountpoint`.
- CIFS/NFS mount rollback command is not explicitly provided in the verified source section: `[Needs confirmation]`.
