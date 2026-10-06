# Cheatsheet — глава 6

Provenance: `rag-generative-ai-denis-rothman-ru:p0161:c01–p0198:c01`.

## Symptom / problem framing

Scaling RAG changes cost, latency, request limits, storage, batch processing and observability. A workflow that works on a small dataset can become expensive or operationally unsafe at larger vector counts.

## Baseline / context

| Component | Purpose |
|---|---|
| 1. Data preparation | Kaggle → cleaned DataFrame → EDA → k-means |
| 2. Vector scale | chunks → OpenAI embeddings → Pinecone index → upsert/query |
| 3. RAG generation | target vector → top-k customer profiles → GPT-4o recommendation |

## Read-only checks

Before remote writes:
1. Confirm row count = 10,000.
2. Confirm removed columns match the intended scenario.
3. Inspect DataFrame schema.
4. Inspect EDA results.
5. Compare silhouette / Davies–Bouldin metrics.
6. Confirm `len(chunks) == len(embeddings)`.
7. Confirm embedding model and vector dimension are compatible.
8. Confirm target Pinecone index name/cloud/region.
9. Check if index already exists.
10. Inspect Pinecone pricing/limits before scaling.
11. Inspect expected batch size.
12. Inspect current index stats before upsert.
13. Confirm query uses the same embedding model as ingestion.

## Interpretation

### EDA before RAG

The source deliberately performs ordinary analysis first. It reports:
- strong association in the example between complaints and churn;
- weaker usefulness for the tested salary threshold;
- two clusters as the best among the tested 2–4 cluster configurations.

Example clustering metrics:
- k=2: silhouette `0.6129`, Davies–Bouldin `0.6144`;
- k=3/4: worse in the source run.

These numbers are dataset/example-specific.

### Embeddings

Each customer row is converted to a text record and then a chunk. The source uses:
- `text-embedding-3-small`;
- one embedding per chunk;
- batching in groups of 1000;
- pause between groups in the example.

### Scaling simulation

The chapter duplicates chunks + embeddings to simulate higher vector counts without paying to regenerate every embedding.

Important:
- duplication tests infrastructure/load behavior;
- it does not create new independent customer evidence.

### Pinecone

Source index configuration:
- serverless;
- example cloud: AWS;
- example region: `us-east-1`;
- dimension: `1536`;
- metric: `cosine`.

Upsert records contain:
- `id`;
- `values`;
- metadata `{"text": chunk}`.

### Query / generation

A target customer profile is embedded and queried against Pinecone. Top-k similar records are combined into context and sent to GPT-4o to generate a personalized retention email.

## Next action

Source-grounded sequence:

1. authenticate to Kaggle;
2. download/unpack dataset;
3. remove unneeded/sensitive columns for the scenario;
4. save cleaned CSV;
5. perform EDA;
6. run clustering evaluation;
7. convert each row to text;
8. create chunks;
9. generate embeddings;
10. verify chunk/embedding counts;
11. decide scale/cost target;
12. create/connect Pinecone index;
13. batch upsert;
14. verify index stats;
15. run a vector query;
16. measure query time;
17. define target vector;
18. retrieve top-k profiles;
19. create augmented prompt;
20. call GPT-4o;
21. measure/inspect result.

## Modifying action

State-changing/external actions:
- mount Google Drive;
- install Kaggle/OpenAI/Pinecone packages;
- set credentials in environment/process;
- download and unzip Kaggle dataset;
- write/copy CSV files;
- create Pinecone index;
- upsert vectors/metadata;
- OpenAI embedding and generation API calls.

See [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported:
- expected CSV row count;
- chunk count;
- embedding count;
- Pinecone index dimension;
- vector count after upsert;
- metadata returned by query;
- query latency;
- top-k similarity results;
- generated recommendation content.

No universal latency/SLO threshold is defined by the chapter. The “under 1 second at 1M vectors” statement is source expectation/example framing, not a repository acceptance criterion.

## Rollback

Formal rollback is not defined for:
- Kaggle/package environment changes;
- Pinecone index creation;
- Pinecone upsert;
- external API calls.

Rollback: `[Needs confirmation]`.

For remote vector-store changes, the chapter does not provide a snapshot/restore or delete-and-recreate procedure.
