# Диаграмма: запуск пользовательского пространства по главе 6

## От kernel к user space

~~~mermaid
flowchart TB
    K["Kernel mounts root filesystem"] --> INIT["init / PID 1"]
    INIT --> LOW["Low-level services<br/>udevd · logging"]
    LOW --> NET["Network configuration"]
    NET --> MID["Mid/high-level services"]
    MID --> LOGIN["Login prompts / GUI / applications"]
~~~

## systemd unit model

~~~mermaid
flowchart LR
    TARGET["target unit"] --> SVC["service unit"]
    TARGET --> MNT["mount unit"]
    TARGET --> SOCK["socket unit"]
    SOCK -->|"request arrives"| SVC
    SVC --> CG["cgroup / process tree"]
    DEP["Wants / Requires"] --> SVC
    ORD["Before / After"] --> SVC
~~~

## Unit troubleshooting

~~~mermaid
flowchart TD
    A["service/unit problem"] --> B["systemctl status"]
    B --> C["journalctl --unit"]
    C --> D["Loaded path + cgroup + jobs"]
    D --> E["Dependencies / ordering"]
    E --> F{"Need config change?"}
    F -->|No| G["Finish"]
    F -->|Yes| H["Edit local config in /etc/systemd/system"]
    H --> I["daemon-reload / reload"]
    I --> J["start/restart if required"]
    J --> B
~~~

## Enable vs activate

~~~mermaid
flowchart LR
    E["systemctl enable"] --> LINK["dependency symlink"]
    LINK --> FUTURE["future boot/activation graph"]
    S["systemctl start"] --> NOW["unit active now"]
~~~

## Initramfs handoff

~~~mermaid
flowchart TB
    BL["Bootloader"] --> KERN["Kernel"]
    BL --> RAM["initramfs archive in RAM"]
    KERN --> TMP["temporary RAM root"]
    RAM --> TMP
    TMP --> I1["init in initramfs"]
    I1 --> MOD["load storage/root modules"]
    MOD --> REAL["mount real root"]
    REAL --> SWITCH["switch to real root"]
    SWITCH --> I2["full init / systemd"]
~~~

## Controlled shutdown

~~~mermaid
flowchart TB
    S["shutdown"] --> N["notify users / restrict new logins"]
    N --> T["terminate services/processes"]
    T --> U["unmount filesystems"]
    U --> R["root remount read-only"]
    R --> SY["sync buffered data"]
    SY --> K["kernel reboot / halt"]
~~~
