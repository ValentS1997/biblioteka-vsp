# Команды и инструменты главы 7

В RAG диапазоне `p0122:c01–p0133:c01` нет explicit shell, Docker или Kubernetes command sequence.

## Command inventory

| Command / action | Type | Source purpose |
|---|---|---|
| executable CLI | [Not applicable] | отсутствует в chapter range |
| topology changes | conceptual | изменить leaf count, shard layout или replica count |

## Source-supported tools / operations

Глава обсуждает архитектурные операции:
- scatter одного запроса на несколько leaf nodes;
- gather partial responses;
- set intersection;
- set union;
- replication каждого logical shard.

Они не представлены как CLI commands.

## Safety boundary

Не добавлять из model memory:
- Kubernetes manifests;
- timeout/retry commands;
- load-generator commands;
- tracing/metrics tooling;
- rollout/rollback commands.

Exact operational commands: `[Needs confirmation]`.
