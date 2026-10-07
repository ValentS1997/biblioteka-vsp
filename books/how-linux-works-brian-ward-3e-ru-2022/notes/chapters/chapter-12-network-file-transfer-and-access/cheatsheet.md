# Cheatsheet — глава 12 «Передача файлов по сети и доступ к ним»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0368:c01`–`p0389:c01`, PDF/печатные страницы 368–389. Только `rag_only`.

## Symptom / problem framing

Глава разделяет несколько разных задач, которые часто ошибочно смешивают:

1. разовая раздача файла/каталога;
2. повторяемая синхронизация;
3. общий SMB-доступ для Windows/macOS/Linux;
4. небольшой secure mount через SSH;
5. NFS/NAS в доверенной локальной сети;
6. облачное хранилище через FUSE.

Для operational work главный вопрос: **нужно копирование или удалённая файловая система**, и какая цена ошибки — перезапись, удаление, раскрытие данных или зависимость от сети.

## Baseline / context

| Механизм | Модель главы | PDF |
|---|---|---:|
| Temporary HTTP | Разовая read-only раздача текущего каталога по сети | 369 |
| rsync | Повторяемая синхронизация local↔remote, обычно через SSH | 370–376 |
| Samba/SMB | File/printer sharing and Windows interoperability | 378–386 |
| CIFS mount | Подключение SMB share в local filesystem tree | 385 |
| SSHFS | FUSE filesystem over SSH/SFTP | 386 |
| NFS | Unix network filesystem; many versions/security modes | 387 |
| Cloud/FUSE | User-space filesystem adapter to cloud storage | 388 |
| Sharing trade-off | Latency, temporary network loss, security complexity | 376–389 |

## Read-only checks

```sh
rsync -nva dir host:dest_dir
rsync --help
systemctl --type=service
smbclient -L -U username SERVER
rpcinfo -p localhost
```

Additional source-grounded inspection points:

- Samba runtime logs such as `log.nmbd` and `log.smbd`, commonly under `/var/log/samba`.
- Samba configuration file `smb.conf`, commonly under `/etc/samba`.
- NFS options documentation via `nfs(5)`.
- For rsync destructive/mirror work, dry-run is the primary pre-change verification mechanism in this chapter.

## Interpretation

| Observation | Interpretation from chapter | Still unchecked |
|---|---|---|
| `rsync -nva` lists files only | Those items would be considered for transfer under current arguments | Destination correctness still depends on source/path semantics |
| Dry-run shows deletions with `--delete` | Destination contains items absent from source under current mapping | Whether deletion is intended |
| `dir` vs `dir/` changes plan | Source-directory object vs source-directory contents | Correct intended destination layout |
| rsync reports remote `rsync not found` | Remote shell cannot find rsync in its command path | Whether absolute path exists |
| smbclient lists Disk/Printer shares | Server advertises those resources to current credentials | Filesystem permissions/read-write rights |
| Samba logs contain startup/runtime error | smbd/nmbd encountered server-side issue | Root cause depends on config/network/account state |
| SSHFS mount works | SSH/SFTP path and FUSE access are sufficient | Performance/multi-user suitability |
| NFS mount works | Client can reach/export selected server directory | Security/availability semantics beyond current session |
| Network filesystem is slow with many random file accesses | Latency can dominate small/random operations | Local CPU/disk/network bottleneck still [Needs confirmation] |

## Next action

1. Classify the task: copy/sync vs mounted sharing.
2. For rsync, write the exact source and destination paths and explicitly decide whether the source ends in `/`.
3. Run `-n`/`-nv` before any `--delete`, overwrite-heavy or automated synchronization.
4. For Samba/NFS/SSHFS, identify trust boundary, authentication model and failure impact if the network disappears.
5. For shared-write setups, verify exact account/share permissions before exposing data.
6. If destination ownership, deletion scope, password/account coupling or mount rollback is unknown → **[Needs confirmation]**.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| `python -m SimpleHTTPServer` | Exposes current directory through a basic HTTP server | Network data exposure; source says use only on protected LAN |
| `rsync -a ...` | Copies directory tree/metadata according to archive mode | Overwrite/path-layout risk |
| `rsync -a --delete ...` | Makes destination mirror source by deleting extra destination files | **High risk destructive** |
| `rsync --exclude/--include` | Changes transferred object set | Wrong pattern can omit/include unexpected data |
| `rsync --backup` / `--update` | Changes overwrite behavior | May leave backup/newer files intentionally |
| `smbpasswd -a/-x/-d/-e` | Add/remove/disable/enable Samba account | Authentication/access state changes |
| Edit `smb.conf` | Changes Samba exposure/access/shares | Misconfiguration can expose or deny data |
| Start `nmbd`/`smbd` | Starts Samba services | Opens network services |
| `mount -t cifs ...` | Mounts SMB share | Remote filesystem becomes part of local path tree |
| `sshfs ... mountpoint` | Mounts remote directory over SSH/FUSE | Network dependency and local mount-state change |
| `fusermount -u mountpoint` | Unmounts user SSHFS/FUSE mount | Applications using mount may fail |
| `mount -t nfs ...` | Mounts NFS export | Network/security/availability coupling |

## Verification / acceptance checks

| Change | Verification | Acceptance |
|---|---|---|
| rsync copy | Re-run `rsync -nva` | No unexpected pending transfer/delete under same arguments |
| rsync mirror | Dry-run before apply, then dry-run again after apply | Destination converges without unintended deletions |
| Samba account change | Authenticated client listing/access | Intended user can/cannot access as planned |
| Samba share config | `smbclient -L` + share access + logs | Intended share visible; permissions match expectation |
| CIFS/SSHFS/NFS mount | Access expected file/tree, then clean unmount when test completes | Correct mountpoint/content and no unintended local shadowing |
| SSHFS unmount | Mountpoint no longer presents remote tree | No dependent process unexpectedly broken |
| NFS client | Required files accessible with expected behavior | Network outage/failure mode still needs environment validation |
| Temporary HTTP | Controlled client can fetch intended file only during test window | Server terminated after transfer; no unplanned exposure remains |

## Rollback

- rsync overwrite/delete: rollback depends on having prior copies/backups. The chapter's `--backup` option can preserve overwritten destination files, but there is no generic transactional restore workflow → **[Needs confirmation]**.
- Trailing-slash/path mistake: stop before apply if dry-run is wrong. After destructive apply, recovery depends on external backups.
- Samba config: preserve prior `smb.conf` and account state before modifying. Exact restore commands are environment-specific.
- Samba account deletion/password changes: previous auth state is not automatically recoverable; capture account intent first.
- CIFS/NFS/SSHFS: unmount is the conceptual rollback for a test mount; persistent boot configuration is not covered by concrete commands here.
- Temporary HTTP: terminate the server process; no persistent configuration is described.
- Network-storage dependency failures cannot be “rolled back” by a generic command; local fallback/design remains **[Needs confirmation]**.

## Guardrails

- **Dry-run before `rsync --delete`.**
- Treat trailing slash on rsync source as a semantic operator, not cosmetic syntax.
- Never assume remote and local copies are identical solely because size/time match when correctness matters; the chapter provides `--checksum` for stronger comparison.
- Do not combine writable guest Samba access casually.
- `unix password sync = yes` can couple Samba password changes to normal Unix password behavior.
- The literal source CIFS example includes credential text in the command; a safer current credential-handling method is not supplied by the chapter and therefore remains **[Needs confirmation]**.
- Do not run the temporary HTTP example on an untrusted/public network.
