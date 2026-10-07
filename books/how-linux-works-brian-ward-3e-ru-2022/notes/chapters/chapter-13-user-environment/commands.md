# Команды и интерфейсы — глава 13 «Пользовательское окружение»

**Provenance:** `p0390:c01`–`p0401:c01`, PDF/печатные страницы 390–401. Только явно поддержанные chapter RAG команды/constructs.

Классы: **RO** — read-only observation; **SC** — state-changing shell/session configuration; **SC-P** — persistent startup-file change.

## 1. PATH and environment inspection

```sh
echo "$PATH"
echo "$0"
echo "$-"
echo "$PS1"
echo "$EDITOR"
echo "$VISUAL"
echo "$PAGER"
umask
```

Source PATH components:

```text
/usr/local/bin
/usr/bin
/bin
$HOME/bin
/usr/local/sbin
/usr/sbin
/sbin
```

The chapter also notes `$HOME/.local/bin` as a current user-binary location.

## 2. PATH assignment

Source-style examples:

```sh
PATH=/usr/local/bin:/usr/bin:/bin:/usr/games
PATH=$HOME/bin:$PATH
export PATH
```

**Class:** SC in current shell; SC-P when stored in startup file.

Boundary:
- earlier path entries have higher command-name precedence;
- source strongly discourages adding `.` to PATH;
- do not append every application installation directory merely to make it runnable.

## 3. Prompt

Source bash example:

```sh
PS1='\u\$ '
```

Source prompt expansions:

| Expansion | Meaning |
|---|---|
| `\u` | username |
| `\h` | short hostname |
| `\!` | history number |
| `\w` | current working directory |
| `\W` | last component of current directory |
| `\$` | `$` for regular user, `#` for superuser |

The source warns against prompt characters with shell meaning, especially `>`.

## 4. Alias/function guidance

The chapter discusses aliases conceptually and says shell functions/new scripts are often clearer than silently changing existing commands.

Observation:

```sh
which command
```

Source wording says `which` can identify an alias but not where it was created. No alias-definition command is promoted as an operational recommendation.

## 5. umask

Source examples:

```sh
umask 077
umask 022
```

**Class:** SC current shell / SC-P in startup file.

Source framing:
- `077`: private defaults for multi-user privacy;
- `022`: permits read access for others where creation mode allows it, useful in some single-user/service scenarios;
- some applications override `umask` internally.

## 6. Bash startup files

Source startup paths:

```text
/etc/profile
~/.bash_profile
~/.bash_login
~/.profile
/etc/bash.bashrc
~/.bashrc
```

Source model for login bash:
1. run `/etc/profile`;
2. find user files `.bash_profile`, `.bash_login`, `.profile`;
3. run only the first one found.

Source model for interactive non-login bash:
1. `/etc/bash.bashrc`;
2. `~/.bashrc`.

The chapter proposes either:
- symlink `.bash_profile` to `.bashrc`; or
- create `.bash_profile` that contains:

```sh
. $HOME/.bashrc
```

The second form is an explicit source command and is **SC-P** when written into the login startup file.

## 7. Login / interactive checks

Source:

```sh
echo $0
```

If first character of output is `-`, the source treats the shell as a login shell.

Source says login mode may be forced with:

```text
-l
--login
```

Source interaction test:

```sh
case $- in
 *i*)
    command
    ;;
 *)
    command
    ;;
esac
```

This is a control-flow example, not a copy-paste policy template.

## 8. Default environment example

The chapter's compact bash startup example includes:

```sh
PATH=/usr/local/bin:/usr/bin:/bin:/usr/games
PATH=$HOME/bin:$PATH
PS1='\u\$ '
EDITOR=vi
VISUAL=vi
PAGER=less
LESS=meiX
export PATH EDITOR VISUAL PAGER LESS
umask 022
```

These values are edition/source defaults, not universal target-system policy.

## 9. tcsh/csh source constructs

Source startup files:

```text
~/.tcshrc
~/.cshrc
```

Source example constructs:

```csh
setenv PATH $HOME/bin:/usr/local/bin:/usr/bin:/bin
setenv EDITOR vi
setenv VISUAL vi
setenv PAGER less
setenv LESS meiX
umask 022
set prompt="%m%% "
```

The chapter recommends `.cshrc` over `.tcshrc` for broader csh compatibility in its source context.

## 10. User-default testing workflow

The source recommends:
1. create a test user with an empty home directory;
2. write startup files from scratch;
3. test console, remote and graphical/login paths;
4. test manual-page and desktop behavior;
5. create a second test user and copy the first user's startup files;
6. distribute only after repeatability is confirmed.

No concrete user-creation command is supplied in this chapter, so none is invented here.

## 11. Commands/settings explicitly discouraged in startup files

The source says not to:
- run graphical commands;
- set `DISPLAY`;
- set terminal type;
- emit stdout;
- set `LD_LIBRARY_PATH`.

These are policy findings, not commands to execute.

## Command discipline

- Startup files are executable code and can affect every session/user that reads them.
- PATH order and `umask` are policy decisions, not cosmetic preferences.
- Test in a fresh shell/session; sourcing a file into the current shell is not equivalent to a clean login-path test.
- Do not add commands or distro-specific startup semantics absent from chapter RAG.
