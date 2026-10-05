# Cheatsheet — глава 4

Provenance: `rag-generative-ai-denis-rothman-ru:p0110:c01–p0135:c01`.

## Symptom / problem framing

Text-only RAG cannot directly answer tasks that require visual context. Chapter 4 extends the pipeline into a modular multimodal system that retrieves:
- textual context from one dataset;
- image-related context from another dataset.

## Baseline / context

The chapter uses two data sources:

| Module | Dataset | Role |
|---|---|---|
| Text | Deep Lake drone dataset from previous work | retrieve text and generate LLM response |
| Image | VisDrone | retrieve image-related labels/nodes and resolve back to source image |

One `user_input` drives both modules.

Example baseline:

`How do drones identify a truck?`

## Read-only checks

Before modifying runtime state:

1. Confirm text dataset loads.
2. Inspect text dataset tensors:
   - embedding;
   - id;
   - metadata;
   - text.
3. Confirm VisDrone loads read-only.
4. Inspect VisDrone summary:
   - images;
   - boxes;
   - labels.
5. Inspect class names.
6. Display a sample image.
7. Inspect labels and bounding boxes for the selected sample.
8. Verify source-node linkage after multimodal query.
9. Check that the selected keyword exists in image labels before drawing boxes.
10. Inspect the exact image passed to GPT-4o before evaluation.

## Interpretation

### Modular multimodal flow

Text module:

`user_input`
→ text VectorStoreIndex
→ query engine
→ `llm_response`

Image module:

`user_input`
→ label documents
→ in-memory vector index
→ query engine
→ `response.source_nodes`
→ keyword
→ source image
→ bounding boxes

Final output:
- user input;
- text response;
- selected image with boxes.

### VisDrone structure

Source summary:
- 6471 image rows;
- tensors:
  - `boxes`;
  - `images`;
  - `labels`.

Example label classes include:
- pedestrian;
- bicycle;
- car;
- van;
- truck;
- bus;
- others.

### Query strategy

The image dataset itself is not converted into an image embedding pipeline in this chapter. Instead:
1. image labels are converted to text documents;
2. LlamaIndex creates a vector index over those label documents;
3. a textual query retrieves a source node;
4. the node is mapped back to the source image row.

### Evaluation

Text response:
- SentenceTransformer embeddings;
- cosine similarity between `user_input` and `llm_response`.

Image response:
- encode selected image to base64;
- send to GPT-4o;
- obtain text description;
- compare target label text with generated image description.

Source example:
- text similarity: `0.691`;
- image-description similarity: `0.505`;
- combined score: `0.598`.

These are example outputs, not acceptance thresholds.

## Next action

Source-grounded sequence:

1. Load text dataset.
2. Build text VectorStoreIndex.
3. Define shared user input.
4. Query text module.
5. Load VisDrone read-only.
6. Inspect dataset structure.
7. Convert labels to DataFrame/documents.
8. Create in-memory vector index.
9. Query image-label module.
10. Inspect source nodes.
11. Extract target keyword.
12. Resolve node/document back to source image.
13. Draw matching bounding boxes.
14. Combine text + image output.
15. Evaluate text response.
16. Send image to GPT-4o for visual description.
17. Compare label vs image description.
18. Interpret metrics with human review.

## Modifying action

Source-confirmed state-changing actions:
- adding `doc_id` column to runtime DataFrame;
- building runtime/in-memory index structures;
- saving `boxed_image.jpg`;
- deleting `boxed_image.jpg`;
- calling external GPT-4o image analysis;
- any required environment setup inherited from previous chapter instructions.

Details: [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported checks:

- text dataset loads;
- VisDrone opens read-only;
- tensors and labels are visible;
- query engines return answers;
- source nodes are present;
- resolved image corresponds to retrieved label/keyword;
- bounding box image is successfully saved/displayed;
- text similarity is computed;
- image description is returned by GPT-4o;
- multimodal similarity is computed;
- final score is interpreted as an experiment indicator, not an absolute truth.

## Rollback

The chapter does not provide formal rollback for:
- runtime DataFrame/index changes;
- local image file creation/deletion;
- external API calls.

For local image output, source explicitly removes the previous file before regenerating it:

`!rm /content/boxed_image.jpg`

No restore procedure for the deleted prior file is provided.
