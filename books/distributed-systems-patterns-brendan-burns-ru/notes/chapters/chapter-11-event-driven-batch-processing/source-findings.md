# Source findings — глава 11

## Finding 1 — Kafka topic-creation loop extraction

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0203:c01`

RAG breaks the shell loop across lines and renders its termination adjacent to the topic argument.

Finding:
- exact shell structure, continuations and placement of `done` are not reliable enough for copy/paste execution.

Action:
- preserve intent and parameters;
- exact executable loop: `[Needs confirmation]`;
- do not silently repair from model knowledge.

## Finding 2 — historical Helm/Tiller workflow

Classification: `[Needs confirmation]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0202:c01`

Source uses:
- `helm init`;
- Tiller;
- incubator chart repository;
- `helm install --name ...`.

No current platform verification is performed under `rag_only`.

## Finding 3 — historical Kafka image/tooling

Classification: `[Needs confirmation]`

Provenance:
- `p0203:c01–p0204:c01`

Source uses image `solsson/kafka:0.11.0.0` and ZooKeeper-oriented topic creation.

Action:
- preserve as chapter-era practical evidence;
- current image availability, broker mode and CLI compatibility are not asserted.

## Finding 4 — Merger completeness boundary

Classification: `[Source semantic boundary]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0197:c01`

Merger combines several input task streams into one source stream.

Important:
- chapter does not claim Merger waits for all parallel inputs or provides barrier synchronization;
- coordinated completeness belongs to later chapter patterns.

Action:
- do not interpret Merger as Join/barrier.
