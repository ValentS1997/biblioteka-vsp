# Диаграмма: сценарии оболочки по главе 11

## Script execution

~~~mermaid
flowchart TD
    F["Script file"] --> MODE["read + execute permission"]
    MODE --> SHEBANG["shebang"]
    SHEBANG --> INT["Interpreter /bin/sh"]
    INT --> PARSE["parse + expansion + redirection"]
    PARSE --> CMD["run command"]
    CMD --> RC["return code"]
    RC --> FLOW["if / && / || / loops"]
~~~

## Arguments and return state

~~~mermaid
flowchart LR
    CLI["command line"] --> A1["$1 $2 ..."]
    CLI --> AC["$#"]
    CLI --> ALL["$@"]
    SCRIPT["script"] --> NAME["$0"]
    SHELL["shell process"] --> PID["$$"]
    CMD["last command"] --> RC["$?"]
    A1 --> SHIFT["shift changes positional view"]
~~~

## Conditional flow

~~~mermaid
flowchart TD
    IF["if command"] --> R{"return code == 0?"}
    R -->|Yes| THEN["then branch"]
    R -->|No| ELSE["else / elif branch"]
    THEN --> FI["fi"]
    ELSE --> FI
~~~

## Temporary file lifecycle

~~~mermaid
flowchart TD
    START["script"] --> TMP["mktemp"]
    TMP --> WORK["write/read temporary file"]
    WORK --> CLEAN["rm -f cleanup"]
    START --> TRAP["trap INT"]
    TRAP --> INTERRUPT["Ctrl+C / INT"]
    INTERRUPT --> CLEAN2["rm -f temp files"]
    CLEAN2 --> EXIT["exit 1"]
~~~

## Filename-safe batch processing

~~~mermaid
flowchart LR
    FIND["find"] --> NULL["-print0"]
    NULL --> XARGS["xargs -0"]
    XARGS --> CMD["target command"]
    FIND --> EXEC["alternative: -exec ... {} \;"]
~~~

## Subshell vs sourcing

~~~mermaid
flowchart TB
    P["Parent shell"] --> SUB["( commands ) subshell"]
    SUB --> TEMPENV["temporary cwd/PATH changes"]
    TEMPENV --> END["subshell exits"]
    END --> P

    P --> SOURCE[". config.sh"]
    SOURCE --> SAME["commands execute in parent shell"]
    SAME --> PERSIST["variables/definitions persist"]
~~~

## Complexity boundary

~~~mermaid
flowchart TD
    TASK["Task"] --> Q{"Commands/files/simple flow?"}
    Q -->|Yes| SH["Shell script"]
    Q -->|No: complex strings/arithmetic/control| LANG["Python / Perl / awk"]
~~~
