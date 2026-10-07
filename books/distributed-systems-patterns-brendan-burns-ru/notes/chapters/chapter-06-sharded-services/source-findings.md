# Source findings — глава 6

Этот файл фиксирует source/RAG contradictions, code mismatches и extraction defects без silent correction.

## Finding 1 — memcache port contradiction

Classification: `[Source contradiction]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0110:c01`

twemproxy configuration states:

~~~text
listen: 127.0.0.1:11211
~~~

The prose immediately below says requests to memcache are served at `localhost:6379`.

Finding:
- `11211` and `6379` conflict within the same source chunk;
- the chapter elsewhere defines memcache port `11211`, but this artifact does not silently rewrite the conflicting sentence.

Action:
- preserve both source facts;
- intended prose port: `[Needs confirmation]`;
- do not use the `6379` sentence as executable configuration guidance.

## Finding 2 — memcached Service filename mismatch

Classification: `[Source code mismatch]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0109:c01–p0110:c01`

Source says:
1. save StatefulSet as `memcached-shards.yaml`;
2. create it from that file;
3. save the headless Service as `memcached-service.yaml`;
4. then deploy the Service using `memcached-shards.yaml` again.

Finding:
- Service filename in prose and deployment filename conflict.

Action:
- do not silently substitute one filename for the other;
- exact intended Service creation command: `[Needs confirmation]`.

## Finding 3 — sharding formula conflicts with modulo prose

Classification: `[Source contradiction]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0114:c01–p0115:c01`

Source prose explicitly says the sharding function commonly uses a hash function and remainder/modulo operator `%`.

The extracted displayed formula is:

~~~text
Shard = hash(Req) / 10
~~~

The following sentence again says the remainder operator preserves determinism and uniformity.

Finding:
- displayed division operator conflicts with surrounding modulo prose.

Action:
- artifact describes the conceptual operation as modulo only when referring to the prose;
- displayed formula is not silently corrected;
- exact intended typeset formula: `[Needs confirmation]`.

## Finding 4 — twemproxy ConfigMap command syntax/order

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0110:c01`
- `distributed-systems-patterns-brendan-burns-ru:p0112:c01`

RAG renders ConfigMap instructions with the object name after `--from-file`, and one example is line-wrapped.

Finding:
- exact shell token order/line formatting is not independently verified under rag_only policy.

Action:
- preserve source rendering in `commands.md`;
- do not reorder tokens from model knowledge;
- exact executable syntax: `[Needs confirmation]`.

## Finding 5 — nginx hash directive punctuation

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0118:c01`

RAG renders:

~~~text
hash $request_uri consistent
~~~

without a visible trailing semicolon before the server entries.

Finding:
- PDF text extraction may have lost punctuation;
- exact production-safe nginx syntax is not established from RAG alone.

Action:
- preserve source fragment;
- exact executable config: `[Needs confirmation]`.

## Finding 6 — Kubernetes YAML indentation/current API

Classification: `[Source extraction issue]`

Provenance:
- StatefulSet/Pod/Deployment fragments: `p0108:c01–p0113:c01`.

Observation:
- YAML indentation is semantically significant and PDF text extraction can alter it;
- source uses API identifiers printed in the book.

Action:
- manifests are treated as architectural/configuration evidence;
- production-copy-safe indentation and current platform compatibility: `[Needs confirmation]`;
- no silent modernization is performed.
