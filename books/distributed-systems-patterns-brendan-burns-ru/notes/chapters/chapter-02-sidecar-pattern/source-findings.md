# Source findings — глава 2

Этот файл фиксирует material source/RAG defects без silent correction.

## Finding 1 — topz port option

Classification: `[Source extraction issue]`

Provenance:
- chunk: `distributed-systems-patterns-brendan-burns-ru:p0041:c01`
- PDF page: `41`

RAG-extracted fragment:

~~~text
docker run --pid=container:${APP_ID} \
    -  p 8080:8080 \
    brendanburns/topz:db0fa58
    /server -addr 0.0.0.0:8080
~~~

Finding:
- option is extracted as `-  p` with whitespace between hyphen and `p`;
- this makes exact executable syntax unreliable;
- chapter text clearly describes port 8080 exposure, but exact corrected option spelling is not reconstructed from model knowledge.

Action:
- preserve extracted variant;
- do not present a silently corrected command;
- exact intended command: `[Needs confirmation]`.

## Finding 2 — LABEL namespace inconsistency

Classification: `[Needs confirmation]`

Provenance:
- chunk: `distributed-systems-patterns-brendan-burns-ru:p0048:c01`
- PDF page: `48`
- related text: `distributed-systems-patterns-brendan-burns-ru:p0049:c01`

Source example:

~~~dockerfile
LABEL "org.label-schema.vendor"="name@company.com"
LABEL "org.label.url"="http://images.company.com/my-cool-image"
LABEL "org.label-schema.version"="1.0.3"
~~~

Observation:
- first and third keys use `org.label-schema.*`;
- middle key uses `org.label.url`;
- next page says the metadata label names are borrowed from the Label Schema project.

No adjudication is possible under rag_only policy without importing an external specification or direct canonical-source inspection.

Action:
- preserve all three source variants;
- do not normalize `org.label.url` to another key;
- exact intended namespace: `[Needs confirmation]`.
