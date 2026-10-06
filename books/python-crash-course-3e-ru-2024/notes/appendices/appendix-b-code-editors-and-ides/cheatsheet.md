# Шпаргалка — приложение Б

## Symptom / problem framing

Редактор мешает работе, если:
- неверно обрабатывает отступы;
- скрывает, где tabs, а где spaces;
- вывод перегружен служебными строками;
- часто повторяемые операции выполняются вручную;
- IDE automation становится сложнее самого Python-кода.

## Baseline / context

Source recommendation:
- если текущий editor/IDE уже работает с вашей Python version — продолжать использовать его;
- если инструмента нет — VS Code используется как учебный baseline.

## Read-only checks

В VS Code source предлагает:
- смотреть статусную строку для Spaces/Tab Size;
- выделять code lines, чтобы увидеть whitespace characters;
- просматривать Keyboard Shortcuts и commonly used settings.

## Interpretation

Python source style:
- spaces предпочтительнее tabs;
- line-length convention описана как 79 characters;
- ruler example ставится на column 80.

VS Code:
- Python extension обычно настраивает Tab как 4 spaces;
- `internalConsole` делает output короче, но read-only;
- programs с `input()` требуют interactive terminal.

## Modifying actions

Source settings example:

```json
"editor.rulers": [
    80
]
```

launch.json example:

```json
"console": "internalConsole",
"justMyCode": true
```

Classification: editor/project configuration changes.

Effect: меняет display/runtime console behavior in VS Code.

Rollback: вернуть предыдущие settings values; exact source rollback procedure `[Needs confirmation]`.

## Verification / acceptance checks

- Python indentation вводится единообразно;
- ruler отображается после save/restart if needed;
- Debug Console показывает только desired program output;
- программы с `input()` запускаются через interactive terminal;
- frequent editing operations выполняются shortcuts, если это реально ускоряет работу.

## Rollback

Source не задает centralized rollback. Для settings changes — вернуть прежние settings; для editor choice — использовать другой editor/IDE.
