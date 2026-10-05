# Команды и интерфейсы главы 12

Только команды, options и interfaces, явно подтверждённые RAG главы 12.

| Команда / интерфейс | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `python -m SimpleHTTPServer` | Temporary HTTP sharing of current directory | workload-generating | Opens HTTP server, default port 8000 | Source warning: do not use on public/untrusted network | Retrieve intended file from trusted client | Terminate foreground process |
| `scp -r directory user@remote_host[:dest_dir]` | Recursive remote copy | state-changing | Writes directory tree at remote destination | Can merge into pre-existing destination instead of exact mirror | Verify destination tree | `[Needs confirmation]` |
| `rsync file1 file2 ... host:` | Copy files to remote home | state-changing | Writes remote files | Existing destination may be overwritten based on rsync comparison | Re-run/inspect destination | `[Needs confirmation]` |
| `rsync file1 file2 ... user@host:` | Same with explicit remote user | state-changing | Writes remote files | Same overwrite/data-state risk | Re-run/inspect destination | `[Needs confirmation]` |
| `rsync -a dir host:dest_dir` | Archive-mode directory copy | state-changing | Copies hierarchy/links/permissions/modes/devices | Wrong source/destination changes remote tree | `rsync -nva ...` before change; verify tree after | `[Needs confirmation]` |
| `rsync -nva dir host:dest_dir` | Dry-run + verbose archive preview | workload-generating/read-only | Connects and computes transfer without copying files | No intended data modification | Inspect planned file list | N/A |
| `rsync -a --delete dir host:dest_dir` | Make destination mirror source | state-changing/destructive | Deletes destination-only files | Explicit source warning: can delete unrelated files | Dry-run first; inspect destination | Deleted files not generically recoverable: `[Needs confirmation]` |
| `rsync -a dir/ host:dest_dir` | Copy contents of source directory | state-changing | Writes contents directly into destination | Trailing slash changes layout; dangerous with delete | Verify planned destination layout | `[Needs confirmation]` |
| `rsync -a --exclude=.git src host:` | Exclude matching names | state-changing | Copies while omitting pattern matches | Pattern may be broader than intended | Dry-run/verbose output | `[Needs confirmation]` |
| `rsync -a --exclude=/src/.git src host:` | Exclude one transfer-root-relative path | state-changing | Omits specific path | Leading slash is relative to transfer root, not filesystem root | Dry-run/verbose output | `[Needs confirmation]` |
| `rsync -az dir host:dest_dir` | Archive + compression | state-changing | Copies compressed over transport | CPU cost can reduce performance on fast LAN | Compare transfer behavior/stats | `[Needs confirmation]` |
| `rsync --bwlimit=100000 -a dir host:dest_dir` | Limit transfer bandwidth | state-changing | Copies while limiting bandwidth | Wrong limit affects transfer time/network use | Observe transfer/network behavior | `[Needs confirmation]` |
| `rsync -a host:src_dir dest_dir` | Pull remote directory locally | state-changing | Writes local destination tree | May overwrite local destination files | Verify local tree | `[Needs confirmation]` |
| `rsync --help` | Show rsync options | read-only | No state change | None | Read output | N/A |
| `systemctl --type=service` | Inspect installed/running services | read-only | No state change | None | Locate Samba services | N/A |
| `smbpasswd -a username` | Add Samba password user | state-changing/security | Creates Samba credential entry | Authentication state changes | Authenticate intended user | `smbpasswd -x username` removes entry, not previous credential restoration |
| `smbpasswd -x username` | Delete Samba user | state-changing/security | Removes Samba credential entry | User loses Samba access | Authentication should fail as intended | Restore prior credentials: `[Needs confirmation]` |
| `smbpasswd -d username` | Disable Samba user | state-changing/security | Disables account in Samba DB | User loses Samba access | Login should be rejected | `smbpasswd -e username` |
| `smbpasswd -e username` | Enable Samba user | state-changing/security | Enables account in Samba DB | Restores network access | Login should succeed as intended | `smbpasswd -d username` |
| `smbpasswd username` | Change Samba password | state-changing/security | Changes Samba credential | With `unix password sync = yes`, may also change Unix password | Authenticate with intended password | Previous password restoration `[Needs confirmation]` |
| `nmbd -D -s smb_config_file` | Start NetBIOS name daemon manually | state-changing | Starts daemon using specified config | Opens network service; source prefers systemd for package install | Check service/process/logs | `[Needs confirmation]` |
| `smbd -D -s smb_config_file` | Start Samba file-sharing daemon manually | state-changing | Starts SMB request daemon | Opens network service/share surface | Check service/process/logs | `[Needs confirmation]` |
| `smbclient -L -U username SERVER` | List remote Samba shares | workload-generating/read-only | Authenticates and queries server | May expose credentials interactively, no persistent data change intended | Inspect share list | N/A |
| `smbclient -U username '\\SERVER\sharename'` | Interactive access to SMB share | workload-generating | Opens client session | Interactive `get/put` may change local/remote files | Inspect prompt/share/path | Session close; file changes `[Needs confirmation]` |
| `mount -t cifs SERVER:sharename mountpoint -o user=username,pass=password` | Mount CIFS share | state-changing | Adds remote filesystem to local namespace | Credential supplied inline in source example; broader exposure implications `[Needs confirmation]` | Verify expected files at mountpoint | Explicit inverse command not provided: `[Needs confirmation]` |
| `sshfs username@host:dir mountpoint` | Mount remote dir via SSH/FUSE | state-changing | Adds SSHFS mount | Performance/multi-user limitations | Verify expected files at mountpoint | `fusermount -u mountpoint` |
| `fusermount -u mountpoint` | Unmount user SSHFS | state-changing | Removes SSHFS mount | Active-use behavior not detailed | Mount disappears | Re-mount if needed |
| `mount -t nfs server:directory mountpoint` | Mount NFS export | state-changing | Adds remote NFS filesystem | Security/version/options and remote availability affect behavior | Verify expected files at mountpoint | Explicit inverse not provided: `[Needs confirmation]` |

