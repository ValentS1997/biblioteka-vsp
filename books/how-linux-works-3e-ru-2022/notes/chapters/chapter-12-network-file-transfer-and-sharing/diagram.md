# Диаграмма: передача файлов и сетевой доступ по главе 12

## Выбор механизма

~~~mermaid
flowchart TD
    G["Goal"] --> Q{"Copy or mounted sharing?"}
    Q -->|One-time copy| HTTP["SimpleHTTPServer / scp"]
    Q -->|Repeatable sync| RS["rsync"]
    Q -->|Mounted sharing| M{"Environment?"}
    M -->|Windows interoperability| SMB["SMB / Samba / CIFS"]
    M -->|Small Linux setup| SSHFS["SSHFS"]
    M -->|Unix/NAS| NFS["NFS"]
    M -->|Cloud| FUSE["FUSE-based client"]
~~~

## rsync safety flow

~~~mermaid
flowchart TD
    SRC["Confirm source"] --> DST["Confirm destination"]
    DST --> SLASH{"dir or dir/ ?"}
    SLASH --> DRY["rsync -nva dry run"]
    DRY --> DEL{"Using --delete?"}
    DEL -->|Yes| REVIEW["Review destination-only files"]
    DEL -->|No| RUN["Run transfer"]
    REVIEW --> RUN
    RUN --> VERIFY["Verbose/stats + destination verification"]
~~~

## Network-storage trade-off

~~~mermaid
flowchart LR
    LOCAL["Local storage"] --> LOW["Lower random-access latency"]
    NET["Network storage"] --> CONV["Centralized/convenient access"]
    NET --> LAT["Network latency"]
    LAT --> RANDOM["Random/many-file workloads suffer"]
    NET --> SEC["Authentication + authorization + encryption"]
~~~

## Samba access model

~~~mermaid
flowchart TD
    CLIENT["SMB client"] --> IFACE["interfaces / bind interfaces only"]
    IFACE --> USER["valid users / guest policy"]
    USER --> AUTH["Samba password DB or domain"]
    AUTH --> SHARE["share section: path / writable / browseable"]
    SHARE --> SMBD["smbd"]
    NAME["nmbd / NetBIOS naming"] --> CLIENT
~~~

## Samba credential state

~~~mermaid
flowchart LR
    ADD["smbpasswd -a"] --> ENABLED["Enabled Samba account"]
    ENABLED --> DIS["smbpasswd -d"]
    DIS --> DISABLED["Disabled"]
    DISABLED --> EN["smbpasswd -e"]
    EN --> ENABLED
    ENABLED --> DEL["smbpasswd -x"]
    DEL --> REMOVED["Removed"]
~~~

## Mounted client choices

~~~mermaid
flowchart TD
    SHARE["Remote files"] --> CIFS["CIFS mount"]
    SHARE --> SSHFS["SSHFS / FUSE"]
    SHARE --> NFS["NFS mount"]
    SSHFS --> SSH["SSH/SFTP transport"]
    NFS --> AUTO["automount recommended for dependency control"]
    CIFS --> SMB["SMB server"]
~~~

## Traditional vs user-space clients

~~~mermaid
flowchart LR
    K["Kernel-centric network FS client"] --> LIMIT["Security/auth changes can be harder"]
    U["FUSE user-space client"] --> FLEX["Authentication/encryption logic in user space"]
    FLEX --> CLOUD["Cloud storage integration"]
~~~
