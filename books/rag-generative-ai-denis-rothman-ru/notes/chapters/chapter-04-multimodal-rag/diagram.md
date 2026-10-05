# Diagram — глава 4

Provenance: `p0110:c01–p0135:c01`.

```mermaid
flowchart TD
    U[Shared user_input] --> TQ[Text query engine]
    U --> IQ[Image-label query engine]

    subgraph TEXT["Text module"]
      TD[Deep Lake drone text dataset] --> TI[VectorStoreIndex]
      TI --> TQ
      TQ --> TR[LLM response]
    end

    subgraph IMAGE["Image module"]
      VD[VisDrone read-only dataset] --> DF[DataFrame: image / boxes / labels]
      DF --> DOC[Label text documents + doc_id]
      DOC --> VI[In-memory vector index]
      VI --> IQ
      IQ --> SN[Source nodes]
      SN --> KW[Unique keyword]
      KW --> SRC[Resolve source image row]
      SRC --> BB[Draw matching bounding boxes]
    end

    TR --> OUT[Combined multimodal output]
    BB --> OUT

    TR --> TE[Text similarity]
    BB --> ENC[Base64 image]
    ENC --> VISION[GPT-4o image analysis]
    VISION --> IE[Image-description similarity]

    TE --> SCORE[Combined score]
    IE --> SCORE

    SCORE --> H[Human interpretation remains necessary]
```

## Interpretation

- The text and image branches share one user input.
- VisDrone retrieval operates over text labels/documents, then maps source nodes back to an image.
- Bounding boxes are applied after source-image resolution.
- GPT-4o is used as a multimodal evaluator that converts the image into a text description.
- Final evaluation is still not purely objective; the source emphasizes the difficulty of judging complex images.
