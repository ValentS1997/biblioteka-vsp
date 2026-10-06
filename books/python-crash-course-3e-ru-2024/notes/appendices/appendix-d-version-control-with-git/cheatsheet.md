# Шпаргалка — приложение Г

## Symptom / problem framing

Нужно:
- фиксировать работоспособные состояния;
- видеть измененные/untracked files;
- безопасно экспериментировать;
- понимать, как вернуться к прежнему состоянию.

## Baseline / context

Source workflow рассчитан на небольшой локальный project.

Перед modifying Git action:

```bash
git status
```

Classification: read-only.

## Read-only checks

```bash
git --version
git status
git log
git log --pretty=oneline
```

Classification: read-only.

## Next action

Initial project:

```text
.gitignore
→ git init
→ git status
→ git add .
→ git commit -m "..."
→ git status = clean
```

Subsequent tracked changes:

```text
edit
→ git status
→ git commit -am "..."
→ git status
→ git log --pretty=oneline
```

Новые files требуют отдельного `git add .`.

## Modifying actions

### Initialize

```bash
git init
```

Effect: создает `.git`.

### Stage new files

```bash
git add .
```

Effect: добавляет non-ignored changes/new files в staging awareness.

### Commit

```bash
git commit -m "Started project."
git commit -am "Extended greeting."
```

Effect: создает snapshot.

### Discard uncommitted tracked changes

```bash
git restore .
```

Risk: **destructive to uncommitted changes**.

Verification: `git status` должен показать clean state.

## Historical inspection

Source:

```bash
git checkout <commit-prefix>
git switch -
```

Первое действие переводит в detached HEAD для просмотра старой commit; второе возвращает на предыдущую branch.

## High-risk rollback

Source показывает hard reset к старой commit и отдельно полное удаление `.git` с повторной инициализацией.

Оба действия **high risk / destructive**. Перед применением вне учебного одиночного repository требуется отдельный recovery plan.

## Verification / acceptance

После каждого сохраненного working state:

```text
On branch main
nothing to commit, working tree clean
```

## Rollback

Source-supported rollback зависит от ситуации:
- uncommitted changes → restore;
- inspect old commit → checkout + switch back;
- discard later branch history → hard reset;
- corrupted solo repository → remove .git + re-init.

Последние два сценария не являются routine rollback.
