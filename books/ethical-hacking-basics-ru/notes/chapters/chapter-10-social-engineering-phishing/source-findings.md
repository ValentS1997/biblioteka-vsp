# Source findings — глава 10

Canonical source: PDF pp. 274–297, SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`. Policy: `rag_only`.

## F-01 — [Needs confirmation] “около 80 процентов атак”

- `p0274:c01` утверждает, что на момент написания около 80% атак включают различные методы social engineering.
- В chapter RAG нет ссылки/датасета/методологии для этой цифры.
- Disposition: сохранять как source claim, не как проверенный современный 2026 statistic.

## F-02 — [Source terminology mismatch] Tailgating

- `p0282:c01` использует термин `Tailgating`.
- В summary `p0296:c01` аналогичный physical-access pattern назван методикой «Задней двери».
- Disposition: artifacts используют `tailgating` как основной source term и отмечают summary wording как inconsistent translation/terminology.

## F-03 — [Source extraction issue] Wifiphisher name split

- `p0293:c01` / `p0297:c01` содержит визуально разорванное имя `wi phisher`.
- Это похоже на extraction/line-layout issue.
- Disposition: не восстанавливать версию/точный package identifier из памяти модели; concept/tool family remains source-grounded.

## F-04 — [Historical data] SET / payload menus

- `p0294:c01`–`p0296:c01` показывает historical Social-Engineer Toolkit / Metasploit menu and file-format payload lists.
- Наличие конкретных modules/payloads в книге не означает current-2026 availability/applicability.
- Artifacts не используют их как current inventory.

## F-05 — [High-risk boundary] Website cloning in phishing context

- `p0288:c01`–`p0290:c01` описывает website cloning/mirroring in a phishing context and provides a recursive mirror example.
- The same tooling can be benign for archival/testing, but combined with impersonation it can facilitate credential theft.
- Exact campaign/cloning recipe is not reproduced in commands.md.

## F-06 — [High-risk boundary] Rogue wireless social engineering

- `p0292:c01`–`p0294:c01` describes rogue/imitated AP scenarios capable of collecting credentials or delivering code.
- This can intercept third-party traffic and credentials.
- Artifacts retain threat model and defensive implications only.

## F-07 — [High-risk boundary] Phishing automation / payload delivery

- `p0294:c01`–`p0296:c01` describes automation frameworks that combine phishing with file-format payloads and reverse/session behavior.
- These details can enable credential theft or malware delivery.
- No runnable phishing/payload workflow is reproduced.

## Defensive takeaway

Source supports independent verification of helpdesk/business requests, user awareness of sender/link/attachment anomalies, strong physical-access controls and recognition that known/social identities can be compromised or cloned. Organization-specific policy and technical implementation: **[Needs confirmation]**.
