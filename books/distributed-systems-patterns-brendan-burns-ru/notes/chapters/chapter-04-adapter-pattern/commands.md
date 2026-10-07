# Команды и инструменты главы 4

Only commands, directives and executable examples explicitly supported by RAG `p0064:c01–p0076:c01`.

## Command inventory

| Command / action | Type | Source purpose | Verification | Rollback |
|---|---|---|---|---|
| `docker logs` | read-only | доступ к stdout/stderr container logs | log output visible | Not applicable |
| `kubectl logs` | read-only | доступ к container logs в Kubernetes | log output visible | Not applicable |
| `db-check ...` example | workload-generating / runtime service | выполнять DB diagnostic query через HTTP health Adapter | HTTP 200/500 behavior | `[Needs confirmation]` |

Глава также содержит Kubernetes Pod YAML и fluentd/Go configuration, но не дает отдельной deploy command sequence для них.

## docker logs / kubectl logs

Source text names:

~~~text
docker logs
kubectl logs
~~~

Purpose:
- access logs exposed through container stdout.

No flags or resource identifiers are supplied in chapter range.

## Redis → Prometheus Adapter

Source Pod concept:

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapter-example
  namespace: default
spec:
  containers:
  - image: redis
    name: redis
  - image: oliver006/redis_exporter
    name: adapter
~~~

This is source-derived structure from PDF text extraction.

Classification:
- state-changing if deployed;
- exact deployment command is `[Needs confirmation]`.

Verification:
- Prometheus-facing metrics interface is the intended result;
- exact scrape/query command is `[Needs confirmation]`.

Rollback:
- `[Needs confirmation]`.

## fluentd Redis SLOWLOG Adapter

Source configuration:

~~~text
<source>
  type redis_slowlog
  host localhost
  port 6379
  tag redis.slowlog
</source>
~~~

Purpose:
- collect Redis slow-query information via a fluentd Adapter.

The chapter relies on the shared network namespace, so source points the Adapter at `localhost:6379`.

Exact fluentd startup/deployment command:
- `[Needs confirmation]`.

## fluentd Storm Adapter

Source configuration:

~~~text
<source>
  type storm
  tag storm
  url http://localhost:8080
  window 600
  sys 0
</source>
~~~

Purpose:
- convert Storm REST API information into queryable time-ordered logging output.

Exact deployment command:
- `[Needs confirmation]`.

## MySQL health Adapter

Source includes a Go program and an example invocation.

The source example contains a concrete username/password-like value. Per repository safety policy, the artifact substitutes placeholders:

~~~text
db-check --query="SELECT * from my-cool-table" \
         --user=<db-user> \
         --passwd=<db-password>
~~~

Classification:
- workload-generating;
- starts/uses an Adapter whose HTTP handler executes the configured query against the database.

Effect:
- health request triggers the configured SQL query;
- success returns HTTP 200 with `OK`;
- error returns HTTP 500.

Risk:
- diagnostic query creates DB workload;
- behavior depends on supplied query;
- credentials must not be embedded as real secrets.

Verification:
- HTTP status behavior from source.

Rollback:
- exact stop/remove process or container command is `[Needs confirmation]`.

## Source code boundary

The Go example includes parameters for:
- user;
- password;
- database;
- query;
- address, default shown as `localhost:8080`.

RAG text wrapping breaks at least one string literal visually. Therefore the extracted Go block is not reproduced here as a verified compile-ready program. See `source-findings.md`.

## Safety boundary

Do not add from model memory:
- `kubectl apply/create/delete` commands;
- Prometheus scrape queries;
- fluentd startup commands;
- MySQL CLI commands;
- health probe YAML;
- corrected/modernized source code.

Unsupported operational details remain `[Needs confirmation]`.
