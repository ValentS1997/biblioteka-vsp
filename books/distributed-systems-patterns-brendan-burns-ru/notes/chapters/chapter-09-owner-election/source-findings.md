# Source findings — глава 9

Этот файл фиксирует material source/RAG issues без silent correction.

## Finding 1 — endpoint cluster-name mismatch

Classification: `[Source code mismatch]`

Provenance:
- cluster manifest: `distributed-systems-patterns-brendan-burns-ru:p0159:c01`
- endpoint command: same chunk.

Source manifest names the cluster:

~~~text
my-etcd-cluster
~~~

The endpoint-discovery command references:

~~~text
example-etcd-cluster
~~~

Finding:
- names do not match inside the practical sequence.

Action:
- preserve both source values;
- exact intended endpoint target: `[Needs confirmation]`;
- do not silently replace one name with the other.

## Finding 2 — ETCD_ENDPOINTS shell extraction

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0159:c01`

RAG renders:

~~~text
export ETCD_ENDPOINTS=kubectl get endpoints example-etcd-cluster
"-o=jsonpath={.subsets[*].addresses[*].ip}:2379,"
~~~

Observation:
- command substitution/quoting is not preserved in a shell-safe form;
- exact executable command cannot be established from RAG alone.

Action:
- do not present this line as copy/paste-safe;
- corrected shell syntax: `[Needs confirmation]`.

## Finding 3 — book-era Helm/etcd toolchain

Classification: `[Needs confirmation]`

Provenance:
- `p0158:c01–p0166:c01`

Source uses:
- `helm init`;
- chart `stable/etcd-operator`;
- etcd operator CRD/API from the book era;
- etcd version `3.1.0`;
- source-era etcdctl command forms.

Under `rag_only`, current platform support is not verified or modernized.

## Finding 4 — availability arithmetic is illustrative/coarse

Classification: `[Source arithmetic approximation]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0154:c01–p0155:c01`

Source maps several downtime examples to approximate “nines” of availability.

Observation:
- the examples are used to motivate the singleton-versus-election trade-off;
- the artifact does not promote those rounded values as a universal SLO calculator.

Action:
- preserve the qualitative conclusion;
- exact availability math for a real SLA should be recalculated from actual downtime assumptions.

## Finding 5 — pseudo-code is not compile-ready language source

Classification: `[Source pseudocode]`

Provenance:
- `p0156:c01–p0167:c01`

The lock/election snippets mix Go-like syntax with generic constructs such as `boolean`, `null`, and abstract `compareAndSwap`.

Action:
- treat snippets as algorithmic pseudocode;
- do not silently turn them into compile-ready Go or another language.
