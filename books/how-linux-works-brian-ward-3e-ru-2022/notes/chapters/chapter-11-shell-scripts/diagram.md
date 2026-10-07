# Mermaid — глава 11 «Сценарии оболочки»

Источник: **RAG `p0344:c01`–`p0367:c01`**, PDF/печатные страницы 344–367. Диаграммы — аналитическое представление текста главы.

## 1. Script execution path

```mermaid
flowchart TD
  FILE["Executable script file"] --> K["Kernel"]
  K --> SHEBANG["Read shebang"]
  SHEBANG --> SH["Start interpreter, e.g. /bin/sh script"]
  SH --> PARSE["Parse shell syntax"]
  PARSE --> EXPAND["Expand variables / globs / substitutions"]
  EXPAND --> EXEC["Execute command(s)"]
  EXEC --> STATUS["Collect exit status"]
```

The chapter treats a shell script as a file of commands executed by the interpreter named in the shebang (§11.1).

## 2. Quoting / expansion boundary

```mermaid
flowchart TD
  TOKEN["Shell input text"] --> Q{"Quoting?"}
  Q -->|Single quotes| LIT["Literal: no shell expansion"]
  Q -->|Double quotes| VAR["Variable expansion allowed; wildcard protected in shown examples"]
  Q -->|Unquoted| FULL["Variable + glob + other shell expansion"]
  LIT --> ARG["Arguments passed to command"]
  VAR --> ARG
  FULL --> ARG
```

The main failure mode described in §11.2 is the shell changing text before the target command sees it.

## 3. Exit status drives control flow

```mermaid
flowchart TD
  CMD["Run command / test"] --> RC["Exit status"]
  RC --> Z{"Status = 0?"}
  Z -->|Yes| TRUE["True / success path"]
  Z -->|No| FALSE["False / nonzero path"]
  TRUE --> IF["if / while / &&"]
  FALSE --> ELSE["else / stop while / ||"]
  RC --> Q["$? stores latest status only"]
```

The chapter explicitly warns that tools such as `grep` and `diff` can assign application-specific meaning to nonzero statuses (§11.4).

## 4. test / [ model

```mermaid
flowchart LR
  INPUT["Arguments"] --> TEST["test / ["]
  TEST --> FILE["File predicates"]
  TEST --> STR["String predicates"]
  TEST --> NUM["Numeric predicates"]
  FILE --> RC["0=true / nonzero=false"]
  STR --> RC
  NUM --> RC
  RC --> FLOW["if / while / logical operators"]
```

§11.5 emphasizes that `[` behaves like a command interface, so spaces and argument boundaries matter.

## 5. case vs if/elif

```mermaid
flowchart TD
  VALUE["Value, e.g. $1"] --> CASE["case patterns"]
  CASE --> P1["bye)"]
  CASE --> P2["hi|hello)"]
  CASE --> P3["what*)"]
  CASE --> P4["*) default"]
  P1 --> END[";; → esac"]
  P2 --> END
  P3 --> END
  P4 --> END
```

The chapter recommends `case` for many string-matching branches (§11.5.6).

## 6. Temporary-file lifecycle

```mermaid
flowchart TD
  START["Script starts"] --> TMP["mktemp creates unique file(s)"]
  TMP --> WORK["Write/read temporary data"]
  WORK --> DONE{"Normal finish?"}
  DONE -->|Yes| RM["rm temporary files"]
  DONE -->|No: INT| TRAP["trap handler"]
  TRAP --> RM
  RM --> EXIT["exit / script ends"]
```

Without signal cleanup, interrupted scripts can leave stale files under `/tmp` (§11.8).

## 7. Command substitution and pipelines

```mermaid
flowchart LR
  C1["Command 1"] --> PIPE["stdout pipe"]
  PIPE --> C2["Command 2"]
  C2 --> OUT["stdout"]
  OUT --> SUB["$(...) command substitution"]
  SUB --> VAR["Shell variable / argument"]
```

The chapter warns against overusing command substitution for filename enumeration (§11.7).

## 8. Filename-safe batch processing

```mermaid
flowchart LR
  FIND["find ... -print0"] --> NULL["NUL-delimited names"]
  NULL --> XARGS["xargs -0"]
  XARGS --> CMD["Target command"]
```

This flow is source-recommended when filenames may contain spaces/newlines (§11.10.4).

## 9. Process/environment contexts

```mermaid
flowchart TD
  SHELL["Current shell"] --> SUB["(...) subshell"]
  SUB --> TEMP["Temporary cwd/env changes"]
  TEMP --> RETURN["Subshell exits; parent unchanged"]
  SHELL --> SRC[". config.sh"]
  SRC --> CURRENT["Changes current shell environment"]
  SHELL --> EX["exec command"]
  EX --> REPLACE["Current shell process is replaced"]
```

Subshells isolate changes; sourcing imports them; `exec` replaces the process (§11.10.6–11.12).

## 10. Tool-choice boundary

```mermaid
flowchart TD
  TASK["Automation task"] --> SIMPLE{"Mostly commands + files?"}
  SIMPLE -->|Yes| SHELL["Short shell script"]
  SIMPLE -->|No| COMPLEX["Complex strings/arithmetic/data/control flow"]
  COMPLEX --> LANG["Python / Perl / awk / compiled language"]
  SHELL --> GROW{"Script keeps growing?"}
  GROW -->|No| KEEP["Keep shell"]
  GROW -->|Yes| LANG
```

This is the chapter's recurring design guidance: shell is a composition tool, not a universal programming language.
