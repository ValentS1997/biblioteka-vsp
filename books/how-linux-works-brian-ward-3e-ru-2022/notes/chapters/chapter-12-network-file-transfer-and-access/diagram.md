# Mermaid — глава 12 «Передача файлов по сети и доступ к ним»

Источник: **RAG `p0368:c01`–`p0389:c01`**, PDF/печатные страницы 368–389. Диаграммы синтезированы только из текстово подтверждённых связей главы; исходные рис. 12.1–12.2 не реконструируются.

## 1. Выбор механизма

```mermaid
flowchart TD
  NEED["Need to move/share files"] --> Q1{"One-off copy?"}
  Q1 -->|Yes| HTTP["Temporary HTTP / direct copy"]
  Q1 -->|No| Q2{"Recurring synchronization?"}
  Q2 -->|Yes| RS["rsync"]
  Q2 -->|No| Q3{"Mounted/shared filesystem?"}
  Q3 -->|Windows/SMB| SMB["Samba / CIFS"]
  Q3 -->|Small Linux↔Linux| SSHFS["SSHFS"]
  Q3 -->|Trusted LAN / NAS| NFS["NFS"]
  Q3 -->|Cloud storage| FUSE["Cloud FUSE client"]
```

The chapter's opening table explicitly treats these as different classes of problem.

## 2. rsync safety workflow

```mermaid
flowchart TD
  SRC["Define exact source"] --> SLASH{"dir or dir/ ?"}
  SLASH --> DST["Define destination"]
  DST --> PRE["rsync -nva ..."]
  PRE --> REVIEW{"Expected mapping/deletions?"}
  REVIEW -->|No| FIX["Fix paths/options"]
  FIX --> PRE
  REVIEW -->|Yes| APPLY["Run real rsync"]
  APPLY --> POST["Repeat dry-run/readback"]
  POST --> CLEAN{"No unexpected delta?"}
  CLEAN -->|Yes| DONE["Accept"]
  CLEAN -->|No| RB["Restore from backup / investigate"]
```

The dry-run/readback boundary is source-grounded; the generic rollback box is an operational synthesis because the chapter does not provide transactional restore semantics.

## 3. Trailing-slash semantics

```mermaid
flowchart LR
  D1["source = dir"] --> R1["destination/dir/..."]
  D2["source = dir/"] --> R2["destination/... contents only"]
  DEL["--delete"] --> R1
  DEL --> R2
  R2 --> RISK["Wrong slash + delete can remove unrelated destination files"]
```

This is the chapter's central rsync path-mapping warning (§12.2.3).

## 4. rsync comparison / overwrite choices

```mermaid
flowchart TD
  CHECK["Compare source ↔ destination"] --> FAST["Default: size + mtime"]
  CHECK --> CS["--checksum"]
  FAST --> DECIDE{"Existing destination file?"}
  CS --> DECIDE
  DECIDE --> IGN["--ignore-existing"]
  DECIDE --> BACK["--backup / --suffix"]
  DECIDE --> UPD["--update"]
  DECIDE --> DEF["Default overwrite behavior"]
```

The source presents these options as ways to control confidence and overwrite behavior (§12.2.5).

## 5. Network-file-sharing trade-off

```mermaid
flowchart TD
  SHARE["Use network filesystem"] --> BENEFIT["Convenience / centralized storage"]
  SHARE --> LAT["Latency"]
  SHARE --> OUTAGE["Dependency on network/storage availability"]
  SHARE --> SEC["Authentication + authorization + encryption"]
  LAT --> RANDOM["Random/many-file workload suffers more"]
  BENEFIT --> STREAM["Large sequential streaming can work well"]
```

§12.3 distinguishes predictable sequential streaming from random access to many files.

## 6. Samba server model

```mermaid
flowchart TD
  CONF["smb.conf"] --> GLOBAL["[global]: identity/network/access"]
  CONF --> SHARES["[share] / [homes] / [printers]"]
  PASS["Samba password DB / smbpasswd"] --> SMBD["smbd"]
  GLOBAL --> SMBD
  SHARES --> SMBD
  NMBD["nmbd"] --> DISC["NetBIOS naming/discovery"]
  SMBD --> CLIENT["SMB clients / smbclient / CIFS mount"]
```

The chapter separates server config, account database, service daemons and client access (§12.4).

## 7. Samba access boundary

```mermaid
flowchart TD
  CLIENT["Client"] --> AUTH{"Credentials / guest?"}
  AUTH -->|Authenticated| USER["valid users / account rules"]
  AUTH -->|Guest| GUEST["guest ok"]
  USER --> SHARE["Share path"]
  GUEST --> SHARE
  SHARE --> MODE{"writable?"}
  MODE -->|No| RO["Read-only share behavior"]
  MODE -->|Yes| RW["Read/write exposure"]
```

The source explicitly warns against writable guest sharing.

## 8. SSHFS / NFS / cloud FUSE placement

```mermaid
flowchart LR
  APP["Local application"] --> VFS["Local filesystem/VFS view"]
  VFS --> SSHFS["SSHFS user-space filesystem"]
  VFS --> NFS["NFS client"]
  VFS --> CFUSE["Cloud FUSE client"]
  SSHFS --> SSH["SSH/SFTP remote host"]
  NFS --> NFSS["NFS server/NAS"]
  CFUSE --> CLOUD["Cloud storage API/service"]
```

The chapter emphasizes that SSHFS/cloud adapters are user-space/FUSE mechanisms, while NFS has historically included kernel client code.

## 9. Failure-coupling view

```mermaid
flowchart TD
  LOCAL["Application expects mounted path"] --> NET{"Network/storage reachable?"}
  NET -->|Yes| IO["Remote file I/O proceeds"]
  NET -->|No| FAIL["Delay / failure / unavailable data"]
  FAIL --> DESIGN["Need workload-specific fallback or automount design"]
```

The exact failure behavior is environment-specific; the chapter's point is that unavailable network storage can degrade the whole system experience.

## 10. Security model

```mermaid
flowchart TD
  SHARE["Shared data"] --> ID["Authentication: who are you?"]
  ID --> AUTHZ["Authorization: what may you access?"]
  AUTHZ --> ENC["Encryption: protect data in transit"]
  ENC --> TRUST["Network/trust boundary"]
```

§12.3.2 explicitly separates identity/access control from encryption.
