# Команды — приложение Д

## Deployment attempt

```bash
platform push
```

Classification: state-changing remote deployment/workload-generating.

Verification: inspect output; successful deployment should not contain errors.

Rollback: `[Needs confirmation]`.

## Set Platform.sh remote mapping

Source pattern:

```bash
platform project:set-remote <project-id>
```

Classification: state-changing local/remote project configuration.

Use only the project ID actually returned for the target account/project.

Verification: CLI reports remote project set; retry deployment.

Rollback: `[Needs confirmation]`.

## Platform.sh CLI installer

Source:

```bash
curl -fsS https://platform.sh/cli/installer | php
```

Classification: state-changing remote-installer execution.

Source explanation:
- `curl` downloads the installer;
- `-f`, `-s`, `-S` modify curl behavior;
- pipe sends installer to PHP.

Risk boundary: execute only when source/provider is trusted and command purpose is understood.

Current installer URL/behavior: `[Needs confirmation]`.

## Windows verification

Source:

```bash
platform list
```

Classification: read-only/discovery.

Expected: list of Platform.sh CLI commands.

## macOS package example

```bash
brew install php
```

Classification: state-changing package installation.

Verification: PHP becomes available and CLI installer can run.

Rollback: `[Needs confirmation]`.

## Linux package example

When system reports curl/PHP missing, source shows:

```bash
sudo apt install curl php-cli
```

Classification: state-changing system package installation.

Verification: rerun CLI installer.

Rollback: `[Needs confirmation]`.

## Windows source path

Source describes installing PHP through XAMPP and adding the PHP directory to Windows Path, then running the Platform.sh installer from an administrator terminal.

Exact current UI/path/install behavior: `[Needs confirmation]`.
