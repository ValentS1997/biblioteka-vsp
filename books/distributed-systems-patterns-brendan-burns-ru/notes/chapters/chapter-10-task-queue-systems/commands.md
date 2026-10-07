# Команды и инструменты главы 10

Only commands/interfaces/API calls explicitly supported by RAG `p0173:c01–p0188:c01`.

## Command inventory

| Command / action | Type | Source purpose | Verification | Rollback |
|---|---|---|---|---|
| `GET /api/v1/items` | read-only | получить список work items | ItemList returned | Not applicable |
| `GET /api/v1/items/<item-name>` | read-only | получить details одного item | Item object returned | Not applicable |
| `batch.list_namespaced_job(...)` | read-only API call | получить existing Jobs | list returned | Not applicable |
| `batch.create_namespaced_job(...)` | state-changing API call | создать worker Job | Job appears/runs | `[Needs confirmation]` |
| `ffmpeg -i ${INPUT_FILE} -frames:v 100 thumb.png` | state-changing local processing | создать thumbnail output | output file(s) expected by source prose | application-specific |

## Source API

Documented source-container interface:

~~~text
GET http://localhost/api/v1/items
GET http://localhost/api/v1/items/<item-name>
~~~

Purpose:
- list all work items;
- retrieve per-item details/data.

The later Python and NodeJS examples do not use exactly the same path/port representation. See `source-findings.md`.

## Kubernetes Python API

Source manager uses:

~~~python
ret = batch.list_namespaced_job(namespace, watch=False)
~~~

Classification:
- read-only.

Purpose:
- inspect Jobs already associated with queue processing.

For missing items:

~~~python
batch.create_namespaced_job(namespace, job)
~~~

Classification:
- state-changing.

Effect:
- creates Kubernetes Job for an unprocessed item.

Risk:
- unbounded creation can create bursty resource consumption, which chapter later addresses through concurrency limits.

Rollback:
- no source-supported delete command is provided.

## Queue polling

Source loop:

~~~text
update_queue(batch)
sleep 10 seconds
repeat
~~~

Purpose:
- periodically reconcile source items against Jobs.

Exact production polling/backoff policy:
- `[Needs confirmation]`.

## Video thumbnail command

Source:

~~~bash
ffmpeg -i ${INPUT_FILE} -frames:v 100 thumb.png
~~~

Classification:
- state-changing local processing;
- reads input media and writes output artifact(s).

Source description associates it with periodic frame extraction and PNG thumbnails.

The literal output name and prose examples are not fully aligned; see `source-findings.md`.

Rollback:
- output cleanup procedure is application-specific and not supplied.

## Tools named by source

- Kubernetes `Job`;
- Kubernetes `ConfigMap`;
- Kubernetes Python client;
- NFS/shared network storage;
- NodeJS source container;
- `ffmpeg`;
- Docker image `jrottenberg/ffmpeg`.

No standalone source-supported `kubectl create/delete` sequence appears in chapter 10.

## Safety boundary

Do not add from model memory:
- Job cleanup/delete commands;
- current Kubernetes Python client object names;
- retry/idempotency implementation;
- autoscaler manifests;
- NFS mount commands;
- corrected HTTP paths/ports;
- modified ffmpeg syntax.

Unsupported operational details remain `[Needs confirmation]`.
