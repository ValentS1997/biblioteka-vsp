# Mermaid — глава 13 «Пользовательское окружение»

Источник: **RAG `p0390:c01`–`p0401:c01`**, PDF/печатные страницы 390–401. Диаграммы — аналитическое представление текстовых связей главы.

## 1. Startup-file change workflow

```mermaid
flowchart TD
  NEED["Need environment change"] --> WHY{"Really necessary?"}
  WHY -->|No| KEEP["Keep existing startup files"]
  WHY -->|Yes| MODE["Identify shell + login/interactive mode"]
  MODE --> FILES["Identify startup files read in that mode"]
  FILES --> SNAP["Capture current file + environment"]
  SNAP --> EDIT["Make one minimal commented change"]
  EDIT --> TEST["Open clean session / clean test user"]
  TEST --> OK{"Acceptance passes?"}
  OK -->|Yes| DIST["Distribute / keep"]
  OK -->|No| RB["Restore previous file"]
```

This operational flow synthesizes §§13.1–13.2 and §13.5.

## 2. PATH lookup model

```mermaid
flowchart LR
  CMD["Command name"] --> P1["First PATH directory"]
  P1 --> F1{"Executable found?"}
  F1 -->|Yes| RUN["Run first match"]
  F1 -->|No| P2["Next PATH directory"]
  P2 --> F2{"Found?"}
  F2 -->|Yes| RUN
  F2 -->|No| MORE["Continue search"]
  DOT[". in PATH"] --> RISK["Current directory can change command resolution"]
```

The source treats PATH order as executable-precedence policy and discourages `.` (§13.3.1).

## 3. Bash login startup path

```mermaid
flowchart TD
  START["bash login shell"] --> ETC["/etc/profile"]
  ETC --> B1{".bash_profile exists?"}
  B1 -->|Yes| BP["Run ~/.bash_profile"]
  B1 -->|No| B2{".bash_login exists?"}
  B2 -->|Yes| BL["Run ~/.bash_login"]
  B2 -->|No| B3{".profile exists?"}
  B3 -->|Yes| PR["Run ~/.profile"]
  B3 -->|No| END["No user login file from this list"]
```

The source explicitly says only the first matching user login file is run (§13.4.1).

## 4. Bash interactive non-login path

```mermaid
flowchart TD
  TERM["Interactive non-login bash"] --> SYSRC["/etc/bash.bashrc"]
  SYSRC --> USERRC["~/.bashrc"]
  USERRC --> ENV["PATH / prompt / editor / pager / umask etc."]
```

This is the chapter's source model for terminal shells (§13.4.1).

## 5. Shared bashrc strategy

```mermaid
flowchart TD
  LOGIN["Login shell"] --> BP["~/.bash_profile"]
  BP --> SRC[". $HOME/.bashrc"]
  NONLOGIN["Interactive non-login shell"] --> RC["~/.bashrc"]
  SRC --> RC
  RC --> COMMON["Common environment/settings"]
```

The source presents sourcing `.bashrc` from `.bash_profile` as a clearer alternative to symlinking the two files.

## 6. umask policy decision

```mermaid
flowchart TD
  NEED["New-file default permissions"] --> PRIV{"Privacy priority?"}
  PRIV -->|Strong| U77["umask 077"]
  PRIV -->|Shared readability needed| U22["umask 022"]
  U77 --> NEW["New files/dirs inherit restricted effective modes"]
  U22 --> NEW2["New files/dirs may be readable by others"]
  APP["Application may override umask"] --> NEW
  APP --> NEW2
```

The chapter frames 077 and 022 as trade-offs, not universal constants (§13.3.5).

## 7. Alias risk model

```mermaid
flowchart TD
  ALIAS["Alias changes command text"] --> HIDDEN["Behavior becomes less obvious"]
  HIDDEN --> ARG["Arguments can be awkward"]
  HIDDEN --> CHILD["Not inherited into child/noninteractive shells"]
  ARG --> ALT["Prefer shell function or new script"]
  CHILD --> ALT
```

This represents the source's reasons for discouraging aliases that redefine standard commands (§13.3.4).

## 8. Clean-user rollout validation

```mermaid
flowchart TD
  TEMPLATE["Candidate default startup files"] --> U1["Clean test user #1"]
  U1 --> CON["Console login"]
  U1 --> REM["Remote login"]
  U1 --> GUI["Graphical/session path"]
  U1 --> MAN["Manual pages / editor / pager"]
  CON --> PASS{"All expected behavior?"}
  REM --> PASS
  GUI --> PASS
  MAN --> PASS
  PASS -->|Yes| U2["Clean test user #2 with copied files"]
  U2 --> REP{"Repeatable?"}
  REP -->|Yes| ROLL["Ready to distribute"]
  REP -->|No| FIX["Fix template"]
```

The chapter explicitly recommends the two-test-user sequence (§13.5).

## 9. Startup-file anti-pattern boundary

```mermaid
flowchart TD
  RC["Generic shell startup file"] --> NO1["No GUI commands"]
  RC --> NO2["Do not set DISPLAY"]
  RC --> NO3["Do not force terminal type"]
  RC --> NO4["Do not emit stdout"]
  RC --> NO5["Do not set LD_LIBRARY_PATH"]
  RC --> YES["Keep short + commented"]
```

These are explicit §13.6 guidance items.
