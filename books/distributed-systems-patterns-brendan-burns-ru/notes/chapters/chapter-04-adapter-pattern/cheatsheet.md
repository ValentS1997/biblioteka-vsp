# Шпаргалка: глава 4 — Адаптеры

## Symptom / problem framing

В реальной системе components гетерогенны:
- разные monitoring interfaces;
- разные log formats;
- разные health semantics;
- разные языки и ownership.

Проблема:

~~~text
many native interfaces
→ many integration paths
→ operational complexity
~~~

Adapter:

~~~text
native application interface
→ Adapter
→ standardized operational interface
~~~

## Baseline / context

Adapter работает рядом с application container и преобразует его interface в заранее ожидаемый common interface.

Chapter use cases:
- monitoring;
- logging;
- health checking.

## Read-only checks

Перед Adapter проверить:

1. Какой native interface предоставляет application?
2. Какой standardized interface ожидает infrastructure?
3. Можно ли безопасно изменить application напрямую?
4. Кто владеет application image?
5. Не создаст ли fork/modified image постоянную maintenance burden?
6. Может ли один Adapter быть reused с несколькими applications?
7. Какие shared resources/namespaces нужны?
8. Каким observable endpoint/output подтверждается transformation?
9. Не зависит ли точность monitoring/logging от корректного parsing?
10. Не является ли health check destructive/workload-heavy?

Exact performance/SLO thresholds: `[Needs confirmation]`.

## Interpretation

### Monitoring

~~~text
Redis native metrics
→ redis_exporter Adapter
→ Prometheus-compatible interface
~~~

### Logging

~~~text
application-specific log
→ fluentd Adapter
→ common structured/time-ordered log
→ aggregator
~~~

### Health

~~~text
database-specific diagnostic query
→ health Adapter
→ HTTP status
→ orchestrator decision
~~~

## Next action

1. Зафиксировать target common interface.
2. Зафиксировать native application interface.
3. Выбрать Adapter boundary.
4. Оставить base application image неизменным, если modification ownership слишком дорог.
5. Parameterize Adapter.
6. Развернуть рядом с application.
7. Verify transformed interface/output.
8. Отдельно проверить failure behavior.

## Modifying action

### Redis + Prometheus exporter

Source shows Pod composition with:
- Redis container;
- `oliver006/redis_exporter` Adapter.

Exact deployment command в chapter range не указан.

Effect:
- adds a Prometheus-facing metrics interface.

Risk:
- additional runtime component/resource consumption.

Verification:
- exact Prometheus scrape command/query: `[Needs confirmation]`.

Rollback:
- `[Needs confirmation]`.

### fluentd Adapter

Effect:
- collects Redis SLOWLOG or Storm API data through localhost;
- turns it into queryable/logging output.

Verification:
- resulting log availability is source intent;
- exact command: `[Needs confirmation]`.

Rollback:
- `[Needs confirmation]`.

### MySQL health Adapter

Effect:
- starts an HTTP-facing adapter that executes configured DB query as health logic.

Risk:
- query generates database workload;
- bad query/config can report unhealthy;
- orchestrator may restart application after failed health check.

Verification:
- source returns HTTP 200/OK on success and HTTP 500 on DB error.

Rollback:
- `[Needs confirmation]`.

## Verification / acceptance checks

### Monitoring Adapter

- common monitoring system sees expected standardized interface;
- application container itself remains unchanged;
- Adapter can be versioned independently.

### Logging Adapter

- source data is reachable over shared local interface;
- transformed output is available later for analysis;
- timestamps/structure are normalized as intended.

### Health Adapter

- configured diagnostic query succeeds → adapter returns success;
- query error → adapter returns failure;
- orchestrator reaction is consistent with configured health policy.

Exact Kubernetes health probe configuration is not present: `[Needs confirmation]`.

## Rollback

No universal rollback workflow is supplied.

- remove monitoring Adapter: exact command `[Needs confirmation]`;
- remove fluentd Adapter: exact command `[Needs confirmation]`;
- revert health Adapter: exact command `[Needs confirmation]`.

Do not invent deletion/rollout commands.

## Decision frame

~~~text
Need standard interface?
        |
        +-- can modify owned app cheaply?
        |       → direct adaptation may be valid
        |
        +-- third-party / reusable / separate ownership?
                → Adapter candidate
~~~
