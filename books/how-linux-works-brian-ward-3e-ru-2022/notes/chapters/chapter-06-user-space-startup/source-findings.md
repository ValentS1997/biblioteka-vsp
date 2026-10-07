# Source findings — глава 6 «Запуск пользовательского пространства»

**Scope:** `p0176:c01`–`p0207:c01`, PDF/печатные страницы 176–207. Политика **rag_only**: конфликтующие варианты и дефекты сохраняются без внешнего исправления.

## F-01 — [Source contradiction]: §6.3.5 отсутствует в оглавлении, но присутствует в главе

- **TOC locator:** `p0011:c01`.
- В оглавлении подразделы идут от **6.3.4 «Процесс работы systemd»** сразу к **6.3.6 «Зависимости systemd»**.
- **Body locators:** `p0186:c01`–`p0188:c01`.
- В тексте главы есть явный заголовок **6.3.5 «Отслеживание и синхронизация процессов systemd»** с описанием cgroups и `Type=simple/forking/notify/dbus/oneshot/idle`.
- **Decision:** chapter map includes §6.3.5 because body evidence is explicit; TOC omission is preserved as a source inconsistency rather than silently repaired.

## F-02 — [Source wording/code mismatch]: prefix auxiliary programs

- **Locator:** `p0196:c01`–`p0197:c01`, §6.3.8.
- Source wording states that executable files for the listed systemd services have prefix **`system-`**.
- Immediately afterward it gives `systemd-udevd` as the integrated udevd daemon name.
- **Issue:** wording and concrete executable example do not match.
- **Decision:** artifacts preserve `systemd-udevd` only as the explicit example; the general prefix claim is not normalized to another value. Correct universal prefix: **[Needs confirmation]**.

## F-03 — [Source wording/code mismatch]: dbus.socket described as a service unit

- **Locator:** `p0182:c01`, §6.3.3.
- Source phrase refers to «служебном юните, подобном `dbus.socket`».
- Earlier in `p0179:c01`, `.socket` is explicitly defined as the suffix/type for a **socket unit**, while service units are a separate unit type.
- **Decision:** `dbus.socket` is not used as an example of a service-unit filename in the artifacts; the source wording is recorded, not silently corrected to another filename.

## F-04 — [Source extraction issue]: `.require` directory token

- **Locator:** `p0191:c01`, §6.3.6.
- The extracted text says the `[Install]` section usually affects directories **`.wants` and `.require`**.
- The same passage demonstrates a concrete `.wants` path, but no concrete `.require` path appears elsewhere in the retrieved chapter.
- **Decision:** do not fabricate or normalize the second directory name. Any exact filesystem path corresponding to `RequiredBy=`: **[Needs confirmation]**.

## F-05 — [Source extraction issue]: figures 6.1–6.3 are text-only in RAG

- `p0180:c01`: figure 6.1 dependency graph.
- `p0195:c01`: figure 6.2 sequential startup timeline.
- `p0196:c01`: figure 6.3 systemd resource-unit startup timeline.
- `rag/manifest.yaml` states that images/diagrams are not independently encoded as multimodal RAG objects.
- **Decision:** Mermaid and SVG artifacts reconstruct only relationships explicitly described in surrounding text; original geometry/timing bars/arrow placement remain **[Needs confirmation]**.

## Current-system applicability

Unit names, paths, init implementation, runlevels, cgroup layout, socket availability, initramfs tooling and rescue behavior in the book are examples/edition context. Values for a real host remain **[Needs confirmation]**.
