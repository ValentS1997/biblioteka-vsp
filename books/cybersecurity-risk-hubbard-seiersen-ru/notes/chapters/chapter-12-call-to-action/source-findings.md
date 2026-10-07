# Глава 12 — source findings

**Book:** `cybersecurity-risk-hubbard-seiersen-ru`. **Boundary:** EPUB spine 45. **Mode:** `rag_only`.

## F-01 — [Source extraction issue] Рис. 12.1 не доступен как самостоятельный RAG-объект

- Locator: `e0045:c02`.
- Caption: «Функция управления рисками кибербезопасности».
- Prose описывает роли/функции, но точная оргсхема, линии подчинения и layout изображения отсутствуют.
- Решение: не реконструировать original figure; Mermaid показывает только подтверждённые функции.

## F-02 — [Source-context caution] Governance recommendation is normative

Source recommends URK reporting to CEO/board and argues against subordination to CIO/CTO. Это позиция авторов, а не универсальное legal/regulatory requirement.

Local governance applicability: **[Needs confirmation]**.

## F-03 — [Source-context caution] Staffing ratio is illustrative

Source says a ratio around 10 new models per analyst «seems reasonable», immediately noting dependence on complexity (`e0045:c02–c03`). It is not treated as a benchmark/KPI.

## F-04 — [Source-context caution] Audit and ecosystem prescriptions

Recommendations to standards bodies, certification programs, auditors, regulators, vendors and insurers (`e0045:c06–c07`) are advocacy/policy prescriptions of the authors. They are not independently validated as current 2026 requirements.

## F-05 — [Source-context caution] «Большой взлом» is a scenario

The final section describes systemic interconnected cyber risk and argues for quantitative network models (`e0045:c07–c08`). It is not a dated forecast or guaranteed event.

**Итог:** canonical EPUB, checksum, RAG and reading state remain unchanged.
