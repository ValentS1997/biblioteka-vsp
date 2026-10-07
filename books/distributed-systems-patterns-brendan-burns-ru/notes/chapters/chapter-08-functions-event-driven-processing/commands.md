# Команды и инструменты главы 8

Only commands explicitly supported by RAG `p0134:c01–p0150:c01`.

## Command inventory

| Command | Type | Source purpose | Verification | Rollback |
|---|---|---|---|---|
| `kubeless install` | state-changing | установить Kubeless в Kubernetes cluster | `kubectl get functions` | `[Needs confirmation]` |
| `kubectl get functions` | read-only | показать deployed functions | function list visible | Not applicable |
| `kubeless function deploy add-defaults ...` | state-changing | deploy Decorator function | invoke with `kubeless function call` | `[Needs confirmation]` |
| `kubeless function call add-defaults --data '{"name": "foo"}'` | workload-generating | invoke Decorator with test payload | returned/transformed result | Not applicable |
| `kubeless function deploy add-two-factor ...` | state-changing | deploy 2FA event handler | source describes async invocation from client | `[Needs confirmation]` |

## Kubeless installation

Source:

~~~bash
kubeless install
~~~

Effect:
- installs Kubeless as a Kubernetes API extension according to chapter framing.

Verification:

~~~bash
kubectl get functions
~~~

Source expectation:
- initially, no functions are deployed.

Risk:
- state-changing cluster installation;
- current compatibility is `[Needs confirmation]`.

Rollback:
- not supplied.

## Decorator deployment

Source:

~~~bash
kubeless function deploy add-defaults     --runtime python27     --handler defaults.handler     --from-file defaults.py     --trigger-http
~~~

Effect:
- deploys HTTP-triggered function `add-defaults`.

Source handler logic:
- add missing `name`;
- set missing `color` to `blue`;
- call underlying API.

Verification:

~~~bash
kubeless function call add-defaults --data '{"name": "foo"}'
~~~

Classification:
- workload-generating;
- invokes deployed function.

Exact expected response body depends on `call_my_api`, which is intentionally application-specific: `[Needs confirmation]`.

## Two-factor function deployment

Source:

~~~bash
kubeless function deploy add-two-factor     --runtime python27     --handler two_factor.two_factor     --from-file two_factor.py     --trigger-http
~~~

Effect:
- deploys HTTP-triggered 2FA handler.

Risk:
- function performs external side effects in source example: login-service registration and message sending;
- example credentials/contact values are not reusable operational values.

Verification:
- chapter describes asynchronous invocation after successful password entry;
- exact test command is not supplied.

Rollback:
- `[Needs confirmation]`.

## Code artifacts

Chapter code snippets include:
- `defaults.py`;
- `two_factor.py`;
- user-registration pipeline handlers.

Some snippets contain source/extraction defects and are not treated as copy/paste-safe. See `source-findings.md`.

## Safety boundary

Do not add from model memory:
- modern Kubeless replacement procedures;
- delete/uninstall commands;
- current Python runtime identifiers;
- Kubernetes manifests;
- real messaging-service credentials;
- production secret-management commands.

Unsupported operational details remain `[Needs confirmation]`.
