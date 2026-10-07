# Source findings — глава 10

Этот файл фиксирует material source/RAG inconsistencies и extraction-sensitive code без silent correction.

## Finding 1 — source API path/port mismatch

Classification: `[Source code mismatch]`

Provenance:
- API contract: `distributed-systems-patterns-brendan-burns-ru:p0176:c01–p0177:c01`
- Python queue manager: `p0181:c01–p0182:c01`
- NodeJS source example: `p0183:c01`

Documented source API:

~~~text
http://localhost/api/v1/items
http://localhost/api/v1/items/<item-name>
~~~

Python queue manager calls:

~~~text
http://localhost:8000/items
http://localhost:8000/items/<item>
~~~

NodeJS source example sets:

~~~text
port = 8080
~~~

Finding:
- path prefix and port representations do not form one internally consistent end-to-end practical configuration.

Action:
- preserve all source forms;
- exact intended binding/path: `[Needs confirmation]`;
- do not silently rewrite examples into one configuration.

## Finding 2 — Python line wrapping / compile-ready status

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0181:c01`

RAG renders:

~~~text
response =
  requests.get(...)
~~~

Observation:
- PDF line wrapping breaks Python assignment formatting;
- extracted block must not be treated as verified compile-ready source.

Action:
- artifacts use semantic behavior only;
- exact whitespace-safe Python: `[Needs confirmation]`.

## Finding 3 — Kubernetes Python API is book-era source

Classification: `[Needs confirmation]`

Provenance:
- `p0181:c01–p0182:c01`

The source constructs Kubernetes client objects directly and uses the API identifiers printed in the book.

Under `rag_only`:
- current Kubernetes Python client compatibility is not verified;
- no modernization is applied.

## Finding 4 — ffmpeg output description mismatch

Classification: `[Source wording/code mismatch]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0184:c01`

Source command:

~~~text
ffmpeg -i ${INPUT_FILE} -frames:v 100 thumb.png
~~~

The following prose refers to generated files such as:

~~~text
thumb1.png, thumb2.png, ...
~~~

Finding:
- fixed output literal `thumb.png` and numbered output examples are not textually aligned.

Action:
- preserve command and prose independently;
- exact intended output pattern: `[Needs confirmation]`.

## Finding 5 — scaling math is a simplified average-rate model

Classification: `[Source modeling limitation]`

Provenance:
- `p0185:c01–p0187:c01`

Chapter compares average inter-arrival interval with average processing time divided by parallelism.

Observation:
- this is the explicit chapter model for queue stability and scaling;
- source does not model variance, retries, failures, burst distributions or percentile latency.

Action:
- keep the model within its stated scope;
- production sizing beyond this average-rate model: `[Needs confirmation]`.
