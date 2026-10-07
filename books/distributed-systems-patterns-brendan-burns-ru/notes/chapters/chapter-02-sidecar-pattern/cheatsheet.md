# Шпаргалка: глава 2 — Паттерн Sidecar

## Scope

- RAG: `p0034:c01–p0049:c01`
- PDF: `34–49`
- Source policy: `rag_only`
- Type: architecture + operational examples

## Symptom / problem framing

Типичная задача:

~~~text
application already exists
+ нужна новая cross-cutting capability
+ менять application дорого / неудобно / дублирует код
→ вынести capability в Sidecar
~~~

Chapter examples:
- HTTPS для legacy HTTP application;
- dynamic configuration;
- resource introspection через `topz`;
- Git-sync для простого PaaS.

## Baseline / context

Sidecar model:

~~~text
application container
+ sidecar container
→ one node / atomic group
→ shared resources where needed
~~~

Potential shared resources:
- network namespace;
- PID namespace;
- filesystem/directory;
- hostname/other namespaces.

## Read-only checks

Перед внедрением Sidecar проверить:

1. Какая capability добавляется к application?
2. Можно ли добавить ее без изменения application source?
3. Должны ли containers находиться на одном узле?
4. Какие ресурсы им действительно нужно разделять?
5. Повторяется ли capability в нескольких applications?
6. Какие параметры sidecar должны быть configurable?
7. Каков полный external API sidecar?
8. Есть ли backward-compatible semantics для параметров?
9. Документированы ли ports/defaults/metadata?
10. Не будет ли port conflict с application container?

Для production security/performance SLO глава не дает численных критериев: `[Needs confirmation]`.

## Interpretation

### Legacy HTTP app

~~~text
app listens on 127.0.0.1
+ nginx Sidecar in same network namespace
→ external HTTPS
→ local HTTP proxy
~~~

Это позволяет не пересобирать legacy app ради HTTPS.

### File-based configuration

~~~text
API config
→ config-manager Sidecar
→ shared file
→ notify app
→ reload/restart
~~~

Notification method is application-specific:
- file watch;
- `SIGHUP`;
- last-resort `SIGKILL` + orchestrator restart.

### Repeated introspection functionality

Если `/topz` нужен приложениям на разных языках:

~~~text
language-specific libraries
→ duplicated implementations

Sidecar utility
→ one implementation
→ same interface across applications
~~~

### Reusable component

~~~text
parameterized
+ stable API
+ documented
→ reusable Sidecar
~~~

Если хотя бы один из этих элементов отсутствует, reuse становится хрупким.

## Next action

Source-grounded design sequence:

1. Определить sidecar responsibility.
2. Определить required shared namespace/resource.
3. Отделить application logic от utility logic.
4. Parameterize environment-specific values.
5. Зафиксировать API и semantics.
6. Document ports/defaults/metadata.
7. Deploy beside application.
8. Verify capability through its observable interface.

## Modifying action

### Docker application container

~~~bash
docker run -d <образ-приложения>
~~~

Effect:
- запускает container application.

Risk:
- создает runtime state;
- image-specific behavior: `[Needs confirmation]`.

Verification:
- source предлагает `docker ps`.

Rollback:
- exact stop/remove command в главе отсутствует: `[Needs confirmation]`.

### topz Sidecar

Source command contains a damaged port option and must not be silently normalized. См. `commands.md` / `source-findings.md`.

Effect:
- Sidecar joins application PID namespace;
- exposes topz HTTP service.

Verification:
- обратиться к `http://localhost:8080/topz`.

Rollback:
- `[Needs confirmation]`.

### Dynamic configuration

Effect:
- Sidecar can update shared configuration file and trigger application reload/restart.

Risk:
- wrong config;
- excessive restart;
- `SIGKILL` forcibly terminates application.

Verification:
- application rereads new configuration; exact application-specific check: `[Needs confirmation]`.

Rollback:
- chapter mentions API-driven rollback as a benefit conceptually, but exact procedure is `[Needs confirmation]`.

## Verification / acceptance checks

### HTTPS case

- external requests served via HTTPS;
- local legacy app remains bound to loopback;
- proxy reaches legacy app through shared namespace.

Exact TLS policy/certificate validation procedure: `[Needs confirmation]`.

### Configuration case

- API state and local file differences are detected;
- shared config file updates;
- application reloads/restarts and reads updated configuration.

### topz case

- Sidecar shares PID namespace with application;
- `/topz` returns process/resource view.

### Reusable Sidecar

- all required parameters are explicit;
- parameter names and semantics stable;
- external interactions documented;
- Dockerfile documents ports/defaults/metadata where applicable.

## Rollback

No universal Sidecar rollback workflow is provided in chapter 2.

Per-example rollback:
- HTTPS sidecar removal: exact steps `[Needs confirmation]`;
- config rollback: conceptually enabled by API automation, exact procedure `[Needs confirmation]`;
- topz removal: exact command `[Needs confirmation]`;
- Git-sync PaaS rollback: `[Needs confirmation]`.

Do not invent operational rollback commands outside chapter scope.

## API stability rule

Breaking changes include not only names:

~~~text
UPDATE_FREQUENCY seconds
→ same parameter interpreted differently
→ behavior changes
→ higher request/check frequency
→ consumers silently affected
~~~

Therefore API compatibility = syntax + semantics.
