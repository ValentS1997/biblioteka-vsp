# Глава 5. Повышение эффективности RAG за счет обратной связи от эксперта

Status: `RAG_GROUNDED`

## Scope

Канонический источник: addressable RAG книги `rag-generative-ai-denis-rothman-ru`.

- Source format: PDF
- RAG chunk range: `p0136:c01–p0160:c01`
- PDF page range: `136–160`
- Printed page range: `[Needs confirmation]`
- Chapter boundary: verified
- Next chapter starts at PDF page `161`: «Масштабирование банковских данных клиентов в системе RAG с помощью Pinecone»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

No external web or model-memory content is used.

## Chapter map

1. Adaptive RAG:
   - human feedback (HF) как часть evaluation;
   - корректировка retrieval behavior без изменения параметров модели.
2. Hybrid RAG:
   - automation + human/expert feedback;
   - user ratings влияют на стратегию retrieval.
3. Retriever:
   - Wikipedia URL map;
   - requests + BeautifulSoup;
   - keyword matching;
   - ограничение извлечения через `num_words`.
4. Generator:
   - выбор RAG mode по ranking;
   - user input;
   - expert-feedback document;
   - GPT-4o.
5. Evaluation:
   - response time;
   - TF-IDF cosine similarity;
   - user rating 1–5;
   - expert evaluation.
6. Expert feedback:
   - thumbs up/down UI;
   - callback;
   - запись `expert_feedback.txt`.
7. Резюме и 10 контрольных вопросов.

## Main principle

Глава переводит RAG из статической схемы retrieval→generation в adaptive feedback loop. Качество ответа оценивается не только автоматическими метриками, но и пользователями/экспертами. В зависимости от рейтинга система меняет способ дополнения запроса: отключает RAG, использует expert feedback или обычный retrieval.

## Source-defined rating logic

Narrative behavior:

- rating 1–2: RAG disabled; generator receives user input without retrieved documents;
- rating 3–4: expert-feedback document augments/replaces ordinary retrieval;
- rating 5: ordinary keyword retrieval, optionally using previously collected feedback.

These thresholds are explicitly presented as an educational scenario, not a universal production policy.

## Key operational boundaries

- HTTP scraping is external workload.
- Package installation changes notebook environment.
- Google Drive mount and API-key environment assignment change runtime state.
- Expert feedback and downloaded helper/assets create local files.
- `expert_feedback.txt` is overwritten with `"w"` mode.
- OpenAI generation is an external workload and may be billable.
- User/expert thresholds are example values, not production acceptance criteria.
- The source explicitly argues that cosine similarity does not establish factual correctness.

## Source inconsistencies

### Rating 3–4 vs code

Narrative on `p0144:c01–p0147:c01` says ratings 3 or 4 activate expert-feedback RAG.

Code on `p0148:c01` uses:

`if ranking > 3 and ranking < 5:`

which activates the branch only for `ranking == 4`.

Status: `[Source contradiction]`.

### Expert trigger variable

The chapter computes `mean_score`, but the expert trigger shown on `p0157:c01` compares:

`score_history <= score_threshold`

where `score_history` is described as accumulated score, while `score_threshold=4`.

Status: `[Source contradiction]`.

### User score wording/output

`p0156:c01` says the user enters score `1`, while the displayed prompt/output shows `3`.

Status: `[Source wording/output mismatch]`.

### private_token

`private_token` is passed to helper downloads on `p0148:c01` and `p0157:c01`, but its initialization is not supported by the retrieved chapter chunks used here.

Status: `[Needs confirmation]`.

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [summary.md](./summary.md)
- [review-questions.md](./review-questions.md)
- [review-answers.md](./review-answers.md)

## RAG provenance used

Concept / architecture:
- `p0136:c01–p0140:c01`

Retriever:
- `p0140:c01–p0143:c01`

Adaptive generator logic:
- `p0144:c01–p0152:c01`

Evaluation / user feedback / expert feedback:
- `p0153:c01–p0158:c01`

Chapter-end artifacts:
- `p0159:c01–p0160:c01`

Boundary evidence:
- chapter start: `p0136:c01`
- next chapter start: `p0161:c01`
