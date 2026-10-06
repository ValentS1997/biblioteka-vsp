# Команды — приложение Г

## Read-only

```bash
git --version
git status
git log
git log --pretty=oneline
```

Classification: read-only.

## Global configuration

```bash
git config --global user.name "имя_пользователя"
git config --global user.email "имя_пользователя@пример.com"
git config --global init.defaultBranch main
```

Classification: state-changing user-level configuration.

Verification: later commits/default init behavior.

Rollback: `[Needs confirmation]`.

## Initialize and stage

```bash
git init
git add .
```

Classification: state-changing.

Effect:
- creates repository metadata;
- stages/tracks relevant files except ignored paths.

Verification:

```bash
git status
```

## Commit snapshots

```bash
git commit -m "Started project."
git commit -am "Extended greeting."
```

Classification: state-changing.

Boundary:
- `-a` handles modified tracked files;
- newly created files still require `git add .`.

Verification: `git status` clean + `git log --pretty=oneline`.

## Discard uncommitted changes

```bash
git restore .
```

Classification: **destructive state-changing**.

Effect: source says all changes since last commit in tracked files are rolled back.

Risk: uncommitted work is lost.

Verification: `git status` clean.

## Inspect earlier commit

```bash
git checkout <commit-prefix>
git switch -
```

Classification:
- checkout: state-changing working tree / HEAD;
- switch back: recovery to previous branch.

Risk: source warns against editing old detached state unless you understand advanced Git behavior.

## Hard rollback to earlier commit

Source command pattern:

```bash
git reset --hard <commit-prefix>
```

Classification: **high-risk destructive state-changing**.

Source precondition:
- be on `main`;
- verify `git status`;
- inspect `git log`;
- choose the intended commit.

Effect: branch/working state is reset to the selected commit; later commits disappear from the shown branch history.

Use outside the source's solo learning repository: `[Needs confirmation]`.

## Delete repository history and start over

Source shows deleting the entire `.git` directory, then:

```bash
git init
git add .
git commit -m "Starting over."
git status
```

Classification: **destructive repository-recovery workflow**.

Effect:
- working files remain;
- all prior Git commit/history metadata is lost;
- a new root history is created.

Exact filesystem deletion command is platform-specific in source and must not be treated as routine cleanup.

Rollback after repository-history deletion: not source-supported.
