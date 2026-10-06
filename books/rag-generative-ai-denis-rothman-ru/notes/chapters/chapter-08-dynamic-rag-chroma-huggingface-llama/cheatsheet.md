# Cheatsheet — глава 8

Provenance: `p0227:c01–p0252:c01`.

## Symptom / problem framing

Some RAG data is useful only for hours or a single meeting. Persisting it indefinitely adds storage/management overhead without adding value.

## Baseline / context

| Stage | Source implementation |
|---|---|
| Prepare fresh data | SciQ from Hugging Face |
| Temporary vector store | local Chroma collection |
| Embeddings | Chroma / all-MiniLM-L6-v2 path |
| Retrieval | Chroma semantic search |
| Generator | meta-llama/Llama-2-7b-chat-hf |
| Evaluation | spaCy similarity + timing |
| Lifecycle | discard collection after the session if no longer needed |

## Read-only checks

1. Confirm HF token exists without printing it.
2. Confirm dataset loads.
3. Confirm filtered row count.
4. Inspect DataFrame columns.
5. Check whether the Chroma collection already exists.
6. Inspect collection fields.
7. Verify first embedding exists and has expected source-observed length.
8. Measure bulk query time.
9. Compare retrieved document with original completion.
10. Verify a meeting-time prompt retrieves at least one document.
11. Inspect augmented input before generation.
12. Verify collection existence after optional deletion.

## Interpretation

### Temporary collection

The default `chromadb.Client()` in the source is described as temporary and non-persistent. That is central to the chapter’s “daily collection” architecture.

### SciQ shaping

The source keeps:
- question;
- correct_answer;
- support;
- generated completion.

Distractors are removed.

### Embeddings

The source reports:
- model path: `all-MiniLM-L6-v2`;
- first embedding length: `384`.

This is a source-observed implementation detail, not a general Chroma invariant.

### Retrieval validation

The chapter queries more than 10,000 questions and compares:
- original completion;
- retrieved document.

A spaCy vector-similarity score is computed. The example counts a result as acceptable when:

`similarity_score > 0.7`

That threshold is source-specific.

### Meeting-time augmentation

Flow:

`prompt`
→ Chroma query
→ retrieved document
→ `iprompt + retrieved document`
→ Llama 2
→ generated summary.

The source notes that prompt rewording can destabilize results, so human supervision remains important.

## Next action

1. Obtain token securely.
2. Prepare runtime packages/model.
3. Start session timer.
4. Load SciQ.
5. Filter/clean data.
6. Create/check Chroma collection.
7. Add completion documents.
8. Inspect embeddings.
9. Run bulk retrieval validation.
10. Review aggregate similarity.
11. Test realistic meeting prompts.
12. Retrieve one relevant document.
13. Build augmented Llama prompt.
14. Generate answer.
15. Measure response time.
16. Adjust parameters/model if output is poor.
17. Delete temporary collection after the session when appropriate.
18. Record total preparation time.

## Modifying action

State-changing/external operations:
- Drive mount;
- package installs;
- model/dataset downloads;
- environment variable assignment;
- Chroma create/add/delete;
- runtime cache writes;
- Llama generation workload.

Details: [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported:
- filtered SciQ rows = `10481`;
- DataFrame has four relevant columns after preparation;
- collection existence check works;
- collection contains IDs/documents/embeddings metadata structures;
- source-observed embedding length = `384`;
- retrieval returns documents;
- similarity can be computed;
- one meeting-time query can be answered quickly;
- Llama returns generated text;
- session duration is measurable.

No production SLO/SLA or universal quality threshold is defined.

## Rollback

- Temporary Chroma collection can be deleted, but the source line is displayed commented.
- Closing the session is also described as a way to lose the temporary collection.
- No restore procedure is provided for a deleted collection.
- Package/environment rollback: `[Needs confirmation]`.
