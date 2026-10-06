# Ответы на контрольные вопросы — глава 8

These answers were derived from the chapter and cross-checked against the book's official appendix answer key. Official answer polarity follows the appendix; chapter-grounded rationale is retained, and appendix/chapter conflicts are marked explicitly.

Official appendix provenance: PDF `315–316`.

| № | Ответ | Основание |
|---:|:---:|---|
| 1 | Да | The source keeps the Hugging Face token outside the notebook code path, using Google Drive or manual/secret-based input and then an environment variable. |
| 2 | Нет | In this chapter accelerate is described primarily for PyTorch/GPU resource handling, mixed precision and processing acceleration, not as a cloud-deployment abstraction. |
| 3 | Нет | The shown Chroma client is local/temporary and no separate Chroma user authentication is configured. |
| 4 | Да | Temporary Chroma storage is the core dynamic-RAG design of the chapter. |
| 5 | Да | The environment uses `accelerate`, `float16` and `device_map="auto"`; GPU is strongly recommended when available. |
| 6 | Да | The chapter explicitly measures session preparation time so the team can tune preparation before a meeting. |
| 7 | Да | Chroma retrieval is combined with embedding models and Llama generation. |
| 8 | Да | Official appendix answer: performance/session metrics can be used to inform project-dependent adjustments. The chapter code itself does not implement automatic Chroma-parameter tuning from those metrics. `[Appendix/chapter interpretation tension]` |

## Provenance by answer

- 1: `p0231:c01–p0232:c01`
- 2: `p0232:c01–p0233:c01`
- 3: `p0237:c01–p0238:c01`
- 4: `p0227:c01–p0230:c01`, `p0237:c01–p0240:c01`
- 5: `p0232:c01–p0235:c01`
- 6: `p0234:c01–p0235:c01`, `p0250:c01`
- 7: `p0237:c01–p0249:c01`
- 8: `p0250:c01–p0252:c01`
