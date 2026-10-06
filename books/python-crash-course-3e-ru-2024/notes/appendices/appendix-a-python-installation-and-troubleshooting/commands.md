# Команды — приложение А

## Interpreter/version checks

```bash
python --version
python -V
```

Classification: read-only.

Windows launcher:

```text
py
```

Classification: interpreter launch.

## apt-based Linux packages

```bash
sudo apt install python3-dev python3-pip python3-venv
```

Classification: state-changing.

Effect: устанавливает source-listed development/pip/venv components.

Verification: interpreter/package workflow после установки.

Rollback: `[Needs confirmation]`.

## Source example: newer Python on apt-based Linux

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
python3.11
sudo apt install python3.11-dev python3.11-venv
```

Classification:
- repository/package operations: state-changing;
- `python3.11`: interpreter launch.

Current suitability/version availability: `[Needs confirmation]`.

Rollback: `[Needs confirmation]`.

## Windows/macOS installer actions

Source uses GUI installer steps rather than terminal commands:
- Windows: rerun installer / Modify / add Python to environment variables;
- macOS: use official Python installer.

Exact current UI/options: `[Needs confirmation]`.
