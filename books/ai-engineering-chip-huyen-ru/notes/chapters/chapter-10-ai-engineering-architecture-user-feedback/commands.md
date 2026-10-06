# Команды, инструменты и действия главы 10

Source policy: `rag_only`.

Глава 10 не предоставляет shell-runbook. Ниже включены только явно названные source tools, code patterns and state-changing actions.

## Shell / CLI commands

`[Not applicable]`

Не добавляются команды установки или запуска перечисленных frameworks, gateways, databases или observability systems: CLI syntax в chapter RAG не приведен.

## Model-gateway code pattern

Class: `state-changing application code`.

Источник показывает упрощенную, прямо обозначенную как нерабочую production-версию обертку над несколькими model APIs. В примере credentials читаются из environment variables, а не встраиваются в код.

Source-confirmed structure:

~~~python
def openai_model(input_data, model_name, max_tokens):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    # provider call
    return {"response": ...}

def gemini_model(input_data, model_name, max_tokens):
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    # provider call
    return {"response": ...}

@app.route("/model", methods=["POST"])
def model_gateway():
    # read model_type/model_name/input_data/max_tokens
    # dispatch to selected provider
    return jsonify(result)
~~~

Operational note from source: the example omits error handling and optimization; it is an architectural illustration, not a deployable implementation.

Effect:
- centralizes provider dispatch.

Risk:
- gateway becomes a shared failure/security boundary.

Verification:
- provider selection;
- access policy;
- error/failover behavior;
- logging;
- latency.

Rollback: previous application/provider path — `[Needs confirmation]`.

## Guardrail tools named in the chapter

| Tool | Class | Source role |
|---|---|---|
| Purple Llama | workload-generating / state-changing integration | application/model safety tooling |
| NVIDIA NeMo Guardrails | state-changing integration | guardrails |
| Azure PyRIT | workload-generating / security testing | AI risk testing |
| Azure AI content filters | state-changing integration | content filtering |
| Perspective API | workload-generating / service integration | content/toxicity analysis |
| OpenAI content moderation API | workload-generating / service integration | moderation |

Exact API/CLI syntax is not supplied.

## Input-guardrail actions

Source-confirmed actions:

- detect PII/confidential data;
- block request;
- mask sensitive value with placeholder;
- restore value through reverse mapping after model response.

Class: `state-changing request-processing policy`.

Risk:
- false positives;
- unmasked leakage;
- incorrect reverse mapping.

Verification:
- known-PII test set;
- output inspection;
- external-API payload inspection.

Rollback: prior masking/blocking policy — `[Needs confirmation]`.

## Output-guardrail actions

Source-confirmed:

- detect invalid format;
- detect factual inconsistency/hallucination;
- detect toxicity/private data;
- detect unsafe tool/code actions;
- retry;
- generate alternatives in parallel and choose a better one;
- escalate to human.

Class: `state-changing serving policy`.

Risk:
- latency and API-cost increase;
- false refusal;
- streaming can expose unsafe partial output.

Verification:
- failure rate;
- false refusal rate;
- latency/cost;
- human-escalation rate.

Rollback: previous policy `[Needs confirmation]`.

## Router

Class: `state-changing request-routing policy`.

Source-confirmed routing destinations/examples:

- FAQ/static answer;
- human operator;
- specialized troubleshooting model;
- cheaper/general model;
- out-of-scope refusal;
- model with sufficient context window.

Common source flow:

~~~text
route → retrieve → generate → evaluate
~~~

Verification:
- route correctness;
- quality by route;
- latency/cost.

Rollback: fixed/default route `[Needs confirmation]`.

## Model gateway products named in the chapter

- Portkey AI Gateway;
- MLflow AI Gateway;
- Wealthsimple LLM Gateway;
- TrueFoundry;
- Kong;
- Cloudflare.

Class: `state-changing infrastructure integration`.

Source-confirmed gateway capabilities include:

- unified API;
- access control;
- usage/cost control;
- failover/retry;
- load balancing;
- logging/analytics;
- optional cache/guardrails.

No version or CLI syntax is supplied.

## Exact caching

Class: `state-changing cache policy`.

Source-confirmed storage examples:

- in-memory store;
- PostgreSQL;
- Redis;
- tiered storage.

