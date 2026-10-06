# Диаграмма: пользовательское окружение по главе 13

## Bash login shell

~~~mermaid
flowchart TD
    LOGIN["Login shell"] --> ETC["/etc/profile"]
    ETC --> BP{"First existing user file"}
    BP --> B1["~/.bash_profile"]
    BP --> B2["~/.bash_login"]
    BP --> B3["~/.profile"]
    B1 --> ENV["User environment"]
    B2 --> ENV
    B3 --> ENV
~~~

## Bash interactive non-login

~~~mermaid
flowchart TD
    TERM["Interactive non-login shell"] --> SYS["/etc/bash.bashrc"]
    SYS --> USER["~/.bashrc"]
    USER --> ENV["PATH / prompt / exports / umask"]
~~~

## Common .bashrc from login

~~~mermaid
flowchart LR
    BP["~/.bash_profile"] --> SOURCE[". $HOME/.bashrc"]
    SOURCE --> BR["~/.bashrc"]
    BR --> COMMON["Common environment"]
~~~

## Startup-file rollout

~~~mermaid
flowchart TD
    NEED["Need for change?"] -->|No| STOP["Do not edit"]
    NEED -->|Yes| BASE["Preserve known-good state"]
    BASE --> MIN["One minimal change"]
    MIN --> TEST1["Clean test user/session"]
    TEST1 --> PATHS["Console + remote + graphical paths"]
    PATHS --> TEST2["Second clean user from defaults"]
    TEST2 --> ACCEPT["Accept only if behavior remains consistent"]
~~~

## PATH security

~~~mermaid
flowchart LR
    USER["$HOME/bin"] --> LOCAL["/usr/local/bin"]
    LOCAL --> SYS["/usr/bin"]
    SYS --> BIN["/bin"]
    DOT[". in PATH"] --> RISK["Context-dependent / malicious executable risk"]
~~~

## Environment propagation

~~~mermaid
flowchart TD
    ASSIGN["VAR=value"] --> CURRENT["Current shell variable"]
    CURRENT --> EXPORT["export VAR"]
    EXPORT --> CHILD["Child process environment"]
    SOURCE[". file"] --> CURRENT
~~~

## Safety boundary

~~~mermaid
flowchart TD
    START["Startup file"] --> GOOD["PATH / prompt / editor / pager / umask"]
    START --> BAD["DISPLAY / terminal type / stdout / LD_LIBRARY_PATH"]
    BAD --> FAIL["Hard-to-debug session/tool breakage"]
~~~
