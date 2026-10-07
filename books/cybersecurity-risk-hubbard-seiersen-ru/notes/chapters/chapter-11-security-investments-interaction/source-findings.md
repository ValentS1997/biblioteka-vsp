# Глава 11 — source findings

**Book:** `cybersecurity-risk-hubbard-seiersen-ru`. **Boundary:** EPUB spine 43–44. **Mode:** `rag_only`.

## F-01 — [Source extraction issue] Figures 11.1–11.7 are not standalone multimodal RAG objects

Confirmed textual references include:
- Fig. 11.1 — standard security data mart / time-value-risk cube (`e0043:c01–c02`);
- Fig. 11.2 — vulnerability mart (`e0044:c01`);
- Fig. 11.3 — extended mart with conformed dimensions (`e0044:c02`);
- Fig. 11.4 — malware dimension/integration (`e0044:c02`);
- Fig. 11.5 — ПУКД days-to-detection survival curve (`e0044:c04`);
- Fig. 11.6 — high-level ПУКД mart (`e0044:c04`);
- Fig. 11.7 — remediation accumulating-snapshot/workflow facts (`e0044:c05`).

Captions/prose are available, but original entities, arrows, curve points, axes and layout are not. Chapter SVG/Mermaid artifacts are conceptual summaries only.

## F-02 — [Source extraction issue] Tables 11.1–11.5 are not fully structured in RAG

Text references:
- Table 11.1 — vulnerability fact table;
- Table 11.2 — decoded vulnerability facts;
- Table 11.3 — asset dimension;
- Table 11.4 — ПУКД dimensions;
- Table 11.5 — ПУКД blocking fact.

RAG retains prose explaining semantics, but not a complete machine-readable set of rows/cells. No SQL/DDL is reconstructed.

## F-03 — [Source-boundary caution] Logical dimensional model is not a required physical schema

The source explicitly states that dimensional modeling is logical and can be virtualized; physical fact/dimension tables are not mandatory (`e0044:c01`).

Therefore chapter artifacts do not mandate star-schema tables, a specific database engine, ETL platform or cloud provider.

## F-04 — [Needs confirmation] Exact field naming / schema

The source prose explicitly contains fields such as `date_http_start_id` and `date_https_end_id` (`e0044:c04–c05`). Without original Table 11.5 layout/schema, potential naming conventions or typos cannot be adjudicated. Field names are preserved as extracted.

## F-05 — [Source-context caution] Numeric operational targets are examples

The source KPI «increase by 20% effectiveness of finding threats surviving 70+ days» belongs to the ПУКД example (`e0044:c04`). It is not adopted as a local KPI/SLA.

Similarly, statements such as historical proxy-log lookup being needed «nine times out of ten» are preserved as source exposition, not validated measurements for the user's environment.

**Итог:** canonical EPUB, checksum, RAG and reading state remain unchanged.
