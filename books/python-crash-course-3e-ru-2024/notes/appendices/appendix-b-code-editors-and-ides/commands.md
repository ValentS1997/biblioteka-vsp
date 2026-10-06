# Команды и операции — приложение Б

Приложение в основном описывает GUI/editor operations, а не shell commands.

## VS Code project configuration

Source creates/edits `settings.json` and `launch.json`.

Example ruler:

```json
"editor.rulers": [80]
```

Classification: state-changing editor configuration.

Example console mode:

```json
"console": "internalConsole",
"justMyCode": true
```

Classification: state-changing project/debug configuration.

Verification: save configuration and rerun program.

Rollback: restore previous setting values; exact process `[Needs confirmation]`.

## Run without debugging

Source shortcut:

```text
Ctrl+F5
```

Classification: workload-generating.

Effect: runs current program.

## High-frequency shortcuts

Indent:
```text
Ctrl+]      / macOS: Command+]
```

Unindent:
```text
Ctrl+[      / macOS: Command+[
```

Toggle comment:
```text
Ctrl+/      / macOS: Command+/
```

Move code:
```text
Alt+Up/Down / macOS: Option+Up/Down
```

Toggle explorer:
```text
Ctrl+B      / macOS: Command+B
```

Classification: editor actions, not repository/system changes.

## Interactive-input boundary

Source states that Debug Console is read-only. Programs using `input()` should use the integrated/external terminal instead.
