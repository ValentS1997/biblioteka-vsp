# Команды и инструменты главы 2

Only commands/directives explicitly present in RAG `p0034:c01–p0049:c01`.

## Command inventory

| Command / action | Type | Source purpose | Verification | Rollback |
|---|---|---|---|---|
| `docker run -d <образ-приложения>` | state-changing | запустить application container | `docker ps` | `[Needs confirmation]` |
| `docker ps` | read-only | показать запущенные containers / найти ID | container appears in list | Not applicable |
| extracted topz `docker run ...` | state-changing | запустить topz beside application in same PID namespace | `http://localhost:8080/topz` | `[Needs confirmation]` |
| `git pull` | state-changing | обновить shared filesystem из Git repository | file update / application reaction: `[Needs confirmation]` | `[Needs confirmation]` |
| `sleep 10` | read-only | задержка между Git sync iterations; persistent configuration/data не меняет | loop interval observable | Not applicable |
| `docker run -e=PORT=<порт> -d <образ>` | state-changing | передать parameter через environment variable и запустить container | container-specific: `[Needs confirmation]` | `[Needs confirmation]` |
| `docker run -e=PROXY_PORT=8080 -e=CERTIFICATE_PATH=/путь/к/сертификату.crt ...` | state-changing | передать proxy port и certificate path | generated nginx config: `[Needs confirmation]` | `[Needs confirmation]` |

## 1. Application container

~~~bash
docker run -d <образ-приложения>
~~~

Source behavior:
- starts a container;
- returns a container identifier.

If ID is unknown:

~~~bash
docker ps
~~~

Source behavior:
- lists currently running containers.

## 2. topz Sidecar

RAG-extracted command on PDF p.41:

~~~text
docker run --pid=container:${APP_ID} \
    -  p 8080:8080 \
    brendanburns/topz:db0fa58
    /server -addr 0.0.0.0:8080
~~~

Classification: state-changing.

Important:
- the `-  p` fragment is preserved exactly as extracted;
- it is classified as `[Source extraction issue]`;
- do not copy/paste as a verified executable command;
- intended spelling is `[Needs confirmation]` under rag_only policy.

Source-supported effect:
- topz joins application container PID namespace;
- service listens on address/port shown;
- author notes port may need changing if application already uses 8080.

Verification from source:

~~~text
http://localhost:8080/topz
~~~

Expected conceptual result:
- process/resource information for application container.

## 3. Git-sync loop

Source script:

~~~bash
#!/bin/bash

while true; do
  git pull
  sleep 10
done
~~~

Purpose:
- repeatedly synchronize shared filesystem with Git repository.

Risk:
- state of shared application files changes every successful pull;
- conflict/error behavior is not defined in chapter;
- source says the script is intentionally simplified.

Verification:
- sidecar updates files as changes are pushed to repository;
- exact Git status/commit verification command: `[Needs confirmation]`.

Rollback:
- `[Needs confirmation]`.

## 4. Parameterized container

Source:

~~~bash
docker run -e=PORT=<порт> -d <образ>
~~~

Preferred source approach:
- environment variables rather than command-line parameters.

Example:

~~~bash
docker run -e=PROXY_PORT=8080 \
  -e=CERTIFICATE_PATH=/путь/к/сертификату.crt ...
~~~

Source behavior:
- container startup script reads variables;
- uses them to generate/adjust configuration such as `nginx.conf`.

## 5. Signals mentioned by source

The chapter names:
- `SIGHUP`;
- `SIGKILL`.

No exact shell command syntax is provided.

### SIGHUP

Purpose in source:
- one possible mechanism for telling application to reread configuration.

Type:
- state-changing.

Verification:
- application-specific: `[Needs confirmation]`.

Rollback:
- `[Needs confirmation]`.

### SIGKILL

Purpose in source:
- last-resort termination so orchestrator restarts legacy application.

Type:
- state-changing / disruptive.

Risk:
- forcibly terminates application.

Verification:
- orchestrator restart + application loads new configuration.

Exact command/rollback:
- `[Needs confirmation]`.

## 6. Dockerfile directives

These are source-confirmed image/configuration directives, not runtime shell commands.

### EXPOSE

~~~dockerfile
# Главный сервер принимает запросы на порт 8080
EXPOSE 8080
~~~

Purpose:
- document exposed network port.

### ENV

~~~dockerfile
# Параметр PROXY_PORT обозначает порт, на который необходимо
# перенаправлять запросы
ENV PROXY_PORT 8000
~~~

Purpose:
- document/provide default environment variable.

### LABEL

Source example:

~~~dockerfile
LABEL "org.label-schema.vendor"="name@company.com"
LABEL "org.label.url"="http://images.company.com/my-cool-image"
LABEL "org.label-schema.version"="1.0.3"
~~~

The namespace difference in the middle key is preserved exactly and marked `[Needs confirmation]` in source findings.

## Safety boundary

Do not add:
- Kubernetes YAML;
- nginx config;
- docker stop/rm commands;
- certificate generation commands;
- Git conflict handling;
- modern Docker replacements/options;

unless supported by another explicit source scope.
