# Шпаргалка — приложение Д

## Symptom / problem framing

Deployment failed.

Не начинать с случайных изменений. Сначала определить, на каком этапе цепочки произошел failure.

## Baseline / context

Source deployment stages:

```text
remote server
→ connection
→ code copy
→ dependencies
→ database + migrations
→ static files
→ application server
→ request routing
```

## Read-only checks

Главный источник evidence — deployment output/log.

Искать:
- какие шаги завершились успешно;
- где появился первый actionable error;
- какие последние errors подтверждают root failure;
- warnings vs actual errors.

Source principle: successful deployment может содержать warnings, но не errors.

## Interpretation

Пример source:
- `gunicorrn` в requirements_remote.txt приводит к package-resolution error;
- проблема находится в dependency spelling, а не в остальных cascade messages.

Другой пример:
- Platform.sh не связан с local Git repository;
- CLI выводит конкретную команду для установки remote mapping.

## Next action

1. Прочитать output.
2. Выделить stage, где начался failure.
3. Проверить prerequisites именно этого stage.
4. Исправить одну локализованную причину.
5. Повторить deployment.
6. Снова прочитать output и проверить результат.

## Modifying actions

Source examples включают:
- Platform.sh remote mapping;
- installation of CLI prerequisites;
- Platform.sh CLI installer;
- repeated deployment push.

Classification: state-changing.

Rollback: зависит от конкретного action; общий rollback source не задает.

## OS-specific prerequisites

CLI installation model в source требует:
- `curl`;
- `php`;
- Git;
- Bash-compatible terminal.

Windows:
- WSL preferred path in source;
- Git Bash alternative.

macOS:
- install PHP if missing.

Linux:
- install missing curl/PHP packages.

## Verification / acceptance checks

- installer prerequisites resolved;
- Platform.sh CLI command list works;
- local project linked to intended remote;
- deployment output has no errors;
- deployed project responds as expected.

## Rollback

`[Needs confirmation]` per platform/action. Source emphasizes targeted correction + redeploy rather than generic destructive recovery.
