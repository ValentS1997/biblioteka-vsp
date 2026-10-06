# Шпаргалка: архитектура AI-инженерии и обратная связь

Цель: строить AI-приложение постепенно, фиксируя failure boundaries, observability и feedback loops до добавления следующего слоя сложности.

## Symptom / problem framing

Типовые симптомы:

- модель не знает нужный внешний контекст;
- конфиденциальные данные уходят во внешний API;
- output имеет неверный формат/галлюцинации/unsafe content;
- одна модель слишком дорогая или плохо подходит всем request types;
- provider API меняется и ломает несколько приложений;
- API rate limit/outage нарушает сервис;
- repeated requests создают лишнюю latency/cost;
- agent loop невозможно отладить;
- write action имеет слишком большой blast radius;
- metrics показывают деградацию, но root cause не виден;
- logs не позволяют восстановить request path;
- user feedback есть, но непонятно, что он означает;
- feedback loop начинает усиливать bias.

## Baseline / context

Перед добавлением нового component зафиксировать:

1. Current request path.
2. Existing model(s)/provider(s).
3. Known failure modes.
4. Data/PII boundary.
5. Access-control boundary.
6. Latency/cost baseline.
7. Evaluation metrics.
8. Logging/tracing coverage.
9. Current cache policy.
10. Read-only vs write-capable tools.
11. User-feedback signals.
12. Consent/privacy assumptions.
13. Rollback/config versioning mechanism — `[Needs confirmation]` if absent.

## Read-only checks

### 1. Нарисовать фактический request path

Минимальный baseline:

~~~text
user request
→ application
→ model API
→ response
~~~

Затем отметить фактические additions:

- retrieval/context;
- input guardrail;
- router;
- gateway;
- cache;
- tool/agent loop;
- output guardrail;
- logs/traces;
- feedback capture.

### 2. Для каждого component определить failure mode

Examples from source:

- retrieval → irrelevant context;
- input guardrail → missed secret / false block;
- router → wrong destination;
- gateway → provider/rate/failover issue;
- cache → stale/wrong/private response reuse;
- model → bad/unsafe output;
- tool → failure/wrong result;
- agent → loop/branch failure;
- write action → harmful external change.

### 3. Проверить guardrail boundary

Input:

- PII/confidential data;
- prompt attacks;
- external-API leakage.

Output:

- invalid format;
- inconsistent/hallucinated facts;
- toxic/private content;
- dangerous tool/code execution;
- brand risk;
- false refusals.

### 4. Проверить routing logic

Router should have an explicit reason to choose:

- specialized model;
- cheaper model;
- retrieval;
- human;
- refusal/out-of-scope path.

Source common pattern:

~~~text
routing → retrieval → generation → evaluation
~~~

### 5. Проверить gateway responsibilities

Potential source-confirmed functions:

- unified model interface;
- access control;
- usage/rate/cost control;
- retries/failover;
- load balancing;
- logging/analytics;
- optional cache/guardrails.

### 6. Проверить cache safety

Exact cache:

- key identity;
- personalization;
- time sensitivity;
- eviction policy.

Semantic cache:

- embedding quality;
- vector search;
- similarity metric;
- threshold;
- wrong-match rate;
- privacy boundary.

Never assume a response is shareable across users merely because the request text is similar.

### 7. Проверить observability

Source DevOps metrics:

- MTTD;
- MTTR;
- CFR.

Per request, logs/traces should allow correlation of:

- user request;
- final model prompt;
- model/version/config;
- sampling settings;
- retrieved data;
- tool calls/results;
- component start/end/errors;
- latency;
- measurable cost.

### 8. Проверить feedback signal type

Explicit:

- thumbs up/down;
- rating;
- yes/no;
- direct comparison.

Implicit:

- regeneration;
- edit;
- delete/rename/share/bookmark;
- action acceptance/rejection;
- conversation length;
- conversational corrections/preferences.

Interpretation must remain application-specific.

## Interpretation

### Нужны внешние/актуальные данные

Добавить context construction before adding more model complexity.

### Leaks/unsafe inputs or outputs

Add guardrails at the actual exposure boundary; measure false positives/refusals and latency overhead.

### One model is expensive for easy tasks

Introduce routing only if request classes and evaluation can support it.

### Many apps depend on heterogeneous providers

Gateway can reduce coupling and centralize access/cost/failover policies.

### Repeated identical work dominates latency/cost

Evaluate exact cache first.

### Semantic cache gives high hit rate but wrong answers

Similarity threshold/model is insufficient; a high hit ratio is not success if correctness falls.

### Complex agent is hard to debug

Improve traces and component boundaries before adding orchestration abstraction.

### Monitoring detects issue but root cause is unclear

Observability is insufficient: logs/traces lack correlation or component timing/context.

### Users regenerate often

Likely negative signal, but not definitive; creative exploration can also cause regeneration.

