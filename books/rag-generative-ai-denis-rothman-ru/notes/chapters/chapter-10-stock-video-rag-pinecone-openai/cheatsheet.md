# Cheatsheet — глава 10

Provenance: `p0271:c01–p0306:c01`.

## Symptom / problem framing

A useful video-RAG system must do more than retrieve text. It needs to:
- produce or collect video;
- break it into searchable units;
- attach machine-generated semantics;
- store vector-searchable metadata;
- trace search results back to concrete frames/video files;
- improve and label results with a second-stage model.

## Baseline / context

| Agent / component | Role |
|---|---|
| Generator | obtain/generate video and split it into frames |
| Commentator | describe sampled frames and save comments/metadata |
| Vector Store Administrator | vectorize comments, populate/query Pinecone, expose source metadata |
| Video Expert | analyze/rewrite retrieved comments and assign labels |

## Read-only checks

Before modifying state:
1. Confirm input video exists.
2. Inspect frame count, FPS and duration.
3. Check requested frame number is valid.
4. Inspect generated JPG frame count.
5. Inspect comment CSV before upload.
6. Confirm CSV columns:
   - ID;
   - FrameNumber;
   - Comment;
   - FileName.
7. Confirm Pinecone query returns metadata.
8. Inspect retrieval score.
9. Verify returned `file_name` and `frame_number`.
10. Check media file existence and size before display.
11. Inspect Video Expert rewritten comment and label.
12. Compare automated similarity with human feedback.

## Interpretation

### Generator

Source workflow:
- video generated/obtained externally;
- downloaded locally;
- split with OpenCV;
- each frame written as JPG.

The chapter scales by processing one video at a time rather than loading a huge media corpus into memory.

### Commentator

A sampled subset of frames is sent to a vision model with the short instruction:

`What is happening in this image?`

The response becomes a comment associated with:
- UUID;
- frame number;
- file name.

### Vector Store Administrator

The chapter reuses chapter-6 mechanics for:
- chunking;
- embeddings;
- Pinecone index;
- upload/upsert.

Chapter 10 does not repeat all implementation code, so this collection does not reconstruct it from model memory.

### Hybrid retrieval

The vector database stores/searches semantic comments and metadata, while the actual MP4/JPG assets may remain in GitHub or another file/object store.

Example query:
`Find a basketball player that is scoring with a dunk.`

Source example returns:
- similarity score around `0.866`;
- frame `191`;
- file `basketball3.mp4`.

### Video Expert

GPT-4o receives the retrieved comment and is instructed to:
1. identify cognitive/logical dissonances;
2. rewrite the comment coherently;
3. assign a label.

### Evaluation

For ten examples:
- a human feedback comment acts as expected output;
- the rewritten GPT-4o comment is extracted;
- SentenceTransformer cosine similarity is computed;
- retrieval score is kept separately;
- aggregate metrics are computed.

Source example aggregate:
- mean around `0.65`.

This is an experiment result, not a production threshold.

## Next action

1. Verify environment and secrets.
2. Select one video.
3. Download/display it.
4. Split into frames.
5. Sample frames.
6. Generate frame comments.
7. Inspect/save comment CSV.
8. Save/copy frames if required.
9. Clean session files only after verifying persistence.
10. Prepare comments for embeddings.
11. Populate/connect Pinecone.
12. Query with user input.
13. Inspect metadata and score.
14. Resolve video/frame from metadata.
15. Verify the file exists and is non-trivial in size.
16. Display media.
17. Send retrieved comment to Video Expert.
18. Inspect rewritten comment + label.
19. Run evaluation corpus.
20. Compare human feedback, similarity and retrieval metrics.

## Modifying action

State-changing/external operations:
- Drive mount;
- file downloads;
- MP4/JPG/CSV creation;
- copying artifacts to Drive;
- optional session file deletion;
- OpenAI vision/GPT-4o workloads;
- Pinecone index population/upsert.

Details: [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported:
- video can be displayed;
- frames are extracted;
- comments are generated;
- CSV is readable;
- query returns score + metadata;
- exact video/frame can be resolved;
- media file existence/size can be checked;
- Video Expert returns rewrite + label;
- evaluation produces per-example similarities and aggregate metrics.

No universal production accuracy/latency threshold is defined.

## Rollback

Formal rollback is not provided for:
- deleted local media/comment files;
- remote Pinecone writes;
- external API calls.

The source does include boolean guards (`save`, `save_frames`, `delf`) intended to require explicit operator choice before persistence/deletion.
