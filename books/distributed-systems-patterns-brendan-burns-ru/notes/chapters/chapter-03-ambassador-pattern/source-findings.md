# Source findings — глава 3

Этот файл фиксирует source/RAG operational ambiguities без silent correction.

## Finding 1 — повторное использование redis-shards.yaml

Classification: `[Source wording/code mismatch]`

Provenance:
- StatefulSet: `distributed-systems-patterns-brendan-burns-ru:p0054:c01–p0055:c01`
- Service: `distributed-systems-patterns-brendan-burns-ru:p0055:c01`

Source сначала предлагает сохранить StatefulSet как `redis-shards.yaml` и создать resource из этого файла. Затем отдельный Service снова предлагается сохранить под тем же именем и выполнить ту же file-based creation operation.

Finding:
- source не уточняет, заменяется ли файл, объединяются ли resources или предполагается другая последовательность;
- точный safe procedure из RAG не выводится.

Action:
- обе source instructions сохраняются как есть;
- intended manifest organization: `[Needs confirmation]`;
- silent normalization запрещена.

## Finding 2 — experiment ConfigMap naming mismatch

Classification: `[Source code mismatch]`

Provenance:
- ConfigMap creation instruction: `distributed-systems-patterns-brendan-burns-ru:p0061:c01`
- Pod volume reference: `distributed-systems-patterns-brendan-burns-ru:p0063:c01`

Source creation instruction не указывает имя `experiment-config`, тогда как более поздний Pod manifest ссылается именно на ConfigMap `experiment-config`.

Finding:
- retrieved source не предоставляет self-contained sequence, связывающую создание ConfigMap с именем, которое затем ожидает Pod.

Action:
- исходная команда сохранена в `commands.md`;
- не считать ее verified copy/paste-safe;
- exact intended executable form: `[Needs confirmation]`.

## Finding 3 — YAML indentation sensitivity

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0057:c01`
- `distributed-systems-patterns-brendan-burns-ru:p0062:c01–p0063:c01`

YAML получен из PDF text-layer extraction, а whitespace для YAML семантически значим.

Action:
- chapter artifacts используют manifests для анализа структуры и intent;
- полный production-copy-safe YAML не реконструируется молча;
- exact whitespace-safe form: `[Needs confirmation]`.
