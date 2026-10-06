# Шпаргалка: RAG и агенты по главе 6

Цель: локализовать качество и риск по компонентам: retrieval → generation → tools → planning → execution → memory.

## Symptom / problem framing

Типовые симптомы:

- модель отвечает уверенно, но ей не хватает релевантного контекста;
- retrieval возвращает нерелевантные документы;
- нужный документ существует, но не попадает в top-k;
- после увеличения числа chunks растут cost/latency без роста качества;
- conversational query не работает без истории;
- agent выбирает отсутствующий tool;
- tool выбран правильно, но параметры неверны;
- план выглядит логично, но цель не достигается;
- agent считает задачу выполненной, хотя часть ограничений нарушена;
- context переполняется промежуточными результатами.

## Baseline / context

Для RAG зафиксировать:

1. corpus/source;
2. chunking strategy + overlap;
3. retrieval algorithm;
4. embedding model, если используется;
5. index/vector-store algorithm;
6. top-k/candidate count;
7. reranking strategy;
8. query-rewrite logic;
9. retrieval evaluation set;
10. end-to-end answer metrics;
11. latency/cost/index size.

Для agent system зафиксировать:

1. environment;
2. goal + constraints;
3. tool inventory;
4. read-only vs write tools;
5. tool schemas;
6. planner model/config;
7. reflection/re-planning logic;
8. memory model;
9. tool-call logs;
10. success/failure/efficiency metrics.

## Read-only checks

### 1. Проверить retrieval отдельно от generation

Измерить:

- context precision;
- context recall;
- NDCG / MAP / MRR, если важен ranking;
- embedding quality;
- latency;
- index build time;
- index size.

Затем отдельно проверить final RAG answer.

### 2. Проверить lexical baseline

Term-based retrieval — простой baseline. Если он уже хорошо решает workload, embedding complexity должна оправдываться измеримым improvement.

### 3. Проверить chunking

Проверить:

- не разрывается ли смысл на границе;
- нужен ли overlap;
- chunk помещается в generator/embedding context;
- сколько chunks попадает в model context;
- не вырос ли index/search space слишком сильно.

Универсального оптимума нет.

### 4. Проверить hybrid/reranking

Если один retrieval method недостаточен:

- lexical → candidate set;
- semantic reranker;
- или parallel retrieval + rank fusion.

Проверить improvement относительно дополнительных cost/latency.

### 5. Проверить query modification

Conversational/ambiguous query должен быть переписан в self-contained query.

Если система не знает недостающую сущность, она не должна ее придумывать.

### 6. Проверить agent plan и tool calls

Всегда логировать:

- выбранный tool;
- parameters;
- parameter values;
- tool output;
- следующий plan step.

Это позволяет отделить planner error от tool error.

### 7. Проверить write boundary

Write action — это отдельный risk class.

Проверить:

- может ли agent менять DB/files/accounts;
- есть ли authorization/approval layer;
- отделены ли read-only tools от write tools;
- можно ли выполнить state change ошибочным/hijacked plan.

## Interpretation

### Низкий context precision

Retriever возвращает много нерелевантных документов. Рассмотреть reranking, chunking, query rewrite или другой retrieval method.

### Низкий context recall

Нужные документы часто не попадают в результат. Проверить corpus coverage, chunking, query formulation и retrieval algorithm.

### Хороший retrieval, плохой final answer

Проблема, вероятно, уже в generation/prompting или interpretation контекста; retrieval менять без evidence не следует.

### Semantic retrieval лучше, но намного дороже

Сравнить improvement с embedding/index/query cost. Глава рассматривает cost/latency как часть выбора retrieval system.

### Agent вызывает invalid tool

Planner/inventory/interface problem, а не tool execution failure.

### Tool корректный, output неправильный

Это tool failure. Тестировать tool независимо.

### План допустим, но цель не достигнута

Goal/planning failure или нарушение constraint. Проверять actual end-state, не только plan text.

