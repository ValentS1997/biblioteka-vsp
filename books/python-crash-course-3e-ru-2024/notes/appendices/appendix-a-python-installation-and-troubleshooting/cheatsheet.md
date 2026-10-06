# Шпаргалка — приложение А

## Symptom / problem framing

Типовые проблемы source:

- Windows не распознает `python`;
- macOS запускает не ту Python version;
- Linux использует старую/system version;
- непонятно, какой interpreter реально запускается;
- имена переменных конфликтуют с keywords/built-ins.

## Baseline / context

Сначала нужно определить:
- операционную систему;
- команду запуска: `python`, `python3`, `py` или versioned executable;
- фактическую версию interpreter.

## Read-only checks

```bash
python --version
python -V
```

Classification: read-only.

На Windows source предлагает попробовать:

```text
py
```

как launcher, если `python` не распознается.

## Interpretation

Windows:
- если `py` работает, source разрешает использовать его вместо `python`/ `python3`;
- частая причина отказа `python` — interpreter path не добавлен в PATH.

macOS:
- source рекомендует официальный installer;
- на старых macOS `python` может ссылаться на Python 2, поэтому используется `python3`.

Linux:
- source предполагает preinstalled Python;
- для development packages нужны dev/pip/venv components;
- пример отдельной новой версии использует versioned command.

## Modifying actions

Source examples для apt-based Linux:

```bash
sudo apt install python3-dev python3-pip python3-venv
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo apt install python3.11-dev python3.11-venv
```

Classification: state-changing system/package operations.

Effect: меняют system package state.

Rollback: `[Needs confirmation]`.

## Verification / acceptance checks

- запускается ожидаемый interpreter;
- `--version` показывает ожидаемую версию;
- после PATH change открыт новый terminal;
- выбранная command form используется последовательно в примерах книги.

## Naming boundary

Keywords использовать как variable names нельзя.

Built-in function names source также рекомендует не использовать как variable names, потому что это изменяет доступ к built-in behavior.

## Rollback

Source не задает общий rollback для installer/package changes: `[Needs confirmation]`.
