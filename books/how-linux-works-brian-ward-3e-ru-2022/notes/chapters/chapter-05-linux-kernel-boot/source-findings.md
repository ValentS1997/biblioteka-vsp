# Source findings — глава 5 «Загрузка ядра Linux»

**Scope:** RAG `p0156:c01`–`p0175:c01`, PDF/печатные страницы 156–175. Политика **rag_only**: варианты источника сохраняются; внешняя документация и model memory не используются для исправления.

## F-01 — [Source extraction issue]: malformed UEFI `grub-install` option

- **Locator:** `p0171:c01`, §5.5.3.
- **Source form:** `grub-install --efi-directory=efi_dir –-bootloader-id=name`.
- Перед `bootloader-id` в extracted text находится символ длинного тире/дефиса, за которым следует ещё один hyphen, а не однозначно два ASCII hyphen.
- **Impact:** строка не должна публиковаться как trusted copy-paste shell command.
- **Decision:** сохранить semantic role («bootloader identifier»), но exact executable spelling: **[Needs confirmation]**.

## F-02 — [Source contradiction]: UEFI directory / ESP mountpoint examples

- **Variant A:** `p0170:c01`, §5.5.3: для UEFI нужно определить current mountpoint EFI system partition, «обычно это `/boot/efi`».
- **Variant B:** `p0171:c01`, тот же раздел: переменная `efi_dir` описана как место, где UEFI directory виден системе, «обычно задействуется `/boot/efi/EFI`, потому что раздел UEFI чаще всего монтируется в `/boot/efi`».
- **Issue:** два соседних объяснения не дают однозначного ответа, какое из этих значений должно выступать аргументом `--efi-directory` в executable example.
- **Decision:** оба source variants preserved. Реальный ESP mountpoint/argument must be discovered from the target system: **[Needs confirmation]**.

## F-03 — [Source extraction issue]: broken tokens caused by page/text wrapping

- **Locators:** `p0167:c01`–`p0171:c01`.
- RAG содержит визуальные разрывы в именах `grub.cfg`, `custom.cfg`, `/dev/sdc` и других path/token examples из-за переноса строк.
- В артефактах нормализуются только те формы, которые **однозначно подтверждены повторением рядом** (например, `grub.cfg`, `custom.cfg`).
- Сомнительные shell option tokens (см. F-01) **не нормализуются**.

## F-04 — [Source extraction issue]: figures 5.1–5.2 unavailable as visual RAG

- **`p0163:c01`:** подпись «Рис. 5.1. Меню загрузчика GRUB».
- **`p0164:c01`:** подпись «Рис. 5.2. Редактор настроек GRUB».
- `rag/manifest.yaml` states that images/diagrams are not independently encoded as multimodal RAG objects.
- **Impact:** exact menu layout, highlighting and screenshot details cannot be reconstructed.
- **Decision:** SVG/Mermaid artifacts represent only text-confirmed concepts and commands, not the original UI.

## Namespace warning — source-grounded, not a contradiction

§5.5 intentionally explains that GRUB has its own `root`, `insmod`, `ls` and modules, independent from Linux kernel/user-space meanings. This is a **semantic collision by design**, not a source defect. Artifacts keep the namespaces separate rather than silently translating between them.

## Current-system applicability

Paths, UUIDs, firmware mode, kernel image names, `(hd0,msdos1)`, Secure Boot state and target disks shown in the source are examples. Their values on a real machine remain **[Needs confirmation]**.
