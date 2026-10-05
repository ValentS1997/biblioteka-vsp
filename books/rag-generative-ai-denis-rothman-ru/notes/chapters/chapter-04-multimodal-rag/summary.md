# Резюме главы 4

Source section: explicit chapter-end «Резюме» in `p0134:c01`.

This file preserves source meaning with structural cleanup and concise paraphrase.

The chapter introduces multimodal RAG as a modular architecture where different modules handle different data types and tasks. The practical system combines text retrieval and image retrieval for a drone-related use case.

The implementation reuses:
- LlamaIndex;
- Deep Lake;
- OpenAI.

Two datasets are involved:
- a text dataset about drone technology;
- the VisDrone dataset containing images, labels and bounding boxes.

The text module:
- loads the text dataset;
- builds/uses a vector index;
- queries it with the user input;
- produces an LLM response.

The image module:
- loads VisDrone;
- inspects images, labels and bounding boxes;
- converts label data into LlamaIndex documents;
- builds an in-memory vector index;
- queries the index;
- uses source nodes to resolve a matching image;
- overlays bounding boxes for the selected object.

The final multimodal output combines:
- the user input;
- the textual LLM response;
- the retrieved annotated image.

For evaluation:
- text quality is measured using embedding-based cosine similarity;
- the image is sent to GPT-4o for visual analysis;
- the resulting textual image description is compared with the target label using the same similarity mechanism.

The source concludes that multimodal RAG introduces substantial complexity, but provenance and transparent access to source data make these systems easier to inspect and improve. This leads into the next chapter on human feedback.

## Provenance

- Summary source: `p0134:c01`
- Context cross-check: `p0110:c01–p0133:c01`
