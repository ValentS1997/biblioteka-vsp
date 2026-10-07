# Шпаргалка: глава 8 — Функции и событийно-ориентированная обработка

## Symptom / problem framing

Есть короткоживущая реакция на discrete event/request, которая:
- независима от основной session flow;
- почти не хранит local state;
- может масштабироваться по числу событий;
- не требует постоянно работающего process.

Candidate:

~~~text
event
→ FaaS function
→ result / next event
~~~

## Baseline / context

FaaS:
- event/request-driven;
- stateless by design;
- network-coupled;
- state lives externally;
- scaling/restart can be delegated to platform.

Serverless и event-driven — разные axes; одно не гарантирует другое.

## Read-only checks

1. Work unit короткоживущий?
2. Есть discrete trigger?
3. Нужен ли long-running background process?
4. Нужно ли preload большого dataset in memory?
5. Какой expected request rate?
6. Видна ли dependency graph functions?
7. Есть ли cycle risk?
8. Где хранится shared state?
9. Есть monitoring/alerting?
10. Какие side effects можно вынести из synchronous path?
11. Может ли flow быть выражен как Event Pipeline?

## Interpretation

### Good fit

~~~text
rare/variable events
+ independent handler
+ little local state
+ asynchronous side effect
→ FaaS useful
~~~

### Poor fit

~~~text
always busy
or long-running background work
or heavy warm-up / large in-memory state
→ long-running service may fit better
~~~

### Decorator

~~~text
request
→ lightweight transformation
→ main API
~~~

### Event handler

~~~text
main service event
→ async function
→ slow/non-critical side effect
~~~

### Event Pipeline

~~~text
event → function → event → function → ...
~~~

## Next action

1. Identify discrete event boundary.
2. Remove long-running/state-heavy work from FaaS candidate.
3. Define input/output contract.
4. Define external state dependencies.
5. Map function-to-function calls.
6. Detect potential cycles.
7. Add monitoring/alerting.
8. Deploy minimal function.
9. Verify trigger/result.
10. Re-evaluate cost once traffic becomes sustained.

## Modifying action

Source-supported modifying actions:
- install Kubeless;
- deploy functions;
- invoke example function.

Exact commands: `commands.md`.

Risk:
- changes cluster/function runtime state;
- source runtime identifiers may be obsolete today;
- function invocation can generate external side effects.

## Verification / acceptance checks

### Decorator
- missing fields receive expected default values;
- transformed payload reaches underlying API.

### 2FA handler
- code is generated;
- login service receives registration;
- user gets message;
- synchronous login UI does not need to wait for full side-effect chain.

### Event Pipeline
- required handlers always run;
- optional handlers run only when condition exists;
- context can be traced across steps.

Exact modern observability commands: `[Needs confirmation]`.

## Rollback

Chapter does not provide a complete rollback procedure.

- Kubeless installation rollback: `[Needs confirmation]`;
- function deployment rollback: `[Needs confirmation]`;
- event-pipeline rollback: `[Needs confirmation]`.

Do not infer delete/rollback commands from model knowledge.
