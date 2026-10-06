# Команды и конфигурационные конструкции главы 13

Только команды, shell assignments и startup constructs, явно подтверждённые RAG главы 13.

| Команда / конструкция | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `echo $0` | Identify login-shell marker | read-only | Prints shell value/name | None | Leading `-` interpreted by source as login shell | N/A |
| `PATH=/usr/local/bin:/usr/bin:/bin:/usr/games` | Set command path example | shell-state-changing | Replaces current PATH | Wrong order changes executable resolution | Verify new-session resolution | Restore previous PATH |
| `PATH=$HOME/bin:$PATH` | Prepend user bin | shell-state-changing | User bin gets higher precedence | User executable can override system command | Verify intended resolution | Remove/revert prepend |
| `PS1='\u\$ '` | Minimal Bash prompt | shell-state-changing | Changes prompt | Bad special chars can cause confusion/redirection issues | Inspect new interactive shell | Restore prior PS1 |
| `EDITOR=vi` | Set editor variable | shell-state-changing | Changes shell variable | Not inherited until exported | Verify intended consumer | Restore value |
| `VISUAL=vi` | Set visual editor variable | shell-state-changing | Changes shell variable | Same | Verify consumer | Restore value |
| `PAGER=less` | Set pager variable | shell-state-changing | Changes shell variable | Not inherited until exported | Verify pager behavior | Restore value |
| `LESS=meiX` | less options example | shell-state-changing | Changes less behavior after export | UI behavior changes | Verify less/man behavior | Restore value |
| `export PATH EDITOR VISUAL PAGER LESS` | Export environment | shell-state-changing | Child processes inherit values | Broken values propagate | Verify child program behavior | Restore previous exports |
| `umask 022` | Default permission mask | shell-state-changing/security | Changes mode mask for future objects | More readable-by-others than 077 | Create controlled test objects | Restore prior umask |
| `umask 077` | Strict default mask | shell-state-changing/security | Restricts future objects | Can interfere with intended sharing/services | Create controlled test objects | Restore prior umask |
| `. $HOME/.bashrc` | Source common config | state-changing/shell-context | Executes .bashrc in current shell | Bad config applies immediately | Login shell gets intended environment | Revert source line / known-good file |
| `case $- in ... esac` | Branch by interactive state | control-flow | Selects startup commands from shell flags | Wrong branch can run unsuitable commands | Test intended contexts | Revert branch |
| `setenv PATH $HOME/bin:/usr/local/bin:/usr/bin:/bin` | tcsh PATH example | shell-state-changing | Sets exported PATH | Changes executable resolution | Verify tcsh resolution | Restore prior .cshrc value |
| `setenv EDITOR vi` | tcsh editor | shell-state-changing | Sets EDITOR | Changes program default | Verify behavior | Restore |
| `setenv VISUAL vi` | tcsh visual editor | shell-state-changing | Sets VISUAL | Changes program default | Verify behavior | Restore |
| `setenv PAGER less` | tcsh pager | shell-state-changing | Sets PAGER | Changes pager choice | Verify behavior | Restore |
| `setenv LESS meiX` | tcsh less options | shell-state-changing | Sets LESS | Changes less behavior | Verify behavior | Restore |
| `set prompt="%m%% "` | tcsh prompt | shell-state-changing | Changes prompt | Poor prompt design can confuse | Inspect prompt | Restore |
| `chsh` | Change login shell; source mention only | state-changing/account | Changes user shell choice | Full invocation/validation workflow absent | `[Needs confirmation]` | `[Needs confirmation]` |

## Startup order named by source

Bash login shell:
1. `/etc/profile`
2. first existing of `~/.bash_profile`, `~/.bash_login`, `~/.profile`.

Bash interactive non-login:
1. `/etc/bash.bashrc`
2. `~/.bashrc`.

tcsh/csh:
1. `~/.tcshrc`
2. fallback `~/.cshrc`.

## PATH elements named by source

- `/usr/local/bin`
- `/usr/bin`
- `/bin`
- `$HOME/bin`
- `$HOME/.local/bin` noted as a current user-binary location
- `/usr/local/sbin`
- `/usr/sbin`
- `/sbin`

Source explicitly advises **not** adding `.`.

## Variables and anti-patterns

Named variables:
- `PATH`, `PS1`, `EDITOR`, `VISUAL`, `PAGER`, `LESS`;
- `MANPATH` — normally do not set manually;
- `DISPLAY` — do not set in startup file;
- `LD_LIBRARY_PATH` — source says never set in startup file;
- `$-` — used for interactive-state check.

Source also says:
1. no graphical commands in shell startup files;
2. no hard-coded terminal type;
3. no commands that print to stdout;
4. avoid aliases that silently change standard command semantics;
5. do not distribute untested personal dotfiles as defaults.
