# Диаграмма: NFS export → mount → observe → automount

~~~mermaid
flowchart TD
    A["Need shared filesystem"] --> B{"NFS version?"}

    B -->|v2/v3| C["stateless-oriented service"]
    C --> C1["mountd + nfsd"]
    C --> C2["lockd + statd for locking"]
    C --> C3["showmount -e for export discovery"]

    B -->|v4| D["stateful protocol"]
    D --> D1["TCP / 2049"]
    D --> D2["integrated locking"]
    D --> D3["pseudofilesystem export"]
    D --> D4["identity mapping"]

    A --> E["Server export policy"]
    E --> E1["/etc/exports"]
    E1 --> E2{"Security mode"}
    E2 -->|AUTH_SYS| E3["UID/GID trust boundary"]
    E2 -->|RPCSEC_GSS| E4["Kerberos: krb5 / krb5i / krb5p"]

    E1 --> F{"OS"}
    F -->|Linux| F1["exportfs -a → exportfs -v"]
    F -->|FreeBSD| F2["nfsd restart → mountd reload"]

    F1 --> G["Client mount test"]
    F2 --> G
    C3 --> G
    D3 --> G

    G --> H{"Mount behavior"}
    H -->|hard| H1["wait for server; processes may block"]
    H -->|soft| H2["return errors after retries/timeouts"]
    H --> H3["bg / intr / nfsvers / sec"]

    G --> I["Verify df + real access"]
    I --> J["Observe nfsstat -s / -c"]
    J --> K{"Problem?"}
    K -->|network loss suspected| K1["inspect netstat; consider rsize/wsize only with evidence"]
    K -->|slow server suspected| K2["inspect server/load; consider timeo/thread tuning"]
    K -->|No| L["Persist in fstab or autofs"]

    L --> M["automount maps"]
    M --> M1["indirect"]
    M --> M2["direct"]
    M --> M3["master"]
    M --> M4["replicas only read-only"]

    N["Risk boundaries"] --> N1["no_root_squash"]
    N --> N2["async"]
    N --> N3["unrestricted export"]
    N --> N4["FreeBSD V4 root = /"]
    N --> N5["umount -f"]
~~~

## Смысл диаграммы

NFS configuration состоит из двух независимых границ: server-side export/access policy и client-side mount/failure semantics. Сначала проверяется export и security scope, затем ручной mount, затем runtime statistics; только после этого конфигурацию следует переносить в fstab или automount.