### Agent выполнил задачу, но слишком дорого/долго

Это efficiency failure. Измерять steps, cost и action latency.

### Контекст переполнен

Разделить short-term и long-term memory; применить eviction/summarization strategy и проверить, не теряется ли критичная информация.

## Next action

Для нового RAG:

1. term-based baseline;
2. evaluation set;
3. chunking experiment;
4. measure precision/recall + end-to-end;
5. при необходимости embeddings;
6. при необходимости hybrid/reranking;
7. query rewrite/contextual metadata;
8. remeasure cost/latency.

Для нового agent:

1. определить environment/goal/constraints;
2. дать минимально нужный tool inventory;
3. разделить read/write capabilities;
4. логировать tool calls;
5. оценить plan validity;
6. independently test tools;
7. измерить goal success + efficiency;
8. добавить reflection/re-planning только если дает измеримый эффект;
9. добавить memory strategy по мере роста state.

## Modifying action

### Изменение chunking/index

Что меняется: corpus representation и retrieval search space.

Risk:

- потеря связности;
- рост index size;
- больше embeddings;
- снижение query speed.

Verification:

- retrieval precision/recall;
- end-to-end answer quality;
- index build time/size;
- query latency.

Rollback: вернуть предыдущую chunk/index version; конкретная procedure — `[Needs confirmation]`.

### Добавление embedding/hybrid retrieval

Effect: улучшение semantic matching потенциально ценой compute/storage/latency.

Verification: сравнить с lexical baseline на одном evaluation set.

Rollback: previous retrieval configuration — `[Needs confirmation]`.

### Добавление нового agent tool

Что меняется: action space агента.

Risk: больше возможностей, но сложнее planning и больше failure/security surface.

Verification:

- tool unit evaluation;
- planner selection accuracy;
- valid parameter rate;
- goal completion;
- safety boundary для write actions.

Rollback: удалить/disable tool из inventory — точная implementation `[Needs confirmation]`.

### Изменение memory policy

Что меняется: что остается в short-term context и что переносится в long-term storage.

Risk: потеря ранней критичной информации или рост context/cost.

Verification:

- task success на длинных interactions;
- retrieval from memory;
- consistency;
- context usage/cost.

Rollback: previous memory policy — `[Needs confirmation]`.

## Verification / acceptance checks

Система соответствует логике главы, если:

- retrieval оценивается отдельно от generation;
- есть lexical baseline;
- chunking выбран экспериментально;
- hybrid/reranking оправданы метриками;
- query rewriting не выдумывает неизвестные entities;
- agent tool inventory минимально достаточен;
- каждый tool call и parameters наблюдаемы;
- planner errors отделены от tool errors;
- write-actions имеют отдельный safety/authorization boundary;
- agent success включает constraints и time;
- efficiency измеряется;
- memory policy проверена на длинных задачах.

## Rollback

- Read-only evaluation: `[Not applicable]`.
- Index/chunking change: `[Needs confirmation]`.
- Retrieval algorithm change: `[Needs confirmation]`.
- Tool inventory change: `[Needs confirmation]`.
- Write authorization policy change: `[Needs confirmation]`.
- Memory policy change: `[Needs confirmation]`.

## Минимальная карта памяти

~~~text
RAG
├─ index
├─ retrieve
│  ├─ lexical
│  ├─ embedding
│  ├─ hybrid
│  └─ rerank / RRF
├─ optimize
│  ├─ chunking + overlap
│  ├─ query rewrite
│  └─ contextual retrieval
└─ evaluate
   ├─ precision / recall
   ├─ NDCG / MAP / MRR
   └─ end-to-end output

Agent
├─ environment
├─ tools
│  ├─ read
│  └─ write
├─ plan
├─ reflect
├─ execute
├─ evaluate failures
└─ memory
   ├─ internal
   ├─ short-term
   └─ long-term
~~~