### Long conversations increase

Could be positive engagement or failure loop; interpret with domain + topic/token diversity.

### Feedback becomes increasingly one-sided

Check selection/exposure/position bias and degenerate feedback loops.

## Next action

Source-grounded architecture progression:

1. Start with minimal model path.
2. Add context construction if information is missing.
3. Add input/output guardrails for known risks.
4. Add router/gateway if multiple models/providers create cost/control complexity.
5. Add exact cache where reuse is safe; semantic cache only after validation.
6. Add agent loops/write actions only with explicit safety boundary.
7. Instrument metrics/logs/traces before scale makes debugging harder.
8. Add orchestrator only when manual component composition becomes real complexity.
9. Collect user feedback throughout the user journey.
10. Feed production failures back into evaluation and dataset design.
11. Detect bias/degenerate feedback loops before using feedback as training signal.

## Modifying action

### Add input/output guardrail

What changes: requests/responses are inspected, blocked, masked, retried or escalated.

Risk:

- false positives;
- false refusals;
- latency/cost overhead;
- streaming may expose partial output before final check.

Verification:

- attack/leakage test set;
- format/safety failure rate;
- false refusal rate;
- latency/cost delta.

Rollback: previous guardrail policy/version — exact mechanism `[Needs confirmation]`.

### Add model router

What changes: request destination becomes dynamic.

Risk:

- misrouting;
- inconsistent behavior across models;
- context-limit mismatch.

Verification:

- route accuracy;
- per-route quality;
- cost;
- latency;
- fallback behavior.

Rollback: fixed/default route — exact config `[Needs confirmation]`.

### Add model gateway

What changes: applications call a centralized interface instead of provider APIs directly.

Risk:

- gateway becomes critical dependency;
- incorrect failover/access policy affects many apps.

Verification:

- auth/access tests;
- provider failover;
- rate-limit behavior;
- logs;
- cost controls.

Rollback: prior gateway/config or provider path — `[Needs confirmation]`.

### Enable caching

What changes: prior results may bypass downstream processing.

Risk:

- stale response;
- wrong semantic match;
- cross-user privacy leak;
- cache storage growth.

Verification:

- hit rate;
- correctness on hits;
- latency/cost;
- privacy/isolation tests;
- eviction behavior.

Rollback: disable cache or revert cache policy; exact procedure `[Needs confirmation]`.

### Add agent/write actions

What changes: system can loop, branch and modify external state.

Risk: substantially higher blast radius.

Verification:

- permission boundaries;
- dry-run/read-only tests where possible;
- trace every tool call;
- explicit success/failure criteria;
- post-action state check.

Rollback for external actions: application/tool-specific `[Needs confirmation]`.

### Add orchestration framework

What changes: component composition moves behind an orchestration abstraction.

Risk:

- hidden API calls;
- added latency;
- harder debugging;
- framework coupling.

Verification:

- equivalent functional behavior;
- full traces;
- error propagation;
- latency;
- scalability.

Rollback: previous direct composition — `[Needs confirmation]`.

### Feed user feedback into training/product logic

What changes: production behavior influences future product/model decisions.

Risk:

- response bias;
- position bias;
- random feedback;
- preference bias;
- privacy issues;
- degenerate feedback loop.

Verification:

- feedback-distribution analysis;
- randomized placement where appropriate;
- independent evaluation set;
- slice analysis;
- consent/data-use checks.

Rollback: stop using the signal / revert model or ranking policy — exact process `[Needs confirmation]`.

## Verification / acceptance checks

Architecture change is acceptable only if:

- it solves an observed failure or measurable need;
- component boundary is explicit;
- access/data boundary is explicit;
- new failure modes are documented;
- metrics/logs/traces cover the new path;
- latency/cost impact is measured;
- security/privacy impact is considered;
- evaluation and monitoring use compatible signals;
- write actions have stronger controls than read-only actions;
- feedback is not treated as unbiased ground truth;
- rollback/config version exists or is marked `[Needs confirmation]`.

## Rollback

- Read-only inspection/monitoring: `[Not applicable]`.
- Guardrail/router/gateway/cache/orchestrator configuration: restore previous version `[Needs confirmation]`.
- Model/provider change: restore previous route/model config `[Needs confirmation]`.
- Agent write action: action-specific compensation/rollback `[Needs confirmation]`.
- Feedback-driven model/product change: restore previous model/ranking/policy version `[Needs confirmation]`.

## Минимальная карта

~~~text
AI application
├─ context
├─ guardrails
├─ router
├─ gateway
├─ cache
├─ agent/tools
│  └─ write boundary
├─ observability
│  ├─ metrics
│  ├─ logs
│  └─ traces
├─ orchestration
└─ user feedback
   ├─ explicit
   ├─ implicit
   ├─ privacy/consent
   ├─ bias
   └─ degenerate feedback loop
~~~