Source-confirmed eviction policies:

- LRU;
- LFU;
- FIFO.

Risk:
- stale/time-sensitive data;
- personalized/private response reused for another user.

Verification:
- hit correctness;
- user isolation;
- TTL/eviction behavior;
- latency/cost delta.

Rollback: disable cache / previous cache config `[Needs confirmation]`.

## Semantic caching

Class: `state-changing cache policy`.

Source algorithm:

~~~text
request
→ embedding
→ vector search nearest cached request
→ similarity score X
→ if X >= threshold: return cached result
→ else: process request and store embedding + result
~~~

Source-required components:

- embedding model;
- vector database/search;
- similarity metric;
- threshold.

Risk:
- false semantic match;
- wrong cached result;
- vector-search cost/latency.

Verification:
- semantic-hit correctness;
- threshold evaluation;
- cost;
- latency.

Rollback: exact-cache/no-cache path `[Needs confirmation]`.

## Agent/write actions

Class: `state-changing external action`.

Source examples:

- compose/send email-like action;
- place order;
- initiate bank transfer.

Effect: system changes external environment.

Risk: materially larger safety blast radius.

Verification:
- explicit permissions;
- trace;
- post-action state;
- human confirmation where application requires it `[Needs confirmation]`.

Rollback: action-specific compensation `[Needs confirmation]`.

## Observability metrics

Class: `read-only measurement`.

Source DevOps metrics:

- MTTD — mean time to detection;
- MTTR — mean time to response;
- CFR — change failure rate.

Source monitoring metrics/examples include:

- invalid-output-format rate;
- factual consistency;
- toxicity;
- PII/confidential-data detections;
- guardrail activation rate;
- refusal rate;
- anomaly rate;
- user stops generation;
- conversation turns;
- input/output token lengths;
- retrieval relevance/precision;
- vector-database memory/query latency;
- request/token/API cost;
- cache cost and hit rate;
- TTFT/TPOT from chapter 9 context.

## Logging

Class: `read-only telemetry collection`.

Source recommends logging:

- model endpoint;
- model name/version;
- sampling settings: temperature, top-p, top-k, stop conditions;
- prompt template;
- user request;
- final model prompt;
- output;
- intermediate results;
- tool calls and outputs;
- component start/end/failure;
- labels/IDs for correlation.

Risk: logs can contain sensitive user/model data; retention/redaction policy `[Needs confirmation]`.

## Tracing

Class: `read-only telemetry collection`.

A trace should reconstruct:

~~~text
user request
→ preprocessing
→ retrieval/context
→ model/tool calls
→ evaluation/guardrails
→ final response
~~~

and include per-step latency and cost where measurable.

Source example tool: LangSmith.

## Drift checks

Class: `read-only analysis`.

Source drift examples:

- system prompt changed;
- user behavior changed;
- underlying provider model changed.

Verification:
- correlate changes with metrics/logs/traces;
- feed production failures into evaluation.

## Orchestration tools named in the chapter

- LangChain;
- LlamaIndex;
- Flowise;
- Langflow;
- Haystack.

Class: `state-changing application integration`.

Source evaluation criteria:

- integration/extensibility;
- complex pipeline support;
- usability;
- performance;
- scalability;
- visibility of API calls/errors.

Source warning: design the application before adopting an orchestrator where possible; premature abstraction can make debugging harder.

## User-feedback actions

Class: `state-changing product/data collection`.

Explicit signals:

- thumbs up/down;
- rating;
- yes/no;
- comparative preference.

Implicit signals:

- regeneration;
- accepting/rejecting suggestions;
- delete/rename/share/bookmark;
- conversation length;
- natural-language correction;
- edits/actions.

Verification:
- signal distribution;
- bias analysis;
- privacy/consent;
- correlation with target product metric;
- independent evaluation.

Rollback: stop/revert use of signal in ranking/training/product policy `[Needs confirmation]`.

## Operational boundary

- No unsupported shell commands or provider SDK signatures were added.
- Source gateway code is intentionally represented as a non-production architectural pattern.
- Secrets remain environment references; no credentials are embedded.
- Every state-changing component needs application-specific rollback/versioning where the source does not specify it.
