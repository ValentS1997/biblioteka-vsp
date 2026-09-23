# Диаграмма: Samba authentication → share policy → filesystem access

~~~mermaid
flowchart TD
    A["Client needs SMB share"] --> B["Read-only config check: testparm -v"]
    B --> C{"Authentication model"}

    C -->|Local| D["UNIX account exists"]
    D --> D1["smbpasswd -a user"]
    D1 --> E["Samba authentication"]

    C -->|Active Directory| F["sssd / Kerberos / keytab"]
    F --> E

    E --> G["Share section in smb.conf"]
    G --> G1["path"]
    G --> G2["valid users / group"]
    G --> G3["read only / guest ok"]
    G --> G4["create/directory masks"]

    G --> H["UNIX filesystem permissions"]
    H --> H1["owner/group"]
    H --> H2["mode / setgid"]
    H --> I["Effective file access"]

    J["Network boundary"] --> J1["hosts allow"]
    J --> J2["hosts deny overrides allow"]
    J --> J3["firewall: SMB ports"]

    K["Client verification"] --> K1["smbclient -L"]
    K1 --> K2["smbclient share"]
    K2 --> K3["mount cifs/smbfs"]

    L["Troubleshooting"] --> L1["smbstatus"]
    L1 --> L2["sessions / shares / locks / PID"]
    L2 --> L3["logs"]
    L3 --> L4["temporary smbcontrol debug"]

    M["Risk boundaries"] --> M1["broad share/guest access"]
    M --> M2["wrong UNIX permissions"]
    M --> M3["external SMB exposure"]
    M --> M4["high debug leaks sensitive data"]
    M --> M5["killing smbd can break clients"]

    I --> K
    J --> K
~~~

## Смысл диаграммы

Samba access — это пересечение трех policy layers: authentication identity, share policy и UNIX filesystem permissions. Диагностика должна сначала подтвердить effective config и authentication/share visibility через smbclient, затем local mount, а при runtime problems — smbstatus и logs.
