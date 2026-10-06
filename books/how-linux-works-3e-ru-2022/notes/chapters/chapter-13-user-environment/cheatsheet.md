# Шпаргалка: пользовательское окружение по главе 13

## Symptom / problem framing

Типовые проблемы:

- запускается не та версия command;
- environment отличается между login shell и terminal shell;
- prompt ведёт себя неожиданно;
- новые files создаются с неправильными permissions;
- alias скрыто меняет semantics familiar command;
- GUI/session ломается после startup-file edit;
- defaults работают у автора dotfiles, но ломаются у новых users.

## Baseline / context

Source-derived startup model:

~~~text
login/session start
      ↓
system startup files
      ↓
user startup files
      ↓
PATH / exported variables / prompt / umask
      ↓
interactive programs and child processes
~~~

Principles:
- keep startup files few and short;
- comment them clearly;
- do not copy accumulated personal clutter into defaults for everyone.

## Read-only checks

### Login-shell marker

~~~bash
echo $0
~~~

According to source, leading `-` indicates a login shell.

### Interactive context

Source uses `$-`; presence of `i` means interactive context.

~~~sh
case $- in
 *i*) ...
      ;;
 *)   ...
      ;;
esac
~~~

### Rollout validation

Source-preferred behavioral validation:
1. create a clean test user;
2. apply startup files;
3. test console/remote/graphical entry paths;
4. test manuals/editor/pager;
5. create a second test user from proposed defaults;
6. verify behavior again.

Exact user-management commands are not supplied: `[Needs confirmation]`.

## Interpretation

### PATH

Baseline order:

~~~text
/usr/local/bin
/usr/bin
/bin
~~~

Optional user path: `$HOME/bin`.  
Administrative paths when needed: `/usr/local/sbin`, `/usr/sbin`, `/sbin`.

Do **not** add `.` to PATH.

### MANPATH

Do not set it merely to reproduce manual-page search paths; source says preserve system defaults from `/etc/manpath.config`.

### Prompt

~~~sh
PS1='\u\$ '
~~~

Useful source substitutions: `\u`, `\h`, `\w`, `\W`, `\!`, `\$`.

Avoid prompt characters with shell meaning, especially `>`.

### Aliases

Use sparingly. Source objections:
- argument handling is awkward;
- origin is hidden;
- they do not propagate like normal environment to child/noninteractive shells;
- they can silently alter familiar command semantics.

Prefer functions/scripts when behavior matters.

### umask

~~~text
077 → strict privacy
022 → others can read most newly created files/dirs
~~~

### Bash startup order

Login shell:

~~~text
/etc/profile
   ↓
first existing:
.bash_profile
.bash_login
.profile
~~~

Interactive non-login:

~~~text
/etc/bash.bashrc
   ↓
~/.bashrc
~~~

Source recommends common environment in `.bashrc`, sourced from `.bash_profile`:

~~~sh
. $HOME/.bashrc
~~~

### Exported defaults

~~~sh
EDITOR=vi
VISUAL=vi
PAGER=less
LESS=meiX
export PATH EDITOR VISUAL PAGER LESS
~~~

### tcsh

Startup search: `.tcshrc`, then fallback `.cshrc`. Source prefers `.cshrc` for portability.

## Next action

1. Identify shell/session type affected.
2. Determine which startup file actually runs.
3. Make one minimal change.
4. Keep PATH deterministic; do not add `.`.
5. Export only variables child processes need.
6. Preserve known-good state before modification.
7. Test on a clean user before distributing defaults.
8. Re-test login and non-login paths separately.

## Modifying action

Source-confirmed Bash examples:

~~~sh
PATH=/usr/local/bin:/usr/bin:/bin:/usr/games
PATH=$HOME/bin:$PATH
PS1='\u\$ '
EDITOR=vi
VISUAL=vi
PAGER=less
LESS=meiX
export PATH EDITOR VISUAL PAGER LESS
umask 022
. $HOME/.bashrc
~~~

Strict alternative:

~~~sh
umask 077
~~~

tcsh examples:

~~~csh
setenv PATH $HOME/bin:/usr/local/bin:/usr/bin:/bin
setenv EDITOR vi
setenv VISUAL vi
setenv PAGER less
setenv LESS meiX
set prompt="%m%% "
~~~

## Verification / acceptance checks

| Change | Verification |
|---|---|
| PATH | intended executable resolution order in new session |
| exported variables | child programs receive intended values |
| prompt | expected minimal prompt, no dangerous special chars |
| umask | new test files/dirs get intended defaults |
| .bash_profile sourcing | login shell receives intended .bashrc environment |
| login/non-login split | both contexts behave as designed |
| tcsh defaults | intended environment appears in tcsh |
| rollout defaults | second clean test user passes intended entry paths |

## Rollback

- PATH/editor/pager/prompt edits → restore previous startup-file lines from known-good copy; otherwise `[Needs confirmation]`.
- `umask` → restore previous value if captured; existing files are not retroactively changed.
- `. $HOME/.bashrc` → remove/revert sourcing line if it was the change.
- tcsh changes → restore previous `.cshrc/.tcshrc`.
- Distributed defaults → revert template and revalidate; already-created user homes may need separate repair: `[Needs confirmation]`.
