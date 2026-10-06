# Diagram — глава 9

Provenance: `p0253:c01–p0270:c01`.

```mermaid
flowchart TD
    A[Stable RAG data] --> B{Fine-tuning threshold reached?}
    B -->|No| C[Keep as RAG data]
    B -->|Yes| D[Prepare SciQ dataset]

    D --> E[Filter Q/A/support]
    E --> F[Build chat-format examples]
    F --> G[Write JSONL-style file]
    G --> H[Upload OpenAI training file]
    H --> I[Create GPT-4o-mini fine-tuning job]

    I --> J[Monitor status / errors]
    J -->|succeeded| K[Fine-tuned model ID]
    J -->|failed| L[Inspect data/schema/errors]

    K --> M[Test science prompt]
    M --> N[Fine-tuned response]
    N --> O[Inspect quality]

    I --> P[Metrics UI]
    P --> Q[loss / tokens / epochs / batch / LR / seed / cost]
```

## Interpretation

- Fine-tuning is an alternative for stable data, not a replacement for dynamic RAG.
- Data preparation quality is a prerequisite for training success.
- Remote OpenAI training state and cost must be monitored.
- The chapter validates the tuned model with known science questions and then inspects training metrics.
