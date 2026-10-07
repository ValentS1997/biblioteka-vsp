# Глава 11 — data-model constructs и operational boundary

**Provenance:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 43–44; RAG `e0043:c01–c02`, `e0044:c01–c06`.

## Executable commands

**[Not applicable].** Глава упоминает SQL, API, ETL, Apache Drill, relational/NoSQL stores, Excel, R и Python, но не предоставляет готовых SQL statements, DDL, ETL jobs или production commands.

Не создавать `CREATE TABLE`, `SELECT`, pipelines или schemas из общих знаний как якобы source code главы.

## Source-confirmed logical structures

### Core cube / dimensions

Глава описывает standard security mart вокруг трёх высокоуровневых измерений:

```text
time × value(asset) × risk
```

Это conceptual model, не SQL schema.

### Example security fact table fields for ПУКД

В `e0044:c04–c05` перечислены:

```text
mit_id
mal_id
http_id
date_http_start_id
date_https_end_id
asset_id
vuln_id
```

Semantics:
- `mit_id` — mitigation/security control identifier;
- `mal_id` — malware-protection identifier;
- `http_id` — HTTP endpoint reference;
- `date_http_start_id` — first observed date;
- `date_https_end_id` — source spelling for prevention/end date field;
- `asset_id` — affected asset;
- `vuln_id` — correlated known vulnerability if present.

Не нормализовать field names без schema source: source explicitly writes `date_https_end_id`, while neighboring start field is `date_http_start_id`.

### Factless fact

Security fact may encode presence/absence of an event rather than a numeric amount. Aggregation may effectively count rows / events (`e0044:c02–c03`).

### Accumulating snapshot

For multi-stage remediation process:
- one process instance;
- multiple milestone date keys;
- derived duration fields such as `Days_Existing` and `Analysis_Days_Reviewing`;
- duration accumulates until stage end date is populated (`e0044:c05–c06`).

## Analytics methods mentioned

| Метод | Класс | Назначение |
|---|---|---|
| Dimensional modeling | read-only design; physical implementation `state-changing` | Organize facts/dimensions |
| Cross-drill via conformed dimensions | read-only analysis | Compare security domains/controls |
| Survival analysis | analytical/workload-generating | Model time-to-detection / threat survival |
| Accumulating snapshot | data-model/process measurement | Measure multi-stage workflow durations |
| BI aggregation/drill-down | read-only analysis | Move between summary and atomic events |

## Production safety boundary

Physical data mart implementation may affect database/storage capacity, ETL/API load, sensitive log/asset data, retention/compliance, RBAC and query performance.

None of these are specified by the chapter. Approval, architecture, schema, query plans, indexes, retention and rollback: **[Needs confirmation]**.
