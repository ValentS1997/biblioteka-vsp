# Diagram — Глава 4 (RAG-only)

Source: PDF 143–180; Pod p0144–p0149, Job p0165–p0172, CronJob p0173–p0178. Conceptual reconstruction from extracted text, not an exact reproduction of source figures.

```mermaid
flowchart TD
 A["kubectl / API"] --> B["Pod"]
 B --> C["Container 1"]
 B --> D["Container 2 if present"]
 B --> E["Shared network and volumes"]
 F["CronJob schedule"] --> G["Job"]
 G --> B
```

## Flow of chapter exercises

```mermaid
flowchart TD
 A["Configured cluster and Ready node"] --> B["Create Pod with run or apply"]
 B --> C["Read with get and describe"]
 C --> D{"Expected state?"}
 D -->|No| E["Inspect conditions and events"]
 E --> C
 D -->|Yes| F["Temporary port-forward to nginx"]
 F --> G["Add labels / annotations"]
 G --> H["Job and CronJob exercises"]
 H --> I["Controlled cleanup"]
```

Source caveat: creating or deleting objects changes a Kubernetes cluster; labels may affect selectors, CronJob schedules repeat executions. Read-only verification and effects are separated in cheatsheet.md and commands.md. Rollback for arbitrary changes: [Needs confirmation].