## rsync options highlighted by source

- `-a` — archive mode.
- `-n` — dry run.
- `-v`, `-vv` — verbose.
- `--delete` — remove destination-only entries.
- `--exclude`, `--exclude-from`, `--include` — pattern selection.
- `--checksum` / `-c` — checksum comparison.
- `--ignore-existing` — preserve existing destination files.
- `--backup` / `-b` — rename replaced destination files.
- `--suffix=s` — backup suffix.
- `--update` / `-u` — preserve newer destination files.
- `--stats` — transfer statistics.
- `-z` — compression.
- `--bwlimit` — bandwidth limit.
- `--rsync-path=path` — remote rsync path.

## Samba configuration surfaces named by source

- `smb.conf` — central server configuration.
- Usually under `/etc/samba`, but source notes alternative install paths exist.
- `[global]`, `[homes]`, `[printers]`, per-share sections.
- Access controls: `interfaces`, `bind interfaces only`, `valid users`, `guest ok`, `browseable`, `writable`.
- Password backend examples: `security = user`, `passdb backend = tdbsam`, `obey pam restrictions = yes`.
- Runtime logs: `log.nmbd`, `log.smbd`, usually under `/var/log/samba`.

## smbclient interactive commands named by source

- `get file`
- `put file`
- `cd dir`
- `lcd localdir`
- `pwd`
- `!command`
- `help`

`put` is state-changing on the remote share; `get` writes locally. Rollback depends on destination contents: `[Needs confirmation]`.

## Safety notes

1. Do not run SimpleHTTPServer on public/untrusted networks.
2. Preview rsync with `-n` when destination effects are uncertain.
3. Treat `--delete` as destructive.
4. Trailing slash in rsync source path changes result layout.
5. Do not combine guest access with writable Samba share casually; source explicitly warns against guest read/write.
6. Watch `unix password sync = yes`: Samba password operations can affect Unix login credentials.
7. For untrusted networks, source requires authentication/authorization and encryption.
8. Network filesystems can fail operationally when remote storage becomes unavailable.
