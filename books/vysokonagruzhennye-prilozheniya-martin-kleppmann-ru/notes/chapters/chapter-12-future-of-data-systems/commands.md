# Source-confirmed commands, mechanisms and conceptual operations — глава 12

Глава в основном концептуальная и прогнозная. Ниже включены только явно поддержанные source examples и mechanisms.

## CREATE INDEX

Источник: `p0576:c01`, PDF 576.

~~~sql
CREATE INDEX
~~~

Тип: state-changing database operation.

Source point: создание secondary index можно понимать как:

1. read consistent snapshot;
2. derive index entries;
3. catch up changes made after snapshot;
4. continuously maintain index on future writes.

Это используется как аналогия для batch + stream maintenance of derived state.

Effect: creates a derived representation of base table data.

Risk: concrete lock/online-build behavior depends on DB implementation and is not specified by chapter.

Verification: derived index reflects source table after catch-up.

Rollback: concrete `DROP INDEX` syntax/product behavior не приводятся в chapter RAG — `[Needs confirmation]`.

## Conceptual dataflow shell

Источник: `p0580:c01`, PDF 580.

Author's illustrative idea:

~~~text
mysql | elasticsearch
~~~

Тип: conceptual/non-executing example.

Это не documented production command. Example expresses desired high-level semantics:

- read source data from MySQL;
- build/search-index representation in Elasticsearch;
- continuously capture future changes;
- keep derived index updated without bespoke glue code.

Verification: `[Not applicable]` as executable command; this is an architectural illustration.

Rollback: `[Not applicable]`.

## Replay historical data through current transformation

Источник: `p0571:c01`–`p0574:c01`, PDF 571–574.

Conceptual operation:

~~~text
historical immutable events
  -> current batch/stream transformation
  -> new derived projection
~~~

Тип: workload-generating / state-changing at derived output.

Source uses this model for:

- schema evolution;
- index/cache rebuilding;
- old/new projections in parallel;
- migration with reversible cutover.

Verification:

- new projection matches expected transformation of source history;
- old projection remains available until cutover acceptance.

Rollback: switch consumers back to old projection while source/history remains unchanged; concrete routing command `[Needs confirmation]`.

## End-to-end request/operation identifier

Источник: `p0596:c01`–`p0600:c01`, PDF 596–600.

Conceptual pattern:

~~~text
client request
  -> assign stable operation ID
  -> propagate same ID through services/messages
  -> persist effect together with ID
  -> duplicate request with same ID is not applied twice
~~~

Тип: state-changing deduplication mechanism.

Source point: lower-level duplicate suppression in TCP or stream processor is insufficient if the user/client retries a whole request. The identifier must survive end-to-end to the point where the logical effect is recorded.

Verification:

- repeated request with same operation ID produces one logical effect;
- ID is visible/traceable across the entire processing path.

Rollback: application-specific `[Needs confirmation]`.

## Partitioned uniqueness decision

Источник: `p0601:c01`–`p0602:c01`, PDF 601–602.

Conceptual algorithm:

~~~text
request(unique_value)
  -> partition by hash(unique_value)
  -> append to partition log
  -> single sequential processor checks local state
  -> emit ACCEPTED or REJECTED event
  -> client waits for matching result if synchronous feedback is needed
~~~

Тип: state-changing coordination mechanism.

Effect: all potentially conflicting requests for one unique value are serialized in the same partition.

Verification:

- two conflicting requests cannot both be accepted for the same constrained value;
- partition processor recovery preserves decision order.

Rollback: accepted external/business effect may require compensation; concrete procedure `[Needs confirmation]`.

## Cross-partition operation without global atomic commit

Источник: `p0603:c01`–`p0604:c01`, PDF 603–604.

Source conceptual sequence for a transfer:

~~~text
1. client assigns unique request ID
2. append one durable transfer-request event, partitioned by request ID
3. deterministic processor emits:
   - debit instruction partitioned by payer account
   - credit instruction partitioned by recipient account
4. downstream processors deduplicate by original request ID
5. apply balance changes
~~~

Тип: state-changing distributed workflow.

Source rationale: make the initial request a single atomic durable write, then derive deterministic downstream instructions. Retries may duplicate messages, but end-to-end request ID allows deduplication.

Verification:

- debit and credit processors each apply the logical request once;
- replay does not duplicate the logical transfer;
- original durable request remains traceable.

Rollback: financial/business compensation semantics are domain-specific — `[Needs confirmation]`.

## Asynchronous constraint checking / compensation

Источник: `p0607:c01`–`p0609:c01`, PDF 607–609.

Conceptual model:

~~~text
accept/process request
  -> asynchronously verify business constraint
  -> if violated:
       execute compensating business process
       notify/apologize/repair
~~~

Тип: state-changing business-process mechanism.

Source examples include overbooking, inventory shortage and overdraft-like cases.

Boundary: source does not claim every invariant may be relaxed. Some irreversible operations still require synchronous checking/coordination.

Verification:

- temporary violation is detected;
- compensation path is executable and restores an acceptable business state;
- integrity is preserved even if timeliness/constraint strictness is relaxed.

Rollback: compensation itself is the recovery path; exact implementation `[Needs confirmation]`.

## Audit / integrity verification

Источник: `p0609:c01`–`p0614:c01`, PDF 609–614.

Source-confirmed mechanisms/concepts:

- independent reconciliation;
- end-to-end checksums;
- replay deterministic derivations;
- event/provenance logs;
- cryptographic integrity checking;
- Merkle trees as an audit/inclusion-proof technique.

Тип: read-only verification and/or state-audit mechanism depending implementation.

Verification: independently derived/checksummed state agrees with the state under test.

Rollback: `[Not applicable]` for read-only verification.

## Named systems/ideas explicitly present

- PostgreSQL full-text search;
- Elasticsearch;
- Hadoop MapReduce;
- Storm;
- Spark;
- Flink;
- Apache Beam;
- Google Cloud Dataflow;
- Differential Dataflow;
- Naiad;
- Jepsen;
- Bitcoin / Ethereum / Ripple / Stellar;
- Merkle trees;
- certificate transparency.

These are historical/source examples only; current product behavior is not inferred.

## Что не добавлено

- executable MySQL→Elasticsearch pipeline command;
- Elasticsearch indexing API;
- Kafka commands;
- Jepsen invocation syntax;
- blockchain CLI;
- Merkle-tree implementation code;
- privacy/compliance commands.

Concrete operational syntax is absent from chapter RAG.
