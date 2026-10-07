# Source findings — глава 8 «Процессы и использование ресурсов»

**Scope:** `p0244:c01`–`p0269:c01`, PDF/печатные страницы 244–269. Политика **rag_only**: source variants are preserved; no external/model correction is used.

## F-01 — [Source wording/code mismatch]: `pids` controller vs `+pid`

- **Locator A:** `p0267:c01`, §8.6.2–8.6.3.
- Source explicitly names the controller/files as `pids`, `pids.current` and `pids.max`.
- **Locator B:** `p0268:c01`, §8.6.3.
- Source says that to give a child group CPU and PID controllers, write **`+cpu +pid`** to `cgroup.subtree_control`.
- **Mismatch:** singular `pid` in the write example versus `pids` everywhere around it.
- **Decision:** do not silently normalize the command. `commands.md` records the state-changing concept and marks the exact controller token as source-ambiguous. Correct target-system value: **[Needs confirmation]**.

## F-02 — [Source extraction issue]: annotation marker embedded in cgroup path

- **Locator:** `p0265:c01`, §8.6.1.
- Extracted output contains `/testcgroup ❶`.
- Surrounding prose uses ❶ as a figure/list annotation pointing to that example group.
- **Decision:** conceptual references use `/testcgroup`; the marker is not treated as part of the cgroup name.

## F-03 — [Source extraction issue]: original cgroup figures unavailable

- **`p0264:c01`:** fig. 8.1 — cgroups v1, one group per controller.
- **`p0265:c01`:** fig. 8.2 — cgroups v2, one cgroup with multiple controllers.
- `rag/manifest.yaml` states that images/diagrams are not independently encoded as multimodal RAG objects.
- **Decision:** chapter Mermaid/SVG diagrams reconstruct only the relationships explicitly described in the text. Exact visual layout/labels/arrows of figures 8.1–8.2 remain **[Needs confirmation]**.

## F-04 — [Needs confirmation]: exact `ionice` syntax absent

- **Locator:** `p0262:c01`, §8.5.6.
- Source says `ionice` can be used to check and change process I/O priority and points to `ionice(1)`.
- No concrete invocation syntax is provided in the chapter.
- **Decision:** record `ionice` as a source-confirmed tool, but do not invent flags/arguments in `commands.md`.

## Current-system applicability

PIDs, device names, process names, cgroup paths, controller layout, page size, memory pressure thresholds and acceptable scheduler priorities shown in examples are source context, not live-host facts. All target values remain **[Needs confirmation]**.
