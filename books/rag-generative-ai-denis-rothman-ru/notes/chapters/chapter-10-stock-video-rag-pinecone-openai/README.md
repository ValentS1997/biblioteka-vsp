# Глава 10. RAG для создания стоковых видео с помощью Pinecone и OpenAI

Status: `RAG_GROUNDED`

## Scope

- Book ID: `rag-generative-ai-denis-rothman-ru`
- RAG chunk range: `p0271:c01–p0306:c01`
- PDF pages: `271–306`
- Printed page range: `[Needs confirmation]`
- Chapter boundary: verified
- Appendix starts at PDF page `307`
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

Source policy: strict `rag_only`. No external web/model-memory fallback used.

## Chapter map

1. Three-agent video RAG architecture:
   - Generator;
   - Commentator;
   - Vector Store Administrator;
   - Video Expert.
2. Shared environment:
   - video/image libraries;
   - GitHub downloads;
   - OpenAI credentials;
   - Pinecone credentials.
3. Generator:
   - source describes Sora/inVideo-generated videos;
   - download/display videos;
   - split video into JPG frames.
4. Commentator:
   - sample frames;
   - send frames to an OpenAI vision model;
   - generate natural-language comments;
   - persist comment metadata to CSV.
5. Local lifecycle:
   - save/copy CSV and frames;
   - optional deletion of session MP4/JPG/CSV files.
6. Vector Store Administrator:
   - reuse chapter-6 chunking/embedding/Pinecone logic;
   - upload comment-derived vectors;
   - query Pinecone;
   - trace result metadata back to video + frame.
7. Hybrid retrieval:
   - vector metadata in Pinecone;
   - media files stored separately;
   - retrieve matching media by `file_name` / `frame_number`.
8. Video Expert:
   - GPT-4o analyzes retrieved technical comment;
   - identify logical/cognitive inconsistencies;
   - rewrite comment;
   - assign a label.
9. Evaluation:
   - ten examples;
   - human rewritten target comment;
   - SentenceTransformer cosine similarity;
   - original retrieval score;
   - aggregate metrics reused from chapter 7.
10. Explicit summary and 10 review questions.

## Main principle

The chapter assembles a full multimodal RAG production pipeline around video. Media files and vector metadata are deliberately separated: Pinecone stores/searches vectorized comments and metadata, while actual video/frame files can live in another storage system. Query results are traced back to exact media assets, then GPT-4o performs a second-stage expert rewrite and labeling step.

## Operational boundaries

- OpenAI/Pinecone keys are secret-bearing runtime inputs.
- GitHub/video downloads and frame extraction create local files.
- Frame commenting invokes external/billable model workloads.
- CSV writes and Drive copies modify local/external storage state.
- `rm -f *.mp4`, `*.jpg`, `*.csv` are destructive local cleanup actions when enabled.
- Pinecone index creation/upsert are remote state-changing; chapter 10 refers back to chapter 6 for their implementation rather than reprinting all code.
- Pinecone queries are read/workload operations.
- The source states CPU + modest memory is sufficient for its per-video processing strategy; this is chapter framing, not a production SLO.
- Source explicitly warns that real production deployment requires substantial engineering effort and continued human involvement.
- Video-generation provenance/ethics matter: the chapter mentions deepfake/misinformation risk and the need for ethical, realistic content.

## Source issues

### OpenAI key extraction is damaged

`p0277:c01` extracts:

`API_KEY=f.readline()o`

and:

`Nf.close()`

Status: `[Source extraction issue]`.

### download_video argument/global mismatch

`p0282:c01` defines:

`def download_video(filename):`

but then assigns:

`filename = file_name`

using a global variable instead of the function argument.

Status: `[Source code mismatch]`.

### save_comment indentation/logic issue

`p0290:c01` shows the data-row write inside:

`if write_header:`

so the displayed structure writes the comment row only when the CSV is first created.

Status: `[Source code issue]`.

### Frame-directory naming mismatch

`p0294:c01` describes removing the extension, but then constructs:

`root_name = root_name + extension.strip('.')`

which joins the basename with the extension text minus the dot.

Status: `[Source wording/code mismatch]`.

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [summary.md](./summary.md)
- [review-questions.md](./review-questions.md)
- [review-answers.md](./review-answers.md)

## Provenance

- Architecture / environment: `p0271:c01–p0278:c01`
- Generator / video processing: `p0279:c01–p0289:c01`
- Commentator / controller / local lifecycle: `p0289:c01–p0294:c01`
- Vector Store Administrator / hybrid retrieval: `p0295:c01–p0299:c01`
- Video Expert / evaluation: `p0300:c01–p0304:c01`
- Summary/questions: `p0305:c01–p0306:c01`
