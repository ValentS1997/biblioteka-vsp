# Source/tooling limitations — book-level roll-up

Этот файл агрегирует material findings из chapter-level `source-findings.md`.

Он не заменяет chapter findings; детали/provenance остаются в соответствующих главах.

## 1. General extraction limitation

PDF text-layer extraction регулярно влияет на executable fragments:

- YAML indentation;
- shell line wrapping;
- punctuation;
- Python/Go line wrapping.

Следствие:

~~~text
architectural intent → usable
literal copy/paste command/config → often needs confirmation
~~~

Особенно заметно в главах 2–6, 8–11.

## 2. Historical platform/tooling boundary

Book-era practicals используют технологии/формы, которые не проверялись на current compatibility:

- older Kubernetes APIs/manifests;
- `helm init` / Tiller;
- historical etcd operator / etcdctl workflow;
- Kubeless + `python27`;
- Kafka `0.11` / ZooKeeper-oriented workflow;
- book-era Kubernetes Python client objects.

Policy for synthesis:

- pattern semantics are retained;
- practicals are treated as historical evidence;
- no silent modernization is performed;
- current syntax/API support remains `[Needs confirmation]`.

## 3. Material source contradictions / mismatches

### Chapter 3

- Redis manifest filename reused ambiguously;
- ConfigMap creation/reference naming mismatch.

### Chapter 6

- memcache/twemproxy port: `11211` vs prose `6379`;
- Service filename mismatch;
- modulo prose conflicts with displayed division formula.

### Chapter 7

- `0.99^5 ≈ 0.95` is shown while prose discusses ~5% straggler probability; 5% is the complement.

### Chapter 8

- messaging-library wording/module mismatch;
- user-registration code contains indentation/quoting/context-variable defects.

### Chapter 9

- `my-etcd-cluster` vs `example-etcd-cluster`;
- endpoint-export shell rendering is broken;
- availability arithmetic is illustrative/coarse.

### Chapter 10

- source API contract `/api/v1/items` differs from Python `:8000/items`;
- NodeJS example uses port `8080`;
- ffmpeg output literal and numbered-output prose do not align.

### Chapter 12

- histogram percentages sum to `105%`;
- Join is later described as if introduced in the previous chapter, despite chapter-local introduction.

## 4. Security-sensitive examples

Some source examples contain credential-like literals.

Repository artifacts deliberately avoid promoting them into reusable commands.

Production secret handling remains outside source-supported scope.

## 5. Modeling boundaries

Several quantitative sections are useful conceptual models but are not complete production models:

- availability examples;
- average-rate queue stability;
- tail-latency examples;
- shard remapping illustrations.

Not covered completely:

- burst distributions;
- retry storms;
- correlated failures;
- queueing percentiles;
- transactional guarantees;
- network-partition behavior.

## 6. Semantic boundaries that must not be blurred

### Merger vs Join

Merger combines streams.

Join is a completeness barrier.

### Health vs readiness

A process can be healthy/alive but not ready for traffic.

### Replica vs shard

Replica repeats the same responsibility.

Shard owns a partition.

### Local owner belief vs authoritative ownership

A resumed process may think it owns a resource after lease loss.

Authority must be verified against current coordination state/version.

## 7. Safe reuse policy for this book

### Safe to reuse conceptually

- pattern names and intents;
- architecture diagrams;
- failure reasoning;
- scale distinctions;
- queue/batch semantics;
- design-review questions.

### Requires current verification

- shell commands;
- Kubernetes YAML;
- Helm/Kafka/etcd/Kubeless procedures;
- runtime/image versions;
- API objects;
- concrete security configuration.

## Final source-quality assessment

The book remains strong as a **pattern and architecture source**.

Its practical snippets are not a reliable current operations runbook without independent verification.

That distinction should be preserved in all future biblioteka-vsp retrieval and reuse.
