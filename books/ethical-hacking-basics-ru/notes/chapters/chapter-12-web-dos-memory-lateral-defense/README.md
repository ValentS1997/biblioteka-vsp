# Глава 12 — веб-приложения, DoS, memory corruption и защитная архитектура

> Общее название главы — редакционное. Source RAG подтверждает разделы `12.1 Атаки на веб-приложения - OWASP, XSS, SQL injection` и `12.2 Dos, Buffer Over ow, Heap Spraying, Гориз.перемещение, Защита`. Статус: `RAG_GROUNDED`; reading state не меняется.

## Источник и границы

- Книга: «Основы этичного хакинга», А. В. Чумилин; `book_id: ethical-hacking-basics-ru`.
- Canonical source: `source/book.pdf`; SHA-256 `80047d7ba9b3799f4ff9b4197cce7ee2e2e9da86bdf7a8bea11b805707507b25`.
- PDF pages **324–349**, 1-indexed: **26 страниц / 44 addressable RAG chunks**.
- Первый chunk: `p0324:c01`; последний: `p0349:c02`.
- Overlap chunks: p. 325–331, 333–334, 339, 341–343, 345–349.
- PDF p. **349** — последняя страница canonical RAG/PDF; p. 350 отсутствует.
- Source policy: `rag_only`; direct PDF/web/model-memory supplementation не применялись.
- Book readiness: `READY`; RAG: `READY_WITH_KNOWN_LIMITATIONS`; chapter contract v1.7.

## Структура

| Раздел | PDF pages | Содержание |
| --- | ---: | --- |
| **12.1 Атаки на веб-приложения - OWASP, XSS, SQL injection** | 324–335 | web architecture, OWASP Top 10 (2021), XXE, XSS, SQL injection, command injection, traversal/access-control issues, validation, WAF/ModSecurity |
| **12.2 Dos, Buffer Over ow, Heap Spraying, Гориз.перемещение, Защита** | 336–349 | DoS/DDoS/amplification/slow attacks, buffer overflow, ASLR/canaries/NX concepts, heap spraying, lateral movement, defense-in-depth/breadth, DMZ/honeypots, logging/SIEM, defensible architecture |

## Главный принцип

**The common failure mode is insufficient trust-boundary enforcement: input, memory, identity and network movement must all be constrained and observable.** Source moves from application input validation to memory-safety mitigations and finally to architecture that assumes compromise is possible and prioritizes visibility, segmentation, containment and response.

Offensive examples for injection, DoS, memory exploitation and lateral movement are source-grounded threat material, but they are not converted into runnable exploitation/denial-of-service workflows.

## Карта знаний

1. **Web application model:** client → web/app logic → data layer; server-side trust boundaries matter. `p0324:c01`–`p0325:c01`.
2. **OWASP 2021 framing:** broken access control, cryptographic failures, injection, insecure design, misconfiguration, vulnerable/outdated components, auth failures, software/data integrity, logging/monitoring failures, SSRF. `p0325:c01`–`p0326:c01`.
3. **Injection family:** XXE, XSS, SQL and command injection illustrate why untrusted input must not flow directly into interpreters/subsystems. `p0326:c01`–`p0332:c01`.
4. **Traversal/access control:** URL/path manipulation and direct-resource assumptions can bypass intended application navigation. `p0332:c01`–`p0334:c01`.
5. **Defensive application controls:** validation, tested libraries and WAF/ModSecurity/CRS as additional—not sufficient alone—controls. `p0334:c01`–`p0335:c01`.
6. **Availability attacks:** amplification, distributed and slow-request patterns exhaust network/application resources. `p0336:c01`–`p0340:c01`.
7. **Memory corruption:** buffer overflow and heap spraying are paired with ASLR, stack canaries and non-executable-memory concepts. `p0340:c01`–`p0344:c01`.
8. **Lateral movement:** post-compromise reconnaissance/credential access enables movement toward higher-value systems. `p0344:c01`–`p0346:c01`.
9. **Architecture/response:** segmentation, firewalls, UTM, DMZ/honeypots, logs/SIEM, endpoint isolation and a defensible network architecture provide detection/containment after initial compromise. `p0346:c01`–`p0349:c02`.

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [source-findings.md](source-findings.md)

Отдельного блока **«Практическое задание»** на PDF pp. 324–349 не обнаружено; review-файлы не создаются.

## Safety boundary

Source содержит concrete injection strings, command/traversal examples, SlowHTTP/DoS tooling, memory-exploitation/shellcode concepts and lateral-movement credential collection. Они могут enable exploitation, service disruption or unauthorized movement. Artifacts preserve taxonomy, evidence and defensive implications but do **not** reproduce runnable exploit/DoS/lateral-movement sequences. Target application, authorized test scope, rate/impact limits, rollback and recovery: **[Needs confirmation]**.
