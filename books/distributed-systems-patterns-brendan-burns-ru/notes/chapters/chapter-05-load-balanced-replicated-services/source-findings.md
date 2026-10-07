# Source findings — глава 5

Этот файл фиксирует source/RAG extraction-sensitive fragments без silent correction.

## Finding 1 — Varnish ConfigMap command line wrapping

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0093:c01`

RAG renders the creation instruction across two lines:

~~~text
kubectl create configmap varnish-config
--from-file=default.vcl
~~~

Finding:
- PDF text extraction may have converted visual line wrapping into a real newline;
- semantic intent is clear, but exact shell-line formatting is not asserted.

Action:
- preserve the extracted form;
- exact copy/paste-safe command: `[Needs confirmation]`.

## Finding 2 — Varnish Deployment YAML indentation

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0094:c01`

Observation:
- extracted indentation around `resources.requests`, `memory`, `image`, `ports`, `volumeMounts` and `volumes` is not safe to treat as canonical YAML;
- YAML whitespace is semantically significant.

Action:
- artifacts preserve configuration intent and individual values;
- full manifest is not represented as production-copy-safe;
- exact whitespace-safe manifest: `[Needs confirmation]`.

## Finding 3 — nginx Deployment YAML indentation

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0099:c01–p0100:c01`

Observation:
- extracted `ports`, `volumeMounts` and volume blocks have indentation whose exact structural meaning cannot be safely reconstructed from text layer alone.

Action:
- use source as architecture/configuration evidence only;
- do not silently normalize to a deployable manifest;
- exact whitespace-safe manifest: `[Needs confirmation]`.

## Finding 4 — current platform compatibility

Classification: `[Needs confirmation]`

Provenance:
- Deployment examples: `p0086:c01`, `p0094:c01`, `p0099:c01`.

Source manifests use the API identifiers printed in the book.

Under `rag_only` policy, this analysis does not verify current Kubernetes API support or translate manifests to newer APIs.

Action:
- current compatibility: `[Needs confirmation]`;
- no web/model-memory modernization is applied.
